from __future__ import absolute_import
from datetime import datetime
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
    
    @Core.periodic(settings.MESSAGE_INTERVAL)
    def publish_test_message(self):
        '''publish test REST API messages '''
        print('publishing a new CTAevent message...')
        
        self.EventID += 1
        now = datetime.utcnow().isoformat(' ') + 'Z'
        
        mesdict = {"message_target": "all",
                   "message_subject": "new_event",
                   "event_uid": str(self.EventID),
                   "event_name": "shed",
                   "event_duration": "4"
                   }
        
        message = json.dumps(mesdict)
        print(message)
        
        self.vip.pubsub.publish('pubsub','CTAevent',{}, message)
        
def main(argv=sys.argv):
    '''main method called by the eggsecutable'''
    try:
        utils.vip_main(TestMessageOriginatorAgent)
    except Exception as e:
        _log.exception(e)
                
if __name__ == '__main__':
    #entry point for script
    sys.exit(main())