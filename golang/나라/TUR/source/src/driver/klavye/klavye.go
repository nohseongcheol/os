package klavye

import . "unsafe"

import . "bağlantıNoktası"
import . "kesme"

import . "konsol"
import . "sistemcall"

type IKlavyeOlayhandler interface {
	AçıkAnahtarAşağı(anahtar byte)
	AçıkAnahtarYukarı(anahtar byte)
}

var iKlavyeOlayhandler IKlavyeOlayhandler
var öntanımlıKlavyeOlayhandler TÖntanımlıKlavyeOlayhandler

type TÖntanımlıKlavyeOlayhandler struct {
}

func (self *TÖntanımlıKlavyeOlayhandler) AçıkAnahtarAşağı(anahtar byte) {
	onaltılık := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = onaltılık[((anahtar >> 4) & 0xF)]
	buffer[18] = onaltılık[anahtar&0xF]

	konsol_2 := TKonsol{}
	konsol_2.MYazdır(buffer)

}
func (self *TÖntanımlıKlavyeOlayhandler) AçıkAnahtarYukarı(anahtar byte) {
}

type TKlavyedriver struct {
	TKesmehandler
}

var aktifKlavyedriver *TKlavyedriver
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

func (self *TKlavyedriver) Initdriver(manager *TKesmemanager, klavyeOlayhandler IKlavyeOlayhandler) {

	iKlavyeOlayhandler = &öntanımlıKlavyeOlayhandler
	if klavyeOlayhandler != nil {
		iKlavyeOlayhandler = klavyeOlayhandler
	}

	aktifKlavyedriver = self
	kesmehandler = handleKlavyeKesme
	var address uintptr
	address = uintptr(Pointer(&kesmehandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (BağlantıNoktasıOkumabyte(komutBağlantıNoktası_2)&0x01) != 0; i++ {
		BağlantıNoktasıOkumabyte(dataBağlantıNoktası_2)
	}

	if !yazmaps2Komut(0xAE) || !yazmaps2Komut(0x20) {
		return
	}
	durum, tamam := okumaps2data()
	if !tamam {
		return
	}
	durum |= 0x01
	durum &^= 0x10
	if !yazmaps2Komut(0x60) || !yazmaps2data(durum) {
		return
	}

	if !yazmaps2data(0xF4) {
		return
	}
	ack, tamam := okumaps2data()
	if !tamam || ack != 0xFA {
		return
	}

}

func handleKlavyeKesme(esp uint32) uint32 {
	if aktifKlavyedriver == nil {
		BağlantıNoktasıOkumabyte(dataBağlantıNoktası_2)
		return esp
	}
	return aktifKlavyedriver.HandleKesme(esp)
}

const klavyequeueBoyut = 64

var klavyequeue [klavyequeueBoyut]byte
var klavyequeueOkuma uint8
var klavyequeueYazma uint8
var solshift bool
var sağshift bool
var extendedTaracode bool

func queueKlavyebyte(anahtar byte) {
	sonraki := (klavyequeueYazma + 1) % klavyequeueBoyut
	if sonraki == klavyequeueOkuma {
		return
	}
	klavyequeue[klavyequeueYazma] = anahtar
	klavyequeueYazma = sonraki
}

func SüreçpendingKlavyeOlaylar() {
	for klavyequeueOkuma != klavyequeueYazma {
		anahtar := klavyequeue[klavyequeueOkuma]
		klavyequeueOkuma = (klavyequeueOkuma + 1) % klavyequeueBoyut
		Stdinputbyte(anahtar)
		if iKlavyeOlayhandler != nil {
			iKlavyeOlayhandler.AçıkAnahtarAşağı(anahtar)
		}
	}
}

func taracodetobyte(taracode uint8) (byte, bool) {
	shift := solshift || sağshift

	if taracode >= 0x02 && taracode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[taracode-0x02], true
		}
		return "1234567890"[taracode-0x02], true
	}
	if taracode >= 0x10 && taracode <= 0x19 {
		anahtar := "qwertyuiop"[taracode-0x10]
		if shift {
			anahtar -= 'a' - 'A'
		}
		return anahtar, true
	}
	if taracode >= 0x1E && taracode <= 0x26 {
		anahtar := "asdfghjkl"[taracode-0x1E]
		if shift {
			anahtar -= 'a' - 'A'
		}
		return anahtar, true
	}
	if taracode >= 0x2C && taracode <= 0x32 {
		anahtar := "zxcvbnm"[taracode-0x2C]
		if shift {
			anahtar -= 'a' - 'A'
		}
		return anahtar, true
	}

	switch taracode {
	case 0x0C:
		if shift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (self *TKlavyedriver) HandleKesme(esp uint32) uint32 {
	durum := BağlantıNoktasıOkumabyte(komutBağlantıNoktası_2)
	if (durum&0x01) == 0 || (durum&0x20) != 0 {
		return esp
	}

	taracode := BağlantıNoktasıOkumabyte(dataBağlantıNoktası_2)
	if taracode == 0xE0 {
		extendedTaracode = true
		return esp
	}
	if extendedTaracode {
		extendedTaracode = false
		return esp
	}

	released := (taracode & 0x80) != 0
	basecode := taracode & 0x7F
	if basecode == 0x2A {
		solshift = !released
		return esp
	}
	if basecode == 0x36 {
		sağshift = !released
		return esp
	}
	if released {
		return esp
	}

	if anahtar, tamam := taracodetobyte(basecode); tamam {
		queueKlavyebyte(anahtar)
	}

	return esp
}
