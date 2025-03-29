import machine
import settings
import time
import math


def read_voltage():
    # Calibration factor (initial estimate, adjust later)
    CALIBRATION_FACTOR = settings.Settings.get("calibration_factor")  # Adjust this based on real measurements
    adc = machine.ADC(machine.Pin(settings.Settings.get("adc_pin")))
    adc.atten(machine.ADC.ATTN_11DB)  # Full range: 0-3.6V
    adc.width(machine.ADC.WIDTH_12BIT)
    
    # Sampling settings
    NUM_SAMPLES = settings.Settings.get("num_samples")
    SAMPLE_INTERVAL = 0.2 / NUM_SAMPLES  # Spread over 1/5th of a 50Hz cycle

    sum_values = 0
    sum_squares = 0
    

    """Reads AC voltage using ZMPT101B and computes RMS value with noise filtering."""
    samples = []
    
    # Take multiple samples
    for _ in range(NUM_SAMPLES):
        adc_value = adc.read()
        sum_values += adc_value
        sum_squares += adc_value ** 2
        time.sleep(SAMPLE_INTERVAL)

    mean_value = sum_values / NUM_SAMPLES
    mean_squared = sum_squares / NUM_SAMPLES
    rms_adc = math.sqrt(mean_squared - mean_value ** 2)  # RMS calculation

    # Convert ADC reading to voltage (ESP32 12-bit ADC: 0-4095 -> 0-3.3V)
    rms_voltage = (rms_adc / 4095.0) * 3.3

    # Scale to actual AC voltage
    ac_voltage = rms_voltage * CALIBRATION_FACTOR
    # print(ac_voltage)
    return ac_voltage
