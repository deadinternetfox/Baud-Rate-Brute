import serial
import serial.tools.list_ports
import time
import colorama
from colorama import Fore, Style
from datetime import datetime

# Initialize colorama
colorama.init(autoreset=True)

# List of common baud rates to test
baud_rates = [
    300, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200
]

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = []
    print(f"{Fore.BLUE}Available COM ports:")
    for i, port in enumerate(ports, start=1):
        available_ports.append(port.device)
        print(f"{Fore.CYAN}{i}. {port.device}: {port.description}")
    return available_ports

def select_serial_port(available_ports):
    while True:
        try:
            index = int(input(f"{Fore.YELLOW}Please select a COM port by number from the list above: "))
            if 1 <= index <= len(available_ports):
                return available_ports[index - 1]
            else:
                print(f"{Fore.RED}Invalid selection. Please try again.")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.")

def validate_data(data):
    if data and len(data) > 0:
        if data == b'\x00' * len(data) or data == b'\xFF' * len(data):
            return False
        expected_pattern = b'\x7f'  # Replace with actual expected pattern
        if expected_pattern in data:
            return True
    return False

def test_baud_rate(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate, timeout=2)
        print(f"{Fore.CYAN}Testing baud rate: {baudrate}")
        ser.flushInput()
        time.sleep(2)  # Wait for data to stabilize
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            if validate_data(data):
                print(f"{Fore.GREEN}Valid data received at {baudrate} baud: {data}")
                log_results(baudrate, data)
                return True
            else:
                print(f"{Fore.RED}Received data is not valid at {baudrate} baud: {data}")
        else:
            print(f"{Fore.YELLOW}No data received at {baudrate} baud.")
        ser.close()
    except Exception as e:
        print(f"{Fore.RED}Failed to connect at {baudrate} baud: {e}")
    return False

def brute_force_baud_rate(port, start=9600, end=115200, step=100):
    print(f"{Fore.MAGENTA}Starting brute-force baud rate detection...")
    for baudrate in range(start, end + 1, step):
        if test_baud_rate(port, baudrate):
            print(f"{Fore.GREEN}Successful connection at baud rate: {baudrate}")
            return baudrate
    print(f"{Fore.RED}Brute-force failed to find a working baud rate in the range {start} to {end}")
    return None

def deep_brute_force_baud_rate(port, start=1, end=115200, step=1):
    print(f"{Fore.MAGENTA}Starting deep brute-force baud rate detection...")
    for baudrate in range(start, end + 1, step):
        if test_baud_rate(port, baudrate):
            print(f"{Fore.GREEN}Successful connection at baud rate: {baudrate}")
            return baudrate
    print(f"{Fore.RED}Deep brute-force failed to find a working baud rate in the range {start} to {end}")
    return None

def pulse_detection(port):
    try:
        ser = serial.Serial(port, 115200, timeout=0)  # Use a high baud rate to capture fast transitions
        print(f"{Fore.CYAN}Starting pulse detection...")
        pulse_times = []
        ser.flushInput()
        
        while len(pulse_times) < 100:  # Capture 100 pulses for better accuracy
            byte = ser.read(1)
            if byte:
                pulse_times.append(datetime.now())

        if len(pulse_times) > 1:
            pulse_durations = [(pulse_times[i] - pulse_times[i - 1]).total_seconds() for i in range(1, len(pulse_times))]
            average_pulse_duration = sum(pulse_durations) / len(pulse_durations)
            estimated_baud_rate = 1 / average_pulse_duration
            print(f"{Fore.GREEN}Estimated baud rate: {estimated_baud_rate:.2f}")
            log_pulse_detection_results(pulse_times, estimated_baud_rate)
        else:
            print(f"{Fore.RED}Not enough pulses detected to estimate baud rate.")
        ser.close()
    except Exception as e:
        print(f"{Fore.RED}Failed to perform pulse detection: {e}")

def log_results(baudrate, data):
    with open("Baud Rate Brute Results.txt", "a") as log_file:
        log_file.write(f"Baud rate: {baudrate}, Data: {data}\n")

def log_pulse_detection_results(pulse_times, estimated_baud_rate):
    with open("Baud Rate Brute Results.txt", "a") as log_file:
        log_file.write(f"Pulse detection times: {pulse_times}, Estimated baud rate: {estimated_baud_rate:.2f}\n")

def display_banner():
    banner = """
    ================================
    |  Baud Rate Detection Utility  |
    |         Version 1.0           |
    |   Author: Scheme              |
    ================================
    """
    print(Fore.GREEN + banner + Style.RESET_ALL)

def select_attack_mode():
    print(f"{Fore.BLUE}Select Attack Mode:")
    print(f"{Fore.GREEN}1. Automatic Scan (Common baud rates + Brute-force)")
    print(f"{Fore.CYAN}2. Brute-force with Custom Range")
    print(f"{Fore.CYAN}3. Deep Brute-force with Custom Range")
    print(f"{Fore.RED}4. Pulse Detection (Experimental)")
    while True:
        try:
            choice = int(input(f"{Fore.YELLOW}Enter your choice (1, 2, 3, or 4): "))
            if choice in [1, 2, 3, 4]:
                return choice
            else:
                print(f"{Fore.RED}Invalid selection. Please try again.")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.")

def get_custom_range():
    while True:
        try:
            start = int(input(f"{Fore.YELLOW}Enter the start of the baud rate range: "))
            end = int(input(f"{Fore.YELLOW}Enter the end of the baud rate range: "))
            step = int(input(f"{Fore.YELLOW}Enter the step value for brute-forcing: "))
            if start > 0 and end > start and step > 0:
                return start, end, step
            else:
                print(f"{Fore.RED}Invalid range or step. Please try again.")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter valid numbers.")

def main():
    display_banner()
    print(f"{Fore.BLUE}Starting baud rate detection utility...\n")
    
    # List and select serial port
    available_ports = list_serial_ports()
    if not available_ports:
        print(f"{Fore.RED}No COM ports found. Please connect a device and try again.")
        return

    selected_port = select_serial_port(available_ports)
    print(f"{Fore.GREEN}Selected COM port: {selected_port}\n")
    
    # Select attack mode
    attack_mode = select_attack_mode()
    
    if attack_mode == 1:
        # Test common baud rates
        for baud_rate in baud_rates:
            if test_baud_rate(selected_port, baud_rate):
                print(f"{Fore.GREEN}Found working baud rate: {baud_rate}")
                return
        
        # If common baud rates fail, attempt brute-force
        if not brute_force_baud_rate(selected_port):
            deep_brute_force_baud_rate(selected_port)
    elif attack_mode == 2:
        start, end, step = get_custom_range()
        brute_force_baud_rate(selected_port, start, end, step)
    elif attack_mode == 3:
        start, end, step = get_custom_range()
        deep_brute_force_baud_rate(selected_port, start, end, step)
    elif attack_mode == 4:
        pulse_detection(selected_port)

if __name__ == "__main__":
    main()
