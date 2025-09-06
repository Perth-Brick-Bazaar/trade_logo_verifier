# Diagnostic Overlay Rig – Software Scaffold

## 🧭 Overview
Modular Python-based system for detecting, counting, and verifying parts on a tray using a Raspberry Pi, camera, and projector. Feedback is projected directly onto the tray, with operator interaction via visual cues and optional input mechanisms.

---

## 📁 Project Structure

# 📁 diagnostic_rig Directory Structure

## Root Files
- `main.py` — Orchestrates the full diagnostic loop
- `capture.py` — Handles camera input and image acquisition
- `detect.py` — Blob detection and confidence scoring
- `overlay.py` — Projects visual feedback via HDMI
- `interface.py` — Operator input handling (keypad, camera, browser)

## Folders
	### `config/`
	- `tray_profiles.json` — Expected counts, logo zones, metadata
	- `logo_templates/` — Reference logos for matching

	### `logs/`
	- `session_log.csv` — Timestamped scan results and feedback events

	### `assets/`
	- `overlay_icons/` — Icons (✓, ⚠, ✖) and feedback graphics

	### Other
	- `README.md` — Project overview, setup instructions, and usage

---

## 🧪 Module Responsibilities

### `main.py`
- Orchestrates the full diagnostic loop
- Loads tray config and initializes modules
- Handles state transitions (scan → feedback → confirm → next)

### `capture.py`
- Interfaces with PiCam or USB camera
- Captures top-down image of tray
- Preprocessing: grayscale, threshold, denoise

### `detect.py`
- Runs blob detection via OpenCV
- Flags oversized or irregular blobs
- Compares found count to expected
- Optional logo check (template match or classifier)

### `overlay.py`
- Projects visual feedback onto tray
- Reserved right-side panel for status and instructions
- Tray-wide green overlay on full confirmation
- Fade-in transitions (no flashing)

### `interface.py`
- Handles operator input:
  - Projected keypad (camera-monitored)
  - Physical keypad (GPIO)
  - Browser interface (future phase)
- Confirms arm clearance before proceeding

---

## 🎛️ Feedback Protocol

- **Visual**:
  - Green: confirmed blobs
  - Yellow: borderline
  - Red: flagged zones
  - Tray-wide green wash on full confirmation
- **Auditory**:
  - Single beep on match
  - Optional mute toggle
- **Interaction**:
  - “Next”, “Retry”, “Flag” via keypad or projected interface

---

## 🧠 Expansion Pathways

- Browser-based BB control via Flask or Node.js
- Logo classification via ML model (TensorFlow Lite or OpenCV)
- Escalation logic and provenance tracking
- Multi-tray session handling and operator profiles

---

## 🧩 Design Principles

- Modular and testable codebase
- Operator-first feedback loop
- Emotionally safe visual signaling
- Scalable from Pi testbed to BB deployment
