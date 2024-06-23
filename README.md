# Baud Rate Detection Utility

This repository contains a utility for detecting the baud rate of a serial device. The utility supports multiple modes, including automatic scan, brute-force, deep brute-force, and pulse detection.

## Features

- **Automatic Scan**: Tests common baud rates and falls back to brute-force if necessary.
- **Brute-force with Custom Range**: Allows the user to specify a custom range of baud rates to test.
- **Deep Brute-force with Custom Range**: Performs a thorough brute-force scan with a step size of 1.
- **Pulse Detection (Experimental)**: Estimates the baud rate by detecting pulse intervals.

## Requirements

- Python 3.x
- `pyserial` and `colorama` packages

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/deadinternetfox/Baud-Rate-Brute.git
    cd Baud-Rate-Brute
    ```

2. **Install dependencies**:
    The script will automatically check for and install required dependencies (`pyserial` and `colorama`) if they are not already installed.

## Usage

1. **Run the script**:
    Double-click the `run.bat` file or run it from the command prompt to start the baud rate detection utility.

    ```sh
    run.bat
    ```

2. **Select the COM port**:
    The script will list all available COM ports. Enter the number corresponding to the COM port you want to test.

3. **Choose the attack mode**:
    Select the desired attack mode from the menu:
    - `1`: Automatic Scan (Common baud rates + Brute-force)
    - `2`: Brute-force with Custom Range
    - `3`: Deep Brute-force with Custom Range
    - `4`: Pulse Detection (Experimental)

4. **Follow the prompts**:
    The script will guide you through the process, testing different baud rates and displaying the results.

## Logging

The script logs all results to a file named `Baud Rate Brute Results.txt` in the same directory. This includes the tested baud rates, received data, and estimated baud rates (for pulse detection).

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Scheme
