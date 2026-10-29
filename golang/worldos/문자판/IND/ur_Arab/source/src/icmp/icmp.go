/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "حافظہ"
import . "etherframe"
import . "ipv4"
import . "util"

var icmp콘솔 = T콘솔{}

type TInternetControlMessageProtocolMessageBuffer struct {
	Type	byte
	code		byte

	checksum	[2]byte
	data		[4]byte
}

var icmpSize int = 64

type TInternetControlMessageProtocolMessage struct {
	Type	uint8
	code		uint8

	checksum	uint16
	data		uint32
}

func (self *TInternetControlMessageProtocolMessage) Vآغاز_کرنا(buffer TInternetControlMessageProtocolMessageBuffer) {
	self.Type = buffer.Type
	self.code = buffer.code

	self.checksum = Uint16_R(ArrayToUint16(buffer.checksum))
	self.data = Uint32_R(ArrayToUint32(buffer.data))
}

func (self *TInternetControlMessageProtocolMessage) SetBuffer(buffer *TInternetControlMessageProtocolMessageBuffer) {
	buffer.Type = self.Type
	buffer.code = self.code

	buffer.checksum = Uint16ToArray(self.checksum)
	buffer.data = Uint32ToArray(self.data)
}

type TICMPHandler struct {
	TInternetProtocolHandler
}

var icmp *TInternetControlMessageProtocol

func (self *TICMPHandler) OnInternetProtocolReceived(srcIP_BE uint32, dstIP_BE uint32, dataPointer uintptr, حجم uint32) bool {
	return icmp.OnInternetProtocolReceived(srcIP_BE, dstIP_BE, dataPointer, حجم)
}

var ipHandler IInternetProtocolHandler

type TInternetControlMessageProtocol struct {
}

func (self *TInternetControlMessageProtocol) Vآغاز_کرنا(backend TInternetProtocolProvider, handler IInternetProtocolHandler) {
	ipHandler = handler
	ipHandler.Vآغاز_کرنا(backend, handler, 0x01)
	icmp = self
}
func (self *TInternetControlMessageProtocol) OnInternetProtocolReceived(srcIP_BE uint32, dstIP_BE uint32, dataPointer uintptr, حجم uint32) bool {
	if حجم < uint32(icmpSize) {
		return false
	}

	var buffer *TInternetControlMessageProtocolMessageBuffer = (*TInternetControlMessageProtocolMessageBuffer)(Pointer(dataPointer))
	var msg TInternetControlMessageProtocolMessage = TInternetControlMessageProtocolMessage{}
	msg.Vآغاز_کرنا(*buffer)

	icmp콘솔.M출력(([]byte)("icmp:OnInternet"))
	icmp콘솔.MUint16출력(uint16(msg.Type))
	icmp콘솔.M출력(([]byte)(":"))

	switch msg.Type {
	case 0:
		icmp콘솔.M출력(([]byte)("ping response from "))
		break

	case 8:
		icmp콘솔.M출력(([]byte)("ping send "))
		msg.Type = 0

		msg.checksum = 0
		msg.SetBuffer(buffer)
		msg.checksum = ipHandler.GetProvider().Checksum((*([4096]uint16))(Pointer(dataPointer)), uint32(icmpSize))

		msg.SetBuffer(buffer)

		return true
		break
	}
	return false
}

func (self *TInternetControlMessageProtocol) SendEchoRequest(ip_be uint32) bool {
	var icmp TInternetControlMessageProtocolMessage = TInternetControlMessageProtocolMessage{}

	var memoryManager = &TMemoryManager{}
	var buffer = (*TInternetControlMessageProtocolMessageBuffer)(memoryManager.Vحافظہ_مختص_کرنا(1024))

	icmp.Type = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.SetBuffer(buffer)
	icmp.checksum = ipHandler.GetProvider().Checksum((*([4096]uint16))(Pointer(&buffer)), uint32(icmpSize))
	icmp.SetBuffer(buffer)

	var dataPointer uintptr = uintptr(Pointer(buffer))
	ipHandler.Send(ip_be, 0x01, dataPointer, uint32(icmpSize))

	return false

}
