#!/usr/bin/env python
'''
gRPC Classification Server
for https://elections.mediawatch.io
'''

import time
import grpc
import logging
import argparse

from concurrent import futures

from numpy import max, argmax
from pandas import read_csv
from sklearn.ensemble import RandomForestClassifier

# Import Generated code by the gRPC Python protocol compiler plugin.
import classification_pb2_grpc as ClassificationServer
from classification_pb2 import UserFeatures, UserClass


FORMAT = '[EMCLGRPC] %(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)


class Classification(ClassificationServer.ClassificationServicer):
    '''
    Classification extends classification_pb2_grpc.ClassificationServicer
    '''
    def __init__(self, model):
        '''
        Constructor
        
        '''
        # Load model file
        # 
        self.model = read_csv(model)
        logging.info('Model: `%s` Loaded', model)

        self.x = self.model.values[:, 1:]
        self.y = self.model.values[:, 0]
        
        self.classes = []

        self.clf = RandomForestClassifier(
            n_jobs=1, criterion='entropy', n_estimators=33, random_state=42, max_depth=18, min_samples_leaf=1
        )
        
        self.Fit()
    
    def Fit(self):
        '''
        Fit Prediction Model
        Set x, y dimmensions and fit the model
        '''
        fit = self.clf.fit(self.x, self.y)
        logging.info('Forest Fitted')
        
        self.classes = fit.classes_
        logging.info('Model Classes %s', self.classes)
    
    def Classify(self, data, context):
        '''
        Classify gRPC endpoint
        UserFeatures:
            'Followers', 'Friends', 
            'Statuses', 'Favorites', 'Lists', 'FFR', 'STFV'
        UserClass:
            Label: 'ACTIVE' 'INFLUENCER' 'AMPLIFIER' 'OTHER' 'UNKNOWN' 'NEW'
            Score: double
        Runs the classifier (random forest) with UserFeatures
        Returns UserClass
        '''
        features = [
            data.followers, data.friends, data.statuses,
            data.favorites, data.lists, data.ffr, data.stfv
        ]
        # Probability
        proba = self.clf.predict_proba([features])
        # Select class with hiegher proba
        predict = self.classes[argmax(proba)]
        logging.info('Prediction -- CLASS: %s | SCORE: %s',
                     predict, proba)
        return UserClass(label=predict, score=max(proba))


def serve(host, port, model):
    '''
    Start gRPC Classification Server
    '''
    # Create Server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Attach gRPC Servicer to Server
    ClassificationServer.add_ClassificationServicer_to_server(Classification(model), server)
    
    # Start Server
    logging.info('Starting Server')
    server.add_insecure_port('{}:{}'.format(host, port))
    server.start()
    logging.info('Server Listening on %s:%d', host, port)

    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Serve GRPC Classification Server'
    )
    parser.add_argument(
        '--host, -h', dest='host', help='Host Address', default='[::]'
    )
    parser.add_argument(
        '--port, -p', dest='port', help='Host Port', default=50051
    )
    parser.add_argument(
        '--model, -m',  dest='model', help='Path to Trainned Model', default='data/classifier.dat'
    )
    args = parser.parse_args()
    logging.debug('%s', args)
    serve(args.host, args.port, args.model)
