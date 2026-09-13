package çalıştırılabilir_ve_bağlanabilir_biçim

import . "unsafe"

import . "konsol"
import . "util"
import . "bellekmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTür		uint16
	emachine	uint16
	eSürüm		uint32
	egirdi		uint32
	ephoff		uint32
	eshoff		uint32
	eİmler		uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shİsim		uint32
	shTür		uint32
	shİmler		uint32
	shaddress	uint32
	shoffset	uint32
	shBoyut		uint32
	shBağ		uint32
	shBilgi		uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfuygulamaheader struct {
	pTür	uint32
	poffset	uint32
	pvaddr	uint32
	ppaddr	uint32
	pfilesz	uint32
	pmemsz	uint32
	pİmler	uint32
	pHizala	uint32
}
type Elf32Not struct {
	nnamesz	uint32
	ndescsz	uint32
	nTür	uint32
}
type Elf32dyn struct {
	dEtiket		uint32
	dvalBelirteç	uint32
}
type Elf32rel struct {
	roffset	uint32
	rBilgi	uint32
}
type Elf32rela struct {
	roffset	uint32
	rBilgi	uint32
	raddend	uint32
}
type Elf32sym struct {
	stİsim	uint32
	stDeğer	uint32
	stBoyut	uint32
	stBilgi	uint8
	stDiğer	uint8
	stshndx	uint16
}
type relocationMetin struct {
	offset		uint32
	sayı		uint32
	oaddress	uint32
}
type Elf struct {
	metin		[]byte
	metinlen	uint32
	relMetin	[100]relocationMetin
	relMetinlen	uint32
	strtab		[100]string
	Got		uint32
	Devingen	uint32
}

func (self *Elf) Getgirdi(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.egirdi
}

func (self *Elf) Parse(data []byte, SayfaDizingirdi uint32) {

	bellekmanager := TBellekmanager{}
	var metinBelirteç Pointer = nil

	var konsol_2 = TKonsol{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderBoyut := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderBoyut*i]))

			var sectİsim []byte
			başlat := uint32(strtab.shoffset + sectheader.shİsim)
			son := başlat
			for ; ; son++ {
				if data[son] == 0x0 || data[son] == ' ' {
					break
				}
			}
			sectİsim = data[başlat:son]

			var sectDeğer []byte
			if sectheader.shTür != 8 {
				sonoffset := sectheader.shoffset + sectheader.shBoyut
				if sonoffset < sectheader.shoffset || sonoffset > uint32(len(data)) {
					continue
				}
				sectDeğer = data[sectheader.shoffset:sonoffset]
			}

			if EşitBayt(sectİsim, ([]byte)(".got.plt")) {
				konsol_2.MYazdır("[")
				konsol_2.MYazdır(sectİsim)
				konsol_2.MYazdır(":")
				self.Got = sectheader.shaddress
				konsol_2.MUnsignedinteger32Yazdır(self.Got)
				konsol_2.MYazdır("]")
			}
			if EşitBayt(sectİsim, ([]byte)(".dynamic")) {
				konsol_2.MYazdır("[")
				konsol_2.MYazdır(sectİsim)
				konsol_2.MYazdır(":")
				devingen := sectheader.shaddress
				self.Devingen = devingen
				konsol_2.MUnsignedinteger32Yazdır(devingen)
				konsol_2.MYazdır("]")
			}

			if sectheader.shaddress > 0x1000 {
				boyut := sectheader.shBoyut
				if sectheader.shTür == 8 {
					SıfırBlokGelenSayfaDizin(sectheader.shaddress, boyut, SayfaDizingirdi)
				} else {
					hedef_2 := GetBaytfromBelirteç(uintptr(sectheader.shaddress), int(boyut), int(boyut))
					AyarlaBlokGelenSayfaDizin(sectDeğer, hedef_2, boyut, SayfaDizingirdi)
				}
			}

			continue

			if EşitBayt(sectİsim, ([]byte)(".text")) {
				konsol_2.MYazdır(".text")
				konsol_2.MYazdır("[")
				konsol_2.MUnsignedinteger32Yazdır(sectheader.shaddress)
				konsol_2.MYazdır(":")
				konsol_2.MUnsignedinteger32Yazdır(sectheader.shoffset)
				konsol_2.MYazdır(":")
				konsol_2.MUnsignedinteger32Yazdır(sectheader.shBoyut)
				konsol_2.MYazdır("]")
				copy(self.metin[:sectheader.shBoyut], sectDeğer[:sectheader.shBoyut])
				self.metinlen = sectheader.shBoyut
			}
			if EşitBayt(sectİsim, ([]byte)(".rel.text")) {
				konsol_2.MYazdır(".rel.text")
				konsol_2.MYazdır("[")
				konsol_2.MUnsignedinteger32Yazdır(sectheader.shaddress)
				konsol_2.MYazdır(":")
				konsol_2.MUnsignedinteger32Yazdır(sectheader.shBoyut)
				konsol_2.MYazdır("]")
				for rt := uint32(0); rt < sectheader.shBoyut/8; rt++ {
					offset := *(*uint32)(Pointer(&sectDeğer[rt*8]))
					self.relMetin[rt].offset = offset
					self.relMetin[rt].oaddress = *(*uint32)(Pointer(&self.metin[offset]))
					self.relMetin[rt].sayı = *(*uint32)(Pointer(&sectDeğer[rt*8+4]))
					self.relMetinlen++
				}
			}
			if EşitBayt(sectİsim, ([]byte)(".dynsym")) {
				konsol_2.MYazdır(".dynsym")
				konsol_2.MYazdır("[")
				konsol_2.MUnsignedinteger32Yazdır(sectheader.shaddress)
				konsol_2.MYazdır(":")
				konsol_2.MUnsignedinteger32Yazdır(sectheader.shBoyut)
				konsol_2.MYazdır("]")
				for rt := uint32(0); rt < sectheader.shBoyut/8; rt++ {
					offset := *(*uint32)(Pointer(&sectDeğer[rt*8]))
					self.relMetin[rt].offset = offset
					self.relMetin[rt].oaddress = *(*uint32)(Pointer(&self.metin[offset]))
					self.relMetin[rt].sayı = *(*uint32)(Pointer(&sectDeğer[rt*8+4]))
					self.relMetinlen++
				}
			}
			if EşitBayt(sectİsim, ([]byte)(".dynstr")) {
				konsol_2.MYazdır(".dynstr")
				konsol_2.MYazdır("[")
				konsol_2.MUnsignedinteger32Yazdır(sectheader.shaddress)
				konsol_2.MYazdır(":")
				konsol_2.MUnsignedinteger32Yazdır(sectheader.shBoyut)
				konsol_2.MYazdır("]")
			}
			if EşitBayt(sectİsim, ([]byte)(".strtab")) {
				konsol_2.MYazdır(".strtab")
				konsol_2.MYazdır("[")
				konsol_2.MUnsignedinteger32Yazdır(sectheader.shaddress)
				konsol_2.MYazdır("]")
				rt := uint32(0)
				başlat := uint32(0)

				for st := uint32(1); st < sectheader.shBoyut; st++ {
					if sectDeğer[st] == 0x0 || sectDeğer[st] == ' ' {
						funcİsim := sectDeğer[başlat+1 : st]
						konsol_2.MYazdır("+")
						konsol_2.MYazdır(funcİsim)
						self.strtab[rt] = BayttoKatar(funcİsim)
						başlat = st
						rt++
					}
				}

			}

		}

		konsol_2.MYazdır(([]byte)("<------------"))
		for rt := uint32(0); rt < self.relMetinlen; rt++ {
			konsol_2.MYazdır("[")
			konsol_2.MYazdır(([]byte)(self.strtab[rt]))
			konsol_2.MYazdır(":")
			konsol_2.MUnsignedinteger32Yazdır(self.relMetin[rt].sayı)
			konsol_2.MYazdır(":")

			konsol_2.MYazdır(([]byte)("]"))
		}
		konsol_2.MYazdır(([]byte)("------------>"))

		if metinBelirteç != nil {
			bellekmanager.Boş(metinBelirteç)
		}

	}

}
