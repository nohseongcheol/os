package りようしゃしりょうでんぶんきやく

import . "unsafe"
import . "こんそーる"
import . "はんよう"
import . "めもりかんりしゃ"
import . "そうごせつぞくあみきやく4"

var udpこんそーる = Tこんそーる{}

type Tりようしゃdatagramprotocolへっだbuffer struct {
	そうしんもとせつぞくばんごう	[2]byte
	あてさきせつぞくばんごう	[2]byte

	ながさ		[2]byte
	checksum	[2]byte
}

var udpへっださいず uint32 = 8

type Tりようしゃしりょうでんぶんせんとうぶ struct {
	そうしんもとせつぞくばんごう	uint16
	あてさきせつぞくばんごう	uint16

	ながさ		uint16
	checksum	uint16
}

func (self *Tりようしゃしりょうでんぶんせんとうぶ) Init(buffer_2 *Tりようしゃdatagramprotocolへっだbuffer) {
	self.そうしんもとせつぞくばんごう = Aはいれつtounsignedinteger16(buffer_2.そうしんもとせつぞくばんごう)
	self.あてさきせつぞくばんごう = Aはいれつtounsignedinteger16(buffer_2.あてさきせつぞくばんごう)

	self.ながさ = Aはいれつtounsignedinteger16(buffer_2.ながさ)
	self.checksum = Aはいれつtounsignedinteger16(buffer_2.checksum)
}
func (self *Tりようしゃしりょうでんぶんせんとうぶ) Sありbuffer(buffer_2 *Tりようしゃdatagramprotocolへっだbuffer) {

	buffer_2.そうしんもとせつぞくばんごう = Unsignedinteger16toはいれつ(self.そうしんもとせつぞくばんごう)
	buffer_2.あてさきせつぞくばんごう = Unsignedinteger16toはいれつ(self.あてさきせつぞくばんごう)

	buffer_2.ながさ = Unsignedinteger16toはいれつ(self.ながさ)
	buffer_2.checksum = Unsignedinteger16toはいれつ(self.checksum)

}

type Iりようしゃdatagramprotocolhandler interface {
	Hとってりようしゃdatagramprotocolめっせーじ(そけっと *Tりようしゃしりょうでんぶんつうしんたんてん, でーた uintptr, さいず uint16)
}

type Tりようしゃdatagramprotocolhandler struct {
}

func (self *Tりようしゃdatagramprotocolhandler) Init(backend Tそうごせつぞくあみきやくていきょううつわ) {
}
func (self *Tりようしゃdatagramprotocolhandler) Hとってりようしゃdatagramprotocolめっせーじ(そけっと *Tりようしゃしりょうでんぶんつうしんたんてん, でーた uintptr, さいず uint16) {
}

type Iりようしゃdatagramprotocolそけっと interface {
	Hとってりようしゃdatagramprotocolめっせーじ(でーた uintptr, さいず uint16)
}
type Tりようしゃしりょうでんぶんつうしんたんてん struct {
	りもーとぽーとnumber	uint16
	りもーとip		uint32
	ろーかるぽーとnumber	uint16
	ろーかるip		uint32

	listening	bool
}

var udpprovider Tりようしゃdatagramprotocolprovider
var udphandler Iりようしゃdatagramprotocolhandler

func (self *Tりようしゃしりょうでんぶんつうしんたんてん) Tてすと() {
}
func (self *Tりようしゃしりょうでんぶんつうしんたんてん) Init(pudpprovider Tりようしゃdatagramprotocolprovider, pudphandler Iりようしゃdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *Tりようしゃしりょうでんぶんつうしんたんてん) Hとってりようしゃdatagramprotocolめっせーじ(でーた uintptr, さいず uint16) {
	if udphandler != nil {
		udphandler.Hとってりようしゃdatagramprotocolめっせーじ(self, でーた, さいず)
	}
}
func (self *Tりようしゃしりょうでんぶんつうしんたんてん) Sそうしん(pでーた []byte, さいず uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(さいず); i++ {
		buffer_2[i] = pでーた[i]
	}
	var でーた = uintptr(Pointer(&buffer_2))
	udpprovider.Sそうしん(self, でーた, さいず)
}
func (self *Tりようしゃしりょうでんぶんつうしんたんてん) Dせつだんする() {
	udpprovider.Dせつだんする(self)
}

type Tりようしゃdatagramprotocolprovider struct {
}

var iphandler Iいんたーねっとprotocolhandler
var sockets [65535]Tりようしゃしりょうでんぶんつうしんたんてん
var numbersockets int
var あきぽーと uint16

func (self *Tりようしゃdatagramprotocolprovider) Init(pipprovider Tそうごせつぞくあみきやくていきょううつわ, piphandler Iいんたーねっとprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	あきぽーと = 1024
}
func (self *Tりようしゃdatagramprotocolprovider) Oいんたーねっとprotocolreceivewhen(てんそうもとipaddressねっとわーくばいとorder uint32, てんそうさきipaddressねっとわーくばいとorder uint32, いんたーねっとprotocolpayload uintptr, さいず uint32) bool {
	if さいず < udpへっださいず {
		return false
	}

	var buffer_2 *Tりようしゃdatagramprotocolへっだbuffer = (*Tりようしゃdatagramprotocolへっだbuffer)(Pointer(いんたーねっとprotocolpayload))
	var msg Tりようしゃしりょうでんぶんせんとうぶ
	msg.Init(buffer_2)

	var そけっと *Tりようしゃしりょうでんぶんつうしんたんてん = nil

	for i := 0; i < numbersockets && そけっと == nil; i++ {
		if sockets[i].ろーかるぽーとnumber == msg.あてさきせつぞくばんごう && sockets[i].ろーかるip == てんそうさきipaddressねっとわーくばいとorder && sockets[i].listening == true {
			そけっと = &sockets[i]
			そけっと.listening = false
			そけっと.りもーとぽーとnumber = msg.そうしんもとせつぞくばんごう
			そけっと.りもーとip = てんそうもとipaddressねっとわーくばいとorder
		} else if sockets[i].ろーかるぽーとnumber == msg.あてさきせつぞくばんごう && sockets[i].ろーかるip == てんそうさきipaddressねっとわーくばいとorder && sockets[i].りもーとぽーとnumber == msg.そうしんもとせつぞくばんごう && sockets[i].りもーとip == てんそうもとipaddressねっとわーくばいとorder {
			そけっと = &sockets[i]

		}
	}

	msg.Sありbuffer(buffer_2)
	if そけっと != nil {
		そけっと.Hとってりようしゃdatagramprotocolめっせーじ(いんたーねっとprotocolpayload+uintptr(udpへっださいず), uint16(さいず-udpへっださいず))
	}

	return false
}

func (self *Tりようしゃdatagramprotocolprovider) Cせつぞく(ip uint32, ぽーと uint16) *Tりようしゃしりょうでんぶんつうしんたんてん {
	var めもりかんりしゃ = &Tめもりかんりしゃ{}
	var そけっと = (*Tりようしゃしりょうでんぶんつうしんたんてん)(めもりかんりしゃ.Mきおくりょういきをかくほ(50))

	if そけっと != nil {

		そけっと.Init(*self, nil)
		そけっと.りもーとぽーとnumber = ぽーと
		そけっと.りもーとip = ip
		そけっと.ろーかるぽーとnumber = あきぽーと
		あきぽーと++
		そけっと.ろーかるip = uint32((*iphandler.Providerget()).Getipaddress())

		そけっと.りもーとぽーとnumber = Unsignedinteger16r(そけっと.りもーとぽーとnumber)
		そけっと.ろーかるぽーとnumber = Unsignedinteger16r(そけっと.ろーかるぽーとnumber)

		sockets[numbersockets] = *そけっと
		numbersockets++

	}
	return そけっと

}
func (self *Tりようしゃdatagramprotocolprovider) Listen(ぽーと uint16) *Tりようしゃしりょうでんぶんつうしんたんてん {
	var そけっと = &Tりようしゃしりょうでんぶんつうしんたんてん{}
	そけっと = nil
	if そけっと != nil {
		そけっと.Init(*self, nil)
		そけっと.listening = true
		そけっと.ろーかるぽーとnumber = ぽーと
		そけっと.ろーかるip = uint32((*iphandler.Providerget()).Getipaddress())

		そけっと.ろーかるぽーとnumber = Unsignedinteger16r(そけっと.ろーかるぽーとnumber)
	}
	return そけっと
}
func (self *Tりようしゃdatagramprotocolprovider) Dせつだんする(そけっと *Tりようしゃしりょうでんぶんつうしんたんてん) {
	for i := 0; i < numbersockets && そけっと == nil; i++ {
		if sockets[i] == *そけっと {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *Tりようしゃdatagramprotocolprovider) Sそうしん(そけっと *Tりようしゃしりょうでんぶんつうしんたんてん, pでーた uintptr, さいず uint16) {
	var ごうけいながさ = uint32(さいず) + udpへっださいず

	var buffer_2 [4096]byte

	var msgbuffer = (*Tりようしゃdatagramprotocolへっだbuffer)(Pointer(&buffer_2))

	var msg = Tりようしゃしりょうでんぶんせんとうぶ{}

	msg.そうしんもとせつぞくばんごう = そけっと.ろーかるぽーとnumber
	msg.あてさきせつぞくばんごう = そけっと.りもーとぽーとnumber
	msg.ながさ = Unsignedinteger16r(uint16(ごうけいながさ))

	msg.checksum = 0x0
	msg.Sありbuffer(msgbuffer)

	var でーたばいと [4096]byte = *(*[4096]byte)(Pointer(pでーた))
	for i := 0; i < int(さいず); i++ {
		buffer_2[int(udpへっださいず)+i] = でーたばいと[i]
	}

	var でーた uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Sそうしん(そけっと.りもーとip, 0x11, でーた, ごうけいながさ)

}
func (self *Tりようしゃdatagramprotocolprovider) Bばいんど(そけっと *Tりようしゃしりょうでんぶんつうしんたんてん, handler *Tりようしゃdatagramprotocolhandler) {
}
