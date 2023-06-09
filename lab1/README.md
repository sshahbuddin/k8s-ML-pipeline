# Appplication Information
1) What does this application do?  
  This fastAPI application runs locally on your machine. It outputs "hello <name>" based on the name query parameter in the '/hello?name=<name>' endpoint. 

2)  How to build the application  
  Build the application with 'docker build . -t lab1_hello_app:v1'.

3)  How to run the application  
  Run the application with  on port 8000 with 'docker run -d -p 8000:8000 --name lab1_hello_app lab1_hello_app:v1'.  
    After you are finished running the application, stop the container with 'docker stop lab1_hello_app' followed by removing the container with 'docker rm lab1_hello_app'

4)  How to test the application
To test the application, run the ./tests/test_src.py script to assert the test cases pass by using 'poetry run pytest'. If there are any additional test cases that you would like to test, add them to the script before running.  
  To manually test, navigate to "http://localhost:8000/" and test each endpoint after running the application.  
    a) "/hello?name=nameparamter"  
    b) "docs"  
    c) "openapi.json"

# Questions
1) What status code should be raised when a query parameter does not match our expectations?  
  A 422, Unprocessable Entity, is returned when a query parameter does not match the expected input because the request was well-formed but was unable to be followed due to semantic errors.

2) What does Python Poetry handle for us?  
  Python Poetry manages our dependencies to ensure that the required versions of the used packages are used in the application build. 

3) What advantages do multi-stage docker builds give us?  
  Multi-stage docker builds allow us to minimize the run size of our container to only utilize the run stage requirements in our final deployable container. 