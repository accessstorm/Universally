# Universally

**Universally** is an AI-powered platform designed to streamline test question generation and machine learning model selection. It provides automated tools to assist users in generating test questions across different genres and intelligently selecting the best machine learning model for training CSV data.

## Features

### 1. **AI-Powered Test Question Generator**
- Uses a **Gemini-powered bot** to generate test questions across multiple genres.
- Enables efficient and diverse test creation for educational and assessment purposes.

### 2. **Smart ML Model Selector**
- Automatically selects the most suitable **machine learning model** for CSV file training.
- Utilizes **scikit-learn, pandas, and numpy** to analyze data and determine the best-fitting model.
- Simplifies the ML model selection process for users without deep ML expertise.

## Technology Stack
- **Python** (for ML model selection)
- **Scikit-learn** (for ML training and evaluation)
- **Pandas & NumPy** (for data processing and analysis)
- **Gemini AI** (for test question generation)

## Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/universally.git
cd universally

# Install dependencies
pip install -r requirements.txt
```

## Usage
### Running the Test Question Generator
```python
from universally.test_generator import generate_questions
questions = generate_questions(topic="Machine Learning", difficulty="Intermediate")
print(questions)
```

### Using the Smart ML Model Selector
```python
from universally.ml_model_selector import select_best_model
best_model = select_best_model("data.csv")
print("Selected Model:", best_model)
```

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
