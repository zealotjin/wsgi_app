## Sharing Data in a Gunicorn + Flask application 
Example code for sharing data in a Python WSGI HTTP Server
Detailed explanation can be found [here](https://medium.com/@jgleeee/sharing-data-across-workers-in-a-gunicorn-flask-application-2ad698591875) @ Medium


### Setup
- Please refer to the `requirements.txt`
- ```
  $ pip install -r requriements.txt
  ```


### Run
- To run the server, please refer to `run.sh`
- ```
  $ bash run.sh
  ```
- Default app configurations are:
  - `--num-workers`: 5
  - `--port`: 8080


### Test
- To test the following behavior, please find the appropriate commands below.
- Global variables
  - ```
    $ bash run.sh test_global_variable
    ```
- Test multiprocess Value
  - ```
    $ bash run.sh test_mp_value 
    ```
- Test multiprocess array
  - ```
    $ bash run.sh test_mp_array 
    ```
- Test multiprocess manager
  - ```
    $ bash run.sh test_mp_manager 
    ```
- Test Signal handling
  - ```
    $ bash run.sh test_signal_handling 
    ```