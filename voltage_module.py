import globals
import machine

adc = machine.ADC(machine.Pin(globals.ADC_PIN))
adc.atten(machine.ADC.ATTN_11DB)  # Full range: 0-3.6V

def read_voltage():
    adc_value = adc.read() - 1900
    print(adc_value)
    voltage = ((adc_value) / 4095.0) * 3.3 * globals.CALIBRATION_FACTOR
    print(f"Voltage: {voltage:.2f} V")
    if voltage < 0:
        voltage = 0
    return voltage * (220.0 / 3.3)
