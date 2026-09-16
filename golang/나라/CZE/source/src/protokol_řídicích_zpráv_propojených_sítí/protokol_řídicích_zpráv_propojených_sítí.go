/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protokol_řídicích_zpráv_propojených_sítí

import . "unsafe"
import . "konzole"
import . "paměťmanager"
import . "rámec_sítě_se_sdíleným_médiem"
import . "protokol_propojených_sítí_4"
import . "util"

var icmpKonzole = TKonzole{}

type TInternetOvládáníZprávaprotocolZprávabuffer struct {
	Typ	byte
	code	byte

	kontrolnísoučet	[2]byte
	data		[4]byte
}

var icmpVelikost int = 64

type TInternetOvládáníZprávaprotocolZpráva struct {
	Typ	uint8
	code	uint8

	kontrolnísoučet	uint16
	data		uint32
}

func (self *TInternetOvládáníZprávaprotocolZpráva) Init(buffer_2 TInternetOvládáníZprávaprotocolZprávabuffer) {
	self.Typ = buffer_2.Typ
	self.code = buffer_2.code

	self.kontrolnísoučet = Unsignedinteger16r(Poledounsignedinteger16(buffer_2.kontrolnísoučet))
	self.data = Unsignedinteger32r(Poledounsignedinteger32(buffer_2.data))
}

func (self *TInternetOvládáníZprávaprotocolZpráva) Nastavitbuffer(buffer_2 *TInternetOvládáníZprávaprotocolZprávabuffer) {
	buffer_2.Typ = self.Typ
	buffer_2.code = self.code

	buffer_2.kontrolnísoučet = Unsignedinteger16doPole(self.kontrolnísoučet)
	buffer_2.data = Unsignedinteger32doPole(self.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var protokol_řídicích_zpráv_propojených_sítí *TProtokol_řídicích_zpráv_propojených_sítí

func (self *Icmphandler) Internetprotocolreceivewhen(zdrojipAdresaSíťbyteorder uint32, cílipAdresaSíťbyteorder uint32, dataKurzor uintptr, velikost uint32) bool {
	return protokol_řídicích_zpráv_propojených_sítí.Internetprotocolreceivewhen(zdrojipAdresaSíťbyteorder, cílipAdresaSíťbyteorder, dataKurzor, velikost)
}

var iphandler IInternetprotocolhandler

type TProtokol_řídicích_zpráv_propojených_sítí struct {
}

func (self *TProtokol_řídicích_zpráv_propojených_sítí) Init(backend TPoskytovatel_protokolu_propojených_sítí, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	protokol_řídicích_zpráv_propojených_sítí = self
}
func (self *TProtokol_řídicích_zpráv_propojených_sítí) Internetprotocolreceivewhen(zdrojipAdresaSíťbyteorder uint32, cílipAdresaSíťbyteorder uint32, dataKurzor uintptr, velikost uint32) bool {
	if velikost < uint32(icmpVelikost) {
		return false
	}

	var buffer_2 *TInternetOvládáníZprávaprotocolZprávabuffer = (*TInternetOvládáníZprávaprotocolZprávabuffer)(Pointer(dataKurzor))
	var msg TInternetOvládáníZprávaprotocolZpráva = TInternetOvládáníZprávaprotocolZpráva{}
	msg.Init(*buffer_2)

	icmpKonzole.MTisknout(([]byte)("icmp:OnInternet"))
	icmpKonzole.MUnsignedinteger16Tisknout(uint16(msg.Typ))
	icmpKonzole.MTisknout(([]byte)(":"))

	switch msg.Typ {
	case 0:
		icmpKonzole.MTisknout(([]byte)("ping response from "))
		break

	case 8:
		icmpKonzole.MTisknout(([]byte)("ping send "))
		msg.Typ = 0

		msg.kontrolnísoučet = 0
		msg.Nastavitbuffer(buffer_2)
		msg.kontrolnísoučet = iphandler.Providerget().Kontrolnísoučet((*([4096]uint16))(Pointer(dataKurzor)), uint32(icmpVelikost))

		msg.Nastavitbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TProtokol_řídicích_zpráv_propojených_sítí) EchorequestPoslat(ipSíťbyteorder uint32) bool {
	var protokol_řídicích_zpráv_propojených_sítí TInternetOvládáníZprávaprotocolZpráva = TInternetOvládáníZprávaprotocolZpráva{}

	var paměťmanager = &TPaměťmanager{}
	var buffer_2 = (*TInternetOvládáníZprávaprotocolZprávabuffer)(paměťmanager.Přidělit_paměť(1024))

	protokol_řídicích_zpráv_propojených_sítí.Typ = 8
	protokol_řídicích_zpráv_propojených_sítí.code = 0
	protokol_řídicích_zpráv_propojených_sítí.data = 0x3713
	protokol_řídicích_zpráv_propojených_sítí.kontrolnísoučet = 0
	protokol_řídicích_zpráv_propojených_sítí.Nastavitbuffer(buffer_2)
	protokol_řídicích_zpráv_propojených_sítí.kontrolnísoučet = iphandler.Providerget().Kontrolnísoučet((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpVelikost))
	protokol_řídicích_zpráv_propojených_sítí.Nastavitbuffer(buffer_2)

	var dataKurzor uintptr = uintptr(Pointer(buffer_2))
	iphandler.Poslat(ipSíťbyteorder, 0x01, dataKurzor, uint32(icmpVelikost))

	return false

}
