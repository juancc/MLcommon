# Vaico - Visual Artificial Intelligence
This package contains Abstract class for Machine Learning models with explicit model protocol.
Instantiate AbcModel for create a new model and ensure better server compatibility.

## New model repository layout
 For better practice assign the same package name for the model class name:
```bash
Repo
|
|
|--- newArchitecture
       |
       |
       |--- NewArchitecture.py
```

## AbcModel methods

Implement required methods and set a dict of the default model parameters (Intended for the user to modify the model behaviour) in a variable **_defaults**. 

All the keywords parameters are loaded as instance variables and also stored in _defaults variable

```python
from MLcommon import AbcModel

class NewModel(AbcModel):
    _defaults = {
        'labels': None,
        'train_epsilon': 0.15
        'any_other': None
    }               
  
```

# Zip architectures
For share a new architecture compress it in zip format under the folder python for AWS lambda compatibility. Install the requirements of each architecture


# Prediction strategies:
## Cascade
Class for combine multiple prediction models based on the output of a main detector model.
The regions output of the detector are passed on other nodes (Classification or detection)
based some rules.

### Cascade Prediction Node
 - Get predictions from a main detector
 - Results are passed to specialized classifiers/detector

All the predictions are obtained from other nodes
Classifiers are run in a concurrent requests
Inputs are:
    - Detector node direction
    - Subregion to be cropped from detector result
    - Subregions dict (detector-output : classifier-node)

#### Example
```python
conf: {
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
```
Use *all* for pass all the subregions in a classifier


#### Models
Each model is loaded from two files:
- zip_path: path to architecture file (.zip)
- model_path: path to model file (.ml)

#### Roi
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


## License
All rights of this library belongs to Vaico Visión Artificial and no one may distribute, reproduce, or create derivative works.