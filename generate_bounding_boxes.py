# # generate_bounding_boxes.py (Standalone – run once)
# import cv2
# import json

# IMAGE_PATH = 'media/report_cards/reportcard_2.jpg'  # Update to full path, e.g., /path/to/your/project/media/report_cards/reportcard_2.jpg
# SUBJECTS = [
#     'mathematics', 'araling_panlipunan', 'english', 'edukasyon_pagpapakatao',
#     'science', 'edukasyon_pangkabuhayan', 'filipino', 'mapeh'
# ]

# ref_point = []
# current_subject_idx = 0
# bounding_boxes = {}
# image = None
# image_copy = None

# def click_and_drag(event, x, y, flags, param):
#     global ref_point, current_subject_idx, bounding_boxes
#     if event == cv2.EVENT_LBUTTONDOWN:
#         ref_point = [(x, y)]
#     elif event == cv2.EVENT_LBUTTONUP:
#         ref_point.append((x, y))
#         cv2.rectangle(image_copy, ref_point[0], ref_point[1], (0, 255, 0), 2)
#         cv2.imshow('Select Final Grades', image_copy)
#         x1, y1 = ref_point[0]
#         x2, y2 = ref_point[1]
#         bbox = (x1, y1, x2 - x1, y2 - y1)
#         current_subject = SUBJECTS[current_subject_idx]
#         bounding_boxes[current_subject] = bbox
#         print(f"{current_subject.capitalize()}: {bbox}")
#         current_subject_idx += 1
#         if current_subject_idx < len(SUBJECTS):
#             next_subject = SUBJECTS[current_subject_idx]
#             print(f"\nNext: Select {next_subject} final grade (post-Quarter 4 column). Click-drag.")
#         else:
#             print("\nDone! Press 'q' to save.")
#             cv2.setMouseCallback('Select Final Grades', lambda *args: None)

# # Load image
# image = cv2.imread(IMAGE_PATH)
# if image is None:
#     print(f"Error: Load {IMAGE_PATH}")
#     exit()
# image_copy = image.copy()

# print("Instructions:")
# print("- Resize window if needed (drag corners).")
# print("- For each subject: Click top-left of final grade cell, drag to bottom-right (post-Quarter 4).")
# print("- Green box appears. Press any key to continue.")
# print(f"Start with {SUBJECTS[0]}.")

# cv2.namedWindow('Select Final Grades', cv2.WINDOW_NORMAL)
# cv2.setMouseCallback('Select Final Grades', click_and_drag)
# cv2.imshow('Select Final Grades', image_copy)

# while True:
#     key = cv2.waitKey(0) & 0xFF
#     if key == ord('q'):
#         break

# cv2.destroyAllWindows()

# # Output
# print("\nCopy this to FINAL_GRADE_BOUNDING_BOXES in model_utils.py:")
# print("FINAL_GRADE_BOUNDING_BOXES = " + json.dumps(bounding_boxes, indent=4))

# # Save JSON
# with open('final_grade_bounding_boxes.json', 'w') as f:
#     json.dump(bounding_boxes, f, indent=4)
# print("Saved to final_grade_bounding_boxes.json")


# generate_bounding_boxes.py
import cv2
import json

IMAGE_PATH = 'media/report_cards/reportcard_2.jpg'  # UPDATE THIS PATH
SUBJECTS = [
    'filipino', 'english', 'science', 'mathematics', 
    'araling_panlipunan', 'mapeh', 'edukasyon_pangkabuhayan', 
    'edukasyon_pagpapakatao'
]

ref_point = []
current_subject_idx = 0
bounding_boxes = {}
image = None
image_copy = None

def click_and_drag(event, x, y, flags, param):
    global ref_point, current_subject_idx, bounding_boxes, image_copy
    
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        
    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        
        # Draw rectangle
        cv2.rectangle(image_copy, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow('Select Final Grades', image_copy)
        
        # Calculate bbox
        x1, y1 = ref_point[0]
        x2, y2 = ref_point[1]
        bbox = [min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)]
        
        current_subject = SUBJECTS[current_subject_idx]
        bounding_boxes[current_subject] = bbox
        
        print(f"✓ {current_subject}: {bbox}")
        
        current_subject_idx += 1
        
        if current_subject_idx < len(SUBJECTS):
            next_subject = SUBJECTS[current_subject_idx]
            print(f"\nNext: Select {next_subject.upper()} Final Grade")
            print("(Click top-left corner, drag to bottom-right, release)")
        else:
            print("\n✓ All subjects selected! Press 'q' to save and quit.")
            cv2.setMouseCallback('Select Final Grades', lambda *args: None)

# Load image
image = cv2.imread(IMAGE_PATH)
if image is None:
    print(f"❌ Error: Could not load {IMAGE_PATH}")
    print("Make sure the path is correct!")
    exit()

image_copy = image.copy()

print("=" * 60)
print("BOUNDING BOX SELECTION TOOL")
print("=" * 60)
print("\nInstructions:")
print("1. Look at the 'Final Grade' column (rightmost grades)")
print("2. For each subject, click TOP-LEFT of the grade cell")
print("3. Drag to BOTTOM-RIGHT of the grade cell")
print("4. Make sure you capture the ENTIRE number (both digits!)")
print("5. Press ANY KEY to continue to next subject")
print("6. Press 'q' when done to save\n")
print(f"Starting with: {SUBJECTS[0].upper()}")
print("=" * 60)

cv2.namedWindow('Select Final Grades', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Select Final Grades', 800, 1000)
cv2.setMouseCallback('Select Final Grades', click_and_drag)
cv2.imshow('Select Final Grades', image_copy)

# Wait for key press after each selection
while current_subject_idx < len(SUBJECTS):
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        break
    # Reset for next selection
    image_copy = image.copy()
    # Redraw all previous boxes
    for i, (subj, bbox) in enumerate(list(bounding_boxes.items())):
        x, y, w, h = bbox
        cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image_copy, subj[:4], (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imshow('Select Final Grades', image_copy)

cv2.destroyAllWindows()

# Save to JSON
output_path = 'final_grade_bounding_boxes.json'
with open(output_path, 'w') as f:
    json.dump(bounding_boxes, f, indent=4)

print("\n" + "=" * 60)
print("SAVED!")
print("=" * 60)
print(f"\nBounding boxes saved to: {output_path}")
print("\nCopy this to model_utils.py:")
print("\nFINAL_GRADE_BOUNDING_BOXES = {")
for subject, bbox in bounding_boxes.items():
    print(f"    '{subject}': {tuple(bbox)},")
print("}")
print("\n" + "=" * 60)