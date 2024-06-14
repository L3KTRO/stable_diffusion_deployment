import flask, base64, torch, threading, time, queue
from io import BytesIO
from diffusers import AutoPipelineForText2Image
from diffusers.pipelines.stable_diffusion import StableDiffusionSafetyChecker

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch.float16,
    variant="fp16",
)
pipe.to("cuda")


def generate_image(prompt):
    buffer = BytesIO()
    prompt = prompt.replace("%20", " ")
    print("Generating image with prompt:", prompt)

    image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str


app = flask.Flask(__name__)
request_queue = queue.Queue()


# Función que procesará las requests de la cola
def process_queue():
    while True:
        try:
            req = request_queue.get(timeout=1)  # Esperar 1 segundo para obtener una request de la cola
            if req:
                generated = generate_image(req['data'])
                # Enviar la respuesta almacenada
                req['response'] = generated
                req['event'].set()
        except queue.Empty:
            continue


# Hilo que ejecuta la función de procesamiento
worker_thread = threading.Thread(target=process_queue)
worker_thread.daemon = True
worker_thread.start()


@app.route("/generate", methods=["GET"])
def response():
    prompt = flask.request.args.get('prompt')
    event = threading.Event()
    req_data = {
        'data': prompt,
        'event': event,
        'response': None
    }
    request_queue.put(req_data)

    # Esperar hasta que la request haya sido procesada
    event.wait()

    return req_data['response']


app.run(host="0.0.0.0", port=5000)
