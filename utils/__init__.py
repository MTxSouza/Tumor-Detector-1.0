# libraries
from sklearn.metrics import precision_recall_fscore_support as score
from PIL import ImageTk, Image

import tensorflow as tf
import numpy as np
import logging
import cv2
import os


# configs
os.environ['XLA_PYTHON_CLIENT_PREALLOCATE'] = 'false'
os.environ['XLA_PYTHON_CLIENT_ALLOCATOR'] = 'platform'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


class Net:

    def __init__(self, _model:str, _log) -> None:
        tf.keras.backend.clear_session()
        try:
            self.__model = tf.keras.models.load_model(filepath=os.path.join('weights', _model))
        except Exception as e:
            _log.log('error', f'Could not load the {_model} model. {e}.')
        else:
            _log.log('info', f'{_model} model has been loaded.')
            self.__log = _log

    def inference(self, _image, _labels):
        try:
            _results = []
            for img in _image:
                _results.append(self.__model.predict(np.expand_dims(np.expand_dims(np.asarray(img), -1), 0)).argmax())
        except Exception as e:
            self.__log.log('critical', f'Something went wrong when inference was running. {e}.')
        return _results, score(_labels, _results)


class Logging:

    def __init__(self) -> None:
        logging.basicConfig(
            filename='tumor_log.log',
            filemode='w',
            format='[TIME]: %(asctime)s - [TYPE]: %(levelname)s - [LOG]: %(message)s',
            level=logging.DEBUG
        )

    def log(self, _type, _txt):
        if _type=='debug':
            return logging.debug(_txt)
        elif _type=='info':
            return logging.info(_txt)
        elif _type=='warning':
            return logging.warning(_txt)
        elif _type=='error':
            return logging.error(_txt)
        elif _type=='critical':
            return logging.critical(_txt)


def get_images(_n_img:int, _log) -> tuple:
    IMAGES=[]
    LABELS=[]
    _log.log('debug', 'Collecting images.')
    for cls in ['no','yes']:
        for img in np.random.choice(os.listdir(os.path.join('test',cls)), _n_img, replace=False):
            IMAGES.append(cv2.resize(cv2.imread(os.path.join('test', cls, img), cv2.IMREAD_GRAYSCALE), (224,224)))
            LABELS.append(1 if cls=='no' else 0)
    _log.log('debug', f'{IMAGES.__len__()} images has been collected.')
    return IMAGES, LABELS


def next_image(_index:list) -> int:
    return np.random.choice(_index, _index.__len__(), replace=False)

def load_image(_image, _size):
    return ImageTk.PhotoImage(image=Image.fromarray(_image).resize(size=_size))
