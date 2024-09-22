import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:camera/camera.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/io.dart';
import 'package:image/image.dart' as img;

enum DetectionStatus { noPose, fail, success, partial }

void main() => runApp(const MaterialApp(
  home: HomePage(),
));

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {

    String formattedDate = DateFormat('d MMMM').format(DateTime.now()).toUpperCase();
  String dayOfWeek = DateFormat('EEEE').format(DateTime.now());

    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 70,
        leading: Padding(
          padding: EdgeInsets.only(left: 20),
          child: SvgPicture.asset('assets/FlexcellentWhite.svg', width: 200.0),
        ),
        leadingWidth: 200,
        backgroundColor: Colors.red[600],

        title: Align(
          alignment: Alignment.centerRight,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.end, // Align text to the right
            children: [
              Text(
                formattedDate,
                style: const TextStyle(
                  fontSize: 12, // Larger font size for the date
                  fontFamily: 'Nunito',
                  fontWeight: FontWeight.w800,
                  color: Colors.white70,
                ),
              ),
              Text(
                dayOfWeek,
                style: const TextStyle(
                  fontSize: 24, // Same font size for the day
                  fontFamily: 'Nunito',
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ],
          ),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const SizedBox(height: 20),
            const Text(
              "Asana, Suvasana!",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 32,
                fontFamily: 'Nunito',
                fontWeight: FontWeight.bold,
                color: Colors.red,
              ),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    buttonPlaceholder(context, 1, 'assets/Pranamasana.png'),
                    const SizedBox(height: 20),
                    buttonPlaceholder(context, 2, 'assets/Hastauttanasana.png'),
                    const SizedBox(height: 20),
                    buttonPlaceholder(context, 3, 'assets/Hastapadasana.png'),
                    const SizedBox(height: 20),
                    buttonPlaceholder(context, 4, 'assets/AshwaSanchalanasanaR.png'),
                    const SizedBox(height: 20),
                    buttonPlaceholder(context, 5, 'assets/AshwaSanchalanasanaL.png'),
                    const SizedBox(height: 20),
                    buttonPlaceholder(context, 6, 'assets/Dandasana.png'),
                    const SizedBox(height: 20),
                    buttonPlaceholder(context, 7, 'assets/AshtangaNamaskara.png'),
                    const SizedBox(height: 20),
                    buttonPlaceholder(context, 8, 'assets/Bhujangasana.png'),
                    const SizedBox(height: 20),
                    buttonPlaceholder(context, 9, 'assets/AdhoMukhaSvanasana.png'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
  // Function to create a placeholder button with image
  Widget buttonPlaceholder(BuildContext context, int asanaNumber, String imagePath) {
    return GestureDetector(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => CameraScreen(asanaNumber: asanaNumber),
          ),
        );
      },
      child: Center(
        child: Container(
          width: 370, // Width of the button image
          height: 150, // Height of the button image
          decoration: BoxDecoration(
            color: Colors.grey[300], // Placeholder color
            borderRadius: BorderRadius.circular(30),
            image: DecorationImage(
              image: AssetImage(imagePath), // Use the image passed into the function
              fit: BoxFit.cover, // Ensures the image covers the container
            ),// Curvature of corners
            boxShadow: [
              BoxShadow(
                color: Colors.black12,
                blurRadius: 5,
                offset: Offset(0, 5),
              ),
            ],
          ),
          child: const Center(
            child: Text(
              '',
              style: TextStyle(
                fontSize: 24,
                color: Colors.black54,
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class CameraScreen extends StatefulWidget {
  final int asanaNumber;

  const CameraScreen({super.key, required this.asanaNumber});

  @override
  _CameraScreenState createState() => _CameraScreenState();
}




class _CameraScreenState extends State<CameraScreen> {
  CameraController? controller;
  late WebSocketChannel channel;
  DetectionStatus? status;

  // Status message based on the detection result
  String get currentStatus {
    if (status == null) return "Initializing...";
    switch (status!) {
      case DetectionStatus.noPose:
        return "No Asana Detected in the screen";
      case DetectionStatus.fail:
        return "Incorrect Pose Detected";
      case DetectionStatus.success:
        return "You're Doing Great Baby!";
      case DetectionStatus.partial:
        return "Adjust Your Pose a Little";
    }
  }

  // Variable to track front (0) or back (1) camera
  int cameraIndex = 1;

  // Handle the camera and WebSocket setup
  @override
  void initState() {
    super.initState();
    initializeCamera();
    initializeWebSocket();
  }

  // Initialize the camera and periodically capture images
  Future<void> initializeCamera() async {
    final cameras = await availableCameras();
    final firstCamera = cameras[cameraIndex]; // Back camera at index 0

    controller = CameraController(
      firstCamera,
      ResolutionPreset.medium,
      enableAudio: false,
    );

    await controller!.initialize();
    setState(() {});

    Timer.periodic(const Duration(seconds: 3), (timer) async {
      try {
        final image = await controller!.takePicture();
        final compressedImageBytes = compressImage(image.path);

        // Create a JSON object to send both the image data and asana number
        final message = {
          'asanaNumber': widget.asanaNumber,
          'imageData': base64Encode(compressedImageBytes), // Convert image bytes to base64
        };

        channel.sink.add(jsonEncode(message)); // Send to WebSocket
      } catch (_) {
        // Handle any errors that occur
      }
    });
  }

  // Initialize WebSocket connection
  void initializeWebSocket() {
    //Emulator
    channel = IOWebSocketChannel.connect('ws://10.0.2.2:8765');
    //Laptop
    // channel = IOWebSocketChannel.connect('ws://<>:8765');
    channel.stream.listen((dynamic data) {
      data = jsonDecode(data);
      if (data['data'] == null) return;

      switch (data['data']) {
        case 0:
          status = DetectionStatus.noPose;
          break;
        case 1:
          status = DetectionStatus.fail;
          break;
        case 2:
          status = DetectionStatus.success;
          break;
        case 3:
          status = DetectionStatus.partial;
          break;
        default:
          status = DetectionStatus.noPose;
      }
      setState(() {});
    }, onError: (dynamic error) {
      debugPrint('WebSocket Error: $error');
    }, onDone: () {
      debugPrint('WebSocket connection closed');
    });
  }

  // Compress the captured image
  Uint8List compressImage(String imagePath, {int quality = 85}) {
    final image = img.decodeImage(Uint8List.fromList(File(imagePath).readAsBytesSync()))!;
    return img.encodeJpg(image, quality: quality);
  }

  // Clean up the resources
  @override
  void dispose() {
    controller?.dispose();
    channel.sink.close();
    super.dispose();
  }

  ////
  @override
  Widget build(BuildContext context) {
    String title = getAsanaName(widget.asanaNumber);
    // String statusMessage = getStatusMessage(widget.asanaNumber);

    return Scaffold(
      appBar: AppBar(
        title: Text(title),
        actions: [
          IconButton(
            icon: Icon(cameraIndex == 0
                ? Icons.cameraswitch_outlined
                : Icons.cameraswitch),
            onPressed: () {
              setState(() {
                cameraIndex = cameraIndex == 0 ? 1 : 0; // Toggle camera
                initializeCamera();
              });
            },
          ),
        ],
      ),
      body: Stack(
        children: [
          if (controller != null && controller!.value.isInitialized)
            Positioned.fill(
              child: AspectRatio(
                aspectRatio: controller!.value.aspectRatio,
                child: CameraPreview(controller!),
              ),
            )
          else
            const Center(
              child: CircularProgressIndicator(), // Display loading indicator while initializing camera
            ),
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              height: 100,
              width: double.infinity,
              color: Colors.black54,
              child: Center(
                child: Text(
                  currentStatus,
                  style: const TextStyle(
                    fontSize: 20,
                    color: Colors.white,
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  // Method to get the asana name based on the number
  String getAsanaName(int asanaNumber) {
    switch (asanaNumber) {
      case 1:
        return "Pranamasana";
      case 2:
        return "Hastauttanasana";
      case 3:
        return "Hastapadasana";
      case 4:
        return "Right Ashwa Sanchalanasana";
      case 5:
        return "Left Ashwa Sanchalanasana";
      case 6:
        return "Dandasana";
      case 7:
        return "Ashtanga Namaskara";
      case 8:
        return "Bhujangasana";
      case 9:
        return "Adho Mukha Svanasana";
      default:
        return "<Asana Name>";
    }
  }
}



// void main() {
//   WidgetsFlutterBinding.ensureInitialized();
//   runApp(const MyApp());
// }

// class MyApp extends StatelessWidget {
//   const MyApp({super.key});
//
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       title: 'Face Recognition Application',
//       theme: ThemeData(
//           useMaterial3: true
//       ),
//       home: const CameraScreen(),
//     );
//   }
// }

// class CameraScreen extends StatefulWidget {
//   const CameraScreen({super.key});
//
//   @override
//   State<CameraScreen> createState() => _CameraScreenState();
// }



// enum DetectionStatus {noPose, fail, success}
//
// class _CameraScreenState extends State<CameraScreen> {
//   CameraController? controller;
//   late WebSocketChannel channel;
//   DetectionStatus? status;
//
//   String get currentStatus {
//     if(status == null) {
//       return "Initializing...";
//     }
//     switch(status!){
//       case DetectionStatus.noPose:
//         return "No Asana Detected in the screen";
//       case DetectionStatus.fail:
//         return "Incorrect Pose Detected";
//       case DetectionStatus.success:
//         return "You're Doing Great Baby!";
//     }
//   }
//
//   Color get currentStatusColor {
//     if(status == null) {
//       return Colors.grey;
//     }
//     switch(status!){
//       case DetectionStatus.noPose:
//         return Colors.grey;
//       case DetectionStatus.fail:
//         return Colors.red;
//       case DetectionStatus.success:
//         return Colors.greenAccent;
//     }
//   }
//
//   @override
//   void initState() {
//     super.initState();
//     initializeCamera();
//     initializeWebSocket();
//   }
//
//   Future<void> initializeCamera() async {
//     final cameras = await availableCameras();
//     final firstCamera = cameras[0]; // back 0th index & front 1st index
//
//     controller = CameraController(
//       firstCamera,
//       ResolutionPreset.medium,
//       enableAudio: false,
//     );
//
//     await controller!.initialize();
//     setState(() {});
//
//     Timer.periodic(const Duration(seconds: 3), (timer) async {
//       try{
//         final image = await controller!.takePicture();
//         final compressedImageBytes = compressImage(image.path);
//         channel.sink.add(compressedImageBytes);
//       }catch(_){}
//     });
//   }
//
//   void initializeWebSocket() {
//     // 0.0.0.0 -> 10.0.2.2 (emulator)
//     channel = IOWebSocketChannel.connect('ws://10.0.2.2:8765');
//     channel.stream.listen((dynamic data) {
//       debugPrint(data);
//       data = jsonDecode(data);
//       if(data['data'] == null){
//         debugPrint('Server error occurred in recognizing face');
//         return;
//       }
//       switch(data['data']){
//         case 0:
//           status = DetectionStatus.noPose;
//           break;
//         case 1:
//           status = DetectionStatus.fail;
//           break;
//         case 2:
//           status = DetectionStatus.success;
//           break;
//         default:
//           status = DetectionStatus.noPose;
//           break;
//       }
//       setState(() {});
//     }, onError: (dynamic error) {
//       debugPrint('Error: $error');
//     }, onDone: () {
//       debugPrint('WebSocket connection closed');
//     });
//   }
//
//   Uint8List compressImage(String imagePath, {int quality = 85}) {
//     final image = img.decodeImage(Uint8List.fromList(File(imagePath).readAsBytesSync()))!;
//     final compressedImage = img.encodeJpg(image, quality: quality); // lossless compression
//     return compressedImage;
//   }
//
//   @override
//   void dispose() {
//     controller?.dispose();
//     channel.sink.close();
//     super.dispose();
//   }
//
//   @override
//   Widget build(BuildContext context) {
//     if (!(controller?.value.isInitialized ?? false)) {
//       return const SizedBox();
//     }
//
//     return Stack(
//       children: [
//         Positioned.fill(
//           child: AspectRatio(
//             aspectRatio: controller!.value.aspectRatio,
//             child: CameraPreview(controller!),
//           ),
//         ),
//         Align(
//           alignment: const Alignment(0, .85),
//           child: ElevatedButton(
//             style: ElevatedButton.styleFrom(
//                 surfaceTintColor: currentStatusColor
//             ),
//             child: Text(currentStatus, style: const TextStyle(fontSize: 20),),
//             onPressed: (){},
//           ),
//         )
//       ],
//     );
//   }
// }
