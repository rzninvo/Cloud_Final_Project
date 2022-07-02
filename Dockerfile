# Stage 1: Builder/Compiler
FROM python:3.8-alpine AS builder

WORKDIR /app
COPY requirements.txt ./
RUN pip install --target=/app/dependencies -r requirements.txt

COPY app.py ./

# Stage 2: Runtime
FROM python:3.8-alpine
WORKDIR /app

#RUN apk update && apk add libusb-dev

COPY --from=builder /app .
ENV PYTHONPATH="${PYTHONPATH}:/app/dependencies"

CMD ["python","./app.py"]
