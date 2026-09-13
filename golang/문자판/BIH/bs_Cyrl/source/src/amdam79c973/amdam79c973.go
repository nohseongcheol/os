package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "port"
import . "pci"

var mrežaKartaškeconsole TConsole = TConsole{}

type TInitializationblok struct {
	režim			uint16
	brojPošaljibuffer	uint8
	brojrecvbuffer		uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferOpisaddress		uintptr
	pošaljibufferOpisaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	zastave		uint32
	zastave2	uint32
	dostupan	uint32
}

type IRawdatahandler interface {
	Uključenrawdatareceive(datapointer uintptr, veličina int) bool
	Pošalji(datapointer uintptr, veličina uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (self *TRawdatahandler) Skupbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (self *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (self *TRawdatahandler) Uključenrawdatareceive(datapointer uintptr, veličina int) bool {
	mrežaKartaškeconsole.MŠtampajxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Pošalji(datapointer uintptr, veličina uint32) {
	mrežaKartaškeconsole.MŠtampajxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Pošalji(datapointer, veličina)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var resetujport uint16
var buscontrolregisterdataport uint16

var initblok TInitializationblok

var pošaljibufferOpis [8]TBufferdescriptor
var pošaljibufferOpisMemorija [2048 + 15]byte
var pošaljibuffer [2*1024 + 15][8]uint8
var currentPošaljibuffer uint8

var recvbufferOpis [8]TBufferdescriptor
var recvbufferOpisMemorija [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var currentrecvbuffer uint8
var funcVrijednost func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	uređajdescriptor	TPeripheralcomponentinterconnectUređajdescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, uređajdescriptor TPeripheralcomponentinterconnectUređajdescriptor, handler IRawdatahandler) {

	self.uređajdescriptor = uređajdescriptor

	funcVrijednost = (*Tamdam79c973).Handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&funcVrijednost))

	self.Init(uint8(0x20+uređajdescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0port = uint16(uređajdescriptor.Portbase)
	Macaddress2port = uint16(uređajdescriptor.Portbase) + 0x02
	Macaddress4port = uint16(uređajdescriptor.Portbase) + 0x04
	registerdataport = uint16(uređajdescriptor.Portbase) + 0x10
	registeraddressport = uint16(uređajdescriptor.Portbase) + 0x12
	resetujport = uint16(uređajdescriptor.Portbase) + 0x14
	buscontrolregisterdataport = uint16(uređajdescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	currentPošaljibuffer = 0
	currentrecvbuffer = 0

	var Mac0 uint64 = uint64(PortČitajword(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortČitajword(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortČitajword(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortČitajword(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortČitajword(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortČitajword(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MŠtampajxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalŠtampaj(uint8(uređajdescriptor.Interrupt))
	console_2.MŠtampaj(([]byte)("]"))
	console_2.MŠtampaj(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Štampaj(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Štampaj(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MŠtampaj(([]byte)("]"))

	PortPišiword(registeraddressport, 20)
	PortPišiword(buscontrolregisterdataport, 0x102)

	PortPišiword(registeraddressport, 0)
	PortPišiword(registerdataport, 0x04)

	initblok.režim = 0x0000
	initblok.brojPošaljibuffer = 3
	initblok.brojrecvbuffer = 3

	initblok.physicaladdress = Mac

	initblok.logicaladdress = 0

	pošaljibufferOpis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&pošaljibufferOpisMemorija)) + 15) & ^(uintptr)(0xF)))
	initblok.pošaljibufferOpisaddress = uintptr(Pointer(&pošaljibufferOpis))
	recvbufferOpis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferOpisMemorija)) + 15) & ^(uintptr)(0xF)))
	initblok.recvbufferOpisaddress = uintptr(Pointer(&recvbufferOpis))

	for i := 0; i < 8; i++ {
		pošaljibufferOpis[i].address_2 = uint32((uintptr(Pointer(&pošaljibuffer[i])) + 15) & ^(uintptr(0xF)))
		pošaljibufferOpis[i].zastave = 0x7FF | 0xF000
		pošaljibufferOpis[i].zastave2 = 0
		pošaljibufferOpis[i].dostupan = 0

		recvbufferOpis[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferOpis[i].zastave = 0xF7FF | 0x80000000

	}

	PortPišiword(registeraddressport, 1)
	PortPišiword(registerdataport, uint16(uintptr(Pointer(&initblok))&0xFFFF))

	PortPišiword(registeraddressport, 2)
	PortPišiword(registerdataport, uint16((uintptr(Pointer(&initblok))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Aktiviraj() {
	PortPišiword(registeraddressport, 0)
	PortPišiword(registerdataport, 0x41)

	PortPišiword(registeraddressport, 4)
	temporary := PortČitajword(registerdataport)
	PortPišiword(registeraddressport, 4)
	PortPišiword(registerdataport, temporary|0xC00)

	PortPišiword(registeraddressport, 0)
	PortPišiword(registerdataport, 0x42)

}
func (self *Tamdam79c973) Resetuj() int {
	PortČitajword(resetujport)
	PortPišiword(resetujport, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) Handleinterrupt(esp uint32) uint32 {

	PortPišiword(registeraddressport, 0)
	temporary := uint32(PortČitajword(registerdataport))
	console_2.MŠtampaj(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Štampaj(esp)
	console_2.MŠtampaj(([]byte)(":"))
	console_2.MUnsignedinteger32Štampaj(temporary)
	console_2.MŠtampaj(([]byte)(":"))
	console_2.MUnsignedinteger16Štampaj(count)
	count++
	console_2.MŠtampaj(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MŠtampaj(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MŠtampaj(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MŠtampaj(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MŠtampaj(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MŠtampaj(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MŠtampaj(([]byte)("am79c973 data sent"))
	}

	PortPišiword(registeraddressport, 0)
	PortPišiword(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MŠtampaj(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Pošalji(datapointer uintptr, veličina uint32) {
	var pošaljidescriptor uint16 = uint16(currentPošaljibuffer)
	currentPošaljibuffer = 0

	if veličina > 1518 {
		veličina = 1518
	}

	var izvor_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	var odredište_2 uint32 = pošaljibufferOpis[pošaljidescriptor].address_2 + veličina - 1

	for i := 0; i < int(veličina); i++ {

		*(*byte)(Pointer(uintptr(odredište_2))) = izvor_2[int(veličina)-i-1]

		odredište_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(datapointer))
	console_2.MŠtampajxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalŠtampaj(data[i])
		console_2.MŠtampaj(([]byte)(":"))
	}
	console_2.MŠtampaj(([]byte)("\n"))

	pošaljibufferOpis[pošaljidescriptor].dostupan = 0
	pošaljibufferOpis[pošaljidescriptor].zastave2 = 0
	pošaljibufferOpis[pošaljidescriptor].zastave = 0x8300F000 | uint32((-veličina)&0xFFF)

	PortPišiword(registeraddressport, 0)
	PortPišiword(registerdataport, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MŠtampaj(([]byte)(":"))
	console_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(&pošaljibuffer))))
	console_2.MŠtampaj(([]byte)(":"))
	console_2.MHexadecimalŠtampaj(pošaljibuffer[0][0])
	console_2.MHexadecimalŠtampaj(pošaljibuffer[0][1])
	console_2.MŠtampaj(([]byte)(":"))
	currentrecvbuffer = 0

	for ; (recvbufferOpis[currentrecvbuffer].zastave & 0x80000000) == 0; currentrecvbuffer = (currentrecvbuffer + 1) % 8 {

		if !(recvbufferOpis[currentrecvbuffer].zastave&0x40000000 != 0) && ((recvbufferOpis[currentrecvbuffer].zastave & 0x03000000) == 0x03000000) {
			var veličina uint32 = recvbufferOpis[currentrecvbuffer].zastave & 0xFFF
			if veličina > 64 {
				veličina -= 4
			}

			console_2.MŠtampaj([]byte(" size : ["))
			console_2.MUnsignedinteger32Štampaj(veličina)
			console_2.MŠtampaj([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferOpis[currentrecvbuffer].address_2)))
			var pointer uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Uključenrawdatareceive(pointer, int(veličina)) {

					console_2.MŠtampajxy(([]byte)("self.Send"), 0, 22)

					self.Pošalji(pointer, veličina)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalŠtampaj(buffer_2[i])
				console_2.MŠtampaj([]byte(":"))
			}

		}
		recvbufferOpis[currentrecvbuffer].zastave2 = 0
		recvbufferOpis[currentrecvbuffer].zastave = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Skuphandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initblok.physicaladdress
}
func (self *Tamdam79c973) Skupipaddress(ip uint64) {
	initblok.logicaladdress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initblok.logicaladdress
}
