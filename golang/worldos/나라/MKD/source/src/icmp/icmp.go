/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "меморијаmanager"
import . "етернетРамка"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TИнтернетcontrolПоракаprotocolПоракаbuffer struct {
	Тип	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpГолемина int = 64

type TИнтернетcontrolПоракаprotocolПорака struct {
	Тип	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (само *TИнтернетcontrolПоракаprotocolПорака) Init(buffer_2 TИнтернетcontrolПоракаprotocolПоракаbuffer) {
	само.Тип = buffer_2.Тип
	само.code = buffer_2.code

	само.checksum = Unsignedinteger16r(Построиtounsignedinteger16(buffer_2.checksum))
	само.data = Unsignedinteger32r(Построиtounsignedinteger32(buffer_2.data))
}

func (само *TИнтернетcontrolПоракаprotocolПорака) Поставиbuffer(buffer_2 *TИнтернетcontrolПоракаprotocolПоракаbuffer) {
	buffer_2.Тип = само.Тип
	buffer_2.code = само.code

	buffer_2.checksum = Unsignedinteger16toПострои(само.checksum)
	buffer_2.data = Unsignedinteger32toПострои(само.data)
}

type Icmphandler struct {
	TИнтернетprotocolhandler
}

var icmp *TИнтернетcontrolПоракаprotocol

func (само *Icmphandler) Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder uint32, одредиштеipaddressМрежаbyteorder uint32, dataСтрелка uintptr, големина uint32) bool {
	return icmp.Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder, одредиштеipaddressМрежаbyteorder, dataСтрелка, големина)
}

var iphandler IИнтернетprotocolhandler

type TИнтернетcontrolПоракаprotocol struct {
}

func (само *TИнтернетcontrolПоракаprotocol) Init(backend TИнтернетprotocolprovider, handler IИнтернетprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = само
}
func (само *TИнтернетcontrolПоракаprotocol) Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder uint32, одредиштеipaddressМрежаbyteorder uint32, dataСтрелка uintptr, големина uint32) bool {
	if големина < uint32(icmpГолемина) {
		return false
	}

	var buffer_2 *TИнтернетcontrolПоракаprotocolПоракаbuffer = (*TИнтернетcontrolПоракаprotocolПоракаbuffer)(Pointer(dataСтрелка))
	var msg TИнтернетcontrolПоракаprotocolПорака = TИнтернетcontrolПоракаprotocolПорака{}
	msg.Init(*buffer_2)

	icmpconsole.MПечати(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Печати(uint16(msg.Тип))
	icmpconsole.MПечати(([]byte)(":"))

	switch msg.Тип {
	case 0:
		icmpconsole.MПечати(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MПечати(([]byte)("ping send "))
		msg.Тип = 0

		msg.checksum = 0
		msg.Поставиbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataСтрелка)), uint32(icmpГолемина))

		msg.Поставиbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (само *TИнтернетcontrolПоракаprotocol) EchorequestИспрати(ipМрежаbyteorder uint32) bool {
	var icmp TИнтернетcontrolПоракаprotocolПорака = TИнтернетcontrolПоракаprotocolПорака{}

	var меморијаmanager = &TМеморијаmanager{}
	var buffer_2 = (*TИнтернетcontrolПоракаprotocolПоракаbuffer)(меморијаmanager.Malloc(1024))

	icmp.Тип = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Поставиbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpГолемина))
	icmp.Поставиbuffer(buffer_2)

	var dataСтрелка uintptr = uintptr(Pointer(buffer_2))
	iphandler.Испрати(ipМрежаbyteorder, 0x01, dataСтрелка, uint32(icmpГолемина))

	return false

}
