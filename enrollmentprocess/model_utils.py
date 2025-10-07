# import os
# import pickle
# import pandas as pd
# import pytesseract  # New: For OCR
# from PIL import Image  # New: For image processing
# import re  # New: For regex parsing in OCR

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# model_path = os.path.join(BASE_DIR, 'trained-model', 'decision_tree_models.pkl')

# with open(model_path, 'rb') as f:
#     models = pickle.load(f)

# feature_columns = ['dost_exam_result', 'filipino grade', 'English grade', 'mathematics grade',
#                    'science grade', 'araling panlipunan grade', 'Edukasyon sa pagpapakatao grade',
#                    'Edukasyong panglipunan at pangkabuhayan grade', 'MAPEH grade', 'Average grade']

# # Mapping for DOST exam result string to numeric
# DOST_RESULT_MAPPING = {
#     'passed': 1,
#     'failed': 0,
#     'not taken': 0,
#     # add other mappings if needed
# }

# # Subject mapping for OCR grade extraction
# SUBJECT_MAPPING = {
#     'mathematics': 'Mathematics',
#     'araling_panlipunan': 'Araling Panlipunan',
#     'english': 'English',
#     'edukasyon_pagpapakatao': 'Edukasyon sa Pagpapakatao',
#     'science': 'Science',
#     'edukasyon_pangkabuhayan': 'Edukasyon Pampahalagang Pangkabuhayang',
#     'filipino': 'Filipino',
#     'mapeh': 'MAPEH',
# }

# def predict_program_eligibility(input_data):
#     # Convert dost_exam_result string to numeric if needed
#     dost_result = input_data.get('dost_exam_result')
#     if isinstance(dost_result, str):
#         input_data['dost_exam_result'] = DOST_RESULT_MAPPING.get(dost_result.lower(), 0)

#     if isinstance(input_data, dict):
#         input_list = [input_data[col] for col in feature_columns]
#     else:
#         input_list = input_data

#     df = pd.DataFrame([input_list], columns=feature_columns)

#     # recommendations = {}
#     # for label, model in models.items():
#     #     prediction = model.predict(df)[0]
#     #     recommendations[label] = "Eligible" if prediction == 1 else "Not Eligible"
#     recommendations = {}
#     for label, model in models.items():
#         # If label is exactly "Top 5", rename it to "Top5"
#         if label == "top 5":
#             label = "top5"

#         prediction = model.predict(df)[0]
#         recommendations[label] = "Eligible" if prediction == 1 else "Not Eligible"

#     return recommendations


# # New: OCR function to extract grades from report card image
# def extract_grades_from_image(image_path):
#     """
#     Extract grades from report card image using OCR.
#     Returns dict of subject: grade (float) or empty dict if extraction fails.
#     """
#     try:
#         # Open and preprocess image
#         img = Image.open(image_path)
#         if img.mode != 'RGB':
#             img = img.convert('RGB')
            
#         # Extract text with Tesseract
#         custom_config = r'--oem 3 --psm 6'  # Better for structured text
#         text = pytesseract.image_to_string(img, config=custom_config)
#         # Parse grades using regex for each subject
#         extracted_grades = {}
#         for field_name, subject_name in SUBJECT_MAPPING.items():
#             # Flexible patterns to match common report card formats
#             patterns = [
#                 rf"{re.escape(subject_name)}[:\s\-–]*\s*(\d{{1,3}}(?:\.\d{{1,2}})?)",  # e.g., "Mathematics: 85.5"
#                 rf"{re.escape(subject_name.lower())}[:\s\-–]*\s*(\d{{1,3}}(?:\.\d{{1,2}})?)",  # Lowercase fallback
#             ]
#             for pattern in patterns:
#                 match = re.search(pattern, text, re.IGNORECASE)
#                 if match:
#                     try:
#                         grade = float(match.group(1))  # Handle decimals
#                         extracted_grades[field_name] = round(grade, 2)
#                         break
#                     except ValueError:
#                         continue
                    
#             return extracted_grades
#     except Exception as e:
#         # Log error (use Django's logger in production)
#         print(f"OCR extraction failed: {e}")
#         return {}
   
import os
import pickle
import pandas as pd
import cv2
import pytesseract
from PIL import Image, ImageEnhance
import numpy as np
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'trained-model', 'decision_tree_models.pkl')

with open(model_path, 'rb') as f:
    models = pickle.load(f)

feature_columns = ['dost_exam_result', 'filipino grade', 'English grade', 'mathematics grade',
                   'science grade', 'araling panlipunan grade', 'Edukasyon sa pagpapakatao grade',
                   'Edukasyong panglipunan at pangkabuhayan grade', 'MAPEH grade', 'Average grade']

# Mapping for DOST exam result string to numeric
DOST_RESULT_MAPPING = {
    'passed': 1,
    'failed': 0,
    'not taken': 0,
    # add other mappings if needed
}

# New: Subject mapping for OCR (form field -> report card name)
SUBJECT_MAPPING = {
    'filipino': ['Filipino'],
    'english': ['English', 'Engl1sh'],  # add OCR mistakes here
    'science': ['Science'],
    'mathematics': ['Mathematics', 'Math'],
    'araling_panlipunan': ['Araling Panlipunan', 'AP'],
    'mapeh': ['MAPEH'],
    'music': ['Music'],
    'art': ['Art'],
    'physical_education': ['Physical Education', 'PE'],
    'health': ['Health'],
    'edukasyon_pangkabuhayan': ['Technology and Livelihood Education', 'TLE'],
    'edukasyon_pagpapakatao': ['Good Manners and Right Conduct', 'GMRC', 'Edukasyon sa Pagpapakatao'],
}

FINAL_GRADE_BOUNDING_BOXES = {
    'mathematics': (703, 402, 124, 79),
    'araling_panlipunan': (703, 487, 129, 93),
    'english': (702, 246, 129, 77),
    'edukasyon_pagpapakatao': (703, 1140, 129, 151),
    'science': (702, 323, 130, 79),
    'edukasyon_pangkabuhayan': (699, 995, 129, 137),
    'filipino': (703, 167, 132, 76),
    'mapeh': (702, 585, 129, 85),
    # Add/adjust if more subjects or different layout
}

def predict_program_eligibility(input_data):
    # Convert dost_exam_result string to numeric if needed
    dost_result = input_data.get('dost_exam_result')
    if isinstance(dost_result, str):
        input_data['dost_exam_result'] = DOST_RESULT_MAPPING.get(dost_result.lower(), 0)

    if isinstance(input_data, dict):
        input_list = [input_data[col] for col in feature_columns]
    else:
        input_list = input_data

    df = pd.DataFrame([input_list], columns=feature_columns)

    # recommendations = {}
    # for label, model in models.items():
    #     prediction = model.predict(df)[0]
    #     recommendations[label] = "Eligible" if prediction == 1 else "Not Eligible"
    recommendations = {}
    for label, model in models.items():
        # If label is exactly "Top 5", rename it to "Top5"
        if label == "top 5":
            label = "top5"

        prediction = model.predict(df)[0]
        recommendations[label] = "Eligible" if prediction == 1 else "Not Eligible"

    return recommendations

def extract_grades_from_image(image_source):
    """
    Enhanced OCR with range filter and improved fallback parsing.
    """
    # Input handling (unchanged)
    if isinstance(image_source, str) and os.path.exists(image_source):
        img_path = image_source
        img = cv2.imread(img_path)
    else:
        if hasattr(image_source, 'read'):
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                for chunk in image_source.chunks():
                    temp_file.write(chunk)
                temp_path = temp_file.name
            img = cv2.imread(temp_path)
            os.unlink(temp_path)
        else:
            return {}

    if img is None:
        print("OCR Error: Could not load image.")
        return {}

    # Print image dimensions
    h_img_orig, w_img_orig = img.shape[:2]
    print(f"DEBUG: Image dimensions: height={h_img_orig}, width={w_img_orig}")

    # Preprocessing (same softer)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # DEBUG: Save full threshold (comment if not needed)
    cv2.imwrite('debug_full_thresh.png', thresh)
    print("DEBUG: Saved full threshold to debug_full_thresh.png")

    extracted = {}
    h_img, w_img = thresh.shape

    # Subject order for fallback (matches typical report card rows)
    SUBJECT_ORDER = ['filipino', 'english', 'science', 'mathematics', 'araling_panlipunan', 'mapeh', 'edukasyon_pangkabuhayan', 'edukasyon_pagpapakatao']

    # Primary: Bounding Box Extraction
    for field_key, bbox in FINAL_GRADE_BOUNDING_BOXES.items():
        x, y, bbox_w, bbox_h = bbox
        x = max(0, min(x, w_img - 1))
        y = max(0, min(y, h_img - 1))
        bbox_w = min(bbox_w, w_img - x)
        bbox_h = min(bbox_h, h_img - y)
        cropped = thresh[y:y+bbox_h, x:x+bbox_w]

        if cropped.size == 0:
            continue

        # DEBUG: Save crop (comment if not needed)
        debug_dir = 'ocr_debug_crops'
        os.makedirs(debug_dir, exist_ok=True)
        crop_filename = os.path.join(debug_dir, f"{field_key}_crop.png")
        cv2.imwrite(crop_filename, cropped)
        print(f"DEBUG: Saved crop to {crop_filename}")

        # OCR (PSM 7 for single line – better for partials)
        config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789. --dpi 300'
        text = pytesseract.image_to_string(cropped, config=config).strip()

        print(f"OCR Raw Crop ({field_key}): '{text}' (from box {bbox})")

        # Parse with range filter
        try:
            if text:
                cleaned = ''.join(c for c in text if c in '0123456789.')
                if cleaned and len(cleaned) >= 2:  # At least 2 chars for full grade
                    grade = float(cleaned)
                    if 50 <= grade <= 100:  # Filter noise/partials
                        extracted[field_key] = grade
                        print(f"OCR Success ({field_key}): {text} -> {grade}")
                    else:
                        print(f"OCR Invalid Range ({field_key}): {text} (filtered)")
                else:
                    print(f"OCR Too Short/Invalid ({field_key}): '{text}'")
            else:
                print(f"OCR Empty Crop ({field_key})")
        except ValueError:
            print(f"OCR Parse Error ({field_key}): '{text}'")

    # ENHANCED Fallback: Full image + row-based number assignment
    missing_subjects = [key for key in FINAL_GRADE_BOUNDING_BOXES if key not in extracted]
    if missing_subjects:
        print(f"OCR Fallback: Processing missing: {missing_subjects}")
        config_fallback = r'--oem 3 --psm 6 -l eng'
        full_text = pytesseract.image_to_string(thresh, config=config_fallback)
        print("=== OCR FALLBACK FULL TEXT ===")
        print(full_text)
        print("=== END FALLBACK FULL TEXT ===")

        # Extract all potential grades (2-3 digits, 50-100)
        all_grades = re.findall(r'\b(\d{2,3}(?:\.\d{1,2})?)\b', full_text)
        valid_grades = [float(g) for g in all_grades if 50 <= float(g) <= 100]

        # Simple row matching: Assume order in text lines; assign sequential valid grades
        lines = [ln.strip() for ln in full_text.splitlines() if ln.strip()]
        grade_index = 0
        for i, field_key in enumerate(SUBJECT_ORDER):
            if field_key in missing_subjects and grade_index < len(valid_grades):
                # Look for keyword in nearby lines
                start_line = max(0, i - 2)
                end_line = min(len(lines), i + 3)
                nearby_text = ' '.join(lines[start_line:end_line])
                if any(syn.lower() in nearby_text.lower() for syn in SUBJECT_MAPPING.get(field_key, [field_key])):
                    extracted[field_key] = valid_grades[grade_index]
                    print(f"OCR Fallback Success ({field_key}): {valid_grades[grade_index]} (row {i+1})")
                    grade_index += 1

    print(f"OCR Final Extracted: {extracted}")
    return extracted
