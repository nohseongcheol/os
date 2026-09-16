/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "minnemanager"
import . "ipv4"

var udpconsole = TConsole{}

type TBrukerdatagramprotocolTopptekstbuffer struct {
	kildeportTall	[2]byte
	målportTall	[2]byte

	lengde		[2]byte
	checksum	[2]byte
}

var udpTopptekstStørrelse uint32 = 8

type TBrukerdatagramprotocolTopptekst struct {
	kildeportTall	uint16
	målportTall	uint16

	lengde		uint16
	checksum	uint16
}

func (selv *TBrukerdatagramprotocolTopptekst) Init(buffer_2 *TBrukerdatagramprotocolTopptekstbuffer) {
	selv.kildeportTall = Tabelltounsignedinteger16(buffer_2.kildeportTall)
	selv.målportTall = Tabelltounsignedinteger16(buffer_2.målportTall)

	selv.lengde = Tabelltounsignedinteger16(buffer_2.lengde)
	selv.checksum = Tabelltounsignedinteger16(buffer_2.checksum)
}
func (selv *TBrukerdatagramprotocolTopptekst) Settbuffer(buffer_2 *TBrukerdatagramprotocolTopptekstbuffer) {

	buffer_2.kildeportTall = Unsignedinteger16toTabell(selv.kildeportTall)
	buffer_2.målportTall = Unsignedinteger16toTabell(selv.målportTall)

	buffer_2.lengde = Unsignedinteger16toTabell(selv.lengde)
	buffer_2.checksum = Unsignedinteger16toTabell(selv.checksum)

}

type IBrukerdatagramprotocolhandler interface {
	HåndtakBrukerdatagramprotocolMelding(sokkel *TBrukerdatagramprotocolsokkel, data uintptr, størrelse uint16)
}

type TBrukerdatagramprotocolhandler struct {
}

func (selv *TBrukerdatagramprotocolhandler) Init(backend TInternettprotocolprovider) {
}
func (selv *TBrukerdatagramprotocolhandler) HåndtakBrukerdatagramprotocolMelding(sokkel *TBrukerdatagramprotocolsokkel, data uintptr, størrelse uint16) {
}

type IBrukerdatagramprotocolsokkel interface {
	HåndtakBrukerdatagramprotocolMelding(data uintptr, størrelse uint16)
}
type TBrukerdatagramprotocolsokkel struct {
	remoteportTall	uint16
	remoteip	uint32
	lokalportTall	uint16
	lokalip		uint32

	listening	bool
}

var udpprovider TBrukerdatagramprotocolprovider
var udphandler IBrukerdatagramprotocolhandler

func (selv *TBrukerdatagramprotocolsokkel) Test() {
}
func (selv *TBrukerdatagramprotocolsokkel) Init(pudpprovider TBrukerdatagramprotocolprovider, pudphandler IBrukerdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	selv.listening = false
}
func (selv *TBrukerdatagramprotocolsokkel) HåndtakBrukerdatagramprotocolMelding(data uintptr, størrelse uint16) {
	if udphandler != nil {
		udphandler.HåndtakBrukerdatagramprotocolMelding(selv, data, størrelse)
	}
}
func (selv *TBrukerdatagramprotocolsokkel) Send(pdata []byte, størrelse uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(størrelse); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(selv, data, størrelse)
}
func (selv *TBrukerdatagramprotocolsokkel) Koblefra() {
	udpprovider.Koblefra(selv)
}

type TBrukerdatagramprotocolprovider struct {
}

var iphandler IInternettprotocolhandler
var sockets [65535]TBrukerdatagramprotocolsokkel
var tallsockets int
var ledigport uint16

func (selv *TBrukerdatagramprotocolprovider) Init(pipprovider TInternettprotocolprovider, piphandler IInternettprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	tallsockets = 0
	ledigport = 1024
}
func (selv *TBrukerdatagramprotocolprovider) Internettprotocolreceivewhen(kildeipaddressNettverkbyteorder uint32, målipaddressNettverkbyteorder uint32, internettprotocolpayload uintptr, størrelse uint32) bool {
	if størrelse < udpTopptekstStørrelse {
		return false
	}

	var buffer_2 *TBrukerdatagramprotocolTopptekstbuffer = (*TBrukerdatagramprotocolTopptekstbuffer)(Pointer(internettprotocolpayload))
	var msg TBrukerdatagramprotocolTopptekst
	msg.Init(buffer_2)

	var sokkel *TBrukerdatagramprotocolsokkel = nil

	for i := 0; i < tallsockets && sokkel == nil; i++ {
		if sockets[i].lokalportTall == msg.målportTall && sockets[i].lokalip == målipaddressNettverkbyteorder && sockets[i].listening == true {
			sokkel = &sockets[i]
			sokkel.listening = false
			sokkel.remoteportTall = msg.kildeportTall
			sokkel.remoteip = kildeipaddressNettverkbyteorder
		} else if sockets[i].lokalportTall == msg.målportTall && sockets[i].lokalip == målipaddressNettverkbyteorder && sockets[i].remoteportTall == msg.kildeportTall && sockets[i].remoteip == kildeipaddressNettverkbyteorder {
			sokkel = &sockets[i]

		}
	}

	msg.Settbuffer(buffer_2)
	if sokkel != nil {
		sokkel.HåndtakBrukerdatagramprotocolMelding(internettprotocolpayload+uintptr(udpTopptekstStørrelse), uint16(størrelse-udpTopptekstStørrelse))
	}

	return false
}

func (selv *TBrukerdatagramprotocolprovider) Kobletil(ip uint32, port uint16) *TBrukerdatagramprotocolsokkel {
	var minnemanager = &TMinnemanager{}
	var sokkel = (*TBrukerdatagramprotocolsokkel)(minnemanager.Malloc(50))

	if sokkel != nil {

		sokkel.Init(*selv, nil)
		sokkel.remoteportTall = port
		sokkel.remoteip = ip
		sokkel.lokalportTall = ledigport
		ledigport++
		sokkel.lokalip = uint32((*iphandler.Providerget()).Getipaddress())

		sokkel.remoteportTall = Unsignedinteger16r(sokkel.remoteportTall)
		sokkel.lokalportTall = Unsignedinteger16r(sokkel.lokalportTall)

		sockets[tallsockets] = *sokkel
		tallsockets++

	}
	return sokkel

}
func (selv *TBrukerdatagramprotocolprovider) Listen(port uint16) *TBrukerdatagramprotocolsokkel {
	var sokkel = &TBrukerdatagramprotocolsokkel{}
	sokkel = nil
	if sokkel != nil {
		sokkel.Init(*selv, nil)
		sokkel.listening = true
		sokkel.lokalportTall = port
		sokkel.lokalip = uint32((*iphandler.Providerget()).Getipaddress())

		sokkel.lokalportTall = Unsignedinteger16r(sokkel.lokalportTall)
	}
	return sokkel
}
func (selv *TBrukerdatagramprotocolprovider) Koblefra(sokkel *TBrukerdatagramprotocolsokkel) {
	for i := 0; i < tallsockets && sokkel == nil; i++ {
		if sockets[i] == *sokkel {
			tallsockets--
			sockets[i] = sockets[tallsockets]
			break
		}
	}
}
func (selv *TBrukerdatagramprotocolprovider) Send(sokkel *TBrukerdatagramprotocolsokkel, pdata uintptr, størrelse uint16) {
	var totaltLengde = uint32(størrelse) + udpTopptekstStørrelse

	var buffer_2 [4096]byte

	var msgbuffer = (*TBrukerdatagramprotocolTopptekstbuffer)(Pointer(&buffer_2))

	var msg = TBrukerdatagramprotocolTopptekst{}

	msg.kildeportTall = sokkel.lokalportTall
	msg.målportTall = sokkel.remoteportTall
	msg.lengde = Unsignedinteger16r(uint16(totaltLengde))

	msg.checksum = 0x0
	msg.Settbuffer(msgbuffer)

	var dataByte [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(størrelse); i++ {
		buffer_2[int(udpTopptekstStørrelse)+i] = dataByte[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(sokkel.remoteip, 0x11, data, totaltLengde)

}
func (selv *TBrukerdatagramprotocolprovider) Bind(sokkel *TBrukerdatagramprotocolsokkel, handler *TBrukerdatagramprotocolhandler) {
}
