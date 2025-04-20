## Running the Project with Docker

This project is containerized for easy setup and execution using Docker. The application is a PyQt5-based GUI text summarizer, and the Docker setup ensures all dependencies and required data are available at build time.

### Project-Specific Docker Details

- **Base Image:** `python:3.11-slim`
- **System Dependencies:** Installs libraries required for PyQt5 and X11 GUI support (e.g., `libxkbcommon-x11-0`, `libxcb-xinerama0`, `libgl1-mesa-glx`, etc.).
- **Python Dependencies:** Installed from `requirements.txt` inside a virtual environment (`.venv`).
- **NLTK and spaCy Data:** Downloads `punkt`, `stopwords` (NLTK), and `en_core_web_sm` (spaCy) at build time.
- **User:** Runs as a non-root user (`appuser`).
- **Entrypoint:** Runs `python text_summarizer.py` by default.

### Environment Variables

- `QT_X11_NO_MITSHM=1` is set to improve Qt/X11 compatibility in containers.
- No additional environment variables are required by default. If you need to set any, you can use an `.env` file and uncomment the `env_file` line in `docker-compose.yml`.

### Ports

- **No ports are exposed by default.**
- This is a GUI application. To display the GUI on your host, you may need to configure X11 forwarding or use a VNC setup. No web or API ports are published.

### Build and Run Instructions

1. **Build and start the container:**
   ```sh
   docker compose up --build
   ```
   This will build the image and start the application using the settings in `docker-compose.yml`.

2. **Display the GUI:**
   - To run the PyQt5 GUI on your host, you may need to enable X11 forwarding. For example, on Linux:
     ```sh
     xhost +local:docker
     docker compose up --build
     ```
   - On Windows or macOS, consider using a VNC server or X11 server (like XQuartz) and configure the container accordingly.

### Special Configuration

- **No persistent volumes or custom networks are required.**
- All required data and models are downloaded at build time.
- If you need to pass environment variables, create a `.env` file and uncomment the `env_file` line in `docker-compose.yml`.

---

_Refer to the Dockerfile and docker-compose.yml for further customization as needed for your environment._
