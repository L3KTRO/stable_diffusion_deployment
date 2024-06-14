import torch, time
from diffusers import AutoPipelineForText2Image
from diffusers.pipelines.stable_diffusion import StableDiffusionSafetyChecker

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch.float16,
    variant="fp16",
    safety_checks=StableDiffusionSafetyChecker.from_pretrained("CompVis/stable-diffusion-safety-checker"),
)
pipe.to("cuda")

prompt = "A cinematic shot of a baby racoon wearing an intricate italian priest robe."
image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

image.save(f'generation_{int(time.time())}.png')
