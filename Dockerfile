FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --no-dev

COPY . .

EXPOSE 8051

CMD ["uv", "run", "streamlit", "run", "dashboard.py", "--server.port=8051", "--server.address=0.0.0.0"]