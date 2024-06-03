<img align="right" width="100" height="100" src="images/PQ_logo.PNG">

# i4Q Data-Driven Continuous Process Qualification

## General Description
Process  Qualification  is  a  common industrial application  to  evaluate  machine  parameters  in  relation to quantitative quality measurement. Keeping these parameters in a predefined range is crucial for manufacturing products of the same quality. Therefore, descriptive statistics is required to check samples to a desired level of confidence if all produced goods stay in the same range of quality. Since  this  approach  can  only  evaluate already manufactured  products  and  is  not  including  a real-time  component, all  produced  goods between  the  time  a  failure  was  identified  and  the current point of time are classified as waste. To counteract these day-to-day issues, sensor data that describes  important  process parameters  are  combined  to  a  predictive  statistical  model which will forecast the process quality as Cpk-value in a specific time frame to a certain level of confidence. Furthermore,  the  collection  of  real-time  data enables a  continuous as-is  evaluation  to  interact when the prediction was not precise enough. 

## Features
This i4Q Solution offers following features:
- Continuously evaluating process parameter Cpk: reading real-time data streams and presenting them over specified time range or product quantity transformed to non-normality performance index. Furthermore, single parameters can be adjusted by inserting them in a sidebar to create personalized analysis. 
- Indication of distribution characteristics: to inform the process owner about the distribution over the specified time range or product quantity, a distribution plot and the highlighted confidence interval of the last number of chosen products is displayed. 
- Capacity forecast and forecast accuracy: as information about the chosen time range into the future, a forecast about the process capacity is made concerning the current conditions of the machine. Additionally, the evaluation criteria of the forecast algorithm are provided to leave the decision about further actions in the process owners responsibility. 

## Comercial information
# Authors
Organization                                | Website                       | Logo                                                          |
--------------------------------------------|-------------------------------|---------------------------------------------------------------|
Technical University of Berlin              | https://www.tu.berlin/        | <img src="images/TU_logo.PNG" alt="TUB" width="250"/>     |
Polytechnic University of Valencia          | https://www.upv.es/en         | <img src="images/UPV_logo.PNG" alt="UPV" width="250"/>    |
IKERLAN                                     | https://www.ikerlan.es/en/    | <img src="images/IKER_logo.PNG" alt="IKER" width="250"/>   |
EXOS                                        | https://exos-solutions.com/   | <img src="images/EXOS_logo.PNG" alt="EXOS" width="250"/>   |


### License
There is no licensing involved for using this software.

### Pricing
Subject             | Value         
-------------       | -------------  
Payment Model       | Open-Source     

## Associated i4Q Solutions
### Required
Runs as stand-alone solution.

### Optional
- i4Q Security Handler
- i4Q Data Repository
- i4Q Data Integration and Transformation
- i4Q Rapid Quality Diagnosis

## Technical Development
This i4Q Solution has the following development requirements:
- Development Language:  Python >= 3.9
- Container: Docker
- Deployment/Orchestration: -
- User Interface: -
- Application Interfaces: 
- Database engine:  i4QDR (helpful but optional)
- Python libraries: streamlit, fedot, matplotlib, pandas

<!-- ### API Specification
Resource      | POST            | GET           | PUT           | DELETE
------------- | -------------   | ------------- | ------------- | -------------
/xxx          |                 | Supported     | Not Supported |
/xxx          |                 | Supported     |               |
/xxx          |Supported        |               |               |
/xxx          |                 |               |               | Supported -->


## System Requirements
- docker requirements:
-- 4 GB Ram
-- 64-bit operating system
-- Hardware virtualisation support

### Installation Guidelines
Resource                 | Location         
-------------            | -------------  
Last release (v.1.0.0)   | https://gitlab.com/i4q/PQ/-/tree/main/subsystems/streamlit-multiapps    

### Installation

1. Clone the repository:
```
$ git clone https://gitlab.com/i4q/PQ.git
$ cd subsystems/streamlit-multiapps
```

2. Install dependencies:
```
$ pip install -r requirements.txt
```

3. Start the application:
```
streamlit run app.py
```

## User Manual

1. Provide your data connection
2. Insert upper and lower limits
3. Choose Forecast Length and variable of interest 
4. click on checkbox to see structural quality assurance
