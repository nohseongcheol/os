/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "atmintismanager"
import . "ipv4"

var udpconsole = TConsole{}

type TNaudotojasdatagramprotocolheaderbuffer struct {
	šaltinisPrievadasSkaičius	[2]byte
	tikslasPrievadasSkaičius	[2]byte

	trukmė		[2]byte
	kontrolinėsuma	[2]byte
}

var udpheaderDydis uint32 = 8

type TNaudotojasdatagramprotocolheader struct {
	šaltinisPrievadasSkaičius	uint16
	tikslasPrievadasSkaičius	uint16

	trukmė		uint16
	kontrolinėsuma	uint16
}

func (self *TNaudotojasdatagramprotocolheader) Init(buffer_2 *TNaudotojasdatagramprotocolheaderbuffer) {
	self.šaltinisPrievadasSkaičius = Masyvastounsignedinteger16(buffer_2.šaltinisPrievadasSkaičius)
	self.tikslasPrievadasSkaičius = Masyvastounsignedinteger16(buffer_2.tikslasPrievadasSkaičius)

	self.trukmė = Masyvastounsignedinteger16(buffer_2.trukmė)
	self.kontrolinėsuma = Masyvastounsignedinteger16(buffer_2.kontrolinėsuma)
}
func (self *TNaudotojasdatagramprotocolheader) Nustatytabuffer(buffer_2 *TNaudotojasdatagramprotocolheaderbuffer) {

	buffer_2.šaltinisPrievadasSkaičius = Unsignedinteger16toMasyvas(self.šaltinisPrievadasSkaičius)
	buffer_2.tikslasPrievadasSkaičius = Unsignedinteger16toMasyvas(self.tikslasPrievadasSkaičius)

	buffer_2.trukmė = Unsignedinteger16toMasyvas(self.trukmė)
	buffer_2.kontrolinėsuma = Unsignedinteger16toMasyvas(self.kontrolinėsuma)

}

type INaudotojasdatagramprotocolhandler interface {
	PozicijaNaudotojasdatagramprotocolPranešimas(lizdas *TNaudotojasdatagramprotocolLizdas, data uintptr, dydis uint16)
}

type TNaudotojasdatagramprotocolhandler struct {
}

func (self *TNaudotojasdatagramprotocolhandler) Init(backend TInternetasprotocolprovider) {
}
func (self *TNaudotojasdatagramprotocolhandler) PozicijaNaudotojasdatagramprotocolPranešimas(lizdas *TNaudotojasdatagramprotocolLizdas, data uintptr, dydis uint16) {
}

type INaudotojasdatagramprotocolLizdas interface {
	PozicijaNaudotojasdatagramprotocolPranešimas(data uintptr, dydis uint16)
}
type TNaudotojasdatagramprotocolLizdas struct {
	nutolęsPrievadasSkaičius	uint16
	nutolęsip			uint32
	vietinisPrievadasSkaičius	uint16
	vietinisip			uint32

	listening	bool
}

var udpprovider TNaudotojasdatagramprotocolprovider
var udphandler INaudotojasdatagramprotocolhandler

func (self *TNaudotojasdatagramprotocolLizdas) Testas() {
}
func (self *TNaudotojasdatagramprotocolLizdas) Init(pudpprovider TNaudotojasdatagramprotocolprovider, pudphandler INaudotojasdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TNaudotojasdatagramprotocolLizdas) PozicijaNaudotojasdatagramprotocolPranešimas(data uintptr, dydis uint16) {
	if udphandler != nil {
		udphandler.PozicijaNaudotojasdatagramprotocolPranešimas(self, data, dydis)
	}
}
func (self *TNaudotojasdatagramprotocolLizdas) Siųsti(pdata []byte, dydis uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(dydis); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Siųsti(self, data, dydis)
}
func (self *TNaudotojasdatagramprotocolLizdas) Atsijungti() {
	udpprovider.Atsijungti(self)
}

type TNaudotojasdatagramprotocolprovider struct {
}

var iphandler IInternetasprotocolhandler
var sockets [65535]TNaudotojasdatagramprotocolLizdas
var skaičiussockets int
var laisvaPrievadas uint16

func (self *TNaudotojasdatagramprotocolprovider) Init(pipprovider TInternetasprotocolprovider, piphandler IInternetasprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	skaičiussockets = 0
	laisvaPrievadas = 1024
}
func (self *TNaudotojasdatagramprotocolprovider) Internetasprotocolreceivewhen(šaltinisipaddressTinklasbyteorder uint32, tikslasipaddressTinklasbyteorder uint32, internetasprotocolpayload uintptr, dydis uint32) bool {
	if dydis < udpheaderDydis {
		return false
	}

	var buffer_2 *TNaudotojasdatagramprotocolheaderbuffer = (*TNaudotojasdatagramprotocolheaderbuffer)(Pointer(internetasprotocolpayload))
	var msg TNaudotojasdatagramprotocolheader
	msg.Init(buffer_2)

	var lizdas *TNaudotojasdatagramprotocolLizdas = nil

	for i := 0; i < skaičiussockets && lizdas == nil; i++ {
		if sockets[i].vietinisPrievadasSkaičius == msg.tikslasPrievadasSkaičius && sockets[i].vietinisip == tikslasipaddressTinklasbyteorder && sockets[i].listening == true {
			lizdas = &sockets[i]
			lizdas.listening = false
			lizdas.nutolęsPrievadasSkaičius = msg.šaltinisPrievadasSkaičius
			lizdas.nutolęsip = šaltinisipaddressTinklasbyteorder
		} else if sockets[i].vietinisPrievadasSkaičius == msg.tikslasPrievadasSkaičius && sockets[i].vietinisip == tikslasipaddressTinklasbyteorder && sockets[i].nutolęsPrievadasSkaičius == msg.šaltinisPrievadasSkaičius && sockets[i].nutolęsip == šaltinisipaddressTinklasbyteorder {
			lizdas = &sockets[i]

		}
	}

	msg.Nustatytabuffer(buffer_2)
	if lizdas != nil {
		lizdas.PozicijaNaudotojasdatagramprotocolPranešimas(internetasprotocolpayload+uintptr(udpheaderDydis), uint16(dydis-udpheaderDydis))
	}

	return false
}

func (self *TNaudotojasdatagramprotocolprovider) Prisijungti(ip uint32, prievadas uint16) *TNaudotojasdatagramprotocolLizdas {
	var atmintismanager = &TAtmintismanager{}
	var lizdas = (*TNaudotojasdatagramprotocolLizdas)(atmintismanager.Malloc(50))

	if lizdas != nil {

		lizdas.Init(*self, nil)
		lizdas.nutolęsPrievadasSkaičius = prievadas
		lizdas.nutolęsip = ip
		lizdas.vietinisPrievadasSkaičius = laisvaPrievadas
		laisvaPrievadas++
		lizdas.vietinisip = uint32((*iphandler.Providerget()).Getipaddress())

		lizdas.nutolęsPrievadasSkaičius = Unsignedinteger16r(lizdas.nutolęsPrievadasSkaičius)
		lizdas.vietinisPrievadasSkaičius = Unsignedinteger16r(lizdas.vietinisPrievadasSkaičius)

		sockets[skaičiussockets] = *lizdas
		skaičiussockets++

	}
	return lizdas

}
func (self *TNaudotojasdatagramprotocolprovider) Listen(prievadas uint16) *TNaudotojasdatagramprotocolLizdas {
	var lizdas = &TNaudotojasdatagramprotocolLizdas{}
	lizdas = nil
	if lizdas != nil {
		lizdas.Init(*self, nil)
		lizdas.listening = true
		lizdas.vietinisPrievadasSkaičius = prievadas
		lizdas.vietinisip = uint32((*iphandler.Providerget()).Getipaddress())

		lizdas.vietinisPrievadasSkaičius = Unsignedinteger16r(lizdas.vietinisPrievadasSkaičius)
	}
	return lizdas
}
func (self *TNaudotojasdatagramprotocolprovider) Atsijungti(lizdas *TNaudotojasdatagramprotocolLizdas) {
	for i := 0; i < skaičiussockets && lizdas == nil; i++ {
		if sockets[i] == *lizdas {
			skaičiussockets--
			sockets[i] = sockets[skaičiussockets]
			break
		}
	}
}
func (self *TNaudotojasdatagramprotocolprovider) Siųsti(lizdas *TNaudotojasdatagramprotocolLizdas, pdata uintptr, dydis uint16) {
	var išvisoTrukmė = uint32(dydis) + udpheaderDydis

	var buffer_2 [4096]byte

	var msgbuffer = (*TNaudotojasdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TNaudotojasdatagramprotocolheader{}

	msg.šaltinisPrievadasSkaičius = lizdas.vietinisPrievadasSkaičius
	msg.tikslasPrievadasSkaičius = lizdas.nutolęsPrievadasSkaičius
	msg.trukmė = Unsignedinteger16r(uint16(išvisoTrukmė))

	msg.kontrolinėsuma = 0x0
	msg.Nustatytabuffer(msgbuffer)

	var dataBaitų [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(dydis); i++ {
		buffer_2[int(udpheaderDydis)+i] = dataBaitų[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Siųsti(lizdas.nutolęsip, 0x11, data, išvisoTrukmė)

}
func (self *TNaudotojasdatagramprotocolprovider) Bind(lizdas *TNaudotojasdatagramprotocolLizdas, handler *TNaudotojasdatagramprotocolhandler) {
}
