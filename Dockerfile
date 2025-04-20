# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables here
ENV AAI_TOKEN="e9087c809137479e98db18c22a5ae39c"

# Expose the port Streamlit will run on
EXPOSE 8501

# Define environment variable for Ollama API URL
ENV OLLAMA_URL=http://ollama:11434

# Run Streamlit when the container launches
ENTRYPOINT ["streamlit", "run", "aai_output.py"]
