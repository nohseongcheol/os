/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package じっこうれんけつけいしき

import . "unsafe"

import . "こんそーる"
import . "はんよう"
import . "めもりかんりしゃ"
import . "ぺーじかんり"

type Elfへっだ struct {
	eident		[16]byte
	eかた		uint16
	emachine	uint16
	eばーじょん		uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eふらぐ		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfくかくへっだ struct {
	shなまえ		uint32
	shかた		uint32
	shふらぐ		uint32
	shaddress	uint32
	shoffset	uint32
	shさいず		uint32
	shれんけつ		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfぷろぐらむへっだ struct {
	pかた	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pふらぐ	uint32
	pせいれつ	uint32
}
type Elf32びこう struct {
	nnamesz	uint32
	ndescsz	uint32
	nかた	uint32
}
type Elf32dyn struct {
	dたぐ		uint32
	dvalぽいんた	uint32
}
type Elf32rel struct {
	roffset	uint32
	rinfo	uint32
}
type Elf32rela struct {
	roffset	uint32
	rinfo	uint32
	raddend	uint32
}
type Elf32sym struct {
	stなまえ	uint32
	stあたい	uint32
	stさいず	uint32
	stinfo	uint8
	stそのほか	uint8
	stshndx	uint16
}
type relocationてきすと struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	てきすと		[]byte
	てきすとlen		uint32
	relてきすと		[100]relocationてきすと
	relてきすとlen	uint32
	strtab		[100]string
	Got		uint32
	Dどうてきに		uint32
}

func (self *Elf) Getentry(でーた []byte) uint32 {
	elfへっだ := (*Elfへっだ)(Pointer(&でーた[0]))
	return elfへっだ.eentry
}

func (self *Elf) Parse(でーた []byte, Pぺーじでぃれくとりentry uint32) {

	めもりかんりしゃ := Tめもりかんりしゃ{}
	var てきすとぽいんた Pointer = nil

	var こんそーる_2 = Tこんそーる{}

	elfへっだ := (*Elfへっだ)(Pointer(&でーた[0]))

	if elfへっだ.eshnum != 0 {
		strtab := (*Elfくかくへっだ)(Pointer(&でーた[elfへっだ.eshoff+uint32(elfへっだ.eshentsize*elfへっだ.eshstrndx)]))
		sectへっださいず := uint32(Sizeof(Elfくかくへっだ{}))

		for i := uint32(0); i < uint32(elfへっだ.eshnum); i++ {
			sectへっだ := (*Elfくかくへっだ)(Pointer(&でーた[elfへっだ.eshoff+sectへっださいず*i]))

			var sectなまえ []byte
			かいし := uint32(strtab.shoffset + sectへっだ.shなまえ)
			ぶんまつ := かいし
			for ; ; ぶんまつ++ {
				if でーた[ぶんまつ] == 0x0 || でーた[ぶんまつ] == ' ' {
					break
				}
			}
			sectなまえ = でーた[かいし:ぶんまつ]

			var sectあたい []byte
			if sectへっだ.shかた != 8 {
				ぶんまつoffset := sectへっだ.shoffset + sectへっだ.shさいず
				if ぶんまつoffset < sectへっだ.shoffset || ぶんまつoffset > uint32(len(でーた)) {
					continue
				}
				sectあたい = でーた[sectへっだ.shoffset:ぶんまつoffset]
			}

			if Eすべておなじばいと(sectなまえ, ([]byte)(".got.plt")) {
				こんそーる_2.Mいんさつ("[")
				こんそーる_2.Mいんさつ(sectなまえ)
				こんそーる_2.Mいんさつ(":")
				self.Got = sectへっだ.shaddress
				こんそーる_2.MUnsignedinteger32いんさつ(self.Got)
				こんそーる_2.Mいんさつ("]")
			}
			if Eすべておなじばいと(sectなまえ, ([]byte)(".dynamic")) {
				こんそーる_2.Mいんさつ("[")
				こんそーる_2.Mいんさつ(sectなまえ)
				こんそーる_2.Mいんさつ(":")
				どうてきに := sectへっだ.shaddress
				self.Dどうてきに = どうてきに
				こんそーる_2.MUnsignedinteger32いんさつ(どうてきに)
				こんそーる_2.Mいんさつ("]")
			}

			if sectへっだ.shaddress > 0x1000 {
				さいず := sectへっだ.shさいず
				if sectへっだ.shかた == 8 {
					Zすうちの0ぶろっくじゅしんぺーじでぃれくとり(sectへっだ.shaddress, さいず, Pぺーじでぃれくとりentry)
				} else {
					てんそうさき_2 := Getばいとからぽいんた(uintptr(sectへっだ.shaddress), int(さいず), int(さいず))
					Sありぶろっくじゅしんぺーじでぃれくとり(sectあたい, てんそうさき_2, さいず, Pぺーじでぃれくとりentry)
				}
			}

			continue

			if Eすべておなじばいと(sectなまえ, ([]byte)(".text")) {
				こんそーる_2.Mいんさつ(".text")
				こんそーる_2.Mいんさつ("[")
				こんそーる_2.MUnsignedinteger32いんさつ(sectへっだ.shaddress)
				こんそーる_2.Mいんさつ(":")
				こんそーる_2.MUnsignedinteger32いんさつ(sectへっだ.shoffset)
				こんそーる_2.Mいんさつ(":")
				こんそーる_2.MUnsignedinteger32いんさつ(sectへっだ.shさいず)
				こんそーる_2.Mいんさつ("]")
				copy(self.てきすと[:sectへっだ.shさいず], sectあたい[:sectへっだ.shさいず])
				self.てきすとlen = sectへっだ.shさいず
			}
			if Eすべておなじばいと(sectなまえ, ([]byte)(".rel.text")) {
				こんそーる_2.Mいんさつ(".rel.text")
				こんそーる_2.Mいんさつ("[")
				こんそーる_2.MUnsignedinteger32いんさつ(sectへっだ.shaddress)
				こんそーる_2.Mいんさつ(":")
				こんそーる_2.MUnsignedinteger32いんさつ(sectへっだ.shさいず)
				こんそーる_2.Mいんさつ("]")
				for rt := uint32(0); rt < sectへっだ.shさいず/8; rt++ {
					offset := *(*uint32)(Pointer(&sectあたい[rt*8]))
					self.relてきすと[rt].offset = offset
					self.relてきすと[rt].oaddress = *(*uint32)(Pointer(&self.てきすと[offset]))
					self.relてきすと[rt].number = *(*uint32)(Pointer(&sectあたい[rt*8+4]))
					self.relてきすとlen++
				}
			}
			if Eすべておなじばいと(sectなまえ, ([]byte)(".dynsym")) {
				こんそーる_2.Mいんさつ(".dynsym")
				こんそーる_2.Mいんさつ("[")
				こんそーる_2.MUnsignedinteger32いんさつ(sectへっだ.shaddress)
				こんそーる_2.Mいんさつ(":")
				こんそーる_2.MUnsignedinteger32いんさつ(sectへっだ.shさいず)
				こんそーる_2.Mいんさつ("]")
				for rt := uint32(0); rt < sectへっだ.shさいず/8; rt++ {
					offset := *(*uint32)(Pointer(&sectあたい[rt*8]))
					self.relてきすと[rt].offset = offset
					self.relてきすと[rt].oaddress = *(*uint32)(Pointer(&self.てきすと[offset]))
					self.relてきすと[rt].number = *(*uint32)(Pointer(&sectあたい[rt*8+4]))
					self.relてきすとlen++
				}
			}
			if Eすべておなじばいと(sectなまえ, ([]byte)(".dynstr")) {
				こんそーる_2.Mいんさつ(".dynstr")
				こんそーる_2.Mいんさつ("[")
				こんそーる_2.MUnsignedinteger32いんさつ(sectへっだ.shaddress)
				こんそーる_2.Mいんさつ(":")
				こんそーる_2.MUnsignedinteger32いんさつ(sectへっだ.shさいず)
				こんそーる_2.Mいんさつ("]")
			}
			if Eすべておなじばいと(sectなまえ, ([]byte)(".strtab")) {
				こんそーる_2.Mいんさつ(".strtab")
				こんそーる_2.Mいんさつ("[")
				こんそーる_2.MUnsignedinteger32いんさつ(sectへっだ.shaddress)
				こんそーる_2.Mいんさつ("]")
				rt := uint32(0)
				かいし := uint32(0)

				for st := uint32(1); st < sectへっだ.shさいず; st++ {
					if sectあたい[st] == 0x0 || sectあたい[st] == ' ' {
						funcなまえ := sectあたい[かいし+1 : st]
						こんそーる_2.Mいんさつ("+")
						こんそーる_2.Mいんさつ(funcなまえ)
						self.strtab[rt] = Bばいとtoもじれつ(funcなまえ)
						かいし = st
						rt++
					}
				}

			}

		}

		こんそーる_2.Mいんさつ(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relてきすとlen; rt++ {
			こんそーる_2.Mいんさつ("[")
			こんそーる_2.Mいんさつ(([]byte)(self.strtab[rt]))
			こんそーる_2.Mいんさつ(":")
			こんそーる_2.MUnsignedinteger32いんさつ(self.relてきすと[rt].number)
			こんそーる_2.Mいんさつ(":")

			こんそーる_2.Mいんさつ(([]byte)("]"))
		}
		こんそーる_2.Mいんさつ(([]byte)("------------>"))

		if てきすとぽいんた != nil {
			めもりかんりしゃ.Fあき(てきすとぽいんた)
		}

	}

}
