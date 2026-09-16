/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "console"
import . "util"
import . "μνήμηmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eΤύπος		uint16
	emachine	uint16
	eΈκδοση		uint32
	eκαταχώρηση	uint32
	ephoff		uint32
	eshoff		uint32
	eΔιακόπτες	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shΌνομα		uint32
	shΤύπος		uint32
	shΔιακόπτες	uint32
	shaddress	uint32
	shoffset	uint32
	shΜέγεθος	uint32
	shΔεσμός	uint32
	shπληροφορία	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfπρόγραμμαheader struct {
	pΤύπος		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pΔιακόπτες	uint32
	pΣτοίχιση	uint32
}
type Elf32Σημείωση struct {
	nnamesz	uint32
	ndescsz	uint32
	nΤύπος	uint32
}
type Elf32dyn struct {
	dΕτικέτα	uint32
	dvalΔείκτης	uint32
}
type Elf32rel struct {
	roffset		uint32
	rπληροφορία	uint32
}
type Elf32rela struct {
	roffset		uint32
	rπληροφορία	uint32
	raddend		uint32
}
type Elf32sym struct {
	stΌνομα		uint32
	stΤιμή		uint32
	stΜέγεθος	uint32
	stπληροφορία	uint8
	stΆλλο		uint8
	stshndx		uint16
}
type relocationΚείμενο struct {
	offset		uint32
	αριθμός		uint32
	oaddress	uint32
}
type Elf struct {
	κείμενο		[]byte
	κείμενοlen	uint32
	relΚείμενο	[100]relocationΚείμενο
	relΚείμενοlen	uint32
	strtab		[100]string
	Got		uint32
	Δυναμικό	uint32
}

func (self *Elf) Getκαταχώρηση(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eκαταχώρηση
}

func (self *Elf) Parse(data []byte, ΣελίδαΚατάλογοςκαταχώρηση uint32) {

	μνήμηmanager := TΜνήμηmanager{}
	var κείμενοΔείκτης Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderΜέγεθος := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderΜέγεθος*i]))

			var sectΌνομα []byte
			έναρξη := uint32(strtab.shoffset + sectheader.shΌνομα)
			τέλος := έναρξη
			for ; ; τέλος++ {
				if data[τέλος] == 0x0 || data[τέλος] == ' ' {
					break
				}
			}
			sectΌνομα = data[έναρξη:τέλος]

			var sectΤιμή []byte
			if sectheader.shΤύπος != 8 {
				τέλοςoffset := sectheader.shoffset + sectheader.shΜέγεθος
				if τέλοςoffset < sectheader.shoffset || τέλοςoffset > uint32(len(data)) {
					continue
				}
				sectΤιμή = data[sectheader.shoffset:τέλοςoffset]
			}

			if Ίσοbytes(sectΌνομα, ([]byte)(".got.plt")) {
				console_2.MΕκτύπωση("[")
				console_2.MΕκτύπωση(sectΌνομα)
				console_2.MΕκτύπωση(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Εκτύπωση(self.Got)
				console_2.MΕκτύπωση("]")
			}
			if Ίσοbytes(sectΌνομα, ([]byte)(".dynamic")) {
				console_2.MΕκτύπωση("[")
				console_2.MΕκτύπωση(sectΌνομα)
				console_2.MΕκτύπωση(":")
				δυναμικό := sectheader.shaddress
				self.Δυναμικό = δυναμικό
				console_2.MUnsignedinteger32Εκτύπωση(δυναμικό)
				console_2.MΕκτύπωση("]")
			}

			if sectheader.shaddress > 0x1000 {
				μέγεθος := sectheader.shΜέγεθος
				if sectheader.shΤύπος == 8 {
					ΜηδένΜπλοκσεΣελίδαΚατάλογος(sectheader.shaddress, μέγεθος, ΣελίδαΚατάλογοςκαταχώρηση)
				} else {
					προορισμός_2 := GetbytesfromΔείκτης(uintptr(sectheader.shaddress), int(μέγεθος), int(μέγεθος))
					ΣύνολοΜπλοκσεΣελίδαΚατάλογος(sectΤιμή, προορισμός_2, μέγεθος, ΣελίδαΚατάλογοςκαταχώρηση)
				}
			}

			continue

			if Ίσοbytes(sectΌνομα, ([]byte)(".text")) {
				console_2.MΕκτύπωση(".text")
				console_2.MΕκτύπωση("[")
				console_2.MUnsignedinteger32Εκτύπωση(sectheader.shaddress)
				console_2.MΕκτύπωση(":")
				console_2.MUnsignedinteger32Εκτύπωση(sectheader.shoffset)
				console_2.MΕκτύπωση(":")
				console_2.MUnsignedinteger32Εκτύπωση(sectheader.shΜέγεθος)
				console_2.MΕκτύπωση("]")
				copy(self.κείμενο[:sectheader.shΜέγεθος], sectΤιμή[:sectheader.shΜέγεθος])
				self.κείμενοlen = sectheader.shΜέγεθος
			}
			if Ίσοbytes(sectΌνομα, ([]byte)(".rel.text")) {
				console_2.MΕκτύπωση(".rel.text")
				console_2.MΕκτύπωση("[")
				console_2.MUnsignedinteger32Εκτύπωση(sectheader.shaddress)
				console_2.MΕκτύπωση(":")
				console_2.MUnsignedinteger32Εκτύπωση(sectheader.shΜέγεθος)
				console_2.MΕκτύπωση("]")
				for rt := uint32(0); rt < sectheader.shΜέγεθος/8; rt++ {
					offset := *(*uint32)(Pointer(&sectΤιμή[rt*8]))
					self.relΚείμενο[rt].offset = offset
					self.relΚείμενο[rt].oaddress = *(*uint32)(Pointer(&self.κείμενο[offset]))
					self.relΚείμενο[rt].αριθμός = *(*uint32)(Pointer(&sectΤιμή[rt*8+4]))
					self.relΚείμενοlen++
				}
			}
			if Ίσοbytes(sectΌνομα, ([]byte)(".dynsym")) {
				console_2.MΕκτύπωση(".dynsym")
				console_2.MΕκτύπωση("[")
				console_2.MUnsignedinteger32Εκτύπωση(sectheader.shaddress)
				console_2.MΕκτύπωση(":")
				console_2.MUnsignedinteger32Εκτύπωση(sectheader.shΜέγεθος)
				console_2.MΕκτύπωση("]")
				for rt := uint32(0); rt < sectheader.shΜέγεθος/8; rt++ {
					offset := *(*uint32)(Pointer(&sectΤιμή[rt*8]))
					self.relΚείμενο[rt].offset = offset
					self.relΚείμενο[rt].oaddress = *(*uint32)(Pointer(&self.κείμενο[offset]))
					self.relΚείμενο[rt].αριθμός = *(*uint32)(Pointer(&sectΤιμή[rt*8+4]))
					self.relΚείμενοlen++
				}
			}
			if Ίσοbytes(sectΌνομα, ([]byte)(".dynstr")) {
				console_2.MΕκτύπωση(".dynstr")
				console_2.MΕκτύπωση("[")
				console_2.MUnsignedinteger32Εκτύπωση(sectheader.shaddress)
				console_2.MΕκτύπωση(":")
				console_2.MUnsignedinteger32Εκτύπωση(sectheader.shΜέγεθος)
				console_2.MΕκτύπωση("]")
			}
			if Ίσοbytes(sectΌνομα, ([]byte)(".strtab")) {
				console_2.MΕκτύπωση(".strtab")
				console_2.MΕκτύπωση("[")
				console_2.MUnsignedinteger32Εκτύπωση(sectheader.shaddress)
				console_2.MΕκτύπωση("]")
				rt := uint32(0)
				έναρξη := uint32(0)

				for st := uint32(1); st < sectheader.shΜέγεθος; st++ {
					if sectΤιμή[st] == 0x0 || sectΤιμή[st] == ' ' {
						funcΌνομα := sectΤιμή[έναρξη+1 : st]
						console_2.MΕκτύπωση("+")
						console_2.MΕκτύπωση(funcΌνομα)
						self.strtab[rt] = BytestoΣυμβολοσειρά(funcΌνομα)
						έναρξη = st
						rt++
					}
				}

			}

		}

		console_2.MΕκτύπωση(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relΚείμενοlen; rt++ {
			console_2.MΕκτύπωση("[")
			console_2.MΕκτύπωση(([]byte)(self.strtab[rt]))
			console_2.MΕκτύπωση(":")
			console_2.MUnsignedinteger32Εκτύπωση(self.relΚείμενο[rt].αριθμός)
			console_2.MΕκτύπωση(":")

			console_2.MΕκτύπωση(([]byte)("]"))
		}
		console_2.MΕκτύπωση(([]byte)("------------>"))

		if κείμενοΔείκτης != nil {
			μνήμηmanager.Ελεύθερα(κείμενοΔείκτης)
		}

	}

}
