from .preset_nodes import (
    LoadAction,
    LoadSubject,
    SavePreset,
    DeletePreset,
    UpdatePreset,
)

NODE_CLASS_MAPPINGS = {
    "DeletePreset": DeletePreset,
    "LoadAction": LoadAction,
    "LoadSubject": LoadSubject,
    "SavePreset": SavePreset,
    "UpdatePreset": UpdatePreset,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DeletePreset": "Delete Preset",
    "LoadAction": "Load Action",
    "LoadSubject": "Load Subject Node",
    "SavePreset": "Save Preset Node",
    "UpdatePreset": "Update Preset",
}


__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
