from fastapi import FastAPI
from diffusers import MotionAdapter, AnimateDiffPipeline, StableDiffusionPipeline
from diffusers.utils import export_to_video
import torch
from pydantic import BaseModel
import os

app = FastAPI()

print("🚀 Starting AnimateDiff video service...")
print("📥 Loading motion adapter...")

try:
    # Load motion adapter
    adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2")

    # Load base model
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float32,  # CPU compatible
        safety_checker=None,
    )

    # FIXED: Correct AnimateDiff pipeline creation
    pipeline = AnimateDiffPipeline.from_pipe(pipe, motion_adapter=adapter)  # Named arg!
    pipeline.to("cpu")
    pipeline.enable_vae_slicing()
    pipeline.enable_vae_tiling()

    app.state = type("State", (), {"pipe": pipeline, "loaded": True})()
    print("✅ AnimateDiff pipeline LOADED SUCCESSFULLY!")

except Exception as e:
    print(f"❌ Load failed: {e}")
    app.state = type("State", (), {"pipe": None, "loaded": False})()


class GenerateRequest(BaseModel):
    prompt: str = "a cat dancing"
    num_frames: int = 16
    steps: int = 25


@app.post("/generate")
async def generate(request: GenerateRequest):
    if not app.state.loaded:
        return {"status": "error", "message": "Model not ready"}

    try:
        print(f"🎬 Generating: {request.prompt[:50]}...")
        output = app.state.pipe(
            prompt=request.prompt,
            num_frames=min(24, request.num_frames),
            num_inference_steps=request.steps,
            guidance_scale=7.5,
            generator=torch.Generator(device="cpu").manual_seed(42),
        )

        frames = output.frames[0]
        video_path = export_to_video(frames)
        print(f"✅ Generated {len(frames)} frames")

        return {
            "status": "success",
            "frames": len(frames),
            "video_path": f"/tmp/{os.path.basename(video_path)}",
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/health")
async def health():
    return {
        "status": "ready" if app.state.loaded else "failed_to_load",
        "model": "AnimateDiff v1.5.2",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
