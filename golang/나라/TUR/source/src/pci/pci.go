package pci

import . "bağlantıNoktası"
import . "kesme"
import . "konsol"
import . "driver/driver"

type IpciDenetleyicihandler interface {
	Açıkgetdriver(aygıt TPeripheralcomponentinterconnectAygıtdescriptor)
}

var ipciDenetleyicihandler IpciDenetleyicihandler

type TÖntanımlıpciDenetleyicihandler struct {
}

func (self TÖntanımlıpciDenetleyicihandler) Açıkgetdriver(aygıt TPeripheralcomponentinterconnectAygıtdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectAygıtdescriptor struct {
	BağlantıNoktasıbase	uint32
	Kesme			uint32

	bus		uint16
	aygıt_2		uint16
	fonksiyon	uint16

	ÜreticiNo	uint16
	AygıtNo		uint16

	sınıfNo		uint8
	subclassNo	uint8
	arayüzNo	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectAygıtdescriptor) Init() {
}

type TPeripheralcomponentinterconnectDenetleyici struct {
	ipciDenetleyicihandler	IpciDenetleyicihandler
	dataBağlantıNoktası	uint16
	komutBağlantıNoktası	uint16
}

func (self *TPeripheralcomponentinterconnectDenetleyici) Init(ipciDenetleyicihandler IpciDenetleyicihandler) {
	self.dataBağlantıNoktası = 0xCFC
	self.komutBağlantıNoktası = 0xCF8

	self.ipciDenetleyicihandler = TÖntanımlıpciDenetleyicihandler{}
	if ipciDenetleyicihandler != nil {
		self.ipciDenetleyicihandler = ipciDenetleyicihandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectDenetleyici) Okuma(bus uint16, aygıt_2 uint16, fonksiyon uint16, registeroffset uint32) uint32 {
	var no uint32 = 0
	no = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(aygıt_2&0x1f) << 11) | (uint32(fonksiyon&0x07) << 8) | uint32(registeroffset&0xFC)

	BağlantıNoktasıYazmadword(self.komutBağlantıNoktası, no)

	sONUÇ1 := BağlantıNoktasıOkumadword(self.dataBağlantıNoktası)
	sONUÇ2 := (sONUÇ1 >> (8 * (registeroffset % 4)))

	return sONUÇ2
}

func (self *TPeripheralcomponentinterconnectDenetleyici) Yazma(bus uint16, aygıt_2 uint16, fonksiyon uint16, registeroffset uint32, değer uint32) {
	var no uint32
	no = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((aygıt_2&0x1f)<<11) | uint32((fonksiyon&0x07)<<8) | uint32(registeroffset&0xFC)
	BağlantıNoktasıYazmadword(self.komutBağlantıNoktası, no)
	BağlantıNoktasıYazmadword(self.dataBağlantıNoktası, değer)
}
func (self *TPeripheralcomponentinterconnectDenetleyici) AygıthasFonksiyonlar(bus uint16, aygıt_2 uint16) bool {
	sONUÇ := self.Okuma(bus, aygıt_2, 0, 0x0E)
	if (sONUÇ & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konsol TKonsol = TKonsol{}

func (self *TPeripheralcomponentinterconnectDenetleyici) Seçdriver(drivermanager *TDrivermanager, interrupts *TKesmemanager) {
	for bus := 0; bus < 8; bus++ {
		for aygıt_2 := 0; aygıt_2 < 32; aygıt_2++ {

			var sayıFonksiyonlar int = 1
			if self.AygıthasFonksiyonlar(uint16(bus), uint16(aygıt_2)) == true {
				sayıFonksiyonlar = 8
			} else {
				sayıFonksiyonlar = 1
			}

			for fonksiyon := 0; fonksiyon < sayıFonksiyonlar; fonksiyon++ {
				var aygıt TPeripheralcomponentinterconnectAygıtdescriptor
				aygıt = self.GetAygıtdescriptor(uint16(bus), uint16(aygıt_2), uint16(fonksiyon))
				if aygıt.ÜreticiNo == 0x0000 || aygıt.ÜreticiNo == 0xFFFF {
					continue
				}

				for çubukSayı := 0; çubukSayı < 6; çubukSayı++ {
					var çubuk TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(aygıt_2), uint16(fonksiyon), uint16(çubukSayı))
					if çubuk.address_2 != 0 && (çubuk.regtype == 1) {
						aygıt.BağlantıNoktasıbase = çubuk.address_2
					}

					self.Getdriver(aygıt, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectDenetleyici) GetAygıtdescriptor(bus uint16, aygıt_2 uint16, fonksiyon uint16) TPeripheralcomponentinterconnectAygıtdescriptor {
	var sONUÇ TPeripheralcomponentinterconnectAygıtdescriptor
	sONUÇ = TPeripheralcomponentinterconnectAygıtdescriptor{}
	sONUÇ.bus = bus
	sONUÇ.aygıt_2 = aygıt_2
	sONUÇ.fonksiyon = fonksiyon

	sONUÇ.ÜreticiNo = uint16(self.Okuma(bus, aygıt_2, fonksiyon, 0x00))
	sONUÇ.AygıtNo = uint16(self.Okuma(bus, aygıt_2, fonksiyon, 0x02))

	sONUÇ.sınıfNo = uint8(self.Okuma(bus, aygıt_2, fonksiyon, 0x0b))
	sONUÇ.subclassNo = uint8(self.Okuma(bus, aygıt_2, fonksiyon, 0x0a))
	sONUÇ.arayüzNo = uint8(self.Okuma(bus, aygıt_2, fonksiyon, 0x09))

	sONUÇ.revision = uint8(self.Okuma(bus, aygıt_2, fonksiyon, 0x08))
	sONUÇ.Kesme = uint32(self.Okuma(bus, aygıt_2, fonksiyon, 0x3C))

	return sONUÇ
}
func (self *TPeripheralcomponentinterconnectDenetleyici) Getbaseaddressregister(bus uint16, aygıt_2 uint16, fonksiyon uint16, çubuk uint16) TBaseaddressregister {
	var sONUÇ TBaseaddressregister

	headertype := self.Okuma(bus, aygıt_2, fonksiyon, 0x0E) & 0x7F
	var makbars int = int(6 - (4 * headertype))
	if çubuk >= uint16(makbars) {
		return sONUÇ
	}

	çubukDeğer := self.Okuma(bus, aygıt_2, fonksiyon, uint32(0x10+4*çubuk))

	if (çubukDeğer & 0x1) != 0 {
		sONUÇ.regtype = 1
	} else {
		sONUÇ.regtype = 0
	}

	if sONUÇ.regtype == 0 {
	} else {
		sONUÇ.address_2 = çubukDeğer & ^uint32(0x3)
		sONUÇ.prefetchcapable = false
	}

	return sONUÇ
}
func (self *TPeripheralcomponentinterconnectDenetleyici) Getdriver(aygıt TPeripheralcomponentinterconnectAygıtdescriptor, interrupts *TKesmemanager) {

	self.ipciDenetleyicihandler.Açıkgetdriver(aygıt)

}
