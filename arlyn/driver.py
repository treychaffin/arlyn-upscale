from __future__ import annotations

import asyncio
from typing import Any, ClassVar
from .util import Client, SerialClient, TcpClient, _is_float

class Scale:
    def __init__(self, address: str = 'COM12', **kwargs: Any) -> None:
        if address.startswith('/dev') or address.startswith('COM'): #serial
            self.hw: Client = SerialClient(address=address, **kwargs)
        else: #TCP 
            self.hw = TcpClient(address=address, **kwargs)
        self.keys = ['mass']
        self.open = True

    async def __aenter__(self, *args: Any) -> Scale:
        """Provide async enter to context manager."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Provide async exit to context manager."""
        await self.close()
        return
    
    @classmethod
    async def is_connected(cls, port: str, unit: str = 'A') -> bool:
        """Return True if the specified port is connected to this device.

        This class can be used to automatically identify ports with connected
        Scales. Iterate through all connected interfaces, and use this to
        test. Ports that come back True should be valid addresses.

        """
        is_device = False
        try:
            device = cls(port, unit)
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
        """Wrap the communicator request, to call _test_scale_open() before any request."""
        self._test_scale_open()
        return await self.hw._write_and_read(command)
    
    async def _write_command(self, command: str) -> str | None:
        """Wrap the communicator request, to call _test_scale_open() before any request."""
        self._test_scale_open()
        return await self.hw._write_and_read(command)
    
    async def print_weight(self) -> dict:
        """

        """
        command = '~*P*~'
        line = await self._write_and_read(command)
        if not line:
            raise OSError("Could not read values")
        return line
    
    async def get_json(self) -> dict:
        """

        """
        command = '~*W*~'
        line = await self._write_and_read(command)
        if not line:
            raise OSError("Could not read values")
        return line
    
    async def toggle_unit(self) -> dict:
        """

        """
        command = '~*U*~'
        await self._write_command(command)

    async def zero_scale(self) -> dict:
        """

        """
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