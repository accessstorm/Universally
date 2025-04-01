# Universally - AI Interview Platform

**Universally** is an AI-powered web platform designed to streamline test question generation and machine learning model selection. This Django application provides the full web interface and backend logic.

## Features

### 1. **AI-Powered Test Question Generator**
- Uses a **Gemini-powered bot** (via API key) to generate test questions across multiple genres directly within the web application.
- Enables efficient and diverse test creation for educational and assessment purposes.

### 2. **Smart ML Model Selector**
- Allows users to upload CSV files and automatically selects the most suitable **machine learning model** for training via the web interface.
- Utilizes **scikit-learn, pandas, and numpy** to analyze data and determine the best-fitting model.
- Simplifies the ML model selection process for users without deep ML expertise.

## Technology Stack
- **Python**
- **Django** & **Django Rest Framework** (Web framework and API toolkit)
- **Gunicorn** (Production WSGI server)
- **Whitenoise** (Static file serving in production)
- **dj-database-url** & **psycopg2-binary** (PostgreSQL database connection in production)
- **python-dotenv** (Managing environment variables locally)
- **Scikit-learn, Pandas, NumPy** (for ML model selection logic)
- **Google Generative AI SDK** (for test question generation)

## Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/universally.git # Replace with your repo URL
    cd universally
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Windows (cmd.exe)
    python -m venv .venv
    .venv\Scripts\activate

    # macOS / Linux (bash/zsh)
    # python3 -m venv .venv
    # source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    *   Create a file named `.env` in the project root directory (where `manage.py` is).
    *   Add the following variables (replace placeholders with your actual values):
        ```dotenv
        SECRET_KEY='your-strong-local-secret-key'
        DEBUG=True
        DATABASE_URL='sqlite:///db.sqlite3' # Use SQLite locally
        GOOGLE_AI_API_KEY='your-google-ai-api-key'
        ```
    *   **Important:** Do NOT commit the `.env` file to Git (it's included in `.gitignore`).

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser (optional, for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The web application will be available at `http://127.0.0.1:8000/`.

## Deployment

This project is configured for deployment to **Render** using the `render.yaml` configuration file. Render will host the entire Django application, including backend logic, template rendering, and static file serving (via Whitenoise).

Refer to the Render deployment steps outlined previously for deploying the application. Ensure you set the necessary environment variables (`GOOGLE_AI_API_KEY`) in the Render dashboard.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
