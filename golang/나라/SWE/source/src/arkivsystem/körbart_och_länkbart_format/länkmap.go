package körbart_och_länkbart_format

import . "unsafe"
import . "konsol"

import mem "minnemanager"

type Länk struct {
	Dynamisk	uintptr
	Previous	*Länk
	Nästa		*Länk
}
type Länkmap struct {
	First	*Länk
	Sista	*Länk

	Storlek_2	int

	mem	*mem.TMinnemanager
}

func (själv *Länkmap) Init(mem *mem.TMinnemanager) {
	själv.mem = mem
}
func (själv *Länkmap) Clone() Länkmap {
	var länkmap Länkmap

	länkmap.Init(själv.mem)

	Länk := själv.First

	for ; Länk != nil; Länk = Länk.Nästa {
		länkmap.Lägg_till_sist_i_listan(Länk.Dynamisk)
	}
	return länkmap
}
func (själv *Länkmap) Lägg_till_först_i_listan(Dynamisk uintptr) {
	nyLänk := (*Länk)(själv.mem.Tilldela_minne(uint32(Sizeof(Länk{}))))
	nyLänk.Dynamisk = Dynamisk
	nyLänk.Nästa = själv.First
	själv.First = nyLänk
	själv.Storlek_2++

	if själv.First.Nästa == nil {
		själv.Sista = själv.First
	}
}
func (själv *Länkmap) Lägg_till_sist_i_listan(Dynamisk uintptr) {
	if Dynamisk == 0 {
		return
	}

	if själv.Storlek_2 == 0 {
		själv.Lägg_till_först_i_listan(Dynamisk)
	} else {
		nyLänk := (*Länk)(själv.mem.Tilldela_minne(uint32(Sizeof(Länk{}))))
		nyLänk.Dynamisk = Dynamisk
		nyLänk.Nästa = nil
		själv.Sista.Nästa = nyLänk
		själv.Sista = nyLänk
		själv.Storlek_2++
	}
}
func (själv *Länkmap) Skrivut(x uint16, y uint16) {
	Länk := själv.First
	konsol_2 := TKonsol{}
	konsol_2.MSkrivutxy("linkmap : ", x, y)
	for ; Länk != nil; Länk = Länk.Nästa {
		konsol_2.MUnsignedinteger32Skrivut(uint32(Länk.Dynamisk))
		konsol_2.MSkrivut("+")

	}
}
