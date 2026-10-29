/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package klavye

import . "unsafe"

import . "bağlantıNoktası"
import . "kesme"
import . "konsol"

type IFareOlayhandler interface {
	AçıkFareAşağı(düğme int8)
	AçıkFareYukarı(düğme int8)
	AçıkFareTaşı(x int8, y int8)
}

var iFareOlayhandler IFareOlayhandler

type TÖntanımlıFareOlayhandler struct {
}

var konsol_2 TKonsol = TKonsol{}
var previousx int16 = 0
var previousy int16 = 0
var xKonum int16 = 0
var yKonum int16 = 0

func (self TÖntanımlıFareOlayhandler) AçıkFareAşağı(düğme int8) {
	buffer := []byte("+")
	konsol_2.MYazdırxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TÖntanımlıFareOlayhandler) AçıkFareYukarı(düğme int8)	{}
func (self TÖntanımlıFareOlayhandler) AçıkFareTaşı(x int8, y int8) {

	xKonum += int16(x)
	if xKonum < 0 {
		xKonum = 0
	}
	if xKonum >= 80 {
		xKonum = 79
	}

	yKonum -= int16(y)

	if yKonum < 0 {
		yKonum = 0
	}
	if yKonum >= 25 {
		yKonum = 24
	}

	buffer := []byte(" ")
	konsol_2.MYazdırxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konsol_2.MYazdırxy(buffer, uint16(xKonum), uint16(yKonum))

	previousx = xKonum
	previousy = yKonum
}

type TFaredriver struct {
	TKesmehandler
}

var aktifFaredriver *TFaredriver
var kesmehandler func(uint32) uint32

var dataBağlantıNoktası_2 uint16 = 0x60
var komutBağlantıNoktası_2 uint16 = 0x64

const ps2BekleKısıtla = 100000

func bekleps2GirdiBoş() bool {
	for i := 0; i < ps2BekleKısıtla; i++ {
		if (BağlantıNoktasıOkumabyte(komutBağlantıNoktası_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func bekleps2ÇıktıTam() bool {
	for i := 0; i < ps2BekleKısıtla; i++ {
		if (BağlantıNoktasıOkumabyte(komutBağlantıNoktası_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func yazmaps2Komut(değer uint8) bool {
	if !bekleps2GirdiBoş() {
		return false
	}
	BağlantıNoktasıYazmabyte(komutBağlantıNoktası_2, değer)
	return true
}

func yazmaps2data(değer uint8) bool {
	if !bekleps2GirdiBoş() {
		return false
	}
	BağlantıNoktasıYazmabyte(dataBağlantıNoktası_2, değer)
	return true
}

func okumaps2data() (uint8, bool) {
	if !bekleps2ÇıktıTam() {
		return 0, false
	}
	return BağlantıNoktasıOkumabyte(dataBağlantıNoktası_2), true
}

func gönderFareKomut(değer uint8) bool {
	if !yazmaps2Komut(0xD4) || !yazmaps2data(değer) {
		return false
	}
	ack, tamam := okumaps2data()
	return tamam && ack == 0xFA
}

func (self *TFaredriver) Initdriver(manager *TKesmemanager, fareOlayhandler IFareOlayhandler) {

	iFareOlayhandler = TÖntanımlıFareOlayhandler{}

	if fareOlayhandler != nil {
		iFareOlayhandler = fareOlayhandler
	}

	aktifFaredriver = self
	kesmehandler = handleFareKesme
	var address uintptr
	address = uintptr(Pointer(&kesmehandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (BağlantıNoktasıOkumabyte(komutBağlantıNoktası_2)&0x01) != 0; i++ {
		BağlantıNoktasıOkumabyte(dataBağlantıNoktası_2)
	}

	if !yazmaps2Komut(0xA8) || !yazmaps2Komut(0x20) {
		return
	}
	durum, tamam := okumaps2data()
	if !tamam {
		return
	}
	durum |= 0x02
	durum &^= 0x20
	if !yazmaps2Komut(0x60) || !yazmaps2data(durum) {
		return
	}

	if !gönderFareKomut(0xF6) || !gönderFareKomut(0xF4) {
		return
	}
	offset = 0

}

func handleFareKesme(esp uint32) uint32 {
	if aktifFaredriver == nil {
		BağlantıNoktasıOkumabyte(dataBağlantıNoktası_2)
		return esp
	}
	return aktifFaredriver.HandleKesme(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var düğme_2 int8
var pendingx int16
var pendingy int16
var pendingDüğme int8
var pendingFareOlay bool

func (self *TFaredriver) HandleKesme(esp uint32) uint32 {
	durum := BağlantıNoktasıOkumabyte(komutBağlantıNoktası_2)
	if (durum&0x01) == 0 || (durum&0x20) == 0 {
		return esp
	}

	data := BağlantıNoktasıOkumabyte(dataBağlantıNoktası_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		pAKETDurum := uint8(buffer_2[0])

		if (pAKETDurum & 0xC0) == 0 {
			pendingx += int16(buffer_2[1])
			pendingy += int16(buffer_2[2])
			if pendingx > 127 {
				pendingx = 127
			} else if pendingx < -127 {
				pendingx = -127
			}
			if pendingy > 127 {
				pendingy = 127
			} else if pendingy < -127 {
				pendingy = -127
			}
		}
		pendingDüğme = int8(pAKETDurum & 0x07)
		pendingFareOlay = true
	}

	return esp

}

func SüreçpendingFareOlaylar() {
	if iFareOlayhandler == nil {
		return
	}

	Kesmedeactive()
	if !pendingFareOlay {
		KesmeAktif()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	yeniDüğme := pendingDüğme
	oldDüğme := düğme_2

	pendingx = 0
	pendingy = 0
	pendingFareOlay = false
	KesmeAktif()

	if x != 0 || y != 0 {
		iFareOlayhandler.AçıkFareTaşı(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maske := int8(0x1 << i)
		if (yeniDüğme & maske) != (oldDüğme & maske) {
			if (yeniDüğme & maske) != 0 {
				iFareOlayhandler.AçıkFareAşağı(int8(i + 1))
			} else {
				iFareOlayhandler.AçıkFareYukarı(int8(i + 1))
			}
		}
	}
	düğme_2 = yeniDüğme
}
