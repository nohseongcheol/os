/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "konzola"
import . "util"
import . "pamäťmanager"
import . "ipv4"

var udpKonzola = TKonzola{}

type TPoužívateľdatagramprotocolheaderbuffer struct {
	zdrojportČíslo	[2]byte
	cieľportČíslo	[2]byte

	dĺžka		[2]byte
	checksum	[2]byte
}

var udpheaderVeľkosť uint32 = 8

type TPoužívateľdatagramprotocolheader struct {
	zdrojportČíslo	uint16
	cieľportČíslo	uint16

	dĺžka		uint16
	checksum	uint16
}

func (vlastný *TPoužívateľdatagramprotocolheader) Init(buffer_2 *TPoužívateľdatagramprotocolheaderbuffer) {
	vlastný.zdrojportČíslo = Poletounsignedinteger16(buffer_2.zdrojportČíslo)
	vlastný.cieľportČíslo = Poletounsignedinteger16(buffer_2.cieľportČíslo)

	vlastný.dĺžka = Poletounsignedinteger16(buffer_2.dĺžka)
	vlastný.checksum = Poletounsignedinteger16(buffer_2.checksum)
}
func (vlastný *TPoužívateľdatagramprotocolheader) Sadabuffer(buffer_2 *TPoužívateľdatagramprotocolheaderbuffer) {

	buffer_2.zdrojportČíslo = Unsignedinteger16toPole(vlastný.zdrojportČíslo)
	buffer_2.cieľportČíslo = Unsignedinteger16toPole(vlastný.cieľportČíslo)

	buffer_2.dĺžka = Unsignedinteger16toPole(vlastný.dĺžka)
	buffer_2.checksum = Unsignedinteger16toPole(vlastný.checksum)

}

type IPoužívateľdatagramprotocolhandler interface {
	UškoPoužívateľdatagramprotocolSpráva(soket *TPoužívateľdatagramprotocolSoket, data uintptr, veľkosť uint16)
}

type TPoužívateľdatagramprotocolhandler struct {
}

func (vlastný *TPoužívateľdatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (vlastný *TPoužívateľdatagramprotocolhandler) UškoPoužívateľdatagramprotocolSpráva(soket *TPoužívateľdatagramprotocolSoket, data uintptr, veľkosť uint16) {
}

type IPoužívateľdatagramprotocolSoket interface {
	UškoPoužívateľdatagramprotocolSpráva(data uintptr, veľkosť uint16)
}
type TPoužívateľdatagramprotocolSoket struct {
	remoteportČíslo		uint16
	remoteip		uint32
	miestnyportČíslo	uint16
	miestnyip		uint32

	listening	bool
}

var udpprovider TPoužívateľdatagramprotocolprovider
var udphandler IPoužívateľdatagramprotocolhandler

func (vlastný *TPoužívateľdatagramprotocolSoket) Otestovať() {
}
func (vlastný *TPoužívateľdatagramprotocolSoket) Init(pudpprovider TPoužívateľdatagramprotocolprovider, pudphandler IPoužívateľdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	vlastný.listening = false
}
func (vlastný *TPoužívateľdatagramprotocolSoket) UškoPoužívateľdatagramprotocolSpráva(data uintptr, veľkosť uint16) {
	if udphandler != nil {
		udphandler.UškoPoužívateľdatagramprotocolSpráva(vlastný, data, veľkosť)
	}
}
func (vlastný *TPoužívateľdatagramprotocolSoket) Poslať(pdata []byte, veľkosť uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(veľkosť); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Poslať(vlastný, data, veľkosť)
}
func (vlastný *TPoužívateľdatagramprotocolSoket) Odpojiť() {
	udpprovider.Odpojiť(vlastný)
}

type TPoužívateľdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TPoužívateľdatagramprotocolSoket
var číslosockets int
var voľnéport uint16

func (vlastný *TPoužívateľdatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	číslosockets = 0
	voľnéport = 1024
}
func (vlastný *TPoužívateľdatagramprotocolprovider) Internetprotocolreceivewhen(zdrojipaddressSieťbyteorder uint32, cieľipaddressSieťbyteorder uint32, internetprotocolpayload uintptr, veľkosť uint32) bool {
	if veľkosť < udpheaderVeľkosť {
		return false
	}

	var buffer_2 *TPoužívateľdatagramprotocolheaderbuffer = (*TPoužívateľdatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TPoužívateľdatagramprotocolheader
	msg.Init(buffer_2)

	var soket *TPoužívateľdatagramprotocolSoket = nil

	for i := 0; i < číslosockets && soket == nil; i++ {
		if sockets[i].miestnyportČíslo == msg.cieľportČíslo && sockets[i].miestnyip == cieľipaddressSieťbyteorder && sockets[i].listening == true {
			soket = &sockets[i]
			soket.listening = false
			soket.remoteportČíslo = msg.zdrojportČíslo
			soket.remoteip = zdrojipaddressSieťbyteorder
		} else if sockets[i].miestnyportČíslo == msg.cieľportČíslo && sockets[i].miestnyip == cieľipaddressSieťbyteorder && sockets[i].remoteportČíslo == msg.zdrojportČíslo && sockets[i].remoteip == zdrojipaddressSieťbyteorder {
			soket = &sockets[i]

		}
	}

	msg.Sadabuffer(buffer_2)
	if soket != nil {
		soket.UškoPoužívateľdatagramprotocolSpráva(internetprotocolpayload+uintptr(udpheaderVeľkosť), uint16(veľkosť-udpheaderVeľkosť))
	}

	return false
}

func (vlastný *TPoužívateľdatagramprotocolprovider) Pripojiť(ip uint32, port uint16) *TPoužívateľdatagramprotocolSoket {
	var pamäťmanager = &TPamäťmanager{}
	var soket = (*TPoužívateľdatagramprotocolSoket)(pamäťmanager.Malloc(50))

	if soket != nil {

		soket.Init(*vlastný, nil)
		soket.remoteportČíslo = port
		soket.remoteip = ip
		soket.miestnyportČíslo = voľnéport
		voľnéport++
		soket.miestnyip = uint32((*iphandler.Providerget()).Getipaddress())

		soket.remoteportČíslo = Unsignedinteger16r(soket.remoteportČíslo)
		soket.miestnyportČíslo = Unsignedinteger16r(soket.miestnyportČíslo)

		sockets[číslosockets] = *soket
		číslosockets++

	}
	return soket

}
func (vlastný *TPoužívateľdatagramprotocolprovider) Listen(port uint16) *TPoužívateľdatagramprotocolSoket {
	var soket = &TPoužívateľdatagramprotocolSoket{}
	soket = nil
	if soket != nil {
		soket.Init(*vlastný, nil)
		soket.listening = true
		soket.miestnyportČíslo = port
		soket.miestnyip = uint32((*iphandler.Providerget()).Getipaddress())

		soket.miestnyportČíslo = Unsignedinteger16r(soket.miestnyportČíslo)
	}
	return soket
}
func (vlastný *TPoužívateľdatagramprotocolprovider) Odpojiť(soket *TPoužívateľdatagramprotocolSoket) {
	for i := 0; i < číslosockets && soket == nil; i++ {
		if sockets[i] == *soket {
			číslosockets--
			sockets[i] = sockets[číslosockets]
			break
		}
	}
}
func (vlastný *TPoužívateľdatagramprotocolprovider) Poslať(soket *TPoužívateľdatagramprotocolSoket, pdata uintptr, veľkosť uint16) {
	var celkomDĺžka = uint32(veľkosť) + udpheaderVeľkosť

	var buffer_2 [4096]byte

	var msgbuffer = (*TPoužívateľdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TPoužívateľdatagramprotocolheader{}

	msg.zdrojportČíslo = soket.miestnyportČíslo
	msg.cieľportČíslo = soket.remoteportČíslo
	msg.dĺžka = Unsignedinteger16r(uint16(celkomDĺžka))

	msg.checksum = 0x0
	msg.Sadabuffer(msgbuffer)

	var dataBajty [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(veľkosť); i++ {
		buffer_2[int(udpheaderVeľkosť)+i] = dataBajty[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Poslať(soket.remoteip, 0x11, data, celkomDĺžka)

}
func (vlastný *TPoužívateľdatagramprotocolprovider) Bind(soket *TPoužívateľdatagramprotocolSoket, handler *TPoužívateľdatagramprotocolhandler,) {
}
