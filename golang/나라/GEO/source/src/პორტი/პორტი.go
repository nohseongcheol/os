/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package პორტი

var position uint16 = 1

type Tპორტი struct {
	portnumber uint16
}

type Tპორტი8bit struct {
	Tპორტი
	კითხვაcount	uint16
	ჩაწერაcount	uint16
}

func (self *Tპორტი8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.კითხვაcount = 65
	self.ჩაწერაcount = 65
}
func (self *Tპორტი8bit) Wჩაწერა(data uint8) {
	Pპორტიდაპატარავებაbyte(self.portnumber, data)
}
func (self *Tპორტი8bit) Rკითხვა() uint8 {
	var result = Pპორტიგადიდებაbyte(self.portnumber)
	return result
}
func Pპორტიჩაწერაbyte(portnumber uint16, data uint8) {
	Pპორტიდაპატარავებაbyte(portnumber, data)
}
func Pპორტიკითხვაbyte(portnumber uint16) uint8 {
	result := Pპორტიგადიდებაbyte(portnumber)
	return result
}

type Tპორტი16bit struct {
	Tპორტი
}

func (self *Tპორტი16bit) Init(portnumber uint16) {
	self.Tპორტი.portnumber = portnumber
}
func (self *Tპორტი16bit) Wჩაწერა(data uint16) {
	Pპორტიდაპატარავებასიტყვა(self.Tპორტი.portnumber, data)
}
func (self *Tპორტი16bit) Rკითხვა() uint16 {
	var result = Pპორტიგადიდებასიტყვა(self.Tპორტი.portnumber)
	return result
}
func Pპორტიჩაწერასიტყვა(portnumber uint16, data uint16) {
	Pპორტიდაპატარავებასიტყვა(portnumber, data)
}
func Pპორტიკითხვასიტყვა(portnumber uint16) uint16 {
	var result uint16 = Pპორტიგადიდებასიტყვა(portnumber)
	return result
}

type Tპორტი32bit struct {
	Tპორტი
}

func (self *Tპორტი32bit) Init(portnumber uint16) {
	self.Tპორტი.portnumber = portnumber
}
func (self *Tპორტი32bit) Wჩაწერა(data uint32) {
	Pპორტიდაპატარავებაdword(self.Tპორტი.portnumber, data)
}
func (self *Tპორტი32bit) Rკითხვა() {
	Pპორტიგადიდებაdword(self.Tპორტი.portnumber)
}
func Pპორტიჩაწერაdword(portnumber uint16, data uint32) {
	Pპორტიდაპატარავებაdword(portnumber, data)
}
func Pპორტიკითხვაdword(portnumber uint16) uint32 {
	var result uint32 = Pპორტიგადიდებაdword(portnumber)
	return result
}

var კითხვაcount uint16 = 65
var ჩაწერაcount uint16 = 66

func Pპორტიდაპატარავებაbyte(portnumber uint16, data uint8)
func Pპორტიგადიდებაbyte(portnumber uint16) uint8

func Pპორტიდაპატარავებასიტყვა(portnumber uint16, data uint16)
func Pპორტიგადიდებასიტყვა(portnumber uint16) uint16

func Pპორტიდაპატარავებაdword(portnumber uint16, data uint32)
func Pპორტიგადიდებაdword(portnumber uint16) uint32
