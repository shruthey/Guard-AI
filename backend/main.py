import os
import cv2
from ultralytics import YOLO
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])

def main():
    video = request.files['video']
    video.save(os.path.join('.','data','input.mp4'))
    classes = ["person","bicycle","car","motorbike","aeroplane","bus","train","truck","boat","traffic light","fire hydrant","stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball","kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket","bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple","sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","sofa","pottedplant","bed","diningtable","toilet","tvmonitor","laptop","mouse","remote","keyboard","cell phone","microwave","oven","toaster","sink","refrigerator","book","clock","vase","scissors","teddy bear","hair drier","toothbrush"]
    video_path =os.path.join('.','data','input.mp4')
    video_out_path = os.path.join('.', 'out.mp4')

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS),(frame.shape[1], frame.shape[0]))
    model = YOLO("yolov8n.pt")
    min_confidence = 0.6
    step = cap.get(cv2.CAP_PROP_FPS)
    objects = set()
    while ret:
        results = model(frame)

        for result in results:

            for r in result.boxes.data.tolist():

                x1, y1, x2, y2, score, class_id = r
                x1 = int(x1)
                w = int(x2)-int(x1)
                y1 = int(y1)
                h = int(y2)-int(y1)
                class_id = int(class_id)
                if score > min_confidence:
                    text = f'{classes[class_id]}: {score:.2f}'
                    frame = cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), (0, 255, 0), 2)
                    frame = cv2.putText(frame, text , (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                    objects.add(classes[class_id])
            cv2.imshow('frame', frame)
        cap_out.write(frame)
        
        ret, frame = cap.read()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cap_out.release()
    cv2.destroyAllWindows()

    print(list(objects))
    return list(objects)

    