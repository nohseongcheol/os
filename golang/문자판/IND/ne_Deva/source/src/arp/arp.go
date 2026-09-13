package arp

import . "unsafe"
import . "console"
import . "etherframe"
import . "util"

var arp콘솔 T콘솔 = T콘솔{}

type TARPMessageBuffer struct {
	hardwareType		[2]byte
	protocol		[2]byte
	hardwareAddressSize	byte
	protocolAddressSize	byte
	command			[2]byte

	srcMAC	[6]byte
	srcIP		[4]byte
	dstMAC	[6]byte
	dstIP	[4]byte
}

var arpMesgSize uint32 = (64+92+64)/8 + 2

type TARPMessage struct {
	hardwareType		uint16
	protocol		uint16
	hardwareAddressSize	uint8
	protocolAddressSize	uint8
	command			uint16

	srcMAC	uint64
	srcIP		uint32
	dstMAC	uint64
	dstIP	uint32
}

func (self *TARPMessage) Vआरम्भ_गर्नु(buffer *TARPMessageBuffer) {

	self.hardwareType = Uint16_R(ArrayToUint16(buffer.hardwareType))
	self.protocol = Uint16_R(ArrayToUint16(buffer.protocol))
	self.hardwareAddressSize = byte(buffer.hardwareAddressSize)
	self.protocolAddressSize = byte(buffer.protocolAddressSize)
	self.command = Uint16_R(ArrayToUint16(buffer.command))

	self.srcMAC = Uint48_R(ArrayToUint48(buffer.srcMAC))
	self.srcIP = Uint32_R(ArrayToUint32(buffer.srcIP))
	self.dstMAC = Uint48_R(ArrayToUint48(buffer.dstMAC))
	self.dstIP = Uint32_R(ArrayToUint32(buffer.dstIP))
}
func (self *TARPMessage) SetBuffer(buffer *TARPMessageBuffer) {
	buffer.hardwareType = Uint16ToArray(self.hardwareType)
	buffer.protocol = Uint16ToArray(self.protocol)
	buffer.hardwareAddressSize = uint8(self.hardwareAddressSize)
	buffer.protocolAddressSize = uint8(self.protocolAddressSize)

	buffer.command = Uint16ToArray(self.command)
	buffer.srcMAC = Uint48ToArray(self.srcMAC)
	buffer.srcIP = Uint32ToArray(self.srcIP)
	buffer.dstMAC = Uint48ToArray(self.dstMAC)
	buffer.dstIP = Uint32ToArray(self.dstIP)
}

type TARPEtherFrameHandler struct {
	TEtherFrameHandler
}

var arpProvider TARPProvider
var etherFrameProvider TEtherFrameProvider

func (self *TARPEtherFrameHandler) OnEtherFrameReceived(dataPointer uintptr, आकार int) bool {
	arp콘솔.M출력XY([]byte("arp recv:"), 0, 23)
	return arpProvider.OnEtherFrameReceived(dataPointer, uint32(आकार))

}
func (self *TARPEtherFrameHandler) Send(dstMAC_BE uint64, dataPointer uintptr, आकार uint32) {
	arp콘솔.M출력XY([]byte("arp send:"), 0, 24)
	var etherType_BE = Uint16_R(0x0806)
	self.TEtherFrameHandler.SendFrame(dstMAC_BE, etherType_BE, dataPointer, आकार)
}

type TARPProvider struct {
	IPCache			[128]uint32
	MACCache		[128]uint64
	numCacheEntries	int

	handler	IEtherFrameHandler
}

var handler IEtherFrameHandler

func (self *TARPProvider) Vआरम्भ_गर्नु(backend TEtherFrameProvider, userhandler IEtherFrameHandler) {

	handler = userhandler
	handler.Vआरम्भ_गर्नु(backend)
	handler.SetHandler(userhandler, 0x0806)
	self.numCacheEntries = 0
	arpProvider = *self

}

func (self *TARPProvider) OnEtherFrameReceived(dataPointer uintptr, आकार uint32) bool {

	if आकार < arpMesgSize {
		return false
	}
	var arpBuffer *TARPMessageBuffer = (*TARPMessageBuffer)(Pointer(dataPointer))
	var arp TARPMessage = TARPMessage{}
	arp.Vआरम्भ_गर्नु(arpBuffer)

	if arp.hardwareType == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareAddressSize == 6 && arp.protocolAddressSize == 4 && uint64(arp.dstIP) == handler.GetIPAddress() {

			arp콘솔.M출력([]byte("arp onetherframe"))
			arp콘솔.MUint16출력(arp.protocol)
			arp콘솔.M출력([]byte(":"))
			arp콘솔.MUint64출력(uint64(arp.dstMAC))
			arp콘솔.M출력([]byte(":"))
			arp콘솔.MUint16출력(arp.command)
			arp콘솔.M출력([]byte(":"))
			arp콘솔.MUint64출력(handler.GetMACAddress())

			switch arp.command {
			case 0x0100:

				if self.GetMACFromCache(arp.srcIP) == 0xFFFFFFFFFFFF {
					if self.numCacheEntries < 128 {
						self.IPCache[self.numCacheEntries] = arp.srcIP
						self.MACCache[self.numCacheEntries] = arp.srcMAC
						self.numCacheEntries++
					}
				}
				arp.command = 0x0200
				arp.dstIP = arp.srcIP
				arp.dstMAC = arp.srcMAC
				arp.srcIP = uint32(handler.GetIPAddress())
				arp.srcMAC = handler.GetMACAddress()
				arp.SetBuffer(arpBuffer)

				return true
				break

			case 0x0200:
				arp콘솔.M출력(([]byte)("self.numCacheEntries"))

				if self.numCacheEntries < 128 {
					self.IPCache[self.numCacheEntries] = arp.srcIP
					self.MACCache[self.numCacheEntries] = arp.srcMAC
					self.numCacheEntries++
				}
				break
			}

		}
	}
	return false

}

func (self *TARPProvider) BroadcastMacAddress(IP_BE uint32) {

	var arp TARPMessage = TARPMessage{}
	arp.hardwareType = 0x0100
	arp.protocol = 0x0008
	arp.hardwareAddressSize = 6
	arp.protocolAddressSize = 4
	arp.command = 0x0200

	arp.srcIP = uint32(handler.GetIPAddress())

	arp.dstMAC = self.Resolve(IP_BE)
	arp.dstIP = IP_BE
	arp콘솔.M출력XY([]byte("broad mac"), 0, 15)

	arp.srcMAC = handler.GetMACAddress()

	var arpBuffer TARPMessageBuffer = TARPMessageBuffer{}
	arp.SetBuffer(&arpBuffer)

	var ठेगाना_सूचक uintptr = uintptr(Pointer(&arpBuffer))
	handler.Send(arp.dstMAC, ठेगाना_सूचक, arpMesgSize)
}
func (self *TARPProvider) RequestMacAddress(IP_BE uint32) {

	var arp TARPMessage = TARPMessage{}
	arp.hardwareType = 0x0100

	arp.protocol = 0x0008
	arp.hardwareAddressSize = 6
	arp.protocolAddressSize = 4
	arp.command = 0x0100

	arp.srcMAC = handler.GetMACAddress()
	arp.srcIP = uint32(handler.GetIPAddress())

	arp.dstMAC = 0xFFFFFFFFFFFF
	arp.dstIP = IP_BE

	var arpBuffer TARPMessageBuffer = TARPMessageBuffer{}
	arp.SetBuffer(&arpBuffer)

	var ठेगाना_सूचक uintptr = uintptr(Pointer(&arpBuffer))
	handler.Send(arp.dstMAC, ठेगाना_सूचक, arpMesgSize)
}
func (self *TARPProvider) TestPrint(data *[]byte, आकार uint32) {
	var buffer [4096]byte = *(*([4096]byte))(Pointer(data))
	arp콘솔.M출력XY([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arp콘솔.MHex출력(buffer[i])
		arp콘솔.M출력([]byte(":"))
	}
	arp콘솔.M출력([]byte("]"))
}

func (self *TARPProvider) GetMACFromCache(IP_BE uint32) uint64 {
	for i := 0; i < self.numCacheEntries; i++ {
		for ipIdx := 0; ipIdx < 4; ipIdx++ {

		}

		for macIdx := 0; macIdx < 6; macIdx++ {

		}

		arp콘솔.M출력(([]byte)("["))
		arp콘솔.MUint32출력(self.IPCache[i])
		arp콘솔.M출력(([]byte)(":"))
		arp콘솔.MUint32출력(IP_BE)
		arp콘솔.M출력(([]byte)(":"))
		arp콘솔.M출력(([]byte)(":"))
		arp콘솔.MUint64출력(self.MACCache[i])
		arp콘솔.M출력(([]byte)("]\n"))

		if self.IPCache[i] == IP_BE {
			arp콘솔.M출력([]byte("getmacfromcache"))
			return self.MACCache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *TARPProvider) Resolve(IP_BE uint32) uint64 {
	var result uint64 = self.GetMACFromCache(IP_BE)
	if result == 0xFFFFFFFFFFFF {
		self.RequestMacAddress(IP_BE)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.GetMACFromCache(IP_BE)

	}

	return result
}
