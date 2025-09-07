# 🧱 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Tool: Focus.py  
# Purpose: Evaluates live camera focus using Laplacian-based sharpness detection  
# Scope: Captures frames, calculates focus score, and displays visual feedback loop  
# Features:  
# - Uses Laplacian variance to measure image sharpness (`is_camera_in_focus`)  
# - Continuously acquires frames until focus threshold is met (`wait_for_focus`)  
# - Annotates live feed with visual status overlay and focus measure  
# Linked Files: Used by main.py, capture.py  
# File Types: live video stream (cv2.VideoCapture), *.jpg (if frame capture applied downstream)  
# Created by: Craig Wilson / GitHub Copilot  
# Last Updated: 2025-09-06  
# 🧱 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import cv2
import numpy as np

def is_camera_in_focus(image, threshold=9.0):
    """
    Detect if the camera is in focus by calculating the variance of the Laplacian.
    Args:
        image: Input image (numpy array).
        threshold: Focus threshold. Higher values indicate sharper images.
    Returns:
        bool: True if the image is in focus, False otherwise.
        float: The focus measure (variance of Laplacian).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var > threshold, laplacian_var

def wait_for_focus(camera_index=0, threshold=9.0):
    """
    Continuously acquires frames until the camera is in focus.
    Returns the focused frame.
    """
    camera = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame.")
            break
        in_focus, focus_measure = is_camera_in_focus(frame, threshold)
        status = "In Focus" if in_focus else "Out of Focus"
        print(f"Focus Measure: {focus_measure:.2f} - Status: {status}")
        cv2.putText(frame, f"{status} ({focus_measure:.2f})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if in_focus else (0, 0, 255), 2)
        cv2.imshow("Camera Focus", frame)
        if in_focus:
            camera.release()
            cv2.destroyWindow("Camera Focus")
            return frame
        if cv2.waitKey(50) & 0xFF == 27:
            camera.release()
            cv2.destroyWindow("Camera Focus")
            break
    return None
