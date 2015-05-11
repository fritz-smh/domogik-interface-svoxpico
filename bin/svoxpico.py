#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Plugin purpose
==============

Svoxpico (tts)

Implements
==========

- TtsManager

@author: Fritz <fritz.smh@gmail.com>
@copyright: (C) 2007-2015 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

from domogik.interface.common.interface import Interface

import tempfile
import threading
import traceback
import os
from subprocess import Popen, PIPE

MEDIA_AUDIO = "audio"

# file where we generate the output 
TTS_FILE="{0}/tmptts.pico2wave.wav".format(tempfile.gettempdir())


class TtsManager(Interface):
    """ Tts
    """

    def __init__(self):
        """ Init plugin
        """
        Interface.__init__(self, name='svoxpico')

        # check if the client is configured. If not, this will stop the client and log an error
        if not self.check_configured():
            return

        ### configuration
        # TODO

        #self.voice = "fr-FR"
        self.voice = self.get_config("language")

        # location
        self.location = "bureau"

        ### check if pico2wave is installed
        # TODO

        ### check if aplay is installed
        # TODO

        ### Create the speak engine
        self.speaker = Speak(self.log, voice = self.voice)

        ### ready
        self.ready()

    def process_response(self, response):
        """ Process the butler response
        """
        self.speaker.tell(response['text'])

 
class Speak():
    """ Speak with svoxpico
    """

    def __init__(self, cb_log, voice = "fr-FR"):
        """ Set up the speak engine
            @param cb_log : callback for domogik logger
            @param voice : fr-FR, en-EN, ...
        """
        self.log = cb_log
        self.log.info(u"Initialize!")

        self.voice = voice
        self.log.debug(u"Voice set to : {0}".format(voice))


    def tell(self, message):
        """ Tell the message with espeak
        """
        self.log.info(u"Tell : {0}".format(message))
        tts = u"pico2wave --lang={2} -w {0} \"{1}\" && aplay {0}".format(TTS_FILE, message, self.voice)
        self.log.debug(u"Command : {0}".format(tts))

        subp = Popen(tts,
                     shell=True)
        pid = subp.pid
        subp.communicate()



if __name__ == "__main__":
    tts = TtsManager()
