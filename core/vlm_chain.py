from core.providers import build_vlm, vlm_fallback_order


def call_vlm(messages, preferred_provider, preferred_model):
    chain = vlm_fallback_order(preferred_provider, preferred_model)
    attempts = []
    for provider, model in chain:
        label = f"{provider}/{model}"
        try:
            vlm = build_vlm(provider, model)
            response = vlm.invoke(messages)
            attempts.append({"provider": label, "status": "success"})
            return response, label, attempts
        except Exception as e:
            error_text = f"{type(e).__name__}: {str(e)[:150]}"
            attempts.append({"provider": label, "status": "failed", "error": error_text})
            print(f"[VLM call failed] {label}: {error_text}")
    raise RuntimeError(f"All VLM providers failed. Attempts: {attempts}")
