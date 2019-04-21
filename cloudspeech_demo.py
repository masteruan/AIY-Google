#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""
import argparse
import locale
import logging
import time

from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient
import aiy.voice.tts

def get_hints(language_code):
    if language_code.startswith('it_'):
        return ('accendi led',
                'spegni led',
                'lampeggia led',
                'ciao',
                'ripeti dopo di me')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Inizializzando per la lingua %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    with Board() as board:
        while True:
            if hints:
                logging.info('Dimmi qualcosa tipo. %s.' % ', '.join(hints))
            else:
                logging.info('Dimmi qualcosa.')
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            if text is None:
                logging.info('Non hai detto nulla.')
                continue

            logging.info('Hai detto: "%s"' % text)
            text = text.lower()
            if 'accendi led' in text:
                board.led.state = Led.ON
            elif 'spegni led' in text:
                board.led.state = Led.OFF
            elif 'lampeggia led' in text:
                board.led.state = Led.BLINK
            elif 'ripeti dopo di me' in text:
                to_repeat = text.replace('ripeti dopo di me', '', 1)
                #to_repeat = (to_repeat).encode('utf-8')
                aiy.voice.tts.say(to_repeat,lang='it-IT')
            elif 'ciao' in text:
                break

if __name__ == '__main__':
    main()
