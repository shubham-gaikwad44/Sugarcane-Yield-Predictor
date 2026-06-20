# 🌾 Sugarcane Yield Advisor

Welcome to the **Sugarcane Yield Advisor**! This project provides a machine learning-powered web application designed to help farmers, agricultural planners, and enthusiasts estimate sugarcane yields based on a variety of environmental and farming factors. 

Using data like the field's area, soil type, irrigation method, and climate conditions, our tool gives you a quick and data-driven estimate of the expected harvest.

---

## 🌟 Features
- **Interactive UI**: A beautiful, user-friendly dashboard built with [Streamlit](https://streamlit.io/).
- **Smart Predictions**: Powered by a trained Machine Learning model to provide accurate yield estimates (in tons/acre).
- **Data-Driven Insights**: Validates your inputs against known, realistic agricultural ranges and provides helpful "reference value" suggestions.
- **Easy Customization**: Built with a modular structure so you can easily swap out models or update feature constraints.

---

## 🛠️ Project Structure
```text
AI_Sugarcane_advisor/
│
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
│
├── data/
│   └── raw/                    # Raw datasets used for training
│
├── eda_reports/                # Exploratory Data Analysis (EDA) visualizations
│
├── models/
│   └── yield_model.pkl         # Trained Machine Learning pipeline
│
└── src/                        # Core source code
    ├── feature_options.py      # Configuration for input fields and validation
    ├── yield_prediction.py     # Prediction logic and CLI interface
    ├── data_processing/        # Scripts for cleaning and generating data
    └── model_training/         # Scripts for training the ML model
```

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### 1. Prerequisites
Make sure you have Python 3.8+ installed on your computer.

### 2. Installation
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/AI_Sugarcane_advisor.git
cd AI_Sugarcane_advisor
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Running the App
To start the web dashboard, simply run the following command in your terminal (make sure you are in the root directory of the project):
```bash
streamlit run app.py
```

The app will automatically open in your default web browser!

---

## 👨‍💻 How it Works

The prediction engine relies on a pre-trained model (`models/yield_model.pkl`). The model evaluates the following inputs:
- **Location**: State
- **Field Details**: Area (acres), Soil Type, Irrigation Type
- **Climate & Crop**: Rainfall (mm), Temperature (°C), Crop Age (months), Fertilizer Used (kg)

If you'd like to use the tool purely via the command line instead of the web UI, you can also run:
```bash
python src/yield_prediction.py
```

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License
This project is open source and available under the [MIT License](LICENSE).
