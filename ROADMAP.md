# ROADMAP.md

## Project Direction

Tech Knowledge Base is a personal local AI knowledge assistant.

The project will be built incrementally.
Each version should remain runnable before moving to the next version.

## v0.1 - Project Foundation

Goal: Create a minimal runnable web application.

- Create project structure
- Create Python virtual environment
- Add FastAPI backend
- Add basic HTML / CSS / JavaScript frontend
- Create homepage
- Add question input field
- Add submit button
- Add `knowledge/` directory
- Add `.gitignore`
- Add `requirements.txt`

Success criteria:

- FastAPI server can start successfully
- Homepage can be opened in the browser
- User can type a question into the UI

## v0.2 - Ollama Integration

Goal: Connect the application to the local Ollama service.

- Send prompts from FastAPI to Ollama
- Receive model responses
- Display responses in the web UI
- Add basic error handling when Ollama is unavailable

Success criteria:

- User enters a question
- Local Ollama generates a response
- Response appears in the browser

## v0.3 - Local Knowledge

Goal: Allow the application to read personal technical notes.

- Read Markdown files from `knowledge/`
- Add sample knowledge files
- Search for relevant content using a simple approach
- Pass relevant knowledge to Ollama as context

Success criteria:

- The system can answer using information stored in local Markdown files

## v0.4 - Source Display

Goal: Make answers traceable.

- Track which knowledge files were used
- Display source filenames with the answer
- Improve the response format

Success criteria:

- User can see where the answer came from

## v0.5 - Demo Polish

Goal: Prepare a clean MVP suitable for demonstration.

- Improve UI readability
- Improve loading and error states
- Add several useful technical knowledge notes
- Clean project structure
- Update README
- Test the full workflow

Success criteria:

Question
→ Knowledge retrieval
→ Ollama
→ Answer
→ Sources

works reliably from end to end.

## Future Ideas

These are not part of the current MVP:

- Vector database
- Semantic embeddings
- Conversation history
- Knowledge management UI
- Automatic note importing
- Tagging / categories
- Multiple Ollama models
- Cloud deployment
- User accounts
