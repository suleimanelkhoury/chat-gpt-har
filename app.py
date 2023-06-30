import os
import openai
import gradio as gr
import kittheme as kit
import logging
from toolbox import format_io
openai.api_key = "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"

title_html = """<h1><center>CHATGPT-based  Prompt  for  Human  Activity  Recognition  (HAR) </center></h1>"""
description = """<p><center>The following code extracts and analyzes information from Human Activity Recognition (HAR) datasets</center></p>"""
model="gpt-3.5-turbo"
system_message={"role": "system", "content": "You are a helpful assistant."}
# Query records, python version 3.9+ is recommended (the newer the better)

os.makedirs("gpt_log", exist_ok=True)
try:logging.basicConfig(filename="gpt_log/chat_secrets.log", level=logging.INFO, encoding="utf-8")
except:logging.basicConfig(filename="gpt_log/chat_secrets.log", level=logging.INFO)
print("All query records will be automatically saved in the local directory./gpt_log/chat_secrets.log")

# Import functional prompts
from functions import get_functions
functions = get_functions()

def user(user_message, history):
    return "", history + [[user_message, None]]

def bot(history, messages_history):
    user_message = history[-1][0]
    bot_message, messages_history = ask_gpt(user_message, messages_history)
    messages_history += [{"role": "assistant", "content": bot_message}]
    history[-1][1] = bot_message

    return history, messages_history

def ask_gpt(message, messages_history):
    messages_history += [{"role": "user", "content": message}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_history,
        temperature=1.0
    )
    return response['choices'][0]['message']['content'], messages_history

def init_history(messages_history):
    messages_history = []
    messages_history += [system_message]
    return messages_history

def upload_file(files):
    print("here")
    file_paths = [file.name for file in files]
    return file_paths
with gr.Blocks(title="ChatGPT Academic Optimization", theme=kit.theme) as demo:
#with gr.Blocks(title="ChatGPT Academic Optimization") as demo:
    gr.Markdown(title_html)
    gr.Markdown(description)
    state = gr.State([])
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(value=[], elem_id="chatbot", label=f"Current model: {model}").style(height=800)
        with gr.Column(scale=1):
            with gr.Tab("choose model") as area_model:
                with gr.Row(container=False):
                    radio = gr.Radio(value='gpt-3.5-turbo', choices=['gpt-3.5-turbo','gpt-4'], label='models')
            with gr.Tab("text area") as area_input_primary:
                with gr.Row():
                    msg = gr.Textbox(placeholder="Enter text here").style(container=False)
                with gr.Row():
                    submit = gr.Button("Submit", variant="primary");
                    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
                        bot, [chatbot, state], [chatbot, state]
                    )
                with gr.Row():
                    reset = gr.Button("Reset", variant="secondary");  reset.style(size="sm")
                    stop = gr.Button("Stop", variant="secondary");  stop.style(size="sm")
                    clear = gr.Button("Clear", variant="secondary"); clear.style(size="sm")
                    clear.click(lambda: None, None, chatbot, queue=False).success(init_history, [state], [state])
            with gr.Tab("txt or pdf upload") as area_txt_pdf:
                with gr.Row(container=False):
                    file_output = gr.File()
                    upload_button = gr.UploadButton("Click to Upload a File", file_types=["txt", "pdf"])
                    upload_button.upload(upload_file, upload_button, file_output)
            with gr.Accordion("Basic functional area", open=True) as area_basic_fn:
                #gr.Markdown("Functions area")
                with gr.Row():
                    for k in functions:
                        if ("Visible" in functions[k]) and (not functions[k]["Visible"]): continue
                        variant = functions[k]["Color"] if "Color" in functions[k] else "secondary"
                        functions[k]["Button"] = gr.Button(k, variant=variant)
    # Ribbon displays the interaction between the switch and the ribbon

demo.launch(debug = True)
