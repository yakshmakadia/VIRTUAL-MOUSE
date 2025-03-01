# VIRTUAL-MOUSE

## Project Objective
This project aims to create a computer vision-based mouse controller using Python libraries like OpenCV and pynput. The system captures video input from a webcam, detects hand gestures, and translates them into mouse actions such as left-clicking and cursor movement.

## Scope of Project
- Utilize OpenCV for image processing (color segmentation, contour detection, etc.)
- Use pynput to simulate mouse actions
- Implement a GUI using wxPython
- Optimize performance for real-time responsiveness
- Ensure robustness across different lighting conditions

## Implementation Details
1. **Gesture Detection**: Uses OpenCV and MediaPipe to track hand landmarks
2. **Cursor Movement**: Hand gestures control cursor positioning
3. **Clicking and Dragging**: Detects different clicks and drag actions
4. **Scrolling and Zooming**: Implements scrolling gestures based on finger movement
5. **GUI Interface**: Provides user-friendly settings adjustment

## System Design
- **Input Module**: Captures video input from the webcam
- **Image Processing**: Uses OpenCV for hand gesture detection
- **Gesture Recognition**: Analyzes gestures for actions
- **Mouse Control**: Maps gestures to mouse actions using pynput
- **GUI Interface**: Allows users to tweak settings

  
## Authors
- Diva Merja
- Makadia Yakshkumar Vijaykumar
- Krishna Wadhwani
