# zeropong
# by winkleink - 2016



Raspberry Pi game where you throw ping pong balls into cups for points

Game board is made from plastic cups with an LDR in each but to detect when the ball passes.
As the Raspberry Pi does not have analog in an MCP3008 is used to provide analog input from the LDRs over SPI.
Using GPIOZero to read the MCP3008

Pygame used for the screen, keyboard input and sound.

