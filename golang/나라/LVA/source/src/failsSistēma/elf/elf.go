package elf

import . "unsafe"

import . "console"
import . "util"
import . "atmiņamanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTips		uint16
	emachine	uint16
	eVersija	uint32
	eieraksts	uint32
	ephoff		uint32
	eshoff		uint32
	eKarogi		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNosaukums	uint32
	shTips		uint32
	shKarogi	uint32
	shaddress	uint32
	shoffset	uint32
	shIzmērs	uint32
	shSaite		uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogrammaheader struct {
	pTips		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pKarogi		uint32
	pLīdzināt	uint32
}
type Elf32Piezīme struct {
	nnamesz	uint32
	ndescsz	uint32
	nTips	uint32
}
type Elf32dyn struct {
	dBirka		uint32
	dvalKursors	uint32
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
	stNosaukums	uint32
	stVērtība	uint32
	stIzmērs	uint32
	stinfo		uint8
	stCiti		uint8
	stshndx		uint16
}
type relocationTeksts struct {
	offset		uint32
	skaitlis	uint32
	oaddress	uint32
}
type Elf struct {
	teksts		[]byte
	tekstslen	uint32
	relTeksts	[100]relocationTeksts
	relTekstslen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (pats *Elf) Getieraksts(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eieraksts
}

func (pats *Elf) Parse(data []byte, LapaMapeieraksts uint32) {

	atmiņamanager := TAtmiņamanager{}
	var tekstsKursors Pointer = nil

	var console_2 = TConsole{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderIzmērs := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderIzmērs*i]))

			var sectNosaukums []byte
			startēt := uint32(strtab.shoffset + sectheader.shNosaukums)
			beigas := startēt
			for ; ; beigas++ {
				if data[beigas] == 0x0 || data[beigas] == ' ' {
					break
				}
			}
			sectNosaukums = data[startēt:beigas]

			var sectVērtība []byte
			if sectheader.shTips != 8 {
				beigasoffset := sectheader.shoffset + sectheader.shIzmērs
				if beigasoffset < sectheader.shoffset || beigasoffset > uint32(len(data)) {
					continue
				}
				sectVērtība = data[sectheader.shoffset:beigasoffset]
			}

			if VienādsBaiti(sectNosaukums, ([]byte)(".got.plt")) {
				console_2.MDrukāt("[")
				console_2.MDrukāt(sectNosaukums)
				console_2.MDrukāt(":")
				pats.Got = sectheader.shaddress
				console_2.MUnsignedinteger32Drukāt(pats.Got)
				console_2.MDrukāt("]")
			}
			if VienādsBaiti(sectNosaukums, ([]byte)(".dynamic")) {
				console_2.MDrukāt("[")
				console_2.MDrukāt(sectNosaukums)
				console_2.MDrukāt(":")
				dynamic := sectheader.shaddress
				pats.Dynamic = dynamic
				console_2.MUnsignedinteger32Drukāt(dynamic)
				console_2.MDrukāt("]")
			}

			if sectheader.shaddress > 0x1000 {
				izmērs := sectheader.shIzmērs
				if sectheader.shTips == 8 {
					ZeroBloksIenākošāLapaMape(sectheader.shaddress, izmērs, LapaMapeieraksts)
				} else {
					mērķis_2 := GetBaitifromKursors(uintptr(sectheader.shaddress), int(izmērs), int(izmērs))
					KopaBloksIenākošāLapaMape(sectVērtība, mērķis_2, izmērs, LapaMapeieraksts)
				}
			}

			continue

			if VienādsBaiti(sectNosaukums, ([]byte)(".text")) {
				console_2.MDrukāt(".text")
				console_2.MDrukāt("[")
				console_2.MUnsignedinteger32Drukāt(sectheader.shaddress)
				console_2.MDrukāt(":")
				console_2.MUnsignedinteger32Drukāt(sectheader.shoffset)
				console_2.MDrukāt(":")
				console_2.MUnsignedinteger32Drukāt(sectheader.shIzmērs)
				console_2.MDrukāt("]")
				copy(pats.teksts[:sectheader.shIzmērs], sectVērtība[:sectheader.shIzmērs])
				pats.tekstslen = sectheader.shIzmērs
			}
			if VienādsBaiti(sectNosaukums, ([]byte)(".rel.text")) {
				console_2.MDrukāt(".rel.text")
				console_2.MDrukāt("[")
				console_2.MUnsignedinteger32Drukāt(sectheader.shaddress)
				console_2.MDrukāt(":")
				console_2.MUnsignedinteger32Drukāt(sectheader.shIzmērs)
				console_2.MDrukāt("]")
				for rt := uint32(0); rt < sectheader.shIzmērs/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVērtība[rt*8]))
					pats.relTeksts[rt].offset = offset
					pats.relTeksts[rt].oaddress = *(*uint32)(Pointer(&pats.teksts[offset]))
					pats.relTeksts[rt].skaitlis = *(*uint32)(Pointer(&sectVērtība[rt*8+4]))
					pats.relTekstslen++
				}
			}
			if VienādsBaiti(sectNosaukums, ([]byte)(".dynsym")) {
				console_2.MDrukāt(".dynsym")
				console_2.MDrukāt("[")
				console_2.MUnsignedinteger32Drukāt(sectheader.shaddress)
				console_2.MDrukāt(":")
				console_2.MUnsignedinteger32Drukāt(sectheader.shIzmērs)
				console_2.MDrukāt("]")
				for rt := uint32(0); rt < sectheader.shIzmērs/8; rt++ {
					offset := *(*uint32)(Pointer(&sectVērtība[rt*8]))
					pats.relTeksts[rt].offset = offset
					pats.relTeksts[rt].oaddress = *(*uint32)(Pointer(&pats.teksts[offset]))
					pats.relTeksts[rt].skaitlis = *(*uint32)(Pointer(&sectVērtība[rt*8+4]))
					pats.relTekstslen++
				}
			}
			if VienādsBaiti(sectNosaukums, ([]byte)(".dynstr")) {
				console_2.MDrukāt(".dynstr")
				console_2.MDrukāt("[")
				console_2.MUnsignedinteger32Drukāt(sectheader.shaddress)
				console_2.MDrukāt(":")
				console_2.MUnsignedinteger32Drukāt(sectheader.shIzmērs)
				console_2.MDrukāt("]")
			}
			if VienādsBaiti(sectNosaukums, ([]byte)(".strtab")) {
				console_2.MDrukāt(".strtab")
				console_2.MDrukāt("[")
				console_2.MUnsignedinteger32Drukāt(sectheader.shaddress)
				console_2.MDrukāt("]")
				rt := uint32(0)
				startēt := uint32(0)

				for st := uint32(1); st < sectheader.shIzmērs; st++ {
					if sectVērtība[st] == 0x0 || sectVērtība[st] == ' ' {
						funcNosaukums := sectVērtība[startēt+1 : st]
						console_2.MDrukāt("+")
						console_2.MDrukāt(funcNosaukums)
						pats.strtab[rt] = Baititovirkne(funcNosaukums)
						startēt = st
						rt++
					}
				}

			}

		}

		console_2.MDrukāt(([]byte)("<------------"))
		for rt := uint32(0); rt < pats.relTekstslen; rt++ {
			console_2.MDrukāt("[")
			console_2.MDrukāt(([]byte)(pats.strtab[rt]))
			console_2.MDrukāt(":")
			console_2.MUnsignedinteger32Drukāt(pats.relTeksts[rt].skaitlis)
			console_2.MDrukāt(":")

			console_2.MDrukāt(([]byte)("]"))
		}
		console_2.MDrukāt(([]byte)("------------>"))

		if tekstsKursors != nil {
			atmiņamanager.Brīvs(tekstsKursors)
		}

	}

}
