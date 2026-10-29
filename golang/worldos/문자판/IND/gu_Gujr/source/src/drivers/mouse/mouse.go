/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package keyboard

import . "unsafe"

import . "port"
import . "interrupt"
import . "console"

type IMouseEventHandler interface {
	OnMouseDown(button int8)
	OnMouseUp(button int8)
	OnMouseMove(x int8, y int8)
}

var iMouseEventHandler IMouseEventHandler

type TDefaultMouseEventHandler struct {
}

var 콘솔 T콘솔 = T콘솔{}
var prevX int16 = 0
var prevY int16 = 0
var xPos int16 = 0
var yPos int16 = 0

func (self TDefaultMouseEventHandler) OnMouseDown(button int8) {
	buf := []byte("+")
	콘솔.M출력XY(buf, uint16(prevX), uint16(prevY))
}
func (self TDefaultMouseEventHandler) OnMouseUp(button int8)	{}
func (self TDefaultMouseEventHandler) OnMouseMove(x int8, y int8) {

	xPos += int16(x)
	if xPos < 0 {
		xPos = 0
	}
	if xPos >= 80 {
		xPos = 79
	}

	yPos -= int16(y)

	if yPos < 0 {
		yPos = 0
	}
	if yPos >= 25 {
		yPos = 24
	}

	buf := []byte(" ")
	콘솔.M출력XY(buf, uint16(prevX), uint16(prevY))

	buf = []byte("0")
	콘솔.M출력XY(buf, uint16(xPos), uint16(yPos))

	prevX = xPos
	prevY = yPos
}

type TMouseDriver struct {
	TInterruptHandler
}

var activeMouseDriver *TMouseDriver
var interruptHandler func(uint32) uint32

var dataport uint16 = 0x60
var commandport uint16 = 0x64

const ps2WaitLimit = 100000

func waitPS2InputEmpty() bool {
	for i := 0; i < ps2WaitLimit; i++ {
		if (PortReadByte(commandport) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitPS2OutputFull() bool {
	for i := 0; i < ps2WaitLimit; i++ {
		if (PortReadByte(commandport) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func writePS2Command(value uint8) bool {
	if !waitPS2InputEmpty() {
		return false
	}
	PortWriteByte(commandport, value)
	return true
}

func writePS2Data(value uint8) bool {
	if !waitPS2InputEmpty() {
		return false
	}
	PortWriteByte(dataport, value)
	return true
}

func readPS2Data() (uint8, bool) {
	if !waitPS2OutputFull() {
		return 0, false
	}
	return PortReadByte(dataport), true
}

func sendMouseCommand(value uint8) bool {
	if !writePS2Command(0xD4) || !writePS2Data(value) {
		return false
	}
	ack, ok := readPS2Data()
	return ok && ack == 0xFA
}

func (self *TMouseDriver) InitDriver(manager *TInterruptManager, mouseEventHandler IMouseEventHandler) {

	iMouseEventHandler = TDefaultMouseEventHandler{}

	if mouseEventHandler != nil {
		iMouseEventHandler = mouseEventHandler
	}

	activeMouseDriver = self
	interruptHandler = handleMouseInterrupt
	var addr uintptr
	addr = uintptr(Pointer(&interruptHandler))
	self.Vઆરંભ_કરવો(0x2C, uintptr(Pointer(manager)), addr)

	for i := 0; i < 32 && (PortReadByte(commandport)&0x01) != 0; i++ {
		PortReadByte(dataport)
	}

	if !writePS2Command(0xA8) || !writePS2Command(0x20) {
		return
	}
	status, ok := readPS2Data()
	if !ok {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !writePS2Command(0x60) || !writePS2Data(status) {
		return
	}

	if !sendMouseCommand(0xF6) || !sendMouseCommand(0xF4) {
		return
	}
	offset = 0

}

func handleMouseInterrupt(esp uint32) uint32 {
	if activeMouseDriver == nil {
		PortReadByte(dataport)
		return esp
	}
	return activeMouseDriver.HandleInterrupt(esp)
}

var count uint8 = 0
var buffer [3]int8
var offset uint8 = 0

var buttons int8
var pendingX int16
var pendingY int16
var pendingButtons int8
var pendingMouseEvent bool

func (self *TMouseDriver) HandleInterrupt(esp uint32) uint32 {
	status := PortReadByte(commandport)
	if (status&0x01) == 0 || (status&0x20) == 0 {
		return esp
	}

	data := PortReadByte(dataport)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetStatus := uint8(buffer[0])

		if (packetStatus & 0xC0) == 0 {
			pendingX += int16(buffer[1])
			pendingY += int16(buffer[2])
			if pendingX > 127 {
				pendingX = 127
			} else if pendingX < -127 {
				pendingX = -127
			}
			if pendingY > 127 {
				pendingY = 127
			} else if pendingY < -127 {
				pendingY = -127
			}
		}
		pendingButtons = int8(packetStatus & 0x07)
		pendingMouseEvent = true
	}

	return esp

}

func ProcessPendingMouseEvents() {
	if iMouseEventHandler == nil {
		return
	}

	InterruptDeactive()
	if !pendingMouseEvent {
		InterruptActive()
		return
	}
	x := int8(pendingX)
	y := int8(pendingY)
	newButtons := pendingButtons
	oldButtons := buttons

	pendingX = 0
	pendingY = 0
	pendingMouseEvent = false
	InterruptActive()

	if x != 0 || y != 0 {
		iMouseEventHandler.OnMouseMove(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (newButtons & mask) != (oldButtons & mask) {
			if (newButtons & mask) != 0 {
				iMouseEventHandler.OnMouseDown(int8(i + 1))
			} else {
				iMouseEventHandler.OnMouseUp(int8(i + 1))
			}
		}
	}
	buttons = newButtons
}
