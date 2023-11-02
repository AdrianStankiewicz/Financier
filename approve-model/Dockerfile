#
FROM python:latest

# Set the working directory in the container
WORKDIR /model

# Copy Python script and dataset into the container
COPY model-training.py /model/model-training.py
COPY model-data.csv /model/model-data.csv

# Copy requirements
COPY requirements.txt /model/requirements.txt

# Install required Python packages
RUN pip install --no-cache-dir --upgrade -r /model/requirements.txt

# Run the script when the container starts
CMD ["python", "model-training.py"]
