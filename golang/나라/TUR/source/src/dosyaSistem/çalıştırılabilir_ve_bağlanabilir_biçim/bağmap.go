package çalıştırılabilir_ve_bağlanabilir_biçim

import . "unsafe"
import . "konsol"

import mem "bellekmanager"

type Bağ struct {
	Devingen	uintptr
	Previous	*Bağ
	Sonraki		*Bağ
}
type Bağmap struct {
	First	*Bağ
	Son	*Bağ

	Boyut_2	int

	mem	*mem.TBellekmanager
}

func (self *Bağmap) Init(mem *mem.TBellekmanager) {
	self.mem = mem
}
func (self *Bağmap) Clone() Bağmap {
	var bağmap Bağmap

	bağmap.Init(self.mem)

	Bağ := self.First

	for ; Bağ != nil; Bağ = Bağ.Sonraki {
		bağmap.Listenin_sonuna_ekle(Bağ.Devingen)
	}
	return bağmap
}
func (self *Bağmap) Listenin_başına_ekle(Devingen uintptr) {
	yeniBağ := (*Bağ)(self.mem.Bellek_ayır(uint32(Sizeof(Bağ{}))))
	yeniBağ.Devingen = Devingen
	yeniBağ.Sonraki = self.First
	self.First = yeniBağ
	self.Boyut_2++

	if self.First.Sonraki == nil {
		self.Son = self.First
	}
}
func (self *Bağmap) Listenin_sonuna_ekle(Devingen uintptr) {
	if Devingen == 0 {
		return
	}

	if self.Boyut_2 == 0 {
		self.Listenin_başına_ekle(Devingen)
	} else {
		yeniBağ := (*Bağ)(self.mem.Bellek_ayır(uint32(Sizeof(Bağ{}))))
		yeniBağ.Devingen = Devingen
		yeniBağ.Sonraki = nil
		self.Son.Sonraki = yeniBağ
		self.Son = yeniBağ
		self.Boyut_2++
	}
}
func (self *Bağmap) Yazdır(x uint16, y uint16) {
	Bağ := self.First
	konsol_2 := TKonsol{}
	konsol_2.MYazdırxy("linkmap : ", x, y)
	for ; Bağ != nil; Bağ = Bağ.Sonraki {
		konsol_2.MUnsignedinteger32Yazdır(uint32(Bağ.Devingen))
		konsol_2.MYazdır("+")

	}
}
