/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package порта

var позиција uint16 = 1

type TПорта struct {
	portnumber uint16
}

type TПорта8bit struct {
	TПорта
	читајcount	uint16
	запишиcount	uint16
}

func (само *TПорта8bit) Init(portnumber uint16) {
	само.portnumber = portnumber
	само.читајcount = 65
	само.запишиcount = 65
}
func (само *TПорта8bit) Запиши(data uint8) {
	ПортаНамалиbyte(само.portnumber, data)
}
func (само *TПорта8bit) Читај() uint8 {
	var result = Портавоbyte(само.portnumber)
	return result
}
func ПортаЗапишиbyte(portnumber uint16, data uint8) {
	ПортаНамалиbyte(portnumber, data)
}
func ПортаЧитајbyte(portnumber uint16) uint8 {
	result := Портавоbyte(portnumber)
	return result
}

type TПорта16bit struct {
	TПорта
}

func (само *TПорта16bit) Init(portnumber uint16) {
	само.TПорта.portnumber = portnumber
}
func (само *TПорта16bit) Запиши(data uint16) {
	ПортаНамализбор(само.TПорта.portnumber, data)
}
func (само *TПорта16bit) Читај() uint16 {
	var result = Портавозбор(само.TПорта.portnumber)
	return result
}
func ПортаЗапишизбор(portnumber uint16, data uint16) {
	ПортаНамализбор(portnumber, data)
}
func ПортаЧитајзбор(portnumber uint16) uint16 {
	var result uint16 = Портавозбор(portnumber)
	return result
}

type TПорта32bit struct {
	TПорта
}

func (само *TПорта32bit) Init(portnumber uint16) {
	само.TПорта.portnumber = portnumber
}
func (само *TПорта32bit) Запиши(data uint32) {
	ПортаНамалиdword(само.TПорта.portnumber, data)
}
func (само *TПорта32bit) Читај() {
	Портавоdword(само.TПорта.portnumber)
}
func ПортаЗапишиdword(portnumber uint16, data uint32) {
	ПортаНамалиdword(portnumber, data)
}
func ПортаЧитајdword(portnumber uint16) uint32 {
	var result uint32 = Портавоdword(portnumber)
	return result
}

var читајcount uint16 = 65
var запишиcount uint16 = 66

func ПортаНамалиbyte(portnumber uint16, data uint8)
func Портавоbyte(portnumber uint16) uint8

func ПортаНамализбор(portnumber uint16, data uint16)
func Портавозбор(portnumber uint16) uint16

func ПортаНамалиdword(portnumber uint16, data uint32)
func Портавоdword(portnumber uint16) uint32
