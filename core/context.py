import contextvars

_session_id_var = contextvars.ContextVar("session_id", default="default")
_vlm_preference_var = contextvars.ContextVar("vlm_preference", default=("Groq", "qwen/qwen3.6-27b"))


def set_session_id(session_id):
    _session_id_var.set(session_id)


def get_session_id():
    return _session_id_var.get()


def set_vlm_preference(provider, model):
    _vlm_preference_var.set((provider, model))


def get_vlm_preference():
    return _vlm_preference_var.get()
