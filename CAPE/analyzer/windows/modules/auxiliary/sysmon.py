import logging
import os
import time
import threading
import subprocess
from lib.common.abstracts import Auxiliary
from lib.common.results import upload_to_host
from lib.core.config import Config

log = logging.getLogger(__name__)

__author__  = "@FernandoDoming"
__version__ = "1.0.0"

class Sysmon(threading.Thread, Auxiliary):

    def __init__(self, options={}, analyzer=None):
        threading.Thread.__init__(self)
        Auxiliary.__init__(self, options, analyzer)
        self.config = Config(cfg="analysis.conf")
        self.enabled = self.config.sysmon
        self.do_run = self.enabled
        self.startupinfo = subprocess.STARTUPINFO()
        self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    def clear_log(self):
        try:
           subprocess.call(["C:\\Windows\\System32\\wevtutil.exe", "clear-log", "microsoft-windows-sysmon/operational"], startupinfo=self.startupinfo)
        except Exception as e:
            log.error("Error clearing Sysmon events - %s" % e)


    def collect_logs(self):
        try:
                      subprocess.call(["C:\\Windows\\System32\\wevtutil.exe", "query-events", "microsoft-windows-sysmon/operational", "/rd:true", "/e:root", "/format:xml", "/uni:true"], startupinfo=self.startupinfo,  stdout=open("C:\\sysmon.xml", "w"))
        except Exception as e:
            log.error("Could not create sysmon log file - %s" % e)

        # Give it some time to create the file
        time.sleep(5)

        if os.path.exists("C:\\sysmon.xml"):
            upload_to_host("C:\\sysmon.xml", "sysmon/%s.sysmon.xml" % time.time())
        else:
            log.error("Sysmon log file not found in guest machine")


    def run(self):
        if self.enabled:
            self.clear_log()
            while self.do_run:
                self.collect_logs()
                time.sleep(15)

            return True
        return False

    def stop(self):
        if self.enabled:
            self.do_run = False
            self.collect_logs()
            return True
        return False
