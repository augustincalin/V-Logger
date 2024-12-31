import urequests
import settings

def send_alert(voltage, count):
    
    try:
        # Data to send in the HTTP POST request
        data = {
            "voltage": voltage,
            "count": count,
            "status": "out_of_range",
            "message": f"""Voltage {voltage:.2f}V is outside the range [{settings.Settings.get("min_voltage")} ... {settings.Settings.get("max_voltage")}]V."""
        }
        # Send the HTTP POST request
        response = urequests.post(settings.Settings.get("alert_url"), json=data)
        
        # Check the response status
        if response.status_code == 200:
            print(f"Alert sent successfully: {voltage}")
        else:
            print(f"Failed to send alert! HTTP Status Code: {response.status_code}")
        
        # Close the response to free up resources
        response.close()

    except Exception as e:
        print(f"Error sending alert: {e}")