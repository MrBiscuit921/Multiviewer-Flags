import time
import requests
# https://coolbiscuit923-2931849.postman.co/workspace/Mr-Biscuit's-Workspace~2be5d73e-bcb8-4e41-8397-3f3b897bb96b/request/53324769-2754a974-2a3a-42ab-9024-8964ba26344e?action=share&creator=53324769

STATUS_URL = "http://localhost:10101/api/v1/live-timing/TrackStatus"
SIGNAL_URL = "http://localhost:16034/canvas/event"

EVENTS = {
    "1": "allClear",
    "2": "yellowFlag",
    "3": "sectorClear",
    "4": "safetyCarDeployed",
    "5": "redFlag",
    "6": "virtualSafetyCarDeployed",
    "7": "virtualSafetyCarEnding",
}

lastStatus = None

while True:
    try:
        data = requests.get(STATUS_URL, timeout=5).json()
        if data and data["Status"] != lastStatus:
            status = data["Status"]

            event = EVENTS.get(status)
            params = {"sender": "F1_Multiviewer", "event": event}
            if event:
                response = requests.post(SIGNAL_URL,params=params)

            lastStatus = status  # only update after a successful send
    except Exception: pass

    time.sleep(0.5)