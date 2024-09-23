# Yoga Pose Corrector

## Overview

**Yoga Pose Corrector** is a computer vision-based application that detects yoga poses in real-time and provides instant feedback on the correctness of the posture. Using OpenCV and machine learning, the app identifies key pose landmarks and compares them against ideal reference poses, helping users correct their yoga postures efficiently. The project also includes audio feedback for hands-free usage, making it user-friendly for home workouts.

## Features

- Real-time yoga pose detection using computer vision.
- Comparison of user pose with ideal pose landmarks for accuracy.
- Instant feedback on posture correction.
- Audio guidance for hands-free usage.
- Supports multiple yoga poses.
- Cross-platform compatibility (mobile/desktop).

## Technologies Used

- **OpenCV**: For computer vision tasks like capturing images and processing pose landmarks.
- **MediaPipe**: To detect pose landmarks from images.
- **Python**: Backend logic for pose comparison and feedback.
- **Flutter**: To build a user-friendly cross-platform interface (mobile/desktop).

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- pip

### Installation
   **Backend**
   1. **Clone the repository**:
      ```bash
      git clone https://github.com/sassy2711/Yoga_Pose_Corrector.git
      ```

   2. **Install Python dependencies**:
      ```bash
      pip install -r requirements.txt
      ```
   
   3. **Navigate into project directory**:
      ```bash
      cd Yoga_Pose_Corrector
      ```

   4. **Running the backend**:
      ```bash
      cd backend
      python main.py
      ```
   
   **Frontend**
   

## Usage 
This version works only when you are standing to your right. That means that, when you are standing in front of the camera, you should turn towards your right and then it will work. This was done because it is hard to detect the landmark points for most poses when we are facing the camera from the front. The functionality could easily be implemented when you turn towards your left also, but was not implemented due to time constraints. It will be implemented in an update very soon.

   **Backend**
   1. You will be given a menu with different asana names.
   2. Type any name from the menu.
   3. Go in front of the camera.
   4. Turn to your right.
   5. Make sure the points are being mapped properly and you are in the frame.
   6. Do your yoga pose and enjoy audio feedback from the application.
   7. Just press Ctrl-C on the terminal to end the application.

   **Frontend**
   1. Open the application.
   2. Select a yoga pose.
   3. The application will start real-time pose detection and guide you through the correct posture.
   4. You'll receive audio feedback to adjust your pose.

## Yoga Poses Supported

- Prayer pose – Pranamasana
- Raised arms pose – Hastauttanasana
- Hand to foot pose – Hasta Padasana
- Equestrian pose – Ashwa Sanchalanasana
- Stick pose – Dandasana
- Salute with eight points – Ashtanga Namaskara
- Cobra pose – Bhujangasana
- Downward facing dog pose - Adho Mukha Svanasana

## Contribution

Feel free to open issues or pull requests to contribute to the project. Suggestions for new features, bug fixes, or improvements are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
