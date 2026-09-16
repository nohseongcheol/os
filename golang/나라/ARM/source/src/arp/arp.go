/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetՇրջանակ"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer struct {
	ապարատայինմիջոցներՏիպ		[2]byte
	protocol			[2]byte
	ապարատայինմիջոցներaddressՉափս	byte
	protocoladdressՉափս		byte
	հրահանգ				[2]byte

	աղբյուրmacaddress	[6]byte
	աղբյուրipaddress	[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgՉափս uint32 = (64+92+64)/8 + 2

type ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ struct {
	ապարատայինմիջոցներՏիպ		uint16
	protocol			uint16
	ապարատայինմիջոցներaddressՉափս	uint8
	protocoladdressՉափս		uint8
	հրահանգ				uint16

	աղբյուրmacaddress	uint64
	աղբյուրipaddress	uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (ինքնուրույն *ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ) Init(buffer_2 *ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer) {

	ինքնուրույն.ապարատայինմիջոցներՏիպ = Unsignedinteger16r(Զանգվածtounsignedinteger16(buffer_2.ապարատայինմիջոցներՏիպ))
	ինքնուրույն.protocol = Unsignedinteger16r(Զանգվածtounsignedinteger16(buffer_2.protocol))
	ինքնուրույն.ապարատայինմիջոցներaddressՉափս = byte(buffer_2.ապարատայինմիջոցներaddressՉափս)
	ինքնուրույն.protocoladdressՉափս = byte(buffer_2.protocoladdressՉափս)
	ինքնուրույն.հրահանգ = Unsignedinteger16r(Զանգվածtounsignedinteger16(buffer_2.հրահանգ))

	ինքնուրույն.աղբյուրmacaddress = Unsignedinteger48r(Զանգվածtounsignedinteger48(buffer_2.աղբյուրmacaddress))
	ինքնուրույն.աղբյուրipaddress = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer_2.աղբյուրipaddress))
	ինքնուրույն.destinationmacaddress = Unsignedinteger48r(Զանգվածtounsignedinteger48(buffer_2.destinationmacaddress))
	ինքնուրույն.destinationipaddress = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer_2.destinationipaddress))
}
func (ինքնուրույն *ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ) Setbuffer(buffer_2 *ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer) {
	buffer_2.ապարատայինմիջոցներՏիպ = Unsignedinteger16toԶանգված(ինքնուրույն.ապարատայինմիջոցներՏիպ)
	buffer_2.protocol = Unsignedinteger16toԶանգված(ինքնուրույն.protocol)
	buffer_2.ապարատայինմիջոցներaddressՉափս = uint8(ինքնուրույն.ապարատայինմիջոցներaddressՉափս)
	buffer_2.protocoladdressՉափս = uint8(ինքնուրույն.protocoladdressՉափս)

	buffer_2.հրահանգ = Unsignedinteger16toԶանգված(ինքնուրույն.հրահանգ)
	buffer_2.աղբյուրmacaddress = Unsignedinteger48toԶանգված(ինքնուրույն.աղբյուրmacaddress)
	buffer_2.աղբյուրipaddress = Unsignedinteger32toԶանգված(ինքնուրույն.աղբյուրipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toԶանգված(ինքնուրույն.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toԶանգված(ինքնուրույն.destinationipaddress)
}

type ArpethernetՇրջանակhandler struct {
	TEthernetՇրջանակhandler
}

var arpprovider Arpprovider
var ethernetՇրջանակprovider TEthernetՇրջանակprovider

func (ինքնուրույն *ArpethernetՇրջանակhandler) EthernetՇրջանակreceivewhen(dataՑուցիչ uintptr, չափս int) bool {
	arpconsole.MՏպելxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetՇրջանակreceivewhen(dataՑուցիչ, uint32(չափս))

}
func (ինքնուրույն *ArpethernetՇրջանակhandler) ՈՒղարկել(destinationmacbe uint64, dataՑուցիչ uintptr, չափս uint32) {
	arpconsole.MՏպելxy([]byte("arp send:"), 0, 24)
	var ethernetՏիպbe = Unsignedinteger16r(0x0806)
	ինքնուրույն.TEthernetՇրջանակhandler.ՇրջանակՈՒղարկել(destinationmacbe, ethernetՏիպbe, dataՑուցիչ, չափս)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	հԱՄԱՐcacheentry	int

	handler	IEthernetՇրջանակhandler
}

var handler IEthernetՇրջանակhandler

func (ինքնուրույն *Arpprovider) Init(backend TEthernetՇրջանակprovider, userhandler IEthernetՇրջանակhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	ինքնուրույն.հԱՄԱՐcacheentry = 0
	arpprovider = *ինքնուրույն

}

func (ինքնուրույն *Arpprovider) EthernetՇրջանակreceivewhen(dataՑուցիչ uintptr, չափս uint32) bool {

	if չափս < arpmesgՉափս {
		return false
	}
	var arpbuffer *ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer = (*ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer)(Pointer(dataՑուցիչ))
	var arp ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ = ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ{}
	arp.Init(arpbuffer)

	if arp.ապարատայինմիջոցներՏիպ == 0x0100 {

		if arp.protocol == 0x0008 && arp.ապարատայինմիջոցներaddressՉափս == 6 && arp.protocoladdressՉափս == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MՏպել([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Տպել(arp.protocol)
			arpconsole.MՏպել([]byte(":"))
			arpconsole.MUnsignedinteger64Տպել(uint64(arp.destinationmacaddress))
			arpconsole.MՏպել([]byte(":"))
			arpconsole.MUnsignedinteger16Տպել(arp.հրահանգ)
			arpconsole.MՏպել([]byte(":"))
			arpconsole.MUnsignedinteger64Տպել(handler.Getmacaddress())

			switch arp.հրահանգ {
			case 0x0100:

				if ինքնուրույն.Getmacիցcache(arp.աղբյուրipaddress) == 0xFFFFFFFFFFFF {
					if ինքնուրույն.հԱՄԱՐcacheentry < 128 {
						ինքնուրույն.Ipcache[ինքնուրույն.հԱՄԱՐcacheentry] = arp.աղբյուրipaddress
						ինքնուրույն.Maccache[ինքնուրույն.հԱՄԱՐcacheentry] = arp.աղբյուրmacaddress
						ինքնուրույն.հԱՄԱՐcacheentry++
					}
				}
				arp.հրահանգ = 0x0200
				arp.destinationipaddress = arp.աղբյուրipaddress
				arp.destinationmacaddress = arp.աղբյուրmacaddress
				arp.աղբյուրipaddress = uint32(handler.Getipaddress())
				arp.աղբյուրmacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MՏպել(([]byte)("self.numCacheEntries"))

				if ինքնուրույն.հԱՄԱՐcacheentry < 128 {
					ինքնուրույն.Ipcache[ինքնուրույն.հԱՄԱՐcacheentry] = arp.աղբյուրipaddress
					ինքնուրույն.Maccache[ինքնուրույն.հԱՄԱՐcacheentry] = arp.աղբյուրmacaddress
					ինքնուրույն.հԱՄԱՐcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (ինքնուրույն *Arpprovider) Broadcastmacaddress(IpՑանցbyteorder uint32) {

	var arp ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ = ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ{}
	arp.ապարատայինմիջոցներՏիպ = 0x0100
	arp.protocol = 0x0008
	arp.ապարատայինմիջոցներaddressՉափս = 6
	arp.protocoladdressՉափս = 4
	arp.հրահանգ = 0x0200

	arp.աղբյուրipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = ինքնուրույն.Resolve(IpՑանցbyteorder)
	arp.destinationipaddress = IpՑանցbyteorder
	arpconsole.MՏպելxy([]byte("broad mac"), 0, 15)

	arp.աղբյուրmacaddress = handler.Getmacaddress()

	var arpbuffer ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer = ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer{}
	arp.Setbuffer(&arpbuffer)

	var ցուցիչ uintptr = uintptr(Pointer(&arpbuffer))
	handler.ՈՒղարկել(arp.destinationmacaddress, ցուցիչ, arpmesgՉափս)
}
func (ինքնուրույն *Arpprovider) Requestmacaddress(IpՑանցbyteorder uint32) {

	var arp ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ = ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ{}
	arp.ապարատայինմիջոցներՏիպ = 0x0100

	arp.protocol = 0x0008
	arp.ապարատայինմիջոցներaddressՉափս = 6
	arp.protocoladdressՉափս = 4
	arp.հրահանգ = 0x0100

	arp.աղբյուրmacaddress = handler.Getmacaddress()
	arp.աղբյուրipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpՑանցbyteorder

	var arpbuffer ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer = ArpՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer{}
	arp.Setbuffer(&arpbuffer)

	var ցուցիչ uintptr = uintptr(Pointer(&arpbuffer))
	handler.ՈՒղարկել(arp.destinationmacaddress, ցուցիչ, arpmesgՉափս)
}
func (ինքնուրույն *Arpprovider) ԹեստՏպել(data *[]byte, չափս uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MՏպելxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalՏպել(buffer_2[i])
		arpconsole.MՏպել([]byte(":"))
	}
	arpconsole.MՏպել([]byte("]"))
}

func (ինքնուրույն *Arpprovider) Getmacիցcache(IpՑանցbyteorder uint32) uint64 {
	for i := 0; i < ինքնուրույն.հԱՄԱՐcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MՏպել(([]byte)("["))
		arpconsole.MUnsignedinteger32Տպել(ինքնուրույն.Ipcache[i])
		arpconsole.MՏպել(([]byte)(":"))
		arpconsole.MUnsignedinteger32Տպել(IpՑանցbyteorder)
		arpconsole.MՏպել(([]byte)(":"))
		arpconsole.MՏպել(([]byte)(":"))
		arpconsole.MUnsignedinteger64Տպել(ինքնուրույն.Maccache[i])
		arpconsole.MՏպել(([]byte)("]\n"))

		if ինքնուրույն.Ipcache[i] == IpՑանցbyteorder {
			arpconsole.MՏպել([]byte("getmacfromcache"))
			return ինքնուրույն.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (ինքնուրույն *Arpprovider) Resolve(IpՑանցbyteorder uint32) uint64 {
	var result uint64 = ինքնուրույն.Getmacիցcache(IpՑանցbyteorder)
	if result == 0xFFFFFFFFFFFF {
		ինքնուրույն.Requestmacaddress(IpՑանցbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = ինքնուրույն.Getmacիցcache(IpՑանցbyteorder)

	}

	return result
}
