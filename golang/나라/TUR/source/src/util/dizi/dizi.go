package dizi

import . "unsafe"
import . "konsol"

var düğümDizi [100]uintptr

type TDizi struct {
	Boyut_2 int
}

func (self *TDizi) Ekle(adres_başvurusu uintptr) {
	düğümDizi[self.Boyut_2] = adres_başvurusu
	self.Boyut_2++
}
func (self *TDizi) Getat(içindekiler int) Pointer {
	return Pointer(düğümDizi[içindekiler])
}
func (self *TDizi) İçindekilerof(adres_başvurusu uintptr) int {
	i := 0
	for ; i < self.Boyut_2; i++ {
		if adres_başvurusu == düğümDizi[i] {
			return i
		}
	}
	return -1
}

var konsol_2 = TKonsol{}

func (self *TDizi) Yazdır() {
	konsol_2.MYazdırxy("array:", 1, 1)

	for i := 0; i < self.Boyut_2; i++ {
		konsol_2.MUnsignedinteger32Yazdır(uint32(düğümDizi[i]))
		konsol_2.MYazdır(":")
	}
}
