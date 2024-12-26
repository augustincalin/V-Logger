import urequests
import globals

def send_alert(voltage):
    
    try:
        # Data to send in the HTTP POST request
        data = {
            "voltage": voltage,
            "status": "out_of_range",
            "message": f"Voltage {voltage:.2f}V is outside the range [{globals.MIN_VOLTAGE} ... {globals.MAX_VOLTAGE}]V."
        }
        # Send the HTTP POST request
        response = urequests.post(globals.ALERT_URL, json=data)
        
        # Check the response status
        if response.status_code == 200:
            print(f"Alert sent successfully: {voltage}")
        else:
            print(f"Failed to send alert! HTTP Status Code: {response.status_code}")
        
        # Close the response to free up resources
        response.close()

    except Exception as e:
        print(f"Error sending alert: {e}")