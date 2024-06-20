# Sebatik Cloud Computing
![291132714-ed84e5bf-4c56-45cc-ba91-e99c6d8e4aab](https://github.com/Sebatik/Backend/assets/139910446/d2081f8b-56e5-4b31-ac7c-6377b6fd8f8a)

# Overview
```
We are developing two APIs, each using a different framework. The APIs we are building include:

1. An API for predicting images using a machine learning model with the Flask framework and Python programming language.
2. An API to get all batik data from the database, using the Node.js framework and JavaScript programming language.

The deployment of these two APIs differs for several reasons. 

Firstly, we deploy the ML API on Cloud Run because App Engine does not support TensorFlow 2.15.0, which is a requirement for our API to function since the model was created using TensorFlow 2.15.0.

Secondly, for the API to get all batik data, we decided to use App Engine standard environment. This decision was made because the creation of this API is relatively simple.
```

# Technology Used
## Cloud Run
<img src="https://github.com/Sebatik/Back-end/assets/139910446/29aa9e61-808d-4e69-a895-26c8084324cb" width="100px">

``` 
  Location : asia-southeast2 (Jakarta) 
  Memory : 2 GiB 
  vCPUs : 2 
```

## Cloud SQL
<img src="https://github.com/Sebatik/Back-end/assets/139910446/ffce3e5b-c850-4f59-bfed-a34f19d18ad5" width="100px">

``` 
  Database type: mysql
  Version : 8.0 
  Memory : 8 GB 
  Storage : 100 GB 
  vCPUs : 2
```
## Cloud APP Engine
<img src="https://github.com/Sebatik/Back-end/assets/139910446/95dce91a-2ccd-4dc0-ad9a-fb47e5ab90dd" width="100px">

``` 
  Location : asia-southeast2 (Jakarta)
  Runtime : nodejs
  CPU: 1
  Memory: 0.5 GB
  Disk size: 10 GB
  OS : Ubuntu22
```

## Cloud Artifact Registry
<img src="https://github.com/Sebatik/Back-end/assets/139910446/a4c5f82c-da4b-4144-8028-ff3a0ca90b67" width="100px">

``` 
  Storage : 10 GB...
```

## Cloud Storage
<img src="https://github.com/Sebatik/Back-end/assets/139910446/c0e17ab2-3069-4d72-beb8-8f10f9d8fce8" width="100px">

``` 
  Location Type : Region 
  Location : asia-southeast2 (Jakarta)
  Storage Class : Standard

  Location Type : Multi-region
  Location : US
  Storage Class : Standard
```
## Python Language
<img src="https://github.com/Sebatik/Back-end/assets/139910446/e8ce1600-4694-48f9-ad11-ffcdfcd63a04" width="100px">


## Node JS Language
<img src="https://github.com/Sebatik/Back-end/assets/139910446/a2560a8d-33af-470a-9e65-f7cfd41a2195" width="100px">


# Instalation
### 1. Clone the repositories : 
```
  git clone https://github.com/Sebatik/Back-end.git
```

### 2. Install dependencies file : 
```
  - Predict Repositories :  pip freeze > requirements.txt
                            pip install -r requirements.txt

  - Batik Repositories   :  npm install
```

### 3. Start : 
```
  - Predict Repositories :  python app.py

  - Batik Repositories   :  node start
```
