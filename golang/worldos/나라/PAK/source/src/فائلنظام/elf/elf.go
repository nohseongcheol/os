/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "console"
import . "util"
import . "یادداشتmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eنوعیت		uint16
	emachine	uint16
	eورژن		uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eجھنڈیاں	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shنام		uint32
	shنوعیت		uint32
	shجھنڈیاں	uint32
	shaddress	uint32
	shoffset	uint32
	shحجم		uint32
	shربط		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfپروگرامheader struct {
	pنوعیت		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pجھنڈیاں	uint32
	pسیدھ		uint32
}
type Elf32نوٹ struct {
	nnamesz	uint32
	ndescsz	uint32
	nنوعیت	uint32
}
type Elf32dyn struct {
	dtag		uint32
	dvalپؤائنٹر	uint32
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
	stنام	uint32
	stقدر	uint32
	stحجم	uint32
	stinfo	uint8
	stدیگر	uint8
	stshndx	uint16
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
	Dمحرک		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, Pصفحہڈائریکٹریentry uint32) {

	یادداشتmanager := Tیادداشتmanager{}
	var متنپؤائنٹر Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderحجم := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderحجم*i]))

			var sectنام []byte
			چلائیں := uint32(strtab.shoffset + sectheader.shنام)
			آخر := چلائیں
			for ; ; آخر++ {
				if data[آخر] == 0x0 || data[آخر] == ' ' {
					break
				}
			}
			sectنام = data[چلائیں:آخر]

			var sectقدر []byte
			if sectheader.shنوعیت != 8 {
				آخرoffset := sectheader.shoffset + sectheader.shحجم
				if آخرoffset < sectheader.shoffset || آخرoffset > uint32(len(data)) {
					continue
				}
				sectقدر = data[sectheader.shoffset:آخرoffset]
			}

			if Eبرابربائٹس(sectنام, ([]byte)(".got.plt")) {
				console_2.Mچھاپیں("[")
				console_2.Mچھاپیں(sectنام)
				console_2.Mچھاپیں(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32چھاپیں(self.Got)
				console_2.Mچھاپیں("]")
			}
			if Eبرابربائٹس(sectنام, ([]byte)(".dynamic")) {
				console_2.Mچھاپیں("[")
				console_2.Mچھاپیں(sectنام)
				console_2.Mچھاپیں(":")
				محرک := sectheader.shaddress
				self.Dمحرک = محرک
				console_2.MUnsignedinteger32چھاپیں(محرک)
				console_2.Mچھاپیں("]")
			}

			if sectheader.shaddress > 0x1000 {
				حجم := sectheader.shحجم
				if sectheader.shنوعیت == 8 {
					Zeroblockاندرصفحہڈائریکٹری(sectheader.shaddress, حجم, Pصفحہڈائریکٹریentry)
				} else {
					destination_2 := Getبائٹسfromپؤائنٹر(uintptr(sectheader.shaddress), int(حجم), int(حجم))
					Sسیٹblockاندرصفحہڈائریکٹری(sectقدر, destination_2, حجم, Pصفحہڈائریکٹریentry)
				}
			}

			continue

			if Eبرابربائٹس(sectنام, ([]byte)(".text")) {
				console_2.Mچھاپیں(".text")
				console_2.Mچھاپیں("[")
				console_2.MUnsignedinteger32چھاپیں(sectheader.shaddress)
				console_2.Mچھاپیں(":")
				console_2.MUnsignedinteger32چھاپیں(sectheader.shoffset)
				console_2.Mچھاپیں(":")
				console_2.MUnsignedinteger32چھاپیں(sectheader.shحجم)
				console_2.Mچھاپیں("]")
				copy(self.متن[:sectheader.shحجم], sectقدر[:sectheader.shحجم])
				self.متنlen = sectheader.shحجم
			}
			if Eبرابربائٹس(sectنام, ([]byte)(".rel.text")) {
				console_2.Mچھاپیں(".rel.text")
				console_2.Mچھاپیں("[")
				console_2.MUnsignedinteger32چھاپیں(sectheader.shaddress)
				console_2.Mچھاپیں(":")
				console_2.MUnsignedinteger32چھاپیں(sectheader.shحجم)
				console_2.Mچھاپیں("]")
				for rt := uint32(0); rt < sectheader.shحجم/8; rt++ {
					offset := *(*uint32)(Pointer(&sectقدر[rt*8]))
					self.relمتن[rt].offset = offset
					self.relمتن[rt].oaddress = *(*uint32)(Pointer(&self.متن[offset]))
					self.relمتن[rt].number = *(*uint32)(Pointer(&sectقدر[rt*8+4]))
					self.relمتنlen++
				}
			}
			if Eبرابربائٹس(sectنام, ([]byte)(".dynsym")) {
				console_2.Mچھاپیں(".dynsym")
				console_2.Mچھاپیں("[")
				console_2.MUnsignedinteger32چھاپیں(sectheader.shaddress)
				console_2.Mچھاپیں(":")
				console_2.MUnsignedinteger32چھاپیں(sectheader.shحجم)
				console_2.Mچھاپیں("]")
				for rt := uint32(0); rt < sectheader.shحجم/8; rt++ {
					offset := *(*uint32)(Pointer(&sectقدر[rt*8]))
					self.relمتن[rt].offset = offset
					self.relمتن[rt].oaddress = *(*uint32)(Pointer(&self.متن[offset]))
					self.relمتن[rt].number = *(*uint32)(Pointer(&sectقدر[rt*8+4]))
					self.relمتنlen++
				}
			}
			if Eبرابربائٹس(sectنام, ([]byte)(".dynstr")) {
				console_2.Mچھاپیں(".dynstr")
				console_2.Mچھاپیں("[")
				console_2.MUnsignedinteger32چھاپیں(sectheader.shaddress)
				console_2.Mچھاپیں(":")
				console_2.MUnsignedinteger32چھاپیں(sectheader.shحجم)
				console_2.Mچھاپیں("]")
			}
			if Eبرابربائٹس(sectنام, ([]byte)(".strtab")) {
				console_2.Mچھاپیں(".strtab")
				console_2.Mچھاپیں("[")
				console_2.MUnsignedinteger32چھاپیں(sectheader.shaddress)
				console_2.Mچھاپیں("]")
				rt := uint32(0)
				چلائیں := uint32(0)

				for st := uint32(1); st < sectheader.shحجم; st++ {
					if sectقدر[st] == 0x0 || sectقدر[st] == ' ' {
						funcنام := sectقدر[چلائیں+1 : st]
						console_2.Mچھاپیں("+")
						console_2.Mچھاپیں(funcنام)
						self.strtab[rt] = Bبائٹسtoڈورا(funcنام)
						چلائیں = st
						rt++
					}
				}

			}

		}

		console_2.Mچھاپیں(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relمتنlen; rt++ {
			console_2.Mچھاپیں("[")
			console_2.Mچھاپیں(([]byte)(self.strtab[rt]))
			console_2.Mچھاپیں(":")
			console_2.MUnsignedinteger32چھاپیں(self.relمتن[rt].number)
			console_2.Mچھاپیں(":")

			console_2.Mچھاپیں(([]byte)("]"))
		}
		console_2.Mچھاپیں(([]byte)("------------>"))

		if متنپؤائنٹر != nil {
			یادداشتmanager.Fخالی(متنپؤائنٹر)
		}

	}

}
