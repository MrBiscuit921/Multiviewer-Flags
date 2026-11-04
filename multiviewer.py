import time
import requests

STATUS_URL = "http://localhost:10101/api/v1/live-timing/TrackStatus"
SECTOR_URL = "http://localhost:10101/api/v1/live-timing/TimingData"
SIGNAL_URL = "http://localhost:16034/canvas/event"

DRIVERNUMBER = "12"

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
lastSectors = None
lastErrors = {}

def classify(sector):
    if sector.get("OverallFastest"):
        return "Fastest"
    if sector.get("PersonalFastest"):
        return "Personal"
    return "None"

def sendEvent(event):
    if event:
        response = requests.post(SIGNAL_URL, params={"sender": "F1_Multiviewer", "event": event}, timeout=5)
        response.raise_for_status()

def report(name, error):
    """Print an error once, instead of every half second."""
    message = f"{name} failed: {error}"
    if lastErrors.get(name) != message:
        print(message)
        lastErrors[name] = message

while True:
    try:
        statusData = requests.get(STATUS_URL, timeout=5).json()
        if statusData and statusData["Status"] != lastStatus:
            status = statusData["Status"]

            event = EVENTS.get(status)
            sendEvent(event)

            lastStatus = status
        lastErrors.pop("Flags", None)
    except Exception as error:
        report("Flags", error)

    try:
        sectorData = requests.get(SECTOR_URL, timeout=5).json()
        if sectorData:
            sectors = []

            for sector in sectorData["Lines"][DRIVERNUMBER]["Sectors"]:
                sectors.append(classify(sector))

            if sectors != lastSectors:
                print("sector:"+",".join(sectors))
                sendEvent("sector_"+"_".join(sectors))

                lastSectors=sectors
            lastErrors.pop("Sectors", None)
    except Exception as error:
        report("Sectors", error)
                    

    time.sleep(0.5)