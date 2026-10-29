/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "atmiņamanager"
import . "ethernetIetvars"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetsCtrlZiņojumsprotocolZiņojumsbuffer struct {
	Tips	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpIzmērs int = 64

type TInternetsCtrlZiņojumsprotocolZiņojums struct {
	Tips	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (pats *TInternetsCtrlZiņojumsprotocolZiņojums) Init(buffer_2 TInternetsCtrlZiņojumsprotocolZiņojumsbuffer) {
	pats.Tips = buffer_2.Tips
	pats.code = buffer_2.code

	pats.checksum = Unsignedinteger16r(Masīvstounsignedinteger16(buffer_2.checksum))
	pats.data = Unsignedinteger32r(Masīvstounsignedinteger32(buffer_2.data))
}

func (pats *TInternetsCtrlZiņojumsprotocolZiņojums) Kopabuffer(buffer_2 *TInternetsCtrlZiņojumsprotocolZiņojumsbuffer) {
	buffer_2.Tips = pats.Tips
	buffer_2.code = pats.code

	buffer_2.checksum = Unsignedinteger16toMasīvs(pats.checksum)
	buffer_2.data = Unsignedinteger32toMasīvs(pats.data)
}

type Icmphandler struct {
	TInternetsprotocolhandler
}

var icmp *TInternetsCtrlZiņojumsprotocol

func (pats *Icmphandler) Internetsprotocolreceivewhen(avotsipaddressTīklsbyteorder uint32, mērķisipaddressTīklsbyteorder uint32, dataKursors uintptr, izmērs uint32) bool {
	return icmp.Internetsprotocolreceivewhen(avotsipaddressTīklsbyteorder, mērķisipaddressTīklsbyteorder, dataKursors, izmērs)
}

var iphandler IInternetsprotocolhandler

type TInternetsCtrlZiņojumsprotocol struct {
}

func (pats *TInternetsCtrlZiņojumsprotocol) Init(backend TInternetsprotocolprovider, handler IInternetsprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = pats
}
func (pats *TInternetsCtrlZiņojumsprotocol) Internetsprotocolreceivewhen(avotsipaddressTīklsbyteorder uint32, mērķisipaddressTīklsbyteorder uint32, dataKursors uintptr, izmērs uint32) bool {
	if izmērs < uint32(icmpIzmērs) {
		return false
	}

	var buffer_2 *TInternetsCtrlZiņojumsprotocolZiņojumsbuffer = (*TInternetsCtrlZiņojumsprotocolZiņojumsbuffer)(Pointer(dataKursors))
	var msg TInternetsCtrlZiņojumsprotocolZiņojums = TInternetsCtrlZiņojumsprotocolZiņojums{}
	msg.Init(*buffer_2)

	icmpconsole.MDrukāt(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Drukāt(uint16(msg.Tips))
	icmpconsole.MDrukāt(([]byte)(":"))

	switch msg.Tips {
	case 0:
		icmpconsole.MDrukāt(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MDrukāt(([]byte)("ping send "))
		msg.Tips = 0

		msg.checksum = 0
		msg.Kopabuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataKursors)), uint32(icmpIzmērs))

		msg.Kopabuffer(buffer_2)

		return true
		break
	}
	return false
}

func (pats *TInternetsCtrlZiņojumsprotocol) EchorequestSūtīt(ipTīklsbyteorder uint32) bool {
	var icmp TInternetsCtrlZiņojumsprotocolZiņojums = TInternetsCtrlZiņojumsprotocolZiņojums{}

	var atmiņamanager = &TAtmiņamanager{}
	var buffer_2 = (*TInternetsCtrlZiņojumsprotocolZiņojumsbuffer)(atmiņamanager.Malloc(1024))

	icmp.Tips = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Kopabuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpIzmērs))
	icmp.Kopabuffer(buffer_2)

	var dataKursors uintptr = uintptr(Pointer(buffer_2))
	iphandler.Sūtīt(ipTīklsbyteorder, 0x01, dataKursors, uint32(icmpIzmērs))

	return false

}
