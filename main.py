import cv2

sides = ["white", "yellow", "green", "blue", "red", "orange"]

def main():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Webcam")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("webcam", frame)

        k = cv2.waitKey(1)
        
        if k%256 == 27:
            print("Escape hit")
            break
        elif k%256 == 32:
            img_name = "Opencv_frame_{}_.png".format(sides[img_counter])
            cv2.imwrite(img_name, frame)
            img_counter += 1
            if img_counter == 6:
                print("all sides recorded")
                break 


    



if __name__ == "__main__":
    main()