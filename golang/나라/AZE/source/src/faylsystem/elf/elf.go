package elf

import . "unsafe"

import . "console"
import . "util"
import . "yaddaşmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eNöv		uint16
	emachine	uint16
	eversion	uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eBayraqlar	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shAd		uint32
	shNöv		uint32
	shBayraqlar	uint32
	shaddress	uint32
	shoffset	uint32
	shBöyüklük	uint32
	shkörpü		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfproqramheader struct {
	pNöv		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pBayraqlar	uint32
	palign		uint32
}
type Elf32note struct {
	nnamesz	uint32
	ndescsz	uint32
	nNöv	uint32
}
type Elf32dyn struct {
	dtag		uint32
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
	stAd		uint32
	stQiymət	uint32
	stBöyüklük	uint32
	stinfo		uint8
	stother		uint8
	stshndx		uint16
}
type relocationMətn struct {
	offset		uint32
	number		uint32
	oaddress	uint32
}
type Elf struct {
	mətn		[]byte
	mətnlen		uint32
	relMətn		[100]relocationMətn
	relMətnlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, SəhifəCərgəentry uint32) {

	yaddaşmanager := TYaddaşmanager{}
	var mətnpointer Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderBöyüklük := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderBöyüklük*i]))

			var sectAd []byte
			start := uint32(strtab.shoffset + sectheader.shAd)
			end := start
			for ; ; end++ {
				if data[end] == 0x0 || data[end] == ' ' {
					break
				}
			}
			sectAd = data[start:end]

			var sectQiymət []byte
			if sectheader.shNöv != 8 {
				endoffset := sectheader.shoffset + sectheader.shBöyüklük
				if endoffset < sectheader.shoffset || endoffset > uint32(len(data)) {
					continue
				}
				sectQiymət = data[sectheader.shoffset:endoffset]
			}

			if EqualBayt(sectAd, ([]byte)(".got.plt")) {
				console_2.MÇapEt("[")
				console_2.MÇapEt(sectAd)
				console_2.MÇapEt(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32ÇapEt(self.Got)
				console_2.MÇapEt("]")
			}
			if EqualBayt(sectAd, ([]byte)(".dynamic")) {
				console_2.MÇapEt("[")
				console_2.MÇapEt(sectAd)
				console_2.MÇapEt(":")
				dynamic := sectheader.shaddress
				self.Dynamic = dynamic
				console_2.MUnsignedinteger32ÇapEt(dynamic)
				console_2.MÇapEt("]")
			}

			if sectheader.shaddress > 0x1000 {
				böyüklük := sectheader.shBöyüklük
				if sectheader.shNöv == 8 {
					ZeroblockinSəhifəCərgə(sectheader.shaddress, böyüklük, SəhifəCərgəentry)
				} else {
					destination_2 := GetBaytfrompointer(uintptr(sectheader.shaddress), int(böyüklük), int(böyüklük))
					SetblockinSəhifəCərgə(sectQiymət, destination_2, böyüklük, SəhifəCərgəentry)
				}
			}

			continue

			if EqualBayt(sectAd, ([]byte)(".text")) {
				console_2.MÇapEt(".text")
				console_2.MÇapEt("[")
				console_2.MUnsignedinteger32ÇapEt(sectheader.shaddress)
				console_2.MÇapEt(":")
				console_2.MUnsignedinteger32ÇapEt(sectheader.shoffset)
				console_2.MÇapEt(":")
				console_2.MUnsignedinteger32ÇapEt(sectheader.shBöyüklük)
				console_2.MÇapEt("]")
				copy(self.mətn[:sectheader.shBöyüklük], sectQiymət[:sectheader.shBöyüklük])
				self.mətnlen = sectheader.shBöyüklük
			}
			if EqualBayt(sectAd, ([]byte)(".rel.text")) {
				console_2.MÇapEt(".rel.text")
				console_2.MÇapEt("[")
				console_2.MUnsignedinteger32ÇapEt(sectheader.shaddress)
				console_2.MÇapEt(":")
				console_2.MUnsignedinteger32ÇapEt(sectheader.shBöyüklük)
				console_2.MÇapEt("]")
				for rt := uint32(0); rt < sectheader.shBöyüklük/8; rt++ {
					offset := *(*uint32)(Pointer(&sectQiymət[rt*8]))
					self.relMətn[rt].offset = offset
					self.relMətn[rt].oaddress = *(*uint32)(Pointer(&self.mətn[offset]))
					self.relMətn[rt].number = *(*uint32)(Pointer(&sectQiymət[rt*8+4]))
					self.relMətnlen++
				}
			}
			if EqualBayt(sectAd, ([]byte)(".dynsym")) {
				console_2.MÇapEt(".dynsym")
				console_2.MÇapEt("[")
				console_2.MUnsignedinteger32ÇapEt(sectheader.shaddress)
				console_2.MÇapEt(":")
				console_2.MUnsignedinteger32ÇapEt(sectheader.shBöyüklük)
				console_2.MÇapEt("]")
				for rt := uint32(0); rt < sectheader.shBöyüklük/8; rt++ {
					offset := *(*uint32)(Pointer(&sectQiymət[rt*8]))
					self.relMətn[rt].offset = offset
					self.relMətn[rt].oaddress = *(*uint32)(Pointer(&self.mətn[offset]))
					self.relMətn[rt].number = *(*uint32)(Pointer(&sectQiymət[rt*8+4]))
					self.relMətnlen++
				}
			}
			if EqualBayt(sectAd, ([]byte)(".dynstr")) {
				console_2.MÇapEt(".dynstr")
				console_2.MÇapEt("[")
				console_2.MUnsignedinteger32ÇapEt(sectheader.shaddress)
				console_2.MÇapEt(":")
				console_2.MUnsignedinteger32ÇapEt(sectheader.shBöyüklük)
				console_2.MÇapEt("]")
			}
			if EqualBayt(sectAd, ([]byte)(".strtab")) {
				console_2.MÇapEt(".strtab")
				console_2.MÇapEt("[")
				console_2.MUnsignedinteger32ÇapEt(sectheader.shaddress)
				console_2.MÇapEt("]")
				rt := uint32(0)
				start := uint32(0)

				for st := uint32(1); st < sectheader.shBöyüklük; st++ {
					if sectQiymət[st] == 0x0 || sectQiymət[st] == ' ' {
						funcAd := sectQiymət[start+1 : st]
						console_2.MÇapEt("+")
						console_2.MÇapEt(funcAd)
						self.strtab[rt] = Bayttostring(funcAd)
						start = st
						rt++
					}
				}

			}

		}

		console_2.MÇapEt(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relMətnlen; rt++ {
			console_2.MÇapEt("[")
			console_2.MÇapEt(([]byte)(self.strtab[rt]))
			console_2.MÇapEt(":")
			console_2.MUnsignedinteger32ÇapEt(self.relMətn[rt].number)
			console_2.MÇapEt(":")

			console_2.MÇapEt(([]byte)("]"))
		}
		console_2.MÇapEt(([]byte)("------------>"))

		if mətnpointer != nil {
			yaddaşmanager.Boş(mətnpointer)
		}

	}

}
