FROM python:3.14-alpine

# 0. Actualizar el sistema
RUN apk update && apk upgrade && apk add --no-cache tzdata

# 1. Configurar el directorio de trabajo
WORKDIR /app

# 2. Copiar el fichero de dependencias
COPY requirements.txt .

# 3. Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el resto de la aplicación
COPY . .

# 5. Declaramos que estas carpetas serán volúmenes
# Esto crea las carpetas vacías en la imagen como puntos de anclaje
RUN mkdir -p /app/data /app/raw
VOLUME ["/app/data", "/app/raw"]

# 6. Exponer el puerto
EXPOSE 8501

# 7. Comando de ejecución
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]