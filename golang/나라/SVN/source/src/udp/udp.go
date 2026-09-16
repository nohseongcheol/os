/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "pomnilnikmanager"
import . "ipv4"

var udpconsole = TConsole{}

type TUporabnikdatagramprotocolheaderbuffer struct {
	virVrataŠtevilka	[2]byte
	ciljVrataŠtevilka	[2]byte

	dolžina		[2]byte
	checksum	[2]byte
}

var udpheaderVelikost uint32 = 8

type TUporabnikdatagramprotocolheader struct {
	virVrataŠtevilka	uint16
	ciljVrataŠtevilka	uint16

	dolžina		uint16
	checksum	uint16
}

func (sam *TUporabnikdatagramprotocolheader) Init(buffer_2 *TUporabnikdatagramprotocolheaderbuffer) {
	sam.virVrataŠtevilka = Poljetounsignedinteger16(buffer_2.virVrataŠtevilka)
	sam.ciljVrataŠtevilka = Poljetounsignedinteger16(buffer_2.ciljVrataŠtevilka)

	sam.dolžina = Poljetounsignedinteger16(buffer_2.dolžina)
	sam.checksum = Poljetounsignedinteger16(buffer_2.checksum)
}
func (sam *TUporabnikdatagramprotocolheader) Množicabuffer(buffer_2 *TUporabnikdatagramprotocolheaderbuffer) {

	buffer_2.virVrataŠtevilka = Unsignedinteger16toPolje(sam.virVrataŠtevilka)
	buffer_2.ciljVrataŠtevilka = Unsignedinteger16toPolje(sam.ciljVrataŠtevilka)

	buffer_2.dolžina = Unsignedinteger16toPolje(sam.dolžina)
	buffer_2.checksum = Unsignedinteger16toPolje(sam.checksum)

}

type IUporabnikdatagramprotocolhandler interface {
	RočicaUporabnikdatagramprotocolSporočilo(vti *TUporabnikdatagramprotocolVti, data uintptr, velikost uint16)
}

type TUporabnikdatagramprotocolhandler struct {
}

func (sam *TUporabnikdatagramprotocolhandler) Init(backend TSpletprotocolprovider) {
}
func (sam *TUporabnikdatagramprotocolhandler) RočicaUporabnikdatagramprotocolSporočilo(vti *TUporabnikdatagramprotocolVti, data uintptr, velikost uint16) {
}

type IUporabnikdatagramprotocolVti interface {
	RočicaUporabnikdatagramprotocolSporočilo(data uintptr, velikost uint16)
}
type TUporabnikdatagramprotocolVti struct {
	oddaljenoVrataŠtevilka	uint16
	oddaljenoip		uint32
	krajevnoVrataŠtevilka	uint16
	krajevnoip		uint32

	listening	bool
}

var udpprovider TUporabnikdatagramprotocolprovider
var udphandler IUporabnikdatagramprotocolhandler

func (sam *TUporabnikdatagramprotocolVti) Preizkus() {
}
func (sam *TUporabnikdatagramprotocolVti) Init(pudpprovider TUporabnikdatagramprotocolprovider, pudphandler IUporabnikdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	sam.listening = false
}
func (sam *TUporabnikdatagramprotocolVti) RočicaUporabnikdatagramprotocolSporočilo(data uintptr, velikost uint16) {
	if udphandler != nil {
		udphandler.RočicaUporabnikdatagramprotocolSporočilo(sam, data, velikost)
	}
}
func (sam *TUporabnikdatagramprotocolVti) Pošlji(pdata []byte, velikost uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(velikost); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Pošlji(sam, data, velikost)
}
func (sam *TUporabnikdatagramprotocolVti) Prekinipovezavo() {
	udpprovider.Prekinipovezavo(sam)
}

type TUporabnikdatagramprotocolprovider struct {
}

var iphandler ISpletprotocolhandler
var sockets [65535]TUporabnikdatagramprotocolVti
var številkasockets int
var prostoVrata uint16

func (sam *TUporabnikdatagramprotocolprovider) Init(pipprovider TSpletprotocolprovider, piphandler ISpletprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	številkasockets = 0
	prostoVrata = 1024
}
func (sam *TUporabnikdatagramprotocolprovider) Spletprotocolreceivewhen(viripaddressOmrežjebyteorder uint32, ciljipaddressOmrežjebyteorder uint32, spletprotocolpayload uintptr, velikost uint32) bool {
	if velikost < udpheaderVelikost {
		return false
	}

	var buffer_2 *TUporabnikdatagramprotocolheaderbuffer = (*TUporabnikdatagramprotocolheaderbuffer)(Pointer(spletprotocolpayload))
	var msg TUporabnikdatagramprotocolheader
	msg.Init(buffer_2)

	var vti *TUporabnikdatagramprotocolVti = nil

	for i := 0; i < številkasockets && vti == nil; i++ {
		if sockets[i].krajevnoVrataŠtevilka == msg.ciljVrataŠtevilka && sockets[i].krajevnoip == ciljipaddressOmrežjebyteorder && sockets[i].listening == true {
			vti = &sockets[i]
			vti.listening = false
			vti.oddaljenoVrataŠtevilka = msg.virVrataŠtevilka
			vti.oddaljenoip = viripaddressOmrežjebyteorder
		} else if sockets[i].krajevnoVrataŠtevilka == msg.ciljVrataŠtevilka && sockets[i].krajevnoip == ciljipaddressOmrežjebyteorder && sockets[i].oddaljenoVrataŠtevilka == msg.virVrataŠtevilka && sockets[i].oddaljenoip == viripaddressOmrežjebyteorder {
			vti = &sockets[i]

		}
	}

	msg.Množicabuffer(buffer_2)
	if vti != nil {
		vti.RočicaUporabnikdatagramprotocolSporočilo(spletprotocolpayload+uintptr(udpheaderVelikost), uint16(velikost-udpheaderVelikost))
	}

	return false
}

func (sam *TUporabnikdatagramprotocolprovider) Poveži(ip uint32, vrata uint16) *TUporabnikdatagramprotocolVti {
	var pomnilnikmanager = &TPomnilnikmanager{}
	var vti = (*TUporabnikdatagramprotocolVti)(pomnilnikmanager.Malloc(50))

	if vti != nil {

		vti.Init(*sam, nil)
		vti.oddaljenoVrataŠtevilka = vrata
		vti.oddaljenoip = ip
		vti.krajevnoVrataŠtevilka = prostoVrata
		prostoVrata++
		vti.krajevnoip = uint32((*iphandler.Providerget()).Getipaddress())

		vti.oddaljenoVrataŠtevilka = Unsignedinteger16r(vti.oddaljenoVrataŠtevilka)
		vti.krajevnoVrataŠtevilka = Unsignedinteger16r(vti.krajevnoVrataŠtevilka)

		sockets[številkasockets] = *vti
		številkasockets++

	}
	return vti

}
func (sam *TUporabnikdatagramprotocolprovider) Listen(vrata uint16) *TUporabnikdatagramprotocolVti {
	var vti = &TUporabnikdatagramprotocolVti{}
	vti = nil
	if vti != nil {
		vti.Init(*sam, nil)
		vti.listening = true
		vti.krajevnoVrataŠtevilka = vrata
		vti.krajevnoip = uint32((*iphandler.Providerget()).Getipaddress())

		vti.krajevnoVrataŠtevilka = Unsignedinteger16r(vti.krajevnoVrataŠtevilka)
	}
	return vti
}
func (sam *TUporabnikdatagramprotocolprovider) Prekinipovezavo(vti *TUporabnikdatagramprotocolVti) {
	for i := 0; i < številkasockets && vti == nil; i++ {
		if sockets[i] == *vti {
			številkasockets--
			sockets[i] = sockets[številkasockets]
			break
		}
	}
}
func (sam *TUporabnikdatagramprotocolprovider) Pošlji(vti *TUporabnikdatagramprotocolVti, pdata uintptr, velikost uint16) {
	var skupnoDolžina = uint32(velikost) + udpheaderVelikost

	var buffer_2 [4096]byte

	var msgbuffer = (*TUporabnikdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TUporabnikdatagramprotocolheader{}

	msg.virVrataŠtevilka = vti.krajevnoVrataŠtevilka
	msg.ciljVrataŠtevilka = vti.oddaljenoVrataŠtevilka
	msg.dolžina = Unsignedinteger16r(uint16(skupnoDolžina))

	msg.checksum = 0x0
	msg.Množicabuffer(msgbuffer)

	var dataBajtov [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(velikost); i++ {
		buffer_2[int(udpheaderVelikost)+i] = dataBajtov[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Pošlji(vti.oddaljenoip, 0x11, data, skupnoDolžina)

}
func (sam *TUporabnikdatagramprotocolprovider) Bind(vti *TUporabnikdatagramprotocolVti, handler *TUporabnikdatagramprotocolhandler) {
}
