/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amd_am79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "port"
import . "pci"

var 넷카드콘솔 T콘솔 = T콘솔{}

type TInitializationBlock struct {
	mode			uint16
	numSendBuffers	uint8
	numRecvBuffers	uint8

	physicalAddress	uint64

	logicalAddress			uint64
	recvBufferDescrAddress	uintptr
	sendBufferDescrAddress	uintptr
}
type TBufferDescriptor struct {
	address	uint32
	flags		uint32
	flags2		uint32
	avail	uint32
}

type IRawDataHandler interface {
	OnRawDataReceived(dataPointer uintptr, വലുപ്പം int) bool
	Send(dataPointer uintptr, വലുപ്പം uint32)
}

var rawDataBackend Tamd_am79c973

type TRawDataHandler struct {
}

func (self *TRawDataHandler) SetBackend(backend Tamd_am79c973) {

	rawDataBackend = backend
}
func (self *TRawDataHandler) GetBackend() Tamd_am79c973 {
	return rawDataBackend
}
func (self *TRawDataHandler) OnRawDataReceived(dataPointer uintptr, വലുപ്പം int) bool {
	넷카드콘솔.M출력XY(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawDataHandler) Send(dataPointer uintptr, വലുപ്പം uint32) {
	넷카드콘솔.M출력XY(([]byte)("TRawDataSend"), 10, 10)
	rawDataBackend.Send(dataPointer, വലുപ്പം)
}

var MACAddress0Port uint16
var MACAddress2Port uint16
var MACAddress4Port uint16
var registerDataPort uint16
var registerAddressPort uint16
var resetPort uint16
var busControlRegisterDataPort uint16

var initBlock TInitializationBlock

var sendBufferDescr [8]TBufferDescriptor
var sendBuffersDescrMemory [2048 + 15]byte
var sendBuffers [2*1024 + 15][8]uint8
var currentSendBuffer uint8

var recvBufferDescr [8]TBufferDescriptor
var recvBuffersDescrMemory [2048 + 15]uint8
var recvBuffers [2*1024 + 15][8]uint8
var currentRecvBuffer uint8
var func_value func(*Tamd_am79c973, uint32) uint32

type Tamd_am79c973 struct {
	TInterruptHandler
	deviceDescriptor	TPeripheralComponentInterconnectDeviceDescriptor
	interrupt	*TInterruptManager
	handler		*TRawDataHandler
}

var 콘솔 T콘솔 = T콘솔{}
var iRawDataHandler IRawDataHandler

func (self *Tamd_am79c973) InitDriver(interrupt *TInterruptManager, deviceDescriptor TPeripheralComponentInterconnectDeviceDescriptor, handler IRawDataHandler) {

	self.deviceDescriptor = deviceDescriptor

	func_value = (*Tamd_am79c973).HandleInterrupt
	var addr uintptr
	addr = uintptr(Pointer(&func_value))

	self.Vആരംഭിക്കുക(uint8(0x20+deviceDescriptor.Interrupt), uintptr(Pointer(interrupt)), addr)

	MACAddress0Port = uint16(deviceDescriptor.PortBase)
	MACAddress2Port = uint16(deviceDescriptor.PortBase) + 0x02
	MACAddress4Port = uint16(deviceDescriptor.PortBase) + 0x04
	registerDataPort = uint16(deviceDescriptor.PortBase) + 0x10
	registerAddressPort = uint16(deviceDescriptor.PortBase) + 0x12
	resetPort = uint16(deviceDescriptor.PortBase) + 0x14
	busControlRegisterDataPort = uint16(deviceDescriptor.PortBase) + 0x16

	iRawDataHandler = &TRawDataHandler{}
	if handler != nil {
		iRawDataHandler = handler
	}

	currentSendBuffer = 0
	currentRecvBuffer = 0

	var MAC0 uint64 = uint64(PortReadWord(MACAddress0Port) % 256)
	var MAC1 uint64 = uint64(PortReadWord(MACAddress0Port) / 256)
	var MAC2 uint64 = uint64(PortReadWord(MACAddress2Port) % 256)
	var MAC3 uint64 = uint64(PortReadWord(MACAddress2Port) / 256)
	var MAC4 uint64 = uint64(PortReadWord(MACAddress4Port) % 256)
	var MAC5 uint64 = uint64(PortReadWord(MACAddress4Port) / 256)

	var MAC uint64 = (MAC5 << 40) | (MAC4 << 32) | (MAC3 << 24) | (MAC2 << 16) | (MAC1 << 8) | MAC0

	var macAddr uint64 = (MAC0 << 40) | (MAC1 << 32) | (MAC2 << 24) | (MAC3 << 16) | (MAC4 << 8) | MAC5

	콘솔.M출력XY(([]byte)("[interrupt num : "), 0, 13)
	콘솔.MHex출력(uint8(deviceDescriptor.Interrupt))
	콘솔.M출력(([]byte)("]"))
	콘솔.M출력(([]byte)("[mac address : "))
	콘솔.MUint16출력(uint16(macAddr >> 32))
	콘솔.MUint32출력(uint32(macAddr & 0x00000000FFFFFFFF))
	콘솔.M출력(([]byte)("]"))

	PortWriteWord(registerAddressPort, 20)
	PortWriteWord(busControlRegisterDataPort, 0x102)

	PortWriteWord(registerAddressPort, 0)
	PortWriteWord(registerDataPort, 0x04)

	initBlock.mode = 0x0000
	initBlock.numSendBuffers = 3
	initBlock.numRecvBuffers = 3

	initBlock.physicalAddress = MAC

	initBlock.logicalAddress = 0

	sendBufferDescr = *(*([8]TBufferDescriptor))(Pointer((uintptr((Pointer)(&sendBuffersDescrMemory)) + 15) & ^(uintptr)(0xF)))
	initBlock.sendBufferDescrAddress = uintptr(Pointer(&sendBufferDescr))
	recvBufferDescr = *(*([8]TBufferDescriptor))(Pointer((uintptr((Pointer)(&recvBuffersDescrMemory)) + 15) & ^(uintptr)(0xF)))
	initBlock.recvBufferDescrAddress = uintptr(Pointer(&recvBufferDescr))

	for i := 0; i < 8; i++ {
		sendBufferDescr[i].address = uint32((uintptr(Pointer(&sendBuffers[i])) + 15) & ^(uintptr(0xF)))
		sendBufferDescr[i].flags = 0x7FF | 0xF000
		sendBufferDescr[i].flags2 = 0
		sendBufferDescr[i].avail = 0

		recvBufferDescr[i].address = uint32((uintptr(Pointer(&recvBuffers[i])) + 15) & ^(uintptr(0xF)))
		recvBufferDescr[i].flags = 0xF7FF | 0x80000000

	}

	PortWriteWord(registerAddressPort, 1)
	PortWriteWord(registerDataPort, uint16(uintptr(Pointer(&initBlock))&0xFFFF))

	PortWriteWord(registerAddressPort, 2)
	PortWriteWord(registerDataPort, uint16((uintptr(Pointer(&initBlock))>>16)&0xFFFF))

}
func (self *Tamd_am79c973) Activate() {
	PortWriteWord(registerAddressPort, 0)
	PortWriteWord(registerDataPort, 0x41)

	PortWriteWord(registerAddressPort, 4)
	temp := PortReadWord(registerDataPort)
	PortWriteWord(registerAddressPort, 4)
	PortWriteWord(registerDataPort, temp|0xC00)

	PortWriteWord(registerAddressPort, 0)
	PortWriteWord(registerDataPort, 0x42)

}
func (self *Tamd_am79c973) Reset() int {
	PortReadWord(resetPort)
	PortWriteWord(resetPort, 0)
	return 10
}

var count uint16 = 0

func (self *Tamd_am79c973) HandleInterrupt(esp uint32) uint32 {

	PortWriteWord(registerAddressPort, 0)
	temp := uint32(PortReadWord(registerDataPort))
	콘솔.M출력(([]byte)("interrupt("))
	콘솔.MUint32출력(esp)
	콘솔.M출력(([]byte)(":"))
	콘솔.MUint32출력(temp)
	콘솔.M출력(([]byte)(":"))
	콘솔.MUint16출력(count)
	count++
	콘솔.M출력(([]byte)(")"))

	if (temp & 0x8000) == 0x8000 {
		콘솔.M출력(([]byte)("am79c973 error"))
	}
	if (temp & 0x2000) == 0x2000 {
		콘솔.M출력(([]byte)("am79c973 collision error"))
	}
	if (temp & 0x1000) == 0x1000 {
		콘솔.M출력(([]byte)("am79c973 missed frame"))
	}
	if (temp & 0x0800) == 0x0800 {
		콘솔.M출력(([]byte)("am79c973 memory error"))
	}
	if (temp & 0x0400) == 0x0400 {
		콘솔.M출력(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temp & 0x0200) == 0x0200 {
		콘솔.M출력(([]byte)("am79c973 data sent"))
	}

	PortWriteWord(registerAddressPort, 0)
	PortWriteWord(registerDataPort, uint16(temp))

	if (temp & 0x0100) == 0x0100 {
		콘솔.M출력(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamd_am79c973) Send(dataPointer uintptr, വലുപ്പം uint32) {
	var sendDescriptor uint16 = uint16(currentSendBuffer)
	currentSendBuffer = 0

	if വലുപ്പം > 1518 {
		വലുപ്പം = 1518
	}

	var src [4096]byte = *(*([4096]byte))(Pointer(dataPointer))
	var dst uint32 = sendBufferDescr[sendDescriptor].address + വലുപ്പം - 1

	for i := 0; i < int(വലുപ്പം); i++ {

		*(*byte)(Pointer(uintptr(dst))) = src[int(വലുപ്പം)-i-1]

		dst--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataPointer))
	콘솔.M출력XY(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		콘솔.MHex출력(data[i])
		콘솔.M출력(([]byte)(":"))
	}
	콘솔.M출력(([]byte)("\n"))

	sendBufferDescr[sendDescriptor].avail = 0
	sendBufferDescr[sendDescriptor].flags2 = 0
	sendBufferDescr[sendDescriptor].flags = 0x8300F000 | uint32((-വലുപ്പം)&0xFFF)

	PortWriteWord(registerAddressPort, 0)
	PortWriteWord(registerDataPort, 0x48)

}
func (self *Tamd_am79c973) Receive() {
	콘솔.M출력(([]byte)(":"))
	콘솔.MUint32출력(uint32(uintptr(Pointer(&sendBuffers))))
	콘솔.M출력(([]byte)(":"))
	콘솔.MHex출력(sendBuffers[0][0])
	콘솔.MHex출력(sendBuffers[0][1])
	콘솔.M출력(([]byte)(":"))
	currentRecvBuffer = 0

	for ; (recvBufferDescr[currentRecvBuffer].flags & 0x80000000) == 0; currentRecvBuffer = (currentRecvBuffer + 1) % 8 {

		if !(recvBufferDescr[currentRecvBuffer].flags&0x40000000 != 0) && ((recvBufferDescr[currentRecvBuffer].flags & 0x03000000) == 0x03000000) {
			var വലുപ്പം uint32 = recvBufferDescr[currentRecvBuffer].flags & 0xFFF
			if വലുപ്പം > 64 {
				വലുപ്പം -= 4
			}

			콘솔.M출력([]byte(" size : ["))
			콘솔.MUint32출력(വലുപ്പം)
			콘솔.M출력([]byte("]"))

			var buffer [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvBufferDescr[currentRecvBuffer].address)))
			var വിലാസ_സൂചിക uintptr = uintptr(Pointer(&buffer))
			if iRawDataHandler != nil {
				if iRawDataHandler.OnRawDataReceived(വിലാസ_സൂചിക, int(വലുപ്പം)) {

					콘솔.M출력XY(([]byte)("self.Send"), 0, 22)

					self.Send(വിലാസ_സൂചിക, വലുപ്പം)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				콘솔.MHex출력(buffer[i])
				콘솔.M출력([]byte(":"))
			}

		}
		recvBufferDescr[currentRecvBuffer].flags2 = 0
		recvBufferDescr[currentRecvBuffer].flags = 0x8000F7FF
	}
}
func (self *Tamd_am79c973) SetHandler(handler *TRawDataHandler) {
	self.handler = handler
}
func (self *Tamd_am79c973) GetMACAddress() uint64 {

	return initBlock.physicalAddress
}
func (self *Tamd_am79c973) SetIPAddress(ip uint64) {
	initBlock.logicalAddress = ip
}
func (self *Tamd_am79c973) GetIPAddress() uint64 {
	return initBlock.logicalAddress
}
