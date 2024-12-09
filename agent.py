from langgraph.graph import MessagesState, START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from pydantic import BaseModel
from typing import List, Optional
from constants import questions, eval_criteria

from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

#########################
# Configuration / Setup #
#########################

APPLICANT_NAME = "Alice"
COMPANY_NAME = "Acme Corp"
ROLE = "Software Engineer"
INTERVIEW_QUESTIONS = [
    "Can you tell me about a challenging project you've worked on?",
    "What is your experience with distributed systems?",
    "How do you approach debugging complex code issues?"
]

# System prompt that defines the behavior of the agent.
SYSTEM_PROMPT = f"""
You are a friendly and professional interviewer from {COMPANY_NAME} interviewing {APPLICANT_NAME} for the role of {ROLE}.

Known interview questions:
1. {INTERVIEW_QUESTIONS[0]}
2. {INTERVIEW_QUESTIONS[1]}
3. {INTERVIEW_QUESTIONS[2]}

The user may ask clarifying questions at any time. If the user asks a question, answer it helpfully and then return to the interview flow.
If the user provides an answer to the current interview question, decide whether to ask a follow-up or move to the next question.
After all questions have been addressed, inform the user the interview is complete and invite any final comments. 
When the user is done, thank them and instruct them to end the session by clicking the "End Interview" button.

Maintain a friendly and professional tone.
"""

# Hardcoded initial AI introduction message
INITIAL_INTRO_MSG = f"Hello {APPLICANT_NAME}, welcome to the interview with {COMPANY_NAME}! I'll be asking you a few questions about your experience as a {ROLE}. Before we begin, do you have any questions for me?"

#########################
# Tools (Optional)      #
#########################

@tool
def dummy_tool(query: str):
    """A placeholder tool, not really used here."""
    return f"I processed the query: {query}"

tools = [dummy_tool]
tool_node = ToolNode(tools)


#########################
# Model and Bindings    #
#########################

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

class AskHuman(BaseModel):
    """Ask the human a question"""
    question: str

model = model.bind_tools(tools + [AskHuman])

#########################
# State and Logic       #
#########################

def interview_is_complete(state) -> bool:
    """Check if all questions have been presented at least once.
    This is a simple heuristic. In practice, track state more explicitly."""
    messages = state["messages"]
    asked_questions = 0
    for q in INTERVIEW_QUESTIONS:
        for msg in messages:
            if isinstance(msg, AIMessage) and q in msg.content:
                asked_questions += 1
                break
    return asked_questions >= len(INTERVIEW_QUESTIONS)

def call_model(state):
    """Node that calls the model."""
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state):
    """Decide what node to call next based on the last message."""
    # If the interview is complete and the user signals they are done, end.
    # If not complete, we return `ask_human` to wait for next user input.
    logger.info(f"Checking if interview should continue. State: {state}")
    if interview_is_complete(state):
        # Check if user indicated they are done.
        # For simplicity, let's just assume we present a message that the interview is complete 
        # and next user input will end it.
        # We can refine this logic later.
        logger.info("Interview is complete.")
        last_ai = [m for m in state["messages"] if isinstance(m, AIMessage)]
        if last_ai and "The interview is complete" in last_ai[-1].content:
            # We told them it's complete, next step is to let them respond one last time 
            # and then potentially end.
            # If the user's next input is empty or "thanks", we might end.
            # Since we don't have complex logic here, let's always go to "ask_human"
            # and rely on a final user input to trigger ending.
            pass
    logger.info("Continuing to ask_human")
    # Continue asking user for input until user ends the session.
    return "ask_human"

def ask_human(state):
    """Waiting node for user input."""
    logger.info("Waiting for user input at 'ask_human' node.")
    pass

#########################
# Building the Workflow #
#########################

workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)
workflow.add_node("ask_human", ask_human)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, {
    "ask_human": "ask_human",
    "end": END,
})
workflow.add_edge("ask_human", "agent")
workflow.add_edge("action", "agent")

memory = MemorySaver()
agent = workflow.compile(checkpointer=memory, interrupt_before=["ask_human"])

#########################
# Initialization        #
#########################

def initialize_conversation():
    """Initialize the conversation state with a system message and initial AI introduction."""
    system_msg = SystemMessage(content=SYSTEM_PROMPT)
    # The initial AI message is hardcoded, no model call needed.
    # This ensures that the user sees it as the first message from the agent.
    intro_ai_message = AIMessage(content=INITIAL_INTRO_MSG)

    # We'll run the workflow once with these initial messages so that the app state 
    # includes this starting point. After this, the next steps involve waiting for user input.
    # Note: We'll store these directly in state by calling app.update_state after creation.
    return [system_msg, intro_ai_message]