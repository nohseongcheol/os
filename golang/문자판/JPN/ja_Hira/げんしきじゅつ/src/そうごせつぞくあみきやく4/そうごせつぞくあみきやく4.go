package そうごせつぞくあみきやく4

import . "unsafe"
import . "はんよう"
import . "こんそーる"
import . "きょうゆうばいたいもうでんそうわく"
import . "arp"

var ipこんそーる Tこんそーる = Tこんそーる{}

type Tいんたーねっとprotocolv4めっせーじbuffer struct {
	lenver	byte
	tos	byte
	ごうけいながさ	[2]byte

	ident		[2]byte
	ふらぐとoffset	[2]byte

	じかんtolive	byte
	protocol	byte
	checksum	[2]byte

	てんそうもとipaddress	[4]byte
	てんそうさきipaddress	[4]byte
}

var ipさいず uint8 = (4 + 4 + 4 + 8)

type Tいんたーねっとprotocolv4めっせーじ struct {
	へっだながさ	uint8
	ばーじょん	uint8
	tos	uint8
	ごうけいながさ	uint16

	ident		uint16
	ふらぐとoffset	uint16

	じかんtolive	uint8
	protocol	uint8
	checksum	uint16

	てんそうもとipaddress	uint32
	てんそうさきipaddress	uint32
}

func (self *Tいんたーねっとprotocolv4めっせーじ) Init(buffer_2 Tいんたーねっとprotocolv4めっせーじbuffer) {

	self.ばーじょん = ((buffer_2.lenver & 0xF0) >> 4)
	self.へっだながさ = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.ごうけいながさ = Unsignedinteger16r(Aはいれつtounsignedinteger16(buffer_2.ごうけいながさ))

	self.ident = Unsignedinteger16r(Aはいれつtounsignedinteger16(buffer_2.ident))
	self.ふらぐとoffset = Unsignedinteger16r(Aはいれつtounsignedinteger16(buffer_2.ふらぐとoffset))

	self.じかんtolive = buffer_2.じかんtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Aはいれつtounsignedinteger16(buffer_2.checksum))

	self.てんそうもとipaddress = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer_2.てんそうもとipaddress))
	self.てんそうさきipaddress = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer_2.てんそうさきipaddress))

}
func (self *Tいんたーねっとprotocolv4めっせーじ) Sありbuffer(buffer_2 *Tいんたーねっとprotocolv4めっせーじbuffer) {

	buffer_2.lenver = byte(((self.ばーじょん & 0x0F) << 4) | (self.へっだながさ & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.ごうけいながさ = Unsignedinteger16toはいれつ(self.ごうけいながさ)

	buffer_2.ident = Unsignedinteger16toはいれつ(self.ident)
	buffer_2.ふらぐとoffset = Unsignedinteger16toはいれつ(self.ふらぐとoffset)

	buffer_2.じかんtolive = self.じかんtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toはいれつ(self.checksum)

	buffer_2.てんそうもとipaddress = Unsignedinteger32toはいれつ(self.てんそうもとipaddress)
	buffer_2.てんそうさきipaddress = Unsignedinteger32toはいれつ(self.てんそうさきipaddress)

}

type Iいんたーねっとprotocolhandler interface {
	Init(backend Tそうごせつぞくあみきやくていきょううつわ, pihandler Iいんたーねっとprotocolhandler, pprotocol uint8)
	Oいんたーねっとprotocolreceivewhen(てんそうもとipaddressねっとわーくばいとorder uint32, てんそうさきipaddressねっとわーくばいとorder uint32, でーたぽいんた uintptr, さいず uint32) bool
	Sそうしん(てんそうさきipaddressねっとわーくばいとorder uint32, pprotocol uint8, でーたぽいんた uintptr, さいず uint32)
	Providerget() *Tそうごせつぞくあみきやくていきょううつわ
}

type Tいんたーねっとprotocolhandler struct {
}

var ipいーさねっとふれーむhandler Ipいーさねっとふれーむhandler = Ipいーさねっとふれーむhandler{}
var protocol uint8

func (self *Tいんたーねっとprotocolhandler) Init(backend Tそうごせつぞくあみきやくていきょううつわ, pihandler Iいんたーねっとprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *Tいんたーねっとprotocolhandler) Oいんたーねっとprotocolreceivewhen(てんそうもとipaddressねっとわーくばいとorder uint32, てんそうさきipaddressねっとわーくばいとorder uint32, でーたぽいんた uintptr, さいず uint32) bool {
	ipこんそーる.Mいんさつ(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *Tいんたーねっとprotocolhandler) Sそうしん(てんそうさきipaddressねっとわーくばいとorder uint32, pprotocol uint8, でーたぽいんた uintptr, さいず uint32) {

	そうごせつぞくあみきやくていきょううつわ.Sそうしん(てんそうさきipaddressねっとわーくばいとorder, pprotocol, でーたぽいんた, さいず)
}
func (self *Tいんたーねっとprotocolhandler) Providerget() *Tそうごせつぞくあみきやくていきょううつわ {
	return &そうごせつぞくあみきやくていきょううつわ
}

type Ipいーさねっとふれーむhandler struct {
	Tいーさねっとふれーむhandler
}

var そうごせつぞくあみきやくていきょううつわ Tそうごせつぞくあみきやくていきょううつわ

func (self *Ipいーさねっとふれーむhandler) Oいーさねっとふれーむreceivewhen(でーたぽいんた uintptr, さいず int) bool {
	ipこんそーる.Mいんさつ(([]byte)("iphandler:onEtherfameRecv\n"))
	return そうごせつぞくあみきやくていきょううつわ.Oいーさねっとふれーむreceivewhen(でーたぽいんた, uint32(さいず))

}

func (self *Ipいーさねっとふれーむhandler) Sそうしん(てんそうさきipaddressねっとわーくばいとorder uint64, でーたぽいんた uintptr, さいず uint32) {
	ipこんそーる.Mいんさつ(([]byte)("ipefhandler:send\n"))
	var いーさねっとかたbe = Unsignedinteger16r(0x0800)
	self.Tいーさねっとふれーむhandler.Sふれーむそうしん(てんそうさきipaddressねっとわーくばいとorder, いーさねっとかたbe, でーたぽいんた, さいず)

}

var handler_2 [255]Iいんたーねっとprotocolhandler

type Tそうごせつぞくあみきやくていきょううつわ struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetますく	uint32
}

var efhandler Iいーさねっとふれーむhandler

func (self *Tそうごせつぞくあみきやくていきょううつわ) Init(pefprovider Tきょうゆうばいたいあみでんそうわくていきょううつわ, pefhandler Iいーさねっとふれーむhandler, arp Arpprovider, gatewayip uint32, subnetますく uint32) {

	efhandler = pefhandler
	efhandler.Sありhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.Subnetますく = subnetますく
	そうごせつぞくあみきやくていきょううつわ = *self
}
func (self *Tそうごせつぞくあみきやくていきょううつわ) Oいーさねっとふれーむreceivewhen(いーさねっとふれーむpayload uintptr, さいず uint32) bool {
	if さいず < uint32(ipさいず) {
		return false
	}

	var buffer_2 *Tいんたーねっとprotocolv4めっせーじbuffer = (*Tいんたーねっとprotocolv4めっせーじbuffer)(Pointer(いーさねっとふれーむpayload))
	var いんたーねっとprotocolめっせーじ Tいんたーねっとprotocolv4めっせーじ
	いんたーねっとprotocolめっせーじ.Init(*buffer_2)

	var reply bool = false

	if いんたーねっとprotocolめっせーじ.てんそうさきipaddress == uint32(efhandler.Getipaddress()) {

		var ながさ uint32 = uint32(いんたーねっとprotocolめっせーじ.ごうけいながさ)
		if ながさ > さいず {
			ながさ = さいず
		}
		if handler_2[いんたーねっとprotocolめっせーじ.protocol] != nil {
			reply = handler_2[いんたーねっとprotocolめっせーじ.protocol].Oいんたーねっとprotocolreceivewhen(いんたーねっとprotocolめっせーじ.てんそうもとipaddress, いんたーねっとprotocolめっせーじ.てんそうさきipaddress, いーさねっとふれーむpayload+uintptr(4*いんたーねっとprotocolめっせーじ.へっだながさ), uint32(ながさ-uint32(4*いんたーねっとprotocolめっせーじ.へっだながさ)))

		}
	}

	if reply {

		var temporary = いんたーねっとprotocolめっせーじ.てんそうさきipaddress
		いんたーねっとprotocolめっせーじ.てんそうさきipaddress = いんたーねっとprotocolめっせーじ.てんそうもとipaddress
		いんたーねっとprotocolめっせーじ.てんそうもとipaddress = temporary

		いんたーねっとprotocolめっせーじ.じかんtolive = 0x40
		いんたーねっとprotocolめっせーじ.checksum = 0

		いんたーねっとprotocolめっせーじ.Sありbuffer(buffer_2)
		いんたーねっとprotocolめっせーじ.checksum = self.Checksum((*([4096]uint16))(Pointer(いーさねっとふれーむpayload)), uint32(4*いんたーねっとprotocolめっせーじ.へっだながさ))

		いんたーねっとprotocolめっせーじ.Sありbuffer(buffer_2)

	}

	ipこんそーる.Mいんさつ(([]byte)("ipmessage"))
	ipこんそーる.MUnsignedinteger32いんさつ(いんたーねっとprotocolめっせーじ.てんそうもとipaddress)
	ipこんそーる.Mいんさつ(([]byte)(":"))
	ipこんそーる.MUnsignedinteger32いんさつ(いんたーねっとprotocolめっせーじ.てんそうさきipaddress)
	ipこんそーる.Mいんさつ(([]byte)(":"))
	ipこんそーる.MUnsignedinteger16いんさつ(uint16(いんたーねっとprotocolめっせーじ.へっだながさ))
	ipこんそーる.Mいんさつ(([]byte)(":"))
	ipこんそーる.MUnsignedinteger16いんさつ(uint16(いんたーねっとprotocolめっせーじ.ばーじょん))
	ipこんそーる.Mいんさつ(([]byte)(":"))
	ipこんそーる.MUnsignedinteger16いんさつ(いんたーねっとprotocolめっせーじ.ごうけいながさ)
	ipこんそーる.Mいんさつ(([]byte)(":"))
	ipこんそーる.MUnsignedinteger32いんさつ(uint32(efhandler.Getipaddress()))
	ipこんそーる.Mいんさつ(([]byte)(":"))
	ipこんそーる.Mいんさつ(([]byte)("\n"))

	return reply

}
func (self *Tそうごせつぞくあみきやくていきょううつわ) Sそうしん(てんそうさきipaddressねっとわーくばいとorder uint32, protocol uint8, でーたぽいんた uintptr, さいず uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *Tいんたーねっとprotocolv4めっせーじbuffer = (*Tいんたーねっとprotocolv4めっせーじbuffer)(Pointer(&buffer1_2))
	var めっせーじ Tいんたーねっとprotocolv4めっせーじ = Tいんたーねっとprotocolv4めっせーじ{}
	めっせーじ.ばーじょん = 4
	めっせーじ.へっだながさ = ipさいず / 4
	めっせーじ.tos = 0
	めっせーじ.ごうけいながさ = Unsignedinteger16r(uint16(さいず + uint32(ipさいず)))

	めっせーじ.ident = 0x0100
	めっせーじ.ふらぐとoffset = 0x0040
	めっせーじ.じかんtolive = 0x40
	めっせーじ.protocol = protocol

	めっせーじ.てんそうさきipaddress = てんそうさきipaddressねっとわーくばいとorder

	めっせーじ.てんそうもとipaddress = uint32(efhandler.Getipaddress())

	めっせーじ.checksum = 0

	めっせーじ.Sありbuffer(buffer_2)
	めっせーじ.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipさいず))
	めっせーじ.Sありbuffer(buffer_2)

	var でーたbuffer_2 [4096]byte = *(*([4096]byte))(Pointer(でーたぽいんた))

	for i := 0; i < int(さいず); i++ {

		buffer1_2[i+int(ipさいず)] = でーたbuffer_2[i]
	}

	ipこんそーる.Mいんさつxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(さいず)+int(ipさいず); i++ {
		ipこんそーる.MHexadecimalいんさつ(buffer1_2[i])
	}
	ipこんそーる.Mいんさつ(([]byte)(":"))
	ipこんそーる.Mいんさつ(([]byte)("]\n"))

	var つぎhopipaddressねっとわーくばいとorder uint32 = てんそうさきipaddressねっとわーくばいとorder
	if (てんそうさきipaddressねっとわーくばいとorder & self.Subnetますく) != (めっせーじ.てんそうもとipaddress & self.Subnetますく) {
		つぎhopipaddressねっとわーくばいとorder = self.Gatewayip
	}

	var そうしんでーたぽいんた = uintptr(Pointer(&buffer1_2))
	ipこんそーる.MUnsignedinteger32いんさつ(つぎhopipaddressねっとわーくばいとorder)

	var いーさねっとかたbe = Unsignedinteger16r(0x0800)
	efhandler.Sふれーむそうしん(self.arpprovider.Rかいけつ(つぎhopipaddressねっとわーくばいとorder), いーさねっとかたbe, そうしんでーたぽいんた, uint32(ipさいず)+uint32(さいず))

}
func (self *Tそうごせつぞくあみきやくていきょううつわ) Checksum(pでーた *[4096]uint16, ながさじゅしんばいと uint32) uint16 {
	var でーた [4096]uint16 = *pでーた
	var temporary uint32 = 0
	var でーたばいと [4096]byte = *(*([4096]byte))(Pointer(&でーた))
	if (ながさじゅしんばいと % 2) != 0 {
		temporary += uint32(uint16(でーたばいと[ながさじゅしんばいと-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *Tそうごせつぞくあみきやくていきょううつわ) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
