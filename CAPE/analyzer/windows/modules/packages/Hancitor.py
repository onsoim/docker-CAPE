# CAPE - Config And Payload Extraction
# Copyright(C) 2015-2017 Context Information Security. (kevin.oreilly@contextis.com)
# See the file 'docs/LICENSE' for copying permission.

import os
import shutil

from lib.common.abstracts import Package

class Hancitor(Package):
    """CAPE Hancitor analysis package."""

    def __init__(self, options={}, config=None):
        """@param options: options dict."""
        self.config = config
        self.options = options
        self.pids = []
        self.options["dll"] = "Hancitor.dll"
        #self.options["dll_64"] = "Hancitor_x64.dll"

    def start(self, path):
        args = self.options.get("arguments")
        
        # If the file doesn't have an extension, add .exe
        # See CWinApp::SetCurrentHandles(), it will throw
        # an exception that will crash the app if it does
        # not find an extension on the main exe's filename
        if "." not in os.path.basename(path):
            new_path = path + ".exe"
            os.rename(path, new_path)
            path = new_path

        return self.execute(path, args, path)
