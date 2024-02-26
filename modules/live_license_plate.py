import datetime
from ultralytics import YOLO
import cv2
import easyocr

# define some constants
CONFIDENCE_THRESHOLD = 0.75
GREEN = (0, 255, 0)

# initialize the video capture object
video_cap = cv2.VideoCapture(0)

# load the pre-trained YOLOv8n model
model = YOLO("license_plate_detector.pt")

# initialize the OCR reader
reader = easyocr.Reader(['en'])

while True:
    ret, frame = video_cap.read()

    # if there are no more frames to process, break out of the loop
    if not ret:
        break

    # run the YOLO model on the frame
    detections = model(frame, verbose=False)[0]

    # loop over the detections
    for data in detections.boxes.data.tolist():
        confidence = data[4]

        # filter out weak detections
        if float(confidence) < CONFIDENCE_THRESHOLD:
            continue

        # draw bounding box on the frame
        xmin, ymin, xmax, ymax = map(int, data[:4])
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)

        # extract license plate region
        plate_roi = frame[ymin:ymax, xmin:xmax]

        # perform OCR on the license plate region
        results = reader.readtext(plate_roi)

        # print the detected license plate numbers
        for (bbox, text, prob) in results:
            if prob >= CONFIDENCE_THRESHOLD:
                print(f"Detected License Plate: {text} (Confidence: {prob:.2f})")

    # show the frame to our screen
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

video_cap.release()
cv2.destroyAllWindows()