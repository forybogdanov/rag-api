FROM continuumio/miniconda3:latest

WORKDIR /code

COPY environment.yml .

# Create conda environment
RUN conda env create -f environment.yml

# Activate conda environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

COPY . .

EXPOSE 8000

CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
