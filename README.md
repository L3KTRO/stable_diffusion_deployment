# Simple Stable Diffusion Deployment

### Requirements
- Python 3.8+ + PiP
- Docker (optional)


### Installation
1. Clone the repository

## Running the application
### Native
1. Install the requirements
```bash
pip3 install -r requirements.txt
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
2. Run the application
```bash
python3 main.py
```

### Docker
1. Build the docker image
```bash
docker build -t simple-stable-diffusion .
```
2. Run the docker image
```bash
docker run -p 5000:5000 simple-stable-diffusion
```

