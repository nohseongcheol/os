package исполняемый_и_компонуемый_формат

import . "unsafe"

import . "консоль"
import . "утилита"
import . "памятьдиспетчер"
import . "управлениеСтраницами"

type Elfзаголовок struct {
	eident		[16]byte
	eтип		uint16
	emachine	uint16
	eВерсия		uint32
	eзапись		uint32
	ephoff		uint32
	eshoff		uint32
	eФлаги		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfразделзаголовок struct {
	shИмя		uint32
	shтип		uint32
	shФлаги		uint32
	shaddress	uint32
	shoffset	uint32
	shРазмер	uint32
	shссылка	uint32
	shИнформация	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfпрограммазаголовок struct {
	pтип		uint32
	poffset		uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pФлаги		uint32
	pВыравнивание	uint32
}
type Elf32Заметка struct {
	nnamesz	uint32
	ndescsz	uint32
	nтип	uint32
}
type Elf32dyn struct {
	dМетка		uint32
	dvalУказатели	uint32
}
type Elf32rel struct {
	roffset		uint32
	rИнформация	uint32
}
type Elf32rela struct {
	roffset		uint32
	rИнформация	uint32
	raddend		uint32
}
type Elf32sym struct {
	stИмя		uint32
	stЗначение	uint32
	stРазмер	uint32
	stИнформация	uint8
	stДругая	uint8
	stshndx		uint16
}
type relocationтекст struct {
	offset		uint32
	число		uint32
	oaddress	uint32
}
type Elf struct {
	текст		[]byte
	текстlen	uint32
	relтекст	[100]relocationтекст
	relтекстlen	uint32
	strtab		[100]string
	Got		uint32
	Динамически	uint32
}

func (текущий *Elf) Getзапись(данные []byte) uint32 {
	elfзаголовок := (*Elfзаголовок)(Pointer(&данные[0]))
	return elfзаголовок.eзапись
}

func (текущий *Elf) Parse(данные []byte, Страницакаталогзапись uint32) {

	памятьдиспетчер := TПамятьдиспетчер{}
	var текстУказатели Pointer = nil

	var консоль_2 = TКонсоль{}

	elfзаголовок := (*Elfзаголовок)(Pointer(&данные[0]))

	if elfзаголовок.eshnum != 0 {
		strtab := (*Elfразделзаголовок)(Pointer(&данные[elfзаголовок.eshoff+uint32(elfзаголовок.eshentsize*elfзаголовок.eshstrndx)]))
		sectзаголовокРазмер := uint32(Sizeof(Elfразделзаголовок{}))

		for i := uint32(0); i < uint32(elfзаголовок.eshnum); i++ {
			sectзаголовок := (*Elfразделзаголовок)(Pointer(&данные[elfзаголовок.eshoff+sectзаголовокРазмер*i]))

			var sectИмя []byte
			пуск := uint32(strtab.shoffset + sectзаголовок.shИмя)
			конце := пуск
			for ; ; конце++ {
				if данные[конце] == 0x0 || данные[конце] == ' ' {
					break
				}
			}
			sectИмя = данные[пуск:конце]

			var sectЗначение []byte
			if sectзаголовок.shтип != 8 {
				концеoffset := sectзаголовок.shoffset + sectзаголовок.shРазмер
				if концеoffset < sectзаголовок.shoffset || концеoffset > uint32(len(данные)) {
					continue
				}
				sectЗначение = данные[sectзаголовок.shoffset:концеoffset]
			}

			if РавныйБайт(sectИмя, ([]byte)(".got.plt")) {
				консоль_2.MПечать("[")
				консоль_2.MПечать(sectИмя)
				консоль_2.MПечать(":")
				текущий.Got = sectзаголовок.shaddress
				консоль_2.MUnsignedinteger32Печать(текущий.Got)
				консоль_2.MПечать("]")
			}
			if РавныйБайт(sectИмя, ([]byte)(".dynamic")) {
				консоль_2.MПечать("[")
				консоль_2.MПечать(sectИмя)
				консоль_2.MПечать(":")
				динамически := sectзаголовок.shaddress
				текущий.Динамически = динамически
				консоль_2.MUnsignedinteger32Печать(динамически)
				консоль_2.MПечать("]")
			}

			if sectзаголовок.shaddress > 0x1000 {
				размер := sectзаголовок.shРазмер
				if sectзаголовок.shтип == 8 {
					НольБлокИсходящийстраницакаталог(sectзаголовок.shaddress, размер, Страницакаталогзапись)
				} else {
					назначение_2 := GetБайтfromУказатели(uintptr(sectзаголовок.shaddress), int(размер), int(размер))
					УказатьБлокИсходящийстраницакаталог(sectЗначение, назначение_2, размер, Страницакаталогзапись)
				}
			}

			continue

			if РавныйБайт(sectИмя, ([]byte)(".text")) {
				консоль_2.MПечать(".text")
				консоль_2.MПечать("[")
				консоль_2.MUnsignedinteger32Печать(sectзаголовок.shaddress)
				консоль_2.MПечать(":")
				консоль_2.MUnsignedinteger32Печать(sectзаголовок.shoffset)
				консоль_2.MПечать(":")
				консоль_2.MUnsignedinteger32Печать(sectзаголовок.shРазмер)
				консоль_2.MПечать("]")
				copy(текущий.текст[:sectзаголовок.shРазмер], sectЗначение[:sectзаголовок.shРазмер])
				текущий.текстlen = sectзаголовок.shРазмер
			}
			if РавныйБайт(sectИмя, ([]byte)(".rel.text")) {
				консоль_2.MПечать(".rel.text")
				консоль_2.MПечать("[")
				консоль_2.MUnsignedinteger32Печать(sectзаголовок.shaddress)
				консоль_2.MПечать(":")
				консоль_2.MUnsignedinteger32Печать(sectзаголовок.shРазмер)
				консоль_2.MПечать("]")
				for rt := uint32(0); rt < sectзаголовок.shРазмер/8; rt++ {
					offset := *(*uint32)(Pointer(&sectЗначение[rt*8]))
					текущий.relтекст[rt].offset = offset
					текущий.relтекст[rt].oaddress = *(*uint32)(Pointer(&текущий.текст[offset]))
					текущий.relтекст[rt].число = *(*uint32)(Pointer(&sectЗначение[rt*8+4]))
					текущий.relтекстlen++
				}
			}
			if РавныйБайт(sectИмя, ([]byte)(".dynsym")) {
				консоль_2.MПечать(".dynsym")
				консоль_2.MПечать("[")
				консоль_2.MUnsignedinteger32Печать(sectзаголовок.shaddress)
				консоль_2.MПечать(":")
				консоль_2.MUnsignedinteger32Печать(sectзаголовок.shРазмер)
				консоль_2.MПечать("]")
				for rt := uint32(0); rt < sectзаголовок.shРазмер/8; rt++ {
					offset := *(*uint32)(Pointer(&sectЗначение[rt*8]))
					текущий.relтекст[rt].offset = offset
					текущий.relтекст[rt].oaddress = *(*uint32)(Pointer(&текущий.текст[offset]))
					текущий.relтекст[rt].число = *(*uint32)(Pointer(&sectЗначение[rt*8+4]))
					текущий.relтекстlen++
				}
			}
			if РавныйБайт(sectИмя, ([]byte)(".dynstr")) {
				консоль_2.MПечать(".dynstr")
				консоль_2.MПечать("[")
				консоль_2.MUnsignedinteger32Печать(sectзаголовок.shaddress)
				консоль_2.MПечать(":")
				консоль_2.MUnsignedinteger32Печать(sectзаголовок.shРазмер)
				консоль_2.MПечать("]")
			}
			if РавныйБайт(sectИмя, ([]byte)(".strtab")) {
				консоль_2.MПечать(".strtab")
				консоль_2.MПечать("[")
				консоль_2.MUnsignedinteger32Печать(sectзаголовок.shaddress)
				консоль_2.MПечать("]")
				rt := uint32(0)
				пуск := uint32(0)

				for st := uint32(1); st < sectзаголовок.shРазмер; st++ {
					if sectЗначение[st] == 0x0 || sectЗначение[st] == ' ' {
						funcИмя := sectЗначение[пуск+1 : st]
						консоль_2.MПечать("+")
						консоль_2.MПечать(funcИмя)
						текущий.strtab[rt] = БайткСтрока(funcИмя)
						пуск = st
						rt++
					}
				}

			}

		}

		консоль_2.MПечать(([]byte)("<------------"))
		for rt := uint32(0); rt < текущий.relтекстlen; rt++ {
			консоль_2.MПечать("[")
			консоль_2.MПечать(([]byte)(текущий.strtab[rt]))
			консоль_2.MПечать(":")
			консоль_2.MUnsignedinteger32Печать(текущий.relтекст[rt].число)
			консоль_2.MПечать(":")

			консоль_2.MПечать(([]byte)("]"))
		}
		консоль_2.MПечать(([]byte)("------------>"))

		if текстУказатели != nil {
			памятьдиспетчер.Свободно(текстУказатели)
		}

	}

}
