# Synthetic Temp Sensor

Synthetic Temp Sensor is a Home Assistant custom integration that creates dashboard-friendly `sensor` entities from existing sensor entities.

It is useful when you want a cleaned-up synthetic device that exposes temperature and battery values as normal Home Assistant sensors while keeping the original source sensors as the actual data providers.

## Features

- Creates one temperature `sensor` entity from a configured temperature sensor.
- Optionally mirrors a battery sensor as a second `sensor` entity on the same synthetic device.
- Exposes source entity IDs as extra state attributes for traceability.
- Updates automatically when the source temperature or battery sensor changes.
- Uses the source temperature sensor unit, including Celsius or Fahrenheit.
- Provides a config flow and options flow in the Home Assistant UI.
- Ships a local brand icon for Home Assistant versions that support custom
  integration brand assets.
- Exposes measured values only and does not provide temperature controls.

## Installation

Copy this integration directory into your Home Assistant `custom_components` directory:

```text
config/
  custom_components/
    synthetic_temp_sensor/
      brand/
        icon.png
      __init__.py
      config_flow.py
      const.py
      manifest.json
      sensor.py
      strings.json
      translations/
```

If you cloned this repository directly, make sure the final directory name is:

```text
custom_components/synthetic_temp_sensor
```

Restart Home Assistant after copying the files.

## Setup

1. Open Home Assistant.
2. Go to **Settings** > **Devices & services**.
3. Select **Add Integration**.
4. Search for **Synthetic Temp Sensor**.
5. Fill in the form:
   - **Name**: Display name for the generated temperature sensor and synthetic device.
   - **Unique ID**: Stable unique identifier for the entity.
   - **Temperature sensor**: Source sensor that provides the current temperature.
   - **Battery sensor**: Optional source sensor that provides battery level.
6. Submit the form.

Home Assistant will create a temperature sensor that mirrors the selected temperature sensor. If a battery sensor is configured, it will also create a battery sensor attached to the same synthetic device.

## Usage

Use the generated sensor entities anywhere Home Assistant accepts sensors, such as dashboards, automations, templates, or scripts.

The temperature sensor reports:

- The numeric state from the configured temperature sensor.
- The source sensor unit, such as `°C` or `°F`.
- `temperature_entity_id` as an extra state attribute.

When a battery sensor is configured, the integration also creates a battery sensor with:

- `device_class` set to `battery`.
- Unit set to `%`.
- `battery_entity_id` as an extra state attribute.

The integration does not heat, cool, or control another device. It only mirrors source sensor state into a synthetic Home Assistant device.

## Changing Settings

To change the source sensors or displayed entity details:

1. Open **Settings** > **Devices & services**.
2. Find **Synthetic Temp Sensor**.
3. Open the integration options.
4. Update the configured name, unique ID, temperature sensor, or battery sensor.

The integration reloads after options are saved.

## Notes

- The temperature sensor should have a numeric state.
- Unavailable, unknown, or non-numeric source states are reported as `None` by the generated sensors.
- The battery sensor is optional and is expected to expose a numeric percentage value.
- This integration has no external Python package requirements.
