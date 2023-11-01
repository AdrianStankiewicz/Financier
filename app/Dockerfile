# ---------- SET BASE IMAGE ----------
FROM python:latest

# ---------- SET WORKING DIRECTORY ----------
WORKDIR /app

# ---------- IMPORT DEPENDANCIES INTO CONTAINER ----------
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# ---------- COPY SAVED MODEL TO CONTAINER ----------
COPY Financier-approver.pkl /app/

# ---------- COPY CODEBASE TO CONTAINER ----------
COPY main.py /app/

# ---------- EXPOSE CONTAINER PORTS TO THE WORLD ----------
EXPOSE 80

# ---------- START THE APPLICATION ----------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]