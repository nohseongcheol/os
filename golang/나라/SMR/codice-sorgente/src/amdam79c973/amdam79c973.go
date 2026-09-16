/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "interrupt"
import . "console"
import . "porta"
import . "pci"

var reteCarteconsole TConsole = TConsole{}

type TInitializationBlocco struct {
	mODO			uint16
	numeroSpediscibuffer	uint8
	numerorecvbuffer	uint8

	physicaladdress	uint64

	logicoaddress				uint64
	recvbufferDescrizioneaddress		uintptr
	spediscibufferDescrizioneaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	flag		uint32
	flag2		uint32
	disponibile	uint32
}

type IRawdatahandler interface {
	Accesorawdatareceive(dataPuntatore uintptr, dimensione int) bool
	Spedisci(dataPuntatore uintptr, dimensione uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (séstesso *TRawdatahandler) Impostabackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (séstesso *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (séstesso *TRawdatahandler) Accesorawdatareceive(dataPuntatore uintptr, dimensione int) bool {
	reteCarteconsole.MStampaxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (séstesso *TRawdatahandler) Spedisci(dataPuntatore uintptr, dimensione uint32) {
	reteCarteconsole.MStampaxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Spedisci(dataPuntatore, dimensione)
}

var Macaddress0Porta uint16
var Macaddress2Porta uint16
var Macaddress4Porta uint16
var registerdataPorta uint16
var registeraddressPorta uint16
var ripristinaPorta uint16
var busCtrlregisterdataPorta uint16

var initBlocco TInitializationBlocco

var spediscibufferDescrizione [8]TBufferdescriptor
var spediscibufferDescrizioneMemoria [2048 + 15]byte
var spediscibuffer [2*1024 + 15][8]uint8
var correnteSpediscibuffer uint8

var recvbufferDescrizione [8]TBufferdescriptor
var recvbufferDescrizioneMemoria [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var correnterecvbuffer uint8
var funcValore func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupthandler
	dispositivodescriptor	TPeripheralcomponentinterconnectDispositivodescriptor
	interrupt		*TInterruptmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (séstesso *Tamdam79c973) Initdriver(interrupt *TInterruptmanager, dispositivodescriptor TPeripheralcomponentinterconnectDispositivodescriptor, handler IRawdatahandler) {

	séstesso.dispositivodescriptor = dispositivodescriptor

	funcValore = (*Tamdam79c973).Manigliainterrupt
	var address uintptr
	address = uintptr(Pointer(&funcValore))

	séstesso.Init(uint8(0x20+dispositivodescriptor.Interrupt), uintptr(Pointer(interrupt)), address)

	Macaddress0Porta = uint16(dispositivodescriptor.Portabase)
	Macaddress2Porta = uint16(dispositivodescriptor.Portabase) + 0x02
	Macaddress4Porta = uint16(dispositivodescriptor.Portabase) + 0x04
	registerdataPorta = uint16(dispositivodescriptor.Portabase) + 0x10
	registeraddressPorta = uint16(dispositivodescriptor.Portabase) + 0x12
	ripristinaPorta = uint16(dispositivodescriptor.Portabase) + 0x14
	busCtrlregisterdataPorta = uint16(dispositivodescriptor.Portabase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	correnteSpediscibuffer = 0
	correnterecvbuffer = 0

	var Mac0 uint64 = uint64(PortaLetturaparola(Macaddress0Porta) % 256)
	var Mac1 uint64 = uint64(PortaLetturaparola(Macaddress0Porta) / 256)
	var Mac2 uint64 = uint64(PortaLetturaparola(Macaddress2Porta) % 256)
	var Mac3 uint64 = uint64(PortaLetturaparola(Macaddress2Porta) / 256)
	var Mac4 uint64 = uint64(PortaLetturaparola(Macaddress4Porta) % 256)
	var Mac5 uint64 = uint64(PortaLetturaparola(Macaddress4Porta) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MStampaxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalStampa(uint8(dispositivodescriptor.Interrupt))
	console_2.MStampa(([]byte)("]"))
	console_2.MStampa(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Stampa(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Stampa(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MStampa(([]byte)("]"))

	PortaScritturaparola(registeraddressPorta, 20)
	PortaScritturaparola(busCtrlregisterdataPorta, 0x102)

	PortaScritturaparola(registeraddressPorta, 0)
	PortaScritturaparola(registerdataPorta, 0x04)

	initBlocco.mODO = 0x0000
	initBlocco.numeroSpediscibuffer = 3
	initBlocco.numerorecvbuffer = 3

	initBlocco.physicaladdress = Mac

	initBlocco.logicoaddress = 0

	spediscibufferDescrizione = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&spediscibufferDescrizioneMemoria)) + 15) & ^(uintptr)(0xF)))
	initBlocco.spediscibufferDescrizioneaddress = uintptr(Pointer(&spediscibufferDescrizione))
	recvbufferDescrizione = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferDescrizioneMemoria)) + 15) & ^(uintptr)(0xF)))
	initBlocco.recvbufferDescrizioneaddress = uintptr(Pointer(&recvbufferDescrizione))

	for i := 0; i < 8; i++ {
		spediscibufferDescrizione[i].address_2 = uint32((uintptr(Pointer(&spediscibuffer[i])) + 15) & ^(uintptr(0xF)))
		spediscibufferDescrizione[i].flag = 0x7FF | 0xF000
		spediscibufferDescrizione[i].flag2 = 0
		spediscibufferDescrizione[i].disponibile = 0

		recvbufferDescrizione[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferDescrizione[i].flag = 0xF7FF | 0x80000000

	}

	PortaScritturaparola(registeraddressPorta, 1)
	PortaScritturaparola(registerdataPorta, uint16(uintptr(Pointer(&initBlocco))&0xFFFF))

	PortaScritturaparola(registeraddressPorta, 2)
	PortaScritturaparola(registerdataPorta, uint16((uintptr(Pointer(&initBlocco))>>16)&0xFFFF))

}
func (séstesso *Tamdam79c973) Attiva() {
	PortaScritturaparola(registeraddressPorta, 0)
	PortaScritturaparola(registerdataPorta, 0x41)

	PortaScritturaparola(registeraddressPorta, 4)
	temporary := PortaLetturaparola(registerdataPorta)
	PortaScritturaparola(registeraddressPorta, 4)
	PortaScritturaparola(registerdataPorta, temporary|0xC00)

	PortaScritturaparola(registeraddressPorta, 0)
	PortaScritturaparola(registerdataPorta, 0x42)

}
func (séstesso *Tamdam79c973) Ripristina() int {
	PortaLetturaparola(ripristinaPorta)
	PortaScritturaparola(ripristinaPorta, 0)
	return 10
}

var conteggio uint16 = 0

func (séstesso *Tamdam79c973) Manigliainterrupt(esp uint32) uint32 {

	PortaScritturaparola(registeraddressPorta, 0)
	temporary := uint32(PortaLetturaparola(registerdataPorta))
	console_2.MStampa(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Stampa(esp)
	console_2.MStampa(([]byte)(":"))
	console_2.MUnsignedinteger32Stampa(temporary)
	console_2.MStampa(([]byte)(":"))
	console_2.MUnsignedinteger16Stampa(conteggio)
	conteggio++
	console_2.MStampa(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MStampa(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MStampa(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MStampa(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MStampa(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MStampa(([]byte)("am79c973 data received"))
		séstesso.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MStampa(([]byte)("am79c973 data sent"))
	}

	PortaScritturaparola(registeraddressPorta, 0)
	PortaScritturaparola(registerdataPorta, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MStampa(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (séstesso *Tamdam79c973) Spedisci(dataPuntatore uintptr, dimensione uint32) {
	var spediscidescriptor uint16 = uint16(correnteSpediscibuffer)
	correnteSpediscibuffer = 0

	if dimensione > 1518 {
		dimensione = 1518
	}

	var origine_2 [4096]byte = *(*([4096]byte))(Pointer(dataPuntatore))
	var destinazione_2 uint32 = spediscibufferDescrizione[spediscidescriptor].address_2 + dimensione - 1

	for i := 0; i < int(dimensione); i++ {

		*(*byte)(Pointer(uintptr(destinazione_2))) = origine_2[int(dimensione)-i-1]

		destinazione_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataPuntatore))
	console_2.MStampaxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalStampa(data[i])
		console_2.MStampa(([]byte)(":"))
	}
	console_2.MStampa(([]byte)("\n"))

	spediscibufferDescrizione[spediscidescriptor].disponibile = 0
	spediscibufferDescrizione[spediscidescriptor].flag2 = 0
	spediscibufferDescrizione[spediscidescriptor].flag = 0x8300F000 | uint32((-dimensione)&0xFFF)

	PortaScritturaparola(registeraddressPorta, 0)
	PortaScritturaparola(registerdataPorta, 0x48)

}
func (séstesso *Tamdam79c973) Receive() {
	console_2.MStampa(([]byte)(":"))
	console_2.MUnsignedinteger32Stampa(uint32(uintptr(Pointer(&spediscibuffer))))
	console_2.MStampa(([]byte)(":"))
	console_2.MHexadecimalStampa(spediscibuffer[0][0])
	console_2.MHexadecimalStampa(spediscibuffer[0][1])
	console_2.MStampa(([]byte)(":"))
	correnterecvbuffer = 0

	for ; (recvbufferDescrizione[correnterecvbuffer].flag & 0x80000000) == 0; correnterecvbuffer = (correnterecvbuffer + 1) % 8 {

		if !(recvbufferDescrizione[correnterecvbuffer].flag&0x40000000 != 0) && ((recvbufferDescrizione[correnterecvbuffer].flag & 0x03000000) == 0x03000000) {
			var dimensione uint32 = recvbufferDescrizione[correnterecvbuffer].flag & 0xFFF
			if dimensione > 64 {
				dimensione -= 4
			}

			console_2.MStampa([]byte(" size : ["))
			console_2.MUnsignedinteger32Stampa(dimensione)
			console_2.MStampa([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferDescrizione[correnterecvbuffer].address_2)))
			var riferimento_di_memoria uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Accesorawdatareceive(riferimento_di_memoria, int(dimensione)) {

					console_2.MStampaxy(([]byte)("self.Send"), 0, 22)

					séstesso.Spedisci(riferimento_di_memoria, dimensione)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalStampa(buffer_2[i])
				console_2.MStampa([]byte(":"))
			}

		}
		recvbufferDescrizione[correnterecvbuffer].flag2 = 0
		recvbufferDescrizione[correnterecvbuffer].flag = 0x8000F7FF
	}
}
func (séstesso *Tamdam79c973) Impostahandler(handler *TRawdatahandler) {
	séstesso.handler = handler
}
func (séstesso *Tamdam79c973) Getmacaddress() uint64 {

	return initBlocco.physicaladdress
}
func (séstesso *Tamdam79c973) Impostaipaddress(ip uint64) {
	initBlocco.logicoaddress = ip
}
func (séstesso *Tamdam79c973) Getipaddress() uint64 {
	return initBlocco.logicoaddress
}
