/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "minnimanager"
import . "ipv4"

var udpconsole = TConsole{}

type TNotandidatagramprotocolheaderbuffer struct {
	uppruniportnumber	[2]byte
	áfangastaðurportnumber	[2]byte

	lengd		[2]byte
	checksum	[2]byte
}

var udpheaderStærð uint32 = 8

type TNotandidatagramprotocolheader struct {
	uppruniportnumber	uint16
	áfangastaðurportnumber	uint16

	lengd		uint16
	checksum	uint16
}

func (sjálft *TNotandidatagramprotocolheader) Init(buffer_2 *TNotandidatagramprotocolheaderbuffer) {
	sjálft.uppruniportnumber = Fylkitounsignedinteger16(buffer_2.uppruniportnumber)
	sjálft.áfangastaðurportnumber = Fylkitounsignedinteger16(buffer_2.áfangastaðurportnumber)

	sjálft.lengd = Fylkitounsignedinteger16(buffer_2.lengd)
	sjálft.checksum = Fylkitounsignedinteger16(buffer_2.checksum)
}
func (sjálft *TNotandidatagramprotocolheader) Setjabuffer(buffer_2 *TNotandidatagramprotocolheaderbuffer) {

	buffer_2.uppruniportnumber = Unsignedinteger16toFylki(sjálft.uppruniportnumber)
	buffer_2.áfangastaðurportnumber = Unsignedinteger16toFylki(sjálft.áfangastaðurportnumber)

	buffer_2.lengd = Unsignedinteger16toFylki(sjálft.lengd)
	buffer_2.checksum = Unsignedinteger16toFylki(sjálft.checksum)

}

type INotandidatagramprotocolhandler interface {
	HaldfangNotandidatagramprotocolSKILABOÐ(sökkull *TNotandidatagramprotocolSökkull, data uintptr, stærð uint16)
}

type TNotandidatagramprotocolhandler struct {
}

func (sjálft *TNotandidatagramprotocolhandler) Init(backend TInternetiðprotocolprovider) {
}
func (sjálft *TNotandidatagramprotocolhandler) HaldfangNotandidatagramprotocolSKILABOÐ(sökkull *TNotandidatagramprotocolSökkull, data uintptr, stærð uint16) {
}

type INotandidatagramprotocolSökkull interface {
	HaldfangNotandidatagramprotocolSKILABOÐ(data uintptr, stærð uint16)
}
type TNotandidatagramprotocolSökkull struct {
	fjarlægtportnumber	uint16
	fjarlægtip		uint32
	staðbundiðportnumber	uint16
	staðbundiðip		uint32

	listening	bool
}

var udpprovider TNotandidatagramprotocolprovider
var udphandler INotandidatagramprotocolhandler

func (sjálft *TNotandidatagramprotocolSökkull) Prófun() {
}
func (sjálft *TNotandidatagramprotocolSökkull) Init(pudpprovider TNotandidatagramprotocolprovider, pudphandler INotandidatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	sjálft.listening = false
}
func (sjálft *TNotandidatagramprotocolSökkull) HaldfangNotandidatagramprotocolSKILABOÐ(data uintptr, stærð uint16) {
	if udphandler != nil {
		udphandler.HaldfangNotandidatagramprotocolSKILABOÐ(sjálft, data, stærð)
	}
}
func (sjálft *TNotandidatagramprotocolSökkull) Senda(pdata []byte, stærð uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(stærð); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Senda(sjálft, data, stærð)
}
func (sjálft *TNotandidatagramprotocolSökkull) Aftengjast() {
	udpprovider.Aftengjast(sjálft)
}

type TNotandidatagramprotocolprovider struct {
}

var iphandler IInternetiðprotocolhandler
var sockets [65535]TNotandidatagramprotocolSökkull
var numbersockets int
var laustport uint16

func (sjálft *TNotandidatagramprotocolprovider) Init(pipprovider TInternetiðprotocolprovider, piphandler IInternetiðprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	laustport = 1024
}
func (sjálft *TNotandidatagramprotocolprovider) Internetiðprotocolreceivewhen(uppruniipaddressNetkerfibyteorder uint32, áfangastaðuripaddressNetkerfibyteorder uint32, internetiðprotocolpayload uintptr, stærð uint32) bool {
	if stærð < udpheaderStærð {
		return false
	}

	var buffer_2 *TNotandidatagramprotocolheaderbuffer = (*TNotandidatagramprotocolheaderbuffer)(Pointer(internetiðprotocolpayload))
	var msg TNotandidatagramprotocolheader
	msg.Init(buffer_2)

	var sökkull *TNotandidatagramprotocolSökkull = nil

	for i := 0; i < numbersockets && sökkull == nil; i++ {
		if sockets[i].staðbundiðportnumber == msg.áfangastaðurportnumber && sockets[i].staðbundiðip == áfangastaðuripaddressNetkerfibyteorder && sockets[i].listening == true {
			sökkull = &sockets[i]
			sökkull.listening = false
			sökkull.fjarlægtportnumber = msg.uppruniportnumber
			sökkull.fjarlægtip = uppruniipaddressNetkerfibyteorder
		} else if sockets[i].staðbundiðportnumber == msg.áfangastaðurportnumber && sockets[i].staðbundiðip == áfangastaðuripaddressNetkerfibyteorder && sockets[i].fjarlægtportnumber == msg.uppruniportnumber && sockets[i].fjarlægtip == uppruniipaddressNetkerfibyteorder {
			sökkull = &sockets[i]

		}
	}

	msg.Setjabuffer(buffer_2)
	if sökkull != nil {
		sökkull.HaldfangNotandidatagramprotocolSKILABOÐ(internetiðprotocolpayload+uintptr(udpheaderStærð), uint16(stærð-udpheaderStærð))
	}

	return false
}

func (sjálft *TNotandidatagramprotocolprovider) Tengjast(ip uint32, port uint16) *TNotandidatagramprotocolSökkull {
	var minnimanager = &TMinnimanager{}
	var sökkull = (*TNotandidatagramprotocolSökkull)(minnimanager.Malloc(50))

	if sökkull != nil {

		sökkull.Init(*sjálft, nil)
		sökkull.fjarlægtportnumber = port
		sökkull.fjarlægtip = ip
		sökkull.staðbundiðportnumber = laustport
		laustport++
		sökkull.staðbundiðip = uint32((*iphandler.Providerget()).Getipaddress())

		sökkull.fjarlægtportnumber = Unsignedinteger16r(sökkull.fjarlægtportnumber)
		sökkull.staðbundiðportnumber = Unsignedinteger16r(sökkull.staðbundiðportnumber)

		sockets[numbersockets] = *sökkull
		numbersockets++

	}
	return sökkull

}
func (sjálft *TNotandidatagramprotocolprovider) Listen(port uint16) *TNotandidatagramprotocolSökkull {
	var sökkull = &TNotandidatagramprotocolSökkull{}
	sökkull = nil
	if sökkull != nil {
		sökkull.Init(*sjálft, nil)
		sökkull.listening = true
		sökkull.staðbundiðportnumber = port
		sökkull.staðbundiðip = uint32((*iphandler.Providerget()).Getipaddress())

		sökkull.staðbundiðportnumber = Unsignedinteger16r(sökkull.staðbundiðportnumber)
	}
	return sökkull
}
func (sjálft *TNotandidatagramprotocolprovider) Aftengjast(sökkull *TNotandidatagramprotocolSökkull) {
	for i := 0; i < numbersockets && sökkull == nil; i++ {
		if sockets[i] == *sökkull {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (sjálft *TNotandidatagramprotocolprovider) Senda(sökkull *TNotandidatagramprotocolSökkull, pdata uintptr, stærð uint16) {
	var totalLengd = uint32(stærð) + udpheaderStærð

	var buffer_2 [4096]byte

	var msgbuffer = (*TNotandidatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TNotandidatagramprotocolheader{}

	msg.uppruniportnumber = sökkull.staðbundiðportnumber
	msg.áfangastaðurportnumber = sökkull.fjarlægtportnumber
	msg.lengd = Unsignedinteger16r(uint16(totalLengd))

	msg.checksum = 0x0
	msg.Setjabuffer(msgbuffer)

	var dataBæti [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(stærð); i++ {
		buffer_2[int(udpheaderStærð)+i] = dataBæti[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Senda(sökkull.fjarlægtip, 0x11, data, totalLengd)

}
func (sjálft *TNotandidatagramprotocolprovider) Bind(sökkull *TNotandidatagramprotocolSökkull, handler *TNotandidatagramprotocolhandler) {
}
