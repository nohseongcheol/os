package elf

import . "unsafe"

import . "console"
import . "util"
import . "эсиmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eТүрү		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eЖелектери	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shАты		uint32
	shТүрү		uint32
	shЖелектери	uint32
	shaddress	uint32
	shoffset	uint32
	shӨлчөм		uint32
	shшилтеме	uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfпрограммаheader struct {
	pТүрү		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pЖелектери	uint32
	pТүздөө		uint32
}
type Elf32Белги struct {
	nnamesz	uint32
	ndescsz	uint32
	nТүрү	uint32
}
type Elf32dyn struct {
	dТеги		uint32
	dvalКөрсөткүч	uint32
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
	stАты		uint32
	stМааниси	uint32
	stӨлчөм		uint32
	stinfo		uint8
	stБашкалар	uint8
	stshndx		uint16
}
type relocationТекст struct {
	offset		uint32
	нОМЕР		uint32
	oaddress	uint32
}
type Elf struct {
	текст		[]byte
	текстlen	uint32
	relТекст	[100]relocationТекст
	relТекстlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, БАРАКкаталогentry uint32) {

	эсиmanager := TЭсиmanager{}
	var текстКөрсөткүч Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderӨлчөм := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderӨлчөм*i]))

			var sectАты []byte
			жүргүзүү := uint32(strtab.shoffset + sectheader.shАты)
			end := жүргүзүү
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectАты = data[жүргүзүү:end]

			var sectМааниси []byte
			if sectheader.shТүрү != 8 {
				endoffset := sectheader.shoffset + sectheader.shӨлчөм
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectМааниси = data[sectheader.shoffset:endoffset]
			}

			if EqualБайт(sectАты, ([]byte)(".got.plt")) {
				console_2.MБасма("[")
				console_2.MБасма(sectАты)
				console_2.MБасма(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Басма(self.Got)
				console_2.MБасма("]")
			}
			if EqualБайт(sectАты, ([]byte)(".dynamic")) {
				console_2.MБасма("[")
				console_2.MБасма(sectАты)
				console_2.MБасма(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				console_2.MUnsignedinteger32Басма(dynamic)
				console_2.MБасма("]")
			}

			if sectheader.shaddress > 0x1000 {
				өлчөм := sectheader.shӨлчөм
				if sectheader.shТүрү == 8 {
					ZeroБлокЧоңойтууБАРАКкаталог(sectheader.shaddress, өлчөм, БАРАКкаталогentry)
				} else {
					destination_2 := GetБайтfromКөрсөткүч(uintptr(sectheader.shaddress), int(өлчөм), int(өлчөм))
					SetБлокЧоңойтууБАРАКкаталог(sectМааниси, destination_2, өлчөм, БАРАКкаталогentry)
				}
			}

			continue

			if EqualБайт(sectАты, ([]byte)(".text")) {
				console_2.MБасма(".text")
				console_2.MБасма("[")
				console_2.MUnsignedinteger32Басма(sectheader.shaddress)
				console_2.MБасма(":")
				console_2.MUnsignedinteger32Басма(sectheader.shoffset)
				console_2.MБасма(":")
				console_2.MUnsignedinteger32Басма(sectheader.shӨлчөм)
				console_2.MБасма("]")
				copy(self.текст[:sectheader.shӨлчөм], sectМааниси[:sectheader.shӨлчөм])
				self.текстlen = sectheader.shӨлчөм
			}
			if EqualБайт(sectАты, ([]byte)(".rel.text")) {
				console_2.MБасма(".rel.text")
				console_2.MБасма("[")
				console_2.MUnsignedinteger32Басма(sectheader.shaddress)
				console_2.MБасма(":")
				console_2.MUnsignedinteger32Басма(sectheader.shӨлчөм)
				console_2.MБасма("]")
				for rt := uint32(0); rt < sectheader.shӨлчөм/8; rt++ {
					offset := *(*uint32)(Pointer(&sectМааниси[rt*8]))
					self.relТекст[rt].offset = offset
					self.relТекст[rt].oaddress = *(*uint32)(Pointer(&self.текст[offset]))
					self.relТекст[rt].нОМЕР = *(*uint32)(Pointer(&sectМааниси[rt*8+4]))
					self.relТекстlen++
				}
			}
			if EqualБайт(sectАты, ([]byte)(".dynsym")) {
				console_2.MБасма(".dynsym")
				console_2.MБасма("[")
				console_2.MUnsignedinteger32Басма(sectheader.shaddress)
				console_2.MБасма(":")
				console_2.MUnsignedinteger32Басма(sectheader.shӨлчөм)
				console_2.MБасма("]")
				for rt := uint32(0); rt < sectheader.shӨлчөм/8; rt++ {
					offset := *(*uint32)(Pointer(&sectМааниси[rt*8]))
					self.relТекст[rt].offset = offset
					self.relТекст[rt].oaddress = *(*uint32)(Pointer(&self.текст[offset]))
					self.relТекст[rt].нОМЕР = *(*uint32)(Pointer(&sectМааниси[rt*8+4]))
					self.relТекстlen++
				}
			}
			if EqualБайт(sectАты, ([]byte)(".dynstr")) {
				console_2.MБасма(".dynstr")
				console_2.MБасма("[")
				console_2.MUnsignedinteger32Басма(sectheader.shaddress)
				console_2.MБасма(":")
				console_2.MUnsignedinteger32Басма(sectheader.shӨлчөм)
				console_2.MБасма("]")
			}
			if EqualБайт(sectАты, ([]byte)(".strtab")) {
				console_2.MБасма(".strtab")
				console_2.MБасма("[")
				console_2.MUnsignedinteger32Басма(sectheader.shaddress)
				console_2.MБасма("]")
				rt := uint32(0)
				жүргүзүү := uint32(0)

				for st := uint32(1); st < sectheader.shӨлчөм; st++ {
					if sectМааниси[st] == 0x0 || sectМааниси[st] == ' ' {
						funcАты := sectМааниси[жүргүзүү+1 : st]
						console_2.MБасма("+")
						console_2.MБасма(funcАты)
						self.strtab[rt] = БайтtoСАП(funcАты)
						жүргүзүү = st
						rt++
					}
				}

			}

		}

		console_2.MБасма(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relТекстlen; rt++ {
			console_2.MБасма("[")
			console_2.MБасма(([]byte)(self.strtab[rt]))
			console_2.MБасма(":")
			console_2.MUnsignedinteger32Басма(self.relТекст[rt].нОМЕР)
			console_2.MБасма(":")

			console_2.MБасма(([]byte)("]"))
		}
		console_2.MБасма(([]byte)("------------>"))

		if текстКөрсөткүч != nil {
			эсиmanager.Бош(текстКөрсөткүч)
		}

	}

}
