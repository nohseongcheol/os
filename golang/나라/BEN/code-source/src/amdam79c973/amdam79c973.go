package amdam79c973

import . "unsafe"
import . "interruption"
import . "console"
import . "port"
import . "pci"

var réseauCartesconsole TConsole = TConsole{}

type TInitializationBloc struct {
	mode			uint16
	nombreEnvoyerbuffer	uint8
	nombrerecvbuffer	uint8

	physiqueaddress	uint64

	logiqueaddress			uint64
	recvbufferdescriptionaddress	uintptr
	envoyerbufferdescriptionaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	attributs_2	uint32
	attributs2	uint32
	disponible	uint32
}

type IRawdonnéeshandler interface {
	Surrawdonnéesreceive(donnéesPointeur uintptr, taille int) bool
	Envoyer(donnéesPointeur uintptr, taille uint32)
}

var rawdonnéesbackend Tamdam79c973

type TRawdonnéeshandler struct {
}

func (self *TRawdonnéeshandler) Ensemblebackend(backend Tamdam79c973) {

	rawdonnéesbackend = backend
}
func (self *TRawdonnéeshandler) Getbackend() Tamdam79c973 {
	return rawdonnéesbackend
}
func (self *TRawdonnéeshandler) Surrawdonnéesreceive(donnéesPointeur uintptr, taille int) bool {
	réseauCartesconsole.MImprimerxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdonnéeshandler) Envoyer(donnéesPointeur uintptr, taille uint32) {
	réseauCartesconsole.MImprimerxy(([]byte)("TRawDataSend"), 10, 10)
	rawdonnéesbackend.Envoyer(donnéesPointeur, taille)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registredonnéesport uint16
var registreaddressport uint16
var réinitialiserport uint16
var busCtrlregistredonnéesport uint16

var initBloc TInitializationBloc

var envoyerbufferdescription [8]TBufferdescriptor
var envoyerbufferdescriptionmémoire [2048 + 15]byte
var envoyerbuffer [2*1024 + 15][8]uint8
var couranteEnvoyerbuffer uint8

var recvbufferdescription [8]TBufferdescriptor
var recvbufferdescriptionmémoire [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var couranterecvbuffer uint8
var funcValeur func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterruptionhandler
	périphériquedescriptor	TPeripheralcomponentinterconnectPériphériquedescriptor
	interruption		*TInterruptiongestionnaire
	handler			*TRawdonnéeshandler
}

var console_2 TConsole = TConsole{}
var irawdonnéeshandler IRawdonnéeshandler

func (self *Tamdam79c973) Initpilote(interruption *TInterruptiongestionnaire, périphériquedescriptor TPeripheralcomponentinterconnectPériphériquedescriptor, handler IRawdonnéeshandler) {

	self.périphériquedescriptor = périphériquedescriptor

	funcValeur = (*Tamdam79c973).Poignéeinterruption
	var address uintptr
	address = uintptr(Pointer(&funcValeur))

	self.Init(uint8(0x20+périphériquedescriptor.Interruption), uintptr(Pointer(interruption)), address)

	Macaddress0port = uint16(périphériquedescriptor.Portbase)
	Macaddress2port = uint16(périphériquedescriptor.Portbase) + 0x02
	Macaddress4port = uint16(périphériquedescriptor.Portbase) + 0x04
	registredonnéesport = uint16(périphériquedescriptor.Portbase) + 0x10
	registreaddressport = uint16(périphériquedescriptor.Portbase) + 0x12
	réinitialiserport = uint16(périphériquedescriptor.Portbase) + 0x14
	busCtrlregistredonnéesport = uint16(périphériquedescriptor.Portbase) + 0x16

	irawdonnéeshandler = &TRawdonnéeshandler{}
	if handler != nil {
		irawdonnéeshandler = handler
	}

	couranteEnvoyerbuffer = 0
	couranterecvbuffer = 0

	var Mac0 uint64 = uint64(Portliremot(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(Portliremot(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(Portliremot(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(Portliremot(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(Portliremot(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(Portliremot(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MImprimerxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalImprimer(uint8(périphériquedescriptor.Interruption))
	console_2.MImprimer(([]byte)("]"))
	console_2.MImprimer(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Imprimer(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Imprimer(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MImprimer(([]byte)("]"))

	Portécriremot(registreaddressport, 20)
	Portécriremot(busCtrlregistredonnéesport, 0x102)

	Portécriremot(registreaddressport, 0)
	Portécriremot(registredonnéesport, 0x04)

	initBloc.mode = 0x0000
	initBloc.nombreEnvoyerbuffer = 3
	initBloc.nombrerecvbuffer = 3

	initBloc.physiqueaddress = Mac

	initBloc.logiqueaddress = 0

	envoyerbufferdescription = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&envoyerbufferdescriptionmémoire)) + 15) & ^(uintptr)(0xF)))
	initBloc.envoyerbufferdescriptionaddress = uintptr(Pointer(&envoyerbufferdescription))
	recvbufferdescription = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferdescriptionmémoire)) + 15) & ^(uintptr)(0xF)))
	initBloc.recvbufferdescriptionaddress = uintptr(Pointer(&recvbufferdescription))

	for i := 0; i < 8; i++ {
		envoyerbufferdescription[i].address_2 = uint32((uintptr(Pointer(&envoyerbuffer[i])) + 15) & ^(uintptr(0xF)))
		envoyerbufferdescription[i].attributs_2 = 0x7FF | 0xF000
		envoyerbufferdescription[i].attributs2 = 0
		envoyerbufferdescription[i].disponible = 0

		recvbufferdescription[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferdescription[i].attributs_2 = 0xF7FF | 0x80000000

	}

	Portécriremot(registreaddressport, 1)
	Portécriremot(registredonnéesport, uint16(uintptr(Pointer(&initBloc))&0xFFFF))

	Portécriremot(registreaddressport, 2)
	Portécriremot(registredonnéesport, uint16((uintptr(Pointer(&initBloc))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Activer() {
	Portécriremot(registreaddressport, 0)
	Portécriremot(registredonnéesport, 0x41)

	Portécriremot(registreaddressport, 4)
	temporary := Portliremot(registredonnéesport)
	Portécriremot(registreaddressport, 4)
	Portécriremot(registredonnéesport, temporary|0xC00)

	Portécriremot(registreaddressport, 0)
	Portécriremot(registredonnéesport, 0x42)

}
func (self *Tamdam79c973) Réinitialiser() int {
	Portliremot(réinitialiserport)
	Portécriremot(réinitialiserport, 0)
	return 10
}

var nombre uint16 = 0

func (self *Tamdam79c973) Poignéeinterruption(esp uint32) uint32 {

	Portécriremot(registreaddressport, 0)
	temporary := uint32(Portliremot(registredonnéesport))
	console_2.MImprimer(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Imprimer(esp)
	console_2.MImprimer(([]byte)(":"))
	console_2.MUnsignedinteger32Imprimer(temporary)
	console_2.MImprimer(([]byte)(":"))
	console_2.MUnsignedinteger16Imprimer(nombre)
	nombre++
	console_2.MImprimer(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MImprimer(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MImprimer(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MImprimer(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MImprimer(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MImprimer(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MImprimer(([]byte)("am79c973 data sent"))
	}

	Portécriremot(registreaddressport, 0)
	Portécriremot(registredonnéesport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MImprimer(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Envoyer(donnéesPointeur uintptr, taille uint32) {
	var envoyerdescriptor uint16 = uint16(couranteEnvoyerbuffer)
	couranteEnvoyerbuffer = 0

	if taille > 1518 {
		taille = 1518
	}

	var source_2 [4096]byte = *(*([4096]byte))(Pointer(donnéesPointeur))
	var destination_2 uint32 = envoyerbufferdescription[envoyerdescriptor].address_2 + taille - 1

	for i := 0; i < int(taille); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = source_2[int(taille)-i-1]

		destination_2--
	}

	var données [4096]byte = *(*([4096]byte))(Pointer(donnéesPointeur))
	console_2.MImprimerxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalImprimer(données[i])
		console_2.MImprimer(([]byte)(":"))
	}
	console_2.MImprimer(([]byte)("\n"))

	envoyerbufferdescription[envoyerdescriptor].disponible = 0
	envoyerbufferdescription[envoyerdescriptor].attributs2 = 0
	envoyerbufferdescription[envoyerdescriptor].attributs_2 = 0x8300F000 | uint32((-taille)&0xFFF)

	Portécriremot(registreaddressport, 0)
	Portécriremot(registredonnéesport, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MImprimer(([]byte)(":"))
	console_2.MUnsignedinteger32Imprimer(uint32(uintptr(Pointer(&envoyerbuffer))))
	console_2.MImprimer(([]byte)(":"))
	console_2.MHexadecimalImprimer(envoyerbuffer[0][0])
	console_2.MHexadecimalImprimer(envoyerbuffer[0][1])
	console_2.MImprimer(([]byte)(":"))
	couranterecvbuffer = 0

	for ; (recvbufferdescription[couranterecvbuffer].attributs_2 & 0x80000000) == 0; couranterecvbuffer = (couranterecvbuffer + 1) % 8 {

		if !(recvbufferdescription[couranterecvbuffer].attributs_2&0x40000000 != 0) && ((recvbufferdescription[couranterecvbuffer].attributs_2 & 0x03000000) == 0x03000000) {
			var taille uint32 = recvbufferdescription[couranterecvbuffer].attributs_2 & 0xFFF
			if taille > 64 {
				taille -= 4
			}

			console_2.MImprimer([]byte(" size : ["))
			console_2.MUnsignedinteger32Imprimer(taille)
			console_2.MImprimer([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferdescription[couranterecvbuffer].address_2)))
			var référence_mémoire uintptr = uintptr(Pointer(&buffer_2))
			if irawdonnéeshandler != nil {
				if irawdonnéeshandler.Surrawdonnéesreceive(référence_mémoire, int(taille)) {

					console_2.MImprimerxy(([]byte)("self.Send"), 0, 22)

					self.Envoyer(référence_mémoire, taille)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalImprimer(buffer_2[i])
				console_2.MImprimer([]byte(":"))
			}

		}
		recvbufferdescription[couranterecvbuffer].attributs2 = 0
		recvbufferdescription[couranterecvbuffer].attributs_2 = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Ensemblehandler(handler *TRawdonnéeshandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initBloc.physiqueaddress
}
func (self *Tamdam79c973) Ensembleipaddress(ip uint64) {
	initBloc.logiqueaddress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initBloc.logiqueaddress
}
