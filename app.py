import os
import openai
import gradio as gr
import kittheme as kit
import logging
import base64
# add your openai key here
openai.api_key = ""

# String variables to use throughout the code
title_html = """<h1><center>CHATGPT-based  Prompt  for  Human  Activity  Recognition  (HAR) </center></h1>"""
description = """<p><center>The following code extracts and analyzes information from Human Activity Recognition (HAR) datasets</center></p>"""
pybliometrics ="""<p><center>Key needed for pybliometrics.cfg</b></center></p>"""
code_area = """<p><center>Execute Code Area</b></center></p>"""
system_message = {"role": "system", "content": "You are a helpful assistant."}

# Chatgpt models (can be switched during runtime)
available_models = ["gpt-3.5-turbo-16k", "gpt-3.5-turbo", "gpt-3.5-turbo-0613","gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"]

# logging
os.makedirs("gpt_log", exist_ok=True)
try:
    logging.basicConfig(filename="gpt_log/chat_secrets.log", level=logging.INFO, encoding="utf-8")
except:
    logging.basicConfig(filename="gpt_log/chat_secrets.log", level=logging.INFO)
print("All query records will be automatically saved in the local directory./gpt_log/chat_secrets.log")

# Import functional prompts
from functions import related_papers, related_papers_with_scholarly, related_papers_with_pybliometrics, algorithm_recommendation\
    , data_exploration, descriptive_statistics, read_n, data_exploration_pipeline, important_information_pipeline, data_format_transformation, execute

# updates user message
def user(user_message, history):
    return "", history + [[user_message, None]]


# updates the message history as the conversation progresses
def bot(history, messages_history, model):
    user_message = history[-1][0]
    bot_message, messages_history = ask_gpt(user_message, messages_history, model)
    messages_history += [{"role": "assistant", "content": bot_message}]
    history[-1][1] = bot_message
    print("history: ", history, "messages_history: ", messages_history)
    return history, messages_history

# queries from chatgpt for an answer
def ask_gpt(message, messages_history, model):
    messages_history += [{"role": "user", "content": message}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages_history,
        temperature=0
    )
    return response['choices'][0]['message']['content'], messages_history

# initializes the message history for each session
def init_history(messages_history):
    messages_history = []
    messages_history += [system_message]
    return messages_history


# gradio file upload function
def upload_file(files):
    file_paths = [file.name for file in files]
    return file_paths

# views uploaded file
def view_file(file_data):
    b64_data = base64.b64encode(file_data).decode()
    if file_data[:4] == b'%PDF':
        return f"<embed src='data:application/pdf;base64,{b64_data}' type='application/pdf' width='100%' height='800px' />"
    else:
        return f"<embed src='data:text/plain;base64,{b64_data}' type='text/plain' width='100%' height='500px' />"


# main interface
with gr.Blocks(title="ChatGPT Academic Optimization", theme=kit.theme) as demo:
    gr.Markdown(title_html)
    gr.Markdown(description)
    state = gr.State([])  # used to store the message history of each user session.
    with gr.Row():
        with gr.Column(scale=2):  # main chatbot
            chatbot = gr.Chatbot(value=[], elem_id="chatbot").style(height=800)
        with gr.Column(scale=1):
            with gr.Row():  # Choose Model and Clear Button
                drop = gr.Dropdown(available_models, value="gpt-3.5-turbo", label="model")
                clear = gr.Button("Clear", variant="secondary");
                clear.style(size="sm")
                clear.click(lambda: None, None, chatbot, queue=False).success(init_history, [state], [state])
            with gr.Row():  # the five tabs for the exercises
                with gr.Tab("Important Information Presentation") as important_information_tab:  # first exercise
                    with gr.Row():
                        description3 = gr.Textbox(placeholder="Enter Dataset Description", label="Description").style(container=False)
                    with gr.Row():
                        information_presentation = gr.Button("Get Important Information Pipeline", variant="secondary")
                        combining_result8 = gr.Textbox(visible=False)
                        click_handle8 = information_presentation.click(important_information_pipeline, description3, chatbot)
                with gr.Tab("Related Work Listing") as important_information_presentation:  # second exercise
                    with gr.Row():
                        paper_name = gr.Textbox(placeholder="Enter Paper Name Here",label="Paper Name").style(container=False)
                        number_of_papers = gr.Slider(2, 20, value=10, label="Count",step=1)
                    #gr.Markdown("Functions area")
                    with gr.Row():
                        pure_gpt = gr.Button("Pure GPT", variant="secondary")
                        combining_result = gr.Textbox(visible=False)
                        click_handle = pure_gpt.click(related_papers, [paper_name, number_of_papers], combining_result).then(user, [combining_result, chatbot], [combining_result, chatbot]).then(
                                bot, [chatbot, state, drop], [chatbot, state]
                        )
                        with_scholarly = gr.Button("Get Citations With Scholarly", variant="secondary")
                        combining_result2 = gr.Textbox(visible=False)
                        click_handle2 = pure_gpt.click(related_papers_with_scholarly, [paper_name, number_of_papers], combining_result2).then(user, [combining_result2, chatbot], [combining_result2, chatbot]).then(
                                bot, [chatbot, state, drop], [chatbot, state]
                        )
                        with gr.Column(scale=1):
                            with_pybliometrics = gr.Button("Get References With Pybliometrics", variant="primary")
                            combining_result3 = gr.Textbox(visible=False)
                            click_handle3 = with_pybliometrics.click(related_papers_with_pybliometrics, [paper_name, number_of_papers], combining_result3).then(user, [combining_result3, chatbot], [combining_result3, chatbot]).then(
                                    bot, [chatbot, state, drop], [chatbot, state]
                            )
                            gr.Markdown(pybliometrics)
                with gr.Tab("Tool and Algorithm Recommendations") as tool_and_algorithm_recommendation:  # third exercise
                    with gr.Row():  # textbox for dataset description and a slider for the number of algorithms returned
                        description = gr.Textbox(placeholder="Enter sample Description", label="Sample").style(container=False)
                        number_of_algorithms = gr.Slider(2, 20, value=10, label="Count",step=1)
                    with gr.Row():  # apply button
                        algorithm_gpt = gr.Button("Algorithm Recommendation Prompt", variant="secondary")
                        combining_result4 = gr.Textbox(visible=False)
                        click_handle4 = algorithm_gpt.click(algorithm_recommendation, [description, number_of_algorithms], combining_result4).then(user, [combining_result4, chatbot], [combining_result4, chatbot]).then(
                                bot, [chatbot, state, drop], [chatbot, state]
                        )
                with gr.Tab("Data Exploration Results") as data_exploration_results:  # fourth exercise
                    with gr.Row():  # Two textboxes for dataset and sample description and a slider for the number of lines for the head of file given
                        description2 = gr.Textbox(placeholder="Enter Dataset Description", label="Description").style(container=False)
                        sample_description = gr.Textbox(placeholder="Enter Sample Description", label="Sample").style(container=False)
                        with gr.Column(scale=1):
                            number_of_lines = gr.Slider(2, 10, value=5, label="Count",step=1)
                    with gr.Column(container=False):  # upload and display file
                        file_output = gr.File(type="binary")
                        upload_button = gr.UploadButton("Click to Upload a File", file_types=["file"])
                        upload_button.upload(upload_file, upload_button, file_output, show_progress=True)
                        viewer_button = gr.Button("View file")
                        file_out = gr.HTML()
                        viewer_button.click(view_file, inputs=file_output, outputs=file_out)
                    with gr.Row():  # Buttons for the data visualization amd descriptive statistics prompts
                        data_exploration_prompt = gr.Button("Data Visualisation Prompt", variant="secondary")
                        file_header = gr.Textbox(visible=False)
                        combining_result5 = gr.Textbox(visible=False)
                        click_handle5 = data_exploration_prompt.click(
                                read_n,[file_output,number_of_lines],file_header).then(
                                data_exploration, [description2, file_header], combining_result5).then(
                                user, [combining_result5, chatbot], [combining_result5, chatbot]).then(
                                bot, [chatbot, state, drop], [chatbot, state]
                        )
                        descriptive_statistics_prompt = gr.Button("Descriptive Statistics Prompt", variant="secondary")
                        file_header2 = gr.Textbox(visible=False)
                        combining_result6 = gr.Textbox(visible=False)
                        click_handle6 = descriptive_statistics_prompt.click(
                                read_n,[file_output,number_of_lines],file_header2).then(
                                descriptive_statistics, [description2, file_header2], combining_result6).then(
                                user, [combining_result6, chatbot], [combining_result6, chatbot]).then(
                                bot, [chatbot, state, drop], [chatbot, state]
                        )
                    with gr.Row():  # button for the pipeline function for the fourth exercise
                        pipeline1 = gr.Button("Pipeline", variant="primary")
                        file_header3 = gr.Textbox(visible=False)
                        sample_desc = gr.Textbox(visible=False)
                        combining_result7 = gr.Textbox(visible=False)
                        # data_exploration_pipeline(description,sample,sample_description):
                        click_handle7 = pipeline1.click(read_n,[file_output,number_of_lines],file_header3).then(
                            data_exploration_pipeline,[chatbot,description2,file_header3,sample_desc,number_of_lines],chatbot
                        )
                with gr.Tab("Data Format Transformation") as data_transformation: # fifth exercise
                    with gr.Row():  # textbox for dataset description and a slider for the number of algorithms returned
                        description3 = gr.Textbox(placeholder="Enter sample Description", label="Sample").style(container=False)
                        number_of_rows4 = gr.Slider(2, 20, value=5, label="Rows",step=1)
                        with gr.Column(scale=1):  # upload file
                            file_output2 = gr.File(type="binary")
                            file_header4 = gr.Textbox(visible=False)
                        upload_button = gr.UploadButton("Click to Select a File", file_types=["file"])
                        upload_button.upload(upload_file, upload_button, file_output2, show_progress=True)
                        combining_result9 = gr.Textbox(visible=False)
                        with gr.Column(scale=1):  # perform the prompt for the fifth exercise button
                            data_button = gr.Button("Prompt", variant="primary")
                            click_handle9 = data_button.click(
                                    read_n,[file_output,number_of_rows4],file_header4).then(
                                    data_format_transformation, [description3,file_header4], combining_result9).then(
                                    user, [combining_result9, chatbot], [combining_result9, chatbot]).then(
                                    bot, [chatbot, state, drop], [chatbot, state]
                            )

    with gr.Row():  # plot results part
        #gr.Markdown(code_area)
        with gr.Accordion("Code Display Area", open=False):
            with gr.Row():  # code field and plot output field
                code = gr.Code()
                plot = gr.Plot()
            with gr.Row():  # perform the code given button
                execute1 = gr.Button("Execute Code", variant="secondary")
                execute_handle = execute1.click(execute,code,plot)
    # Ribbon displays the interaction between the switch and the ribbon

demo.launch(debug=True)
