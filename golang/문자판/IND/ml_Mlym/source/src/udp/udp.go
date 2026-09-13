package udp

import . "unsafe"
import . "console"
import . "util"
import . "ഓർമ്മ"
import . "ipv4"

var udp콘솔 = T콘솔{}

type TUserDatagramProtocolHeaderBuffer struct {
	srcPort	[2]byte
	dstPort	[2]byte

	length		[2]byte
	checksum	[2]byte
}

var udpHeaderSize uint32 = 8

type TUserDatagramProtocolHeader struct {
	srcPort	uint16
	dstPort	uint16

	length		uint16
	checksum	uint16
}

func (self *TUserDatagramProtocolHeader) Vആരംഭിക്കുക(buffer *TUserDatagramProtocolHeaderBuffer) {
	self.srcPort = ArrayToUint16(buffer.srcPort)
	self.dstPort = ArrayToUint16(buffer.dstPort)

	self.length = ArrayToUint16(buffer.length)
	self.checksum = ArrayToUint16(buffer.checksum)
}
func (self *TUserDatagramProtocolHeader) SetBuffer(buffer *TUserDatagramProtocolHeaderBuffer) {

	buffer.srcPort = Uint16ToArray(self.srcPort)
	buffer.dstPort = Uint16ToArray(self.dstPort)

	buffer.length = Uint16ToArray(self.length)
	buffer.checksum = Uint16ToArray(self.checksum)

}

type IUserDatagramProtocolHandler interface {
	HandleUserDatagramProtocolMessage(socket *TUserDatagramProtocolSocket, data uintptr, വലുപ്പം uint16)
}

type TUserDatagramProtocolHandler struct {
}

func (self *TUserDatagramProtocolHandler) Vആരംഭിക്കുക(backend TInternetProtocolProvider) {
}
func (self *TUserDatagramProtocolHandler) HandleUserDatagramProtocolMessage(socket *TUserDatagramProtocolSocket, data uintptr, വലുപ്പം uint16) {
}

type IUserDatagramProtocolSocket interface {
	HandleUserDatagramProtocolMessage(data uintptr, വലുപ്പം uint16)
}
type TUserDatagramProtocolSocket struct {
	remotePort	uint16
	remoteIP		uint32
	localPort		uint16
	localIP			uint32

	listening	bool
}

var udpProvider TUserDatagramProtocolProvider
var udpHandler IUserDatagramProtocolHandler

func (self *TUserDatagramProtocolSocket) Test() {
}
func (self *TUserDatagramProtocolSocket) Vആരംഭിക്കുക(p_udpProvider TUserDatagramProtocolProvider, p_udpHandler IUserDatagramProtocolHandler) {
	udpProvider = p_udpProvider
	if udpHandler == nil && p_udpHandler != nil {
		udpHandler = p_udpHandler
	}
	self.listening = false
}
func (self *TUserDatagramProtocolSocket) HandleUserDatagramProtocolMessage(data uintptr, വലുപ്പം uint16) {
	if udpHandler != nil {
		udpHandler.HandleUserDatagramProtocolMessage(self, data, വലുപ്പം)
	}
}
func (self *TUserDatagramProtocolSocket) Send(p_data []byte, വലുപ്പം uint16) {
	var buffer [4096]byte
	for i := 0; i < int(വലുപ്പം); i++ {
		buffer[i] = p_data[i]
	}
	var data = uintptr(Pointer(&buffer))
	udpProvider.Send(self, data, വലുപ്പം)
}
func (self *TUserDatagramProtocolSocket) Disconnect() {
	udpProvider.Disconnect(self)
}

type TUserDatagramProtocolProvider struct {
}

var ipHandler IInternetProtocolHandler
var sockets [65535]TUserDatagramProtocolSocket
var numSockets int
var freePort uint16

func (self *TUserDatagramProtocolProvider) Vആരംഭിക്കുക(p_ipProvider TInternetProtocolProvider, p_ipHandler IInternetProtocolHandler) {
	ipHandler = p_ipHandler
	ipHandler.Vആരംഭിക്കുക(p_ipProvider, p_ipHandler, 0x11)
	numSockets = 0
	freePort = 1024
}
func (self *TUserDatagramProtocolProvider) OnInternetProtocolReceived(srcIP_BE uint32, dstIP_BE uint32, internetprotocolPayload uintptr, വലുപ്പം uint32) bool {
	if വലുപ്പം < udpHeaderSize {
		return false
	}

	var buffer *TUserDatagramProtocolHeaderBuffer = (*TUserDatagramProtocolHeaderBuffer)(Pointer(internetprotocolPayload))
	var msg TUserDatagramProtocolHeader
	msg.Vആരംഭിക്കുക(buffer)

	var socket *TUserDatagramProtocolSocket = nil

	for i := 0; i < numSockets && socket == nil; i++ {
		if sockets[i].localPort == msg.dstPort && sockets[i].localIP == dstIP_BE && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remotePort = msg.srcPort
			socket.remoteIP = srcIP_BE
		} else if sockets[i].localPort == msg.dstPort && sockets[i].localIP == dstIP_BE && sockets[i].remotePort == msg.srcPort && sockets[i].remoteIP == srcIP_BE {
			socket = &sockets[i]

		}
	}

	msg.SetBuffer(buffer)
	if socket != nil {
		socket.HandleUserDatagramProtocolMessage(internetprotocolPayload+uintptr(udpHeaderSize), uint16(വലുപ്പം-udpHeaderSize))
	}

	return false
}

func (self *TUserDatagramProtocolProvider) Connect(ip uint32, port uint16) *TUserDatagramProtocolSocket {
	var memoryManager = &TMemoryManager{}
	var socket = (*TUserDatagramProtocolSocket)(memoryManager.Vഓർമ്മസ്ഥലം_അനുവദിക്കുക(50))

	if socket != nil {

		socket.Vആരംഭിക്കുക(*self, nil)
		socket.remotePort = port
		socket.remoteIP = ip
		socket.localPort = freePort
		freePort++
		socket.localIP = uint32((*ipHandler.GetProvider()).GetIPAddress())

		socket.remotePort = Uint16_R(socket.remotePort)
		socket.localPort = Uint16_R(socket.localPort)

		sockets[numSockets] = *socket
		numSockets++

	}
	return socket

}
func (self *TUserDatagramProtocolProvider) Listen(port uint16) *TUserDatagramProtocolSocket {
	var socket = &TUserDatagramProtocolSocket{}
	socket = nil
	if socket != nil {
		socket.Vആരംഭിക്കുക(*self, nil)
		socket.listening = true
		socket.localPort = port
		socket.localIP = uint32((*ipHandler.GetProvider()).GetIPAddress())

		socket.localPort = Uint16_R(socket.localPort)
	}
	return socket
}
func (self *TUserDatagramProtocolProvider) Disconnect(socket *TUserDatagramProtocolSocket) {
	for i := 0; i < numSockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numSockets--
			sockets[i] = sockets[numSockets]
			break
		}
	}
}
func (self *TUserDatagramProtocolProvider) Send(socket *TUserDatagramProtocolSocket, p_data uintptr, വലുപ്പം uint16) {
	var totalLength = uint32(വലുപ്പം) + udpHeaderSize

	var buffer [4096]byte

	var msgBuffer = (*TUserDatagramProtocolHeaderBuffer)(Pointer(&buffer))

	var msg = TUserDatagramProtocolHeader{}

	msg.srcPort = socket.localPort
	msg.dstPort = socket.remotePort
	msg.length = Uint16_R(uint16(totalLength))

	msg.checksum = 0x0
	msg.SetBuffer(msgBuffer)

	var dataBytes [4096]byte = *(*[4096]byte)(Pointer(p_data))
	for i := 0; i < int(വലുപ്പം); i++ {
		buffer[int(udpHeaderSize)+i] = dataBytes[i]
	}

	var data uintptr = uintptr(Pointer(&buffer))

	ipHandler.Send(socket.remoteIP, 0x11, data, totalLength)

}
func (self *TUserDatagramProtocolProvider) Bind(socket *TUserDatagramProtocolSocket, handler *TUserDatagramProtocolHandler) {
}
