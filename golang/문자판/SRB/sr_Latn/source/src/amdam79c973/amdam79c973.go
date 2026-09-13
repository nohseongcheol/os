package amdam79c973

import . "unsafe"
import . "ometanje"
import . "konzola"
import . "port"
import . "pci"

var mrežacardKonzola TKonzola = TKonzola{}

type TInitializationBlok struct {
	rEŽIM			uint16
	brojPošaljibuffer	uint8
	brojrecvbuffer		uint8

	physicaladdress	uint64

	logicaladdress		uint64
	recvbufferOpisaddress	uintptr
	pošaljibufferOpisaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	parametri	uint32
	parametri2	uint32
	raspoloživo	uint32
}

type IRawdatahandler interface {
	Narawdatareceive(dataPokazivač uintptr, veličina int) bool
	Pošalji(dataPokazivač uintptr, veličina uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (isti *TRawdatahandler) Skupbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (isti *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (isti *TRawdatahandler) Narawdatareceive(dataPokazivač uintptr, veličina int) bool {
	mrežacardKonzola.MŠtampajxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (isti *TRawdatahandler) Pošalji(dataPokazivač uintptr, veličina uint32) {
	mrežacardKonzola.MŠtampajxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Pošalji(dataPokazivač, veličina)
}

var Macaddress0Port uint16
var Macaddress2Port uint16
var Macaddress4Port uint16
var registerdataPort uint16
var registeraddressPort uint16
var ponovopostaviPort uint16
var busKontrolregisterdataPort uint16

var initBlok TInitializationBlok

var pošaljibufferOpis [8]TBufferdescriptor
var pošaljibufferOpisMemorija [2048 + 15]byte
var pošaljibuffer [2*1024 + 15][8]uint8
var trenutnoPošaljibuffer uint8

var recvbufferOpis [8]TBufferdescriptor
var recvbufferOpisMemorija [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var trenutnorecvbuffer uint8
var funcVrednost func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TOmetanjehandler
	uređajdescriptor	TPeripheralcomponentinterconnectUređajdescriptor
	ometanje			*TOmetanjemanager
	handler			*TRawdatahandler
}

var konzola_2 TKonzola = TKonzola{}
var irawdatahandler IRawdatahandler

func (isti *Tamdam79c973) Initdriver(ometanje *TOmetanjemanager, uređajdescriptor TPeripheralcomponentinterconnectUređajdescriptor, handler IRawdatahandler) {

	isti.uređajdescriptor = uređajdescriptor

	funcVrednost = (*Tamdam79c973).RučkaOmetanje
	var address uintptr
	address = uintptr(Pointer(&funcVrednost))

	isti.Init(uint8(0x20+uređajdescriptor.Ometanje), uintptr(Pointer(ometanje)), address)

	Macaddress0Port = uint16(uređajdescriptor.Portbase)
	Macaddress2Port = uint16(uređajdescriptor.Portbase) + 0x02
	Macaddress4Port = uint16(uređajdescriptor.Portbase) + 0x04
	registerdataPort = uint16(uređajdescriptor.Portbase) + 0x10
	registeraddressPort = uint16(uređajdescriptor.Portbase) + 0x12
	ponovopostaviPort = uint16(uređajdescriptor.Portbase) + 0x14
	busKontrolregisterdataPort = uint16(uređajdescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	trenutnoPošaljibuffer = 0
	trenutnorecvbuffer = 0

	var Mac0 uint64 = uint64(Portčitanjereč(Macaddress0Port) % 256)
	var Mac1 uint64 = uint64(Portčitanjereč(Macaddress0Port) / 256)
	var Mac2 uint64 = uint64(Portčitanjereč(Macaddress2Port) % 256)
	var Mac3 uint64 = uint64(Portčitanjereč(Macaddress2Port) / 256)
	var Mac4 uint64 = uint64(Portčitanjereč(Macaddress4Port) % 256)
	var Mac5 uint64 = uint64(Portčitanjereč(Macaddress4Port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konzola_2.MŠtampajxy(([]byte)("[interrupt num : "), 0, 13)
	konzola_2.MHexadecimalŠtampaj(uint8(uređajdescriptor.Ometanje))
	konzola_2.MŠtampaj(([]byte)("]"))
	konzola_2.MŠtampaj(([]byte)("[mac address : "))
	konzola_2.MUnsignedinteger16Štampaj(uint16(macaddress >> 32))
	konzola_2.MUnsignedinteger32Štampaj(uint32(macaddress & 0x00000000FFFFFFFF))
	konzola_2.MŠtampaj(([]byte)("]"))

	PortPišereč(registeraddressPort, 20)
	PortPišereč(busKontrolregisterdataPort, 0x102)

	PortPišereč(registeraddressPort, 0)
	PortPišereč(registerdataPort, 0x04)

	initBlok.rEŽIM = 0x0000
	initBlok.brojPošaljibuffer = 3
	initBlok.brojrecvbuffer = 3

	initBlok.physicaladdress = Mac

	initBlok.logicaladdress = 0

	pošaljibufferOpis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&pošaljibufferOpisMemorija)) + 15) & ^(uintptr)(0xF)))
	initBlok.pošaljibufferOpisaddress = uintptr(Pointer(&pošaljibufferOpis))
	recvbufferOpis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferOpisMemorija)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferOpisaddress = uintptr(Pointer(&recvbufferOpis))

	for i := 0; i < 8; i++ {
		pošaljibufferOpis[i].address_2 = uint32((uintptr(Pointer(&pošaljibuffer[i])) + 15) & ^(uintptr(0xF)))
		pošaljibufferOpis[i].parametri = 0x7FF | 0xF000
		pošaljibufferOpis[i].parametri2 = 0
		pošaljibufferOpis[i].raspoloživo = 0

		recvbufferOpis[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferOpis[i].parametri = 0xF7FF | 0x80000000

	}

	PortPišereč(registeraddressPort, 1)
	PortPišereč(registerdataPort, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	PortPišereč(registeraddressPort, 2)
	PortPišereč(registerdataPort, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (isti *Tamdam79c973) Pokreni() {
	PortPišereč(registeraddressPort, 0)
	PortPišereč(registerdataPort, 0x41)

	PortPišereč(registeraddressPort, 4)
	temporary := Portčitanjereč(registerdataPort)
	PortPišereč(registeraddressPort, 4)
	PortPišereč(registerdataPort, temporary|0xC00)

	PortPišereč(registeraddressPort, 0)
	PortPišereč(registerdataPort, 0x42)

}
func (isti *Tamdam79c973) Ponovopostavi() int {
	Portčitanjereč(ponovopostaviPort)
	PortPišereč(ponovopostaviPort, 0)
	return 10
}

var count uint16 = 0

func (isti *Tamdam79c973) RučkaOmetanje(esp uint32) uint32 {

	PortPišereč(registeraddressPort, 0)
	temporary := uint32(Portčitanjereč(registerdataPort))
	konzola_2.MŠtampaj(([]byte)("interrupt("))
	konzola_2.MUnsignedinteger32Štampaj(esp)
	konzola_2.MŠtampaj(([]byte)(":"))
	konzola_2.MUnsignedinteger32Štampaj(temporary)
	konzola_2.MŠtampaj(([]byte)(":"))
	konzola_2.MUnsignedinteger16Štampaj(count)
	count++
	konzola_2.MŠtampaj(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konzola_2.MŠtampaj(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konzola_2.MŠtampaj(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konzola_2.MŠtampaj(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konzola_2.MŠtampaj(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konzola_2.MŠtampaj(([]byte)("am79c973 data received"))
		isti.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konzola_2.MŠtampaj(([]byte)("am79c973 data sent"))
	}

	PortPišereč(registeraddressPort, 0)
	PortPišereč(registerdataPort, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konzola_2.MŠtampaj(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (isti *Tamdam79c973) Pošalji(dataPokazivač uintptr, veličina uint32) {
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
	konzola_2.MŠtampajxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konzola_2.MHexadecimalŠtampaj(data[i])
		konzola_2.MŠtampaj(([]byte)(":"))
	}
	konzola_2.MŠtampaj(([]byte)("\n"))

	pošaljibufferOpis[pošaljidescriptor].raspoloživo = 0
	pošaljibufferOpis[pošaljidescriptor].parametri2 = 0
	pošaljibufferOpis[pošaljidescriptor].parametri = 0x8300F000 | uint32((-veličina)&0xFFF)

	PortPišereč(registeraddressPort, 0)
	PortPišereč(registerdataPort, 0x48)

}
func (isti *Tamdam79c973) Receive() {
	konzola_2.MŠtampaj(([]byte)(":"))
	konzola_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(&pošaljibuffer))))
	konzola_2.MŠtampaj(([]byte)(":"))
	konzola_2.MHexadecimalŠtampaj(pošaljibuffer[0][0])
	konzola_2.MHexadecimalŠtampaj(pošaljibuffer[0][1])
	konzola_2.MŠtampaj(([]byte)(":"))
	trenutnorecvbuffer = 0

	for ; (recvbufferOpis[trenutnorecvbuffer].parametri & 0x80000000) == 0; trenutnorecvbuffer = (trenutnorecvbuffer + 1) % 8 {

		if !(recvbufferOpis[trenutnorecvbuffer].parametri&0x40000000 != 0) && ((recvbufferOpis[trenutnorecvbuffer].parametri & 0x03000000) == 0x03000000) {
			var veličina uint32 = recvbufferOpis[trenutnorecvbuffer].parametri & 0xFFF
			if veličina > 64 {
				veličina -= 4
			}

			konzola_2.MŠtampaj([]byte(" size : ["))
			konzola_2.MUnsignedinteger32Štampaj(veličina)
			konzola_2.MŠtampaj([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferOpis[trenutnorecvbuffer].address_2)))
			var pokazivač uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Narawdatareceive(pokazivač, int(veličina)) {

					konzola_2.MŠtampajxy(([]byte)("self.Send"), 0, 22)

					isti.Pošalji(pokazivač, veličina)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konzola_2.MHexadecimalŠtampaj(buffer_2[i])
				konzola_2.MŠtampaj([]byte(":"))
			}

		}
		recvbufferOpis[trenutnorecvbuffer].parametri2 = 0
		recvbufferOpis[trenutnorecvbuffer].parametri = 0x8000F7FF
	}
}
func (isti *Tamdam79c973) Skuphandler(handler *TRawdatahandler) {
	isti.handler = handler
}
func (isti *Tamdam79c973) Getmacaddress() uint64 {

	return initBlok.physicaladdress
}
func (isti *Tamdam79c973) Skupipaddress(ip uint64) {
	initBlok.logicaladdress = ip
}
func (isti *Tamdam79c973) Getipaddress() uint64 {
	return initBlok.logicaladdress
}
