# install python version 3.6

# install required packages including rasa and supportive packages
- pip install -r requirement.txt

# Commands to run project
To train rasa project
- rasa train

To run core server
- rasa run -m models --enable-api --cors "*"

To run action server
- rasa run actions