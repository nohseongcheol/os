/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "konzol"
import . "util"
import . "memóriamanager"
import . "ipv4"

var udpKonzol = TKonzol{}

type TFelhasználódatagramprotocolheaderbuffer struct {
	forrásportSzám	[2]byte
	célportSzám	[2]byte

	hossz		[2]byte
	checksum	[2]byte
}

var udpheaderMéret uint32 = 8

type TFelhasználódatagramprotocolheader struct {
	forrásportSzám	uint16
	célportSzám	uint16

	hossz		uint16
	checksum	uint16
}

func (self *TFelhasználódatagramprotocolheader) Init(buffer_2 *TFelhasználódatagramprotocolheaderbuffer) {
	self.forrásportSzám = Tömbtounsignedinteger16(buffer_2.forrásportSzám)
	self.célportSzám = Tömbtounsignedinteger16(buffer_2.célportSzám)

	self.hossz = Tömbtounsignedinteger16(buffer_2.hossz)
	self.checksum = Tömbtounsignedinteger16(buffer_2.checksum)
}
func (self *TFelhasználódatagramprotocolheader) Halmazbuffer(buffer_2 *TFelhasználódatagramprotocolheaderbuffer) {

	buffer_2.forrásportSzám = Unsignedinteger16toTömb(self.forrásportSzám)
	buffer_2.célportSzám = Unsignedinteger16toTömb(self.célportSzám)

	buffer_2.hossz = Unsignedinteger16toTömb(self.hossz)
	buffer_2.checksum = Unsignedinteger16toTömb(self.checksum)

}

type IFelhasználódatagramprotocolhandler interface {
	FogantyúFelhasználódatagramprotocolÜzenet(foglalat *TFelhasználódatagramprotocolFoglalat, data uintptr, méret uint16)
}

type TFelhasználódatagramprotocolhandler struct {
}

func (self *TFelhasználódatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (self *TFelhasználódatagramprotocolhandler) FogantyúFelhasználódatagramprotocolÜzenet(foglalat *TFelhasználódatagramprotocolFoglalat, data uintptr, méret uint16) {
}

type IFelhasználódatagramprotocolFoglalat interface {
	FogantyúFelhasználódatagramprotocolÜzenet(data uintptr, méret uint16)
}
type TFelhasználódatagramprotocolFoglalat struct {
	távoliportSzám	uint16
	távoliip	uint32
	helyiportSzám	uint16
	helyiip		uint32

	listening	bool
}

var udpprovider TFelhasználódatagramprotocolprovider
var udphandler IFelhasználódatagramprotocolhandler

func (self *TFelhasználódatagramprotocolFoglalat) Teszt() {
}
func (self *TFelhasználódatagramprotocolFoglalat) Init(pudpprovider TFelhasználódatagramprotocolprovider, pudphandler IFelhasználódatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TFelhasználódatagramprotocolFoglalat) FogantyúFelhasználódatagramprotocolÜzenet(data uintptr, méret uint16) {
	if udphandler != nil {
		udphandler.FogantyúFelhasználódatagramprotocolÜzenet(self, data, méret)
	}
}
func (self *TFelhasználódatagramprotocolFoglalat) Küldés(pdata []byte, méret uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(méret); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Küldés(self, data, méret)
}
func (self *TFelhasználódatagramprotocolFoglalat) Bontás() {
	udpprovider.Bontás(self)
}

type TFelhasználódatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TFelhasználódatagramprotocolFoglalat
var számsockets int
var szabadport uint16

func (self *TFelhasználódatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	számsockets = 0
	szabadport = 1024
}
func (self *TFelhasználódatagramprotocolprovider) Internetprotocolreceivewhen(forrásipaddressHálózatbyteorder uint32, célipaddressHálózatbyteorder uint32, internetprotocolpayload uintptr, méret uint32) bool {
	if méret < udpheaderMéret {
		return false
	}

	var buffer_2 *TFelhasználódatagramprotocolheaderbuffer = (*TFelhasználódatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TFelhasználódatagramprotocolheader
	msg.Init(buffer_2)

	var foglalat *TFelhasználódatagramprotocolFoglalat = nil

	for i := 0; i < számsockets && foglalat == nil; i++ {
		if sockets[i].helyiportSzám == msg.célportSzám && sockets[i].helyiip == célipaddressHálózatbyteorder && sockets[i].listening == true {
			foglalat = &sockets[i]
			foglalat.listening = false
			foglalat.távoliportSzám = msg.forrásportSzám
			foglalat.távoliip = forrásipaddressHálózatbyteorder
		} else if sockets[i].helyiportSzám == msg.célportSzám && sockets[i].helyiip == célipaddressHálózatbyteorder && sockets[i].távoliportSzám == msg.forrásportSzám && sockets[i].távoliip == forrásipaddressHálózatbyteorder {
			foglalat = &sockets[i]

		}
	}

	msg.Halmazbuffer(buffer_2)
	if foglalat != nil {
		foglalat.FogantyúFelhasználódatagramprotocolÜzenet(internetprotocolpayload+uintptr(udpheaderMéret), uint16(méret-udpheaderMéret))
	}

	return false
}

func (self *TFelhasználódatagramprotocolprovider) Kapcsolódás(ip uint32, port uint16) *TFelhasználódatagramprotocolFoglalat {
	var memóriamanager = &TMemóriamanager{}
	var foglalat = (*TFelhasználódatagramprotocolFoglalat)(memóriamanager.Malloc(50))

	if foglalat != nil {

		foglalat.Init(*self, nil)
		foglalat.távoliportSzám = port
		foglalat.távoliip = ip
		foglalat.helyiportSzám = szabadport
		szabadport++
		foglalat.helyiip = uint32((*iphandler.Providerget()).Getipaddress())

		foglalat.távoliportSzám = Unsignedinteger16r(foglalat.távoliportSzám)
		foglalat.helyiportSzám = Unsignedinteger16r(foglalat.helyiportSzám)

		sockets[számsockets] = *foglalat
		számsockets++

	}
	return foglalat

}
func (self *TFelhasználódatagramprotocolprovider) Listen(port uint16) *TFelhasználódatagramprotocolFoglalat {
	var foglalat = &TFelhasználódatagramprotocolFoglalat{}
	foglalat = nil
	if foglalat != nil {
		foglalat.Init(*self, nil)
		foglalat.listening = true
		foglalat.helyiportSzám = port
		foglalat.helyiip = uint32((*iphandler.Providerget()).Getipaddress())

		foglalat.helyiportSzám = Unsignedinteger16r(foglalat.helyiportSzám)
	}
	return foglalat
}
func (self *TFelhasználódatagramprotocolprovider) Bontás(foglalat *TFelhasználódatagramprotocolFoglalat) {
	for i := 0; i < számsockets && foglalat == nil; i++ {
		if sockets[i] == *foglalat {
			számsockets--
			sockets[i] = sockets[számsockets]
			break
		}
	}
}
func (self *TFelhasználódatagramprotocolprovider) Küldés(foglalat *TFelhasználódatagramprotocolFoglalat, pdata uintptr, méret uint16) {
	var összesenHossz = uint32(méret) + udpheaderMéret

	var buffer_2 [4096]byte

	var msgbuffer = (*TFelhasználódatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TFelhasználódatagramprotocolheader{}

	msg.forrásportSzám = foglalat.helyiportSzám
	msg.célportSzám = foglalat.távoliportSzám
	msg.hossz = Unsignedinteger16r(uint16(összesenHossz))

	msg.checksum = 0x0
	msg.Halmazbuffer(msgbuffer)

	var dataBájt [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(méret); i++ {
		buffer_2[int(udpheaderMéret)+i] = dataBájt[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Küldés(foglalat.távoliip, 0x11, data, összesenHossz)

}
func (self *TFelhasználódatagramprotocolprovider) Bind(foglalat *TFelhasználódatagramprotocolFoglalat, handler *TFelhasználódatagramprotocolhandler,) {
}
