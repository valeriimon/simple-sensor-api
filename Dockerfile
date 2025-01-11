# Use the official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements.txt first for caching dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's code
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
