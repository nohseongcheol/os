/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package poort

var positie uint16 = 1

type TPoort struct {
	portnumber uint16
}

type TPoort8bit struct {
	TPoort
	lezenAantal	uint16
	schrijvenAantal	uint16
}

func (zelf *TPoort8bit) Init(portnumber uint16) {
	zelf.portnumber = portnumber
	zelf.lezenAantal = 65
	zelf.schrijvenAantal = 65
}
func (zelf *TPoort8bit) Schrijven(data uint8) {
	PoortUitbyte(zelf.portnumber, data)
}
func (zelf *TPoort8bit) Lezen() uint8 {
	var rESULTAAT = Poortinbyte(zelf.portnumber)
	return rESULTAAT
}
func PoortSchrijvenbyte(portnumber uint16, data uint8) {
	PoortUitbyte(portnumber, data)
}
func PoortLezenbyte(portnumber uint16) uint8 {
	rESULTAAT := Poortinbyte(portnumber)
	return rESULTAAT
}

type TPoort16bit struct {
	TPoort
}

func (zelf *TPoort16bit) Init(portnumber uint16) {
	zelf.TPoort.portnumber = portnumber
}
func (zelf *TPoort16bit) Schrijven(data uint16) {
	PoortUitWoord(zelf.TPoort.portnumber, data)
}
func (zelf *TPoort16bit) Lezen() uint16 {
	var rESULTAAT = PoortinWoord(zelf.TPoort.portnumber)
	return rESULTAAT
}
func PoortSchrijvenWoord(portnumber uint16, data uint16) {
	PoortUitWoord(portnumber, data)
}
func PoortLezenWoord(portnumber uint16) uint16 {
	var rESULTAAT uint16 = PoortinWoord(portnumber)
	return rESULTAAT
}

type TPoort32bit struct {
	TPoort
}

func (zelf *TPoort32bit) Init(portnumber uint16) {
	zelf.TPoort.portnumber = portnumber
}
func (zelf *TPoort32bit) Schrijven(data uint32) {
	PoortUitdword(zelf.TPoort.portnumber, data)
}
func (zelf *TPoort32bit) Lezen() {
	Poortindword(zelf.TPoort.portnumber)
}
func PoortSchrijvendword(portnumber uint16, data uint32) {
	PoortUitdword(portnumber, data)
}
func PoortLezendword(portnumber uint16) uint32 {
	var rESULTAAT uint32 = Poortindword(portnumber)
	return rESULTAAT
}

var lezenAantal uint16 = 65
var schrijvenAantal uint16 = 66

func PoortUitbyte(portnumber uint16, data uint8)
func Poortinbyte(portnumber uint16) uint8

func PoortUitWoord(portnumber uint16, data uint16)
func PoortinWoord(portnumber uint16) uint16

func PoortUitdword(portnumber uint16, data uint32)
func Poortindword(portnumber uint16) uint32
