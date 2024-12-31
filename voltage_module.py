import machine
import settings


def read_voltage():
    adc = machine.ADC(machine.Pin(settings.Settings.get("adc_pin")))
    adc.atten(machine.ADC.ATTN_11DB)  # Full range: 0-3.6V

    adc_value = adc.read() - 1900
    print(adc_value)
    voltage = ((adc_value) / 4095.0) * 3.3 * settings.Settings.get("calibration_factor")
    print(f"Voltage: {voltage:.2f} V")
    if voltage < 0:
        voltage = 0
    return voltage * (220.0 / 3.3)
