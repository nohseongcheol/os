package amdam79c973

import . "unsafe"
import . "avbrott"
import . "konsol"
import . "port"
import . "pci"

var nätverkKortspelKonsol TKonsol = TKonsol{}

type TInitializationblock struct {
	lÄGE			uint16
	nummerSkickabuffer	uint8
	nummerrecvbuffer	uint8

	physicalAdress	uint64

	logiskAdress			uint64
	recvbufferBeskrivningAdress	uintptr
	skickabufferBeskrivningAdress	uintptr
}
type TBufferdescriptor struct {
	adress_2	uint32
	flaggor		uint32
	flaggor2	uint32
	tillgängligt	uint32
}

type IRawdatahandler interface {
	Pårawdatareceive(dataMuspekare uintptr, storlek int) bool
	Skicka(dataMuspekare uintptr, storlek uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (själv *TRawdatahandler) Mängdbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (själv *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (själv *TRawdatahandler) Pårawdatareceive(dataMuspekare uintptr, storlek int) bool {
	nätverkKortspelKonsol.MSkrivutxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (själv *TRawdatahandler) Skicka(dataMuspekare uintptr, storlek uint32) {
	nätverkKortspelKonsol.MSkrivutxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Skicka(dataMuspekare, storlek)
}

var MacAdress0port uint16
var MacAdress2port uint16
var MacAdress4port uint16
var registerdataport uint16
var registerAdressport uint16
var återställport uint16
var busCtrlregisterdataport uint16

var initblock TInitializationblock

var skickabufferBeskrivning [8]TBufferdescriptor
var skickabufferBeskrivningMinne [2048 + 15]byte
var skickabuffer [2*1024 + 15][8]uint8
var aktuellSkickabuffer uint8

var recvbufferBeskrivning [8]TBufferdescriptor
var recvbufferBeskrivningMinne [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var aktuellrecvbuffer uint8
var funcVärde func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TAvbrotthandler
	enhetdescriptor	TPeripheralcomponentinterconnectEnhetdescriptor
	avbrott		*TAvbrottmanager
	handler		*TRawdatahandler
}

var konsol_2 TKonsol = TKonsol{}
var irawdatahandler IRawdatahandler

func (själv *Tamdam79c973) Initdriver(avbrott *TAvbrottmanager, enhetdescriptor TPeripheralcomponentinterconnectEnhetdescriptor, handler IRawdatahandler) {

	själv.enhetdescriptor = enhetdescriptor

	funcVärde = (*Tamdam79c973).HandtagAvbrott
	var adress uintptr
	adress = uintptr(Pointer(&funcVärde))

	själv.Init(uint8(0x20+enhetdescriptor.Avbrott), uintptr(Pointer(avbrott)), adress)

	MacAdress0port = uint16(enhetdescriptor.Portbase)
	MacAdress2port = uint16(enhetdescriptor.Portbase) + 0x02
	MacAdress4port = uint16(enhetdescriptor.Portbase) + 0x04
	registerdataport = uint16(enhetdescriptor.Portbase) + 0x10
	registerAdressport = uint16(enhetdescriptor.Portbase) + 0x12
	återställport = uint16(enhetdescriptor.Portbase) + 0x14
	busCtrlregisterdataport = uint16(enhetdescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	aktuellSkickabuffer = 0
	aktuellrecvbuffer = 0

	var Mac0 uint64 = uint64(PortLäsord(MacAdress0port) % 256)
	var Mac1 uint64 = uint64(PortLäsord(MacAdress0port) / 256)
	var Mac2 uint64 = uint64(PortLäsord(MacAdress2port) % 256)
	var Mac3 uint64 = uint64(PortLäsord(MacAdress2port) / 256)
	var Mac4 uint64 = uint64(PortLäsord(MacAdress4port) % 256)
	var Mac5 uint64 = uint64(PortLäsord(MacAdress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macAdress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konsol_2.MSkrivutxy(([]byte)("[interrupt num : "), 0, 13)
	konsol_2.MHexadecimalSkrivut(uint8(enhetdescriptor.Avbrott))
	konsol_2.MSkrivut(([]byte)("]"))
	konsol_2.MSkrivut(([]byte)("[mac address : "))
	konsol_2.MUnsignedinteger16Skrivut(uint16(macAdress >> 32))
	konsol_2.MUnsignedinteger32Skrivut(uint32(macAdress & 0x00000000FFFFFFFF))
	konsol_2.MSkrivut(([]byte)("]"))

	PortSkrivord(registerAdressport, 20)
	PortSkrivord(busCtrlregisterdataport, 0x102)

	PortSkrivord(registerAdressport, 0)
	PortSkrivord(registerdataport, 0x04)

	initblock.lÄGE = 0x0000
	initblock.nummerSkickabuffer = 3
	initblock.nummerrecvbuffer = 3

	initblock.physicalAdress = Mac

	initblock.logiskAdress = 0

	skickabufferBeskrivning = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&skickabufferBeskrivningMinne)) + 15) & ^(uintptr)(0xF)))
	initblock.skickabufferBeskrivningAdress = uintptr(Pointer(&skickabufferBeskrivning))
	recvbufferBeskrivning = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferBeskrivningMinne)) + 15) & ^(uintptr)(0xF)))
	initblock.recvbufferBeskrivningAdress = uintptr(Pointer(&recvbufferBeskrivning))

	for i := 0; i < 8; i++ {
		skickabufferBeskrivning[i].adress_2 = uint32((uintptr(Pointer(&skickabuffer[i])) + 15) & ^(uintptr(0xF)))
		skickabufferBeskrivning[i].flaggor = 0x7FF | 0xF000
		skickabufferBeskrivning[i].flaggor2 = 0
		skickabufferBeskrivning[i].tillgängligt = 0

		recvbufferBeskrivning[i].adress_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferBeskrivning[i].flaggor = 0xF7FF | 0x80000000

	}

	PortSkrivord(registerAdressport, 1)
	PortSkrivord(registerdataport, uint16(uintptr(Pointer(&initblock))&0xFFFF))

	PortSkrivord(registerAdressport, 2)
	PortSkrivord(registerdataport, uint16((uintptr(Pointer(&initblock))>>16)&0xFFFF))

}
func (själv *Tamdam79c973) Aktivera() {
	PortSkrivord(registerAdressport, 0)
	PortSkrivord(registerdataport, 0x41)

	PortSkrivord(registerAdressport, 4)
	temporary := PortLäsord(registerdataport)
	PortSkrivord(registerAdressport, 4)
	PortSkrivord(registerdataport, temporary|0xC00)

	PortSkrivord(registerAdressport, 0)
	PortSkrivord(registerdataport, 0x42)

}
func (själv *Tamdam79c973) Återställ() int {
	PortLäsord(återställport)
	PortSkrivord(återställport, 0)
	return 10
}

var antal uint16 = 0

func (själv *Tamdam79c973) HandtagAvbrott(esp uint32) uint32 {

	PortSkrivord(registerAdressport, 0)
	temporary := uint32(PortLäsord(registerdataport))
	konsol_2.MSkrivut(([]byte)("interrupt("))
	konsol_2.MUnsignedinteger32Skrivut(esp)
	konsol_2.MSkrivut(([]byte)(":"))
	konsol_2.MUnsignedinteger32Skrivut(temporary)
	konsol_2.MSkrivut(([]byte)(":"))
	konsol_2.MUnsignedinteger16Skrivut(antal)
	antal++
	konsol_2.MSkrivut(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konsol_2.MSkrivut(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konsol_2.MSkrivut(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konsol_2.MSkrivut(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konsol_2.MSkrivut(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konsol_2.MSkrivut(([]byte)("am79c973 data received"))
		själv.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konsol_2.MSkrivut(([]byte)("am79c973 data sent"))
	}

	PortSkrivord(registerAdressport, 0)
	PortSkrivord(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konsol_2.MSkrivut(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (själv *Tamdam79c973) Skicka(dataMuspekare uintptr, storlek uint32) {
	var skickadescriptor uint16 = uint16(aktuellSkickabuffer)
	aktuellSkickabuffer = 0

	if storlek > 1518 {
		storlek = 1518
	}

	var källa_2 [4096]byte = *(*([4096]byte))(Pointer(dataMuspekare))
	var mål_2 uint32 = skickabufferBeskrivning[skickadescriptor].adress_2 + storlek - 1

	for i := 0; i < int(storlek); i++ {

		*(*byte)(Pointer(uintptr(mål_2))) = källa_2[int(storlek)-i-1]

		mål_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataMuspekare))
	konsol_2.MSkrivutxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konsol_2.MHexadecimalSkrivut(data[i])
		konsol_2.MSkrivut(([]byte)(":"))
	}
	konsol_2.MSkrivut(([]byte)("\n"))

	skickabufferBeskrivning[skickadescriptor].tillgängligt = 0
	skickabufferBeskrivning[skickadescriptor].flaggor2 = 0
	skickabufferBeskrivning[skickadescriptor].flaggor = 0x8300F000 | uint32((-storlek)&0xFFF)

	PortSkrivord(registerAdressport, 0)
	PortSkrivord(registerdataport, 0x48)

}
func (själv *Tamdam79c973) Receive() {
	konsol_2.MSkrivut(([]byte)(":"))
	konsol_2.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(&skickabuffer))))
	konsol_2.MSkrivut(([]byte)(":"))
	konsol_2.MHexadecimalSkrivut(skickabuffer[0][0])
	konsol_2.MHexadecimalSkrivut(skickabuffer[0][1])
	konsol_2.MSkrivut(([]byte)(":"))
	aktuellrecvbuffer = 0

	for ; (recvbufferBeskrivning[aktuellrecvbuffer].flaggor & 0x80000000) == 0; aktuellrecvbuffer = (aktuellrecvbuffer + 1) % 8 {

		if !(recvbufferBeskrivning[aktuellrecvbuffer].flaggor&0x40000000 != 0) && ((recvbufferBeskrivning[aktuellrecvbuffer].flaggor & 0x03000000) == 0x03000000) {
			var storlek uint32 = recvbufferBeskrivning[aktuellrecvbuffer].flaggor & 0xFFF
			if storlek > 64 {
				storlek -= 4
			}

			konsol_2.MSkrivut([]byte(" size : ["))
			konsol_2.MUnsignedinteger32Skrivut(storlek)
			konsol_2.MSkrivut([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferBeskrivning[aktuellrecvbuffer].adress_2)))
			var adressreferens uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Pårawdatareceive(adressreferens, int(storlek)) {

					konsol_2.MSkrivutxy(([]byte)("self.Send"), 0, 22)

					själv.Skicka(adressreferens, storlek)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konsol_2.MHexadecimalSkrivut(buffer_2[i])
				konsol_2.MSkrivut([]byte(":"))
			}

		}
		recvbufferBeskrivning[aktuellrecvbuffer].flaggor2 = 0
		recvbufferBeskrivning[aktuellrecvbuffer].flaggor = 0x8000F7FF
	}
}
func (själv *Tamdam79c973) Mängdhandler(handler *TRawdatahandler) {
	själv.handler = handler
}
func (själv *Tamdam79c973) GetmacAdress() uint64 {

	return initblock.physicalAdress
}
func (själv *Tamdam79c973) MängdipAdress(ip uint64) {
	initblock.logiskAdress = ip
}
func (själv *Tamdam79c973) GetipAdress() uint64 {
	return initblock.logiskAdress
}
