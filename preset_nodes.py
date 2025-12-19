from pathlib import Path

from .db import Database, _get_presets


def _get_db_path() -> str:
    BASE_DIR = Path(__file__).parent
    db_path = BASE_DIR / "presets.db"
    return db_path


class LoadAction:
    def __init__(self):
        self.db = Database(_get_db_path())
        self.preset_type = "action"

    @classmethod
    def INPUT_TYPES(cls):
        db = Database(_get_db_path())
        labels = db.read_labels("action")
        labels = [r[0] for r in labels]
        return {
            "required": {
                "label": (labels,),
            }
        }

    FUNCTION = "run"
    CATEGORY = "Presets/load-action-preset"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("description",)

    def run(self, label: str):
        description = self.db.read_description(label, self.preset_type)
        description = description[0][0]
        return (description,)


class LoadSubject:
    def __init__(self):
        self.db = Database(_get_db_path())
        self.preset_type = "subject"

    @classmethod
    def INPUT_TYPES(cls):
        db = Database(_get_db_path())
        labels = db.read_labels("subject")
        labels = [r[0] for r in labels]
        return {
            "required": {
                "label": (labels,),
            }
        }

    FUNCTION = "run"
    CATEGORY = "Presets/load-subject-preset"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("description",)

    def run(self, label: str):
        print(f"LABEL: {label} ")
        # label = label[0]
        #
        description = self.db.read_description(label, self.preset_type)
        description = description[0][0]
        return (description,)


class SavePreset:
    def __init__(self):
        self.db = Database(_get_db_path())

    @classmethod
    def INPUT_TYPES(cls):

        presets = _get_presets()
        db = Database(_get_db_path())
        labels = db.read_labels("", get_all=True)
        labels = [r[0] for r in labels]
        return {
            "required": {
                "preset_type": (presets,),
                "label": ("STRING", {"default": ""}),
                "description": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "run"
    CATEGORY = "Presets/save-preset"

    def run(self, preset_type: str, label: str, description: str):
        print(
            f"PRESET_TYP: {preset_type}   LABEL: {label}   DESCRIPTION: {description}"
        )
        self.db.insert_data(label, description, preset_type)
        return ()


class UpdatePreset:
    def __init__(self):
        self.db = Database(_get_db_path())

    @classmethod
    def INPUT_TYPES(cls):
        db = Database(_get_db_path())
        labels = db.read_labels("", get_all=True)
        labels = [r[0] for r in labels]
        return {
            "required": {
                "label": (labels,),
                "description": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "run"
    CATEGORY = "Presets/update-preset"

    def run(self, label: str, description: str):
        self.db.update_data(label, description)
        return ()


class DeletePreset:
    def __init__(self):
        self.db = Database(_get_db_path())

    @classmethod
    def INPUT_TYPES(cls):
        db = Database(_get_db_path())
        labels = db.read_labels("", get_all=True)
        labels = [r[0] for r in labels]
        return {
            "required": {
                "label": (labels,),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "run"
    CATEGORY = "Presets/delete-preset"

    def run(self, label: str):
        self.db.delete_data(label)
        return ()
