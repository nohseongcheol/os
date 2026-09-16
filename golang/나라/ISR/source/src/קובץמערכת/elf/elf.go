/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"

import . "console"
import . "util"
import . "זיכרוןmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eסוג		uint16
	emachine	uint16
	eגרסה		uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eדגלים		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shשם		uint32
	shסוג		uint32
	shדגלים		uint32
	shaddress	uint32
	shoffset	uint32
	shגודל		uint32
	shקישור		uint32
	shמידע		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfתכניתheader struct {
	pסוג	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pדגלים	uint32
	pישר	uint32
}
type Elf32פתקית struct {
	nnamesz	uint32
	ndescsz	uint32
	nסוג	uint32
}
type Elf32dyn struct {
	dתג	uint32
	dvalסמן	uint32
}
type Elf32rel struct {
	roffset	uint32
	rמידע	uint32
}
type Elf32rela struct {
	roffset	uint32
	rמידע	uint32
	raddend	uint32
}
type Elf32sym struct {
	stשם	uint32
	stערך	uint32
	stגודל	uint32
	stמידע	uint8
	stאחר	uint8
	stshndx	uint16
}
type relocationטקסט struct {
	offset		uint32
	מספר		uint32
	oaddress	uint32
}
type Elf struct {
	טקסט		[]byte
	טקסטlen		uint32
	relטקסט		[100]relocationטקסט
	relטקסטlen	uint32
	strtab		[100]string
	Got		uint32
	Dדינמי		uint32
}

func (self *Elf) Getentry(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eentry
}

func (self *Elf) Parse(data []byte, Pעמודספרייהentry uint32) {

	זיכרוןmanager := Tזיכרוןmanager{}
	var טקסטסמן Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderגודל := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderגודל*i]))

			var sectשם []byte
			התחלה := uint32(strtab.shoffset + sectheader.shשם)
			סיום := התחלה
			for ; ; סיום++ {
				if data[סיום] == 0x0 || data[סיום] == ' ' {
					break
				}
			}
			sectשם = data[התחלה:סיום]

			var sectערך []byte
			if sectheader.shסוג != 8 {
				סיוםoffset := sectheader.shoffset + sectheader.shגודל
				if סיוםoffset < sectheader.shoffset || סיוםoffset > uint32(len(data)) {
					continue
				}
				sectערך = data[sectheader.shoffset:סיוםoffset]
			}

			if Equalבתים(sectשם, ([]byte)(".got.plt")) {
				console_2.Mהדפסה("[")
				console_2.Mהדפסה(sectשם)
				console_2.Mהדפסה(":")
				self.Got = sectheader.shaddress
				console_2.MUnsignedinteger32הדפסה(self.Got)
				console_2.Mהדפסה("]")
			}
			if Equalבתים(sectשם, ([]byte)(".dynamic")) {
				console_2.Mהדפסה("[")
				console_2.Mהדפסה(sectשם)
				console_2.Mהדפסה(":")
				דינמי := sectheader.shaddress
				self.Dדינמי = דינמי
				console_2.MUnsignedinteger32הדפסה(דינמי)
				console_2.Mהדפסה("]")
			}

			if sectheader.shaddress > 0x1000 {
				גודל := sectheader.shגודל
				if sectheader.shסוג == 8 {
					Zeroבלוקנכנסעמודספרייה(sectheader.shaddress, גודל, Pעמודספרייהentry)
				} else {
					יעד_2 := Getבתיםfromסמן(uintptr(sectheader.shaddress), int(גודל), int(גודל))
					Sקבעבלוקנכנסעמודספרייה(sectערך, יעד_2, גודל, Pעמודספרייהentry)
				}
			}

			continue

			if Equalבתים(sectשם, ([]byte)(".text")) {
				console_2.Mהדפסה(".text")
				console_2.Mהדפסה("[")
				console_2.MUnsignedinteger32הדפסה(sectheader.shaddress)
				console_2.Mהדפסה(":")
				console_2.MUnsignedinteger32הדפסה(sectheader.shoffset)
				console_2.Mהדפסה(":")
				console_2.MUnsignedinteger32הדפסה(sectheader.shגודל)
				console_2.Mהדפסה("]")
				copy(self.טקסט[:sectheader.shגודל], sectערך[:sectheader.shגודל])
				self.טקסטlen = sectheader.shגודל
			}
			if Equalבתים(sectשם, ([]byte)(".rel.text")) {
				console_2.Mהדפסה(".rel.text")
				console_2.Mהדפסה("[")
				console_2.MUnsignedinteger32הדפסה(sectheader.shaddress)
				console_2.Mהדפסה(":")
				console_2.MUnsignedinteger32הדפסה(sectheader.shגודל)
				console_2.Mהדפסה("]")
				for rt := uint32(0); rt < sectheader.shגודל/8; rt++ {
					offset := *(*uint32)(Pointer(&sectערך[rt*8]))
					self.relטקסט[rt].offset = offset
					self.relטקסט[rt].oaddress = *(*uint32)(Pointer(&self.טקסט[offset]))
					self.relטקסט[rt].מספר = *(*uint32)(Pointer(&sectערך[rt*8+4]))
					self.relטקסטlen++
				}
			}
			if Equalבתים(sectשם, ([]byte)(".dynsym")) {
				console_2.Mהדפסה(".dynsym")
				console_2.Mהדפסה("[")
				console_2.MUnsignedinteger32הדפסה(sectheader.shaddress)
				console_2.Mהדפסה(":")
				console_2.MUnsignedinteger32הדפסה(sectheader.shגודל)
				console_2.Mהדפסה("]")
				for rt := uint32(0); rt < sectheader.shגודל/8; rt++ {
					offset := *(*uint32)(Pointer(&sectערך[rt*8]))
					self.relטקסט[rt].offset = offset
					self.relטקסט[rt].oaddress = *(*uint32)(Pointer(&self.טקסט[offset]))
					self.relטקסט[rt].מספר = *(*uint32)(Pointer(&sectערך[rt*8+4]))
					self.relטקסטlen++
				}
			}
			if Equalבתים(sectשם, ([]byte)(".dynstr")) {
				console_2.Mהדפסה(".dynstr")
				console_2.Mהדפסה("[")
				console_2.MUnsignedinteger32הדפסה(sectheader.shaddress)
				console_2.Mהדפסה(":")
				console_2.MUnsignedinteger32הדפסה(sectheader.shגודל)
				console_2.Mהדפסה("]")
			}
			if Equalבתים(sectשם, ([]byte)(".strtab")) {
				console_2.Mהדפסה(".strtab")
				console_2.Mהדפסה("[")
				console_2.MUnsignedinteger32הדפסה(sectheader.shaddress)
				console_2.Mהדפסה("]")
				rt := uint32(0)
				התחלה := uint32(0)

				for st := uint32(1); st < sectheader.shגודל; st++ {
					if sectערך[st] == 0x0 || sectערך[st] == ' ' {
						funcשם := sectערך[התחלה+1 : st]
						console_2.Mהדפסה("+")
						console_2.Mהדפסה(funcשם)
						self.strtab[rt] = Bבתיםtoמחרוזת(funcשם)
						התחלה = st
						rt++
					}
				}

			}

		}

		console_2.Mהדפסה(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relטקסטlen; rt++ {
			console_2.Mהדפסה("[")
			console_2.Mהדפסה(([]byte)(self.strtab[rt]))
			console_2.Mהדפסה(":")
			console_2.MUnsignedinteger32הדפסה(self.relטקסט[rt].מספר)
			console_2.Mהדפסה(":")

			console_2.Mהדפסה(([]byte)("]"))
		}
		console_2.Mהדפסה(([]byte)("------------>"))

		if טקסטסמן != nil {
			זיכרוןmanager.Fפנוי(טקסטסמן)
		}

	}

}
