## Running the Project with Docker

This project is containerized for easy setup and execution using Docker. The application is a web-based text summarizer built with Streamlit, and the Docker setup ensures all dependencies and required data are available at build time.

### Project-Specific Docker Details

- **Base Image:** `python:3.11-slim`
- **System Dependencies:** Installs libraries required for NLP (e.g., `gcc`, `build-essential`).
- **Python Dependencies:** Installed from `requirements.txt`.
- **NLTK and spaCy Data:** Downloads `punkt`, `stopwords` (NLTK), and `en_core_web_sm` (spaCy) at build time.
- **Entrypoint:** Runs the Streamlit web server (`streamlit run web_summarizer.py`).

### Environment Variables

- No additional environment variables are required by default. If you need to set any, you can use an `.env` file and uncomment the `env_file` line in `docker-compose.yml`.

### Ports

- **Port 8501 is exposed by default.**
- Access the application in your browser at: [http://localhost:8501](http://localhost:8501)

### Build and Run Instructions

1. **Build the Docker image:**
   ```sh
   docker build -f Dockerfile.web -t web-summarizer .
   ```

2. **Run the container:**
   ```sh
   docker run -it --rm -p 8501:8501 web-summarizer
   ```

3. **Use the web app:**
   - Open your browser and go to [http://localhost:8501](http://localhost:8501)
   - Upload a text file or paste text, select your summarization method from the sidebar, and click "Summarize".

### Special Configuration

- **No persistent volumes or custom networks are required.**
- All required data and models are downloaded at build time.
- If you need to pass environment variables, create a `.env` file and uncomment the `env_file` line in `docker-compose.yml`.

---

_Refer to the Dockerfile and docker-compose.yml for further customization as needed for your environment._
