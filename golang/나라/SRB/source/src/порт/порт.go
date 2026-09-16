/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package порт

var положај uint16 = 1

type TПорт struct {
	portnumber uint16
}

type TПорт8bit struct {
	TПорт
	читањеcount	uint16
	пишеcount	uint16
}

func (исти *TПорт8bit) Init(portnumber uint16) {
	исти.portnumber = portnumber
	исти.читањеcount = 65
	исти.пишеcount = 65
}
func (исти *TПорт8bit) Пише(data uint8) {
	ПортПослатоbyte(исти.portnumber, data)
}
func (исти *TПорт8bit) Читање() uint8 {
	var иСХОД = ПортПримљеноbyte(исти.portnumber)
	return иСХОД
}
func ПортПишеbyte(portnumber uint16, data uint8) {
	ПортПослатоbyte(portnumber, data)
}
func Портчитањеbyte(portnumber uint16) uint8 {
	иСХОД := ПортПримљеноbyte(portnumber)
	return иСХОД
}

type TПорт16bit struct {
	TПорт
}

func (исти *TПорт16bit) Init(portnumber uint16) {
	исти.TПорт.portnumber = portnumber
}
func (исти *TПорт16bit) Пише(data uint16) {
	ПортПослатореч(исти.TПорт.portnumber, data)
}
func (исти *TПорт16bit) Читање() uint16 {
	var иСХОД = ПортПримљенореч(исти.TПорт.portnumber)
	return иСХОД
}
func ПортПишереч(portnumber uint16, data uint16) {
	ПортПослатореч(portnumber, data)
}
func Портчитањереч(portnumber uint16) uint16 {
	var иСХОД uint16 = ПортПримљенореч(portnumber)
	return иСХОД
}

type TПорт32bit struct {
	TПорт
}

func (исти *TПорт32bit) Init(portnumber uint16) {
	исти.TПорт.portnumber = portnumber
}
func (исти *TПорт32bit) Пише(data uint32) {
	ПортПослатоdword(исти.TПорт.portnumber, data)
}
func (исти *TПорт32bit) Читање() {
	ПортПримљеноdword(исти.TПорт.portnumber)
}
func ПортПишеdword(portnumber uint16, data uint32) {
	ПортПослатоdword(portnumber, data)
}
func Портчитањеdword(portnumber uint16) uint32 {
	var иСХОД uint32 = ПортПримљеноdword(portnumber)
	return иСХОД
}

var читањеcount uint16 = 65
var пишеcount uint16 = 66

func ПортПослатоbyte(portnumber uint16, data uint8)
func ПортПримљеноbyte(portnumber uint16) uint8

func ПортПослатореч(portnumber uint16, data uint16)
func ПортПримљенореч(portnumber uint16) uint16

func ПортПослатоdword(portnumber uint16, data uint32)
func ПортПримљеноdword(portnumber uint16) uint32
