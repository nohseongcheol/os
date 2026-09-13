package format_wykonywalny_i_konsolidowalny

import . "unsafe"

import . "konsola"
import . "util"
import . "pamięćmanager"
import . "paging"

type Elfheader struct {
	eident		[16]byte
	eTyp		uint16
	emachine	uint16
	eWersja		uint32
	ewpis		uint32
	ephoff		uint32
	eshoff		uint32
	eZnaczniki	uint32
	eehsize		uint16
	ephentsize	uint16
	ephnum		uint16
	eshentsize	uint16
	eshnum		uint16
	eshstrndx	uint16
}
type Elfsectionheader struct {
	shNazwa		uint32
	shTyp		uint32
	shZnaczniki	uint32
	shAdres		uint32
	shPrzesunięcie	uint32
	shRozmiar	uint32
	shOdnośnik	uint32
	shInformacja	uint32
	shaddralign	uint32
	shentsize	uint32
}
type Elfprogramheader struct {
	pTyp		uint32
	pPrzesunięcie	uint32
	pvaddr		uint32
	ppaddr		uint32
	pfilesz		uint32
	pmemsz		uint32
	pZnaczniki	uint32
	pWyrównanie	uint32
}
type Elf32Uwaga struct {
	nnamesz	uint32
	ndescsz	uint32
	nTyp	uint32
}
type Elf32dyn struct {
	dZnacznik	uint32
	dvalKursor	uint32
}
type Elf32rel struct {
	rPrzesunięcie	uint32
	rInformacja	uint32
}
type Elf32rela struct {
	rPrzesunięcie	uint32
	rInformacja	uint32
	raddend		uint32
}
type Elf32sym struct {
	stNazwa		uint32
	stWartość	uint32
	stRozmiar	uint32
	stInformacja	uint8
	stInne		uint8
	stshndx		uint16
}
type relocationTekst struct {
	przesunięcie	uint32
	liczba_2	uint32
	oAdres		uint32
}
type Elf struct {
	tekst		[]byte
	tekstlen	uint32
	relTekst	[100]relocationTekst
	relTekstlen	uint32
	strtab		[100]string
	Got		uint32
	Dynamicznie	uint32
}

func (bieżący *Elf) Getwpis(data []byte) uint32 {
	elfheader := (*Elfheader)(Pointer(&data[0]))
	return elfheader.ewpis
}

func (bieżący *Elf) Parse(data []byte, StronaKatalogwpis uint32) {

	pamięćmanager := TPamięćmanager{}
	var tekstKursor Pointer = nil

	var konsola_2 = TKonsola{}

	elfheader := (*Elfheader)(Pointer(&data[0]))

	if elfheader.eshnum != 0 {
		strtab := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+uint32(elfheader.eshentsize*elfheader.eshstrndx)]))
		sectheaderRozmiar := uint32(Sizeof(Elfsectionheader{}))

		for i := uint32(0); i < uint32(elfheader.eshnum); i++ {
			sectheader := (*Elfsectionheader)(Pointer(&data[elfheader.eshoff+sectheaderRozmiar*i]))

			var sectNazwa []byte
			uruchom := uint32(strtab.shPrzesunięcie + sectheader.shNazwa)
			koniec := uruchom
			for ; ; koniec++ {
				if data[koniec] == 0x0 || data[koniec] == ' ' {
					break
				}
			}
			sectNazwa = data[uruchom:koniec]

			var sectWartość []byte
			if sectheader.shTyp != 8 {
				koniecPrzesunięcie := sectheader.shPrzesunięcie + sectheader.shRozmiar
				if koniecPrzesunięcie < sectheader.shPrzesunięcie || koniecPrzesunięcie > uint32(len(data)) {
					continue
				}
				sectWartość = data[sectheader.shPrzesunięcie:koniecPrzesunięcie]
			}

			if OdpowiedniBajty(sectNazwa, ([]byte)(".got.plt")) {
				konsola_2.MWydrukuj("[")
				konsola_2.MWydrukuj(sectNazwa)
				konsola_2.MWydrukuj(":")
				bieżący.Got = sectheader.shAdres
				konsola_2.MUnsignedinteger32Wydrukuj(bieżący.Got)
				konsola_2.MWydrukuj("]")
			}
			if OdpowiedniBajty(sectNazwa, ([]byte)(".dynamic")) {
				konsola_2.MWydrukuj("[")
				konsola_2.MWydrukuj(sectNazwa)
				konsola_2.MWydrukuj(":")
				dynamicznie := sectheader.shAdres
				bieżący.Dynamicznie = dynamicznie
				konsola_2.MUnsignedinteger32Wydrukuj(dynamicznie)
				konsola_2.MWydrukuj("]")
			}

			if sectheader.shAdres > 0x1000 {
				rozmiar := sectheader.shRozmiar
				if sectheader.shTyp == 8 {
					ZeroBlokWchodzącyStronaKatalog(sectheader.shAdres, rozmiar, StronaKatalogwpis)
				} else {
					cel_2 := GetBajtyzKursor(uintptr(sectheader.shAdres), int(rozmiar), int(rozmiar))
					ZbiórBlokWchodzącyStronaKatalog(sectWartość, cel_2, rozmiar, StronaKatalogwpis)
				}
			}

			continue

			if OdpowiedniBajty(sectNazwa, ([]byte)(".text")) {
				konsola_2.MWydrukuj(".text")
				konsola_2.MWydrukuj("[")
				konsola_2.MUnsignedinteger32Wydrukuj(sectheader.shAdres)
				konsola_2.MWydrukuj(":")
				konsola_2.MUnsignedinteger32Wydrukuj(sectheader.shPrzesunięcie)
				konsola_2.MWydrukuj(":")
				konsola_2.MUnsignedinteger32Wydrukuj(sectheader.shRozmiar)
				konsola_2.MWydrukuj("]")
				copy(bieżący.tekst[:sectheader.shRozmiar], sectWartość[:sectheader.shRozmiar])
				bieżący.tekstlen = sectheader.shRozmiar
			}
			if OdpowiedniBajty(sectNazwa, ([]byte)(".rel.text")) {
				konsola_2.MWydrukuj(".rel.text")
				konsola_2.MWydrukuj("[")
				konsola_2.MUnsignedinteger32Wydrukuj(sectheader.shAdres)
				konsola_2.MWydrukuj(":")
				konsola_2.MUnsignedinteger32Wydrukuj(sectheader.shRozmiar)
				konsola_2.MWydrukuj("]")
				for rt := uint32(0); rt < sectheader.shRozmiar/8; rt++ {
					przesunięcie := *(*uint32)(Pointer(&sectWartość[rt*8]))
					bieżący.relTekst[rt].przesunięcie = przesunięcie
					bieżący.relTekst[rt].oAdres = *(*uint32)(Pointer(&bieżący.tekst[przesunięcie]))
					bieżący.relTekst[rt].liczba_2 = *(*uint32)(Pointer(&sectWartość[rt*8+4]))
					bieżący.relTekstlen++
				}
			}
			if OdpowiedniBajty(sectNazwa, ([]byte)(".dynsym")) {
				konsola_2.MWydrukuj(".dynsym")
				konsola_2.MWydrukuj("[")
				konsola_2.MUnsignedinteger32Wydrukuj(sectheader.shAdres)
				konsola_2.MWydrukuj(":")
				konsola_2.MUnsignedinteger32Wydrukuj(sectheader.shRozmiar)
				konsola_2.MWydrukuj("]")
				for rt := uint32(0); rt < sectheader.shRozmiar/8; rt++ {
					przesunięcie := *(*uint32)(Pointer(&sectWartość[rt*8]))
					bieżący.relTekst[rt].przesunięcie = przesunięcie
					bieżący.relTekst[rt].oAdres = *(*uint32)(Pointer(&bieżący.tekst[przesunięcie]))
					bieżący.relTekst[rt].liczba_2 = *(*uint32)(Pointer(&sectWartość[rt*8+4]))
					bieżący.relTekstlen++
				}
			}
			if OdpowiedniBajty(sectNazwa, ([]byte)(".dynstr")) {
				konsola_2.MWydrukuj(".dynstr")
				konsola_2.MWydrukuj("[")
				konsola_2.MUnsignedinteger32Wydrukuj(sectheader.shAdres)
				konsola_2.MWydrukuj(":")
				konsola_2.MUnsignedinteger32Wydrukuj(sectheader.shRozmiar)
				konsola_2.MWydrukuj("]")
			}
			if OdpowiedniBajty(sectNazwa, ([]byte)(".strtab")) {
				konsola_2.MWydrukuj(".strtab")
				konsola_2.MWydrukuj("[")
				konsola_2.MUnsignedinteger32Wydrukuj(sectheader.shAdres)
				konsola_2.MWydrukuj("]")
				rt := uint32(0)
				uruchom := uint32(0)

				for st := uint32(1); st < sectheader.shRozmiar; st++ {
					if sectWartość[st] == 0x0 || sectWartość[st] == ' ' {
						funcNazwa := sectWartość[uruchom+1 : st]
						konsola_2.MWydrukuj("+")
						konsola_2.MWydrukuj(funcNazwa)
						bieżący.strtab[rt] = BajtytoCIĄG(funcNazwa)
						uruchom = st
						rt++
					}
				}

			}

		}

		konsola_2.MWydrukuj(([]byte)("<------------"))
		for rt := uint32(0); rt < bieżący.relTekstlen; rt++ {
			konsola_2.MWydrukuj("[")
			konsola_2.MWydrukuj(([]byte)(bieżący.strtab[rt]))
			konsola_2.MWydrukuj(":")
			konsola_2.MUnsignedinteger32Wydrukuj(bieżący.relTekst[rt].liczba_2)
			konsola_2.MWydrukuj(":")

			konsola_2.MWydrukuj(([]byte)("]"))
		}
		konsola_2.MWydrukuj(([]byte)("------------>"))

		if tekstKursor != nil {
			pamięćmanager.Wolne(tekstKursor)
		}

	}

}
