/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "памяцьmanager"
import . "лякальнаясеткаФрэйм"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TІнтэрнэтCtrlпаведамленнеprotocolпаведамленнеbuffer struct {
	Тып	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpПамер int = 64

type TІнтэрнэтCtrlпаведамленнеprotocolпаведамленне struct {
	Тып	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TІнтэрнэтCtrlпаведамленнеprotocolпаведамленне) Init(buffer_2 TІнтэрнэтCtrlпаведамленнеprotocolпаведамленнеbuffer) {
	self.Тып = buffer_2.Тып
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Масіўtounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Масіўtounsignedinteger32(buffer_2.data))
}

func (self *TІнтэрнэтCtrlпаведамленнеprotocolпаведамленне) Вызначанаbuffer(buffer_2 *TІнтэрнэтCtrlпаведамленнеprotocolпаведамленнеbuffer) {
	buffer_2.Тып = self.Тып
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toМасіў(self.checksum)
	buffer_2.data = Unsignedinteger32toМасіў(self.data)
}

type Icmphandler struct {
	TІнтэрнэтprotocolhandler
}

var icmp *TІнтэрнэтCtrlпаведамленнеprotocol

func (self *Icmphandler) Інтэрнэтprotocolreceivewhen(крыніцаipaddressСеткаbyteorder uint32, destinationipaddressСеткаbyteorder uint32, dataПаказальнік uintptr, памер uint32) bool {
	return icmp.Інтэрнэтprotocolreceivewhen(крыніцаipaddressСеткаbyteorder, destinationipaddressСеткаbyteorder, dataПаказальнік, памер)
}

var iphandler IІнтэрнэтprotocolhandler

type TІнтэрнэтCtrlпаведамленнеprotocol struct {
}

func (self *TІнтэрнэтCtrlпаведамленнеprotocol) Init(backend TІнтэрнэтprotocolprovider, handler IІнтэрнэтprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TІнтэрнэтCtrlпаведамленнеprotocol) Інтэрнэтprotocolreceivewhen(крыніцаipaddressСеткаbyteorder uint32, destinationipaddressСеткаbyteorder uint32, dataПаказальнік uintptr, памер uint32) bool {
	if памер < uint32(icmpПамер) {
		return false
	}

	var buffer_2 *TІнтэрнэтCtrlпаведамленнеprotocolпаведамленнеbuffer = (*TІнтэрнэтCtrlпаведамленнеprotocolпаведамленнеbuffer)(Pointer(dataПаказальнік))
	var msg TІнтэрнэтCtrlпаведамленнеprotocolпаведамленне = TІнтэрнэтCtrlпаведамленнеprotocolпаведамленне{}
	msg.Init(*buffer_2)

	icmpconsole.MДрукаваць(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Друкаваць(uint16(msg.Тып))
	icmpconsole.MДрукаваць(([]byte)(":"))

	switch msg.Тып {
	case 0:
		icmpconsole.MДрукаваць(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MДрукаваць(([]byte)("ping send "))
		msg.Тып = 0

		msg.checksum = 0
		msg.Вызначанаbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataПаказальнік)), uint32(icmpПамер))

		msg.Вызначанаbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TІнтэрнэтCtrlпаведамленнеprotocol) EchorequestДаслаць(ipСеткаbyteorder uint32) bool {
	var icmp TІнтэрнэтCtrlпаведамленнеprotocolпаведамленне = TІнтэрнэтCtrlпаведамленнеprotocolпаведамленне{}

	var памяцьmanager = &TПамяцьmanager{}
	var buffer_2 = (*TІнтэрнэтCtrlпаведамленнеprotocolпаведамленнеbuffer)(памяцьmanager.Malloc(1024))

	icmp.Тып = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Вызначанаbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpПамер))
	icmp.Вызначанаbuffer(buffer_2)

	var dataПаказальнік uintptr = uintptr(Pointer(buffer_2))
	iphandler.Даслаць(ipСеткаbyteorder, 0x01, dataПаказальнік, uint32(icmpПамер))

	return false

}
