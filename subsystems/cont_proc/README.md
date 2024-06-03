# Continuous Process Qualification User Interface
A user interface in python to check if your manufacturing process is currently and in the future inbetween tolerance levels.

# How to Run via Terminal

1. Clone the repository:
```
$ git clone https://gitlab.com/i4q/PQ.git
$ cd subsystems/streamlit-multiapps/cont_proc
```

2. Install dependencies:
```
$ pip install -r requirements.txt
```

3. Either start the application via terminal:
```
streamlit run app.py
```

# How to Run via Docker

1. Clone the repository:
```
$ git clone https://gitlab.com/i4q/PQ.git
$ cd subsystems/streamlit-multiapps/cont_proc
```

2. Create docker container:
```
$ docker-compose up
```


# For Developers: How to add new app

1. Add a new python file in `apps/`  folder with a function named `app`.

```
# apps/new_app.py

import streamlit as st

def app():
    st.title('New App')
```

2. Now add it to `app.py`

```
from apps import newapp # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("New App", newapp.app)
```

That's it your new app is added to your application and is live in default browser.