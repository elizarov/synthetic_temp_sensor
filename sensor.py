"""Sensor platform for Synthetic Temp Sensor."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_NAME,
    CONF_UNIQUE_ID,
    PERCENTAGE,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    UnitOfTemperature,
)
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import CONF_BATTERY_ENTITY, CONF_TEMPERATURE_ENTITY, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Synthetic Temp Sensor entities."""
    cfg = dict(entry.data)
    cfg.update(entry.options)
    entities: list[SensorEntity] = [SyntheticTemperatureSensor(hass, entry)]
    if cfg.get(CONF_BATTERY_ENTITY):
        entities.append(SyntheticBatterySensor(hass, entry))
    async_add_entities(entities)


class SyntheticSensorBase(SensorEntity):
    """Base class for sensors backed by configured source entities."""

    _attr_has_entity_name = False
    _attr_should_poll = False
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the synthetic sensor."""
        self.hass = hass
        self.entry = entry

    @property
    def _config(self) -> dict[str, Any]:
        """Return merged config entry data and options."""
        cfg = dict(self.entry.data)
        cfg.update(self.entry.options)
        return cfg

    @property
    def _source_entity_id(self) -> str:
        """Return the source entity id."""
        raise NotImplementedError

    async def async_added_to_hass(self) -> None:
        """Subscribe to source sensor state changes."""
        await super().async_added_to_hass()
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._source_entity_id],
                self._async_source_changed,
            )
        )

    @callback
    def _async_source_changed(self, event: Event) -> None:
        """Write state when the source entity changes."""
        self.async_write_ha_state()


class SyntheticTemperatureSensor(SyntheticSensorBase):
    """Temperature sensor backed by the configured source temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the synthetic temperature sensor."""
        super().__init__(hass, entry)
        cfg = self._config

        self._attr_unique_id = cfg[CONF_UNIQUE_ID]
        self._attr_suggested_object_id = cfg[CONF_UNIQUE_ID]
        self._attr_name = cfg[CONF_NAME]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, cfg[CONF_UNIQUE_ID])},
            "name": cfg[CONF_NAME],
            "manufacturer": "Synthetic Temp Sensor",
        }

    @property
    def _source_entity_id(self) -> str:
        """Return source temperature entity id."""
        return self.temperature_entity_id

    @property
    def temperature_entity_id(self) -> str:
        """Return source temperature entity id."""
        return self._config[CONF_TEMPERATURE_ENTITY]

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit used by the source temperature sensor."""
        state = self.hass.states.get(self.temperature_entity_id)
        if state:
            unit = state.attributes.get(ATTR_UNIT_OF_MEASUREMENT)
            if unit:
                return unit
        return UnitOfTemperature.CELSIUS

    @property
    def native_value(self) -> float | None:
        """Return temperature from the source sensor."""
        return _float_state(self.hass, self.temperature_entity_id)

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return source temperature entity metadata."""
        return {"temperature_entity_id": self.temperature_entity_id}


class SyntheticBatterySensor(SyntheticSensorBase):
    """Battery sensor backed by the configured source battery sensor."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the synthetic battery sensor."""
        super().__init__(hass, entry)
        cfg = self._config

        self._attr_unique_id = f"{cfg[CONF_UNIQUE_ID]}_battery"
        self._attr_suggested_object_id = f"{cfg[CONF_UNIQUE_ID]}_battery"
        self._attr_name = f"{cfg[CONF_NAME]} Battery"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, cfg[CONF_UNIQUE_ID])},
            "name": cfg[CONF_NAME],
            "manufacturer": "Synthetic Temp Sensor",
        }

    @property
    def _source_entity_id(self) -> str:
        """Return source battery entity id."""
        return self.battery_entity_id

    @property
    def battery_entity_id(self) -> str:
        """Return source battery entity id."""
        return self._config[CONF_BATTERY_ENTITY]

    @property
    def native_value(self) -> float | None:
        """Return battery level from the source sensor."""
        return _float_state(self.hass, self.battery_entity_id)

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return source battery entity metadata."""
        return {"battery_entity_id": self.battery_entity_id}


def _float_state(hass: HomeAssistant, entity_id: str) -> float | None:
    """Return the state as float, or None when unavailable."""
    state = hass.states.get(entity_id)
    if state is None or state.state in {STATE_UNKNOWN, STATE_UNAVAILABLE}:
        return None
    try:
        return float(state.state)
    except (TypeError, ValueError):
        return None
