import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx

# Initialize mouse controller
mouse = Controller()

# Initialize wx App to get screen size
app = wx.App(False)
sx, sy = wx.GetDisplaySize()
(camx, camy) = (480, 320)

# Define HSV range for detecting red color
lower_bound = np.array([130, 90, 109])
upper_bound = np.array([203, 225, 180])

# Capture video
cam = cv2.VideoCapture(0)
cam.set(3, camx)
cam.set(4, camy)

# Define kernels for morphological operations
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

# Variables for smooth movement
mLocOld = np.array([0, 0])
mouseLoc = np.array([0, 0])
Df = 2.3  # Damping Factor
pinchFlag = 0

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create mask for color detection
    mask = cv2.inRange(imgHSV, lower_bound, upper_bound)
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
    maskFinal = maskClose

    # Find contours
    conts, _ = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(conts) == 2:
        if pinchFlag == 1:
            pinchFlag = 0
            mouse.release(Button.left)

        x1, y1, w1, h1 = cv2.boundingRect(conts[0])
        x2, y2, w2, h2 = cv2.boundingRect(conts[1])

        cx1, cy1 = x1 + w1 // 2, y1 + h1 // 2
        cx2, cy2 = x2 + w2 // 2, y2 + h2 // 2

        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
        cv2.line(img, (cx1, cy1), (cx2, cy2), (255, 0, 0), 2)

        cx, cy = (cx1 + cx2) // 2, (cy1 + cy2) // 2
        cv2.circle(img, (cx, cy), 2, (0, 255, 0), 2)

        mouseLoc = mLocOld + ((cx, cy) - mLocOld) / Df
        mouse.position = (sx - (mouseLoc[0] * sx / camx), mouseLoc[1] * sy / camy)
        mLocOld = mouseLoc

    elif len(conts) == 1:
        if pinchFlag == 0:
            pinchFlag = 1
            mouse.press(Button.left)

        x, y, w, h = cv2.boundingRect(conts[0])
        cx, cy = x + w // 2, y + h // 2

        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.circle(img, (cx, cy), (w + h) // 6, (0, 0, 255), 2)

        mouseLoc = mLocOld + ((cx, cy) - mLocOld) / Df
        mouse.position = (sx - (mouseLoc[0] * sx / camx), mouseLoc[1] * sy / camy)
        mLocOld = mouseLoc

    cv2.imshow('Virtual Mouse', img)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    pass
