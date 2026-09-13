package порт

var турганжери uint16 = 1

type TПорт struct {
	portnumber uint16
}

type TПорт8bit struct {
	TПорт
	окууcount	uint16
	жазууcount	uint16
}

func (self *TПорт8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.окууcount = 65
	self.жазууcount = 65
}
func (self *TПорт8bit) Жазуу(data uint8) {
	ПортКичирейтүүbyte(self.portnumber, data)
}
func (self *TПорт8bit) Окуу() uint8 {
	var result = ПортЧоңойтууbyte(self.portnumber)
	return result
}
func ПортЖазууbyte(portnumber uint16, data uint8) {
	ПортКичирейтүүbyte(portnumber, data)
}
func ПортОкууbyte(portnumber uint16) uint8 {
	result := ПортЧоңойтууbyte(portnumber)
	return result
}

type TПорт16bit struct {
	TПорт
}

func (self *TПорт16bit) Init(portnumber uint16) {
	self.TПорт.portnumber = portnumber
}
func (self *TПорт16bit) Жазуу(data uint16) {
	ПортКичирейтүүсөз(self.TПорт.portnumber, data)
}
func (self *TПорт16bit) Окуу() uint16 {
	var result = ПортЧоңойтуусөз(self.TПорт.portnumber)
	return result
}
func ПортЖазуусөз(portnumber uint16, data uint16) {
	ПортКичирейтүүсөз(portnumber, data)
}
func ПортОкуусөз(portnumber uint16) uint16 {
	var result uint16 = ПортЧоңойтуусөз(portnumber)
	return result
}

type TПорт32bit struct {
	TПорт
}

func (self *TПорт32bit) Init(portnumber uint16) {
	self.TПорт.portnumber = portnumber
}
func (self *TПорт32bit) Жазуу(data uint32) {
	ПортКичирейтүүdword(self.TПорт.portnumber, data)
}
func (self *TПорт32bit) Окуу() {
	ПортЧоңойтууdword(self.TПорт.portnumber)
}
func ПортЖазууdword(portnumber uint16, data uint32) {
	ПортКичирейтүүdword(portnumber, data)
}
func ПортОкууdword(portnumber uint16) uint32 {
	var result uint32 = ПортЧоңойтууdword(portnumber)
	return result
}

var окууcount uint16 = 65
var жазууcount uint16 = 66

func ПортКичирейтүүbyte(portnumber uint16, data uint8)
func ПортЧоңойтууbyte(portnumber uint16) uint8

func ПортКичирейтүүсөз(portnumber uint16, data uint16)
func ПортЧоңойтуусөз(portnumber uint16) uint16

func ПортКичирейтүүdword(portnumber uint16, data uint32)
func ПортЧоңойтууdword(portnumber uint16) uint32
