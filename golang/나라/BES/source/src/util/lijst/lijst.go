package lijst

import . "unsafe"
import . "console"
import mem "geheugenmanager"

type TLijstknooppunt struct {
	adresverwijzing	uintptr
	previous	*TLijstknooppunt
	volgende	*TLijstknooppunt
}

type LinkedLijst struct {
	head		*TLijstknooppunt
	tail		*TLijstknooppunt
	Grootte_2	int

	mem	*mem.TGeheugenmanager
}

func (zelf *LinkedLijst) Init(mem *mem.TGeheugenmanager) {
	zelf.head = nil
	zelf.tail = nil
	zelf.Grootte_2 = 0

	zelf.mem = mem
}
func (zelf *LinkedLijst) Vooraan_toevoegen(adresverwijzing uintptr) {
	nieuwSysteemnaam := (*TLijstknooppunt)(zelf.mem.Geheugen_toewijzen(uint32(Sizeof(TLijstknooppunt{}))))
	if nieuwSysteemnaam == nil {
		return
	}
	nieuwSysteemnaam.adresverwijzing = adresverwijzing
	nieuwSysteemnaam.previous = nil
	nieuwSysteemnaam.volgende = zelf.head
	if zelf.head != nil {
		zelf.head.previous = nieuwSysteemnaam
	}
	zelf.head = nieuwSysteemnaam
	zelf.Grootte_2++

	if zelf.head.volgende == nil {
		zelf.tail = zelf.head
	}

}
func (zelf *LinkedLijst) Achteraan_toevoegen(adresverwijzing uintptr) {
	if zelf.Grootte_2 == 0 {
		zelf.Vooraan_toevoegen(adresverwijzing)
	} else {
		nieuwSysteemnaam := (*TLijstknooppunt)(zelf.mem.Geheugen_toewijzen(uint32(Sizeof(TLijstknooppunt{}))))
		if nieuwSysteemnaam == nil {
			return
		}
		nieuwSysteemnaam.adresverwijzing = adresverwijzing
		nieuwSysteemnaam.previous = zelf.tail
		nieuwSysteemnaam.volgende = nil
		zelf.tail.volgende = nieuwSysteemnaam
		zelf.tail = nieuwSysteemnaam
		zelf.Grootte_2++
	}
}
func (zelf *LinkedLijst) Op_positie_invoegen(index int, adresverwijzing uintptr) {
	if index == 0 {
		zelf.Vooraan_toevoegen(adresverwijzing)
	} else {
		previousSysteemnaam := zelf.GetSysteemnaamat(index - 1)
		volgendeSysteemnaam := previousSysteemnaam.volgende
		nieuwSysteemnaam := (*TLijstknooppunt)(zelf.mem.Geheugen_toewijzen(uint32(Sizeof(TLijstknooppunt{}))))
		if nieuwSysteemnaam == nil {
			return
		}
		nieuwSysteemnaam.adresverwijzing = adresverwijzing

		previousSysteemnaam.volgende = nieuwSysteemnaam
		nieuwSysteemnaam.previous = previousSysteemnaam
		nieuwSysteemnaam.volgende = volgendeSysteemnaam
		if volgendeSysteemnaam != nil {
			volgendeSysteemnaam.previous = nieuwSysteemnaam
		}

		zelf.Grootte_2++

		if nieuwSysteemnaam.volgende == nil {
			zelf.tail = nieuwSysteemnaam
		}
	}
}
func (zelf *LinkedLijst) GetSysteemnaamat(index int) *TLijstknooppunt {
	if index < 0 || index >= zelf.Grootte_2 {
		return nil
	}
	var x *TLijstknooppunt = zelf.head
	for i := 0; i < index; i++ {
		x = x.volgende
	}
	return x
}

func (zelf *LinkedLijst) InstellenSysteemnaamat(index int, adresverwijzing uintptr) {
	var x *TLijstknooppunt = zelf.head
	for i := 0; i < index; i++ {
		x = x.volgende
	}
	if x != nil {
		x.adresverwijzing = adresverwijzing
	}
}
func (zelf *LinkedLijst) Getat(index int) Pointer {
	lijstknooppunt := zelf.GetSysteemnaamat(index)
	if lijstknooppunt == nil {
		return nil
	}
	var adresverwijzing uintptr = lijstknooppunt.adresverwijzing
	return Pointer(adresverwijzing)
}
func (zelf *LinkedLijst) Indexvan(adresverwijzing uintptr) int {
	var n *TLijstknooppunt = zelf.head
	i := 0
	for ; i < zelf.Grootte_2; i++ {
		if adresverwijzing == n.adresverwijzing {
			return i
		}
		n = n.volgende
	}
	return -1
}
func (zelf *LinkedLijst) Verwijderen_2(adresverwijzing uintptr) {
	index := zelf.Indexvan(adresverwijzing)
	if index < 0 {
		return
	}
	zelf.Verwijderenat(index)
}
func (zelf *LinkedLijst) Verwijderenat(index int) {
	if index < 0 || index >= zelf.Grootte_2 {
		return
	}
	lijstknooppunt := zelf.GetSysteemnaamat(index)
	if lijstknooppunt == nil {
		return
	}
	if lijstknooppunt.previous != nil {
		lijstknooppunt.previous.volgende = lijstknooppunt.volgende
	} else {
		zelf.head = lijstknooppunt.volgende
	}
	if lijstknooppunt.volgende != nil {
		lijstknooppunt.volgende.previous = lijstknooppunt.previous
	} else {
		zelf.tail = lijstknooppunt.previous
	}
	zelf.Grootte_2 = zelf.Grootte_2 - 1

	if zelf.mem != nil {
		zelf.mem.Vrij(Pointer(lijstknooppunt))
	}
}

var console_2 = TConsole{}

func (zelf *LinkedLijst) Afdrukken() {
	console_2.MAfdrukkenxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Afdrukken(uint32(uintptr(Pointer(zelf))))
	for i := 0; i < zelf.Grootte_2; i++ {
		lijstknooppunt := (*TLijstknooppunt)(zelf.Getat(i))
		console_2.MUnsignedinteger32Afdrukken(uint32(lijstknooppunt.adresverwijzing))
		console_2.MAfdrukken(":")
	}
}
