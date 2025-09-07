# 🧱 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# File: main.py
# Purpose: Orchestrates the Diagnostic Overlay Rig workflow
# Scope: Loads config, manages camera, detects parts, provides operator feedback
# Features:
# - Live camera feed and scan trigger
# - Blob detection and edge exclusion
# - Operator messaging and overlap alerts
# - Ready for integration with focus check and API modules
# Linked Files: Focus.py, capture.py, detect.py, overlay.py, interface.py
# File Types: Python, live video stream (cv2.VideoCapture)
# Created by: Craig Wilson / GitHub Copilot
# Last Updated: 2025-09-06
# 🧱 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
Main orchestration for Diagnostic Overlay Rig
"""

# Camera and image manipulation imports
import cv2
import numpy as np
import json
import time

# Module imports (to be implemented)
# from capture import capture_image
# from detect import detect_blobs, check_logos
# from overlay import project_feedback
# from interface import get_operator_input

# Load tray configuration
def load_tray_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def detect_blobs(image, config):
    """Detect blobs fully within the image, using config for parameters. Flags non-average sized blobs and draws red circles around them."""
    margin = config.get('blob_margin', 10)
    min_area = config.get('blob_min_area')
    max_area = config.get('blob_max_area', 100000)  # Allow large parts by default
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    _, thresh = cv2.threshold(blurred, 200, 250, cv2.THRESH_BINARY_INV)
    cv2.imshow('Thresholded Image', thresh)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Contours found: {len(contours)}")

    params = cv2.SimpleBlobDetector_Params()
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False
    params.filterByColor = True
    params.blobColor = 255
    params.minArea = min_area
    params.maxArea = max_area
    params.minThreshold = 10
    params.maxThreshold = 255
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(thresh)
    print(f"Number of keypoints detected: {len(keypoints)}")
    h, w = image.shape[:2]
    blobs = []
    radii = [kp.size / 2 for kp in keypoints]
    mean_radius = np.mean(radii) if radii else 0
    std_radius = np.std(radii) if radii else 0
    # Draw circles: red for non-average, green for normal
    im_with_keypoints = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    for i, kp in enumerate(keypoints):
        x, y = int(kp.pt[0]), int(kp.pt[1])
        r = int(kp.size / 2)
        print(f"Blob center: ({x:.1f}, {y:.1f}), radius: {r:.1f}")
        if (x - r > margin and x + r < w - margin and
            y - r > margin and y + r < h - margin):
            blobs.append({'pt': kp.pt, 'size': kp.size})
            if std_radius > 0 and abs(r - mean_radius) > 2 * std_radius:
                print(f"Non-average blob detected at ({x:.1f}, {y:.1f}), radius: {r:.1f} (possible out-of-position or touching part)")
                color = (0, 0, 255)  # Red
            else:
                color = (0, 255, 0)  # Green
            cv2.circle(im_with_keypoints, (x, y), r, color, 2)
        else:
            print("Excluded by edge filter")
    cv2.imshow('Blobs', im_with_keypoints)
    return blobs

def operator_message(msg):
    """Simple operator message display (prints to terminal for now)."""
    print(f"[OPERATOR MESSAGE]: {msg}")

# Main diagnostic loop
def main():
    config = load_tray_config('C:\\Users\\livin\\OneDrive\\Documents\\Python Code\\BrickMark\\trade_logo_verifier\\config\\tray_profiles.json')
    expected_count = config.get('expected_count', 0)
    cap = cv2.VideoCapture(0)
    print("Press SPACE to scan tray, ESC to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            operator_message("Camera error.")
            break
        cv2.imshow('Tray View', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            blobs = detect_blobs(frame, config)
            found_count = len(blobs)
            diff = expected_count - found_count
            operator_message(f"Found: {found_count}, Expected: {expected_count}, Difference: {diff}")
            # Highlight large blobs (possible overlaps)
            avg_size = np.mean([b['size'] for b in blobs]) if blobs else 0
            for b in blobs:
                if b['size'] > avg_size * 1.5:
                    operator_message(f"Large blob at {b['pt']} (size: {b['size']}) - possible overlap. Please separate parts.")
            # Feedback logic can be added here
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

"""
Trade Logo Verifier - Starter Script
"""

def verify_logo(logo_path: str) -> bool:
    # Placeholder: Add actual verification logic here
    print(f"Verifying logo: {logo_path}")
    return True  # Assume always valid for now

if __name__ == "__main__":
    logo_file = "sample_logo.png"  # Replace with your logo file
    result = verify_logo(logo_file)
    print(f"Logo verification result: {result}")
