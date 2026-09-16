/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package umuyoboro

var position uint16 = 1

type TUmuyoboro struct {
	portnumber uint16
}

type TUmuyoboro8bit struct {
	TUmuyoboro
	gusomacount	uint16
	kwandikacount	uint16
}

func (self *TUmuyoboro8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.gusomacount = 65
	self.kwandikacount = 65
}
func (self *TUmuyoboro8bit) Kwandika(data uint8) {
	UmuyoboroInyumabyte(self.portnumber, data)
}
func (self *TUmuyoboro8bit) Gusoma() uint8 {
	var result = UmuyoboroImberebyte(self.portnumber)
	return result
}
func Umuyoborokwandikabyte(portnumber uint16, data uint8) {
	UmuyoboroInyumabyte(portnumber, data)
}
func Umuyoborogusomabyte(portnumber uint16) uint8 {
	result := UmuyoboroImberebyte(portnumber)
	return result
}

type TUmuyoboro16bit struct {
	TUmuyoboro
}

func (self *TUmuyoboro16bit) Init(portnumber uint16) {
	self.TUmuyoboro.portnumber = portnumber
}
func (self *TUmuyoboro16bit) Kwandika(data uint16) {
	UmuyoboroInyumaword(self.TUmuyoboro.portnumber, data)
}
func (self *TUmuyoboro16bit) Gusoma() uint16 {
	var result = UmuyoboroImbereword(self.TUmuyoboro.portnumber)
	return result
}
func Umuyoborokwandikaword(portnumber uint16, data uint16) {
	UmuyoboroInyumaword(portnumber, data)
}
func Umuyoborogusomaword(portnumber uint16) uint16 {
	var result uint16 = UmuyoboroImbereword(portnumber)
	return result
}

type TUmuyoboro32bit struct {
	TUmuyoboro
}

func (self *TUmuyoboro32bit) Init(portnumber uint16) {
	self.TUmuyoboro.portnumber = portnumber
}
func (self *TUmuyoboro32bit) Kwandika(data uint32) {
	UmuyoboroInyumadword(self.TUmuyoboro.portnumber, data)
}
func (self *TUmuyoboro32bit) Gusoma() {
	UmuyoboroImberedword(self.TUmuyoboro.portnumber)
}
func Umuyoborokwandikadword(portnumber uint16, data uint32) {
	UmuyoboroInyumadword(portnumber, data)
}
func Umuyoborogusomadword(portnumber uint16) uint32 {
	var result uint32 = UmuyoboroImberedword(portnumber)
	return result
}

var gusomacount uint16 = 65
var kwandikacount uint16 = 66

func UmuyoboroInyumabyte(portnumber uint16, data uint8)
func UmuyoboroImberebyte(portnumber uint16) uint8

func UmuyoboroInyumaword(portnumber uint16, data uint16)
func UmuyoboroImbereword(portnumber uint16) uint16

func UmuyoboroInyumadword(portnumber uint16, data uint32)
func UmuyoboroImberedword(portnumber uint16) uint32
