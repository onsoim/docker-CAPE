# Copyright (C) 2016 Kevin Ross
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature

try:
    import re2 as re
except ImportError:
    import re

class RansomwareMessage(Signature):
    name = "ransomware_message"
    description = "Writes a potential ransom message to disk"
    severity = 3
    categories = ["ransomware"]
    authors = ["Kevin Ross"]
    minimum = "1.3"
    evented = True
    match = True

    def __init__(self, *args, **kwargs):
        Signature.__init__(self, *args, **kwargs)
        self.ransomfile = []
        self.indicators = [
            "your files",
            "your data",
            "your documents",
            "restore files",
            "restore data",
            "restore the files",
            "restore the data",
            "recover files",
            "recover data"
            "recover the files",
            "recover the data",
            "has been locked",
            "pay fine",
            "pay a fine",
            "pay the fine",
            "decrypt",
            "encrypt",
            "recover files",
            "recover data",
            "recover them",
            "recover your",
            "recover personal",
            "bitcoin",
            "secret server",
            "secret internet server",
            "install tor",
            "download tor",
            "tor browser",
            "tor gateway",
            "tor-browser",
            "tor-gateway",
            "torbrowser",
            "torgateway",
            "torproject.org",
            "ransom",
            "bootkit",
            "rootkit",
            "payment",
            "victim",
            "AES128",
            "AES256",
            "AES 128",
            "AES 256",
            "AES-128",
            "AES-256",
            "RSA1024",
            "RSA2048",
            "RSA4096",
            "RSA 1024",
            "RSA 2048",
            "RSA 4096",
            "RSA-1024",
            "RSA-2048",
            "RSA-4096",
            "private key",
            "personal key",
            "your code",
            "private code",
            "personal code",
            "enter code",
            "your key",
            "unique key"
    ]


    filter_apinames = set(["NtWriteFile"])

    def on_call(self, call, process):
        if call["api"] == "NtWriteFile":
            filescore = 0
            buff = self.get_raw_argument(call, "Buffer").lower()
            filepath = self.get_raw_argument(call, "HandleName")
            patterns = "|".join(self.indicators)
            if (filepath.lower() == "\\??\\physicaldrive0" or filepath.lower().startswith("\\device\\harddisk")) and len(buff) >= 128:
                if len(set(re.findall(patterns, buff))) > 1:
                    if filepath not in self.ransomfile:
                        self.ransomfile.append(filepath)

    def on_complete(self):
        if "dropped" in self.results:
            for dropped in self.results["dropped"]:
                mimetype = dropped["type"]
                if "ASCII text" in mimetype:
                    filename = dropped["name"]
                    data = dropped["data"]
                    patterns = "|".join(self.indicators)
                    if len(data) >= 128:
                        if len(set(re.findall(patterns, data))) > 1:
                            if filename not in self.ransomfile:
                                self.ransomfile.append(filename)

        if len(self.ransomfile) > 0:
            for filename in self.ransomfile:
                self.data.append({"ransom_file" : "%s" % (filename)})
            return True

        return False
