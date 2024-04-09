'''
testing for the arlyn driver over a Serial connection

running this will zero the scale
'''

import pytest
import random

from arlyn.driver import Scale

SCALE_ADDRESS_SERIAL = 'COM6' #ex: 'COM14' or '/dev/ttyS0'

@pytest.mark.asyncio
async def test_get_weight_string_TCP_connection() -> None:
    async with Scale(SCALE_ADDRESS_SERIAL) as scale:
        assert await scale.get_weight_string()

@pytest.mark.asyncio
async def test_get_weight_dict_TCP_connection() -> None:
    async with Scale(SCALE_ADDRESS_SERIAL) as scale:
        scale_dict = await scale.get_weight_dict()
        assert type(scale_dict['date'] is str)
        assert type(scale_dict['time'] is str)
        assert type(scale_dict['unit'] is str)
        assert type(scale_dict['weight']) is float
        assert type(scale_dict['netMode']) is bool

@pytest.mark.asyncio
async def test_get_json_string_TCP_connection() -> None:
    async with Scale(SCALE_ADDRESS_SERIAL) as scale:
        assert await scale.get_json_string()

@pytest.mark.asyncio
async def test_get_json_dict_TCP_connection() -> None:
    async with Scale(SCALE_ADDRESS_SERIAL) as scale:
        scale_dict = await scale.get_json_dict()
        assert type(scale_dict['bSIndi'] is bool)
        assert type(scale_dict['sNet'] is str)
        assert type(scale_dict['sUnit'] is str)
        assert type(scale_dict['sWeight'] is str)
        assert type(scale_dict['_CMD_ACK'] is str)
        assert type(scale_dict['_id'] is bool)
        assert type(scale_dict['_name'] is str)
        assert type(scale_dict['_rSNo'] is int)
        assert type(scale_dict['_sSNo'] is int)

@pytest.mark.asyncio
async def test_toggle_unit_TCP_connection() -> None:
    async with Scale(SCALE_ADDRESS_SERIAL) as scale:
       await scale.toggle_unit()

@pytest.mark.asyncio
async def test_get_unit_TCP_connection() -> None:
    async with Scale(SCALE_ADDRESS_SERIAL) as scale:
        assert await scale.get_unit()

@pytest.mark.asyncio
async def test_change_unit_TCP_connection() -> None:
    async with Scale(SCALE_ADDRESS_SERIAL) as scale:
        current_unit = await scale.get_unit()
        list_of_units = list(scale.units)
        list_of_units.remove(current_unit)
        unit = random.choice(list_of_units)
        await scale.change_unit(unit)

@pytest.mark.asyncio
async def test_zero_scale_TCP_connection() -> None:
    async with Scale(SCALE_ADDRESS_SERIAL) as scale:
        await scale.zero_scale()