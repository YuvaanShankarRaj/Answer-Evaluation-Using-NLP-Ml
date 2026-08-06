# Answer-Evaluation-Using-NLP-Ml
Using Ml And NLP 
# AI-Based Student Answer Sheet Evaluation System

Overview

This project is an AI-powered Student Answer Sheet Evaluation System that automates the process of extracting text from uploaded answer sheets and evaluating them using Natural Language Processing (NLP) and Machine Learning techniques.

The application provides a web interface where users can upload answer sheets and receive automated evaluation results.

---

 Features

* Upload student answer sheet images
* OCR-based text extraction using Tesseract OCR
* NLP-based answer comparison
* AI-assisted evaluation
* Student evaluation dashboard
* MySQL database integration
* Web interface using Flask

---
Tech Stack

* Python
* Flask
* MySQL
* HTML
* CSS
* JavaScript
* Pandas
* Scikit-learn
* Sentence Transformers
* PyTorch
* OpenCV
* Pytesseract



## Required Python Packages

Install the required packages using:

bash
pip install flask mysql-connector-python sentence-transformers pandas scikit-learn torch opencv-python pytesseract

Additional Requirements

Install **Tesseract OCR** on your system.

After installation, configure the Tesseract executable path inside the project if required.

Example:

python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

## How to Run
Step 1

Clone the repository.

bash
git clone <repository-url>

 Step 2

Move into the project folder.

bash
cd <project-folder>

Step 3
Install all required dependencies.

bash
pip install flask mysql-connector-python sentence-transformers pandas scikit-learn torch opencv-python pytesseract


Step 4

Run the Flask application.

bash
python app.py




 Access the Application

After running the application, open your browser and visit:
text
http://127.0.0.1:5000/student


Project Structure

text
Project/
│── app.py
│── templates/
│── static/
│── uploads/
│── database/
│── README.md



## Future Enhancements

* Support PDF answer sheets
* Subject-wise evaluation
* Teacher/Admin Dashboard
* Student Login
* Performance Analytics
* AI-based feedback generation


## Author

**Yuvan Shankar Raj K.**

