import gradio as gr
from .. import data as wemu_data

def funcTesterTab():
    with gr.TabItem(label="🧰[Debug Mode]函数调试器") as tab:
        with gr.Accordion("数据模块", open=False):
            gr.Markdown("## 新建数据结构")
            with gr.Row():
                with gr.Column():
                    type = gr.Dropdown(label="新建数据类型",choices=["World","WAAConfig"])
                    name = gr.Textbox(label="名字",lines=1,max_lines=1)
                    testBtn = gr.Button("进行测试")
                jsonOut = gr.JSON(label="测试输出")
                testBtn.click(fn=wemu_data.new,inputs=[name,type],outputs=jsonOut)
    return tab