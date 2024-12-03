# Custom Graph Generation using Large Language Models
This is a Flask-based web application for generating variable graphs from CSV files using natural language queries. The application uses a language model (Llama 2) via the LangChain library to understand user queries and dynamically generate appropriate graphs using Plotly.

# Useage
Step-1: Clone the repository 

Step-2: Install the modules in the 'Requirements.txt' 

Step-3: Download the llama2 model locally. 
        Model used in this project is from 'https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML' 
        (minimum requirment : 16GB RAM)

Step-4: Run the Application
        Start the Flask server by running:
        python app.py

# Features
* Upload CSV files and generate interactive graphs.
* Natural language queries are used to generate graphs (e.g., "Show sales over time").
* Supports common graph types: line charts, bar charts, and scatter plots.
* Interactive, responsive, and easy-to-use interface.

# Working
-> A Flask application acts as the frontend to retrive the csv file from the user. <br/>
-> Then the user is prompted for a query for graph generation. <br/>
-> The headers of the .csv file and prompt is sent to the llama2 large language model to retrive the appropriate X-axis, Y-axis and the graph type. <br/>
-> Results are then processed and a graph is generated via the plotly module. <br/>

# Project Structure
├── app.py                 # Main application file <br/>
├── templates/             <br/>
│   └── index.html         # HTML template for the web interface <br/>
├── llama-2-7b-chat.ggmlv3.q8_0.bin  # Llama 2 model file <br/>
