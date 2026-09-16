/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package שער

var מיקום uint16 = 1

type Tשער struct {
	portnumber uint16
}

type Tשער8bit struct {
	Tשער
	קריאהcount	uint16
	כתיבהcount	uint16
}

func (self *Tשער8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.קריאהcount = 65
	self.כתיבהcount = 65
}
func (self *Tשער8bit) Wכתיבה(data uint8) {
	Pשעריוצאbyte(self.portnumber, data)
}
func (self *Tשער8bit) Rקריאה() uint8 {
	var result = Pשערנכנסbyte(self.portnumber)
	return result
}
func Pשערכתיבהbyte(portnumber uint16, data uint8) {
	Pשעריוצאbyte(portnumber, data)
}
func Pשערקריאהbyte(portnumber uint16) uint8 {
	result := Pשערנכנסbyte(portnumber)
	return result
}

type Tשער16bit struct {
	Tשער
}

func (self *Tשער16bit) Init(portnumber uint16) {
	self.Tשער.portnumber = portnumber
}
func (self *Tשער16bit) Wכתיבה(data uint16) {
	Pשעריוצאמילים(self.Tשער.portnumber, data)
}
func (self *Tשער16bit) Rקריאה() uint16 {
	var result = Pשערנכנסמילים(self.Tשער.portnumber)
	return result
}
func Pשערכתיבהמילים(portnumber uint16, data uint16) {
	Pשעריוצאמילים(portnumber, data)
}
func Pשערקריאהמילים(portnumber uint16) uint16 {
	var result uint16 = Pשערנכנסמילים(portnumber)
	return result
}

type Tשער32bit struct {
	Tשער
}

func (self *Tשער32bit) Init(portnumber uint16) {
	self.Tשער.portnumber = portnumber
}
func (self *Tשער32bit) Wכתיבה(data uint32) {
	Pשעריוצאdword(self.Tשער.portnumber, data)
}
func (self *Tשער32bit) Rקריאה() {
	Pשערנכנסdword(self.Tשער.portnumber)
}
func Pשערכתיבהdword(portnumber uint16, data uint32) {
	Pשעריוצאdword(portnumber, data)
}
func Pשערקריאהdword(portnumber uint16) uint32 {
	var result uint32 = Pשערנכנסdword(portnumber)
	return result
}

var קריאהcount uint16 = 65
var כתיבהcount uint16 = 66

func Pשעריוצאbyte(portnumber uint16, data uint8)
func Pשערנכנסbyte(portnumber uint16) uint8

func Pשעריוצאמילים(portnumber uint16, data uint16)
func Pשערנכנסמילים(portnumber uint16) uint16

func Pשעריוצאdword(portnumber uint16, data uint32)
func Pשערנכנסdword(portnumber uint16) uint32
