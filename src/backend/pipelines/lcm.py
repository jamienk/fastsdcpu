from constants import LCM_DEFAULT_MODEL
from diffusers import (
    DiffusionPipeline,
    AutoencoderTiny,
    UNet2DConditionModel,
    LCMScheduler,
)
import torch
from backend.tiny_decoder import get_tiny_decoder_vae_model
from typing import Any


def _get_lcm_pipeline_from_base_model(
    lcm_model_id: str,
    base_model_id: str,
    use_local_model: bool,
):
    pipeline = None
    unet = UNet2DConditionModel.from_pretrained(
        lcm_model_id, torch_dtype=torch.float32, local_files_only=use_local_model
    )
    pipeline = DiffusionPipeline.from_pretrained(
        base_model_id,
        unet=unet,
        torch_dtype=torch.float32,
        local_files_only=use_local_model,
    )
    pipeline.scheduler = LCMScheduler.from_config(pipeline.scheduler.config)
    return pipeline


def load_taesd(
    pipeline: Any,
    use_local_model: bool = False,
    torch_data_type: torch.dtype = torch.float32,
):
    vae_model = get_tiny_decoder_vae_model(pipeline.__class__.__name__)
    pipeline.vae = AutoencoderTiny.from_pretrained(
        vae_model,
        torch_dtype=torch_data_type,
        local_files_only=use_local_model,
    )


def get_lcm_model_pipeline(
    model_id: str = LCM_DEFAULT_MODEL,
    use_local_model: bool = False,
):
    pipeline = None
    if model_id == "latent-consistency/lcm-sdxl":
        pipeline = _get_lcm_pipeline_from_base_model(
            model_id,
            "stabilityai/stable-diffusion-xl-base-1.0",
            use_local_model,
        )

    elif model_id == "latent-consistency/lcm-ssd-1b":
        pipeline = _get_lcm_pipeline_from_base_model(
            model_id,
            "segmind/SSD-1B",
            use_local_model,
        )
    else:
        pipeline = DiffusionPipeline.from_pretrained(
            model_id,
            local_files_only=use_local_model,
        )

    return pipeline