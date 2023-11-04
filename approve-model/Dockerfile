FROM python:3.12

# Set the working directory in the container
WORKDIR /model

# Copy Python script and dataset into the container
COPY main.py ./main.py
COPY model-data.csv ./model-data.csv

# Copy requirements
COPY requirements.txt /model/requirements.txt

# Install required Python packages
RUN pip install --no-cache-dir --upgrade -r /model/requirements.txt

# Run the script when the container starts and save the output file to /model/
CMD ["python", "main.py"]
