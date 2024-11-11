import numpy as np
import cv2
from ultralytics import YOLO
import supervision as sv
import pandas as pd

# Load YOLOv8 model
model = YOLO("yolov8n.pt")
box_annotator = sv.BoxAnnotator()

# Define zones
zone_1 = np.array([[10, 14], [1896, 24], [1905, 1058], [20, 1049]])
zones = [zone_1]
zone_annotator = sv.PolygonAnnotator()
tracker = sv.ByteTrack()

people_enter_queue = {}
frame_count = 0
cap = cv2.VideoCapture("video2.mp4")

# Create a DataFrame to store the last frame count only
df = pd.DataFrame(columns=['Frame', 'Num_People_in_Zone1'])
num_people_counts = []  # List to store people count for each frame

def process_frame(frame: np.ndarray, i) -> np.ndarray:
    global frame_count, num_people_in_zone1

    results = model(frame)
    detections = sv.Detections.from_ultralytics(results[0])
    detections = detections[(detections.class_id == 0) & (detections.confidence > 0.5)]

    # Update tracker with detections
    detections = tracker.update_with_detections(detections)

    # Get the boxes and track IDs
    boxes = detections.xyxy
    track_ids = detections.tracker_id if isinstance(detections.tracker_id, np.ndarray) else np.array(detections.tracker_id)

    num_people_in_zone1 = 0

    for box, track_id in zip(boxes, track_ids):
        x1, y1, x2, y2 = map(int, box)
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        in_zone_1 = cv2.pointPolygonTest(zone_1, (x, y), False) > 0

        if in_zone_1:
            num_people_in_zone1 += 1

        if str(track_id) not in people_enter_queue:
            people_enter_queue[str(track_id)] = {
                'entry_frame': frame_count,
            }

        entry_frame = people_enter_queue[str(track_id)]['entry_frame']
        time_spent = (frame_count - entry_frame) / cap.get(cv2.CAP_PROP_FPS)
        cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Time: {time_spent:.2f}s", (x1, y1 - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)

    # Append the count of people in the zone to the list
    num_people_counts.append(num_people_in_zone1)

    # Annotate zones
    frame = box_annotator.annotate(frame.copy(), detections=detections)
    cv2.putText(frame, f'People in counter: {num_people_in_zone1}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    frame_count += 1
    return frame

# Process the video and save the results
sv.process_video(
    source_path="video2.mp4",
    target_path="result.mp4",
    callback=process_frame
)

# After processing all frames, save only the last frame's count to an Excel file
df.loc[0] = [frame_count - 1, num_people_in_zone1]  # Store last frame count
df.to_excel("waittime.xlsx", index=False)

# Print all values of num_people_in_zone1 after processing the video
print("People count per frame in Zone 1:")
print(num_people_counts)