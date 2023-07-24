from scholarly import scholarly
from pybliometrics.scopus import AbstractRetrieval
import openai
import textwrap
import json
import logging
import requests
from urllib import parse
import io
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import os
# Get related papers using just a ChatGPT prompt
def related_papers(paper_name,k):
    return f"""
                        "Generate a JSON list of {k} influential scientific papers related to the paper with the title delimited by ''' along with their authors, 
                        publication (journal/conference/etc.), year of publication and a short description of why the paper is relevant. The desired JSON format should be similar to the following example:
                        
                        {{
                          "papers": [
                            {{
                              "title": "On the Electrodynamics of Moving Bodies",
                              "author": "Albert Einstein",
                              "publication": "Annalen der Physik",
                              "pub_year": 1905,
                              "description": ""On the Electrodynamics of Moving Bodies" is a seminal paper by Albert Einstein that introduced the 
                              special theory of relativity, revolutionizing our understanding of space, time, and motion. It challenges conventional 
                              notions by demonstrating that the laws of physics remain consistent for all observers in inertial frames of reference. 
                              This paper's significance lies in its foundational role in modern physics and its relevance to a wide range of scientific disciplines."
                            }},
                            ...
                            ]
                        }}
                        
                        The paper in question has the title: '''{paper_name}'''.
                        
                        Before providing the list, start with a caution statement about your limitations and potential shortcomings due to your training data and knowledge cut-off. 
                        Also mention that some of your information might be incorrect. This statement should be a concise text."
                        """

# Get related papers using a ChatGPT prompt and the results from scholarly
def related_papers_with_scholarly(paper_name,k):
    ref = get_citations(paper_name)
    return f"""
                        Delimited by <> is a list of papers that were used as references in the paper '{paper_name}'. The sequence of the papers in the provided list 
                        does not necessarily indicate their relevance. As my research assistant, I would like you to evaluate the significance of each of the 
                        provided papers and identify the top {k} most important ones. To do this I want you to first give an 'importance score' between 0 and 10 to each paper listed. 
                        Then use the {k} papers with the highest score. Additionally, give a description of these papers consisting of at most 100 words, 
                        highlighting their relevance as references for the current research.
                        Please provide me with the list of those papers in a JSON format that should follow this example:
                        
                        {{
                        "most relevant references": [
                        {{
                          "title": "Example Paper Title",
                          "authors": "Example Authors",
                          "publication": "Example",
                          "pub_year": Example Year,
                          "importance_score": example score,
                          "description": "example description"
                        }},
                        ...
                        ]
                        }}.
                        
                        List of references:
                        <{ref}>
                        """

# Get related papers using a ChatGPT prompt and the results from pybliometrics
def related_papers_with_pybliometrics(paper_name,k):
    ref = get_referenced_papers(paper_name)
    return f"""
                        Delimited by <> is a list of papers that were used as references in the paper '{paper_name}'. The sequence of the papers in the provided list 
                        does not necessarily indicate their relevance. As my research assistant, I would like you to evaluate the significance of each of the 
                        provided papers and identify the top {k} most important ones. To do this I want you to first give an 'importance score' between 0 and 10 to each paper listed. 
                        Then use the {k} papers with the highest score. Additionally, give a description of these papers consisting of at most 100 words, 
                        highlighting their relevance as references for the current research.
                        Please provide me with the list of those papers in a JSON format that should follow this example:
                        
                        {{
                        "most relevant references": [
                        {{
                          "title": "Example Paper Title",
                          "authors": "Example Authors",
                          "publication": "Example",
                          "pub_year": Example Year,
                          "importance_score": example score,
                          "description": "example description"
                        }},
                        ...
                        ]
                        }}.
                        
                        List of references:
                        <{ref}>
                        """
# Get the papers that cited this publication. In the case of a dataset this should mainly be papers that use the dataset.
def get_citations(paper_name):
    try:
        # Get publication object from title
        pub = scholarly.search_single_pub(paper_name)

        # Which papers cited that publication?
        citations = [{
                       'title': citation['bib'].get('title'),
                       'author': citation['bib'].get('author'),
                       'year': citation['bib'].get('pub_year')
                     }
                     for citation in scholarly.citedby(pub)]

        return citations

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

#paper_name = "Transition-Aware Human Activity Recognition Using Smartphones"
#citations = get_citations(paper_name)
#print(citations)

# Get the papers that were referenced in the dataset paper. These are influential papers for the creation of the dataset
def get_referenced_papers(title):
    title = parse.quote(title)
    url = f"https://api.crossref.org/works?query.title={title}"

    response = requests.get(url)
    data = response.json()

    if data['message']['items']:
        doi = data['message']['items'][0]['DOI']
    else:
        doi = "no results found"
        return doi
    references = AbstractRetrieval(doi, view='FULL').references
    ref = [{
        'title': reference.title,
        'author': reference.authors,
        'year': reference.publicationyear
      }
      for reference in references]
    return ref

#print(get_referenced_papers('Basic Economics'))

def algorithm_recommendation(decription,k):
    return f"""
                        Given the following dataset description for data in a Human Activity Recognition Context delimited by ''':
                        ''' 
                        {decription} 
                        '''
                        Recommend relevant  algorithms  available for researchers to analyze the dataset, display the first {k} results.
                        Calculate the relevance of the algorithm depending on the relevance for the given dataset.
                        the relevance has a scale of 1 to 10.
                        Provide the information in JSON format with the following keys: 
                        algorithm_id, title, description, relevance, documentation_link.
                        """
def data_exploration(description,head):
    return f"""
                        in a Human Activity Recognition Context, Given the following description for a dataset delimited by ''':
                        ''' 
                        {description} 
                        '''
                        and the first 5 rows of the segment s01 performed by the subject p01 for the activity a01 delimited by < >:
                        <
                        {head}
                        >
                        knowing that the data are stored in s01 variable as a string, and using sensor names from the description,
                        perform simple data exploration on the sample data, and plot the results for every unit in a plot
                        """

def descriptive_statistics(description,head):
    return f"""
                        in a Human Activity Recognition Context, Given the following description for a dataset delimited by ''':
                        ''' 
                        {description} 
                        '''
                        and the first 5 rows of the segment s01 performed by the subject p01 for the activity a01 delimited by < >:
                        <
                        {head}
                        >
                        knowing that the data are stored in s01 variable as a string, and using sensor names from the description,
                        perform descriptive statistics on the sample data, and plot all the statistics for every sensor in one plot. output one python code
                        """
#return the frist n lines of string
def read_n (file,n):
    head = '\n'.join(file.decode('utf-8').splitlines()[-n:])
    return head

# define what choices does chatGPT suggests

# small function for openai response (not so flexible like in our main)
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
def data_exploration_choice(description,sample,sample_description,k):
    prompt = f"""
    in a Human Activity Recognition Context, Given the following description for a dataset delimited by ''':
    ''' 
    {description} 
    '''
    and the first {k} lines of {sample_description} delimited by < >:
    <
    {sample}
    >
    suggest a couple of data exploration methods that are suitable for the data given above.
    Provide the information in one JSON file with only the method name
    """
    response = get_completion(prompt)
    # take the data exploration methods
    response_json = json.loads(response)
    response_values = []
    for key, value in response_json.items():
            response_values+= value
    return response_values

# perform the defined method on the description and sample given
def data_exploration_apply(description,sample,sample_description,method,k):
    prompt = f"""
    in a Human Activity Recognition Context, Given the following description for a dataset delimited by ''':
    ''' 
    {description} 
    '''
    and the first {k} lines of {sample_description} delimited by < >:
    <
    {sample}
    >
    knowing that the data are stored in s01 variable as a string, and using sensor names from the description, 
    """
    if method == 'Descriptive statistics':
        prompt = prompt + "perform descriptive statistics on the sample data, and plot all the statistics for every sensor in one plot. output one python code"
    elif method == 'Data visualization':
        prompt = prompt + "perform simple data exploration on the sample data, and plot the results for every unit in a plot"
    response = get_completion(prompt)
    return response

# define the whole data exploration pipeline
def data_exploration_pipeline(history,description,sample,sample_description,k):
    values = data_exploration_choice(description,sample,sample_description,k)
    for i in range(len(values)):
        logging.info('Data exploration choice number ' + str(i+1) + ': ' + values[i])
        message = "#Data exploration choice number " + str(i+1) + ": " + values[i] + "\n"
        output = data_exploration_apply(description,sample,sample_description,values[i],k)
        logging.info(output[output.rfind("```python"):output.rfind("```")-3])
        message = message + output[output.rfind("```python"):output.rfind("```")-3] +"\n"
        history = history + [(message, None)]
    return history

# includes all the prompts in a sequence as a pipeline
# the first prompts are used to tell ChatGPT the context that its an assistant helping a scientific researcher in the context of Human Activity Recognition (HAR).
# The prompt takes a description of a HAR dataset as an input. This can be a copy of the description found on a website
# The prompt gives a structured format in which the information found in the HAR description needs to be displayed as well as the required format in JSON.
def important_information_pipeline(description):
    context =  [
                    {'role':'system', 'content':'You are an assistant helping a scientific researcher in the context of Human Activity Recognition. The researcher wants help\
                     with quicker undestanding datasets of human activities. The researcher can give meta input like sensors, column names, features, attributes and \
                     needs a summary in JSON format for all the meta information about the dataset. The researcher furhter needs recommendations on how to handle\
                     the data, the steps for data preprocessing, processing algorithms etc.'},
                    {'role':'assistant', 'content':'Of course! How can I help you with your scientific research in Human Activity Recognition?'},
                    {'role':'user', 'content':'Help me with understanding a Human Activity Recognition Dataset. Ask me about the specifics\
                      of a Human Recognition Dataset so you can understand the overall structure of the dataset. After this give me the \
                      results of the structure of the dataset as a table.'},
                    { 'role':'user', 'content': f"""
                      Your task is to extract relevant information and generate a summary of a description \
                      of a human activity recognition dataset delimited by **. \
                      For the format of the summary use the generic one below delimited by ``````.\
                      Insert the relevant information where there are "".
                     
                      Human Actvity Dataset: *{description}*
                       
                    
                      ```
                      Brief Description of the Dataset:
                      ---------------------------------
                      "Insert brief description of the Dataset"
                    
                      Subjects:
                      ----------
                      The dataset includes data from a total of "" subjects. "Description of the subjects"
                    
                      Activities:
                      -----------
                      There are a total of "" activities performed by the subjects. Each activity is labeled with a specific code or name. "Description of activities"
                    
                      Sensors:
                      --------
                      "Describtions of Sensors"
                    
                      Data Structure:
                      ---------------
                      "Describe the Data Structure"
                    
                      Summary of Dataset Structure:
                      -----------------------------
                      The following table summarizes the structure of the Human Activity Recognition dataset:
                    
                      | Attribute   | Description                                                                 |
                      |-------------|-----------------------------------------------------------------------------|
                      | Subjects    | "" subjects                                                                 |
                      | Activities  | "" activities                                                               |
                      | Sensors     | "" sensors                                                                  |
                      | Sampling Rate | ""
                      | Instances   | ""                                                                          |
                      | Attributes  | ""                                                                          |
                      | Data Format | ""                                                                          |
                      | Folder Structure | ""                                                                     |
                      | Column Structure | ""                                                                     |
                    
                      ```
                      Description: {description}
                      """},
                    {'role':'user', 'content':'Take the your output of the previous task display it again and then put it in a JSON format. The format should include \
                     Brief Description of the Dataset,\
                     Brief Description of Subjects,\
                     Brief Description of Activities,\
                     Brief Description of Sensors,\
                     Brief Description of Data Structure,\
                     Summary of Dataset Structure,\
                     A table with subjects, activities, sensors, sampling rate, instances, attributes, data format, folder structure, column structure.\
                     Add any additional important information that can be found in the description of the Dataset.'},
                ]
    message = get_completion_chat(context, model="gpt-3.5-turbo")
    return [(message, None)]
def execute(text):
    exec(text)
    return plt

def get_completion_chat(prompt, model):
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# Define the data transformation function
def transform_to_fixed_format(root_path):
    file_list = os.listdir(root_path)
    df_dict = {}
    sub_ids_of_each_sub = {}

    for file in file_list:
        sub_data = pd.read_table(os.path.join(root_path, file), header=None, delim_whitespace=True)
        sub_data = sub_data.iloc[:, 1:11]  # Selecting the relevant columns
        sub_data.columns = ["acc_x_ankle", "acc_y_ankle", "acc_z_ankle",
                            "acc_x_leg", "acc_y_leg", "acc_z_leg",
                            "acc_x_trunk", "acc_y_trunk", "acc_z_trunk",
                            "activity_id"]

        sub_id = file.split(".")[0]  # Extracting the sub_id from the file name
        sub_data["sub_id"] = sub_id
        sub_data["sub"] = int(sub_id.split("S")[1].split("R")[0])

        if sub_data["sub"][0] not in sub_ids_of_each_sub.keys():
            sub_ids_of_each_sub[sub_data["sub"][0]] = []
        sub_ids_of_each_sub[sub_data["sub"][0]].append(sub_id)

        df_dict[sub_id] = sub_data

    df_all = pd.concat(df_dict.values())
    df_all = df_all.set_index('sub_id')

    return df_all

def data_format_transformation(description,head):
    return  f"""
Given the following dataset description for data in a Human Activity Recognition Context delimited by ''':
''' 
{description} 
'''
Use the information from this description, as well as the first 5 rows of the data delimited by <>:
<
{head}
>

The format should look like this:
<Sub_id | Sensor_1 | Sensor_2 | ... | Sensor_n | Activity_ID
1 | 0.93 | 0.88 | ... | 2.33 | 0 
... | ... | ... | ... | ... | ... > 

Columns in the .txt file are separated by an empty space. Each sensor is in a separate column. 
These columns do not have headers. 
The column names have to be inferred from the dataset description. 
If there are additional columns in the .txt file you can also include them in the format if you know what the column name should be.
You need to infer the sub_id from the title of the file which will typically be in the format <sub_id.txt>.
The title of this file is {'S01R01.txt'}. Make the sub_id the index of the dataframe.

Your answer should only consist of a table with the previous specifications

"""

def data_format_transformation2(description):
    return  f"""
Given the following dataset description for data in a Human Activity Recognition Context delimited by ''':
''' 
{description} 
'''
Use the information from this description as well as a .txt file that contains the data to generate python code that produces a fixed format dataframe.

The format should look like this:
<Sub_id | Sensor_1 | Sensor_2 | ... | Sensor_n | Activity_ID
1 | 0.93 | 0.88 | ... | 2.33 | 0 
... | ... | ... | ... | ... | ... > 

Columns in the .txt file are separated by an empty space. Each sensor is in a separate column. 
These columns do not have headers. 
The column names have to be inferred from the dataset description. 
If there are additional columns in the .txt file you can also include them in the format if you know what the column name should be.
You need to infer the sub_id from the title of the file which will typically be in the format <sub_id.txt>.
The title of this file is {'S01R01.txt'}. Make the sub_id the index of the dataframe.

Your answer should only consist of the code with comments.

"""
