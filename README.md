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

## License
All rights of this library belongs to Vaico Visión Artificial and no one may distribute, reproduce, or create derivative works.