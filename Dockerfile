FROM python:3.11

# Install npm
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Makes Python output available to container logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN cd PizzaPyWebApp/js_lib && npm install

EXPOSE 8000

CMD ["python", "PizzaPyWebApp/manage.py", "runserver", "0.0.0.0:8000"]
