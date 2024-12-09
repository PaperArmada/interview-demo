from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from langchain_core.messages import HumanMessage, ToolMessage
from agent import agent, initialize_conversation

# We'll store session configuration in a simple dict for demo purposes
session_states = {}

app_api = FastAPI()

class StartSessionResponse(BaseModel):
    session_id: str
    message: str

class RespondRequest(BaseModel):
    session_id: str
    user_message: str

class RespondResponse(BaseModel):
    message: str

class EndSessionRequest(BaseModel):
    session_id: str

@app_api.post("/start_session", response_model=StartSessionResponse)
def start_session():
    session_id = str(uuid.uuid4())
    initial_messages = initialize_conversation()

    # We create a new state in the langgraph app
    config = {"configurable": {"thread_id": session_id}}
    # Update state with initial messages
    agent.update_state(config, {"messages": [m.dict() for m in initial_messages]}, as_node="agent")

    # The last message should be the introduction from AI
    state = agent.get_state(config)
    last_ai_message = state.values["messages"][-1].content

    session_states[session_id] = {}
    return StartSessionResponse(session_id=session_id, message=last_ai_message)

@app_api.post("/respond", response_model=RespondResponse)
def respond(req: RespondRequest):
    session_id = req.session_id
    user_message = req.user_message

    config = {"configurable": {"thread_id": session_id}}
    # Retrieve the current state
    state_before = agent.get_state(config)
    state_before = state_before.values
    tool_call_id = None

    # Safely check for `tool_calls` only if the last message is an AI message
    if state_before["messages"]:
        last_message = state_before["messages"][-1]
        if isinstance(last_message, ToolMessage) or hasattr(last_message, 'tool_calls'):
            tool_call_id = last_message.tool_calls[0]["id"] if last_message.tool_calls else None

    if tool_call_id:
        # User response as tool output
        tool_message = [{"tool_call_id": tool_call_id, "type": "tool", "content": user_message}]
        agent.update_state(config, {"messages": tool_message}, as_node="ask_human")
    else:
        # Treat user input as a HumanMessage
        human_msg = HumanMessage(content=user_message)
        agent.update_state(config, {"messages": [human_msg]}, as_node="ask_human")

    # Continue the workflow to generate AI response
    result = agent.invoke(None, config)
    return RespondResponse(message=result["messages"][-1].content)


@app_api.post("/end_session")
def end_session(req: EndSessionRequest):
    # Clear out the session if needed
    session_states.pop(req.session_id, None)
    return {"status": "session_ended"}
