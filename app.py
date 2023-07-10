import os
import openai
import gradio as gr
import kittheme as kit
import logging
import base64
# Key
openai.api_key = "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"
#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

# String variables to use throughout the code
title_html = """<h1><center>CHATGPT-based  Prompt  for  Human  Activity  Recognition  (HAR) </center></h1>"""
description = """<p><center>The following code extracts and analyzes information from Human Activity Recognition (HAR) datasets</center></p>"""
#model = "gpt-3.5-turbo"
system_message = {"role": "system", "content": "You are a helpful assistant."}
# Query records, python version 3.9+ is recommended (the newer the better)


available_models = ["gpt-3.5-turbo-16k", "gpt-3.5-turbo", "gpt-4", "gpt-4-32k", "text-davinci-003", "text-curie-001",
                    "text-babbage-001", "text-ada-001",""]
# logging
os.makedirs("gpt_log", exist_ok=True)
try:
    logging.basicConfig(filename="gpt_log/chat_secrets.log", level=logging.INFO, encoding="utf-8")
except:
    logging.basicConfig(filename="gpt_log/chat_secrets.log", level=logging.INFO)
print("All query records will be automatically saved in the local directory./gpt_log/chat_secrets.log")

# Import functional prompts
from functions import get_functions

functions = get_functions()

# updates user message
def user(user_message, history):
    return "", history + [[user_message, None]]


# updates the message history as the conversation progresses
def bot(history, messages_history, model):
    user_message = history[-1][0]
    print(history)
    print(messages_history)
    bot_message, messages_history = ask_gpt(user_message, messages_history, model)
    messages_history += [{"role": "assistant", "content": bot_message}]
    print(messages_history)
    history[-1][1] = bot_message
    print("history: ", history, "messages_history: ", messages_history)
    return history, messages_history

# queries from chatgpt for an answer
def ask_gpt(message, messages_history, model):
    messages_history += [{"role": "user", "content": message}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages_history,
        temperature=1.0
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
model2 = ""
# main interface
with gr.Blocks(title="ChatGPT Academic Optimization", theme=kit.theme) as demo:
    gr.Markdown(title_html)
    gr.Markdown(description)
    state = gr.State([])  # used to store the message history of each user session.
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(value=[], elem_id="chatbot").style(height=800)
        with gr.Column(scale=1):
            with gr.Row():
                drop = gr.Dropdown(available_models, value="gpt-3.5-turbo", label="model")
                #drop.select(fn= lambda x: x , inputs=drop, outputs=model2)
            with gr.Tab("text area") as area_input_primary:
                with gr.Row():
                    msg = gr.Textbox(placeholder="Enter text here").style(container=False)
                with gr.Row():
                    submit = gr.Button("Submit", variant="primary")
                    # submit with click
                    submit.click(user, [msg, chatbot], [msg, chatbot]).then(
                        bot, [chatbot, state, drop], [chatbot, state]
                    )
                    # submit with enter
                    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
                        bot, [chatbot, state, drop], [chatbot, state]
                    )
                with gr.Row():
                    clear = gr.Button("Clear", variant="secondary");
                    clear.style(size="sm")
                    clear.click(lambda: None, None, chatbot, queue=False).success(init_history, [state], [state])
            with gr.Tab("txt or pdf upload") as area_txt_pdf:
                with gr.Column(container=False):
                    file_output = gr.File(type="binary")
                    upload_button = gr.UploadButton("Click to Upload a File", file_types=["file"])
                    upload_button.upload(upload_file, upload_button, file_output)
                    viewer_button = gr.Button("View file")
                    txt = gr.Textbox(file_output)
                    file_out = gr.HTML()
                    viewer_button.click(view_file, inputs=file_output, outputs=file_out)
            with gr.Accordion("Basic functional area", open=True) as area_basic_fn:
                #gr.Markdown("Functions area")
                with gr.Row():
                    for k in functions:
                        variant = functions[k]['Color']
                        functions[k]["Button"] = gr.Button(k, variant=variant)
                        # hier müsste eigentlich msg durch functions[k]["Prefix"] ersetzt werden, aber das funktioniert nicht
                        click_handle = functions[k]["Button"].click(user, [msg, chatbot], [msg, chatbot]).then(
                        bot, [chatbot, state, drop], [chatbot, state]
                        )
                        #cancel_handles.append(click_handle)
    # Ribbon displays the interaction between the switch and the ribbon

demo.launch(debug=True)
