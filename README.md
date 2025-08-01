# Face Recognition Attendance System

This project is a facial recognition-based attendance system that identifies students using their facial data and updates attendance records accordingly. The program utilizes a camera feed to detect and recognize faces, then retrieves and displays corresponding student data from a JSON file.

## Features

- Detect and recognize faces using the `face_recognition` library.
- Display student information (e.g., name, department, total attendance) on a graphical background.
- Record attendance in a JSON file while preventing duplicate entries within a specific timeframe.
- Resize and display student photos.

## Requirements

### Python Libraries

Install the required Python libraries using pip:

```bash
pip install numpy opencv-python opencv-contrib-python face_recognition cvzone
```

### Additional Resources

1. **Background Image:** Place the background image in the `Resources` folder and name it `background.png`.
2. **Mode Images:** Add images for different application modes in the `Resources/Modes` folder.
3. **Student Data:** A JSON file named `students.json` should contain student information (in UTF-8 encoding for Arabic support).
4. **Student Photos:** Store student photos in a folder named `blob` with filenames corresponding to their IDs (e.g., `1.png`, `2.png`).
5. **Encoding File:** Generate or provide an encoding file named `EncodeFile.pickle` for facial data.

## How It Works

1. **Initialization:**
   - Load the background and mode images.
   - Load the facial encoding file (`EncodeFile.pickle`).
   - Read the student data from `students.json`.

2. **Face Detection:**
   - Capture frames from the webcam.
   - Detect and encode faces in the frame.
   - Compare the detected face against known encodings to identify the student.

3. **Attendance Marking:**
   - Retrieve student data based on their ID.
   - Check if sufficient time has elapsed since their last recorded attendance.
   - Update their attendance record in the JSON file if eligible.

4. **Display:**
   - Overlay the webcam feed onto a graphical background.
   - Display student information and their photo on the interface.

## Folder Structure

```
.
├── blob/               # Folder containing student photos
├── Resources/
│   ├── background.png  # Background image for the GUI
│   ├── Modes/          # Folder containing mode images
├── students.json       # JSON file with student data
├── EncodeFile.pickle   # Pickle file with face encodings and IDs
├── attendance.py       # Main Python script
```

## Student JSON File Format

The `students.json` file should have the following format:

```json
{
  "1": {
    "الاسم": "Hammam Rassam",
    "التخصص": "Software Engineering",
    "سنة البدء": 2024,
    "اجمالي_الحضور": 7,
    "التقدير": "G",
    "السنة": 1,
    "اخر حضور": "2025-02-15 18:47:23"
  }
}
```

## Running the Application

1. Ensure the necessary resources are placed in their respective folders.
2. Run the Python script:

   ```bash
   python attendance.py
   ```

## Notes

- Make sure the `EncodeFile.pickle` is properly generated to include all student encodings.
- Adjust image paths and positions as necessary to fit your specific requirements.
- To support Arabic text rendering, additional libraries like `Pillow`, `arabic_reshaper`, and `python-bidi` may be required.

## Future Enhancements

- Integrate with a database for better scalability.
- Add support for mobile or web-based access.
- Implement a notification system for students upon attendance marking.
