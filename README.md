# AI Interviewer Application

## Repository Overview

This repository contains the codebase for an AI-powered interview assistant designed to conduct structured interviews, evaluate candidate responses, and provide insights for further analysis. The project is modular, with distinct components for handling interview logic, backend APIs, a Streamlit-based frontend, and tools for testing and evaluation.

---

## Project Components

### 1. **`frontend_app.py`**
- **Purpose**: Provides the user interface for conducting AI-assisted interviews.
- **Technology**: Built with [Streamlit](https://streamlit.io/).
- **Features**:
  - Starts a new interview session.
  - Displays interview questions and captures responses.
  - Enables submission of responses and ends sessions.
- **How to Use**: Run the frontend with:
  ```bash
  streamlit run frontend_app.py
  ```

### 2. **`backend_app.py`**
- **Purpose**: Acts as the server backend for managing interview sessions and AI interactions.
- **Technology**: Built with [FastAPI](https://fastapi.tiangolo.com/).
- **Endpoints**:
  - `/start_session`: Initializes a new session and returns the first question.
  - `/respond`: Processes user responses and provides follow-up questions or prompts.
  - `/end_session`: Ends the session and triggers any analyses.
- **How to Use**: Start the backend server with:
  ```bash
  uvicorn backend_app:app_api --reload
  ```

### 3. **`agent.py`**
- **Purpose**: Implements the interview flow and manages the AI's logic.
- **Key Responsibilities**:
  - Tracks session state, including questions asked and responses given.
  - Uses evaluation criteria defined in `constants.py` for assessing responses.
  - Powers AI interactions, leveraging tools and workflows for seamless session management.

### 4. **`constants.py`**
- **Purpose**: Provides static configuration data for the application. Intended for future iterations.
- **Contents**:
  - Question bank organized by categories (behavioral, situational, technical, cultural fit).
  - Evaluation criteria mapped to competencies such as problem-solving, technical expertise, and adaptability.

### 5. **`response_viewer.py`**
- **Purpose**: A helper tool to make things easier when testing out the application manually.
- **Features**:
  - Upload mock candidate response JSON files for evaluation.
  - Navigate responses with an interactive interface.
  - Copy individual responses for easy input into the UI.
- **How to Use**: Run the response viewer with:
  ```bash
  streamlit run response_viewer.py
  ```

---

## Repository Structure

```
.
├── agent.py                # Core interview logic and session management
├── backend_app.py          # Backend API for interview operations
├── constants.py            # Static questions and evaluation criteria
├── frontend_app.py         # Streamlit-based interview frontend
├── response_viewer.py      # Response navigator for testing mock candidates
├── mock_candidates/        # Example resumes and responses for testing
├── requirements.txt        # Python dependencies
└── README.md               # Repository info
```

---

## Getting Started

### Prerequisites
- Python 3.9+
- `pip` or `conda` for package management.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add necessary configurations (e.g., OpenAI API key):
     ```
     OPENAI_API_KEY=<your_api_key>
     ```

---

## Usage

### Backend
Start the FastAPI backend:
```bash
uvicorn backend_app:app_api --reload
```
Default URL: `http://localhost:8000`

### Frontend
Launch the Streamlit interview frontend:
```bash
streamlit run frontend_app.py
```
Default URL: `http://localhost:8501`

### Response Viewer
Run the response viewer:
```bash
streamlit run response_viewer.py
```
This tool can access files from the `mock_candidates/` directory for easier testing (future state).

---

## Future Plans

- **Session Analysis**:
  - Automate post-interview evaluations based on competency criteria.
  - Generate structured feedback reports for candidate performance.

- **Enhanced State Management**:
  - Dynamically track the mapping between responses and questions.
  - Improve handling of clarifying questions and off-topic responses.

- **Expanded Evaluation Criteria**:
  - Add support for weighted scoring and nuanced assessments.

- **Integration Capabilities**:
  - Multi-agent systems to automatically generate questions / eval criteria based on job posting and company.
  - Support exporting interview data in standardized formats (e.g., JSON, CSV).

- **Visualization**:
  - Create dashboards to visualize candidate strengths and improvement areas.

---

## Exploring and Tinkering

- **Mock Candidates**:
  - Explore the `mock_candidates/` folder to find test resumes and sample responses.
  - Use the `response_viewer.py` app to quickly access answers to feed into the main application.

- **Constants**:
  - Adjust `constants.py` to add, modify, or categorize questions and scoring criteria.

- **Agent Logic**:
  - Tinker with `agent.py` to customize the interview flow, AI interactions, or evaluation rules.

---

Feel free to explore, experiment, and adapt this project to your specific needs. Let me know if you'd like clarification or additional features documented!
