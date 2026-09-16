/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package verkkojen_ohjausviestien_yhteyskäytäntö

import . "unsafe"
import . "konsoli"
import . "muistimanager"
import . "jaetun_siirtotien_verkkokehys"
import . "verkkojen_yhdyskäytäntö_4"
import . "util"

var icmpKonsoli = TKonsoli{}

type TInternetCtrlViestiprotocolViestibuffer struct {
	Tyyppi	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpKoko int = 64

type TInternetCtrlViestiprotocolViesti struct {
	Tyyppi	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (itse *TInternetCtrlViestiprotocolViesti) Init(buffer_2 TInternetCtrlViestiprotocolViestibuffer) {
	itse.Tyyppi = buffer_2.Tyyppi
	itse.code = buffer_2.code

	itse.checksum = Unsignedinteger16r(Taulukkotounsignedinteger16(buffer_2.checksum))
	itse.data = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer_2.data))
}

func (itse *TInternetCtrlViestiprotocolViesti) Asetabuffer(buffer_2 *TInternetCtrlViestiprotocolViestibuffer) {
	buffer_2.Tyyppi = itse.Tyyppi
	buffer_2.code = itse.code

	buffer_2.checksum = Unsignedinteger16toTaulukko(itse.checksum)
	buffer_2.data = Unsignedinteger32toTaulukko(itse.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var verkkojen_ohjausviestien_yhteyskäytäntö *TVerkkojen_ohjausviestien_yhteyskäytäntö

func (itse *Icmphandler) Internetprotocolreceivewhen(lähdeipaddressVerkkobyteorder uint32, kohdeipaddressVerkkobyteorder uint32, dataOsoitin uintptr, koko uint32) bool {
	return verkkojen_ohjausviestien_yhteyskäytäntö.Internetprotocolreceivewhen(lähdeipaddressVerkkobyteorder, kohdeipaddressVerkkobyteorder, dataOsoitin, koko)
}

var iphandler IInternetprotocolhandler

type TVerkkojen_ohjausviestien_yhteyskäytäntö struct {
}

func (itse *TVerkkojen_ohjausviestien_yhteyskäytäntö) Init(backend TVerkkojen_yhteyskäytännön_tarjoaja, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	verkkojen_ohjausviestien_yhteyskäytäntö = itse
}
func (itse *TVerkkojen_ohjausviestien_yhteyskäytäntö) Internetprotocolreceivewhen(lähdeipaddressVerkkobyteorder uint32, kohdeipaddressVerkkobyteorder uint32, dataOsoitin uintptr, koko uint32) bool {
	if koko < uint32(icmpKoko) {
		return false
	}

	var buffer_2 *TInternetCtrlViestiprotocolViestibuffer = (*TInternetCtrlViestiprotocolViestibuffer)(Pointer(dataOsoitin))
	var msg TInternetCtrlViestiprotocolViesti = TInternetCtrlViestiprotocolViesti{}
	msg.Init(*buffer_2)

	icmpKonsoli.MTulosta(([]byte)("icmp:OnInternet"))
	icmpKonsoli.MUnsignedinteger16Tulosta(uint16(msg.Tyyppi))
	icmpKonsoli.MTulosta(([]byte)(":"))

	switch msg.Tyyppi {
	case 0:
		icmpKonsoli.MTulosta(([]byte)("ping response from "))
		break

	case 8:
		icmpKonsoli.MTulosta(([]byte)("ping send "))
		msg.Tyyppi = 0

		msg.checksum = 0
		msg.Asetabuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataOsoitin)), uint32(icmpKoko))

		msg.Asetabuffer(buffer_2)

		return true
		break
	}
	return false
}

func (itse *TVerkkojen_ohjausviestien_yhteyskäytäntö) EchorequestLähetä(ipVerkkobyteorder uint32) bool {
	var verkkojen_ohjausviestien_yhteyskäytäntö TInternetCtrlViestiprotocolViesti = TInternetCtrlViestiprotocolViesti{}

	var muistimanager = &TMuistimanager{}
	var buffer_2 = (*TInternetCtrlViestiprotocolViestibuffer)(muistimanager.Varaa_muistia(1024))

	verkkojen_ohjausviestien_yhteyskäytäntö.Tyyppi = 8
	verkkojen_ohjausviestien_yhteyskäytäntö.code = 0
	verkkojen_ohjausviestien_yhteyskäytäntö.data = 0x3713
	verkkojen_ohjausviestien_yhteyskäytäntö.checksum = 0
	verkkojen_ohjausviestien_yhteyskäytäntö.Asetabuffer(buffer_2)
	verkkojen_ohjausviestien_yhteyskäytäntö.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpKoko))
	verkkojen_ohjausviestien_yhteyskäytäntö.Asetabuffer(buffer_2)

	var dataOsoitin uintptr = uintptr(Pointer(buffer_2))
	iphandler.Lähetä(ipVerkkobyteorder, 0x01, dataOsoitin, uint32(icmpKoko))

	return false

}
