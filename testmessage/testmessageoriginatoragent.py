from __future__ import absolute_import
from datetime import datetime, timedelta
import logging
import sys
import json

from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.agent import utils
from volttron.platform.messaging import headers as headers_mod

from . import settings

utils.setup_logging()
_log = logging.getLogger(__name__)

class TestMessageOriginatorAgent(Agent):
    EventID = 0
    
    def __init__(self, config_path, **kwargs):
        super(TestMessageOriginatorAgent, self).__init__(**kwargs)
        self.config = utils.load_config(config_path)
        self._agent_id = self.config['agentid']
        
        _log.info(self.config['message'])
        self._agent_id = self.config['agentid']
        
    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        _log.info(self.config['message'])
        self._agent_id = self.config['agentid']    
    
    def publish_test_message(self):
        '''publish test REST API messages '''
        print('publishing a new CTAevent message...')
        
        self.EventID += 1
        now = datetime.utcnow().isoformat(' ') + 'Z'
        
        mesdict = self.supplyMessageDict((self.EventID % 10) + 1)
        
        mesdict["message_target"] = "all"
        mesdict["message_subject"] = "new_event"
        mesdict["event_uid"] = str(self.EventID)
        mesdict["priority"] = "1"
        #set the start time for a minute from now
        mesdict["ADR_start_time"] = (datetime.utcnow() + timedelta(minutes = 1)).isoformat() + 'Z'
        
        message = json.dumps(mesdict)
        print(message)
        
        self.vip.pubsub.publish('pubsub','CTAevent',{}, message)
        
    @Core.periodic(settings.MESSAGE_INTERVAL)    
    def periodic_messaging(self):
        ''' post messages to be delivered at almost the same future time'''
        #self.publish_test_message()
        self.EventID += 1
        #self.publishADRmessage(self.EventID % 5)
        self.publishESIFtest(self.EventID % 5)
    
    def publishESIFtest(self,choice):
        start = (datetime.utcnow() + timedelta(minutes = 1)).isoformat() + 'Z'
        mesdict = {"event_ID": str(self.EventID),
                   "event_name": "simple_signal",
                   "priority": "1",
                   "start_time": start,
                   "duration": "60S"}
        if choice == 0:
            mesdict["signalPayload"] = 0
        elif choice == 1:
            mesdict["signalPayload"] = 1
        elif choice == 2:
            mesdict["signalPayload"] = 2
        elif choice == 3:
            mesdict["signalPayload"] = 3
        elif choice == 4:
            mesdict["signalPayload"] = 4    
            
        messtr = json.dumps(mesdict)
        print("publishing an openADR message to openADRevent: {message}".format(message = messtr))
        self.vip.pubsub.publish('pubsub','openADRevent',{}, messtr)
      
    
    def publishADRmessage(self,choice):
        start = (datetime.utcnow() + timedelta(minutes = 1)).isoformat() + 'Z'
        mesdict = {"event_ID": str(self.EventID),
                   "event_name": "simple_signal",
                   "priority": str(choice % 2),
                   "start_time": start,
                   "duration": "45S"
                   }
        if choice == 0:
            mesdict["signalPayload"] = 0
        elif choice == 1:
            mesdict["signalPayload"] = 1
        elif choice == 2:
            mesdict["signalPayload"] = 2
        elif choice == 3:
            mesdict["signalPayload"] = 3
        elif choice == 4:
            mesdict["signalPayload"] = 4    
            
        messtr = json.dumps(mesdict)
        print("publishing an openADR message to openADRevent: {message}".format(message = messtr))
        self.vip.pubsub.publish('pubsub','openADRevent',{}, messtr)
        
    def supplyMessageDict(self,choice):
        if choice == 1:
            mesdict = {"event_name": "shed",
                       "event_duration": "4",
                       "message_type": "shed"}
        elif choice == 2:
            mesdict = {"event_name": "normal",
                       "message_type": "normal"}
        elif choice == 3:
            mesdict = {"event_name": "critical_peak",
                       "event_duration": "134",
                       "message_type": "critical_peak"}
        elif choice == 4:
            mesdict = {"event_name": "grid_emergency",
                       "event_duration": "23",
                       "message_type": "grid_emergency"}
        elif choice == 5:
            mesdict = {"cur_price": "5.7",
                       "message_type": "cur_price"}
        elif choice == 6:
            mesdict = {"next_price": "3.4",
                      "message_type": "next_price"}
        elif choice == 7:
            mesdict = {"time_remaining": "24",
                      "message_type": "time_remaining"}
        elif choice == 8:
            mesdict = {"day": "3",
                      "hour": "12",
                      "message_type": "time_sync"}
        elif choice == 9:
            mesdict = {"message_type": "query_op_state"}
        elif choice == 10:
            mesdict = {"message_type": "info_request"}
            
        return mesdict 
        

def main(argv=sys.argv):
    '''main method called by the eggsecutable'''
    try:
        utils.vip_main(TestMessageOriginatorAgent)
    except Exception as e:
        _log.exception(e)
                
if __name__ == '__main__':
    #entry point for script
    sys.exit(main())