# Synthetic Climate

Synthetic Climate is a Home Assistant custom integration that creates a read-only `climate` entity from existing sensor entities.

It is useful when a temperature sensor should appear in Home Assistant as a climate device, for example to show pool, spa, room, or equipment temperature in climate dashboards while keeping the source sensor as the actual data provider.

## Features

- Creates one `climate` entity from a configured temperature sensor.
- Optionally links a battery sensor and exposes its value as extra state attributes.
- Updates automatically when the source temperature or battery sensor changes.
- Uses the source temperature sensor unit, including Celsius or Fahrenheit.
- Provides a config flow and options flow in the Home Assistant UI.
- Keeps the climate entity read-only with HVAC mode and action set to `off`.

## Installation

Copy this integration directory into your Home Assistant `custom_components` directory:

```text
config/
  custom_components/
    synthetic_climate/
      __init__.py
      climate.py
      config_flow.py
      const.py
      manifest.json
      strings.json
      translations/
```

If you cloned this repository directly, make sure the final directory name is:

```text
custom_components/synthetic_climate
```

Restart Home Assistant after copying the files.

## Setup

1. Open Home Assistant.
2. Go to **Settings** > **Devices & services**.
3. Select **Add Integration**.
4. Search for **Synthetic Climate**.
5. Fill in the form:
   - **Name**: Display name for the generated climate entity.
   - **Unique ID**: Stable unique identifier for the entity.
   - **Temperature sensor**: Source sensor that provides the current temperature.
   - **Battery sensor**: Optional source sensor that provides battery level.
6. Submit the form.

Home Assistant will create a climate entity that mirrors the selected temperature sensor.

## Usage

Use the generated climate entity anywhere Home Assistant accepts climate entities, such as dashboards, automations, templates, or scripts.

The entity reports:

- `current_temperature` from the configured temperature sensor.
- `temperature_entity_id` as an extra state attribute.
- `battery_entity_id`, `battery_level`, and `battery_unit` when a battery sensor is configured.

The climate entity does not heat, cool, or control another device. It is intentionally read-only and reports `off` for HVAC mode and HVAC action.

## Changing Settings

To change the source sensors or displayed entity details:

1. Open **Settings** > **Devices & services**.
2. Find **Synthetic Climate**.
3. Open the integration options.
4. Update the configured name, unique ID, temperature sensor, or battery sensor.

The integration reloads after options are saved.

## Notes

- The temperature sensor should have a numeric state.
- Unavailable, unknown, or non-numeric source states are reported as `None` by the climate entity.
- The battery sensor is optional and is expected to expose a numeric percentage value.
- This integration has no external Python package requirements.
