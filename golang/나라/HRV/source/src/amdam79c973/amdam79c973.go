package amdam79c973

import . "unsafe"
import . "prekid"
import . "console"
import . "port"
import . "pci"

var mrežaKarteconsole TConsole = TConsole{}

type TInitializationBlokiraj struct {
	nAČIN			uint16
	bROJPošaljibuffer	uint8
	bROJrecvbuffer		uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferOpisaddress		uintptr
	pošaljibufferOpisaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	zastavice	uint32
	zastavice2	uint32
	dostupno	uint32
}

type IRawdatahandler interface {
	Uključenorawdatareceive(dataPokazivač uintptr, veličina int) bool
	Pošalji(dataPokazivač uintptr, veličina uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (sam *TRawdatahandler) Postavibackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (sam *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (sam *TRawdatahandler) Uključenorawdatareceive(dataPokazivač uintptr, veličina int) bool {
	mrežaKarteconsole.MIspisxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (sam *TRawdatahandler) Pošalji(dataPokazivač uintptr, veličina uint32) {
	mrežaKarteconsole.MIspisxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Pošalji(dataPokazivač, veličina)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var vratiizvornoport uint16
var busCtrlregisterdataport uint16

var initBlokiraj TInitializationBlokiraj

var pošaljibufferOpis [8]TBufferdescriptor
var pošaljibufferOpisMemorija [2048 + 15]byte
var pošaljibuffer [2*1024 + 15][8]uint8
var trenutnoPošaljibuffer uint8

var recvbufferOpis [8]TBufferdescriptor
var recvbufferOpisMemorija [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var trenutnorecvbuffer uint8
var funcVrijednost func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TPrekidhandler
	uređajdescriptor	TPeripheralcomponentinterconnectUređajdescriptor
	prekid			*TPrekidmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (sam *Tamdam79c973) Initdriver(prekid *TPrekidmanager, uređajdescriptor TPeripheralcomponentinterconnectUređajdescriptor, handler IRawdatahandler) {

	sam.uređajdescriptor = uređajdescriptor

	funcVrijednost = (*Tamdam79c973).RučkaPrekid
	var address uintptr
	address = uintptr(Pointer(&funcVrijednost))

	sam.Init(uint8(0x20+uređajdescriptor.Prekid), uintptr(Pointer(prekid)), address)

	Macaddress0port = uint16(uređajdescriptor.Portbase)
	Macaddress2port = uint16(uređajdescriptor.Portbase) + 0x02
	Macaddress4port = uint16(uređajdescriptor.Portbase) + 0x04
	registerdataport = uint16(uređajdescriptor.Portbase) + 0x10
	registeraddressport = uint16(uređajdescriptor.Portbase) + 0x12
	vratiizvornoport = uint16(uređajdescriptor.Portbase) + 0x14
	busCtrlregisterdataport = uint16(uređajdescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	trenutnoPošaljibuffer = 0
	trenutnorecvbuffer = 0

	var Mac0 uint64 = uint64(PortČitajriječ(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortČitajriječ(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortČitajriječ(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortČitajriječ(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortČitajriječ(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortČitajriječ(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MIspisxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalIspis(uint8(uređajdescriptor.Prekid))
	console_2.MIspis(([]byte)("]"))
	console_2.MIspis(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Ispis(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Ispis(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MIspis(([]byte)("]"))

	PortZapiširiječ(registeraddressport, 20)
	PortZapiširiječ(busCtrlregisterdataport, 0x102)

	PortZapiširiječ(registeraddressport, 0)
	PortZapiširiječ(registerdataport, 0x04)

	initBlokiraj.nAČIN = 0x0000
	initBlokiraj.bROJPošaljibuffer = 3
	initBlokiraj.bROJrecvbuffer = 3

	initBlokiraj.physicaladdress = Mac

	initBlokiraj.logicaladdress = 0

	pošaljibufferOpis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&pošaljibufferOpisMemorija)) + 15) & ^(uintptr)(0xF)))
	initBlokiraj.pošaljibufferOpisaddress = uintptr(Pointer(&pošaljibufferOpis))
	recvbufferOpis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferOpisMemorija)) + 15) & ^(uintptr)(0xF)))
	initBlokiraj.recvbufferOpisaddress = uintptr(Pointer(&recvbufferOpis))

	for i := 0; i < 8; i++ {
		pošaljibufferOpis[i].address_2 = uint32((uintptr(Pointer(&pošaljibuffer[i])) + 15) & ^(uintptr(0xF)))
		pošaljibufferOpis[i].zastavice = 0x7FF | 0xF000
		pošaljibufferOpis[i].zastavice2 = 0
		pošaljibufferOpis[i].dostupno = 0

		recvbufferOpis[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferOpis[i].zastavice = 0xF7FF | 0x80000000

	}

	PortZapiširiječ(registeraddressport, 1)
	PortZapiširiječ(registerdataport, uint16(uintptr(Pointer(&initBlokiraj))&0xFFFF))

	PortZapiširiječ(registeraddressport, 2)
	PortZapiširiječ(registerdataport, uint16((uintptr(Pointer(&initBlokiraj))>>16)&0xFFFF))

}
func (sam *Tamdam79c973) Aktiviraj() {
	PortZapiširiječ(registeraddressport, 0)
	PortZapiširiječ(registerdataport, 0x41)

	PortZapiširiječ(registeraddressport, 4)
	temporary := PortČitajriječ(registerdataport)
	PortZapiširiječ(registeraddressport, 4)
	PortZapiširiječ(registerdataport, temporary|0xC00)

	PortZapiširiječ(registeraddressport, 0)
	PortZapiširiječ(registerdataport, 0x42)

}
func (sam *Tamdam79c973) Vratiizvorno() int {
	PortČitajriječ(vratiizvornoport)
	PortZapiširiječ(vratiizvornoport, 0)
	return 10
}

var count uint16 = 0

func (sam *Tamdam79c973) RučkaPrekid(esp uint32) uint32 {

	PortZapiširiječ(registeraddressport, 0)
	temporary := uint32(PortČitajriječ(registerdataport))
	console_2.MIspis(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Ispis(esp)
	console_2.MIspis(([]byte)(":"))
	console_2.MUnsignedinteger32Ispis(temporary)
	console_2.MIspis(([]byte)(":"))
	console_2.MUnsignedinteger16Ispis(count)
	count++
	console_2.MIspis(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MIspis(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MIspis(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MIspis(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MIspis(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MIspis(([]byte)("am79c973 data received"))
		sam.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MIspis(([]byte)("am79c973 data sent"))
	}

	PortZapiširiječ(registeraddressport, 0)
	PortZapiširiječ(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MIspis(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (sam *Tamdam79c973) Pošalji(dataPokazivač uintptr, veličina uint32) {
	var pošaljidescriptor uint16 = uint16(trenutnoPošaljibuffer)
	trenutnoPošaljibuffer = 0

	if veličina > 1518 {
		veličina = 1518
	}

	var izvor_2 [4096]byte = *(*([4096]byte))(Pointer(dataPokazivač))
	var odredište_2 uint32 = pošaljibufferOpis[pošaljidescriptor].address_2 + veličina - 1

	for i := 0; i < int(veličina); i++ {

		*(*byte)(Pointer(uintptr(odredište_2))) = izvor_2[int(veličina)-i-1]

		odredište_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataPokazivač))
	console_2.MIspisxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalIspis(data[i])
		console_2.MIspis(([]byte)(":"))
	}
	console_2.MIspis(([]byte)("\n"))

	pošaljibufferOpis[pošaljidescriptor].dostupno = 0
	pošaljibufferOpis[pošaljidescriptor].zastavice2 = 0
	pošaljibufferOpis[pošaljidescriptor].zastavice = 0x8300F000 | uint32((-veličina)&0xFFF)

	PortZapiširiječ(registeraddressport, 0)
	PortZapiširiječ(registerdataport, 0x48)

}
func (sam *Tamdam79c973) Receive() {
	console_2.MIspis(([]byte)(":"))
	console_2.MUnsignedinteger32Ispis(uint32(uintptr(Pointer(&pošaljibuffer))))
	console_2.MIspis(([]byte)(":"))
	console_2.MHexadecimalIspis(pošaljibuffer[0][0])
	console_2.MHexadecimalIspis(pošaljibuffer[0][1])
	console_2.MIspis(([]byte)(":"))
	trenutnorecvbuffer = 0

	for ; (recvbufferOpis[trenutnorecvbuffer].zastavice & 0x80000000) == 0; trenutnorecvbuffer = (trenutnorecvbuffer + 1) % 8 {

		if !(recvbufferOpis[trenutnorecvbuffer].zastavice&0x40000000 != 0) && ((recvbufferOpis[trenutnorecvbuffer].zastavice & 0x03000000) == 0x03000000) {
			var veličina uint32 = recvbufferOpis[trenutnorecvbuffer].zastavice & 0xFFF
			if veličina > 64 {
				veličina -= 4
			}

			console_2.MIspis([]byte(" size : ["))
			console_2.MUnsignedinteger32Ispis(veličina)
			console_2.MIspis([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferOpis[trenutnorecvbuffer].address_2)))
			var pokazivač uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Uključenorawdatareceive(pokazivač, int(veličina)) {

					console_2.MIspisxy(([]byte)("self.Send"), 0, 22)

					sam.Pošalji(pokazivač, veličina)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalIspis(buffer_2[i])
				console_2.MIspis([]byte(":"))
			}

		}
		recvbufferOpis[trenutnorecvbuffer].zastavice2 = 0
		recvbufferOpis[trenutnorecvbuffer].zastavice = 0x8000F7FF
	}
}
func (sam *Tamdam79c973) Postavihandler(handler *TRawdatahandler) {
	sam.handler = handler
}
func (sam *Tamdam79c973) Getmacaddress() uint64 {

	return initBlokiraj.physicaladdress
}
func (sam *Tamdam79c973) Postaviipaddress(ip uint64) {
	initBlokiraj.logicaladdress = ip
}
func (sam *Tamdam79c973) Getipaddress() uint64 {
	return initBlokiraj.logicaladdress
}
