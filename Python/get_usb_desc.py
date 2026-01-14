import usb.core
import usb.util


def find_device_by_serial(vid, pid, serial_number):
    """
    Find a USB device by its Vendor ID, Product ID, and serial number.
    """
    def match_serial(device):
        """Custom matching function to filter devices by serial number."""
        try:
            serial = usb.util.get_string(device, device.iSerialNumber)
            return serial == serial_number
        except (ValueError, usb.core.USBError):
            return False

    dev = usb.core.find(idVendor=vid, idProduct=pid, custom_match=match_serial)
    return dev

def get_all_devices(vid, pid):
    """
    Find and list all devices with the specified Vendor ID and Product ID.
    """
    devs = usb.core.find(find_all=True, idVendor=vid, idProduct=pid)

    if not devs:
        print(f"No devices found with VID 0x{vid:04x} and PID 0x{pid:04x}.")
        return None

    print("Found the following devices:")
    for i, dev in enumerate(devs):
        serial_number = usb.util.get_string(dev, dev.iSerialNumber)
        print(f"Device {i}: Serial Number = {serial_number}")
    return devs

def main(vid, pid, sn):
    # First, list all connected devices to find their serial numbers
    get_all_devices(vid, pid)

    # Find and connect to the specific device
    dev = find_device_by_serial(vid, pid, sn)

    if dev is None:
        print(f"Device with serial number '{sn}' not found.")
        return
    else:
        print(f"\nSuccessfully connected to device with serial number: {usb.util.get_string(dev, dev.iSerialNumber)}")
        # Now you can work with the 'dev' object

    # Read the device descriptor
    print(f'Manufacturer: {usb.util.get_string(dev, dev.iManufacturer)}')
    print(f'Product: {usb.util.get_string(dev, dev.iProduct)}')
    
    # To get a specific string descriptor by index:
    # The first parameter is the device, the second is the string index.
    # The third parameter specifies the language ID (0 for default).
    # str_index = 0xEE  # WINUSB string descriptor index
    for str_index in range(255):
        try:
            string_desc = usb.util.get_string(dev, str_index, 0)
            print(f'String Descriptor at index {str_index}: "{string_desc}"')
        except usb.core.USBError:
            # ignore non-existing strings
            pass

# must be run as:
#   sudo `which python3` get_usb_desc.py
if __name__ == "__main__":
    # The Vendor ID and Product ID of your devices
    TARGET_VID = 0x1d50
    TARGET_PID = 0x606f
    TARGET_SN = "3069375D3232"
    main(TARGET_VID, TARGET_PID, TARGET_SN)

