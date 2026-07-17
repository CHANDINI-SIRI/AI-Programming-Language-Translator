import os
import gradio as gr
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def convert_program(code, source, target):
    if not code.strip():
        return "Please enter a program."

    prompt = f"""
Convert the following {source} program into {target}.

Requirements:
- Preserve the same logic.
- Follow {target} coding conventions.
- Return only the converted code without any explanation.

Program:
{code}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


demo = gr.Interface(
    fn=convert_program,
    inputs=[
        gr.Textbox(
            label="Input Program",
            placeholder="Paste your source code here...",
            lines=15
        ),
        gr.Dropdown(
            choices=[
                "Python",
                "C",
                "Java",
                "JavaScript"
            ],
            label="Source Programming Language",
            value="Python"
        ),
        gr.Dropdown(
            choices=[
                "Python",
                "C",
                "Java",
                "JavaScript"
            ],
            label="Target Programming Language",
            value="Java"
        )
    ],
    outputs=gr.Textbox(
        label="Converted Program",
        lines=20
    ),
    title="AI Programming Language Converter",
    description="Convert source code from one programming language to another using Gemini."
)

port = int(os.environ.get("PORT", 7860))

demo.launch(
    server_name="0.0.0.0",
    server_port=port
)
