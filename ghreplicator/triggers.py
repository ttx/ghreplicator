#! /usr/bin/env python

# Copyright 2017 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import paho.mqtt.client as mqtt


class MQTTTrigger:

    def __init__(self, callback, server, topic):
        self.client = mqtt.Client()
        self.server = server
        self.topic = topic

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))
            client.subscribe(self.topic)

        self.client.on_connect = on_connect

        def on_message(client, userdata, msg):
            data = json.loads(msg.payload)
            callback(data['project'], data['newRev'])

        self.client.on_message = on_message

    def run(self):
        # Connect to the firehose
        self.client.connect(self.server)
        # Listen forever
        self.client.loop_forever()
