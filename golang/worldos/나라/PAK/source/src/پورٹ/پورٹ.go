/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package پورٹ

var position uint16 = 1

type Tپورٹ struct {
	portnumber uint16
}

type Tپورٹ8bit struct {
	Tپورٹ
	پڑھیںcount	uint16
	لکھیںcount	uint16
}

func (self *Tپورٹ8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.پڑھیںcount = 65
	self.لکھیںcount = 65
}
func (self *Tپورٹ8bit) Wلکھیں(data uint8) {
	Pپورٹباہرbyte(self.portnumber, data)
}
func (self *Tپورٹ8bit) Rپڑھیں() uint8 {
	var result = Pپورٹاندرbyte(self.portnumber)
	return result
}
func Pپورٹلکھیںbyte(portnumber uint16, data uint8) {
	Pپورٹباہرbyte(portnumber, data)
}
func Pپورٹپڑھیںbyte(portnumber uint16) uint8 {
	result := Pپورٹاندرbyte(portnumber)
	return result
}

type Tپورٹ16bit struct {
	Tپورٹ
}

func (self *Tپورٹ16bit) Init(portnumber uint16) {
	self.Tپورٹ.portnumber = portnumber
}
func (self *Tپورٹ16bit) Wلکھیں(data uint16) {
	Pپورٹباہرلفظ(self.Tپورٹ.portnumber, data)
}
func (self *Tپورٹ16bit) Rپڑھیں() uint16 {
	var result = Pپورٹاندرلفظ(self.Tپورٹ.portnumber)
	return result
}
func Pپورٹلکھیںلفظ(portnumber uint16, data uint16) {
	Pپورٹباہرلفظ(portnumber, data)
}
func Pپورٹپڑھیںلفظ(portnumber uint16) uint16 {
	var result uint16 = Pپورٹاندرلفظ(portnumber)
	return result
}

type Tپورٹ32bit struct {
	Tپورٹ
}

func (self *Tپورٹ32bit) Init(portnumber uint16) {
	self.Tپورٹ.portnumber = portnumber
}
func (self *Tپورٹ32bit) Wلکھیں(data uint32) {
	Pپورٹباہرdword(self.Tپورٹ.portnumber, data)
}
func (self *Tپورٹ32bit) Rپڑھیں() {
	Pپورٹاندرdword(self.Tپورٹ.portnumber)
}
func Pپورٹلکھیںdword(portnumber uint16, data uint32) {
	Pپورٹباہرdword(portnumber, data)
}
func Pپورٹپڑھیںdword(portnumber uint16) uint32 {
	var result uint32 = Pپورٹاندرdword(portnumber)
	return result
}

var پڑھیںcount uint16 = 65
var لکھیںcount uint16 = 66

func Pپورٹباہرbyte(portnumber uint16, data uint8)
func Pپورٹاندرbyte(portnumber uint16) uint8

func Pپورٹباہرلفظ(portnumber uint16, data uint16)
func Pپورٹاندرلفظ(portnumber uint16) uint16

func Pپورٹباہرdword(portnumber uint16, data uint32)
func Pپورٹاندرdword(portnumber uint16) uint32
