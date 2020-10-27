import base64
import io
import json
from typing import Any

import PIL.Image  # type: ignore
from PIL.Image import Image  # type: ignore

from arcor2.cached import CachedProject as CProject
from arcor2.cached import CachedScene as CScene
from arcor2.parameter_plugins.base import ParameterPlugin, TypesDict


class ImagePlugin(ParameterPlugin):
    @classmethod
    def type(cls) -> Any:
        return Image

    @classmethod
    def type_name(cls) -> str:
        return "image"

    @classmethod
    def parameter_value(
        cls, type_defs: TypesDict, scene: CScene, project: CProject, action_id: str, parameter_id: str
    ) -> Image:
        json_str = super(ImagePlugin, cls).parameter_value(type_defs, scene, project, action_id, parameter_id)
        return cls._value_from_json(json_str)

    @classmethod
    def _value_from_json(cls, value: str) -> Image:

        b64_bytes = value.encode()
        image_data = base64.b64decode(b64_bytes)
        return PIL.Image.open(io.BytesIO(image_data))

    @classmethod
    def value_to_json(cls, value: Image) -> str:

        with io.BytesIO() as output:
            value.save(output, "jpeg")
            b64_bytes = base64.b64encode(output.getvalue())
            b64_str = b64_bytes.decode()
            return json.dumps(b64_str)
