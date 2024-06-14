FROM python:3.9.11-slim-buster
LABEL authors="L3KTRO"

COPY main.py ./main.py
COPY requirements.txt ./requirements.txt
RUN python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install -r ./requirements.txt

ENTRYPOINT ["python"]
CMD ["./main.py"]