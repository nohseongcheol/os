package صيغة_التنفيذ_والربط

import . "unsafe"

import . "طرفية"
import . "أداة"
import . "ذاكرةمدير"
import . "إدارةصفحات"

type Elfترويسة struct {
	eident		[16]byte
	eنوع		uint16
	emachine	uint16
	eإصدار		uint32
	eentry		uint32
	ephoff		uint32
	eshoff		uint32
	eخيارات		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfقسمترويسة struct {
	shالاسم		uint32
	shنوع		uint32
	shخيارات	uint32
	shaddress	uint32
	shoffset	uint32
	shالحجم		uint32
	shرابط		uint32
	shمعلومات	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfبرنامجترويسة struct {
	pنوع	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pخيارات	uint32
	palign	uint32
}
type Elf32ملاحظة struct {
	nnamesz	uint32
	ndescsz	uint32
	nنوع	uint32
}
type Elf32dyn struct {
	dالوسم		uint32
	dvalالمؤشر	uint32
}
type Elf32rel struct {
	roffset		uint32
	rمعلومات	uint32
}
type Elf32rela struct {
	roffset		uint32
	rمعلومات	uint32
	raddend		uint32
}
type Elf32sym struct {
	stالاسم		uint32
	stالقيمة	uint32
	stالحجم		uint32
	stمعلومات	uint8
	stأخرى		uint8
	stshndx		uint16
}
type relocationنص struct {
	offset		uint32
	الأرقام		uint32
	oaddress	uint32
}
type Elf struct {
	نص		[]byte
	نصlen		uint32
	relنص		[100]relocationنص
	relنصlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamic		uint32
}

func (نفسه *Elf) Getentry(بيانات []byte) uint32 {
	elfترويسة := (*Elfترويسة)(Pointer(&بيانات[0]))
	return elfترويسة.eentry
}

func (نفسه *Elf) Parse(بيانات []byte, Pصفحةدليلentry uint32) {

	ذاكرةمدير := Tذاكرةمدير{}
	var نصالمؤشر Pointer = nil

	var طرفية_2 = Tطرفية{}

	elfترويسة := (*Elfترويسة)(Pointer(&بيانات[0]))

	if elfترويسة.eshnum != 0 {
		strtab := (*Elfقسمترويسة)(Pointer(&بيانات[elfترويسة.eshoff+uint32(elfترويسة.eshentsize*elfترويسة.eshstrndx)]))
		sectترويسةالحجم := uint32(Sizeof(Elfقسمترويسة{}))

		for i := uint32(0); i < uint32(elfترويسة.eshnum); i++ {
			sectترويسة := (*Elfقسمترويسة)(Pointer(&بيانات[elfترويسة.eshoff+sectترويسةالحجم*i]))

			var sectالاسم []byte
			ابدأ := uint32(strtab.shoffset + sectترويسة.shالاسم)
			نهاية := ابدأ
			for ; ; نهاية++ {
				if بيانات[نهاية] == 0x0 || بيانات[نهاية] == ' ' {
					break
				}
			}
			sectالاسم = بيانات[ابدأ:نهاية]

			var sectالقيمة []byte
			if sectترويسة.shنوع != 8 {
				نهايةoffset := sectترويسة.shoffset + sectترويسة.shالحجم
				if نهايةoffset < sectترويسة.shoffset || نهايةoffset > uint32(len(بيانات)) {
					continue
				}
				sectالقيمة = بيانات[sectترويسة.shoffset:نهايةoffset]
			}

			if Eمساويبايت(sectالاسم, ([]byte)(".got.plt")) {
				طرفية_2.Mاطبع("[")
				طرفية_2.Mاطبع(sectالاسم)
				طرفية_2.Mاطبع(":")
				نفسه.Got = sectترويسة.shaddress
				طرفية_2.MUnsignedinteger32اطبع(نفسه.Got)
				طرفية_2.Mاطبع("]")
			}
			if Eمساويبايت(sectالاسم, ([]byte)(".dynamic")) {
				طرفية_2.Mاطبع("[")
				طرفية_2.Mاطبع(sectالاسم)
				طرفية_2.Mاطبع(":")
				dynamic := sectترويسة.shaddress
				نفسه.Dynamic = dynamic
				طرفية_2.MUnsignedinteger32اطبع(dynamic)
				طرفية_2.Mاطبع("]")
			}

			if sectترويسة.shaddress > 0x1000 {
				الحجم := sectترويسة.shالحجم
				if sectترويسة.shنوع == 8 {
					Zeroحظرداخلصفحةدليل(sectترويسة.shaddress, الحجم, Pصفحةدليلentry)
				} else {
					المقصد_2 := Getبايتfromالمؤشر(uintptr(sectترويسة.shaddress), int(الحجم), int(الحجم))
					Sتحديدحظرداخلصفحةدليل(sectالقيمة, المقصد_2, الحجم, Pصفحةدليلentry)
				}
			}

			continue

			if Eمساويبايت(sectالاسم, ([]byte)(".text")) {
				طرفية_2.Mاطبع(".text")
				طرفية_2.Mاطبع("[")
				طرفية_2.MUnsignedinteger32اطبع(sectترويسة.shaddress)
				طرفية_2.Mاطبع(":")
				طرفية_2.MUnsignedinteger32اطبع(sectترويسة.shoffset)
				طرفية_2.Mاطبع(":")
				طرفية_2.MUnsignedinteger32اطبع(sectترويسة.shالحجم)
				طرفية_2.Mاطبع("]")
				copy(نفسه.نص[:sectترويسة.shالحجم], sectالقيمة[:sectترويسة.shالحجم])
				نفسه.نصlen = sectترويسة.shالحجم
			}
			if Eمساويبايت(sectالاسم, ([]byte)(".rel.text")) {
				طرفية_2.Mاطبع(".rel.text")
				طرفية_2.Mاطبع("[")
				طرفية_2.MUnsignedinteger32اطبع(sectترويسة.shaddress)
				طرفية_2.Mاطبع(":")
				طرفية_2.MUnsignedinteger32اطبع(sectترويسة.shالحجم)
				طرفية_2.Mاطبع("]")
				for rt := uint32(0); rt < sectترويسة.shالحجم/8; rt++ {
					offset := *(*uint32)(Pointer(&sectالقيمة[rt*8]))
					نفسه.relنص[rt].offset = offset
					نفسه.relنص[rt].oaddress = *(*uint32)(Pointer(&نفسه.نص[offset]))
					نفسه.relنص[rt].الأرقام = *(*uint32)(Pointer(&sectالقيمة[rt*8+4]))
					نفسه.relنصlen++
				}
			}
			if Eمساويبايت(sectالاسم, ([]byte)(".dynsym")) {
				طرفية_2.Mاطبع(".dynsym")
				طرفية_2.Mاطبع("[")
				طرفية_2.MUnsignedinteger32اطبع(sectترويسة.shaddress)
				طرفية_2.Mاطبع(":")
				طرفية_2.MUnsignedinteger32اطبع(sectترويسة.shالحجم)
				طرفية_2.Mاطبع("]")
				for rt := uint32(0); rt < sectترويسة.shالحجم/8; rt++ {
					offset := *(*uint32)(Pointer(&sectالقيمة[rt*8]))
					نفسه.relنص[rt].offset = offset
					نفسه.relنص[rt].oaddress = *(*uint32)(Pointer(&نفسه.نص[offset]))
					نفسه.relنص[rt].الأرقام = *(*uint32)(Pointer(&sectالقيمة[rt*8+4]))
					نفسه.relنصlen++
				}
			}
			if Eمساويبايت(sectالاسم, ([]byte)(".dynstr")) {
				طرفية_2.Mاطبع(".dynstr")
				طرفية_2.Mاطبع("[")
				طرفية_2.MUnsignedinteger32اطبع(sectترويسة.shaddress)
				طرفية_2.Mاطبع(":")
				طرفية_2.MUnsignedinteger32اطبع(sectترويسة.shالحجم)
				طرفية_2.Mاطبع("]")
			}
			if Eمساويبايت(sectالاسم, ([]byte)(".strtab")) {
				طرفية_2.Mاطبع(".strtab")
				طرفية_2.Mاطبع("[")
				طرفية_2.MUnsignedinteger32اطبع(sectترويسة.shaddress)
				طرفية_2.Mاطبع("]")
				rt := uint32(0)
				ابدأ := uint32(0)

				for st := uint32(1); st < sectترويسة.shالحجم; st++ {
					if sectالقيمة[st] == 0x0 || sectالقيمة[st] == ' ' {
						funcالاسم := sectالقيمة[ابدأ+1 : st]
						طرفية_2.Mاطبع("+")
						طرفية_2.Mاطبع(funcالاسم)
						نفسه.strtab[rt] = Bبايتtoسلسلة(funcالاسم)
						ابدأ = st
						rt++
					}
				}

			}

		}

		طرفية_2.Mاطبع(([]byte)("<------------"))
		for rt := uint32(0); rt < نفسه.relنصlen; rt++ {
			طرفية_2.Mاطبع("[")
			طرفية_2.Mاطبع(([]byte)(نفسه.strtab[rt]))
			طرفية_2.Mاطبع(":")
			طرفية_2.MUnsignedinteger32اطبع(نفسه.relنص[rt].الأرقام)
			طرفية_2.Mاطبع(":")

			طرفية_2.Mاطبع(([]byte)("]"))
		}
		طرفية_2.Mاطبع(([]byte)("------------>"))

		if نصالمؤشر != nil {
			ذاكرةمدير.Fخالي(نصالمؤشر)
		}

	}

}
