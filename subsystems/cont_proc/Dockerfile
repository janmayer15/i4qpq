# Use a slimmer base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy only the requirements.txt initially
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "subsystems/cont_proc/app.py", "--server.port=8501", "--server.enableCORS=false"]
