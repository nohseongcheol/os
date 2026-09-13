package icmp

import . "unsafe"
import . "конзола"
import . "memorijamanager"
import . "žičanavezaOkvir"
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

func (isti *TИнтернетКонтролпорукаprotocolпорука) Init(buffer_2 TИнтернетКонтролпорукаprotocolпорукаbuffer) {
	isti.Врста = buffer_2.Врста
	isti.code = buffer_2.code

	isti.checksum = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.checksum))
	isti.data = Unsignedinteger32r(Низtounsignedinteger32(buffer_2.data))
}

func (isti *TИнтернетКонтролпорукаprotocolпорука) Скупbuffer(buffer_2 *TИнтернетКонтролпорукаprotocolпорукаbuffer) {
	buffer_2.Врста = isti.Врста
	buffer_2.code = isti.code

	buffer_2.checksum = Unsignedinteger16toНиз(isti.checksum)
	buffer_2.data = Unsignedinteger32toНиз(isti.data)
}

type Icmphandler struct {
	TИнтернетprotocolhandler
}

var icmp *TИнтернетКонтролпорукаprotocol

func (isti *Icmphandler) Интернетprotocolreceivewhen(izvoripaddressМрежаbyteorder uint32, odredišteipaddressМрежаbyteorder uint32, dataPokazivač uintptr, величина uint32) bool {
	return icmp.Интернетprotocolreceivewhen(izvoripaddressМрежаbyteorder, odredišteipaddressМрежаbyteorder, dataPokazivač, величина)
}

var iphandler IИнтернетprotocolhandler

type TИнтернетКонтролпорукаprotocol struct {
}

func (isti *TИнтернетКонтролпорукаprotocol) Init(backend TИнтернетprotocolprovider, handler IИнтернетprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = isti
}
func (isti *TИнтернетКонтролпорукаprotocol) Интернетprotocolreceivewhen(izvoripaddressМрежаbyteorder uint32, odredišteipaddressМрежаbyteorder uint32, dataPokazivač uintptr, величина uint32) bool {
	if величина < uint32(icmpВеличина) {
		return false
	}

	var buffer_2 *TИнтернетКонтролпорукаprotocolпорукаbuffer = (*TИнтернетКонтролпорукаprotocolпорукаbuffer)(Pointer(dataPokazivač))
	var msg TИнтернетКонтролпорукаprotocolпорука = TИнтернетКонтролпорукаprotocolпорука{}
	msg.Init(*buffer_2)

	icmpКонзола.MŠtampaj(([]byte)("icmp:OnInternet"))
	icmpКонзола.MUnsignedinteger16Štampaj(uint16(msg.Врста))
	icmpКонзола.MŠtampaj(([]byte)(":"))

	switch msg.Врста {
	case 0:
		icmpКонзола.MŠtampaj(([]byte)("ping response from "))
		break

	case 8:
		icmpКонзола.MŠtampaj(([]byte)("ping send "))
		msg.Врста = 0

		msg.checksum = 0
		msg.Скупbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataPokazivač)), uint32(icmpВеличина))

		msg.Скупbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (isti *TИнтернетКонтролпорукаprotocol) EchorequestПошаљи(ipМрежаbyteorder uint32) bool {
	var icmp TИнтернетКонтролпорукаprotocolпорука = TИнтернетКонтролпорукаprotocolпорука{}

	var memorijamanager = &TMemorijamanager{}
	var buffer_2 = (*TИнтернетКонтролпорукаprotocolпорукаbuffer)(memorijamanager.Malloc(1024))

	icmp.Врста = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Скупbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpВеличина))
	icmp.Скупbuffer(buffer_2)

	var dataPokazivač uintptr = uintptr(Pointer(buffer_2))
	iphandler.Пошаљи(ipМрежаbyteorder, 0x01, dataPokazivač, uint32(icmpВеличина))

	return false

}
