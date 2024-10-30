from __future__ import annotations
import json
import re
from typing import Any
from .util import Client, SerialClient, TcpClient

class Scale:
    def __init__(self, address: str = 'COM12', **kwargs: Any) -> None:
        if address.startswith('/dev') or address.startswith('COM'): #serial
            self.hw: Client = SerialClient(address=address, **kwargs)
        else: #TCP 
            self.hw = TcpClient(address=address, **kwargs)
        self.open = True
        self.units = ('kg','g','oz','lb')

    async def __aenter__(self, *args: Any) -> Scale:
        """Provide async enter to context manager."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Provide async exit to context manager."""
        await self.close()
        return
    
    @classmethod
    async def is_connected(cls, port: str) -> bool:
        """Return True if the specified port is connected to this device.

        This class can be used to automatically identify ports with connected
        Scales. Iterate through all connected interfaces, and use this to
        test. Ports that come back True should be valid addresses.

        """
        is_device = False
        try:
            device = cls(port)
            try:
                c = await device.get()
                if cls.__name__ == 'Scale':
                    assert c
                else:
                    raise NotImplementedError('Must be Scale')
                is_device = True
            finally:
                await device.close()
        except Exception:
            pass
        return is_device
    
    def _test_scale_open(self) -> None:
        """Raise an IOError if the Scale has been closed.

        Does nothing if the scale is open and good for read/write
        otherwise raises an IOError. This only checks if the meter
        has been closed by the Scale.close method.
        """
        if not self.open:
            raise OSError(f"The scale with port {self.hw.address} is not open")
        
    async def _write_and_read(self, command: str) -> str | None:
        """Wrap the communicator request, to call _test_scale_open() 
        before any request."""
        self._test_scale_open()
        return await self.hw._write_and_read(command)
    
    async def _write_command(self, command: str) -> str | None:
        """Wrap the communicator request, to call _test_scale_open() 
        before any request."""
        self._test_scale_open()
        return await self.hw._write_and_read(command)
    
    async def get_weight_string(self) -> str:
        """print the weight string"""
        command = '~*P*~'
        line = await self._write_and_read(command)
        if not line: raise OSError("Could not read values")
        return line
    
    async def get_json_dict(self) -> dict:
        """retrieve JSON string string from the scale"""
        command = '~*W*~'
        line = await self._write_and_read(command)
        if not line: raise OSError("Could not read values")
        return json.loads(line)
    
    async def get_json_string(self) -> str:
        """retrieve JSON string string from the scale"""
        command = '~*W*~'
        line = await self._write_and_read(command)
        if not line: raise OSError("Could not read values")
        return line
    
    async def get_unit(self) -> str:
        """return the current unit"""
        json_dict = await self.get_json_dict()
        current_unit = json_dict['sUnit']
        return current_unit
            
    async def toggle_unit(self) -> None:
        """toggle the unit"""
        command = '~*U*~'
        await self._write_command(command)
        await self.get_unit()

    async def change_unit(self, desired_unit: str) -> None:
        """toggles through units until scale is set to desired unit"""

        if desired_unit not in self.units:
            raise ValueError("desired unit must be one of the following: kg, g, oz, lb")
        
        unit = (await self.get_json_dict())["sUnit"]

        if desired_unit != unit:
            toggle_count = self.units.index(desired_unit) - self.units.index(unit) + len(self.units)
            for i in range(toggle_count):
                await self.toggle_unit()

    async def get_weight_dict(self) -> dict:
        '''
        Retrieve the weight string from the scale, then extracts the information into 
        a dictionary. Converts weight value into a float

        contains time and date, unlike get_json method
        '''
        weight_string = await self.get_weight_string()
        date = re.search(r"\d{2}/\d{2}/\d{4}",weight_string).group()
        time = re.search(r"\d{2}:\d{2}:\d{2}",weight_string).group()
        unit = re.search(r"kg|g|oz|lb",weight_string).group()
        netMode = True if re.search(r"net",weight_string) else False
        weight = re.search(r", -?\d+.\d+ |, -?\d+ ",weight_string).group()[2:-1]
    
        return {"date":date,"time":time,"weight":float(weight),"unit":unit, "netMode":netMode}
    
    async def zero_scale(self) -> None:
        """zero the scale"""
        command = '~*Z*~'
        await self._write_command(command)
    
    async def close(self) -> None:
        """Close the scale. Call this on program termination.

        Also closes the serial port if no other Scale object has
        a reference to the port.
        """
        if not self.open:
            return
        await self.hw.close()
        self.open = False