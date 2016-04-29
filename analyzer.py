"""
This class describes the behavior of the Router Node
"""
import collections
import numpy as np
import scipy.stats as st

import logging
logging.basicConfig(filename='log.log', level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

import parser


class AnalysisEngine():

    period =0.05
    jitter =0.05
    lastMsgTime = 0
    sensorMin = 0
    sensorMax = 200
    slack = 0.01

    sampleSize = 30
    samples = sampleSize*[0]

    trueIntrusionDetected=False
    falseIntrusionDetected=False


    def __init__(self,period=None,jitter=None,msgCount=None):
        
        if period is not None:
            self.period = period
        if jitter is not None:
            self.jitter = jitter
        
        self.mean = self.period+self.jitter/2
        self.samples = collections.deque(self.sampleSize*[self.mean],maxlen=self.sampleSize)


    falsePositives = 0.0
    falseNegatives = 0
    msgsFrom3 = 0
    msgsFrom2 = 0
    def analyzemsg(self, time, sensor,ID,fwd):
        #update number of msgs
        node = ID
        if node is 3:
            self.msgsFrom3 +=1
        elif node is 2:
            self.msgsFrom2 += 1

        #update fp or FN
        if node is 3 and fwd is False:
            self.falsePositives +=1.0
        elif node is 2 and fwd is True:
            self.falseNegatives +=1.0

        #check of Intrusion
        totalMsgs = self.msgsFrom2+self.msgsFrom3
        if totalMsgs > self.sampleSize:
            sampleMean = sum(self.samples)/len(self.samples)
            standardErr = np.std(self.samples)/np.sqrt(self.sampleSize)
            zscore = (sampleMean-self.mean)/(standardErr)
            pValue = st.norm.cdf(zscore)

            #perform single tailed test to see if sample is 99%  less than mean
            if pValue < 0.01: 
                if totalMsgs > self.msgCount/2:
                    self.trueIntrusionDetected=True
                    print("true intrusion")
                else:
                    self.falseIntrusionDetected=True
                    print("false instrusion")
                    print(pValue)
                    print(standardErr)

    def results(self):
        if self.msgsFrom3 is not 0:
            fpRate = self.falsePositives/self.msgsFrom3 * 100
        else:
            fpRate = 0
        if self.msgsFrom2 is not 0:
            fnRate = self.falseNegatives/self.msgsFrom2 * 100
        else:
            fnRate = 0
        print(str(self.period)+"\t"+str(self.jitter)+"\t"+str(self.msgsFrom3)+"\t"+str(self.msgsFrom2)+"\t"+str(fpRate)+"\t"+str(fnRate)+"\t"+str(self.trueIntrusionDetected)+"\t"+str(self.falseIntrusionDetected))

    def analyze(self,dictData):
        startTime = 0
        
        for value in dictData:
            #set diff time
            diffTime = float(value['Time']) - startTime
            self.samples.append(diffTime)
            #reset time
            startTime = float(value['Time'])

            self.analyzemsg(float(value['Time']),float(value['Sensor']),int(value['ID']),bool(value['Forward']))

#driver
if __name__ == '__main__':
    ae = AnalysisEngine()
    traceDictionary =  parser.parseTrace('Routerlog.txt')
    ae.analyze(traceDictionary);
