package amdam79c973

import . "unsafe"
import . "unterbrechung"
import . "konsole"
import . "anschluss"
import . "pci"

var netzwerkKartenspieleKonsole TKonsole = TKonsole{}

type TInitializationRechteck struct {
	modus			uint16
	nummerSendenbuffer	uint8
	nummerrecvbuffer	uint8

	physischaddress	uint64

	logikaddress			uint64
	recvbufferBeschreibungaddress	uintptr
	sendenbufferBeschreibungaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	optionen	uint32
	optionen2	uint32
	verfügbar	uint32
}

type IRawDatenhandler interface {
	BeirawDatenreceive(datenZeiger uintptr, größe int) bool
	Senden(datenZeiger uintptr, größe uint32)
}

var rawDatenbackend Tamdam79c973

type TRawDatenhandler struct {
}

func (selbst *TRawDatenhandler) Setzenbackend(backend Tamdam79c973) {

	rawDatenbackend = backend
}
func (selbst *TRawDatenhandler) Getbackend() Tamdam79c973 {
	return rawDatenbackend
}
func (selbst *TRawDatenhandler) BeirawDatenreceive(datenZeiger uintptr, größe int) bool {
	netzwerkKartenspieleKonsole.MDruckenxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (selbst *TRawDatenhandler) Senden(datenZeiger uintptr, größe uint32) {
	netzwerkKartenspieleKonsole.MDruckenxy(([]byte)("TRawDataSend"), 10, 10)
	rawDatenbackend.Senden(datenZeiger, größe)
}

var Macaddress0Anschluss uint16
var Macaddress2Anschluss uint16
var Macaddress4Anschluss uint16
var registerDatenAnschluss uint16
var registeraddressAnschluss uint16
var zurücksetzenAnschluss uint16
var busStrgRegisterDatenAnschluss uint16

var initRechteck TInitializationRechteck

var sendenbufferBeschreibung [8]TBufferdescriptor
var sendenbufferBeschreibungSpeicher [2048 + 15]byte
var sendenbuffer [2*1024 + 15][8]uint8
var systemzeitSendenbuffer uint8

var recvbufferBeschreibung [8]TBufferdescriptor
var recvbufferBeschreibungSpeicher [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var systemzeitrecvbuffer uint8
var funcWert func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TUnterbrechunghandler
	gerätdescriptor	TPeripheralcomponentinterconnectGerätdescriptor
	unterbrechung	*TUnterbrechungVerwalter
	handler		*TRawDatenhandler
}

var konsole_2 TKonsole = TKonsole{}
var irawDatenhandler IRawDatenhandler

func (selbst *Tamdam79c973) InitTreiber(unterbrechung *TUnterbrechungVerwalter, gerätdescriptor TPeripheralcomponentinterconnectGerätdescriptor, handler IRawDatenhandler) {

	selbst.gerätdescriptor = gerätdescriptor

	funcWert = (*Tamdam79c973).GriffUnterbrechung
	var address uintptr
	address = uintptr(Pointer(&funcWert))

	selbst.Init(uint8(0x20+gerätdescriptor.Unterbrechung), uintptr(Pointer(unterbrechung)), address)

	Macaddress0Anschluss = uint16(gerätdescriptor.Anschlussbase)
	Macaddress2Anschluss = uint16(gerätdescriptor.Anschlussbase) + 0x02
	Macaddress4Anschluss = uint16(gerätdescriptor.Anschlussbase) + 0x04
	registerDatenAnschluss = uint16(gerätdescriptor.Anschlussbase) + 0x10
	registeraddressAnschluss = uint16(gerätdescriptor.Anschlussbase) + 0x12
	zurücksetzenAnschluss = uint16(gerätdescriptor.Anschlussbase) + 0x14
	busStrgRegisterDatenAnschluss = uint16(gerätdescriptor.Anschlussbase) + 0x16

	irawDatenhandler = &TRawDatenhandler{}
	if handler != nil {
		irawDatenhandler = handler
	}

	systemzeitSendenbuffer = 0
	systemzeitrecvbuffer = 0

	var Mac0 uint64 = uint64(AnschlussLesenWort(Macaddress0Anschluss) % 256)
	var Mac1 uint64 = uint64(AnschlussLesenWort(Macaddress0Anschluss) / 256)
	var Mac2 uint64 = uint64(AnschlussLesenWort(Macaddress2Anschluss) % 256)
	var Mac3 uint64 = uint64(AnschlussLesenWort(Macaddress2Anschluss) / 256)
	var Mac4 uint64 = uint64(AnschlussLesenWort(Macaddress4Anschluss) % 256)
	var Mac5 uint64 = uint64(AnschlussLesenWort(Macaddress4Anschluss) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konsole_2.MDruckenxy(([]byte)("[interrupt num : "), 0, 13)
	konsole_2.MHexadecimalDrucken(uint8(gerätdescriptor.Unterbrechung))
	konsole_2.MDrucken(([]byte)("]"))
	konsole_2.MDrucken(([]byte)("[mac address : "))
	konsole_2.MUnsignedinteger16Drucken(uint16(macaddress >> 32))
	konsole_2.MUnsignedinteger32Drucken(uint32(macaddress & 0x00000000FFFFFFFF))
	konsole_2.MDrucken(([]byte)("]"))

	AnschlussSchreibenWort(registeraddressAnschluss, 20)
	AnschlussSchreibenWort(busStrgRegisterDatenAnschluss, 0x102)

	AnschlussSchreibenWort(registeraddressAnschluss, 0)
	AnschlussSchreibenWort(registerDatenAnschluss, 0x04)

	initRechteck.modus = 0x0000
	initRechteck.nummerSendenbuffer = 3
	initRechteck.nummerrecvbuffer = 3

	initRechteck.physischaddress = Mac

	initRechteck.logikaddress = 0

	sendenbufferBeschreibung = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&sendenbufferBeschreibungSpeicher)) + 15) & ^(uintptr)(0xF)))
	initRechteck.sendenbufferBeschreibungaddress = uintptr(Pointer(&sendenbufferBeschreibung))
	recvbufferBeschreibung = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferBeschreibungSpeicher)) + 15) & ^(uintptr)(0xF)))
	initRechteck.recvbufferBeschreibungaddress = uintptr(Pointer(&recvbufferBeschreibung))

	for i := 0; i < 8; i++ {
		sendenbufferBeschreibung[i].address_2 = uint32((uintptr(Pointer(&sendenbuffer[i])) + 15) & ^(uintptr(0xF)))
		sendenbufferBeschreibung[i].optionen = 0x7FF | 0xF000
		sendenbufferBeschreibung[i].optionen2 = 0
		sendenbufferBeschreibung[i].verfügbar = 0

		recvbufferBeschreibung[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferBeschreibung[i].optionen = 0xF7FF | 0x80000000

	}

	AnschlussSchreibenWort(registeraddressAnschluss, 1)
	AnschlussSchreibenWort(registerDatenAnschluss, uint16(uintptr(Pointer(&initRechteck))&0xFFFF))

	AnschlussSchreibenWort(registeraddressAnschluss, 2)
	AnschlussSchreibenWort(registerDatenAnschluss, uint16((uintptr(Pointer(&initRechteck))>>16)&0xFFFF))

}
func (selbst *Tamdam79c973) Aktivieren() {
	AnschlussSchreibenWort(registeraddressAnschluss, 0)
	AnschlussSchreibenWort(registerDatenAnschluss, 0x41)

	AnschlussSchreibenWort(registeraddressAnschluss, 4)
	temporary := AnschlussLesenWort(registerDatenAnschluss)
	AnschlussSchreibenWort(registeraddressAnschluss, 4)
	AnschlussSchreibenWort(registerDatenAnschluss, temporary|0xC00)

	AnschlussSchreibenWort(registeraddressAnschluss, 0)
	AnschlussSchreibenWort(registerDatenAnschluss, 0x42)

}
func (selbst *Tamdam79c973) Zurücksetzen() int {
	AnschlussLesenWort(zurücksetzenAnschluss)
	AnschlussSchreibenWort(zurücksetzenAnschluss, 0)
	return 10
}

var anzahl uint16 = 0

func (selbst *Tamdam79c973) GriffUnterbrechung(esp uint32) uint32 {

	AnschlussSchreibenWort(registeraddressAnschluss, 0)
	temporary := uint32(AnschlussLesenWort(registerDatenAnschluss))
	konsole_2.MDrucken(([]byte)("interrupt("))
	konsole_2.MUnsignedinteger32Drucken(esp)
	konsole_2.MDrucken(([]byte)(":"))
	konsole_2.MUnsignedinteger32Drucken(temporary)
	konsole_2.MDrucken(([]byte)(":"))
	konsole_2.MUnsignedinteger16Drucken(anzahl)
	anzahl++
	konsole_2.MDrucken(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konsole_2.MDrucken(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konsole_2.MDrucken(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konsole_2.MDrucken(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konsole_2.MDrucken(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konsole_2.MDrucken(([]byte)("am79c973 data received"))
		selbst.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konsole_2.MDrucken(([]byte)("am79c973 data sent"))
	}

	AnschlussSchreibenWort(registeraddressAnschluss, 0)
	AnschlussSchreibenWort(registerDatenAnschluss, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konsole_2.MDrucken(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (selbst *Tamdam79c973) Senden(datenZeiger uintptr, größe uint32) {
	var sendendescriptor uint16 = uint16(systemzeitSendenbuffer)
	systemzeitSendenbuffer = 0

	if größe > 1518 {
		größe = 1518
	}

	var quelle_2 [4096]byte = *(*([4096]byte))(Pointer(datenZeiger))
	var ziel_2 uint32 = sendenbufferBeschreibung[sendendescriptor].address_2 + größe - 1

	for i := 0; i < int(größe); i++ {

		*(*byte)(Pointer(uintptr(ziel_2))) = quelle_2[int(größe)-i-1]

		ziel_2--
	}

	var daten [4096]byte = *(*([4096]byte))(Pointer(datenZeiger))
	konsole_2.MDruckenxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konsole_2.MHexadecimalDrucken(daten[i])
		konsole_2.MDrucken(([]byte)(":"))
	}
	konsole_2.MDrucken(([]byte)("\n"))

	sendenbufferBeschreibung[sendendescriptor].verfügbar = 0
	sendenbufferBeschreibung[sendendescriptor].optionen2 = 0
	sendenbufferBeschreibung[sendendescriptor].optionen = 0x8300F000 | uint32((-größe)&0xFFF)

	AnschlussSchreibenWort(registeraddressAnschluss, 0)
	AnschlussSchreibenWort(registerDatenAnschluss, 0x48)

}
func (selbst *Tamdam79c973) Receive() {
	konsole_2.MDrucken(([]byte)(":"))
	konsole_2.MUnsignedinteger32Drucken(uint32(uintptr(Pointer(&sendenbuffer))))
	konsole_2.MDrucken(([]byte)(":"))
	konsole_2.MHexadecimalDrucken(sendenbuffer[0][0])
	konsole_2.MHexadecimalDrucken(sendenbuffer[0][1])
	konsole_2.MDrucken(([]byte)(":"))
	systemzeitrecvbuffer = 0

	for ; (recvbufferBeschreibung[systemzeitrecvbuffer].optionen & 0x80000000) == 0; systemzeitrecvbuffer = (systemzeitrecvbuffer + 1) % 8 {

		if !(recvbufferBeschreibung[systemzeitrecvbuffer].optionen&0x40000000 != 0) && ((recvbufferBeschreibung[systemzeitrecvbuffer].optionen & 0x03000000) == 0x03000000) {
			var größe uint32 = recvbufferBeschreibung[systemzeitrecvbuffer].optionen & 0xFFF
			if größe > 64 {
				größe -= 4
			}

			konsole_2.MDrucken([]byte(" size : ["))
			konsole_2.MUnsignedinteger32Drucken(größe)
			konsole_2.MDrucken([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferBeschreibung[systemzeitrecvbuffer].address_2)))
			var adressverweis uintptr = uintptr(Pointer(&buffer_2))
			if irawDatenhandler != nil {
				if irawDatenhandler.BeirawDatenreceive(adressverweis, int(größe)) {

					konsole_2.MDruckenxy(([]byte)("self.Send"), 0, 22)

					selbst.Senden(adressverweis, größe)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konsole_2.MHexadecimalDrucken(buffer_2[i])
				konsole_2.MDrucken([]byte(":"))
			}

		}
		recvbufferBeschreibung[systemzeitrecvbuffer].optionen2 = 0
		recvbufferBeschreibung[systemzeitrecvbuffer].optionen = 0x8000F7FF
	}
}
func (selbst *Tamdam79c973) Setzenhandler(handler *TRawDatenhandler) {
	selbst.handler = handler
}
func (selbst *Tamdam79c973) Getmacaddress() uint64 {

	return initRechteck.physischaddress
}
func (selbst *Tamdam79c973) Setzenipaddress(ip uint64) {
	initRechteck.logikaddress = ip
}
func (selbst *Tamdam79c973) Getipaddress() uint64 {
	return initRechteck.logikaddress
}
