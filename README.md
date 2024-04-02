arlyn
=====

*This repository was adapted from the [alicat](https://github.com/numat/alicat/tree/master) repository*

This repository has not been fully tested and still a work in progress

TCP/Serial driver for [Arlyn UpScale Touchscreen Indicator](https://www.arlynscales.com/scales/arlyn-upscale-touchscreen-indicator/) with the RS-232 serial port upgrade option.

Example Connections
===================

| Type | Usage |
| --- | --- |
| The standard [DB9 cable](http://www.alicat.com/wpinstall/wp-content/uploads/2013/07/MD8DB9.jpg) connected directly to a computer (unix: `/dev/ttyS0`, windows: `COM1`). | Good with older computers that still have the connector. |
| The cable connected to a computer through a [USB converter](https://www.amazon.com/gp/product/B0007T27H8) (unix: `/dev/ttyUSB0`, windows: `COM1`). | Good for newer computers and maker boards such as Raspberry Pis. |
| The rj45 network port on the [Arlyn UpScale Touchscreen Indicator](https://www.arlynscales.com/scales/arlyn-upscale-touchscreen-indicator/) (`192.168.1.100:23`) | Using the scale over a network connection |
| Cables routed through a [TCP device server](https://moxa.com/en/products/industrial-edge-connectivity/serial-device-servers/general-device-servers/nport-5100a-series) (`192.168.1.100:23`). | Using the scale over a network connection |

Installation
============

```
git clone https://github.com/treychaffin/arlyn.git
cd alicat/
python setup.py install
```

Python Usage
============

## Getting the weight string

This `.print_weight` method inputs the `~*P*~` serial command (shown in the [Arlyn UpScale Touchscreen User Manual](https://www.arlynscales.com/arlyn-upscale-touchscreen-indicator-user-manual/))

### Example Usage

```python
from arlyn import Scale

arlyn_address = 'ip-address:port'

async def get_weight_string(scale_address):
    '''
    Retrieve the weight string from the scale 

    Args:
        scale_address: The serial or TCP address of the scale (string)

    Returns:
        The weight string from the scale (string)
        ex: '03/31/2024 17:28:08, 0.00 kg'
    '''
    async with Scale(scale_address) as scale:
        return await scale.print_weight()

print(await get_weight_string(arlyn_address))
```
The method and the function shown will return a string showing the date, time, weight, and unit from the scale

```python
'03/31/2024 17:28:08, 0.00 kg'
```

## Toggle Unit

This `.toggle_unit` method inputs the `~*U*~` serial command (shown in the [Arlyn UpScale Touchscreen User Manual](https://www.arlynscales.com/arlyn-upscale-touchscreen-indicator-user-manual/))

The order in which the scale toggles: `kg -> g -> oz -> lb ->`

### Example Usage

```python
from arlyn import Scale

arlyn_address = 'COM6'

async def toggle_unit(scale_address):
    '''
    Toggles the unit change command
    kg -> g -> oz -> lb ->

    Args:
        scale_address: The serial or TCP address of the scale (string)

    Returns:
        nothing
    '''
    async with Scale(scale_address) as scale:
        await scale.toggle_unit()

await toggle_unit(arlyn_address)
```

This method and function shown returns nothing

## Zero Scale

This `.zero_scale` method inputs the `~*Z*~` serial command (shown in the [Arlyn UpScale Touchscreen User Manual](https://www.arlynscales.com/arlyn-upscale-touchscreen-indicator-user-manual/))

### Example Usage

```python
from arlyn import Scale

arlyn_address = 'ip-address:port'

async def zero_scale(scale_address):
    '''
    Sets the current weight on the scale to zero

    Args:
        scale_address: The serial or TCP address of the scale (string)

    Returns:
        nothing
    '''
    async with Scale(scale_address) as scale:
        await scale.zero_scale()

await zero_scale(arlyn_address)
```

This method and function shown returns nothing

## JSON String

This `.get_json` method inputs the `~*W*~` serial command (shown in the [Arlyn UpScale Touchscreen User Manual](https://www.arlynscales.com/arlyn-upscale-touchscreen-indicator-user-manual/))

### Example Usage

```python
from arlyn import Scale

arlyn_address = 'COM6'

async def get_json(scale_address):
    '''
    Retrieve a JSON string of the scales current status

    Args:
        scale_address: The serial or TCP address of the scale (string)

    Returns:
        JSON string of current scale status
        ex: '{"bSIndi":true,"sNet":"","sUnit":"kg","sWeight":"0.00","_CMD_ACK":"ACK","_id":1,"_name":"*W","_rSNo":42,"_sSNo":18}'
    '''
    async with Scale(scale_address) as scale:
        return await scale.get_json()

print(await get_json(arlyn_address))
```

This method and function shown will return a JSON string

```python
'{"bSIndi":true,"sNet":"","sUnit":"kg","sWeight":"0.00","_CMD_ACK":"ACK","_id":1,"_name":"*W","_rSNo":42,"_sSNo":18}'
```

## Get weight dictionary

This example function shown will use the `get_weight_string(scale_address)` function shown earlier to retrieve the weight string and use regex to organize the data into a dictionary.

```python
from arlyn import Scale
import re

arlyn_address = 'ip-address:port'

async def get_weight_dict(scale_address):
    '''
    Retrieve the weight string from the scale, then extracts the information into a dictionary
    Converts weight value into a float

    Args:
        scale_address: The serial or TCP address of the scale (string)

    Returns:
        The weight string from the scale (dict)
        ex: {'date': '03/31/2024', 'time': '17:35:55', 'weight': 0.0, 'unit': 'kg'}
    '''
    weight_string = await get_weight_string(scale_address)
    date = re.search(r"\d{2}/\d{2}/\d{4}",weight_string).group()
    time = re.search(r"\d{2}:\d{2}:\d{2}",weight_string).group()
    weight = re.search(r", .* ",weight_string).group()[2:-1]
    unit = re.search(r"[a-zA-Z]{1,2}",weight_string).group()
    return {"date":date,"time":time,"weight":float(weight),"unit":unit}

print(await get_weight_dict(arlyn_address))
```

Output:

```python
{'date': '03/31/2024', 'time': '17:35:55', 'weight': 0.0, 'unit': 'kg'}
```

## Change to specified unit

This example function uses the `toggle_unit(scale_address)` function shown earlier to set the scale to a desired unit.

```python
from arlyn import Scale

arlyn_address = 'COM6'

async def change_unit(scale_address, desired_unit):
    '''
    Toggles through units until scale is set to desired unit
    kg -> g -> oz -> lb ->

    Args:
        scale_address: The serial or TCP address of the scale (string)
        desired_unit: The unit to change the scale to (string)

    Returns:
        nothing
    '''
    units = ('kg','g','oz','lb')
    assert desired_unit in units, (
    "desired unit must be one of the following: kg, g, oz, lb")

    unit = await get_weight_dict(scale_address)
    unit = unit['unit']

    if desired_unit != unit:
        toggle_count = units.index(desired_unit) - units.index(unit) + len(units)
        for i in range(toggle_count):
            await toggle_unit(scale_address)
        unit = await get_weight_dict(scale_address)
        unit = unit['unit']
        print(f"unit set to: {unit}")
    else:
        print(f"unit was already set to: {unit}")

await change_unit(arlyn_address,'g')
```