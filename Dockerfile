# Usar una imagen base de Python
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app.py .
COPY .env .
COPY data/processed/train_data.csv data/processed/train_data.csv
COPY static/ static/
COPY src/ src/

# Copy the requirements file into the container
COPY requirements.txt .

#Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "pinecone-client[grpc]"
RUN pip3 install pinecone


# Exponer el puerto 8501 para Streamlit UI
EXPOSE 8501

# Execute uvicorn
CMD ["streamlit", "run", "app.py"]