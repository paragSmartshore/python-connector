# Use the official Python image
FROM python:3.12-slim

# Install Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
 && poetry install --no-dev

# Expose the Flask port
EXPOSE 6000

# Run the Flask app
CMD ["poetry", "run", "python", "app.py"]
