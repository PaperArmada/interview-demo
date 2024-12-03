-- PostgreSQL script to create the initial database schema for the AI Interviewer MVP project

-- Create a new database
CREATE DATABASE ai_interviewer;

-- Connect to the newly created database
\connect ai_interviewer;

-- Create User table to store candidate information
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Company table to store information about companies
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    industry VARCHAR(100),
    address VARCHAR(255),
    contact_info VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create JobPosting table to store information about specific job postings
CREATE TABLE job_postings (
    job_id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(company_id),
    job_title VARCHAR(150) NOT NULL,
    job_description TEXT,
    skills_required TEXT,
    questions TEXT,
    revision_number INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Case table to link users to job postings and store interview session information
CREATE TABLE cases (
    case_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    job_id INT REFERENCES job_postings(job_id),
    resume TEXT,  -- This could be a path to a resume file or the resume content itself
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create InterviewSession table to store information about interview sessions
CREATE TABLE interview_sessions (
    session_id SERIAL PRIMARY KEY,
    case_id INT REFERENCES cases(case_id),
    current_state VARCHAR(50),
    conversation_history TEXT,  -- JSON or plain text to store Q&A history
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert mock data for testing purposes
INSERT INTO companies (company_name, industry, address, contact_info) VALUES
('Tech Corp', 'Software Development', '123 Tech Street, Tech City', 'info@techcorp.com');

INSERT INTO job_postings (company_id, job_title, job_description, skills_required, questions, revision_number) VALUES
(1, 'Software Engineer', 'Develop and maintain software solutions.', 'Python, SQL, REST APIs', '[{"question": "What is your experience with Python?"}, {"question": "Describe a challenging project you worked on."}]', 1);

INSERT INTO users (name, email) VALUES
('John Doe', 'john.doe@example.com');

INSERT INTO cases (user_id, job_id, resume) VALUES
(1, 1, 'Path/to/resume_john_doe.pdf');