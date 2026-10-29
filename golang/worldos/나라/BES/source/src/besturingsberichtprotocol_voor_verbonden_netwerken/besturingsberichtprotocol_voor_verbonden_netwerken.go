/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package besturingsberichtprotocol_voor_verbonden_netwerken

import . "unsafe"
import . "console"
import . "geheugenmanager"
import . "frame_van_het_gedeelde_medium_netwerk"
import . "protocol_voor_verbonden_netwerken_4"
import . "util"

var icmpconsole = TConsole{}

type TInternetBedieningBerichtprotocolBerichtbuffer struct {
	Soort	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpGrootte int = 64

type TInternetBedieningBerichtprotocolBericht struct {
	Soort	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (zelf *TInternetBedieningBerichtprotocolBericht) Init(buffer_2 TInternetBedieningBerichtprotocolBerichtbuffer) {
	zelf.Soort = buffer_2.Soort
	zelf.code = buffer_2.code

	zelf.checksum = Unsignedinteger16r(Reeksnaarunsignedinteger16(buffer_2.checksum))
	zelf.data = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer_2.data))
}

func (zelf *TInternetBedieningBerichtprotocolBericht) Instellenbuffer(buffer_2 *TInternetBedieningBerichtprotocolBerichtbuffer) {
	buffer_2.Soort = zelf.Soort
	buffer_2.code = zelf.code

	buffer_2.checksum = Unsignedinteger16naarReeks(zelf.checksum)
	buffer_2.data = Unsignedinteger32naarReeks(zelf.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var besturingsberichtprotocol_voor_verbonden_netwerken *TBesturingsberichtprotocol_voor_verbonden_netwerken

func (zelf *Icmphandler) Internetprotocolreceivewhen(bronipaddressNetwerkbyteorder uint32, bestemmingipaddressNetwerkbyteorder uint32, dataMuisaanwijzer uintptr, grootte uint32) bool {
	return besturingsberichtprotocol_voor_verbonden_netwerken.Internetprotocolreceivewhen(bronipaddressNetwerkbyteorder, bestemmingipaddressNetwerkbyteorder, dataMuisaanwijzer, grootte)
}

var iphandler IInternetprotocolhandler

type TBesturingsberichtprotocol_voor_verbonden_netwerken struct {
}

func (zelf *TBesturingsberichtprotocol_voor_verbonden_netwerken) Init(backend TProtocolleverancier_voor_verbonden_netwerken, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	besturingsberichtprotocol_voor_verbonden_netwerken = zelf
}
func (zelf *TBesturingsberichtprotocol_voor_verbonden_netwerken) Internetprotocolreceivewhen(bronipaddressNetwerkbyteorder uint32, bestemmingipaddressNetwerkbyteorder uint32, dataMuisaanwijzer uintptr, grootte uint32) bool {
	if grootte < uint32(icmpGrootte) {
		return false
	}

	var buffer_2 *TInternetBedieningBerichtprotocolBerichtbuffer = (*TInternetBedieningBerichtprotocolBerichtbuffer)(Pointer(dataMuisaanwijzer))
	var msg TInternetBedieningBerichtprotocolBericht = TInternetBedieningBerichtprotocolBericht{}
	msg.Init(*buffer_2)

	icmpconsole.MAfdrukken(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Afdrukken(uint16(msg.Soort))
	icmpconsole.MAfdrukken(([]byte)(":"))

	switch msg.Soort {
	case 0:
		icmpconsole.MAfdrukken(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MAfdrukken(([]byte)("ping send "))
		msg.Soort = 0

		msg.checksum = 0
		msg.Instellenbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataMuisaanwijzer)), uint32(icmpGrootte))

		msg.Instellenbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (zelf *TBesturingsberichtprotocol_voor_verbonden_netwerken) EchorequestVerzenden(ipNetwerkbyteorder uint32) bool {
	var besturingsberichtprotocol_voor_verbonden_netwerken TInternetBedieningBerichtprotocolBericht = TInternetBedieningBerichtprotocolBericht{}

	var geheugenmanager = &TGeheugenmanager{}
	var buffer_2 = (*TInternetBedieningBerichtprotocolBerichtbuffer)(geheugenmanager.Geheugen_toewijzen(1024))

	besturingsberichtprotocol_voor_verbonden_netwerken.Soort = 8
	besturingsberichtprotocol_voor_verbonden_netwerken.code = 0
	besturingsberichtprotocol_voor_verbonden_netwerken.data = 0x3713
	besturingsberichtprotocol_voor_verbonden_netwerken.checksum = 0
	besturingsberichtprotocol_voor_verbonden_netwerken.Instellenbuffer(buffer_2)
	besturingsberichtprotocol_voor_verbonden_netwerken.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpGrootte))
	besturingsberichtprotocol_voor_verbonden_netwerken.Instellenbuffer(buffer_2)

	var dataMuisaanwijzer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Verzenden(ipNetwerkbyteorder, 0x01, dataMuisaanwijzer, uint32(icmpGrootte))

	return false

}
