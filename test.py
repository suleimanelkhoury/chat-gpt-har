import gradio as gr

import openai

import os

import json

openai.api_key = "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"
model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
]

def add_text(history, text):
    global messages  #message[list] is defined globally
    history = history + [(text,'')]
    messages = messages + [{"role":'user', 'content': text}]
    return history, ""
def generate_response(history, model ):
        global messages, cost

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1.0,
        )

        response_msg = response.choices[0].message.content
        cost = cost + (response.usage['total_tokens'])*(0.002/1000)
        messages = messages + [{"role":'assistant', 'content': response_msg}]

        for char in response_msg:

            history[-1][1] += char
            #time.sleep(0.05)
            yield history
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(value=[], elem_id="chatbot").style(height=650)
with gr.Row():
      with gr.Column(scale=0.85):
          txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter",
                ).style(container=False)
with gr.Blocks() as demo:
    radio = gr.Radio(value='gpt-3.5-turbo', choices=['gpt-3.5-turbo','gpt-4'], label='models')
    chatbot = gr.Chatbot(value=[], elem_id="chatbot").style(height=650)
    with gr.Row():
        with gr.Column(scale=0.70):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter, or upload an image",
            ).style(container=False)
        with gr.Column(scale=0.10):
            cost_view = gr.Textbox(label='usage in $',value=0)
    txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
            generate_response, inputs =[chatbot,],outputs = chatbot,).then(
            cost, outputs=cost_view)

demo.queue()
demo.launch(debug=True)
