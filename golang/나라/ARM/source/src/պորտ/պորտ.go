/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package պորտ

var դիրք uint16 = 1

type TՊորտ struct {
	portnumber uint16
}

type TՊորտ8bit struct {
	TՊորտ
	ընթերցումcount	uint16
	գրելcount	uint16
}

func (ինքնուրույն *TՊորտ8bit) Init(portnumber uint16) {
	ինքնուրույն.portnumber = portnumber
	ինքնուրույն.ընթերցումcount = 65
	ինքնուրույն.գրելcount = 65
}
func (ինքնուրույն *TՊորտ8bit) Գրել(data uint8) {
	ՊորտԴուրսbyte(ինքնուրույն.portnumber, data)
}
func (ինքնուրույն *TՊորտ8bit) Ընթերցում() uint8 {
	var result = ՊորտՄեջbyte(ինքնուրույն.portnumber)
	return result
}
func ՊորտԳրելbyte(portnumber uint16, data uint8) {
	ՊորտԴուրսbyte(portnumber, data)
}
func ՊորտԸնթերցումbyte(portnumber uint16) uint8 {
	result := ՊորտՄեջbyte(portnumber)
	return result
}

type TՊորտ16bit struct {
	TՊորտ
}

func (ինքնուրույն *TՊորտ16bit) Init(portnumber uint16) {
	ինքնուրույն.TՊորտ.portnumber = portnumber
}
func (ինքնուրույն *TՊորտ16bit) Գրել(data uint16) {
	ՊորտԴուրսբառ(ինքնուրույն.TՊորտ.portnumber, data)
}
func (ինքնուրույն *TՊորտ16bit) Ընթերցում() uint16 {
	var result = ՊորտՄեջբառ(ինքնուրույն.TՊորտ.portnumber)
	return result
}
func ՊորտԳրելբառ(portnumber uint16, data uint16) {
	ՊորտԴուրսբառ(portnumber, data)
}
func ՊորտԸնթերցումբառ(portnumber uint16) uint16 {
	var result uint16 = ՊորտՄեջբառ(portnumber)
	return result
}

type TՊորտ32bit struct {
	TՊորտ
}

func (ինքնուրույն *TՊորտ32bit) Init(portnumber uint16) {
	ինքնուրույն.TՊորտ.portnumber = portnumber
}
func (ինքնուրույն *TՊորտ32bit) Գրել(data uint32) {
	ՊորտԴուրսdword(ինքնուրույն.TՊորտ.portnumber, data)
}
func (ինքնուրույն *TՊորտ32bit) Ընթերցում() {
	ՊորտՄեջdword(ինքնուրույն.TՊորտ.portnumber)
}
func ՊորտԳրելdword(portnumber uint16, data uint32) {
	ՊորտԴուրսdword(portnumber, data)
}
func ՊորտԸնթերցումdword(portnumber uint16) uint32 {
	var result uint32 = ՊորտՄեջdword(portnumber)
	return result
}

var ընթերցումcount uint16 = 65
var գրելcount uint16 = 66

func ՊորտԴուրսbyte(portnumber uint16, data uint8)
func ՊորտՄեջbyte(portnumber uint16) uint8

func ՊորտԴուրսբառ(portnumber uint16, data uint16)
func ՊորտՄեջբառ(portnumber uint16) uint16

func ՊորտԴուրսdword(portnumber uint16, data uint32)
func ՊորտՄեջdword(portnumber uint16) uint32
