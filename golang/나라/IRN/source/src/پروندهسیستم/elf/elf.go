package elf

import . "unsafe"

import . "console"
import . "util"
import . "حافظهmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eنوع		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eflags		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shنام		uint32
	shنوع		uint32
	shflags		uint32
	shaddress	uint32
	shoffset	uint32
	shاندازه	uint32
	shپیوند		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfبرنامهheader struct {
	pنوع	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pflags	uint32
	pردیف	uint32
}
type Elf32یادداشت struct {
	nnamesz	uint32
	ndescsz	uint32
	nنوع	uint32
}
type Elf32dyn struct {
	dبرچسب		uint32
	dvalpointer	uint32
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
	stنام		uint32
	stمقدار		uint32
	stاندازه	uint32
	stinfo		uint8
	stبقیه		uint8
	stshndx		uint16
}
type relocationمتن struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	متن		[]byte
	متنlen		uint32
	relمتن		[100]relocationمتن
	relمتنlen	uint32
	strtab		[100]string
	Got		uint32
	Dپویا		uint32
}

func (خود *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (خود *Elf) Parse(data []byte, Pصفحهشاخهentry uint32) {

	حافظهmanager := Tحافظهmanager{}
	var متنpointer Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderاندازه := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderاندازه*i]))

			var sectنام []byte
			start := uint32(strtab.shoffset + sectheader.shنام)
			پایان := start
			for ; ; پایان++ {
				if data[پایان] == 0x0 || data[پایان] == ' ' {
					break
				}
			}
			sectنام = data[start:پایان]

			var sectمقدار []byte
			if sectheader.shنوع != 8 {
				پایانoffset := sectheader.shoffset + sectheader.shاندازه
				if پایانoffset < sectheader.shoffset || پایانoffset > uint32(len(data)) {
					continue
				}
				sectمقدار = data[sectheader.shoffset:پایانoffset]
			}

			if Equalبایت(sectنام, ([]byte)(".got.plt")) {
				console_2.Mچاپ("[")
				console_2.Mچاپ(sectنام)
				console_2.Mچاپ(":")
				خود.Got = sectheader.shaddress
				console_2.MUnsignedinteger32چاپ(خود.Got)
				console_2.Mچاپ("]")
			}
			if Equalبایت(sectنام, ([]byte)(".dynamic")) {
				console_2.Mچاپ("[")
				console_2.Mچاپ(sectنام)
				console_2.Mچاپ(":")
				پویا := sectheader.shaddress
				خود.Dپویا = پویا
				console_2.MUnsignedinteger32چاپ(پویا)
				console_2.Mچاپ("]")
			}

			if sectheader.shaddress > 0x1000 {
				اندازه := sectheader.shاندازه
				if sectheader.shنوع == 8 {
					Zeroقطعهداخلصفحهشاخه(sectheader.shaddress, اندازه, Pصفحهشاخهentry)
				} else {
					مقصد_2 := Getبایتfrompointer(uintptr(sectheader.shaddress), int(اندازه), int(اندازه))
					Setقطعهداخلصفحهشاخه(sectمقدار, مقصد_2, اندازه, Pصفحهشاخهentry)
				}
			}

			continue

			if Equalبایت(sectنام, ([]byte)(".text")) {
				console_2.Mچاپ(".text")
				console_2.Mچاپ("[")
				console_2.MUnsignedinteger32چاپ(sectheader.shaddress)
				console_2.Mچاپ(":")
				console_2.MUnsignedinteger32چاپ(sectheader.shoffset)
				console_2.Mچاپ(":")
				console_2.MUnsignedinteger32چاپ(sectheader.shاندازه)
				console_2.Mچاپ("]")
				copy(خود.متن[:sectheader.shاندازه], sectمقدار[:sectheader.shاندازه])
				خود.متنlen = sectheader.shاندازه
			}
			if Equalبایت(sectنام, ([]byte)(".rel.text")) {
				console_2.Mچاپ(".rel.text")
				console_2.Mچاپ("[")
				console_2.MUnsignedinteger32چاپ(sectheader.shaddress)
				console_2.Mچاپ(":")
				console_2.MUnsignedinteger32چاپ(sectheader.shاندازه)
				console_2.Mچاپ("]")
				for rt := uint32(0); rt < sectheader.shاندازه/8; rt++ {
					offset := *(*uint32)(Pointer(&sectمقدار[rt*8]))
					خود.relمتن[rt].offset = offset
					خود.relمتن[rt].oaddress = *(*uint32)(Pointer(&خود.متن[offset]))
					خود.relمتن[rt].number = *(*uint32)(Pointer(&sectمقدار[rt*8+4]))
					خود.relمتنlen++
				}
			}
			if Equalبایت(sectنام, ([]byte)(".dynsym")) {
				console_2.Mچاپ(".dynsym")
				console_2.Mچاپ("[")
				console_2.MUnsignedinteger32چاپ(sectheader.shaddress)
				console_2.Mچاپ(":")
				console_2.MUnsignedinteger32چاپ(sectheader.shاندازه)
				console_2.Mچاپ("]")
				for rt := uint32(0); rt < sectheader.shاندازه/8; rt++ {
					offset := *(*uint32)(Pointer(&sectمقدار[rt*8]))
					خود.relمتن[rt].offset = offset
					خود.relمتن[rt].oaddress = *(*uint32)(Pointer(&خود.متن[offset]))
					خود.relمتن[rt].number = *(*uint32)(Pointer(&sectمقدار[rt*8+4]))
					خود.relمتنlen++
				}
			}
			if Equalبایت(sectنام, ([]byte)(".dynstr")) {
				console_2.Mچاپ(".dynstr")
				console_2.Mچاپ("[")
				console_2.MUnsignedinteger32چاپ(sectheader.shaddress)
				console_2.Mچاپ(":")
				console_2.MUnsignedinteger32چاپ(sectheader.shاندازه)
				console_2.Mچاپ("]")
			}
			if Equalبایت(sectنام, ([]byte)(".strtab")) {
				console_2.Mچاپ(".strtab")
				console_2.Mچاپ("[")
				console_2.MUnsignedinteger32چاپ(sectheader.shaddress)
				console_2.Mچاپ("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectheader.shاندازه; st++ {
					if sectمقدار[st] == 0x0 || sectمقدار[st] == ' ' {
						funcنام := sectمقدار[start+1 : st]
						console_2.Mچاپ("+")
						console_2.Mچاپ(funcنام)
						خود.strtab[rt] = Bبایتtoرشته(funcنام)
						start = st
						rt++
					}
				}

			}

		}

		console_2.Mچاپ(([]byte)("<------------"))
		for rt := uint32(0); rt < خود.relمتنlen; rt++ {
			console_2.Mچاپ("[")
			console_2.Mچاپ(([]byte)(خود.strtab[rt]))
			console_2.Mچاپ(":")
			console_2.MUnsignedinteger32چاپ(خود.relمتن[rt].number)
			console_2.Mچاپ(":")

			console_2.Mچاپ(([]byte)("]"))
		}
		console_2.Mچاپ(([]byte)("------------>"))

		if متنpointer != nil {
			حافظهmanager.Fآزاد(متنpointer)
		}

	}

}
