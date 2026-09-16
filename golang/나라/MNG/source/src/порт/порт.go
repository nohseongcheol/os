/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package порт

var position uint16 = 1

type TПорт struct {
	portnumber uint16
}

type TПорт8bit struct {
	TПорт
	уншихcount	uint16
	бичихcount	uint16
}

func (self *TПорт8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.уншихcount = 65
	self.бичихcount = 65
}
func (self *TПорт8bit) Бичих(data uint8) {
	Портoutbyte(self.portnumber, data)
}
func (self *TПорт8bit) Унших() uint8 {
	var result = Портinbyte(self.portnumber)
	return result
}
func ПортБичихbyte(portnumber uint16, data uint8) {
	Портoutbyte(portnumber, data)
}
func ПортУншихbyte(portnumber uint16) uint8 {
	result := Портinbyte(portnumber)
	return result
}

type TПорт16bit struct {
	TПорт
}

func (self *TПорт16bit) Init(portnumber uint16) {
	self.TПорт.portnumber = portnumber
}
func (self *TПорт16bit) Бичих(data uint16) {
	Портoutword(self.TПорт.portnumber, data)
}
func (self *TПорт16bit) Унших() uint16 {
	var result = Портinword(self.TПорт.portnumber)
	return result
}
func ПортБичихword(portnumber uint16, data uint16) {
	Портoutword(portnumber, data)
}
func ПортУншихword(portnumber uint16) uint16 {
	var result uint16 = Портinword(portnumber)
	return result
}

type TПорт32bit struct {
	TПорт
}

func (self *TПорт32bit) Init(portnumber uint16) {
	self.TПорт.portnumber = portnumber
}
func (self *TПорт32bit) Бичих(data uint32) {
	Портoutdword(self.TПорт.portnumber, data)
}
func (self *TПорт32bit) Унших() {
	Портindword(self.TПорт.portnumber)
}
func ПортБичихdword(portnumber uint16, data uint32) {
	Портoutdword(portnumber, data)
}
func ПортУншихdword(portnumber uint16) uint32 {
	var result uint32 = Портindword(portnumber)
	return result
}

var уншихcount uint16 = 65
var бичихcount uint16 = 66

func Портoutbyte(portnumber uint16, data uint8)
func Портinbyte(portnumber uint16) uint8

func Портoutword(portnumber uint16, data uint16)
func Портinword(portnumber uint16) uint16

func Портoutdword(portnumber uint16, data uint32)
func Портindword(portnumber uint16) uint32
