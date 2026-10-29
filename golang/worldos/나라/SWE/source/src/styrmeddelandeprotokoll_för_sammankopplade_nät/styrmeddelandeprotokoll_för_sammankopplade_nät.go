/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package styrmeddelandeprotokoll_för_sammankopplade_nät

import . "unsafe"
import . "konsol"
import . "minnemanager"
import . "ram_i_nät_med_delat_medium"
import . "protokoll_för_sammankopplade_nät_4"
import . "util"

var icmpKonsol = TKonsol{}

type TInternetCtrlMeddelandeprotocolMeddelandebuffer struct {
	Typ	byte
	code	byte

	kontrollsumma	[2]byte
	data		[4]byte
}

var icmpStorlek int = 64

type TInternetCtrlMeddelandeprotocolMeddelande struct {
	Typ	uint8
	code	uint8

	kontrollsumma	uint16
	data		uint32
}

func (själv *TInternetCtrlMeddelandeprotocolMeddelande) Init(buffer_2 TInternetCtrlMeddelandeprotocolMeddelandebuffer) {
	själv.Typ = buffer_2.Typ
	själv.code = buffer_2.code

	själv.kontrollsumma = Unsignedinteger16r(Vektortounsignedinteger16(buffer_2.kontrollsumma))
	själv.data = Unsignedinteger32r(Vektortounsignedinteger32(buffer_2.data))
}

func (själv *TInternetCtrlMeddelandeprotocolMeddelande) Mängdbuffer(buffer_2 *TInternetCtrlMeddelandeprotocolMeddelandebuffer) {
	buffer_2.Typ = själv.Typ
	buffer_2.code = själv.code

	buffer_2.kontrollsumma = Unsignedinteger16toVektor(själv.kontrollsumma)
	buffer_2.data = Unsignedinteger32toVektor(själv.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var styrmeddelandeprotokoll_för_sammankopplade_nät *TStyrmeddelandeprotokoll_för_sammankopplade_nät

func (själv *Icmphandler) Internetprotocolreceivewhen(källaipAdressNätverkbyteorder uint32, målipAdressNätverkbyteorder uint32, dataMuspekare uintptr, storlek uint32) bool {
	return styrmeddelandeprotokoll_för_sammankopplade_nät.Internetprotocolreceivewhen(källaipAdressNätverkbyteorder, målipAdressNätverkbyteorder, dataMuspekare, storlek)
}

var iphandler IInternetprotocolhandler

type TStyrmeddelandeprotokoll_för_sammankopplade_nät struct {
}

func (själv *TStyrmeddelandeprotokoll_för_sammankopplade_nät) Init(backend TProtokolleverantör_för_sammankopplade_nät, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	styrmeddelandeprotokoll_för_sammankopplade_nät = själv
}
func (själv *TStyrmeddelandeprotokoll_för_sammankopplade_nät) Internetprotocolreceivewhen(källaipAdressNätverkbyteorder uint32, målipAdressNätverkbyteorder uint32, dataMuspekare uintptr, storlek uint32) bool {
	if storlek < uint32(icmpStorlek) {
		return false
	}

	var buffer_2 *TInternetCtrlMeddelandeprotocolMeddelandebuffer = (*TInternetCtrlMeddelandeprotocolMeddelandebuffer)(Pointer(dataMuspekare))
	var msg TInternetCtrlMeddelandeprotocolMeddelande = TInternetCtrlMeddelandeprotocolMeddelande{}
	msg.Init(*buffer_2)

	icmpKonsol.MSkrivut(([]byte)("icmp:OnInternet"))
	icmpKonsol.MUnsignedinteger16Skrivut(uint16(msg.Typ))
	icmpKonsol.MSkrivut(([]byte)(":"))

	switch msg.Typ {
	case 0:
		icmpKonsol.MSkrivut(([]byte)("ping response from "))
		break

	case 8:
		icmpKonsol.MSkrivut(([]byte)("ping send "))
		msg.Typ = 0

		msg.kontrollsumma = 0
		msg.Mängdbuffer(buffer_2)
		msg.kontrollsumma = iphandler.Providerget().Kontrollsumma((*([4096]uint16))(Pointer(dataMuspekare)), uint32(icmpStorlek))

		msg.Mängdbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (själv *TStyrmeddelandeprotokoll_för_sammankopplade_nät) EchorequestSkicka(ipNätverkbyteorder uint32) bool {
	var styrmeddelandeprotokoll_för_sammankopplade_nät TInternetCtrlMeddelandeprotocolMeddelande = TInternetCtrlMeddelandeprotocolMeddelande{}

	var minnemanager = &TMinnemanager{}
	var buffer_2 = (*TInternetCtrlMeddelandeprotocolMeddelandebuffer)(minnemanager.Tilldela_minne(1024))

	styrmeddelandeprotokoll_för_sammankopplade_nät.Typ = 8
	styrmeddelandeprotokoll_för_sammankopplade_nät.code = 0
	styrmeddelandeprotokoll_för_sammankopplade_nät.data = 0x3713
	styrmeddelandeprotokoll_för_sammankopplade_nät.kontrollsumma = 0
	styrmeddelandeprotokoll_för_sammankopplade_nät.Mängdbuffer(buffer_2)
	styrmeddelandeprotokoll_för_sammankopplade_nät.kontrollsumma = iphandler.Providerget().Kontrollsumma((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpStorlek))
	styrmeddelandeprotokoll_för_sammankopplade_nät.Mängdbuffer(buffer_2)

	var dataMuspekare uintptr = uintptr(Pointer(buffer_2))
	iphandler.Skicka(ipNätverkbyteorder, 0x01, dataMuspekare, uint32(icmpStorlek))

	return false

}
