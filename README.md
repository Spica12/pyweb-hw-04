I used the following commands:

- create the image: 
1) docker build . -t spica12/pyweb_hw_04

- run the container:
2) docker run --name pyweb_hw_04 -p 80:3000 -v ~/GoIT/PythonWEB-homework/pyweb-hw-04/myStorage:/app/storage spica12/pyweb_hw_04 

- open the terminal container:
3) docker exec -it <id_container> sh
