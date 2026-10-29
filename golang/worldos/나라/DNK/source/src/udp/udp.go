/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "hukommelsemanager"
import . "ipv4"

var udpconsole = TConsole{}

type TBrugerdatagramprotocolheaderbuffer struct {
	kildeportTal		[2]byte
	destinationportTal	[2]byte

	længde		[2]byte
	checksum	[2]byte
}

var udpheaderStørrelse uint32 = 8

type TBrugerdatagramprotocolheader struct {
	kildeportTal		uint16
	destinationportTal	uint16

	længde		uint16
	checksum	uint16
}

func (selv *TBrugerdatagramprotocolheader) Init(buffer_2 *TBrugerdatagramprotocolheaderbuffer) {
	selv.kildeportTal = Tabeltounsignedinteger16(buffer_2.kildeportTal)
	selv.destinationportTal = Tabeltounsignedinteger16(buffer_2.destinationportTal)

	selv.længde = Tabeltounsignedinteger16(buffer_2.længde)
	selv.checksum = Tabeltounsignedinteger16(buffer_2.checksum)
}
func (selv *TBrugerdatagramprotocolheader) Satbuffer(buffer_2 *TBrugerdatagramprotocolheaderbuffer) {

	buffer_2.kildeportTal = Unsignedinteger16toTabel(selv.kildeportTal)
	buffer_2.destinationportTal = Unsignedinteger16toTabel(selv.destinationportTal)

	buffer_2.længde = Unsignedinteger16toTabel(selv.længde)
	buffer_2.checksum = Unsignedinteger16toTabel(selv.checksum)

}

type IBrugerdatagramprotocolhandler interface {
	HåndtagBrugerdatagramprotocolMeddelelse(sokkel *TBrugerdatagramprotocolSokkel, data uintptr, størrelse uint16)
}

type TBrugerdatagramprotocolhandler struct {
}

func (selv *TBrugerdatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (selv *TBrugerdatagramprotocolhandler) HåndtagBrugerdatagramprotocolMeddelelse(sokkel *TBrugerdatagramprotocolSokkel, data uintptr, størrelse uint16) {
}

type IBrugerdatagramprotocolSokkel interface {
	HåndtagBrugerdatagramprotocolMeddelelse(data uintptr, størrelse uint16)
}
type TBrugerdatagramprotocolSokkel struct {
	eksternportTal	uint16
	eksternip	uint32
	lokalportTal	uint16
	lokalip		uint32

	listening	bool
}

var udpprovider TBrugerdatagramprotocolprovider
var udphandler IBrugerdatagramprotocolhandler

func (selv *TBrugerdatagramprotocolSokkel) Prøv() {
}
func (selv *TBrugerdatagramprotocolSokkel) Init(pudpprovider TBrugerdatagramprotocolprovider, pudphandler IBrugerdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	selv.listening = false
}
func (selv *TBrugerdatagramprotocolSokkel) HåndtagBrugerdatagramprotocolMeddelelse(data uintptr, størrelse uint16) {
	if udphandler != nil {
		udphandler.HåndtagBrugerdatagramprotocolMeddelelse(selv, data, størrelse)
	}
}
func (selv *TBrugerdatagramprotocolSokkel) Send(pdata []byte, størrelse uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(størrelse); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(selv, data, størrelse)
}
func (selv *TBrugerdatagramprotocolSokkel) Afbryd() {
	udpprovider.Afbryd(selv)
}

type TBrugerdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TBrugerdatagramprotocolSokkel
var talsockets int
var friport uint16

func (selv *TBrugerdatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	talsockets = 0
	friport = 1024
}
func (selv *TBrugerdatagramprotocolprovider) Internetprotocolreceivewhen(kildeipaddressNetværkbyteorder uint32, destinationipaddressNetværkbyteorder uint32, internetprotocolpayload uintptr, størrelse uint32) bool {
	if størrelse < udpheaderStørrelse {
		return false
	}

	var buffer_2 *TBrugerdatagramprotocolheaderbuffer = (*TBrugerdatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TBrugerdatagramprotocolheader
	msg.Init(buffer_2)

	var sokkel *TBrugerdatagramprotocolSokkel = nil

	for i := 0; i < talsockets && sokkel == nil; i++ {
		if sockets[i].lokalportTal == msg.destinationportTal && sockets[i].lokalip == destinationipaddressNetværkbyteorder && sockets[i].listening == true {
			sokkel = &sockets[i]
			sokkel.listening = false
			sokkel.eksternportTal = msg.kildeportTal
			sokkel.eksternip = kildeipaddressNetværkbyteorder
		} else if sockets[i].lokalportTal == msg.destinationportTal && sockets[i].lokalip == destinationipaddressNetværkbyteorder && sockets[i].eksternportTal == msg.kildeportTal && sockets[i].eksternip == kildeipaddressNetværkbyteorder {
			sokkel = &sockets[i]

		}
	}

	msg.Satbuffer(buffer_2)
	if sokkel != nil {
		sokkel.HåndtagBrugerdatagramprotocolMeddelelse(internetprotocolpayload+uintptr(udpheaderStørrelse), uint16(størrelse-udpheaderStørrelse))
	}

	return false
}

func (selv *TBrugerdatagramprotocolprovider) Tilslut(ip uint32, port uint16) *TBrugerdatagramprotocolSokkel {
	var hukommelsemanager = &THukommelsemanager{}
	var sokkel = (*TBrugerdatagramprotocolSokkel)(hukommelsemanager.Malloc(50))

	if sokkel != nil {

		sokkel.Init(*selv, nil)
		sokkel.eksternportTal = port
		sokkel.eksternip = ip
		sokkel.lokalportTal = friport
		friport++
		sokkel.lokalip = uint32((*iphandler.Providerget()).Getipaddress())

		sokkel.eksternportTal = Unsignedinteger16r(sokkel.eksternportTal)
		sokkel.lokalportTal = Unsignedinteger16r(sokkel.lokalportTal)

		sockets[talsockets] = *sokkel
		talsockets++

	}
	return sokkel

}
func (selv *TBrugerdatagramprotocolprovider) Listen(port uint16) *TBrugerdatagramprotocolSokkel {
	var sokkel = &TBrugerdatagramprotocolSokkel{}
	sokkel = nil
	if sokkel != nil {
		sokkel.Init(*selv, nil)
		sokkel.listening = true
		sokkel.lokalportTal = port
		sokkel.lokalip = uint32((*iphandler.Providerget()).Getipaddress())

		sokkel.lokalportTal = Unsignedinteger16r(sokkel.lokalportTal)
	}
	return sokkel
}
func (selv *TBrugerdatagramprotocolprovider) Afbryd(sokkel *TBrugerdatagramprotocolSokkel) {
	for i := 0; i < talsockets && sokkel == nil; i++ {
		if sockets[i] == *sokkel {
			talsockets--
			sockets[i] = sockets[talsockets]
			break
		}
	}
}
func (selv *TBrugerdatagramprotocolprovider) Send(sokkel *TBrugerdatagramprotocolSokkel, pdata uintptr, størrelse uint16) {
	var totalLængde = uint32(størrelse) + udpheaderStørrelse

	var buffer_2 [4096]byte

	var msgbuffer = (*TBrugerdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TBrugerdatagramprotocolheader{}

	msg.kildeportTal = sokkel.lokalportTal
	msg.destinationportTal = sokkel.eksternportTal
	msg.længde = Unsignedinteger16r(uint16(totalLængde))

	msg.checksum = 0x0
	msg.Satbuffer(msgbuffer)

	var dataByte [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(størrelse); i++ {
		buffer_2[int(udpheaderStørrelse)+i] = dataByte[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(sokkel.eksternip, 0x11, data, totalLængde)

}
func (selv *TBrugerdatagramprotocolprovider) Bind(sokkel *TBrugerdatagramprotocolSokkel, handler *TBrugerdatagramprotocolhandler) {
}
