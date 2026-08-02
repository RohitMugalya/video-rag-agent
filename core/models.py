import os

import torch

try:
    import spaces
except Exception:  # pragma: no cover - local/dev environments may not have spaces installed
    spaces = None


if spaces is not None and hasattr(spaces, "GPU"):
    @spaces.GPU(duration=1)
    def _spaces_runtime_marker():
        return "spaces-runtime-marker"
else:
    def _spaces_runtime_marker():
        return "spaces-runtime-marker"


_MODEL_CACHE = {}


def _cuda_is_usable():
    if not torch.cuda.is_available():
        return False
    try:
        torch.zeros(1).cuda()
        return True
    except Exception:
        return False


def _get_device():
    return "cuda" if _cuda_is_usable() else "cpu"


def load_siglip():
    if "siglip" not in _MODEL_CACHE:
        from transformers import AutoModel, AutoProcessor

        model = AutoModel.from_pretrained("google/siglip2-base-patch16-224").eval()
        device = _get_device()
        model = model.to(device)
        processor = AutoProcessor.from_pretrained("google/siglip2-base-patch16-224")
        _MODEL_CACHE["siglip"] = (model, processor, device)
    return _MODEL_CACHE["siglip"]


def run_with_gpu_fallback(gpu_fn, cpu_fn):
    if not _cuda_is_usable():
        return cpu_fn(), True
    try:
        return gpu_fn(), False
    except RuntimeError as e:
        msg = str(e)
        if "No CUDA GPUs are available" in msg or "Low-level CUDA init" in msg or "CUDA emulation" in msg or "CUDA" in msg and "init" in msg:
            return cpu_fn(), True
        raise


def load_ocr():
    if "ocr" not in _MODEL_CACHE:
        import easyocr

        bad_zip = os.path.expanduser("~/.EasyOCR/model/temp.zip")
        for attempt in range(3):
            try:
                _MODEL_CACHE["ocr"] = easyocr.Reader(["en"], gpu=False)
                break
            except Exception as e:
                if os.path.exists(bad_zip):
                    os.remove(bad_zip)
                if attempt == 2:
                    raise e
    return _MODEL_CACHE["ocr"]


def load_whisper():
    if "whisper" not in _MODEL_CACHE:
        from faster_whisper import WhisperModel

        _MODEL_CACHE["whisper"] = WhisperModel("base", device="cpu")
    return _MODEL_CACHE["whisper"]


def load_viclip():
    if "viclip" not in _MODEL_CACHE:
        import json

        from huggingface_hub import snapshot_download
        from transformers import AutoModel

        local_dir = snapshot_download("OpenGVLab/ViCLIP-L-14-hf")
        config_path = f"{local_dir}/config.json"
        with open(config_path) as f:
            config = json.load(f)
        config["tokenizer_path"] = f"{local_dir}/bpe_simple_vocab_16e6.txt.gz"
        with open(config_path, "w") as f:
            json.dump(config, f)
        model = AutoModel.from_pretrained(local_dir, trust_remote_code=True)
        device = _get_device()
        model = model.to(device).eval()
        _MODEL_CACHE["viclip"] = (model, model.tokenizer, device)
    return _MODEL_CACHE["viclip"]


MODEL_LOADERS = {
    "SigLIP2 (visual search)": load_siglip,
    "EasyOCR (on-screen text)": load_ocr,
    "Whisper (spoken dialogue)": load_whisper,
    "ViCLIP (motion search)": load_viclip,
}


def warm_up_models():
    for name, loader in MODEL_LOADERS.items():
        print(f"Loading {name}...")
        loader()
        print(f"{name} ready.")
