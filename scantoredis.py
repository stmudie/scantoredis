from epics import PV, caget
from time import sleep
import redis
import cPickle as pickle
from threading import Thread

class ScanToRedis():

    def __init__(self):

        self.scanBasePV = 'SMTEST:scan1'
        
        self.detActive = ['']*70
        self.detPVArray = []
        self.detPVName = []
        for i in range(1,71):
            pvarray = '%s.D%02dCA' % (self.scanBasePV,i)
            pvname = '%s.D%02dPV' % (self.scanBasePV,i)
            self.detPVArray.append(PV(pvarray))
            self.detPVName.append(PV(pvname))
        
        self.posArray = PV(self.scanBasePV+'.P1CA')
        self.currentPoint = PV(self.scanBasePV+'.CPT', callback = self.CPTCallback)

        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    
        
    
    def CPTCallback(self, pvname, value, **kwargs):
        th = Thread(target=self.SendToRedis,args=(value,))
        th.start()

    def SendToRedis(self,cpt):
        
        if cpt == 0:
            self.redis.publish('scantoredis:message','NewScan')
            for i,pv in enumerate(self.detPVName):
                self.detActive[i] = pv.get()
        
        self.redis.set('scantoredis:pos1',pickle.dumps(self.posArray.get(use_monitor=False)[0:cpt]))
        self.redis.set('scantoredis:detActive',pickle.dumps(self.detActive))
        
        for i,pv in enumerate(self.detPVArray):
            if self.detActive[i] != None:
                self.redis.set('scantoredis:det%02d' % (i+1,),pickle.dumps(pv.get(use_monitor=False)[0:cpt]))
    
        self.redis.publish('scantoredis:message','NewPoint')
        

if __name__ == '__main__':
    a = ScanToRedis()
    while True:
        sleep(0.01)