/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ausführbares_und_bindbares_Format

import . "unsafe"

import . "konsole"
import . "hilfswerkzeug"
import . "speicherVerwalter"
import . "seitenverwaltung"

type ElfKopf struct {
	eident		[16]byte
	eTyp		uint16
	emachine	uint16
	eversion	uint32
	eEintrag	uint32
	ephoff		uint32
	eshoff		uint32
	eOptionen	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type ElfAbschnittKopf struct {
	shElementname	uint32
	shTyp		uint32
	shOptionen	uint32
	shaddress	uint32
	shVersatz	uint32
	shGröße		uint32
	shVerknüpfung	uint32
	shinfo		uint32
	shaddralign	uint32
	shentsize	uint32
}
type ElfProgrammKopf struct {
	pTyp		uint32
	pVersatz	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pOptionen	uint32
	pAusrichtung	uint32
}
type Elf32Notiz struct {
	nnamesz	uint32
	ndescsz	uint32
	nTyp	uint32
}
type Elf32dyn struct {
	dAttribut	uint32
	dvalZeiger	uint32
}
type Elf32rel struct {
	rVersatz	uint32
	rinfo		uint32
}
type Elf32rela struct {
	rVersatz	uint32
	rinfo		uint32
	raddend		uint32
}
type Elf32sym struct {
	stElementname	uint32
	stWert		uint32
	stGröße		uint32
	stinfo		uint8
	stWeitere	uint8
	stshndx		uint16
}
type relocationText struct {
	versatz		uint32
	nummer		uint32
	oaddress	uint32
}
type Elf struct {
	text		[]byte
	textlen		uint32
	relText		[100]relocationText
	relTextlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamisch	uint32
}

func (selbst *Elf) GetEintrag(daten []byte) uint32 {
	elfKopf := (*ElfKopf)(Pointer(&daten[0]))
	return elfKopf.eEintrag
}

func (selbst *Elf) Parse(daten []byte, SeiteOrdnerEintrag uint32) {

	speicherVerwalter := TSpeicherVerwalter{}
	var textZeiger Pointer = nil

	var konsole_2 = TKonsole{}

	elfKopf := (*ElfKopf)(Pointer(&daten[0]))

	if elfKopf.eshnum != 0 {
		strtab := (*ElfAbschnittKopf)(Pointer(&daten[elfKopf.eshoff+uint32(elfKopf.eshentsize*elfKopf.eshstrndx)]))
		sectKopfGröße := uint32(Sizeof(ElfAbschnittKopf{}))

		for i := uint32(0); i < uint32(elfKopf.eshnum); i++ {
			sectKopf := (*ElfAbschnittKopf)(Pointer(&daten[elfKopf.eshoff+sectKopfGröße*i]))

			var sectElementname []byte
			starten := uint32(strtab.shVersatz + sectKopf.shElementname)
			ende := starten
			for ; ; ende++ {
				if daten[ende] == 0x0 || daten[ende] == ' ' {
					break
				}
			}
			sectElementname = daten[starten:ende]

			var sectWert []byte
			if sectKopf.shTyp != 8 {
				endeVersatz := sectKopf.shVersatz + sectKopf.shGröße
				if endeVersatz < sectKopf.shVersatz || endeVersatz > uint32(len(daten)) {
					continue
				}
				sectWert = daten[sectKopf.shVersatz:endeVersatz]
			}

			if EntsprechendByte(sectElementname, ([]byte)(".got.plt")) {
				konsole_2.MDrucken("[")
				konsole_2.MDrucken(sectElementname)
				konsole_2.MDrucken(":")
				selbst.Got = sectKopf.shaddress
				konsole_2.MUnsignedinteger32Drucken(selbst.Got)
				konsole_2.MDrucken("]")
			}
			if EntsprechendByte(sectElementname, ([]byte)(".dynamic")) {
				konsole_2.MDrucken("[")
				konsole_2.MDrucken(sectElementname)
				konsole_2.MDrucken(":")
				dynamisch := sectKopf.shaddress
				selbst.Dynamisch = dynamisch
				konsole_2.MUnsignedinteger32Drucken(dynamisch)
				konsole_2.MDrucken("]")
			}

			if sectKopf.shaddress > 0x1000 {
				größe := sectKopf.shGröße
				if sectKopf.shTyp == 8 {
					NullRechteckEinSeiteOrdner(sectKopf.shaddress, größe, SeiteOrdnerEintrag)
				} else {
					ziel_2 := GetBytevonZeiger(uintptr(sectKopf.shaddress), int(größe), int(größe))
					SetzenRechteckEinSeiteOrdner(sectWert, ziel_2, größe, SeiteOrdnerEintrag)
				}
			}

			continue

			if EntsprechendByte(sectElementname, ([]byte)(".text")) {
				konsole_2.MDrucken(".text")
				konsole_2.MDrucken("[")
				konsole_2.MUnsignedinteger32Drucken(sectKopf.shaddress)
				konsole_2.MDrucken(":")
				konsole_2.MUnsignedinteger32Drucken(sectKopf.shVersatz)
				konsole_2.MDrucken(":")
				konsole_2.MUnsignedinteger32Drucken(sectKopf.shGröße)
				konsole_2.MDrucken("]")
				copy(selbst.text[:sectKopf.shGröße], sectWert[:sectKopf.shGröße])
				selbst.textlen = sectKopf.shGröße
			}
			if EntsprechendByte(sectElementname, ([]byte)(".rel.text")) {
				konsole_2.MDrucken(".rel.text")
				konsole_2.MDrucken("[")
				konsole_2.MUnsignedinteger32Drucken(sectKopf.shaddress)
				konsole_2.MDrucken(":")
				konsole_2.MUnsignedinteger32Drucken(sectKopf.shGröße)
				konsole_2.MDrucken("]")
				for rt := uint32(0); rt < sectKopf.shGröße/8; rt++ {
					versatz := *(*uint32)(Pointer(&sectWert[rt*8]))
					selbst.relText[rt].versatz = versatz
					selbst.relText[rt].oaddress = *(*uint32)(Pointer(&selbst.text[versatz]))
					selbst.relText[rt].nummer = *(*uint32)(Pointer(&sectWert[rt*8+4]))
					selbst.relTextlen++
				}
			}
			if EntsprechendByte(sectElementname, ([]byte)(".dynsym")) {
				konsole_2.MDrucken(".dynsym")
				konsole_2.MDrucken("[")
				konsole_2.MUnsignedinteger32Drucken(sectKopf.shaddress)
				konsole_2.MDrucken(":")
				konsole_2.MUnsignedinteger32Drucken(sectKopf.shGröße)
				konsole_2.MDrucken("]")
				for rt := uint32(0); rt < sectKopf.shGröße/8; rt++ {
					versatz := *(*uint32)(Pointer(&sectWert[rt*8]))
					selbst.relText[rt].versatz = versatz
					selbst.relText[rt].oaddress = *(*uint32)(Pointer(&selbst.text[versatz]))
					selbst.relText[rt].nummer = *(*uint32)(Pointer(&sectWert[rt*8+4]))
					selbst.relTextlen++
				}
			}
			if EntsprechendByte(sectElementname, ([]byte)(".dynstr")) {
				konsole_2.MDrucken(".dynstr")
				konsole_2.MDrucken("[")
				konsole_2.MUnsignedinteger32Drucken(sectKopf.shaddress)
				konsole_2.MDrucken(":")
				konsole_2.MUnsignedinteger32Drucken(sectKopf.shGröße)
				konsole_2.MDrucken("]")
			}
			if EntsprechendByte(sectElementname, ([]byte)(".strtab")) {
				konsole_2.MDrucken(".strtab")
				konsole_2.MDrucken("[")
				konsole_2.MUnsignedinteger32Drucken(sectKopf.shaddress)
				konsole_2.MDrucken("]")
				rt := uint32(0)
				starten := uint32(0)

				for st := uint32(1); st < sectKopf.shGröße; st++ {
					if sectWert[st] == 0x0 || sectWert[st] == ' ' {
						funcElementname := sectWert[starten+1 : st]
						konsole_2.MDrucken("+")
						konsole_2.MDrucken(funcElementname)
						selbst.strtab[rt] = BytetoZeichenkette(funcElementname)
						starten = st
						rt++
					}
				}

			}

		}

		konsole_2.MDrucken(([]byte)("<------------"))
		for rt := uint32(0); rt < selbst.relTextlen; rt++ {
			konsole_2.MDrucken("[")
			konsole_2.MDrucken(([]byte)(selbst.strtab[rt]))
			konsole_2.MDrucken(":")
			konsole_2.MUnsignedinteger32Drucken(selbst.relText[rt].nummer)
			konsole_2.MDrucken(":")

			konsole_2.MDrucken(([]byte)("]"))
		}
		konsole_2.MDrucken(([]byte)("------------>"))

		if textZeiger != nil {
			speicherVerwalter.Frei(textZeiger)
		}

	}

}
