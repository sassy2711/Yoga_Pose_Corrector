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

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sassy2711/Yoga_Pose_Corrector.git
   cd Yoga_Pose_Corrector
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

   (For a Flutter app, follow the build instructions in the `flutter_app/` directory.)

## Usage

1. Open the application.
2. Follow the on-screen instructions to select a yoga pose.
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
