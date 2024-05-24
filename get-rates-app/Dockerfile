# ---------- SET BASE IMAGE ----------
FROM python:3.12
# ---------- SET WORKING DIRECTORY ----------
WORKDIR /code
# ---------- IMPORT DEPENDANCIES INTO CONTAINER ----------
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# ---------- COPY SCRIPT TO CONTAINER ----------
COPY ./main.py /code/main.py
# ---------- RUN THE SCRIPT ----------
CMD ["python", "/code/main.py"]