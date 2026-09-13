package icmp

import . "unsafe"
import . "console"
import . "հիշողությունmanager"
import . "ethernetՇրջանակ"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer struct {
	Տիպ	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpՉափս int = 64

type TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ struct {
	Տիպ	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (ինքնուրույն *TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ) Init(buffer_2 TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer) {
	ինքնուրույն.Տիպ = buffer_2.Տիպ
	ինքնուրույն.code = buffer_2.code

	ինքնուրույն.checksum = Unsignedinteger16r(Զանգվածtounsignedinteger16(buffer_2.checksum))
	ինքնուրույն.data = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer_2.data))
}

func (ինքնուրույն *TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ) Setbuffer(buffer_2 *TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer) {
	buffer_2.Տիպ = ինքնուրույն.Տիպ
	buffer_2.code = ինքնուրույն.code

	buffer_2.checksum = Unsignedinteger16toԶանգված(ինքնուրույն.checksum)
	buffer_2.data = Unsignedinteger32toԶանգված(ինքնուրույն.data)
}

type Icmphandler struct {
	TՀամացանցprotocolhandler
}

var icmp *TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocol

func (ինքնուրույն *Icmphandler) Համացանցprotocolreceivewhen(աղբյուրipaddressՑանցbyteorder uint32, destinationipaddressՑանցbyteorder uint32, dataՑուցիչ uintptr, չափս uint32) bool {
	return icmp.Համացանցprotocolreceivewhen(աղբյուրipaddressՑանցbyteorder, destinationipaddressՑանցbyteorder, dataՑուցիչ, չափս)
}

var iphandler IՀամացանցprotocolhandler

type TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocol struct {
}

func (ինքնուրույն *TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocol) Init(backend TՀամացանցprotocolprovider, handler IՀամացանցprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = ինքնուրույն
}
func (ինքնուրույն *TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocol) Համացանցprotocolreceivewhen(աղբյուրipaddressՑանցbyteorder uint32, destinationipaddressՑանցbyteorder uint32, dataՑուցիչ uintptr, չափս uint32) bool {
	if չափս < uint32(icmpՉափս) {
		return false
	}

	var buffer_2 *TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer = (*TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer)(Pointer(dataՑուցիչ))
	var msg TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ = TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ{}
	msg.Init(*buffer_2)

	icmpconsole.MՏպել(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Տպել(uint16(msg.Տիպ))
	icmpconsole.MՏպել(([]byte)(":"))

	switch msg.Տիպ {
	case 0:
		icmpconsole.MՏպել(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MՏպել(([]byte)("ping send "))
		msg.Տիպ = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataՑուցիչ)), uint32(icmpՉափս))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (ինքնուրույն *TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocol) EchorequestՈՒղարկել(ipՑանցbyteorder uint32) bool {
	var icmp TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ = TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ{}

	var հիշողությունmanager = &TՀիշողությունmanager{}
	var buffer_2 = (*TՀամացանցcontrolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer)(հիշողությունmanager.Malloc(1024))

	icmp.Տիպ = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpՉափս))
	icmp.Setbuffer(buffer_2)

	var dataՑուցիչ uintptr = uintptr(Pointer(buffer_2))
	iphandler.ՈՒղարկել(ipՑանցbyteorder, 0x01, dataՑուցիչ, uint32(icmpՉափս))

	return false

}
