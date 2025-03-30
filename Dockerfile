# Use a lightweight official Python image
FROM python:3.12.1

# Prevent Python from writing .pyc files to disc & enable stdout/stderr logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy dependency definitions and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the application using Uvicorn (adjust module path as needed)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
