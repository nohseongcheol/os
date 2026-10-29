/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "паметmanager"
import . "локалнамрежаEthernetРамка"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕbuffer struct {
	Тип	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpРазмер int = 64

type TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕ struct {
	Тип	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (себеси *TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕ) Init(buffer_2 TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕbuffer) {
	себеси.Тип = buffer_2.Тип
	себеси.code = buffer_2.code

	себеси.checksum = Unsignedinteger16r(Масивtounsignedinteger16(buffer_2.checksum))
	себеси.data = Unsignedinteger32r(Масивtounsignedinteger32(buffer_2.data))
}

func (себеси *TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕ) Задайbuffer(buffer_2 *TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕbuffer) {
	buffer_2.Тип = себеси.Тип
	buffer_2.code = себеси.code

	buffer_2.checksum = Unsignedinteger16toМасив(себеси.checksum)
	buffer_2.data = Unsignedinteger32toМасив(себеси.data)
}

type Icmphandler struct {
	TИнтернетprotocolhandler
}

var icmp *TИнтернетCtrlСЪОБЩЕНИЕprotocol

func (себеси *Icmphandler) Интернетprotocolreceivewhen(източникipaddressМрежаbyteorder uint32, назначениеipaddressМрежаbyteorder uint32, dataПоказалци uintptr, размер uint32) bool {
	return icmp.Интернетprotocolreceivewhen(източникipaddressМрежаbyteorder, назначениеipaddressМрежаbyteorder, dataПоказалци, размер)
}

var iphandler IИнтернетprotocolhandler

type TИнтернетCtrlСЪОБЩЕНИЕprotocol struct {
}

func (себеси *TИнтернетCtrlСЪОБЩЕНИЕprotocol) Init(backend TИнтернетprotocolprovider, handler IИнтернетprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = себеси
}
func (себеси *TИнтернетCtrlСЪОБЩЕНИЕprotocol) Интернетprotocolreceivewhen(източникipaddressМрежаbyteorder uint32, назначениеipaddressМрежаbyteorder uint32, dataПоказалци uintptr, размер uint32) bool {
	if размер < uint32(icmpРазмер) {
		return false
	}

	var buffer_2 *TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕbuffer = (*TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕbuffer)(Pointer(dataПоказалци))
	var msg TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕ = TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕ{}
	msg.Init(*buffer_2)

	icmpconsole.MПечат(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Печат(uint16(msg.Тип))
	icmpconsole.MПечат(([]byte)(":"))

	switch msg.Тип {
	case 0:
		icmpconsole.MПечат(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MПечат(([]byte)("ping send "))
		msg.Тип = 0

		msg.checksum = 0
		msg.Задайbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataПоказалци)), uint32(icmpРазмер))

		msg.Задайbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (себеси *TИнтернетCtrlСЪОБЩЕНИЕprotocol) EchorequestИзпращане(ipМрежаbyteorder uint32) bool {
	var icmp TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕ = TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕ{}

	var паметmanager = &TПаметmanager{}
	var buffer_2 = (*TИнтернетCtrlСЪОБЩЕНИЕprotocolСЪОБЩЕНИЕbuffer)(паметmanager.Malloc(1024))

	icmp.Тип = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Задайbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpРазмер))
	icmp.Задайbuffer(buffer_2)

	var dataПоказалци uintptr = uintptr(Pointer(buffer_2))
	iphandler.Изпращане(ipМрежаbyteorder, 0x01, dataПоказалци, uint32(icmpРазмер))

	return false

}
