/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package användardatagramprotokoll

import . "unsafe"
import . "konsol"
import . "util"
import . "minnemanager"
import . "protokoll_för_sammankopplade_nät_4"

var udpKonsol = TKonsol{}

type TAnvändaredatagramprotocolheaderbuffer struct {
	källportnummer	[2]byte
	målportnummer	[2]byte

	längd		[2]byte
	kontrollsumma	[2]byte
}

var udpheaderStorlek uint32 = 8

type THuvud_för_användardatagram struct {
	källportnummer	uint16
	målportnummer	uint16

	längd		uint16
	kontrollsumma	uint16
}

func (själv *THuvud_för_användardatagram) Init(buffer_2 *TAnvändaredatagramprotocolheaderbuffer) {
	själv.källportnummer = Vektortounsignedinteger16(buffer_2.källportnummer)
	själv.målportnummer = Vektortounsignedinteger16(buffer_2.målportnummer)

	själv.längd = Vektortounsignedinteger16(buffer_2.längd)
	själv.kontrollsumma = Vektortounsignedinteger16(buffer_2.kontrollsumma)
}
func (själv *THuvud_för_användardatagram) Mängdbuffer(buffer_2 *TAnvändaredatagramprotocolheaderbuffer) {

	buffer_2.källportnummer = Unsignedinteger16toVektor(själv.källportnummer)
	buffer_2.målportnummer = Unsignedinteger16toVektor(själv.målportnummer)

	buffer_2.längd = Unsignedinteger16toVektor(själv.längd)
	buffer_2.kontrollsumma = Unsignedinteger16toVektor(själv.kontrollsumma)

}

type IAnvändaredatagramprotocolhandler interface {
	HandtagAnvändaredatagramprotocolMeddelande(uttag *TSlutpunkt_för_användardatagram, data uintptr, storlek uint16)
}

type TAnvändaredatagramprotocolhandler struct {
}

func (själv *TAnvändaredatagramprotocolhandler) Init(backend TProtokolleverantör_för_sammankopplade_nät) {
}
func (själv *TAnvändaredatagramprotocolhandler) HandtagAnvändaredatagramprotocolMeddelande(uttag *TSlutpunkt_för_användardatagram, data uintptr, storlek uint16) {
}

type IAnvändaredatagramprotocolUttag interface {
	HandtagAnvändaredatagramprotocolMeddelande(data uintptr, storlek uint16)
}
type TSlutpunkt_för_användardatagram struct {
	fjärrportNummer	uint16
	fjärrip		uint32
	lokalportNummer	uint16
	lokalip		uint32

	listening	bool
}

var udpprovider TAnvändaredatagramprotocolprovider
var udphandler IAnvändaredatagramprotocolhandler

func (själv *TSlutpunkt_för_användardatagram) Testa() {
}
func (själv *TSlutpunkt_för_användardatagram) Init(pudpprovider TAnvändaredatagramprotocolprovider, pudphandler IAnvändaredatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	själv.listening = false
}
func (själv *TSlutpunkt_för_användardatagram) HandtagAnvändaredatagramprotocolMeddelande(data uintptr, storlek uint16) {
	if udphandler != nil {
		udphandler.HandtagAnvändaredatagramprotocolMeddelande(själv, data, storlek)
	}
}
func (själv *TSlutpunkt_för_användardatagram) Skicka(pdata []byte, storlek uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(storlek); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Skicka(själv, data, storlek)
}
func (själv *TSlutpunkt_för_användardatagram) Kopplaifrån() {
	udpprovider.Kopplaifrån(själv)
}

type TAnvändaredatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TSlutpunkt_för_användardatagram
var nummersockets int
var ledigtport uint16

func (själv *TAnvändaredatagramprotocolprovider) Init(pipprovider TProtokolleverantör_för_sammankopplade_nät, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	nummersockets = 0
	ledigtport = 1024
}
func (själv *TAnvändaredatagramprotocolprovider) Internetprotocolreceivewhen(källaipAdressNätverkbyteorder uint32, målipAdressNätverkbyteorder uint32, internetprotocolpayload uintptr, storlek uint32) bool {
	if storlek < udpheaderStorlek {
		return false
	}

	var buffer_2 *TAnvändaredatagramprotocolheaderbuffer = (*TAnvändaredatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg THuvud_för_användardatagram
	msg.Init(buffer_2)

	var uttag *TSlutpunkt_för_användardatagram = nil

	for i := 0; i < nummersockets && uttag == nil; i++ {
		if sockets[i].lokalportNummer == msg.målportnummer && sockets[i].lokalip == målipAdressNätverkbyteorder && sockets[i].listening == true {
			uttag = &sockets[i]
			uttag.listening = false
			uttag.fjärrportNummer = msg.källportnummer
			uttag.fjärrip = källaipAdressNätverkbyteorder
		} else if sockets[i].lokalportNummer == msg.målportnummer && sockets[i].lokalip == målipAdressNätverkbyteorder && sockets[i].fjärrportNummer == msg.källportnummer && sockets[i].fjärrip == källaipAdressNätverkbyteorder {
			uttag = &sockets[i]

		}
	}

	msg.Mängdbuffer(buffer_2)
	if uttag != nil {
		uttag.HandtagAnvändaredatagramprotocolMeddelande(internetprotocolpayload+uintptr(udpheaderStorlek), uint16(storlek-udpheaderStorlek))
	}

	return false
}

func (själv *TAnvändaredatagramprotocolprovider) Anslut(ip uint32, port uint16) *TSlutpunkt_för_användardatagram {
	var minnemanager = &TMinnemanager{}
	var uttag = (*TSlutpunkt_för_användardatagram)(minnemanager.Tilldela_minne(50))

	if uttag != nil {

		uttag.Init(*själv, nil)
		uttag.fjärrportNummer = port
		uttag.fjärrip = ip
		uttag.lokalportNummer = ledigtport
		ledigtport++
		uttag.lokalip = uint32((*iphandler.Providerget()).GetipAdress())

		uttag.fjärrportNummer = Unsignedinteger16r(uttag.fjärrportNummer)
		uttag.lokalportNummer = Unsignedinteger16r(uttag.lokalportNummer)

		sockets[nummersockets] = *uttag
		nummersockets++

	}
	return uttag

}
func (själv *TAnvändaredatagramprotocolprovider) Listen(port uint16) *TSlutpunkt_för_användardatagram {
	var uttag = &TSlutpunkt_för_användardatagram{}
	uttag = nil
	if uttag != nil {
		uttag.Init(*själv, nil)
		uttag.listening = true
		uttag.lokalportNummer = port
		uttag.lokalip = uint32((*iphandler.Providerget()).GetipAdress())

		uttag.lokalportNummer = Unsignedinteger16r(uttag.lokalportNummer)
	}
	return uttag
}
func (själv *TAnvändaredatagramprotocolprovider) Kopplaifrån(uttag *TSlutpunkt_för_användardatagram) {
	for i := 0; i < nummersockets && uttag == nil; i++ {
		if sockets[i] == *uttag {
			nummersockets--
			sockets[i] = sockets[nummersockets]
			break
		}
	}
}
func (själv *TAnvändaredatagramprotocolprovider) Skicka(uttag *TSlutpunkt_för_användardatagram, pdata uintptr, storlek uint16) {
	var totaltLängd = uint32(storlek) + udpheaderStorlek

	var buffer_2 [4096]byte

	var msgbuffer = (*TAnvändaredatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = THuvud_för_användardatagram{}

	msg.källportnummer = uttag.lokalportNummer
	msg.målportnummer = uttag.fjärrportNummer
	msg.längd = Unsignedinteger16r(uint16(totaltLängd))

	msg.kontrollsumma = 0x0
	msg.Mängdbuffer(msgbuffer)

	var dataByte [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(storlek); i++ {
		buffer_2[int(udpheaderStorlek)+i] = dataByte[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Skicka(uttag.fjärrip, 0x11, data, totaltLängd)

}
func (själv *TAnvändaredatagramprotocolprovider) Bind(uttag *TSlutpunkt_för_användardatagram, handler *TAnvändaredatagramprotocolhandler) {
}
