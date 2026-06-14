"""Constants for Synthetic Temp Sensor."""

from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID

DOMAIN = "synthetic_temp_sensor"
PLATFORMS = ["sensor"]

CONF_TEMPERATURE_ENTITY = "temperature_entity"
CONF_BATTERY_ENTITY = "battery_entity"

DEFAULT_NAME = "Бассейн температура"
DEFAULT_UNIQUE_ID = "s_pool_temp"

CONFIG_KEYS = {
    CONF_NAME,
    CONF_UNIQUE_ID,
    CONF_TEMPERATURE_ENTITY,
    CONF_BATTERY_ENTITY,
}
