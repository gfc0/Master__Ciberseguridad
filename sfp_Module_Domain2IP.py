# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_Module_Domain2IP_GCASTILLO
# Purpose:      SpiderFoot plug-in for creating new modules.
#
# Author:      Alumno Gianfranco Castillo
#
# Created:     17/02/2022
# Copyright:   (c) Gianfranco Castillo 2022
# Licence:     GPL
# -------------------------------------------------------------------------------
from spiderfoot import SpiderFootEvent, SpiderFootPlugin
import subprocess
class sfp_Module_Domain2IP_GCASTILLO(SpiderFootPlugin):

    meta = {
        'name': "Module_Domain2IP_Gianfranco_Castillo",
        'summary': "Leccion2",
        'flags': [""],
        'useCases': ["Passive"],
        'categories': ["Passive DNS"]
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    def watchedEvents(self):
        return ["DOMAIN_NAME"] 
    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["IP_ADDRESS"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")

        try:
            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")
            data = subprocess.run("ping -c 1 "+eventData,shell=True, text=True, capture_output=True)
            outdata = data.stdout
            splitted = outdata.split(" ")
            ip = splitted[2]
            ipdef = splitted[2][1:-1]

            if not ipdef:
                self.sf.error("Unable to perform <ACTION MODULE> on " + eventData)
                return
        except Exception as e:
            self.sf.error("Unable to perform the <ACTION MODULE> on " + eventData + ": " + str(e))
            return




        evt = SpiderFootEvent("IP_ADDRESS", ipdef, self.__name__, event)
        self.notifyListeners(evt)


# End of sfp_Module_Domain2IP_GCASTILLO class
