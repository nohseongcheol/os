package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "etherframe"
import . "arp"

var ip콘솔 T콘솔 = T콘솔{}

type TInternetProtocolV4MessageBuffer struct {
	len_ver		byte
	tos		byte
	totalLength	[2]byte

	ident		[2]byte
	flagsAndOffset	[2]byte

	timeToLive	byte
	protocol	byte
	checksum	[2]byte

	srcIP		[4]byte
	dstIP	[4]byte
}

var ipSize uint8 = (4 + 4 + 4 + 8)

type TInternetProtocolV4Message struct {
	headerLength	uint8
	version		uint8
	tos		uint8
	totalLength	uint16

	ident		uint16
	flagsAndOffset	uint16

	timeToLive	uint8
	protocol	uint8
	checksum	uint16

	srcIP		uint32
	dstIP	uint32
}

func (self *TInternetProtocolV4Message) Init(buffer TInternetProtocolV4MessageBuffer) {

	self.version = ((buffer.len_ver & 0xF0) >> 4)
	self.headerLength = buffer.len_ver & 0x0F
	self.tos = buffer.tos
	self.totalLength = Uint16_R(ArrayToUint16(buffer.totalLength))

	self.ident = Uint16_R(ArrayToUint16(buffer.ident))
	self.flagsAndOffset = Uint16_R(ArrayToUint16(buffer.flagsAndOffset))

	self.timeToLive = buffer.timeToLive
	self.protocol = buffer.protocol
	self.checksum = Uint16_R(ArrayToUint16(buffer.checksum))

	self.srcIP = Uint32_R(ArrayToUint32(buffer.srcIP))
	self.dstIP = Uint32_R(ArrayToUint32(buffer.dstIP))

}
func (self *TInternetProtocolV4Message) SetBuffer(buffer *TInternetProtocolV4MessageBuffer) {

	buffer.len_ver = byte(((self.version & 0x0F) << 4) | (self.headerLength & 0x0F))
	buffer.tos = self.tos
	buffer.totalLength = Uint16ToArray(self.totalLength)

	buffer.ident = Uint16ToArray(self.ident)
	buffer.flagsAndOffset = Uint16ToArray(self.flagsAndOffset)

	buffer.timeToLive = self.timeToLive
	buffer.protocol = self.protocol
	buffer.checksum = Uint16ToArray(self.checksum)

	buffer.srcIP = Uint32ToArray(self.srcIP)
	buffer.dstIP = Uint32ToArray(self.dstIP)

}

type IInternetProtocolHandler interface {
	Init(backend TInternetProtocolProvider, p_iHandler IInternetProtocolHandler, p_protocol uint8)
	OnInternetProtocolReceived(srcIP_BE uint32, dstIP_BE uint32, dataPointer uintptr, size uint32) bool
	Send(dstIP_BE uint32, p_protocol uint8, dataPointer uintptr, size uint32)
	GetProvider() *TInternetProtocolProvider
}

type TInternetProtocolHandler struct {
}

var ipEtherFrameHandler TIPEtherFrameHandler = TIPEtherFrameHandler{}
var protocol uint8

func (self *TInternetProtocolHandler) Init(backend TInternetProtocolProvider, p_iHandler IInternetProtocolHandler, p_protocol uint8) {
	protocol = p_protocol
	handlers[protocol] = p_iHandler
}
func (self *TInternetProtocolHandler) OnInternetProtocolReceived(srcIP_BE uint32, dstIP_BE uint32, dataPointer uintptr, size uint32) bool {
	ip콘솔.M출력(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetProtocolHandler) Send(dstIP_BE uint32, p_protocol uint8, dataPointer uintptr, size uint32) {

	ipProvider.Send(dstIP_BE, p_protocol, dataPointer, size)
}
func (self *TInternetProtocolHandler) GetProvider() *TInternetProtocolProvider {
	return &ipProvider
}

type TIPEtherFrameHandler struct {
	TEtherFrameHandler
}

var ipProvider TInternetProtocolProvider

func (self *TIPEtherFrameHandler) OnEtherFrameReceived(dataPointer uintptr, size int) bool {
	ip콘솔.M출력(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipProvider.OnEtherFrameReceived(dataPointer, uint32(size))

}

func (self *TIPEtherFrameHandler) Send(dstIP_BE uint64, dataPointer uintptr, size uint32) {
	ip콘솔.M출력(([]byte)("ipefhandler:send\n"))
	var etherType_BE = Uint16_R(0x0800)
	self.TEtherFrameHandler.SendFrame(dstIP_BE, etherType_BE, dataPointer, size)

}

var handlers [255]IInternetProtocolHandler

type TInternetProtocolProvider struct {
	arpProvider	TARPProvider
	GatewayIP	uint32
	SubnetMask	uint32
}

var efHandler IEtherFrameHandler

func (self *TInternetProtocolProvider) Init(p_efProvider TEtherFrameProvider, p_efHandler IEtherFrameHandler, arp TARPProvider, gatewayIP uint32, subnetMask uint32) {

	efHandler = p_efHandler
	efHandler.SetHandler(p_efHandler, 0x0800)

	for i := 0; i < 255; i++ {
		handlers[i] = nil
	}

	self.arpProvider = arp
	self.GatewayIP = gatewayIP
	self.SubnetMask = subnetMask
	ipProvider = *self
}
func (self *TInternetProtocolProvider) OnEtherFrameReceived(etherframePayload uintptr, size uint32) bool {
	if size < uint32(ipSize) {
		return false
	}

	var buffer *TInternetProtocolV4MessageBuffer = (*TInternetProtocolV4MessageBuffer)(Pointer(etherframePayload))
	var ipmessage TInternetProtocolV4Message
	ipmessage.Init(*buffer)

	var sendBack bool = false

	if ipmessage.dstIP == uint32(efHandler.GetIPAddress()) {

		var length uint32 = uint32(ipmessage.totalLength)
		if length > size {
			length = size
		}
		if handlers[ipmessage.protocol] != nil {
			sendBack = handlers[ipmessage.protocol].OnInternetProtocolReceived(ipmessage.srcIP, ipmessage.dstIP, etherframePayload+uintptr(4*ipmessage.headerLength), uint32(length-uint32(4*ipmessage.headerLength)))

		}
	}

	if sendBack {

		var temp = ipmessage.dstIP
		ipmessage.dstIP = ipmessage.srcIP
		ipmessage.srcIP = temp

		ipmessage.timeToLive = 0x40
		ipmessage.checksum = 0

		ipmessage.SetBuffer(buffer)
		ipmessage.checksum = self.Checksum((*([4096]uint16))(Pointer(etherframePayload)), uint32(4*ipmessage.headerLength))

		ipmessage.SetBuffer(buffer)

	}

	ip콘솔.M출력(([]byte)("ipmessage"))
	ip콘솔.MUint32출력(ipmessage.srcIP)
	ip콘솔.M출력(([]byte)(":"))
	ip콘솔.MUint32출력(ipmessage.dstIP)
	ip콘솔.M출력(([]byte)(":"))
	ip콘솔.MUint16출력(uint16(ipmessage.headerLength))
	ip콘솔.M출력(([]byte)(":"))
	ip콘솔.MUint16출력(uint16(ipmessage.version))
	ip콘솔.M출력(([]byte)(":"))
	ip콘솔.MUint16출력(ipmessage.totalLength)
	ip콘솔.M출력(([]byte)(":"))
	ip콘솔.MUint32출력(uint32(efHandler.GetIPAddress()))
	ip콘솔.M출력(([]byte)(":"))
	ip콘솔.M출력(([]byte)("\n"))

	return sendBack

}
func (self *TInternetProtocolProvider) Send(dstIP_BE uint32, protocol uint8, dataPointer uintptr, size uint32) {
	var buffer1 [4096]byte
	var buffer *TInternetProtocolV4MessageBuffer = (*TInternetProtocolV4MessageBuffer)(Pointer(&buffer1))
	var message TInternetProtocolV4Message = TInternetProtocolV4Message{}
	message.version = 4
	message.headerLength = ipSize / 4
	message.tos = 0
	message.totalLength = Uint16_R(uint16(size + uint32(ipSize)))

	message.ident = 0x0100
	message.flagsAndOffset = 0x0040
	message.timeToLive = 0x40
	message.protocol = protocol

	message.dstIP = dstIP_BE

	message.srcIP = uint32(efHandler.GetIPAddress())

	message.checksum = 0

	message.SetBuffer(buffer)
	message.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1)), uint32(ipSize))
	message.SetBuffer(buffer)

	var databuffer [4096]byte = *(*([4096]byte))(Pointer(dataPointer))

	for i := 0; i < int(size); i++ {

		buffer1[i+int(ipSize)] = databuffer[i]
	}

	ip콘솔.M출력XY(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(size)+int(ipSize); i++ {
		ip콘솔.MHex출력(buffer1[i])
	}
	ip콘솔.M출력(([]byte)(":"))
	ip콘솔.M출력(([]byte)("]\n"))

	var nextHopIP_BE uint32 = dstIP_BE
	if (dstIP_BE & self.SubnetMask) != (message.srcIP & self.SubnetMask) {
		nextHopIP_BE = self.GatewayIP
	}

	var sendDataPointer = uintptr(Pointer(&buffer1))
	ip콘솔.MUint32출력(nextHopIP_BE)

	var etherType_BE = Uint16_R(0x0800)
	efHandler.SendFrame(self.arpProvider.Resolve(nextHopIP_BE), etherType_BE, sendDataPointer, uint32(ipSize)+uint32(size))

}
func (self *TInternetProtocolProvider) Checksum(p_data *[4096]uint16, lengthInBytes uint32) uint16 {
	var data [4096]uint16 = *p_data
	var temp uint32 = 0
	var dataBytes [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengthInBytes % 2) != 0 {
		temp += uint32(uint16(dataBytes[lengthInBytes-1]) << 8)
	}

	for (temp & 0xFFFF0000) != 0 {
		temp = (temp & 0xFFFF) + (temp >> 16)
	}

	return uint16(((^temp & 0xFF00) >> 8) | ((^temp & 0x00FF) << 8))
}
func (self *TInternetProtocolProvider) GetIPAddress() uint64 {
	return efHandler.GetIPAddress()
}
