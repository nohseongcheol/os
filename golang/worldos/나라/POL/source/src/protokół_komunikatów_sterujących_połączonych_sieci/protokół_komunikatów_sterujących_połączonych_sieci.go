/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protokół_komunikatów_sterujących_połączonych_sieci

import . "unsafe"
import . "konsola"
import . "pamięćmanager"
import . "ramka_sieci_o_wspólnym_medium"
import . "protokół_połączonych_sieci_4"
import . "util"

var icmpKonsola = TKonsola{}

type TInternetSterowanieWiadomośćprotocolWiadomośćbuffer struct {
	Typ	byte
	code	byte

	sumakontrolna	[2]byte
	data		[4]byte
}

var icmpRozmiar int = 64

type TInternetSterowanieWiadomośćprotocolWiadomość struct {
	Typ	uint8
	code	uint8

	sumakontrolna	uint16
	data		uint32
}

func (bieżący *TInternetSterowanieWiadomośćprotocolWiadomość) Init(buffer_2 TInternetSterowanieWiadomośćprotocolWiadomośćbuffer) {
	bieżący.Typ = buffer_2.Typ
	bieżący.code = buffer_2.code

	bieżący.sumakontrolna = Unsignedinteger16r(Tablicatounsignedinteger16(buffer_2.sumakontrolna))
	bieżący.data = Unsignedinteger32r(Tablicatounsignedinteger32(buffer_2.data))
}

func (bieżący *TInternetSterowanieWiadomośćprotocolWiadomość) Zbiórbuffer(buffer_2 *TInternetSterowanieWiadomośćprotocolWiadomośćbuffer) {
	buffer_2.Typ = bieżący.Typ
	buffer_2.code = bieżący.code

	buffer_2.sumakontrolna = Unsignedinteger16toTablica(bieżący.sumakontrolna)
	buffer_2.data = Unsignedinteger32toTablica(bieżący.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var protokół_komunikatów_sterujących_połączonych_sieci *TProtokół_komunikatów_sterujących_połączonych_sieci

func (bieżący *Icmphandler) Internetprotocolreceivewhen(źródłoipAdresSiećbyteorder uint32, celipAdresSiećbyteorder uint32, dataKursor uintptr, rozmiar uint32) bool {
	return protokół_komunikatów_sterujących_połączonych_sieci.Internetprotocolreceivewhen(źródłoipAdresSiećbyteorder, celipAdresSiećbyteorder, dataKursor, rozmiar)
}

var iphandler IInternetprotocolhandler

type TProtokół_komunikatów_sterujących_połączonych_sieci struct {
}

func (bieżący *TProtokół_komunikatów_sterujących_połączonych_sieci) Init(backend TDostawca_protokołu_połączonych_sieci, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	protokół_komunikatów_sterujących_połączonych_sieci = bieżący
}
func (bieżący *TProtokół_komunikatów_sterujących_połączonych_sieci) Internetprotocolreceivewhen(źródłoipAdresSiećbyteorder uint32, celipAdresSiećbyteorder uint32, dataKursor uintptr, rozmiar uint32) bool {
	if rozmiar < uint32(icmpRozmiar) {
		return false
	}

	var buffer_2 *TInternetSterowanieWiadomośćprotocolWiadomośćbuffer = (*TInternetSterowanieWiadomośćprotocolWiadomośćbuffer)(Pointer(dataKursor))
	var msg TInternetSterowanieWiadomośćprotocolWiadomość = TInternetSterowanieWiadomośćprotocolWiadomość{}
	msg.Init(*buffer_2)

	icmpKonsola.MWydrukuj(([]byte)("icmp:OnInternet"))
	icmpKonsola.MUnsignedinteger16Wydrukuj(uint16(msg.Typ))
	icmpKonsola.MWydrukuj(([]byte)(":"))

	switch msg.Typ {
	case 0:
		icmpKonsola.MWydrukuj(([]byte)("ping response from "))
		break

	case 8:
		icmpKonsola.MWydrukuj(([]byte)("ping send "))
		msg.Typ = 0

		msg.sumakontrolna = 0
		msg.Zbiórbuffer(buffer_2)
		msg.sumakontrolna = iphandler.Providerget().Sumakontrolna((*([4096]uint16))(Pointer(dataKursor)), uint32(icmpRozmiar))

		msg.Zbiórbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (bieżący *TProtokół_komunikatów_sterujących_połączonych_sieci) EchorequestWyślij(ipSiećbyteorder uint32) bool {
	var protokół_komunikatów_sterujących_połączonych_sieci TInternetSterowanieWiadomośćprotocolWiadomość = TInternetSterowanieWiadomośćprotocolWiadomość{}

	var pamięćmanager = &TPamięćmanager{}
	var buffer_2 = (*TInternetSterowanieWiadomośćprotocolWiadomośćbuffer)(pamięćmanager.Przydziel_pamięć(1024))

	protokół_komunikatów_sterujących_połączonych_sieci.Typ = 8
	protokół_komunikatów_sterujących_połączonych_sieci.code = 0
	protokół_komunikatów_sterujących_połączonych_sieci.data = 0x3713
	protokół_komunikatów_sterujących_połączonych_sieci.sumakontrolna = 0
	protokół_komunikatów_sterujących_połączonych_sieci.Zbiórbuffer(buffer_2)
	protokół_komunikatów_sterujących_połączonych_sieci.sumakontrolna = iphandler.Providerget().Sumakontrolna((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpRozmiar))
	protokół_komunikatów_sterujących_połączonych_sieci.Zbiórbuffer(buffer_2)

	var dataKursor uintptr = uintptr(Pointer(buffer_2))
	iphandler.Wyślij(ipSiećbyteorder, 0x01, dataKursor, uint32(icmpRozmiar))

	return false

}
