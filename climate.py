"""Climate platform for Synthetic Climate."""

from __future__ import annotations

from typing import Any

from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature
from homeassistant.components.climate.const import HVACAction, HVACMode
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
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import StateType

from .const import CONF_BATTERY_ENTITY, CONF_TEMPERATURE_ENTITY, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Synthetic Climate climate entity."""
    async_add_entities([SyntheticClimateEntity(hass, entry)])


class SyntheticClimateEntity(ClimateEntity, RestoreEntity):
    """Read-only climate entity backed by temperature and battery sensors."""

    _attr_has_entity_name = False
    _attr_icon = "mdi:pool-thermometer"
    _attr_hvac_modes = [HVACMode.OFF]
    _attr_hvac_mode = HVACMode.OFF
    _attr_hvac_action = HVACAction.OFF
    _attr_supported_features = ClimateEntityFeature(0)
    _attr_precision = 0.1
    _attr_target_temperature_step = 0.1
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the synthetic climate entity."""
        self.hass = hass
        self.entry = entry
        cfg = self._config

        self._attr_unique_id = cfg[CONF_UNIQUE_ID]
        self._attr_suggested_object_id = cfg[CONF_UNIQUE_ID]
        self._attr_name = cfg[CONF_NAME]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, cfg[CONF_UNIQUE_ID])},
            "name": cfg[CONF_NAME],
            "manufacturer": "Synthetic Climate",
        }

    @property
    def _config(self) -> dict[str, Any]:
        """Return merged config entry data and options."""
        cfg = dict(self.entry.data)
        cfg.update(self.entry.options)
        return cfg

    @property
    def temperature_entity_id(self) -> str:
        """Return source temperature entity id."""
        return self._config[CONF_TEMPERATURE_ENTITY]

    @property
    def battery_entity_id(self) -> str | None:
        """Return source battery entity id."""
        return self._config.get(CONF_BATTERY_ENTITY)

    @property
    def temperature_unit(self) -> str:
        """Return the unit used by the source temperature sensor."""
        state = self.hass.states.get(self.temperature_entity_id)
        if state and state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == UnitOfTemperature.FAHRENHEIT:
            return UnitOfTemperature.FAHRENHEIT
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self) -> float | None:
        """Return current temperature from the source sensor."""
        return _float_state(self.hass, self.temperature_entity_id)

    @property
    def extra_state_attributes(self) -> dict[str, StateType]:
        """Return translated source attributes."""
        attrs: dict[str, StateType] = {
            "temperature_entity_id": self.temperature_entity_id,
        }
        battery_entity = self.battery_entity_id
        if battery_entity:
            attrs["battery_entity_id"] = battery_entity
            attrs["battery_level"] = _float_state(self.hass, battery_entity)
            attrs["battery_unit"] = PERCENTAGE
        return attrs

    async def async_added_to_hass(self) -> None:
        """Subscribe to source entity state changes."""
        await super().async_added_to_hass()
        entity_ids = [self.temperature_entity_id]
        if self.battery_entity_id:
            entity_ids.append(self.battery_entity_id)

        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                entity_ids,
                self._async_source_changed,
            )
        )

    @callback
    def _async_source_changed(self, event: Event) -> None:
        """Write state when a source entity changes."""
        self.async_write_ha_state()


def _float_state(hass: HomeAssistant, entity_id: str) -> float | None:
    """Return the state as float, or None when unavailable."""
    state = hass.states.get(entity_id)
    if state is None or state.state in {STATE_UNKNOWN, STATE_UNAVAILABLE}:
        return None
    try:
        return float(state.state)
    except (TypeError, ValueError):
        return None
