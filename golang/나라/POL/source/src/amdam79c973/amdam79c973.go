package amdam79c973

import . "unsafe"
import . "przerwanie"
import . "konsola"
import . "port"
import . "pci"

var siećKarcianeKonsola TKonsola = TKonsola{}

type TInitializationBlok struct {
	tRYB			uint16
	liczbaWyślijbuffer	uint8
	liczbarecvbuffer	uint8

	physicalAdres	uint64

	logiczneAdres		uint64
	recvbufferOpisAdres	uintptr
	wyślijbufferOpisAdres	uintptr
}
type TBufferdescriptor struct {
	adres_2		uint32
	znaczniki	uint32
	znaczniki2	uint32
	dostępne	uint32
}

type IRawdatahandler interface {
	Włączrawdatareceive(dataKursor uintptr, rozmiar int) bool
	Wyślij(dataKursor uintptr, rozmiar uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (bieżący *TRawdatahandler) Zbiórbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (bieżący *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (bieżący *TRawdatahandler) Włączrawdatareceive(dataKursor uintptr, rozmiar int) bool {
	siećKarcianeKonsola.MWydrukujxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (bieżący *TRawdatahandler) Wyślij(dataKursor uintptr, rozmiar uint32) {
	siećKarcianeKonsola.MWydrukujxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Wyślij(dataKursor, rozmiar)
}

var MacAdres0port uint16
var MacAdres2port uint16
var MacAdres4port uint16
var registerdataport uint16
var registerAdresport uint16
var wyzerujport uint16
var busSterowanieregisterdataport uint16

var initBlok TInitializationBlok

var wyślijbufferOpis [8]TBufferdescriptor
var wyślijbufferOpisPamięć [2048 + 15]byte
var wyślijbuffer [2*1024 + 15][8]uint8
var bieżącyWyślijbuffer uint8

var recvbufferOpis [8]TBufferdescriptor
var recvbufferOpisPamięć [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var bieżącyrecvbuffer uint8
var funcWartość func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TPrzerwaniehandler
	urządzeniedescriptor	TPeripheralcomponentinterconnectUrządzeniedescriptor
	przerwanie		*TPrzerwaniemanager
	handler			*TRawdatahandler
}

var konsola_2 TKonsola = TKonsola{}
var irawdatahandler IRawdatahandler

func (bieżący *Tamdam79c973) Initdriver(przerwanie *TPrzerwaniemanager, urządzeniedescriptor TPeripheralcomponentinterconnectUrządzeniedescriptor, handler IRawdatahandler) {

	bieżący.urządzeniedescriptor = urządzeniedescriptor

	funcWartość = (*Tamdam79c973).UchwytPrzerwanie
	var adres uintptr
	adres = uintptr(Pointer(&funcWartość))

	bieżący.Init(uint8(0x20+urządzeniedescriptor.Przerwanie), uintptr(Pointer(przerwanie)), adres)

	MacAdres0port = uint16(urządzeniedescriptor.Portbase)
	MacAdres2port = uint16(urządzeniedescriptor.Portbase) + 0x02
	MacAdres4port = uint16(urządzeniedescriptor.Portbase) + 0x04
	registerdataport = uint16(urządzeniedescriptor.Portbase) + 0x10
	registerAdresport = uint16(urządzeniedescriptor.Portbase) + 0x12
	wyzerujport = uint16(urządzeniedescriptor.Portbase) + 0x14
	busSterowanieregisterdataport = uint16(urządzeniedescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	bieżącyWyślijbuffer = 0
	bieżącyrecvbuffer = 0

	var Mac0 uint64 = uint64(PortOdczytsłowo(MacAdres0port) % 256)
	var Mac1 uint64 = uint64(PortOdczytsłowo(MacAdres0port) / 256)
	var Mac2 uint64 = uint64(PortOdczytsłowo(MacAdres2port) % 256)
	var Mac3 uint64 = uint64(PortOdczytsłowo(MacAdres2port) / 256)
	var Mac4 uint64 = uint64(PortOdczytsłowo(MacAdres4port) % 256)
	var Mac5 uint64 = uint64(PortOdczytsłowo(MacAdres4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macAdres uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konsola_2.MWydrukujxy(([]byte)("[interrupt num : "), 0, 13)
	konsola_2.MHexadecimalWydrukuj(uint8(urządzeniedescriptor.Przerwanie))
	konsola_2.MWydrukuj(([]byte)("]"))
	konsola_2.MWydrukuj(([]byte)("[mac address : "))
	konsola_2.MUnsignedinteger16Wydrukuj(uint16(macAdres >> 32))
	konsola_2.MUnsignedinteger32Wydrukuj(uint32(macAdres & 0x00000000FFFFFFFF))
	konsola_2.MWydrukuj(([]byte)("]"))

	PortZapissłowo(registerAdresport, 20)
	PortZapissłowo(busSterowanieregisterdataport, 0x102)

	PortZapissłowo(registerAdresport, 0)
	PortZapissłowo(registerdataport, 0x04)

	initBlok.tRYB = 0x0000
	initBlok.liczbaWyślijbuffer = 3
	initBlok.liczbarecvbuffer = 3

	initBlok.physicalAdres = Mac

	initBlok.logiczneAdres = 0

	wyślijbufferOpis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&wyślijbufferOpisPamięć)) + 15) & ^(uintptr)(0xF)))
	initBlok.wyślijbufferOpisAdres = uintptr(Pointer(&wyślijbufferOpis))
	recvbufferOpis = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferOpisPamięć)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferOpisAdres = uintptr(Pointer(&recvbufferOpis))

	for i := 0; i < 8; i++ {
		wyślijbufferOpis[i].adres_2 = uint32((uintptr(Pointer(&wyślijbuffer[i])) + 15) & ^(uintptr(0xF)))
		wyślijbufferOpis[i].znaczniki = 0x7FF | 0xF000
		wyślijbufferOpis[i].znaczniki2 = 0
		wyślijbufferOpis[i].dostępne = 0

		recvbufferOpis[i].adres_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferOpis[i].znaczniki = 0xF7FF | 0x80000000

	}

	PortZapissłowo(registerAdresport, 1)
	PortZapissłowo(registerdataport, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	PortZapissłowo(registerAdresport, 2)
	PortZapissłowo(registerdataport, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (bieżący *Tamdam79c973) Włącz() {
	PortZapissłowo(registerAdresport, 0)
	PortZapissłowo(registerdataport, 0x41)

	PortZapissłowo(registerAdresport, 4)
	temporary := PortOdczytsłowo(registerdataport)
	PortZapissłowo(registerAdresport, 4)
	PortZapissłowo(registerdataport, temporary|0xC00)

	PortZapissłowo(registerAdresport, 0)
	PortZapissłowo(registerdataport, 0x42)

}
func (bieżący *Tamdam79c973) Wyzeruj() int {
	PortOdczytsłowo(wyzerujport)
	PortZapissłowo(wyzerujport, 0)
	return 10
}

var liczba uint16 = 0

func (bieżący *Tamdam79c973) UchwytPrzerwanie(esp uint32) uint32 {

	PortZapissłowo(registerAdresport, 0)
	temporary := uint32(PortOdczytsłowo(registerdataport))
	konsola_2.MWydrukuj(([]byte)("interrupt("))
	konsola_2.MUnsignedinteger32Wydrukuj(esp)
	konsola_2.MWydrukuj(([]byte)(":"))
	konsola_2.MUnsignedinteger32Wydrukuj(temporary)
	konsola_2.MWydrukuj(([]byte)(":"))
	konsola_2.MUnsignedinteger16Wydrukuj(liczba)
	liczba++
	konsola_2.MWydrukuj(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konsola_2.MWydrukuj(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konsola_2.MWydrukuj(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konsola_2.MWydrukuj(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konsola_2.MWydrukuj(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konsola_2.MWydrukuj(([]byte)("am79c973 data received"))
		bieżący.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konsola_2.MWydrukuj(([]byte)("am79c973 data sent"))
	}

	PortZapissłowo(registerAdresport, 0)
	PortZapissłowo(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konsola_2.MWydrukuj(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (bieżący *Tamdam79c973) Wyślij(dataKursor uintptr, rozmiar uint32) {
	var wyślijdescriptor uint16 = uint16(bieżącyWyślijbuffer)
	bieżącyWyślijbuffer = 0

	if rozmiar > 1518 {
		rozmiar = 1518
	}

	var źródło_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursor))
	var cel_2 uint32 = wyślijbufferOpis[wyślijdescriptor].adres_2 + rozmiar - 1

	for i := 0; i < int(rozmiar); i++ {

		*(*byte)(Pointer(uintptr(cel_2))) = źródło_2[int(rozmiar)-i-1]

		cel_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataKursor))
	konsola_2.MWydrukujxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konsola_2.MHexadecimalWydrukuj(data[i])
		konsola_2.MWydrukuj(([]byte)(":"))
	}
	konsola_2.MWydrukuj(([]byte)("\n"))

	wyślijbufferOpis[wyślijdescriptor].dostępne = 0
	wyślijbufferOpis[wyślijdescriptor].znaczniki2 = 0
	wyślijbufferOpis[wyślijdescriptor].znaczniki = 0x8300F000 | uint32((-rozmiar)&0xFFF)

	PortZapissłowo(registerAdresport, 0)
	PortZapissłowo(registerdataport, 0x48)

}
func (bieżący *Tamdam79c973) Receive() {
	konsola_2.MWydrukuj(([]byte)(":"))
	konsola_2.MUnsignedinteger32Wydrukuj(uint32(uintptr(Pointer(&wyślijbuffer))))
	konsola_2.MWydrukuj(([]byte)(":"))
	konsola_2.MHexadecimalWydrukuj(wyślijbuffer[0][0])
	konsola_2.MHexadecimalWydrukuj(wyślijbuffer[0][1])
	konsola_2.MWydrukuj(([]byte)(":"))
	bieżącyrecvbuffer = 0

	for ; (recvbufferOpis[bieżącyrecvbuffer].znaczniki & 0x80000000) == 0; bieżącyrecvbuffer = (bieżącyrecvbuffer + 1) % 8 {

		if !(recvbufferOpis[bieżącyrecvbuffer].znaczniki&0x40000000 != 0) && ((recvbufferOpis[bieżącyrecvbuffer].znaczniki & 0x03000000) == 0x03000000) {
			var rozmiar uint32 = recvbufferOpis[bieżącyrecvbuffer].znaczniki & 0xFFF
			if rozmiar > 64 {
				rozmiar -= 4
			}

			konsola_2.MWydrukuj([]byte(" size : ["))
			konsola_2.MUnsignedinteger32Wydrukuj(rozmiar)
			konsola_2.MWydrukuj([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferOpis[bieżącyrecvbuffer].adres_2)))
			var odwołanie_do_adresu uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Włączrawdatareceive(odwołanie_do_adresu, int(rozmiar)) {

					konsola_2.MWydrukujxy(([]byte)("self.Send"), 0, 22)

					bieżący.Wyślij(odwołanie_do_adresu, rozmiar)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konsola_2.MHexadecimalWydrukuj(buffer_2[i])
				konsola_2.MWydrukuj([]byte(":"))
			}

		}
		recvbufferOpis[bieżącyrecvbuffer].znaczniki2 = 0
		recvbufferOpis[bieżącyrecvbuffer].znaczniki = 0x8000F7FF
	}
}
func (bieżący *Tamdam79c973) Zbiórhandler(handler *TRawdatahandler) {
	bieżący.handler = handler
}
func (bieżący *Tamdam79c973) GetmacAdres() uint64 {

	return initBlok.physicalAdres
}
func (bieżący *Tamdam79c973) ZbióripAdres(ip uint64) {
	initBlok.logiczneAdres = ip
}
func (bieżący *Tamdam79c973) GetipAdres() uint64 {
	return initBlok.logiczneAdres
}
