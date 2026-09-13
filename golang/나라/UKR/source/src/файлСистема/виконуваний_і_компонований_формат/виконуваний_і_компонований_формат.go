package виконуваний_і_компонований_формат

import . "unsafe"

import . "консоль"
import . "util"
import . "памятьmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eТип		uint16
	emachine	uint16
	eВерсія		uint32
	eзапис		uint32
	ephoff		uint32
	eshoff		uint32
	eПрапори	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shНазва		uint32
	shТип		uint32
	shПрапори	uint32
	shАдреса	uint32
	shoffset	uint32
	shРозмір	uint32
	shПосилання	uint32
	shІнфо		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfпрограмаheader struct {
	pТип		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pПрапори	uint32
	pВирівнювання	uint32
}
type Elf32Нотатка struct {
	nnamesz	uint32
	ndescsz	uint32
	nТип	uint32
}
type Elf32dyn struct {
	dМітка		uint32
	dvalВказівник	uint32
}
type Elf32rel struct {
	roffset	uint32
	rІнфо	uint32
}
type Elf32rela struct {
	roffset	uint32
	rІнфо	uint32
	raddend	uint32
}
type Elf32sym struct {
	stНазва		uint32
	stЗначення	uint32
	stРозмір	uint32
	stІнфо		uint8
	stІнше		uint8
	stshndx		uint16
}
type relocationТекст struct {
	offset	uint32
	число	uint32
	oАдреса	uint32
}
type Elf struct {
	текст		[]byte
	текстlen	uint32
	relТекст	[100]relocationТекст
	relТекстlen	uint32
	strtab		[100]string
	Got		uint32
	Динамічно	uint32
}

func (поточний *Elf) Getзапис(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.eзапис
}

func (поточний *Elf) Parse(data []byte, СторінкаТеказапис uint32) {

	памятьmanager := TПамятьmanager{}
	var текстВказівник Pointer = nil

	var консоль_2 = TКонсоль{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderРозмір := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderРозмір*i]))

			var sectНазва []byte
			запустити := uint32(strtab.shoffset + sectheader.shНазва)
			кінець := запустити
			for ; ; кінець++ {
				if data[кінець] == 0x0 || data[кінець] == ' ' {
					break
				}
			}
			sectНазва = data[запустити:кінець]

			var sectЗначення []byte
			if sectheader.shТип != 8 {
				кінецьoffset := sectheader.shoffset + sectheader.shРозмір
				if кінецьoffset < sectheader.shoffset || кінецьoffset > uint32(len(data)) {
					continue
				}
				sectЗначення = data[sectheader.shoffset:кінецьoffset]
			}

			if РівноБайт(sectНазва, ([]byte)(".got.plt")) {
				консоль_2.MДрук("[")
				консоль_2.MДрук(sectНазва)
				консоль_2.MДрук(":")
				поточний.Got = sectheader.shАдреса
				консоль_2.MUnsignedinteger32Друк(поточний.Got)
				консоль_2.MДрук("]")
			}
			if РівноБайт(sectНазва, ([]byte)(".dynamic")) {
				консоль_2.MДрук("[")
				консоль_2.MДрук(sectНазва)
				консоль_2.MДрук(":")
				динамічно := sectheader.shАдреса
				поточний.Динамічно = динамічно
				консоль_2.MUnsignedinteger32Друк(динамічно)
				консоль_2.MДрук("]")
			}

			if sectheader.shАдреса > 0x1000 {
				розмір := sectheader.shРозмір
				if sectheader.shТип == 8 {
					НульБлокВхіднийСторінкаТека(sectheader.shАдреса, розмір, СторінкаТеказапис)
				} else {
					призначення_2 := GetБайтзВказівник(uintptr(sectheader.shАдреса), int(розмір), int(розмір))
					МножинаБлокВхіднийСторінкаТека(sectЗначення, призначення_2, розмір, СторінкаТеказапис)
				}
			}

			continue

			if РівноБайт(sectНазва, ([]byte)(".text")) {
				консоль_2.MДрук(".text")
				консоль_2.MДрук("[")
				консоль_2.MUnsignedinteger32Друк(sectheader.shАдреса)
				консоль_2.MДрук(":")
				консоль_2.MUnsignedinteger32Друк(sectheader.shoffset)
				консоль_2.MДрук(":")
				консоль_2.MUnsignedinteger32Друк(sectheader.shРозмір)
				консоль_2.MДрук("]")
				copy(поточний.текст[:sectheader.shРозмір], sectЗначення[:sectheader.shРозмір])
				поточний.текстlen = sectheader.shРозмір
			}
			if РівноБайт(sectНазва, ([]byte)(".rel.text")) {
				консоль_2.MДрук(".rel.text")
				консоль_2.MДрук("[")
				консоль_2.MUnsignedinteger32Друк(sectheader.shАдреса)
				консоль_2.MДрук(":")
				консоль_2.MUnsignedinteger32Друк(sectheader.shРозмір)
				консоль_2.MДрук("]")
				for rt := uint32(0); rt < sectheader.shРозмір/8; rt++ {
					offset := *(*uint32)(Pointer(&sectЗначення[rt*8]))
					поточний.relТекст[rt].offset = offset
					поточний.relТекст[rt].oАдреса = *(*uint32)(Pointer(&поточний.текст[offset]))
					поточний.relТекст[rt].число = *(*uint32)(Pointer(&sectЗначення[rt*8+4]))
					поточний.relТекстlen++
				}
			}
			if РівноБайт(sectНазва, ([]byte)(".dynsym")) {
				консоль_2.MДрук(".dynsym")
				консоль_2.MДрук("[")
				консоль_2.MUnsignedinteger32Друк(sectheader.shАдреса)
				консоль_2.MДрук(":")
				консоль_2.MUnsignedinteger32Друк(sectheader.shРозмір)
				консоль_2.MДрук("]")
				for rt := uint32(0); rt < sectheader.shРозмір/8; rt++ {
					offset := *(*uint32)(Pointer(&sectЗначення[rt*8]))
					поточний.relТекст[rt].offset = offset
					поточний.relТекст[rt].oАдреса = *(*uint32)(Pointer(&поточний.текст[offset]))
					поточний.relТекст[rt].число = *(*uint32)(Pointer(&sectЗначення[rt*8+4]))
					поточний.relТекстlen++
				}
			}
			if РівноБайт(sectНазва, ([]byte)(".dynstr")) {
				консоль_2.MДрук(".dynstr")
				консоль_2.MДрук("[")
				консоль_2.MUnsignedinteger32Друк(sectheader.shАдреса)
				консоль_2.MДрук(":")
				консоль_2.MUnsignedinteger32Друк(sectheader.shРозмір)
				консоль_2.MДрук("]")
			}
			if РівноБайт(sectНазва, ([]byte)(".strtab")) {
				консоль_2.MДрук(".strtab")
				консоль_2.MДрук("[")
				консоль_2.MUnsignedinteger32Друк(sectheader.shАдреса)
				консоль_2.MДрук("]")
				rt := uint32(0)
				запустити := uint32(0)

				for st := uint32(1); st < sectheader.shРозмір; st++ {
					if sectЗначення[st] == 0x0 || sectЗначення[st] == ' ' {
						funcНазва := sectЗначення[запустити+1 : st]
						консоль_2.MДрук("+")
						консоль_2.MДрук(funcНазва)
						поточний.strtab[rt] = БайттоРядок(funcНазва)
						запустити = st
						rt++
					}
				}

			}

		}

		консоль_2.MДрук(([]byte)("<------------"))
		for rt := uint32(0); rt < поточний.relТекстlen; rt++ {
			консоль_2.MДрук("[")
			консоль_2.MДрук(([]byte)(поточний.strtab[rt]))
			консоль_2.MДрук(":")
			консоль_2.MUnsignedinteger32Друк(поточний.relТекст[rt].число)
			консоль_2.MДрук(":")

			консоль_2.MДрук(([]byte)("]"))
		}
		консоль_2.MДрук(([]byte)("------------>"))

		if текстВказівник != nil {
			памятьmanager.Вільно(текстВказівник)
		}

	}

}
