import cv2
camera=cv2.VideoCapture(0)


def generate_frames():
    while True:
        success,frame=camera.read() #reads camera frame
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)#incode image into memory buffer
            frame=buffer.tobytes()#convert buffer to frames
        yield(b' -- frame\r\n'
                    b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')#we use yield instade of return becuse return will end the loop