package liste

import . "unsafe"
import . "konsol"
import mem "bellekmanager"

type TListe_düğümü struct {
	adres_başvurusu	uintptr
	previous	*TListe_düğümü
	sonraki		*TListe_düğümü
}

type LinkedListe struct {
	head	*TListe_düğümü
	tail	*TListe_düğümü
	Boyut_2	int

	mem	*mem.TBellekmanager
}

func (self *LinkedListe) Init(mem *mem.TBellekmanager) {
	self.head = nil
	self.tail = nil
	self.Boyut_2 = 0

	self.mem = mem
}
func (self *LinkedListe) Listenin_başına_ekle(adres_başvurusu uintptr) {
	yeniDüğüm := (*TListe_düğümü)(self.mem.Bellek_ayır(uint32(Sizeof(TListe_düğümü{}))))
	if yeniDüğüm == nil {
		return
	}
	yeniDüğüm.adres_başvurusu = adres_başvurusu
	yeniDüğüm.previous = nil
	yeniDüğüm.sonraki = self.head
	if self.head != nil {
		self.head.previous = yeniDüğüm
	}
	self.head = yeniDüğüm
	self.Boyut_2++

	if self.head.sonraki == nil {
		self.tail = self.head
	}

}
func (self *LinkedListe) Listenin_sonuna_ekle(adres_başvurusu uintptr) {
	if self.Boyut_2 == 0 {
		self.Listenin_başına_ekle(adres_başvurusu)
	} else {
		yeniDüğüm := (*TListe_düğümü)(self.mem.Bellek_ayır(uint32(Sizeof(TListe_düğümü{}))))
		if yeniDüğüm == nil {
			return
		}
		yeniDüğüm.adres_başvurusu = adres_başvurusu
		yeniDüğüm.previous = self.tail
		yeniDüğüm.sonraki = nil
		self.tail.sonraki = yeniDüğüm
		self.tail = yeniDüğüm
		self.Boyut_2++
	}
}
func (self *LinkedListe) Dizine_göre_araya_ekle(içindekiler int, adres_başvurusu uintptr) {
	if içindekiler == 0 {
		self.Listenin_başına_ekle(adres_başvurusu)
	} else {
		previousDüğüm := self.GetDüğümat(içindekiler - 1)
		sonrakiDüğüm := previousDüğüm.sonraki
		yeniDüğüm := (*TListe_düğümü)(self.mem.Bellek_ayır(uint32(Sizeof(TListe_düğümü{}))))
		if yeniDüğüm == nil {
			return
		}
		yeniDüğüm.adres_başvurusu = adres_başvurusu

		previousDüğüm.sonraki = yeniDüğüm
		yeniDüğüm.previous = previousDüğüm
		yeniDüğüm.sonraki = sonrakiDüğüm
		if sonrakiDüğüm != nil {
			sonrakiDüğüm.previous = yeniDüğüm
		}

		self.Boyut_2++

		if yeniDüğüm.sonraki == nil {
			self.tail = yeniDüğüm
		}
	}
}
func (self *LinkedListe) GetDüğümat(içindekiler int) *TListe_düğümü {
	if içindekiler < 0 || içindekiler >= self.Boyut_2 {
		return nil
	}
	var x *TListe_düğümü = self.head
	for i := 0; i < içindekiler; i++ {
		x = x.sonraki
	}
	return x
}

func (self *LinkedListe) AyarlaDüğümat(içindekiler int, adres_başvurusu uintptr) {
	var x *TListe_düğümü = self.head
	for i := 0; i < içindekiler; i++ {
		x = x.sonraki
	}
	if x != nil {
		x.adres_başvurusu = adres_başvurusu
	}
}
func (self *LinkedListe) Getat(içindekiler int) Pointer {
	liste_düğümü := self.GetDüğümat(içindekiler)
	if liste_düğümü == nil {
		return nil
	}
	var adres_başvurusu uintptr = liste_düğümü.adres_başvurusu
	return Pointer(adres_başvurusu)
}
func (self *LinkedListe) İçindekilerof(adres_başvurusu uintptr) int {
	var n *TListe_düğümü = self.head
	i := 0
	for ; i < self.Boyut_2; i++ {
		if adres_başvurusu == n.adres_başvurusu {
			return i
		}
		n = n.sonraki
	}
	return -1
}
func (self *LinkedListe) Kaldır(adres_başvurusu uintptr) {
	içindekiler := self.İçindekilerof(adres_başvurusu)
	if içindekiler < 0 {
		return
	}
	self.Kaldırat(içindekiler)
}
func (self *LinkedListe) Kaldırat(içindekiler int) {
	if içindekiler < 0 || içindekiler >= self.Boyut_2 {
		return
	}
	liste_düğümü := self.GetDüğümat(içindekiler)
	if liste_düğümü == nil {
		return
	}
	if liste_düğümü.previous != nil {
		liste_düğümü.previous.sonraki = liste_düğümü.sonraki
	} else {
		self.head = liste_düğümü.sonraki
	}
	if liste_düğümü.sonraki != nil {
		liste_düğümü.sonraki.previous = liste_düğümü.previous
	} else {
		self.tail = liste_düğümü.previous
	}
	self.Boyut_2 = self.Boyut_2 - 1

	if self.mem != nil {
		self.mem.Boş(Pointer(liste_düğümü))
	}
}

var konsol_2 = TKonsol{}

func (self *LinkedListe) Yazdır() {
	konsol_2.MYazdırxy("LinkedList:", 1, 1)
	konsol_2.MUnsignedinteger32Yazdır(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Boyut_2; i++ {
		liste_düğümü := (*TListe_düğümü)(self.Getat(i))
		konsol_2.MUnsignedinteger32Yazdır(uint32(liste_düğümü.adres_başvurusu))
		konsol_2.MYazdır(":")
	}
}
