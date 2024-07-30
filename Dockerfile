# imagen base oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app
#actualizamos pip
RUN pip install --upgrade pip

# Copiar el archivo de requerimientos y luego instala las dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del codigo de la aplicacion al contenedor
COPY . .

# Expone el puerto en el que se ejecutara Streamlit
EXPOSE 8501

# Define el comando por defecto para ejecutar la aplicación Streamlit
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]

