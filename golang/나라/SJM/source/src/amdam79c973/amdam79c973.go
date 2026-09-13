package amdam79c973

import . "unsafe"
import . "avbrudd"
import . "console"
import . "port"
import . "pci"

var nettverkKortconsole TConsole = TConsole{}

type TInitializationBlokk struct {
	modus		uint16
	tallsendbuffer	uint8
	tallrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferBeskrivelseaddress	uintptr
	sendbufferBeskrivelseaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	flagg		uint32
	flagg2		uint32
	tilgjengelig	uint32
}

type IRawdatahandler interface {
	Pårawdatareceive(dataPeker uintptr, størrelse int) bool
	Send(dataPeker uintptr, størrelse uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (selv *TRawdatahandler) Settbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (selv *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (selv *TRawdatahandler) Pårawdatareceive(dataPeker uintptr, størrelse int) bool {
	nettverkKortconsole.MSkrivutxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (selv *TRawdatahandler) Send(dataPeker uintptr, størrelse uint32) {
	nettverkKortconsole.MSkrivutxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Send(dataPeker, størrelse)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var nullstillport uint16
var busKontrollregisterdataport uint16

var initBlokk TInitializationBlokk

var sendbufferBeskrivelse [8]TBufferdescriptor
var sendbufferBeskrivelseMinne [2048 + 15]byte
var sendbuffer [2*1024 + 15][8]uint8
var gjeldendesendbuffer uint8

var recvbufferBeskrivelse [8]TBufferdescriptor
var recvbufferBeskrivelseMinne [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var gjeldenderecvbuffer uint8
var funcVerdi func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TAvbruddhandler
	enhetdescriptor	TPeripheralcomponentinterconnectEnhetdescriptor
	avbrudd		*TAvbruddmanager
	handler		*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (selv *Tamdam79c973) Initdriver(avbrudd *TAvbruddmanager, enhetdescriptor TPeripheralcomponentinterconnectEnhetdescriptor, handler IRawdatahandler) {

	selv.enhetdescriptor = enhetdescriptor

	funcVerdi = (*Tamdam79c973).HåndtakAvbrudd
	var address uintptr
	address = uintptr(Pointer(&funcVerdi))

	selv.Init(uint8(0x20+enhetdescriptor.Avbrudd), uintptr(Pointer(avbrudd)), address)

	Macaddress0port = uint16(enhetdescriptor.Portbase)
	Macaddress2port = uint16(enhetdescriptor.Portbase) + 0x02
	Macaddress4port = uint16(enhetdescriptor.Portbase) + 0x04
	registerdataport = uint16(enhetdescriptor.Portbase) + 0x10
	registeraddressport = uint16(enhetdescriptor.Portbase) + 0x12
	nullstillport = uint16(enhetdescriptor.Portbase) + 0x14
	busKontrollregisterdataport = uint16(enhetdescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	gjeldendesendbuffer = 0
	gjeldenderecvbuffer = 0

	var Mac0 uint64 = uint64(PortLesord(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortLesord(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortLesord(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortLesord(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortLesord(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortLesord(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MSkrivutxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalSkrivut(uint8(enhetdescriptor.Avbrudd))
	console_2.MSkrivut(([]byte)("]"))
	console_2.MSkrivut(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Skrivut(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Skrivut(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MSkrivut(([]byte)("]"))

	PortSkrivord(registeraddressport, 20)
	PortSkrivord(busKontrollregisterdataport, 0x102)

	PortSkrivord(registeraddressport, 0)
	PortSkrivord(registerdataport, 0x04)

	initBlokk.modus = 0x0000
	initBlokk.tallsendbuffer = 3
	initBlokk.tallrecvbuffer = 3

	initBlokk.physicaladdress = Mac

	initBlokk.logicaladdress = 0

	sendbufferBeskrivelse = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendbufferBeskrivelseMinne)) + 15) & ^(uintptr)(0xF)))
	initBlokk.sendbufferBeskrivelseaddress = uintptr(Pointer(&sendbufferBeskrivelse))
	recvbufferBeskrivelse = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferBeskrivelseMinne)) + 15) & ^(uintptr)(0xF)))
	initBlokk.recvbufferBeskrivelseaddress = uintptr(Pointer(&recvbufferBeskrivelse))

	for i := 0; i < 8; i++ {
		sendbufferBeskrivelse[i].address_2 = uint32((uintptr(Pointer(&sendbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendbufferBeskrivelse[i].flagg = 0x7FF | 0xF000
		sendbufferBeskrivelse[i].flagg2 = 0
		sendbufferBeskrivelse[i].tilgjengelig = 0

		recvbufferBeskrivelse[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferBeskrivelse[i].flagg = 0xF7FF | 0x80000000

	}

	PortSkrivord(registeraddressport, 1)
	PortSkrivord(registerdataport, uint16(uintptr(Pointer(&initBlokk))&0xFFFF))

	PortSkrivord(registeraddressport, 2)
	PortSkrivord(registerdataport, uint16((uintptr(Pointer(&initBlokk))>>16)&0xFFFF))

}
func (selv *Tamdam79c973) Aktiver() {
	PortSkrivord(registeraddressport, 0)
	PortSkrivord(registerdataport, 0x41)

	PortSkrivord(registeraddressport, 4)
	temporary := PortLesord(registerdataport)
	PortSkrivord(registeraddressport, 4)
	PortSkrivord(registerdataport, temporary|0xC00)

	PortSkrivord(registeraddressport, 0)
	PortSkrivord(registerdataport, 0x42)

}
func (selv *Tamdam79c973) Nullstill() int {
	PortLesord(nullstillport)
	PortSkrivord(nullstillport, 0)
	return 10
}

var antall uint16 = 0

func (selv *Tamdam79c973) HåndtakAvbrudd(esp uint32) uint32 {

	PortSkrivord(registeraddressport, 0)
	temporary := uint32(PortLesord(registerdataport))
	console_2.MSkrivut(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Skrivut(esp)
	console_2.MSkrivut(([]byte)(":"))
	console_2.MUnsignedinteger32Skrivut(temporary)
	console_2.MSkrivut(([]byte)(":"))
	console_2.MUnsignedinteger16Skrivut(antall)
	antall++
	console_2.MSkrivut(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MSkrivut(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MSkrivut(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MSkrivut(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MSkrivut(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MSkrivut(([]byte)("am79c973 data received"))
		selv.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MSkrivut(([]byte)("am79c973 data sent"))
	}

	PortSkrivord(registeraddressport, 0)
	PortSkrivord(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MSkrivut(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (selv *Tamdam79c973) Send(dataPeker uintptr, størrelse uint32) {
	var senddescriptor uint16 = uint16(gjeldendesendbuffer)
	gjeldendesendbuffer = 0

	if størrelse > 1518 {
		størrelse = 1518
	}

	var kilde_2 [4096]byte = *(*([4096]byte))(Pointer(dataPeker))
	var mål_2 uint32 = sendbufferBeskrivelse[senddescriptor].address_2 + størrelse - 1

	for i := 0; i < int(størrelse); i++ {

		*(*byte)(Pointer(uintptr(mål_2))) = kilde_2[int(størrelse)-i-1]

		mål_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataPeker))
	console_2.MSkrivutxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalSkrivut(data[i])
		console_2.MSkrivut(([]byte)(":"))
	}
	console_2.MSkrivut(([]byte)("\n"))

	sendbufferBeskrivelse[senddescriptor].tilgjengelig = 0
	sendbufferBeskrivelse[senddescriptor].flagg2 = 0
	sendbufferBeskrivelse[senddescriptor].flagg = 0x8300F000 | uint32((-størrelse)&0xFFF)

	PortSkrivord(registeraddressport, 0)
	PortSkrivord(registerdataport, 0x48)

}
func (selv *Tamdam79c973) Receive() {
	console_2.MSkrivut(([]byte)(":"))
	console_2.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(&sendbuffer))))
	console_2.MSkrivut(([]byte)(":"))
	console_2.MHexadecimalSkrivut(sendbuffer[0][0])
	console_2.MHexadecimalSkrivut(sendbuffer[0][1])
	console_2.MSkrivut(([]byte)(":"))
	gjeldenderecvbuffer = 0

	for ; (recvbufferBeskrivelse[gjeldenderecvbuffer].flagg & 0x80000000) == 0; gjeldenderecvbuffer = (gjeldenderecvbuffer + 1) % 8 {

		if !(recvbufferBeskrivelse[gjeldenderecvbuffer].flagg&0x40000000 != 0) && ((recvbufferBeskrivelse[gjeldenderecvbuffer].flagg & 0x03000000) == 0x03000000) {
			var størrelse uint32 = recvbufferBeskrivelse[gjeldenderecvbuffer].flagg & 0xFFF
			if størrelse > 64 {
				størrelse -= 4
			}

			console_2.MSkrivut([]byte(" size : ["))
			console_2.MUnsignedinteger32Skrivut(størrelse)
			console_2.MSkrivut([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferBeskrivelse[gjeldenderecvbuffer].address_2)))
			var peker uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Pårawdatareceive(peker, int(størrelse)) {

					console_2.MSkrivutxy(([]byte)("self.Send"), 0, 22)

					selv.Send(peker, størrelse)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalSkrivut(buffer_2[i])
				console_2.MSkrivut([]byte(":"))
			}

		}
		recvbufferBeskrivelse[gjeldenderecvbuffer].flagg2 = 0
		recvbufferBeskrivelse[gjeldenderecvbuffer].flagg = 0x8000F7FF
	}
}
func (selv *Tamdam79c973) Setthandler(handler *TRawdatahandler) {
	selv.handler = handler
}
func (selv *Tamdam79c973) Getmacaddress() uint64 {

	return initBlokk.physicaladdress
}
func (selv *Tamdam79c973) Settipaddress(ip uint64) {
	initBlokk.logicaladdress = ip
}
func (selv *Tamdam79c973) Getipaddress() uint64 {
	return initBlokk.logicaladdress
}
