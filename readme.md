This is the readme of the third exercise of Group 1 of the course Smart Data Analytics.
Tobias Biegert, Suleiman Elkhoury, Moritz Diener
1. Download the project
```
git clone https://git.scc.kit.edu/uzlsf/smartdataeins
cd smartdataeins
```
2. Install the dependencies
```
pip install -r requirements.txt
```
3. Insert OpenAI-API Key:
```
Insert your OpenAI Key in the app.py
openai.api_key ="Your_Key"
```
4. Run it
```
python app.py
```

####### Project Files #######
app.py contains chatgpt required functions and the Gradio UI

functions.py contains all the prompts and pipelines for the exercises

kittheme.py contains a theme imported by the Gradio UI with the colors of the karlsruher institut für technologie

requirements.txt contains the dependencies used 


#######Explaination of the User Interface########
Model:
In the top right corner you can select your preferred ChatGPT model via a dropdown menu. Standard setting is the gpt-3.5-turbo. 

Important Information Representation:
-In this tab you can input a dataset description and get as an output a structured and standardized JSON format of the important information.

Related Work Listing 
-You can enter a paper name and select with "count" how many related work you want to get displayed. 
-The button "Pure GPT" gives relevant related papers that are recommended by ChatGPT.
-With "Get Citations With Scholarly" you get papers that cite the one inputted.
-"Get References With Plybliometrics" outputs the papers which are referenced in the input paper. (A key is needed for pybliometrics.cfg.) 

Tools and Algorithm Recommendations 
-Gives several suggested algorithms as an output.

Data Exploration
-In this tab you can upload a .txt file from the Human Activity Recognition dataset. Via "count" the number of rows used for Data Exploration can be changed.
-"Data Visualization Prompt" gives code that can be run to visualize the data.
-"Descriptive Statistics Prompt" gives out a statistical analysis of the input data.

Data Format Transformation
-Transform input data into a structured format. 
