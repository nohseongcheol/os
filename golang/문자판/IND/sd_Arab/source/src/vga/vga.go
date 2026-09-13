package vga

import . "unsafe"
import . "port"

type TVideoGraphicsArray struct {
}

var micsPort uint16 = 0x3c2
var crtcIndexPort uint16 = 0x3d4
var crtcDataPort uint16 = 0x3d5
var sequencerIndexPort uint16 = 0x3c4
var sequencerDataPort uint16 = 0x3c5
var graphicsControllerIndexPort uint16 = 0x3ce
var graphicsControllerDataPort uint16 = 0x3cf
var attributeControllerIndexPort uint16 = 0x3c0
var attributeControllerReadPort uint16 = 0x3c1
var attributeControllerWritePort uint16 = 0x3c0
var attributeControllerResetPort uint16 = 0x3da

func (self *TVideoGraphicsArray) WriteRegisters(registers []byte) {
	var regIndex uint16 = 0

	PortWriteByte(micsPort, registers[regIndex])
	regIndex++

	var i uint8
	for i = 0; i < 5; i++ {
		PortWriteByte(sequencerIndexPort, i)
		PortWriteByte(sequencerDataPort, registers[regIndex])
		regIndex++
	}

	PortWriteByte(crtcIndexPort, 0x03)

	PortWriteByte(crtcDataPort, (PortReadByte(crtcDataPort) | 0x80))
	PortWriteByte(crtcIndexPort, 0x11)
	PortWriteByte(crtcDataPort, (PortReadByte(crtcDataPort) & ^uint8(0x80)))

	registers[0x03] = registers[0x03] | 0x80
	registers[0x11] = registers[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		PortWriteByte(crtcIndexPort, i)
		PortWriteByte(crtcDataPort, registers[regIndex])
		regIndex++
	}

	for i = 0; i < 9; i++ {
		PortWriteByte(graphicsControllerIndexPort, i)
		PortWriteByte(graphicsControllerDataPort, registers[regIndex])
		regIndex++
	}

	for i = 0; i < 21; i++ {
		PortReadByte(attributeControllerResetPort)
		PortWriteByte(attributeControllerIndexPort, i)
		PortWriteByte(attributeControllerWritePort, registers[regIndex])
		regIndex++
	}

	PortReadByte(attributeControllerResetPort)
	PortWriteByte(attributeControllerIndexPort, 0x20)

}

func (self *TVideoGraphicsArray) GetFrameBufferSegment() uintptr {
	PortWriteByte(graphicsControllerIndexPort, 0x06)
	var segmentNumber uint8 = ((PortReadByte(graphicsControllerDataPort) >> 2) & 0x03)
	switch segmentNumber {
	case 0:
		return uintptr(0x00000)
	case 1:
		return uintptr(0xa0000)
	case 2:
		return uintptr(0xb0000)
	case 3:
		return uintptr(0xb8000)
	}

	return uintptr(0xB0000)
}
func (self *TVideoGraphicsArray) PutPixel(x uint32, y uint32, colorIndex uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixelAddress uintptr = self.GetFrameBufferSegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixelAddress)) = colorIndex

}
func (self *TVideoGraphicsArray) GetColorIndex(r uint8, g uint8, b uint8) uint8 {
	if r == 0x00 && g == 0x00 && b == 0x00 {
		return 0x00
	}
	if r == 0x00 && g == 0x00 && b == 0xA8 {
		return 0x01
	}
	if r == 0x00 && g == 0xA8 && b == 0x00 {
		return 0x02
	}
	if r == 0xA8 && g == 0x00 && b == 0x00 {
		return 0x04
	}
	if r == 0xFF && g == 0xFF && b == 0xFF {
		return 0x3F
	}

	return 0x01
}
func (self *TVideoGraphicsArray) PutPixelRGB(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.PutPixel(x, y, self.GetColorIndex(r, g, b))
}
func (self *TVideoGraphicsArray) FillRectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.PutPixelRGB(X, Y, r, g, b)
		}
	}
}
func (self *TVideoGraphicsArray) SupportMode(width uint32, height uint32, colordepth uint32) bool {
	return width == 320 && height == 200 && colordepth == 8
}
func (self *TVideoGraphicsArray) SetMode(width uint32, height uint32, colordepth uint32) bool {
	if !self.SupportMode(width, height, colordepth) {
		return false
	}

	var g_320x200x256 = []byte{

		0x63,

		0x03, 0x01, 0x0F, 0x00, 0x0E,

		0x5F, 0x4F, 0x50, 0x82, 0x54, 0x80, 0xBF, 0x1F,
		0x00, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x9C, 0x0E, 0x8F, 0x28, 0x40, 0x96, 0xB9, 0xA3,
		0xFF,

		0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x05, 0x0F,
		0xFF,

		0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
		0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
		0x41, 0x00, 0x0F, 0x00, 0x00}

	self.WriteRegisters(g_320x200x256)

	return true
}
