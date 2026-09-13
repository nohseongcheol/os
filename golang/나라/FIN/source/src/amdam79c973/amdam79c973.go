package amdam79c973

import . "unsafe"
import . "keskeytys"
import . "konsoli"
import . "portti"
import . "pci"

var verkkoKorttiKonsoli TKonsoli = TKonsoli{}

type TInitializationLohko struct {
	tILA			uint16
	numeroLähetäbuffer	uint8
	numerorecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress			uint64
	recvbufferKuvausaddress		uintptr
	lähetäbufferKuvausaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	liput		uint32
	liput2		uint32
	käytettävissä	uint32
}

type IRawdatahandler interface {
	Päällärawdatareceive(dataOsoitin uintptr, koko int) bool
	Lähetä(dataOsoitin uintptr, koko uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (itse *TRawdatahandler) Asetabackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (itse *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (itse *TRawdatahandler) Päällärawdatareceive(dataOsoitin uintptr, koko int) bool {
	verkkoKorttiKonsoli.MTulostaxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (itse *TRawdatahandler) Lähetä(dataOsoitin uintptr, koko uint32) {
	verkkoKorttiKonsoli.MTulostaxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Lähetä(dataOsoitin, koko)
}

var Macaddress0Portti uint16
var Macaddress2Portti uint16
var Macaddress4Portti uint16
var registerdataPortti uint16
var registeraddressPortti uint16
var palautaPortti uint16
var busCtrlregisterdataPortti uint16

var initLohko TInitializationLohko

var lähetäbufferKuvaus [8]TBufferdescriptor
var lähetäbufferKuvausMuisti [2048 + 15]byte
var lähetäbuffer [2*1024 + 15][8]uint8
var nykyinenLähetäbuffer uint8

var recvbufferKuvaus [8]TBufferdescriptor
var recvbufferKuvausMuisti [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var nykyinenrecvbuffer uint8
var funcArvo func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TKeskeytyshandler
	laitedescriptor	TPeripheralcomponentinterconnectLaitedescriptor
	keskeytys	*TKeskeytysmanager
	handler		*TRawdatahandler
}

var konsoli_2 TKonsoli = TKonsoli{}
var irawdatahandler IRawdatahandler

func (itse *Tamdam79c973) Initdriver(keskeytys *TKeskeytysmanager, laitedescriptor TPeripheralcomponentinterconnectLaitedescriptor, handler IRawdatahandler) {

	itse.laitedescriptor = laitedescriptor

	funcArvo = (*Tamdam79c973).KahvaKeskeytys
	var address uintptr
	address = uintptr(Pointer(&funcArvo))

	itse.Init(uint8(0x20+laitedescriptor.Keskeytys), uintptr(Pointer(keskeytys)), address)

	Macaddress0Portti = uint16(laitedescriptor.Porttibase)
	Macaddress2Portti = uint16(laitedescriptor.Porttibase) + 0x02
	Macaddress4Portti = uint16(laitedescriptor.Porttibase) + 0x04
	registerdataPortti = uint16(laitedescriptor.Porttibase) + 0x10
	registeraddressPortti = uint16(laitedescriptor.Porttibase) + 0x12
	palautaPortti = uint16(laitedescriptor.Porttibase) + 0x14
	busCtrlregisterdataPortti = uint16(laitedescriptor.Porttibase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	nykyinenLähetäbuffer = 0
	nykyinenrecvbuffer = 0

	var Mac0 uint64 = uint64(PorttiLukusana(Macaddress0Portti) % 256)
	var Mac1 uint64 = uint64(PorttiLukusana(Macaddress0Portti) / 256)
	var Mac2 uint64 = uint64(PorttiLukusana(Macaddress2Portti) % 256)
	var Mac3 uint64 = uint64(PorttiLukusana(Macaddress2Portti) / 256)
	var Mac4 uint64 = uint64(PorttiLukusana(Macaddress4Portti) % 256)
	var Mac5 uint64 = uint64(PorttiLukusana(Macaddress4Portti) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konsoli_2.MTulostaxy(([]byte)("[interrupt num : "), 0, 13)
	konsoli_2.MHexadecimalTulosta(uint8(laitedescriptor.Keskeytys))
	konsoli_2.MTulosta(([]byte)("]"))
	konsoli_2.MTulosta(([]byte)("[mac address : "))
	konsoli_2.MUnsignedinteger16Tulosta(uint16(macaddress >> 32))
	konsoli_2.MUnsignedinteger32Tulosta(uint32(macaddress & 0x00000000FFFFFFFF))
	konsoli_2.MTulosta(([]byte)("]"))

	PorttiKirjoitussana(registeraddressPortti, 20)
	PorttiKirjoitussana(busCtrlregisterdataPortti, 0x102)

	PorttiKirjoitussana(registeraddressPortti, 0)
	PorttiKirjoitussana(registerdataPortti, 0x04)

	initLohko.tILA = 0x0000
	initLohko.numeroLähetäbuffer = 3
	initLohko.numerorecvbuffer = 3

	initLohko.physicaladdress = Mac

	initLohko.logicaladdress = 0

	lähetäbufferKuvaus = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&lähetäbufferKuvausMuisti)) + 15) & ^(uintptr)(0xF)))
	initLohko.lähetäbufferKuvausaddress = uintptr(Pointer(&lähetäbufferKuvaus))
	recvbufferKuvaus = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferKuvausMuisti)) + 15) & ^(uintptr)(0xF)))
	initLohko.recvbufferKuvausaddress = uintptr(Pointer(&recvbufferKuvaus))

	for i := 0; i < 8; i++ {
		lähetäbufferKuvaus[i].address_2 = uint32((uintptr(Pointer(&lähetäbuffer[i])) + 15) & ^(uintptr(0xF)))
		lähetäbufferKuvaus[i].liput = 0x7FF | 0xF000
		lähetäbufferKuvaus[i].liput2 = 0
		lähetäbufferKuvaus[i].käytettävissä = 0

		recvbufferKuvaus[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferKuvaus[i].liput = 0xF7FF | 0x80000000

	}

	PorttiKirjoitussana(registeraddressPortti, 1)
	PorttiKirjoitussana(registerdataPortti, uint16(uintptr(Pointer(&initLohko))&0xFFFF))

	PorttiKirjoitussana(registeraddressPortti, 2)
	PorttiKirjoitussana(registerdataPortti, uint16((uintptr(Pointer(&initLohko))>>16)&0xFFFF))

}
func (itse *Tamdam79c973) Otakäyttöön() {
	PorttiKirjoitussana(registeraddressPortti, 0)
	PorttiKirjoitussana(registerdataPortti, 0x41)

	PorttiKirjoitussana(registeraddressPortti, 4)
	temporary := PorttiLukusana(registerdataPortti)
	PorttiKirjoitussana(registeraddressPortti, 4)
	PorttiKirjoitussana(registerdataPortti, temporary|0xC00)

	PorttiKirjoitussana(registeraddressPortti, 0)
	PorttiKirjoitussana(registerdataPortti, 0x42)

}
func (itse *Tamdam79c973) Palauta() int {
	PorttiLukusana(palautaPortti)
	PorttiKirjoitussana(palautaPortti, 0)
	return 10
}

var count uint16 = 0

func (itse *Tamdam79c973) KahvaKeskeytys(esp uint32) uint32 {

	PorttiKirjoitussana(registeraddressPortti, 0)
	temporary := uint32(PorttiLukusana(registerdataPortti))
	konsoli_2.MTulosta(([]byte)("interrupt("))
	konsoli_2.MUnsignedinteger32Tulosta(esp)
	konsoli_2.MTulosta(([]byte)(":"))
	konsoli_2.MUnsignedinteger32Tulosta(temporary)
	konsoli_2.MTulosta(([]byte)(":"))
	konsoli_2.MUnsignedinteger16Tulosta(count)
	count++
	konsoli_2.MTulosta(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konsoli_2.MTulosta(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konsoli_2.MTulosta(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konsoli_2.MTulosta(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konsoli_2.MTulosta(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konsoli_2.MTulosta(([]byte)("am79c973 data received"))
		itse.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konsoli_2.MTulosta(([]byte)("am79c973 data sent"))
	}

	PorttiKirjoitussana(registeraddressPortti, 0)
	PorttiKirjoitussana(registerdataPortti, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konsoli_2.MTulosta(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (itse *Tamdam79c973) Lähetä(dataOsoitin uintptr, koko uint32) {
	var lähetädescriptor uint16 = uint16(nykyinenLähetäbuffer)
	nykyinenLähetäbuffer = 0

	if koko > 1518 {
		koko = 1518
	}

	var lähde_2 [4096]byte = *(*([4096]byte))(Pointer(dataOsoitin))
	var kohde_2 uint32 = lähetäbufferKuvaus[lähetädescriptor].address_2 + koko - 1

	for i := 0; i < int(koko); i++ {

		*(*byte)(Pointer(uintptr(kohde_2))) = lähde_2[int(koko)-i-1]

		kohde_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataOsoitin))
	konsoli_2.MTulostaxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konsoli_2.MHexadecimalTulosta(data[i])
		konsoli_2.MTulosta(([]byte)(":"))
	}
	konsoli_2.MTulosta(([]byte)("\n"))

	lähetäbufferKuvaus[lähetädescriptor].käytettävissä = 0
	lähetäbufferKuvaus[lähetädescriptor].liput2 = 0
	lähetäbufferKuvaus[lähetädescriptor].liput = 0x8300F000 | uint32((-koko)&0xFFF)

	PorttiKirjoitussana(registeraddressPortti, 0)
	PorttiKirjoitussana(registerdataPortti, 0x48)

}
func (itse *Tamdam79c973) Receive() {
	konsoli_2.MTulosta(([]byte)(":"))
	konsoli_2.MUnsignedinteger32Tulosta(uint32(uintptr(Pointer(&lähetäbuffer))))
	konsoli_2.MTulosta(([]byte)(":"))
	konsoli_2.MHexadecimalTulosta(lähetäbuffer[0][0])
	konsoli_2.MHexadecimalTulosta(lähetäbuffer[0][1])
	konsoli_2.MTulosta(([]byte)(":"))
	nykyinenrecvbuffer = 0

	for ; (recvbufferKuvaus[nykyinenrecvbuffer].liput & 0x80000000) == 0; nykyinenrecvbuffer = (nykyinenrecvbuffer + 1) % 8 {

		if !(recvbufferKuvaus[nykyinenrecvbuffer].liput&0x40000000 != 0) && ((recvbufferKuvaus[nykyinenrecvbuffer].liput & 0x03000000) == 0x03000000) {
			var koko uint32 = recvbufferKuvaus[nykyinenrecvbuffer].liput & 0xFFF
			if koko > 64 {
				koko -= 4
			}

			konsoli_2.MTulosta([]byte(" size : ["))
			konsoli_2.MUnsignedinteger32Tulosta(koko)
			konsoli_2.MTulosta([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferKuvaus[nykyinenrecvbuffer].address_2)))
			var osoiteviite uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Päällärawdatareceive(osoiteviite, int(koko)) {

					konsoli_2.MTulostaxy(([]byte)("self.Send"), 0, 22)

					itse.Lähetä(osoiteviite, koko)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konsoli_2.MHexadecimalTulosta(buffer_2[i])
				konsoli_2.MTulosta([]byte(":"))
			}

		}
		recvbufferKuvaus[nykyinenrecvbuffer].liput2 = 0
		recvbufferKuvaus[nykyinenrecvbuffer].liput = 0x8000F7FF
	}
}
func (itse *Tamdam79c973) Asetahandler(handler *TRawdatahandler) {
	itse.handler = handler
}
func (itse *Tamdam79c973) Getmacaddress() uint64 {

	return initLohko.physicaladdress
}
func (itse *Tamdam79c973) Asetaipaddress(ip uint64) {
	initLohko.logicaladdress = ip
}
func (itse *Tamdam79c973) Getipaddress() uint64 {
	return initLohko.logicaladdress
}
