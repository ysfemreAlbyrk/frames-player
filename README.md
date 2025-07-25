# Frame Player

A simple application to view and play image frames, created by Yusuf Emre ALBAYRAK for project HÜMA in TEKNOFEST 2025 HYZ competition.

## Features

*   **Frame Playback**: View and play sequences of image frames.
*   **Directory Loading**: Load frames from a specified directory. The application looks for files matching the pattern `frame_*.webp`.
*   **Adjustable Speed**: Control playback speed with options ranging from 0.25x to 32x.
*   **Navigation Controls**: Easily navigate through frames using next/previous buttons and a slider.
*   **Responsive Display**: Frames are resized to fit the application window while maintaining aspect ratio.
*   **Command-line Interface**: Option to specify the frames directory directly when launching the application.

## Usage

### Running the Application

1.  **Prerequisites**:
    *   Python 3.x installed.
    *   
        ```bash
        pip install opencv-python Pillow
        ```

2.  **Launching from Source**:
    *   Navigate to the project directory in your terminal:
        ```bash
        cd d:/ProjelerV2/frames-player
        ```
    *   Run the Python script:
        ```bash
        python frame_player.py
        ```
    *   The application will open, prompting you to select a folder containing your image frames.

3.  **Launching with a Specific Directory**:
    You can also specify the directory containing the frames directly as a command-line argument:
    ```bash
    python frame_player.py /path/to/your/frames
    ```
    Replace `/path/to/your/frames` with the actual path to the directory containing your `frame_*.webp` files.

### Interacting with the Application

*   **Open Folder**: Use the "File" menu to select a directory containing your image frames.
*   **Play/Pause**: Click the "▶" button to start or pause playback.
*   **Next/Previous Frame**: Use the ">>" and "<<" buttons to move to the next or previous frame.
*   **Frame Slider**: Drag the slider to quickly jump to a specific frame.
*   **Speed Control**: Use the dropdown menu to select the desired playback speed.
*   **Exit**: Use the "File" menu to close the application.

## About

**Frame Player v0.1**

A simple application to view and play image frames.

Created by Yusuf Emre ALBAYRAK for project HÜMA in TEKNOFEST 2025 HYZ competition.

[GitHub Repository](https://github.com/ysfemreAlbyrk/frames-player)
