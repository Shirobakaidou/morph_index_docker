# Base Image
FROM continuumio/miniconda3

# Set Working Directory to /app
WORKDIR /app

# Create the environment
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new env
SHELL ["conda", "run", "-n", "conda_env", "/bin/bash", "-c"]

# Make sure the env is activated
RUN echo "Make sure numpy is installed:"
RUN python -c "import numpy"

# The code ro run when container is started
COPY my_script.py .
COPY sample_data/. ./sample_data/
ENTRYPOINT ["conda", "run", "-n", "conda_env", "python", "my_script.py"]
