from flask import Flask, render_template, request
import pandas as pd
import os
from werkzeug.utils import secure_filename
import plotly.express as px
from langchain.llms import CTransformers

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_llm():
    return CTransformers(
        model="llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        max_new_tokens=512,
        temperature=0.5
    )

llm = load_llm()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    dataset = pd.read_csv(file_path)

    user_query = request.form.get('query', 'Show sales over time')

    # Prompt the Llama 2 model
    prompt = f"""
    The user query is: '{user_query}'
    The dataset has the following columns: {', '.join(dataset.columns)}.
    Suggest:
    - graph_type: the type of graph (e.g., line chart, bar chart, scatter plot)
    - x_axis: the column for the x-axis.
    - y_axis: the column for the y-axis
    Provide the result in the format:
    graph_type: [type], x_axis: [column], y_axis: [column].
    """

    response = llm.invoke(prompt)
    response_text = response.strip()

    try:
        parsed_response = {}
        for part in response_text.split(','):
            key, value = part.split(':')
            parsed_response[key.strip()] = value.strip()

        graph_type = parsed_response.get('graph_type', 'line chart')
        x_axis = parsed_response.get('x_axis')
        y_axis = parsed_response.get('y_axis')

        if not x_axis or not y_axis:
            return "Could not determine x-axis or y-axis from the response.", 400

        # Generate the graph
        if graph_type == 'line chart':
            fig = px.line(dataset, x=x_axis, y=y_axis, title="Line Chart")
        elif graph_type == 'bar chart':
            fig = px.bar(dataset, x=x_axis, y=y_axis, title="Bar Chart")
        elif graph_type == 'scatter plot':
            fig = px.scatter(dataset, x=x_axis, y=y_axis, title="Scatter Plot")
        else:
            return f"Unsupported graph type: {graph_type}", 400

        return render_template('index.html', graph_html=fig.to_html(full_html=False))

    except Exception as e:
        return f"Failed to parse model response: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
