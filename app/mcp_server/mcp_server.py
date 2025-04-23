import gradio as gr
from fastapi import FastAPI
from gradio.routes import mount_gradio_app
import uvicorn
import os
import subprocess
from context_manager import save_context, load_context

# 🧠 Gradio-UI
with gr.Blocks() as mcp_ui:
    gr.Markdown("## 🧠 Model Context Protocol Server\nVerwalte globalen AI-Kontext für HeyBot & Co.")

    with gr.Row():
        style = gr.Dropdown(["neutral", "sarkastisch", "eingebildet", "freundlich"], value="neutral", label="Ton / Stil")
        mode = gr.Dropdown(["default", "devsecops", "alert-only", "humor", "juristisch"], value="default", label="Modus")
        language = gr.Dropdown(["de", "en"], value="de", label="Sprache")

    output = gr.JSON(label="Aktueller Kontext")

    with gr.Row():
        set_btn = gr.Button("📝 Kontext speichern")
        get_btn = gr.Button("🔍 Kontext anzeigen")
        run_btn = gr.Button("🚀 Bazinga Skript ausführen")

    set_btn.click(fn=save_context, inputs=[style, mode, language], outputs=output)
    get_btn.click(fn=load_context, outputs=output)

    # Skript manuell ausführen
    def run_script():
        """Führt das bazinga.py Skript manuell aus und gibt die Ausgabe zurück."""
        script_path = os.path.join(os.path.dirname(__file__), '..', 'bazinga_cve_bot.py')
        process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return stdout.decode('utf-8')
        else:
            return stderr.decode('utf-8')

    run_btn.click(fn=run_script, outputs=gr.Textbox(label="Progress"))

# 🚀 FastAPI + REST-Endpunkte
api = FastAPI()

@api.get("/mcp/context")
def read_context():
    return load_context()

@api.post("/mcp/context")
def write_context(style: str, mode: str, language: str):
    return save_context(style, mode, language)

# 🎯 Gradio mit FastAPI verbinden
mount_gradio_app(app=api, blocks=mcp_ui, path="/ui")

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=7861)
