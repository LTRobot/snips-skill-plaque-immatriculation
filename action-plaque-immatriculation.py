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


def action_wrapper(hermes, intentMessage, conf):

    plaque_bloc_g = intentMessage.slots.bloc_gauche.first().value
    plaque_num = intentMessage.slots.numero.first().value
    plaque_bloc_d = intentMessage.slots.bloc_droit.first().value

    result_sentence = "Est-ce bien la plaque {0} {1} {2} ?".format(plaque_bloc_g,
            str(plaque_num),plaque_bloc_d)
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)
    
    


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("LTRobot:askPlate", subscribe_intent_callback) \
         .start()
