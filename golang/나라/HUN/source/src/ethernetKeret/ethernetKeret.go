package ethernetKeret

import . "konzol"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetKonzol TKonzol = TKonzol{}

type TEthernetKeretheaderbuffer struct {
	célmacbe	[6]byte
	forrásmacbe	[6]byte
	ethernetTípusbe	[2]byte
}

var keretheaderMéret int = 14

type TEthernetKeretheader struct {
	célmacbe	uint64
	forrásmacbe	uint64
	ethernetTípusbe	uint16
}

func (self *TEthernetKeretheader) Init(buffer_2 TEthernetKeretheaderbuffer) {
	self.célmacbe = (Tömbtounsignedinteger48(buffer_2.célmacbe))
	self.forrásmacbe = (Tömbtounsignedinteger48(buffer_2.forrásmacbe))
	self.ethernetTípusbe = (Tömbtounsignedinteger16(buffer_2.ethernetTípusbe))

}
func (self *TEthernetKeretheader) Halmazbuffer(buffer_2 *TEthernetKeretheaderbuffer) {
	buffer_2.célmacbe = Unsignedinteger48toTömb(Unsignedinteger48r(self.célmacbe))
	buffer_2.forrásmacbe = Unsignedinteger48toTömb(Unsignedinteger48r(self.forrásmacbe))
	buffer_2.ethernetTípusbe = Unsignedinteger16toTömb(Unsignedinteger16r(self.ethernetTípusbe))
}

type IEthernetKerethandler interface {
	Init(backend TEthernetKeretprovider)
	Halmazhandler(handler IEthernetKerethandler, ethernetTípus uint16)
	EthernetKeretreceivewhen(dataMutató uintptr, méret int) bool
	Küldés(célmacbe uint64, dataMutató uintptr, méret uint32)
	KeretKüldés(célmacbe uint64, ethernetTípusbe uint16, dataMutató uintptr, méret uint32)
	Providerget() TEthernetKeretprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetKerethandler struct {
}

var keret TEthernetKeretheader
var Backend TEthernetKeretprovider
var handler_2 [65535]IEthernetKerethandler
var efhandler *TEthernetKerethandler = nil

func (self *TEthernetKerethandler) Init(backend TEthernetKeretprovider) {
	Backend = backend
}

func (self *TEthernetKerethandler) Halmazhandler(handler IEthernetKerethandler, pethernetTípus uint16) {
	handler_2[pethernetTípus] = handler
}
func (self *TEthernetKerethandler) Halmazbackend(backend TEthernetKeretprovider) {
	Backend = backend
}
func (self *TEthernetKerethandler) Getbackend() TEthernetKeretprovider {
	return Backend
}
func (self *TEthernetKerethandler) EthernetKeretreceivewhen(dataMutató uintptr, méret int) bool {
	ethernetKonzol.MNyomtatás(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetKerethandler) Küldés(célmacbe uint64, dataMutató uintptr, méret uint32) {
	Backend.KeretKüldés(célmacbe, keret.ethernetTípusbe, dataMutató, méret)
}
func (self *TEthernetKerethandler) KeretKüldés(célmacbe uint64, ethernetTípusbe uint16, dataMutató uintptr, méret uint32) {
	Backend.KeretKüldés(célmacbe, ethernetTípusbe, dataMutató, méret)
}
func (self *TEthernetKerethandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEthernetKerethandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEthernetKerethandler) Providerget() TEthernetKeretprovider {
	return Backend
}

type TEthernetKeretrawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetKeretprovider

func (self *TEthernetKeretrawdatahandler) Init(pprovider TEthernetKeretprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernetKeretrawdatahandler) Berawdatareceive(dataMutató uintptr, méret int) bool {
	return provider.Berawdatareceive(dataMutató, méret)
}
func (self *TEthernetKeretrawdatahandler) Küldés(dataMutató uintptr, méret uint32) {
	provider.Küldés(dataMutató, méret)
}
func (self *TEthernetKeretrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEthernetKeretrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEthernetKeretrawdatahandler) Providerget() TEthernetKeretprovider {
	return provider
}

type TEthernetKeretprovider struct {
	hálózatKártya	Tamdam79c973
	handler_2	[65565]IEthernetKerethandler
}

func (self *TEthernetKeretprovider) Init(backend Tamdam79c973) {

	self.hálózatKártya = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var számláló uint16 = 0

func (self *TEthernetKeretprovider) Berawdatareceive(dataMutató uintptr, méret int) bool {

	var buffer_2 *TEthernetKeretheaderbuffer = (*TEthernetKeretheaderbuffer)(Pointer(dataMutató))
	var keret TEthernetKeretheader = TEthernetKeretheader{}
	keret.Init(*buffer_2)
	var reply bool = false

	if keret.célmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(keret.célmacbe) == self.Getmacaddress() {
		if handler_2[keret.ethernetTípusbe] != nil {
			ethernetKonzol.MNyomtatás(([]byte)("provider\n"))

			var mutató uintptr = uintptr(Pointer(dataMutató)) + uintptr(keretheaderMéret)
			reply = handler_2[keret.ethernetTípusbe].EthernetKeretreceivewhen(mutató, méret-keretheaderMéret)

		}
	}

	if reply {
		keret.célmacbe = keret.forrásmacbe
		keret.forrásmacbe = Unsignedinteger48r(self.Getmacaddress())
		keret.Halmazbuffer(buffer_2)

	}

	ethernetKonzol.MNyomtatásxy(([]byte)("spro["), 0, 1)
	ethernetKonzol.MUnsignedinteger64Nyomtatás(keret.forrásmacbe)
	ethernetKonzol.MNyomtatás(([]byte)(":"))
	ethernetKonzol.MUnsignedinteger64Nyomtatás(keret.célmacbe)
	ethernetKonzol.MNyomtatás(([]byte)(":]["))
	ethernetKonzol.MUnsignedinteger64Nyomtatás(self.Getmacaddress())
	ethernetKonzol.MNyomtatás(([]byte)(":"))
	ethernetKonzol.MUnsignedinteger16Nyomtatás(keret.ethernetTípusbe)
	ethernetKonzol.MNyomtatás(([]byte)("]"))

	return reply

}
func (self *TEthernetKeretprovider) Küldés(dataMutató uintptr, méret uint32) {
	self.hálózatKártya.Küldés(dataMutató, méret)
}
func (self *TEthernetKeretprovider) KeretKüldés(célmacbe uint64, ethernetTípusbe uint16, dataMutató uintptr, méret uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetKeretheaderbuffer = (*TEthernetKeretheaderbuffer)(Pointer(&buffer2_2))

	var keret TEthernetKeretheader = TEthernetKeretheader{}
	keret.Init(*buffer_2)

	keret.célmacbe = Unsignedinteger48r(célmacbe)
	keret.forrásmacbe = Unsignedinteger48r(self.hálózatKártya.Getmacaddress())
	keret.ethernetTípusbe = Unsignedinteger16r(ethernetTípusbe)

	keret.Halmazbuffer(buffer_2)
	var forrás_2 [4096]byte = *(*([4096]byte))(Pointer(dataMutató))

	var i uint32 = 0
	for i = 0; i < méret; i++ {
		buffer2_2[uint32(keretheaderMéret)+i] = forrás_2[i]

	}

	var mutató uintptr = uintptr(Pointer(&buffer2_2))

	self.hálózatKártya.Küldés(mutató, méret+uint32(keretheaderMéret))

}
func (self *TEthernetKeretprovider) Getmacaddress() uint64 {
	return self.hálózatKártya.Getmacaddress()
}
func (self *TEthernetKeretprovider) Getipaddress() uint64 {
	return self.hálózatKártya.Getipaddress()
}
