# Web-based CHATGPT-powered Prompt for Human Activity Recognition (HAR)

## Project Overview

This repository contains a web-based application designed to leverage ChatGPT for Human Activity Recognition (HAR) tasks. Follow the instructions below to set up and run the project.

## Getting Started

### 1. Clone the Repository
```bash
git clone https://git.scc.kit.edu/chat-gpt-har](https://github.com/suleimanelkhoury/chat-gpt-har.git
cd chat-gpt-har
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure OpenAI API Key
Open `app.py` and insert your OpenAI API key:
```python
openai.api_key = "Your_Key"
```

### 4. Run the Application
```bash
python app.py
```

## Project Structure

- **app.py**: Contains the ChatGPT integration and the Gradio-based user interface.
- **functions.py**: Includes all prompts and processing pipelines for the HAR exercises.
- **kittheme.py**: Provides a custom theme for the Gradio UI, using the Karlsruhe Institute of Technology color scheme.
- **requirements.txt**: Lists all dependencies required for the project.

## User Interface Guide

### Model Selection
- **Location**: Top-right corner.
- **Description**: Choose your preferred ChatGPT model from a dropdown menu. The default setting is GPT-3.5-turbo.

### Important Information Representation
- **Function**: Input a dataset description to receive a structured and standardized JSON output of the key information.

### Related Work Listing
- **Function**: Enter a paper title and specify the number of related works to display using the "count" option.
  - **"Pure GPT" Button**: Displays relevant related papers recommended by ChatGPT.
  - **"Get Citations With Scholarly" Button**: Shows papers that cite the entered paper.
  - **"Get References With Plybliometrics" Button**: Outputs references from the entered paper (requires a key in `pybliometrics.cfg`).

### Tools and Algorithm Recommendations
- **Function**: Provides recommended algorithms based on the input.

### Data Exploration
- **Function**: Upload a `.txt` file from the Human Activity Recognition dataset.
  - **"count" Option**: Adjust the number of rows used for data exploration.
  - **"Data Visualization Prompt" Button**: Generates code for visualizing the data.
  - **"Descriptive Statistics Prompt" Button**: Outputs a statistical analysis of the input data.

### Data Format Transformation
- **Function**: Transforms input data into a structured format.
