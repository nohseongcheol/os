/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "конзола"
import . "меморијаmanager"
import . "жичанавезаОквир"
import . "ipv4"
import . "util"

var icmpКонзола = TКонзола{}

type TИнтернетКонтролпорукаprotocolпорукаbuffer struct {
	Врста	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpВеличина int = 64

type TИнтернетКонтролпорукаprotocolпорука struct {
	Врста	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (исти *TИнтернетКонтролпорукаprotocolпорука) Init(buffer_2 TИнтернетКонтролпорукаprotocolпорукаbuffer) {
	исти.Врста = buffer_2.Врста
	исти.code = buffer_2.code

	исти.checksum = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.checksum))
	исти.data = Unsignedinteger32r(Низtounsignedinteger32(buffer_2.data))
}

func (исти *TИнтернетКонтролпорукаprotocolпорука) Скупbuffer(buffer_2 *TИнтернетКонтролпорукаprotocolпорукаbuffer) {
	buffer_2.Врста = исти.Врста
	buffer_2.code = исти.code

	buffer_2.checksum = Unsignedinteger16toНиз(исти.checksum)
	buffer_2.data = Unsignedinteger32toНиз(исти.data)
}

type Icmphandler struct {
	TИнтернетprotocolhandler
}

var icmp *TИнтернетКонтролпорукаprotocol

func (исти *Icmphandler) Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder uint32, одредиштеipaddressМрежаbyteorder uint32, dataПоказивач uintptr, величина uint32) bool {
	return icmp.Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder, одредиштеipaddressМрежаbyteorder, dataПоказивач, величина)
}

var iphandler IИнтернетprotocolhandler

type TИнтернетКонтролпорукаprotocol struct {
}

func (исти *TИнтернетКонтролпорукаprotocol) Init(backend TИнтернетprotocolprovider, handler IИнтернетprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = исти
}
func (исти *TИнтернетКонтролпорукаprotocol) Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder uint32, одредиштеipaddressМрежаbyteorder uint32, dataПоказивач uintptr, величина uint32) bool {
	if величина < uint32(icmpВеличина) {
		return false
	}

	var buffer_2 *TИнтернетКонтролпорукаprotocolпорукаbuffer = (*TИнтернетКонтролпорукаprotocolпорукаbuffer)(Pointer(dataПоказивач))
	var msg TИнтернетКонтролпорукаprotocolпорука = TИнтернетКонтролпорукаprotocolпорука{}
	msg.Init(*buffer_2)

	icmpКонзола.MШтампај(([]byte)("icmp:OnInternet"))
	icmpКонзола.MUnsignedinteger16Штампај(uint16(msg.Врста))
	icmpКонзола.MШтампај(([]byte)(":"))

	switch msg.Врста {
	case 0:
		icmpКонзола.MШтампај(([]byte)("ping response from "))
		break

	case 8:
		icmpКонзола.MШтампај(([]byte)("ping send "))
		msg.Врста = 0

		msg.checksum = 0
		msg.Скупbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataПоказивач)), uint32(icmpВеличина))

		msg.Скупbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (исти *TИнтернетКонтролпорукаprotocol) EchorequestПошаљи(ipМрежаbyteorder uint32) bool {
	var icmp TИнтернетКонтролпорукаprotocolпорука = TИнтернетКонтролпорукаprotocolпорука{}

	var меморијаmanager = &TМеморијаmanager{}
	var buffer_2 = (*TИнтернетКонтролпорукаprotocolпорукаbuffer)(меморијаmanager.Malloc(1024))

	icmp.Врста = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Скупbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpВеличина))
	icmp.Скупbuffer(buffer_2)

	var dataПоказивач uintptr = uintptr(Pointer(buffer_2))
	iphandler.Пошаљи(ipМрежаbyteorder, 0x01, dataПоказивач, uint32(icmpВеличина))

	return false

}
