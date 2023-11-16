from datetime import datetime as dt

class RequestTracker:

    def __init__(self):
        self.requestIDs = {}

    def newRequest(self, requestID: str):
        self.requestIDs[requestID] = [("CREATED", dt.now())]
        return len(self.requestIDs)
    
    def resolveRequest(self, requestID: str):
        self.requestIDs.pop(requestID)
        return len(self.requestIDs)
    
    def getTimeDelta(self, requestID: str):
        if requestID in self.requestIDs:
            return self.requestIDs.get(requestID)
        else:
            return 0
        
    def updateRequest(self, requestID: str, status: str):
        if not (requestID in self.requestIDs):
            return
        currentEntry = self.requestIDs[requestID]
        newEntry = [(status, dt.now()), currentEntry]
        self.requestIDs[requestID] = newEntry