import gradio as gr
from .functionTester import funcTesterTab

with gr.Blocks(title="WEmulator Gradio WebUI") as wemulatorWebUI:
    funcTesterTab()

def main():
    wemulatorWebUI.launch(server_port=7861)