# Lark Bot Integration

## Steps

1. Create app at open.larksuite.com
2. pip install lark-oapi
3. Enable im.message.receive_v1 (WebSocket mode)

## Example

```python
import os, json, lark_oapi as lark
from lark_oapi.api.im.v1 import *
APP_ID = os.environ['LARK_APP_ID']
APP_SECRET = os.environ['LARK_APP_SECRET']
def handle(data):
    msg = data.event.message
    print(json.loads(msg.content).get('text',''))
handler = lark.EventDispatcherHandler.builder('','').register_p2_im_message_receive_v1(handle).build()
lark.ws.Client(APP_ID, APP_SECRET, event_handler=handler).start()
```

## Alternative Platforms

Same pattern works for Slack, Discord, Microsoft Teams.
