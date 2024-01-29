FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=$OPENAI_API_KEY

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]