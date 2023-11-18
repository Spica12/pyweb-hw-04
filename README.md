docker build . -t spica12/pyweb_hw_04
docker run --name pyweb_hw_04 -p 80:3000 -v ~/GoIT/PythonWEB-homework/pyweb-hw-04/myStorage:/app/storage spica12/pyweb_hw_04 
