package そうごせつぞくあみせいぎょでんぶんきやく

import . "unsafe"
import . "こんそーる"
import . "めもりかんりしゃ"
import . "きょうゆうばいたいもうでんそうわく"
import . "そうごせつぞくあみきやく4"
import . "はんよう"

var icmpこんそーる = Tこんそーる{}

type Tいんたーねっとせいぎょめっせーじprotocolめっせーじbuffer struct {
	Tかた	byte
	code	byte

	checksum	[2]byte
	でーた		[4]byte
}

var icmpさいず int = 64

type Tいんたーねっとせいぎょめっせーじprotocolめっせーじ struct {
	Tかた	uint8
	code	uint8

	checksum	uint16
	でーた		uint32
}

func (self *Tいんたーねっとせいぎょめっせーじprotocolめっせーじ) Init(buffer_2 Tいんたーねっとせいぎょめっせーじprotocolめっせーじbuffer) {
	self.Tかた = buffer_2.Tかた
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Aはいれつtounsignedinteger16(buffer_2.checksum))
	self.でーた = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer_2.でーた))
}

func (self *Tいんたーねっとせいぎょめっせーじprotocolめっせーじ) Sありbuffer(buffer_2 *Tいんたーねっとせいぎょめっせーじprotocolめっせーじbuffer) {
	buffer_2.Tかた = self.Tかた
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toはいれつ(self.checksum)
	buffer_2.でーた = Unsignedinteger32toはいれつ(self.でーた)
}

type Icmphandler struct {
	Tいんたーねっとprotocolhandler
}

var そうごせつぞくあみせいぎょでんぶんきやく *Tそうごせつぞくあみせいぎょでんぶんきやく

func (self *Icmphandler) Oいんたーねっとprotocolreceivewhen(てんそうもとipaddressねっとわーくばいとorder uint32, てんそうさきipaddressねっとわーくばいとorder uint32, でーたぽいんた uintptr, さいず uint32) bool {
	return そうごせつぞくあみせいぎょでんぶんきやく.Oいんたーねっとprotocolreceivewhen(てんそうもとipaddressねっとわーくばいとorder, てんそうさきipaddressねっとわーくばいとorder, でーたぽいんた, さいず)
}

var iphandler Iいんたーねっとprotocolhandler

type Tそうごせつぞくあみせいぎょでんぶんきやく struct {
}

func (self *Tそうごせつぞくあみせいぎょでんぶんきやく) Init(backend Tそうごせつぞくあみきやくていきょううつわ, handler Iいんたーねっとprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	そうごせつぞくあみせいぎょでんぶんきやく = self
}
func (self *Tそうごせつぞくあみせいぎょでんぶんきやく) Oいんたーねっとprotocolreceivewhen(てんそうもとipaddressねっとわーくばいとorder uint32, てんそうさきipaddressねっとわーくばいとorder uint32, でーたぽいんた uintptr, さいず uint32) bool {
	if さいず < uint32(icmpさいず) {
		return false
	}

	var buffer_2 *Tいんたーねっとせいぎょめっせーじprotocolめっせーじbuffer = (*Tいんたーねっとせいぎょめっせーじprotocolめっせーじbuffer)(Pointer(でーたぽいんた))
	var msg Tいんたーねっとせいぎょめっせーじprotocolめっせーじ = Tいんたーねっとせいぎょめっせーじprotocolめっせーじ{}
	msg.Init(*buffer_2)

	icmpこんそーる.Mいんさつ(([]byte)("icmp:OnInternet"))
	icmpこんそーる.MUnsignedinteger16いんさつ(uint16(msg.Tかた))
	icmpこんそーる.Mいんさつ(([]byte)(":"))

	switch msg.Tかた {
	case 0:
		icmpこんそーる.Mいんさつ(([]byte)("ping response from "))
		break

	case 8:
		icmpこんそーる.Mいんさつ(([]byte)("ping send "))
		msg.Tかた = 0

		msg.checksum = 0
		msg.Sありbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(でーたぽいんた)), uint32(icmpさいず))

		msg.Sありbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *Tそうごせつぞくあみせいぎょでんぶんきやく) Echorequestそうしん(ipねっとわーくばいとorder uint32) bool {
	var そうごせつぞくあみせいぎょでんぶんきやく Tいんたーねっとせいぎょめっせーじprotocolめっせーじ = Tいんたーねっとせいぎょめっせーじprotocolめっせーじ{}

	var めもりかんりしゃ = &Tめもりかんりしゃ{}
	var buffer_2 = (*Tいんたーねっとせいぎょめっせーじprotocolめっせーじbuffer)(めもりかんりしゃ.Mきおくりょういきをかくほ(1024))

	そうごせつぞくあみせいぎょでんぶんきやく.Tかた = 8
	そうごせつぞくあみせいぎょでんぶんきやく.code = 0
	そうごせつぞくあみせいぎょでんぶんきやく.でーた = 0x3713
	そうごせつぞくあみせいぎょでんぶんきやく.checksum = 0
	そうごせつぞくあみせいぎょでんぶんきやく.Sありbuffer(buffer_2)
	そうごせつぞくあみせいぎょでんぶんきやく.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpさいず))
	そうごせつぞくあみせいぎょでんぶんきやく.Sありbuffer(buffer_2)

	var でーたぽいんた uintptr = uintptr(Pointer(buffer_2))
	iphandler.Sそうしん(ipねっとわーくばいとorder, 0x01, でーたぽいんた, uint32(icmpさいず))

	return false

}
