/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "pomnilnikmanager"
import . "ethernetOkvir"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TSpletNadzorSporočiloprotocolSporočilobuffer struct {
	Vrsta	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpVelikost int = 64

type TSpletNadzorSporočiloprotocolSporočilo struct {
	Vrsta	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (sam *TSpletNadzorSporočiloprotocolSporočilo) Init(buffer_2 TSpletNadzorSporočiloprotocolSporočilobuffer) {
	sam.Vrsta = buffer_2.Vrsta
	sam.code = buffer_2.code

	sam.checksum = Unsignedinteger16r(Poljetounsignedinteger16(buffer_2.checksum))
	sam.data = Unsignedinteger32r(Poljetounsignedinteger32(buffer_2.data))
}

func (sam *TSpletNadzorSporočiloprotocolSporočilo) Množicabuffer(buffer_2 *TSpletNadzorSporočiloprotocolSporočilobuffer) {
	buffer_2.Vrsta = sam.Vrsta
	buffer_2.code = sam.code

	buffer_2.checksum = Unsignedinteger16toPolje(sam.checksum)
	buffer_2.data = Unsignedinteger32toPolje(sam.data)
}

type Icmphandler struct {
	TSpletprotocolhandler
}

var icmp *TSpletNadzorSporočiloprotocol

func (sam *Icmphandler) Spletprotocolreceivewhen(viripaddressOmrežjebyteorder uint32, ciljipaddressOmrežjebyteorder uint32, dataKazalnik uintptr, velikost uint32) bool {
	return icmp.Spletprotocolreceivewhen(viripaddressOmrežjebyteorder, ciljipaddressOmrežjebyteorder, dataKazalnik, velikost)
}

var iphandler ISpletprotocolhandler

type TSpletNadzorSporočiloprotocol struct {
}

func (sam *TSpletNadzorSporočiloprotocol) Init(backend TSpletprotocolprovider, handler ISpletprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = sam
}
func (sam *TSpletNadzorSporočiloprotocol) Spletprotocolreceivewhen(viripaddressOmrežjebyteorder uint32, ciljipaddressOmrežjebyteorder uint32, dataKazalnik uintptr, velikost uint32) bool {
	if velikost < uint32(icmpVelikost) {
		return false
	}

	var buffer_2 *TSpletNadzorSporočiloprotocolSporočilobuffer = (*TSpletNadzorSporočiloprotocolSporočilobuffer)(Pointer(dataKazalnik))
	var msg TSpletNadzorSporočiloprotocolSporočilo = TSpletNadzorSporočiloprotocolSporočilo{}
	msg.Init(*buffer_2)

	icmpconsole.MNatisni(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Natisni(uint16(msg.Vrsta))
	icmpconsole.MNatisni(([]byte)(":"))

	switch msg.Vrsta {
	case 0:
		icmpconsole.MNatisni(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MNatisni(([]byte)("ping send "))
		msg.Vrsta = 0

		msg.checksum = 0
		msg.Množicabuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataKazalnik)), uint32(icmpVelikost))

		msg.Množicabuffer(buffer_2)

		return true
		break
	}
	return false
}

func (sam *TSpletNadzorSporočiloprotocol) EchorequestPošlji(ipOmrežjebyteorder uint32) bool {
	var icmp TSpletNadzorSporočiloprotocolSporočilo = TSpletNadzorSporočiloprotocolSporočilo{}

	var pomnilnikmanager = &TPomnilnikmanager{}
	var buffer_2 = (*TSpletNadzorSporočiloprotocolSporočilobuffer)(pomnilnikmanager.Malloc(1024))

	icmp.Vrsta = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Množicabuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpVelikost))
	icmp.Množicabuffer(buffer_2)

	var dataKazalnik uintptr = uintptr(Pointer(buffer_2))
	iphandler.Pošlji(ipOmrežjebyteorder, 0x01, dataKazalnik, uint32(icmpVelikost))

	return false

}
