package bağlantıNoktası

var konum uint16 = 1

type TBağlantıNoktası struct {
	portnumber uint16
}

type TBağlantıNoktası8bit struct {
	TBağlantıNoktası
	okumacount	uint16
	yazmacount	uint16
}

func (self *TBağlantıNoktası8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.okumacount = 65
	self.yazmacount = 65
}
func (self *TBağlantıNoktası8bit) Yazma(data uint8) {
	BağlantıNoktasıGidenbyte(self.portnumber, data)
}
func (self *TBağlantıNoktası8bit) Okuma() uint8 {
	var sONUÇ = BağlantıNoktasıGelenbyte(self.portnumber)
	return sONUÇ
}
func BağlantıNoktasıYazmabyte(portnumber uint16, data uint8) {
	BağlantıNoktasıGidenbyte(portnumber, data)
}
func BağlantıNoktasıOkumabyte(portnumber uint16) uint8 {
	sONUÇ := BağlantıNoktasıGelenbyte(portnumber)
	return sONUÇ
}

type TBağlantıNoktası16bit struct {
	TBağlantıNoktası
}

func (self *TBağlantıNoktası16bit) Init(portnumber uint16) {
	self.TBağlantıNoktası.portnumber = portnumber
}
func (self *TBağlantıNoktası16bit) Yazma(data uint16) {
	BağlantıNoktasıGidenkelime(self.TBağlantıNoktası.portnumber, data)
}
func (self *TBağlantıNoktası16bit) Okuma() uint16 {
	var sONUÇ = BağlantıNoktasıGelenkelime(self.TBağlantıNoktası.portnumber)
	return sONUÇ
}
func BağlantıNoktasıYazmakelime(portnumber uint16, data uint16) {
	BağlantıNoktasıGidenkelime(portnumber, data)
}
func BağlantıNoktasıOkumakelime(portnumber uint16) uint16 {
	var sONUÇ uint16 = BağlantıNoktasıGelenkelime(portnumber)
	return sONUÇ
}

type TBağlantıNoktası32bit struct {
	TBağlantıNoktası
}

func (self *TBağlantıNoktası32bit) Init(portnumber uint16) {
	self.TBağlantıNoktası.portnumber = portnumber
}
func (self *TBağlantıNoktası32bit) Yazma(data uint32) {
	BağlantıNoktasıGidendword(self.TBağlantıNoktası.portnumber, data)
}
func (self *TBağlantıNoktası32bit) Okuma() {
	BağlantıNoktasıGelendword(self.TBağlantıNoktası.portnumber)
}
func BağlantıNoktasıYazmadword(portnumber uint16, data uint32) {
	BağlantıNoktasıGidendword(portnumber, data)
}
func BağlantıNoktasıOkumadword(portnumber uint16) uint32 {
	var sONUÇ uint32 = BağlantıNoktasıGelendword(portnumber)
	return sONUÇ
}

var okumacount uint16 = 65
var yazmacount uint16 = 66

func BağlantıNoktasıGidenbyte(portnumber uint16, data uint8)
func BağlantıNoktasıGelenbyte(portnumber uint16) uint8

func BağlantıNoktasıGidenkelime(portnumber uint16, data uint16)
func BağlantıNoktasıGelenkelime(portnumber uint16) uint16

func BağlantıNoktasıGidendword(portnumber uint16, data uint32)
func BağlantıNoktasıGelendword(portnumber uint16) uint32
