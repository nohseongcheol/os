package etherframe

import . "console"

import . "amd_am79c973"
import . "unsafe"
import . "util"

var 이더넷콘솔 T콘솔 = T콘솔{}

type TEtherFrameHeaderBuffer struct {
	dstMAC_BE	[6]byte
	srcMAC_BE		[6]byte
	etherType_BE		[2]byte
}

var frameHeaderSize int = 14

type TEtherFrameHeader struct {
	dstMAC_BE	uint64
	srcMAC_BE		uint64
	etherType_BE		uint16
}

func (self *TEtherFrameHeader) Vآغاز_کرنا(buffer TEtherFrameHeaderBuffer) {
	self.dstMAC_BE = (ArrayToUint48(buffer.dstMAC_BE))
	self.srcMAC_BE = (ArrayToUint48(buffer.srcMAC_BE))
	self.etherType_BE = (ArrayToUint16(buffer.etherType_BE))

}
func (self *TEtherFrameHeader) SetBuffer(buffer *TEtherFrameHeaderBuffer) {
	buffer.dstMAC_BE = Uint48ToArray(Uint48_R(self.dstMAC_BE))
	buffer.srcMAC_BE = Uint48ToArray(Uint48_R(self.srcMAC_BE))
	buffer.etherType_BE = Uint16ToArray(Uint16_R(self.etherType_BE))
}

type IEtherFrameHandler interface {
	Vآغاز_کرنا(backend TEtherFrameProvider)
	SetHandler(handler IEtherFrameHandler, etherType uint16)
	OnEtherFrameReceived(dataPointer uintptr, حجم int) bool
	Send(dstMAC_BE uint64, dataPointer uintptr, حجم uint32)
	SendFrame(dstMAC_BE uint64, etherType_BE uint16, dataPointer uintptr, حجم uint32)
	GetProvider() TEtherFrameProvider
	GetMACAddress() uint64
	GetIPAddress() uint64
}

type TEtherFrameHandler struct {
}

var frame TEtherFrameHeader
var Backend TEtherFrameProvider
var handlers [65535]IEtherFrameHandler
var efHandler *TEtherFrameHandler = nil

func (self *TEtherFrameHandler) Vآغاز_کرنا(backend TEtherFrameProvider) {
	Backend = backend
}

func (self *TEtherFrameHandler) SetHandler(handler IEtherFrameHandler, p_etherType uint16) {
	handlers[p_etherType] = handler
}
func (self *TEtherFrameHandler) SetBackend(backend TEtherFrameProvider) {
	Backend = backend
}
func (self *TEtherFrameHandler) GetBackend() TEtherFrameProvider {
	return Backend
}
func (self *TEtherFrameHandler) OnEtherFrameReceived(dataPointer uintptr, حجم int) bool {
	이더넷콘솔.M출력(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEtherFrameHandler) Send(dstMAC_BE uint64, dataPointer uintptr, حجم uint32) {
	Backend.SendFrame(dstMAC_BE, frame.etherType_BE, dataPointer, حجم)
}
func (self *TEtherFrameHandler) SendFrame(dstMAC_BE uint64, etherType_BE uint16, dataPointer uintptr, حجم uint32) {
	Backend.SendFrame(dstMAC_BE, etherType_BE, dataPointer, حجم)
}
func (self *TEtherFrameHandler) GetMACAddress() uint64 {
	return Backend.GetMACAddress()
}
func (self *TEtherFrameHandler) GetIPAddress() uint64 {
	return Backend.GetIPAddress()
}
func (self *TEtherFrameHandler) GetProvider() TEtherFrameProvider {
	return Backend
}

type TEtherFrameRawDataHandler struct {
	TRawDataHandler
}

var provider TEtherFrameProvider

func (self *TEtherFrameRawDataHandler) Vآغاز_کرنا(p_provider TEtherFrameProvider, p_backend Tamd_am79c973) {
	provider = p_provider
	provider.Vآغاز_کرنا(p_backend)
}
func (self *TEtherFrameRawDataHandler) OnRawDataReceived(dataPointer uintptr, حجم int) bool {
	return provider.OnRawDataReceived(dataPointer, حجم)
}
func (self *TEtherFrameRawDataHandler) Send(dataPointer uintptr, حجم uint32) {
	provider.Send(dataPointer, حجم)
}
func (self *TEtherFrameRawDataHandler) GetMACAddress() uint64 {
	return provider.GetMACAddress()
}
func (self *TEtherFrameRawDataHandler) GetIPAddress() uint64 {
	return provider.GetIPAddress()
}
func (self *TEtherFrameRawDataHandler) GetProvider() TEtherFrameProvider {
	return provider
}

type TEtherFrameProvider struct {
	netCard	Tamd_am79c973
	handlers	[65565]IEtherFrameHandler
}

func (self *TEtherFrameProvider) Vآغاز_کرنا(backend Tamd_am79c973) {

	self.netCard = backend
	for i := 0; i < 65535; i++ {
		handlers[i] = nil
		self.handlers[i] = nil
	}
}

var count uint16 = 0

func (self *TEtherFrameProvider) OnRawDataReceived(dataPointer uintptr, حجم int) bool {

	var buffer *TEtherFrameHeaderBuffer = (*TEtherFrameHeaderBuffer)(Pointer(dataPointer))
	var frame TEtherFrameHeader = TEtherFrameHeader{}
	frame.Vآغاز_کرنا(*buffer)
	var sendBack bool = false

	if frame.dstMAC_BE == 0x0000FFFFFFFFFFFF || Uint48_R(frame.dstMAC_BE) == self.GetMACAddress() {
		if handlers[frame.etherType_BE] != nil {
			이더넷콘솔.M출력(([]byte)("provider\n"))

			var پتے_کا_حوالہ uintptr = uintptr(Pointer(dataPointer)) + uintptr(frameHeaderSize)
			sendBack = handlers[frame.etherType_BE].OnEtherFrameReceived(پتے_کا_حوالہ, حجم-frameHeaderSize)

		}
	}

	if sendBack {
		frame.dstMAC_BE = frame.srcMAC_BE
		frame.srcMAC_BE = Uint48_R(self.GetMACAddress())
		frame.SetBuffer(buffer)

	}

	이더넷콘솔.M출력XY(([]byte)("spro["), 0, 1)
	이더넷콘솔.MUint64출력(frame.srcMAC_BE)
	이더넷콘솔.M출력(([]byte)(":"))
	이더넷콘솔.MUint64출력(frame.dstMAC_BE)
	이더넷콘솔.M출력(([]byte)(":]["))
	이더넷콘솔.MUint64출력(self.GetMACAddress())
	이더넷콘솔.M출력(([]byte)(":"))
	이더넷콘솔.MUint16출력(frame.etherType_BE)
	이더넷콘솔.M출력(([]byte)("]"))

	return sendBack

}
func (self *TEtherFrameProvider) Send(dataPointer uintptr, حجم uint32) {
	self.netCard.Send(dataPointer, حجم)
}
func (self *TEtherFrameProvider) SendFrame(dstMAC_BE uint64, etherType_BE uint16, dataPointer uintptr, حجم uint32) {

	var buffer2 [4096]byte
	var buffer *TEtherFrameHeaderBuffer = (*TEtherFrameHeaderBuffer)(Pointer(&buffer2))

	var frame TEtherFrameHeader = TEtherFrameHeader{}
	frame.Vآغاز_کرنا(*buffer)

	frame.dstMAC_BE = Uint48_R(dstMAC_BE)
	frame.srcMAC_BE = Uint48_R(self.netCard.GetMACAddress())
	frame.etherType_BE = Uint16_R(etherType_BE)

	frame.SetBuffer(buffer)
	var src [4096]byte = *(*([4096]byte))(Pointer(dataPointer))

	var i uint32 = 0
	for i = 0; i < حجم; i++ {
		buffer2[uint32(frameHeaderSize)+i] = src[i]

	}

	var پتے_کا_حوالہ uintptr = uintptr(Pointer(&buffer2))

	self.netCard.Send(پتے_کا_حوالہ, حجم+uint32(frameHeaderSize))

}
func (self *TEtherFrameProvider) GetMACAddress() uint64 {
	return self.netCard.GetMACAddress()
}
func (self *TEtherFrameProvider) GetIPAddress() uint64 {
	return self.netCard.GetIPAddress()
}
