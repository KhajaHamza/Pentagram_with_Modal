import modal
import io
from fastapi import Response,HTTPException,Query,Request
from datetime import datetime,timezone
import requests
import os


def download_model():
    from diffusers import AutoPipelineForText2Image
    import torch
    AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")

image=(modal.Image.debian_slim().pip_install("fastapi[standard]","transformers","accelerate","diffusers")
       .run_function(download_model))

app=modal.App("sd-demo",image=image)

@app.cls(
    image=image,
    gpu="A10G",
    container_idle_timeout=300,
    secrets=[modal.Secret.from_name("API_KEY")]
)

class Model:

    @modal.build()
    @modal.enter()
    def load_weights(self):
        from diffusers import AutoPipelineForText2Image
        import torch 

        self.pipe=AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", 
            torch_dtype=torch.float16,
            variant="fp16"
        )
        self.pipe.to("cuda")
        self.API_KEY=os.environ["API_KEY"]
    @modal.web_endpoint()
    def generate(self,request:Request,prompt:str=Query(...,description="The prompt for image generation")):
        """This function generates an image using a text prompt provided via a query parameter.
            It uses an image generation pipeline, converts the output to JPEG format, and returns it as an HTTP response.
            Example-
            Request: GET /generate?prompt="A sunset over mountains"
            Response: A JPEG image of the described scene.
        """

        api_key=request.headers.get("X-API-Key")
        if api_key!= self.API_KEY:
            raise HTTPException(
                status_code=401,
                detail="unauthorized"

            )
        image=self.pipe(prompt,num_inference_steps=4,guidance_scale=2.0).images[0]

        buffer=io.BytesIO()
        image.save(buffer,format="JPEG")

        return Response(content=buffer.getvalue(),media_type="image/jpeg")
    @modal.web_endpoint()
    def health(self):
        """Lightweight endpoint for keeping the container warm"""
        return {"status":"healthy","timestamp":datetime.now(timezone.utc).isoformat()}
#Warm-keeping function that runs every 5 minutes
@app.function(
    schedule=modal.Cron("*/5 * * * *"),
    secrets=[modal.Secret.from_name("API_KEY")]
)
def keep_warm():
    health_url="https://khajahamza--sd-demo-model-health.modal.run"
    generate_url="https://khajahamza--sd-demo-model-generate.modal.run"

    #First check health endpoint(no API Key needed)
    health_response=requests.get(health_url)
    print(f"Health check at: {health_response.json()['timestamp']}")

    #Then make a test request to generate endpoint with API Key
    headers={"X-API-KEY":os.environ["API_KEY"]}
    generate_response=requests.get(generate_url,headers=headers)
    print(f"Generate endpoint tested successfully at : {datetime.now(timezone.utc).isoformat()}")