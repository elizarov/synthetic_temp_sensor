"""Config flow for Synthetic Temp Sensor."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_BATTERY_ENTITY,
    CONF_TEMPERATURE_ENTITY,
    DEFAULT_NAME,
    DEFAULT_UNIQUE_ID,
    DOMAIN,
)


def _schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    """Return the UI form schema."""
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_NAME,
                default=defaults.get(CONF_NAME, DEFAULT_NAME),
            ): selector.TextSelector(),
            vol.Required(
                CONF_UNIQUE_ID,
                default=defaults.get(CONF_UNIQUE_ID, DEFAULT_UNIQUE_ID),
            ): selector.TextSelector(),
            vol.Required(
                CONF_TEMPERATURE_ENTITY,
                default=defaults.get(CONF_TEMPERATURE_ENTITY),
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
            vol.Optional(
                CONF_BATTERY_ENTITY,
                default=defaults.get(CONF_BATTERY_ENTITY),
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor")
            ),
        }
    )


class SyntheticTempSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Synthetic Temp Sensor."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            unique_id = user_input[CONF_UNIQUE_ID].strip()
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            user_input[CONF_NAME] = user_input[CONF_NAME].strip()
            user_input[CONF_UNIQUE_ID] = unique_id
            if not user_input.get(CONF_BATTERY_ENTITY):
                user_input.pop(CONF_BATTERY_ENTITY, None)

            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_schema(),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return SyntheticTempSensorOptionsFlow(config_entry)


class SyntheticTempSensorOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Synthetic Temp Sensor."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Manage options."""
        current = dict(self._config_entry.data)
        current.update(self._config_entry.options)

        if user_input is not None:
            user_input[CONF_NAME] = user_input[CONF_NAME].strip()
            user_input[CONF_UNIQUE_ID] = user_input[CONF_UNIQUE_ID].strip()
            if not user_input.get(CONF_BATTERY_ENTITY):
                user_input.pop(CONF_BATTERY_ENTITY, None)
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=_schema(current),
        )
