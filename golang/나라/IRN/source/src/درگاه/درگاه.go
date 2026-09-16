/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package درگاه

var position uint16 = 1

type Tدرگاه struct {
	portnumber uint16
}

type Tدرگاه8bit struct {
	Tدرگاه
	خواندنcount	uint16
	نوشتنcount	uint16
}

func (خود *Tدرگاه8bit) Init(portnumber uint16) {
	خود.portnumber = portnumber
	خود.خواندنcount = 65
	خود.نوشتنcount = 65
}
func (خود *Tدرگاه8bit) Wنوشتن(data uint8) {
	Pدرگاهخارجbyte(خود.portnumber, data)
}
func (خود *Tدرگاه8bit) Rخواندن() uint8 {
	var result = Pدرگاهداخلbyte(خود.portnumber)
	return result
}
func Pدرگاهنوشتنbyte(portnumber uint16, data uint8) {
	Pدرگاهخارجbyte(portnumber, data)
}
func Pدرگاهخواندنbyte(portnumber uint16) uint8 {
	result := Pدرگاهداخلbyte(portnumber)
	return result
}

type Tدرگاه16bit struct {
	Tدرگاه
}

func (خود *Tدرگاه16bit) Init(portnumber uint16) {
	خود.Tدرگاه.portnumber = portnumber
}
func (خود *Tدرگاه16bit) Wنوشتن(data uint16) {
	Pدرگاهخارجکلمه(خود.Tدرگاه.portnumber, data)
}
func (خود *Tدرگاه16bit) Rخواندن() uint16 {
	var result = Pدرگاهداخلکلمه(خود.Tدرگاه.portnumber)
	return result
}
func Pدرگاهنوشتنکلمه(portnumber uint16, data uint16) {
	Pدرگاهخارجکلمه(portnumber, data)
}
func Pدرگاهخواندنکلمه(portnumber uint16) uint16 {
	var result uint16 = Pدرگاهداخلکلمه(portnumber)
	return result
}

type Tدرگاه32bit struct {
	Tدرگاه
}

func (خود *Tدرگاه32bit) Init(portnumber uint16) {
	خود.Tدرگاه.portnumber = portnumber
}
func (خود *Tدرگاه32bit) Wنوشتن(data uint32) {
	Pدرگاهخارجdword(خود.Tدرگاه.portnumber, data)
}
func (خود *Tدرگاه32bit) Rخواندن() {
	Pدرگاهداخلdword(خود.Tدرگاه.portnumber)
}
func Pدرگاهنوشتنdword(portnumber uint16, data uint32) {
	Pدرگاهخارجdword(portnumber, data)
}
func Pدرگاهخواندنdword(portnumber uint16) uint32 {
	var result uint32 = Pدرگاهداخلdword(portnumber)
	return result
}

var خواندنcount uint16 = 65
var نوشتنcount uint16 = 66

func Pدرگاهخارجbyte(portnumber uint16, data uint8)
func Pدرگاهداخلbyte(portnumber uint16) uint8

func Pدرگاهخارجکلمه(portnumber uint16, data uint16)
func Pدرگاهداخلکلمه(portnumber uint16) uint16

func Pدرگاهخارجdword(portnumber uint16, data uint32)
func Pدرگاهداخلdword(portnumber uint16) uint32
