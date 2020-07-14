"""
Class for combine multiple prediction nodes based on the output of a main detector model.
The regions output of the detector are passed on other nodes (Classification or detection)
based some rules.

Cascade Prediction Node
 - Get predictions from a main detector
 - Results are passed to specialized classifiers/detector

All the predictions are obtained from other nodes
Classifiers are run in a concurrent requests
Inputs are:
    - Detector node direction
    - Subregion to be cropped from detector result
    - Subregions dict (detector-output : classifier-node)

EXAMPLE
conf:{
    'max_concur_req': 10,
    'main_model':{
        'model_path': '/path/to/main/mode.ml',
        'zip_path': '/path/to/architecture.zip'
    }
     'sub_models':
        {
            'person':

                [
                    {
                        'model_path': '/path/to/sub_mode.ml',
                        'zip_path': '/path/to/architecture.zip',
                        'weights': (0,0,1,1),
                        'conditions':['square_h']

                    },
                ],
            ...
        }
}
Use *all* for pass all the subregions in a classifier

MODELS
Each model is loaded from two files:
- .zip -> architecture
- .ml -> model weights and configuration

ROI
    The roi inside the located class by the detector is defined by weights
    Each weight from 0-1 of the values: (xi, yi, w, h)
    Where 0 -> xi | 1 -> xi+W
    Example:
        "roi_weights": (0.1, 1, 0.5, 1),
        "roi_conditions": ["center_x", ],

    - Conditions:
        * center_x: center x direction
        * center_y: center y direction
        * square_w: square to width (after weighted)
        * square_h: square to height (after weighted)


JCA
Vaico
"""
import json
from concurrent import futures
import logging

from MLcommon.loader import load_zip_model
from MLcommon.PredictionStrategies.auxfunc.cropper import crop_rect


class Cascade:
    """
    Cascade strategy of passing the input for several models to build a final prediction.
    Usually general prediction is returned by a Detector and specialized Classifiers
    run on the output of the detector.
    Instantiate outside lambda_function.
    """
    def __init__(self, conf):
        """
        :param max_concur_req: (int) max number of concurrent requests to specialized nodes
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info('Instantiating Cascade prediction strategy')
        self.max_concur_req = conf['max_concur_req'] if 'max_concur_req' in conf else 1
        self.conf = dict(conf)

        self.logger.info('Loading main model from: {}'.format(conf['main_model']['model_path']))
        self.conf['main_model']['model'] = load_zip_model(conf['main_model']['model_path'],
                                                          conf['main_model']['zip_path'])
        for roi, models in self.conf['sub_models'].items():
            self.logger.info('Loading models for {}'.format(roi))
            for model_conf in models:
                self.logger.info('Loading sub-model from: {}'.format(model_conf['model_path']))
                model_conf['model'] = load_zip_model(model_conf['model_path'], model_conf['zip_path'])


    def predict_one(self,model, frame):
        return model.predict(frame)

    def calc_max_concur_req(self, preds_from_main):
        """
        Calculate the maximum number of concurrent requests based the max number and the
        :param max_concur_req:
        :return:
        """
        max_requests = min(self.max_concur_req, len(preds_from_main))

        return max_requests

    def predict(self, frame):
        # Run detector
        self.logger.info('Predicting with main model on Cascade')
        areas = self.predict_one(self.conf['main_model']['model'], frame)
        concur_req = self.calc_max_concur_req(areas)
        self.logger.info('Number of workers: {}'.format(concur_req))

        # Deploy concurrent classification nodes
        future_roi = {}  # dict to asociate a future with the region on the image
        idx = 0  # roi index

        with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:
            for roi in areas:
                if roi.label in self.conf['sub_models']:
                    roi.subobject = []
                    for model in self.conf['sub_models'][roi.label]:
                        area = {
                            'xmin': roi.geometry.xmin,
                            'ymin': roi.geometry.ymin,
                            'xmax': roi.geometry.xmax,
                            'ymax': roi.geometry.ymax,
                        }

                        im_crop = crop_rect(
                            frame, area,
                            model['weights'],
                            model['conditions']
                        )
                        self.logger.debug('Predicting region with: {}'.format(model['model']))
                        future = executor.submit(self.predict_one, model['model'], im_crop)
                        future_roi[future] = idx

                idx += 1
            done_roi = futures.as_completed(future_roi)

            # Add subregions predictions
            for future in done_roi:
                # Return future one by one as they be done
                pred = future.result()[0]
                areas[future_roi[future]]['subobject'].append(pred)

        print(areas)

        return areas
