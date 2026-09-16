/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package seitenverwaltung

import unsafe "unsafe"
import . "unterbrechung"
import . "speicherVerwalter"
import . "hilfswerkzeug"

type SeiteOrdnerEintrag_2 uintptr

const (
	SeiteVorhanden	uint32	= 0x001
	Seitewritable	uint32	= 0x002
	SeiteBenutzer	uint32	= 0x004
	SeiteRahmen	uint32	= 0xFFFFF000
	Seitecow	uint32	= 0x200
)

func SetzenByteataddress(x byte, address uint32)
func Setzenunsignedinteger8ataddress(x uint8, address uint32)
func Setzenunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setzencr3(seitenverzeichnis uint32)
func getcr3() uint32

type Seitenverwaltung struct {
	TUnterbrechunghandler
}
type TcowRahmenVerwalter struct {
	mem		*TSpeicherVerwalter
	refs		[]uint16
	rahmenAnzahl	uint32
}

var (
	SeiteOrdnerEintrag	uintptr
	SeiteTabelleEintrag	uint32
	pdelen			uint32
	virtlen			uint32
	cowRahmenVerwalter	TcowRahmenVerwalter
)

func (selbst *TcowRahmenVerwalter) Init(mem *TSpeicherVerwalter, rahmenAnzahl uint32) bool {
	selbst.mem = mem
	selbst.rahmenAnzahl = rahmenAnzahl
	referenceByte := rahmenAnzahl * uint32(unsafe.Sizeof(uint16(0)))
	referenceZeiger := mem.Speicher_reservieren(referenceByte)
	if referenceZeiger == nil {
		selbst.refs = nil
		selbst.rahmenAnzahl = 0
		return false
	}
	selbst.refs = (*[1 << 28]uint16)(referenceZeiger)[:rahmenAnzahl:rahmenAnzahl]
	for i := uint32(0); i < rahmenAnzahl; i++ {
		selbst.refs[i] = 0
	}
	return true
}

func (selbst *TcowRahmenVerwalter) Reference(rahmen uint32) uint16 {
	idx := rahmen >> 12
	if idx >= selbst.rahmenAnzahl || selbst.refs == nil {
		return 0
	}
	return selbst.refs[idx]
}

func (selbst *TcowRahmenVerwalter) Increment(rahmen uint32) {
	idx := rahmen >> 12
	if idx >= selbst.rahmenAnzahl || selbst.refs == nil {
		return
	}
	if selbst.refs[idx] == 0 {
		selbst.refs[idx] = 2
	} else {
		selbst.refs[idx]++
	}
}

func (selbst *TcowRahmenVerwalter) Decrement(rahmen uint32) {
	idx := rahmen >> 12
	if idx >= selbst.rahmenAnzahl || selbst.refs == nil || selbst.refs[idx] == 0 {
		return
	}
	selbst.refs[idx]--
}

func (selbst *Seitenverwaltung) Init(seiteOrdnerEintrag uintptr, seiteTabelleEintrag uint32, speicherVerwalter *TSpeicherVerwalter) {

	SeiteOrdnerEintrag = seiteOrdnerEintrag
	SeiteTabelleEintrag = seiteTabelleEintrag

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRahmenVerwalter.Init(speicherVerwalter, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressZeiger, _ := speicherVerwalter.Alignedmalloc(0x1000)
			if addressZeiger == nil {
				return
			}
			address := uint32(uintptr(addressZeiger))

			Setzenunsignedinteger32ataddress(address|0x87, uint32(seiteOrdnerEintrag)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setzenunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		seiteOrdnerEintrag = seiteOrdnerEintrag + 0x1000
	}

}
func (selbst *Seitenverwaltung) SharedSpeicherregion() {

	seiteOrdnerEintrag := SeiteOrdnerEintrag
	kSeiteOrdnerEintrag := SeiteOrdnerEintrag

	for i := uint32(1); i <= virtlen; i++ {

		seiteOrdnerEintrag = seiteOrdnerEintrag + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetWert(uint32(kSeiteOrdnerEintrag) + pde*4)
			v = (v & 0xFFFFF000)
			Setzenunsignedinteger32ataddress(v|0x87, uint32(seiteOrdnerEintrag)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetWert(uint32(kSeiteOrdnerEintrag) + pde*4)
			v = (v & 0xFFFFF000)
			Setzenunsignedinteger32ataddress(v|0x87, uint32(seiteOrdnerEintrag)+pde*4)

		}

	}
}
func (selbst *Seitenverwaltung) SeiteFehler(verwalter *TUnterbrechungVerwalter) {
	unterbrechunghandler = griffSeitenverwaltungUnterbrechung

	var address uintptr
	address = uintptr(unsafe.Pointer(&unterbrechunghandler))
	selbst.TUnterbrechunghandler.Init(0xE, uintptr(unsafe.Pointer(verwalter)), address)
}

var unterbrechunghandler func(uint32) uint32

func griffSeitenverwaltungUnterbrechung(esp uint32) uint32 {
	if AuflösenKopierenbeiSchreibenFehler() {
		return esp
	}
	return GrifffatalUnterbrechungRahmen(esp, 0x0E)
}

func CloneaddressLeerzeichencow(quelleSeiteOrdner uint32) uint32 {
	if AktivSpeicherVerwalter == nil || quelleSeiteOrdner == 0 {
		return 0
	}
	zielZeiger, _ := AktivSpeicherVerwalter.Alignedmalloc(0x1000)
	if zielZeiger == nil {
		return 0
	}
	zielSeiteOrdner := uint32(uintptr(zielZeiger))
	for i := uint32(0); i < 1024; i++ {
		Setzenunsignedinteger32ataddress(0, zielSeiteOrdner+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		quellepdeaddress := quelleSeiteOrdner + pde*4
		quellepde := GetWert(quellepdeaddress)
		if (quellepde & SeiteVorhanden) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setzenunsignedinteger32ataddress(quellepde, zielSeiteOrdner+pde*4)
			continue
		}

		zielptZeiger, _ := AktivSpeicherVerwalter.Alignedmalloc(0x1000)
		if zielptZeiger == nil {
			continue
		}
		quellept := quellepde & SeiteRahmen
		zielpt := uint32(uintptr(zielptZeiger))
		Setzenunsignedinteger32ataddress((zielpt | (quellepde & 0xFFF)), zielSeiteOrdner+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := quellept + pte*4
			eintrag := GetWert(pteaddress)
			if (eintrag & SeiteVorhanden) != 0 {
				if (eintrag & Seitewritable) != 0 {
					eintrag = (eintrag &^ Seitewritable) | Seitecow
					Setzenunsignedinteger32ataddress(eintrag, pteaddress)
					cowRahmenVerwalter.Increment(eintrag & SeiteRahmen)
				} else if (eintrag & Seitecow) != 0 {
					cowRahmenVerwalter.Increment(eintrag & SeiteRahmen)
				}
			}
			Setzenunsignedinteger32ataddress(eintrag, zielpt+pte*4)
		}
	}
	neuladencr3()
	return zielSeiteOrdner
}

func AuflösenKopierenbeiSchreibenFehler() bool {
	if AktivSpeicherVerwalter == nil {
		return false
	}
	fehleraddress := getcr2()
	seitenverzeichnis := getcr3()
	pdeaddress := seitenverzeichnis + ((fehleraddress>>22)&0x3FF)*4
	pde := GetWert(pdeaddress)
	if (pde & SeiteVorhanden) == 0 {
		return false
	}
	pt := pde & SeiteRahmen
	pteaddress := pt + ((fehleraddress>>12)&0x3FF)*4
	pte := GetWert(pteaddress)
	if (pte&Seitecow) == 0 || (pte&SeiteVorhanden) == 0 {
		return false
	}
	altRahmen := pte & SeiteRahmen
	if cowRahmenVerwalter.Reference(altRahmen) <= 1 {
		Setzenunsignedinteger32ataddress((pte|Seitewritable)&^Seitecow, pteaddress)
		neuladencr3()
		return true
	}

	neuZeiger, _ := AktivSpeicherVerwalter.Alignedmalloc(0x1000)
	if neuZeiger == nil {
		return false
	}
	neuRahmen := uint32(uintptr(neuZeiger)) & SeiteRahmen

	quelle_2 := GetBytevonZeiger(uintptr(fehleraddress&SeiteRahmen), 0x1000, 0x1000)
	ziel_2 := GetBytevonZeiger(uintptr(neuRahmen), 0x1000, 0x1000)
	copy(ziel_2, quelle_2)
	cowRahmenVerwalter.Decrement(altRahmen)
	Setzenunsignedinteger32ataddress((neuRahmen|(pte&0xFFF)|Seitewritable)&^Seitecow, pteaddress)
	neuladencr3()
	return true
}

func issharedpde(pde uint32) bool {
	if pde < 12 {
		return true
	}
	if pde >= 16 && pde < 20 {
		return true
	}
	return false
}

func neuladencr3() {
	cr3 := getcr3()
	setzencr3(cr3)
}

func SetzenByteEinSeiteOrdner(x byte, address uint32, seitenverzeichnis uint32) {
	altcr3 := getcr3()
	setzencr3(seitenverzeichnis)
	SetzenByteataddress(x, address)
	setzencr3(altcr3)
}

func SetzenRechteckEinSeiteOrdner(quelle_2 []byte, ziel_2 []byte, größe uint32, seitenverzeichnis uint32) {
	if größe == 0 || seitenverzeichnis == 0 {
		return
	}
	altcr3 := getcr3()
	setzencr3(seitenverzeichnis)
	makeSpannweitePrivatwritableSystemzeit(seitenverzeichnis, uint32(uintptr(unsafe.Pointer(&ziel_2[0]))), größe)

	for i := uint32(0); i < größe; i++ {
		ziel_2[i] = quelle_2[i]
	}
	setzencr3(altcr3)
}

func NullRechteckEinSeiteOrdner(address uint32, größe uint32, seitenverzeichnis uint32) {
	if größe == 0 || seitenverzeichnis == 0 {
		return
	}
	altcr3 := getcr3()
	setzencr3(seitenverzeichnis)
	makeSpannweitePrivatwritableSystemzeit(seitenverzeichnis, address, größe)
	ziel_2 := GetBytevonZeiger(uintptr(address), int(größe), int(größe))
	for i := uint32(0); i < größe; i++ {
		ziel_2[i] = 0
	}
	setzencr3(altcr3)
}

func makeSeitePrivatwritableSystemzeit(seitenverzeichnis uint32, virtuelladdress uint32) bool {
	pde := GetWert(seitenverzeichnis + ((virtuelladdress>>22)&0x3FF)*4)
	if (pde & SeiteVorhanden) == 0 {
		return false
	}
	pteaddress := (pde & SeiteRahmen) + ((virtuelladdress>>12)&0x3FF)*4
	pte := GetWert(pteaddress)
	if (pte & SeiteVorhanden) == 0 {
		return false
	}
	if (pte & Seitecow) == 0 {
		return (pte & Seitewritable) != 0
	}
	if AktivSpeicherVerwalter == nil {
		return false
	}
	neuZeiger, _ := AktivSpeicherVerwalter.Alignedmalloc(0x1000)
	if neuZeiger == nil {
		return false
	}
	neuRahmen := uint32(uintptr(neuZeiger)) & SeiteRahmen
	quelle_2 := GetBytevonZeiger(uintptr(virtuelladdress&SeiteRahmen), 0x1000, 0x1000)
	ziel_2 := GetBytevonZeiger(uintptr(neuRahmen), 0x1000, 0x1000)
	copy(ziel_2, quelle_2)
	cowRahmenVerwalter.Decrement(pte & SeiteRahmen)
	Setzenunsignedinteger32ataddress((neuRahmen|(pte&0xFFF)|Seitewritable)&^Seitecow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	neuladencr3()
	return true
}

func makeSpannweitePrivatwritableSystemzeit(seitenverzeichnis uint32, address uint32, größe uint32) bool {
	if größe == 0 {
		return true
	}
	letzter := address + größe - 1
	if letzter < address {
		return false
	}
	for seite := address & SeiteRahmen; ; seite += 0x1000 {
		if !makeSeitePrivatwritableSystemzeit(seitenverzeichnis, seite) {
			return false
		}
		if seite == (letzter & SeiteRahmen) {
			break
		}
	}
	return true
}

func MakeSpannweitePrivatwritable(seitenverzeichnis uint32, address uint32, größe uint32) bool {
	if seitenverzeichnis == 0 {
		return false
	}
	altcr3 := getcr3()
	setzencr3(seitenverzeichnis)
	bestätigen := makeSpannweitePrivatwritableSystemzeit(seitenverzeichnis, address, größe)
	setzencr3(altcr3)
	return bestätigen
}

func Setzenunsignedinteger32EinSeiteOrdner(x uint32, address uint32, seitenverzeichnis uint32) {
	if seitenverzeichnis == 0 {
		return
	}
	altcr3 := getcr3()
	setzencr3(seitenverzeichnis)
	Setzenunsignedinteger32ataddress(x, address)
	setzencr3(altcr3)
}

func GetWert(address uint32) uint32 {
	var orgWert uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgWert
}
func GetWertEinSeiteOrdner(address uint32, seitenverzeichnis uint32) uint32 {
	if seitenverzeichnis == 0 {
		return 0
	}
	altcr3 := getcr3()
	setzencr3(seitenverzeichnis)
	v := GetWert(address)
	setzencr3(altcr3)
	return v
}

var v uint32 = 0

func KopierenSeiteRahmenRechteck(xSeiteOrdner uint32, ySeiteOrdner uint32, vaddress uint32) {
	if xSeiteOrdner == 0 || ySeiteOrdner == 0 {
		return
	}
	altcr3 := getcr3()
	setzencr3(xSeiteOrdner)
	v = GetWert(vaddress)
	Setzenunsignedinteger32EinSeiteOrdner(v, vaddress, ySeiteOrdner)

	setzencr3(altcr3)
}
