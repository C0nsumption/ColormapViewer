import gradio as gr
from main import apply_colormap, get_all_colormaps

all_colormaps, cmap_categories = get_all_colormaps()

css = """
.gradio-container {max-width: 1200px; margin: auto;}
.output-image img {
    max-height: 600px !important;
    width: 100% !important;
    object-fit: contain !important;
}
"""

iface = gr.Interface(
    fn=apply_colormap,
    inputs=[gr.Image(type="pil", label="Input Image"), gr.Dropdown(choices=all_colormaps, label="Colormap", info="Select a colormap to apply")],
    outputs=[gr.Image(type="pil", label="Colormap Applied", elem_id="output-image"), gr.Textbox(label="Colormap Information")],
    title="Apply Colormap to Image",
    description="Upload an image and select a colormap to apply. The image will be converted to grayscale before applying the colormap.",
    examples=[["path/to/example/image.jpg", "viridis"], ["path/to/another/example/image.jpg", "jet"]],
    article="""
    <p>This tool allows you to apply various colormaps to your images. Here are some tips:</p>
    <ul>
        <li>Perceptually Uniform Sequential colormaps like 'viridis' are great for most use cases.</li>
        <li>For diverging data, consider using a Diverging colormap like 'coolwarm'.</li>
        <li>Qualitative colormaps are best for categorical data.</li>
        <li>Be cautious with 'jet' and similar colormaps, as they can be misleading in some contexts.</li>
    </ul>
    """,
    css=css
)
