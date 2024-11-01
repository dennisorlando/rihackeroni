FROM python:3.10-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV GEMINI_API_KEY=hihi
EXPOSE 5000
COPY . .
CMD ["flask", "run", "--debug", "--host=0.0.0.0"]
