/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "megszakítás"
import . "konzol"
import . "port"
import . "pci"

var hálózatKártyaKonzol TKonzol = TKonzol{}

type TInitializationBlokk struct {
	mód			uint16
	számKüldésbuffer	uint8
	számrecvbuffer		uint8

	physicaladdress	uint64

	logikaiaddress			uint64
	recvbufferLeírásaddress		uintptr
	küldésbufferLeírásaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	flagek		uint32
	flagek2		uint32
	elérhető	uint32
}

type IRawdatahandler interface {
	Berawdatareceive(dataMutató uintptr, méret int) bool
	Küldés(dataMutató uintptr, méret uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (self *TRawdatahandler) Halmazbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (self *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (self *TRawdatahandler) Berawdatareceive(dataMutató uintptr, méret int) bool {
	hálózatKártyaKonzol.MNyomtatásxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Küldés(dataMutató uintptr, méret uint32) {
	hálózatKártyaKonzol.MNyomtatásxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Küldés(dataMutató, méret)
}

var Macaddress0port uint16
var Macaddress2port uint16
var Macaddress4port uint16
var registerdataport uint16
var registeraddressport uint16
var visszaállításport uint16
var busVezérlésregisterdataport uint16

var initBlokk TInitializationBlokk

var küldésbufferLeírás [8]TBufferdescriptor
var küldésbufferLeírásMemória [2048 + 15]byte
var küldésbuffer [2*1024 + 15][8]uint8
var jelenlegiKüldésbuffer uint8

var recvbufferLeírás [8]TBufferdescriptor
var recvbufferLeírásMemória [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var jelenlegirecvbuffer uint8
var funcÉrték func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TMegszakításhandler
	eszközdescriptor	TPeripheralcomponentinterconnectEszközdescriptor
	megszakítás		*TMegszakításmanager
	handler			*TRawdatahandler
}

var konzol_2 TKonzol = TKonzol{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(megszakítás *TMegszakításmanager, eszközdescriptor TPeripheralcomponentinterconnectEszközdescriptor, handler IRawdatahandler) {

	self.eszközdescriptor = eszközdescriptor

	funcÉrték = (*Tamdam79c973).FogantyúMegszakítás
	var address uintptr
	address = uintptr(Pointer(&funcÉrték))

	self.Init(uint8(0x20+eszközdescriptor.Megszakítás), uintptr(Pointer(megszakítás)), address)

	Macaddress0port = uint16(eszközdescriptor.Portbase)
	Macaddress2port = uint16(eszközdescriptor.Portbase) + 0x02
	Macaddress4port = uint16(eszközdescriptor.Portbase) + 0x04
	registerdataport = uint16(eszközdescriptor.Portbase) + 0x10
	registeraddressport = uint16(eszközdescriptor.Portbase) + 0x12
	visszaállításport = uint16(eszközdescriptor.Portbase) + 0x14
	busVezérlésregisterdataport = uint16(eszközdescriptor.Portbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	jelenlegiKüldésbuffer = 0
	jelenlegirecvbuffer = 0

	var Mac0 uint64 = uint64(PortOlvasásszó(Macaddress0port) % 256)
	var Mac1 uint64 = uint64(PortOlvasásszó(Macaddress0port) / 256)
	var Mac2 uint64 = uint64(PortOlvasásszó(Macaddress2port) % 256)
	var Mac3 uint64 = uint64(PortOlvasásszó(Macaddress2port) / 256)
	var Mac4 uint64 = uint64(PortOlvasásszó(Macaddress4port) % 256)
	var Mac5 uint64 = uint64(PortOlvasásszó(Macaddress4port) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konzol_2.MNyomtatásxy(([]byte)("[interrupt num : "), 0, 13)
	konzol_2.MHexadecimalNyomtatás(uint8(eszközdescriptor.Megszakítás))
	konzol_2.MNyomtatás(([]byte)("]"))
	konzol_2.MNyomtatás(([]byte)("[mac address : "))
	konzol_2.MUnsignedinteger16Nyomtatás(uint16(macaddress >> 32))
	konzol_2.MUnsignedinteger32Nyomtatás(uint32(macaddress & 0x00000000FFFFFFFF))
	konzol_2.MNyomtatás(([]byte)("]"))

	PortÍrásszó(registeraddressport, 20)
	PortÍrásszó(busVezérlésregisterdataport, 0x102)

	PortÍrásszó(registeraddressport, 0)
	PortÍrásszó(registerdataport, 0x04)

	initBlokk.mód = 0x0000
	initBlokk.számKüldésbuffer = 3
	initBlokk.számrecvbuffer = 3

	initBlokk.physicaladdress = Mac

	initBlokk.logikaiaddress = 0

	küldésbufferLeírás = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&küldésbufferLeírásMemória)) + 15) & ^(uintptr)(0xF)))
	initBlokk.küldésbufferLeírásaddress = uintptr(Pointer(&küldésbufferLeírás))
	recvbufferLeírás = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferLeírásMemória)) + 15) & ^(uintptr)(0xF)))
	initBlokk.recvbufferLeírásaddress = uintptr(Pointer(&recvbufferLeírás))

	for i := 0; i < 8; i++ {
		küldésbufferLeírás[i].address_2 = uint32((uintptr(Pointer(&küldésbuffer[i])) + 15) & ^(uintptr(0xF)))
		küldésbufferLeírás[i].flagek = 0x7FF | 0xF000
		küldésbufferLeírás[i].flagek2 = 0
		küldésbufferLeírás[i].elérhető = 0

		recvbufferLeírás[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferLeírás[i].flagek = 0xF7FF | 0x80000000

	}

	PortÍrásszó(registeraddressport, 1)
	PortÍrásszó(registerdataport, uint16(uintptr(Pointer(&initBlokk))&0xFFFF))

	PortÍrásszó(registeraddressport, 2)
	PortÍrásszó(registerdataport, uint16((uintptr(Pointer(&initBlokk))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Aktiválás() {
	PortÍrásszó(registeraddressport, 0)
	PortÍrásszó(registerdataport, 0x41)

	PortÍrásszó(registeraddressport, 4)
	temporary := PortOlvasásszó(registerdataport)
	PortÍrásszó(registeraddressport, 4)
	PortÍrásszó(registerdataport, temporary|0xC00)

	PortÍrásszó(registeraddressport, 0)
	PortÍrásszó(registerdataport, 0x42)

}
func (self *Tamdam79c973) Visszaállítás() int {
	PortOlvasásszó(visszaállításport)
	PortÍrásszó(visszaállításport, 0)
	return 10
}

var számláló uint16 = 0

func (self *Tamdam79c973) FogantyúMegszakítás(esp uint32) uint32 {

	PortÍrásszó(registeraddressport, 0)
	temporary := uint32(PortOlvasásszó(registerdataport))
	konzol_2.MNyomtatás(([]byte)("interrupt("))
	konzol_2.MUnsignedinteger32Nyomtatás(esp)
	konzol_2.MNyomtatás(([]byte)(":"))
	konzol_2.MUnsignedinteger32Nyomtatás(temporary)
	konzol_2.MNyomtatás(([]byte)(":"))
	konzol_2.MUnsignedinteger16Nyomtatás(számláló)
	számláló++
	konzol_2.MNyomtatás(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konzol_2.MNyomtatás(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konzol_2.MNyomtatás(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konzol_2.MNyomtatás(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konzol_2.MNyomtatás(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konzol_2.MNyomtatás(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konzol_2.MNyomtatás(([]byte)("am79c973 data sent"))
	}

	PortÍrásszó(registeraddressport, 0)
	PortÍrásszó(registerdataport, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konzol_2.MNyomtatás(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Küldés(dataMutató uintptr, méret uint32) {
	var küldésdescriptor uint16 = uint16(jelenlegiKüldésbuffer)
	jelenlegiKüldésbuffer = 0

	if méret > 1518 {
		méret = 1518
	}

	var forrás_2 [4096]byte = *(*([4096]byte))(Pointer(dataMutató))
	var cél_2 uint32 = küldésbufferLeírás[küldésdescriptor].address_2 + méret - 1

	for i := 0; i < int(méret); i++ {

		*(*byte)(Pointer(uintptr(cél_2))) = forrás_2[int(méret)-i-1]

		cél_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataMutató))
	konzol_2.MNyomtatásxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konzol_2.MHexadecimalNyomtatás(data[i])
		konzol_2.MNyomtatás(([]byte)(":"))
	}
	konzol_2.MNyomtatás(([]byte)("\n"))

	küldésbufferLeírás[küldésdescriptor].elérhető = 0
	küldésbufferLeírás[küldésdescriptor].flagek2 = 0
	küldésbufferLeírás[küldésdescriptor].flagek = 0x8300F000 | uint32((-méret)&0xFFF)

	PortÍrásszó(registeraddressport, 0)
	PortÍrásszó(registerdataport, 0x48)

}
func (self *Tamdam79c973) Receive() {
	konzol_2.MNyomtatás(([]byte)(":"))
	konzol_2.MUnsignedinteger32Nyomtatás(uint32(uintptr(Pointer(&küldésbuffer))))
	konzol_2.MNyomtatás(([]byte)(":"))
	konzol_2.MHexadecimalNyomtatás(küldésbuffer[0][0])
	konzol_2.MHexadecimalNyomtatás(küldésbuffer[0][1])
	konzol_2.MNyomtatás(([]byte)(":"))
	jelenlegirecvbuffer = 0

	for ; (recvbufferLeírás[jelenlegirecvbuffer].flagek & 0x80000000) == 0; jelenlegirecvbuffer = (jelenlegirecvbuffer + 1) % 8 {

		if !(recvbufferLeírás[jelenlegirecvbuffer].flagek&0x40000000 != 0) && ((recvbufferLeírás[jelenlegirecvbuffer].flagek & 0x03000000) == 0x03000000) {
			var méret uint32 = recvbufferLeírás[jelenlegirecvbuffer].flagek & 0xFFF
			if méret > 64 {
				méret -= 4
			}

			konzol_2.MNyomtatás([]byte(" size : ["))
			konzol_2.MUnsignedinteger32Nyomtatás(méret)
			konzol_2.MNyomtatás([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferLeírás[jelenlegirecvbuffer].address_2)))
			var mutató uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Berawdatareceive(mutató, int(méret)) {

					konzol_2.MNyomtatásxy(([]byte)("self.Send"), 0, 22)

					self.Küldés(mutató, méret)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konzol_2.MHexadecimalNyomtatás(buffer_2[i])
				konzol_2.MNyomtatás([]byte(":"))
			}

		}
		recvbufferLeírás[jelenlegirecvbuffer].flagek2 = 0
		recvbufferLeírás[jelenlegirecvbuffer].flagek = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Halmazhandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initBlokk.physicaladdress
}
func (self *Tamdam79c973) Halmazipaddress(ip uint64) {
	initBlokk.logikaiaddress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initBlokk.logikaiaddress
}
