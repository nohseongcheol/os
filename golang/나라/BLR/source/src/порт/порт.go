package порт

var пазіцыя uint16 = 1

type TПорт struct {
	portnumber uint16
}

type TПорт8bit struct {
	TПорт
	чытаннеcount	uint16
	запісcount	uint16
}

func (self *TПорт8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.чытаннеcount = 65
	self.запісcount = 65
}
func (self *TПорт8bit) Запіс(data uint8) {
	ПортВыходныяbyte(self.portnumber, data)
}
func (self *TПорт8bit) Чытанне() uint8 {
	var result = Портуbyte(self.portnumber)
	return result
}
func ПортЗапісbyte(portnumber uint16, data uint8) {
	ПортВыходныяbyte(portnumber, data)
}
func ПортЧытаннеbyte(portnumber uint16) uint8 {
	result := Портуbyte(portnumber)
	return result
}

type TПорт16bit struct {
	TПорт
}

func (self *TПорт16bit) Init(portnumber uint16) {
	self.TПорт.portnumber = portnumber
}
func (self *TПорт16bit) Запіс(data uint16) {
	ПортВыходныяслова(self.TПорт.portnumber, data)
}
func (self *TПорт16bit) Чытанне() uint16 {
	var result = Портуслова(self.TПорт.portnumber)
	return result
}
func ПортЗапісслова(portnumber uint16, data uint16) {
	ПортВыходныяслова(portnumber, data)
}
func ПортЧытаннеслова(portnumber uint16) uint16 {
	var result uint16 = Портуслова(portnumber)
	return result
}

type TПорт32bit struct {
	TПорт
}

func (self *TПорт32bit) Init(portnumber uint16) {
	self.TПорт.portnumber = portnumber
}
func (self *TПорт32bit) Запіс(data uint32) {
	ПортВыходныяdword(self.TПорт.portnumber, data)
}
func (self *TПорт32bit) Чытанне() {
	Портуdword(self.TПорт.portnumber)
}
func ПортЗапісdword(portnumber uint16, data uint32) {
	ПортВыходныяdword(portnumber, data)
}
func ПортЧытаннеdword(portnumber uint16) uint32 {
	var result uint32 = Портуdword(portnumber)
	return result
}

var чытаннеcount uint16 = 65
var запісcount uint16 = 66

func ПортВыходныяbyte(portnumber uint16, data uint8)
func Портуbyte(portnumber uint16) uint8

func ПортВыходныяслова(portnumber uint16, data uint16)
func Портуслова(portnumber uint16) uint16

func ПортВыходныяdword(portnumber uint16, data uint32)
func Портуdword(portnumber uint16) uint32
