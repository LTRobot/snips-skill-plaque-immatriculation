#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)

def add_zeros(num):
   
    num = str(num)

    if(int(num) < 100):

        if(int(num) < 10):

            num = "0"+num

        num = "0"+num

    return num


def action_wrapper(hermes, intentMessage, conf):

    plaque_letter_1 = intentMessage.slots.letter_1.first().value
    plaque_letter_2 = intentMessage.slots.letter_2.first().value
    plaque_num = int(intentMessage.slots.numero.first().value)
    plaque_num = add_zeros(plaque_num)
    plaque_letter_3 = intentMessage.slots.letter_3.first().value
    plaque_letter_4 = intentMessage.slots.letter_4.first().value

    if(plaque_num != "" and len(plaque_num) == 3 and plaque_letter_1 != "" and plaque_letter_2 != "" and 
            plaque_letter_3 != "" and plaque_letter_4 != ""):

        result_sentence = "Est-ce bien la plaque {0} {1} {2} {3} {4} ?".format(plaque_letter_1[0],
                plaque_letter_2[0], plaque_num, plaque_letter_3[0], plaque_letter_4[0])
    else:
        result_sentence = u"Format incorrect, veuillez réessayer."

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    
    


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("LTRobot:askPlate", subscribe_intent_callback) \
         .start()
