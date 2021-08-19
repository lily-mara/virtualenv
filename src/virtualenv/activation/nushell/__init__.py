from __future__ import absolute_import, unicode_literals

import os

from virtualenv.util.path import Path
from virtualenv.util.six import ensure_text

from ..via_template import ViaTemplateActivator


class NushellActivator(ViaTemplateActivator):
    def templates(self):
        yield Path("activate.nu")
        yield Path("deactivate.nu")

    def replacements(self, creator, dest_folder):
        # Due to nushell scoping, it isn't easy to create a function that will
        # deactivate the environment. For that reason a __DEACTIVATE_PATH__
        # replacement pointing to the deactivate.nu file is created
        virtual_env = ensure_text(str(creator.dest))
        bin_name = ensure_text(str(creator.bin_dir.relative_to(creator.dest)))

        return {
            "__VIRTUAL_PROMPT__": "" if self.flag_prompt is None else self.flag_prompt,
            "__VIRTUAL_ENV__": virtual_env,
            "__VIRTUAL_NAME__": creator.env_name,
            "__BIN_NAME__": bin_name,
            "__PATH_SEP__": ensure_text(os.pathsep),
            "__DEACTIVATE_PATH__": str(Path(virtual_env, bin_name, "deactivate.nu")),
        }
