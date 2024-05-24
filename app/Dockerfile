# ---------- SET BASE IMAGE ----------
FROM python:3.12
# ---------- SET WORKING DIRECTORY ----------
WORKDIR /app
# ---------- IMPORT DEPENDANCIES INTO CONTAINER ----------
COPY requirements.txt /app/
RUN pip install -r requirements.txt
# ---------- COPY SAVED MODEL TO CONTAINER ----------
COPY package/Financier-approver.pkl /app/package/
# ---------- COPY CODEBASE TO CONTAINER ----------
COPY main.py /app/
# ---------- COPY TEMPLATES TO CONTAINER ----------
COPY templates /app/templates
# ---------- EXPOSE CONTAINER PORTS TO THE WORLD ----------
EXPOSE 80
# ---------- START THE APPLICATION ----------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]