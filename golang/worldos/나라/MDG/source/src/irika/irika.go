/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package irika

var position uint16 = 1

type TIrika struct {
	portnumber uint16
}

type TIrika8bit struct {
	TIrika
	mamakycount	uint16
	manoratracount	uint16
}

func (nytena *TIrika8bit) Init(portnumber uint16) {
	nytena.portnumber = portnumber
	nytena.mamakycount = 65
	nytena.manoratracount = 65
}
func (nytena *TIrika8bit) Manoratra(data uint8) {
	IrikaIvelanybyte(nytena.portnumber, data)
}
func (nytena *TIrika8bit) Mamaky() uint8 {
	var result = IrikaAnatybyte(nytena.portnumber)
	return result
}
func IrikaManoratrabyte(portnumber uint16, data uint8) {
	IrikaIvelanybyte(portnumber, data)
}
func IrikaMamakybyte(portnumber uint16) uint8 {
	result := IrikaAnatybyte(portnumber)
	return result
}

type TIrika16bit struct {
	TIrika
}

func (nytena *TIrika16bit) Init(portnumber uint16) {
	nytena.TIrika.portnumber = portnumber
}
func (nytena *TIrika16bit) Manoratra(data uint16) {
	IrikaIvelanyteny(nytena.TIrika.portnumber, data)
}
func (nytena *TIrika16bit) Mamaky() uint16 {
	var result = IrikaAnatyteny(nytena.TIrika.portnumber)
	return result
}
func IrikaManoratrateny(portnumber uint16, data uint16) {
	IrikaIvelanyteny(portnumber, data)
}
func IrikaMamakyteny(portnumber uint16) uint16 {
	var result uint16 = IrikaAnatyteny(portnumber)
	return result
}

type TIrika32bit struct {
	TIrika
}

func (nytena *TIrika32bit) Init(portnumber uint16) {
	nytena.TIrika.portnumber = portnumber
}
func (nytena *TIrika32bit) Manoratra(data uint32) {
	IrikaIvelanydword(nytena.TIrika.portnumber, data)
}
func (nytena *TIrika32bit) Mamaky() {
	IrikaAnatydword(nytena.TIrika.portnumber)
}
func IrikaManoratradword(portnumber uint16, data uint32) {
	IrikaIvelanydword(portnumber, data)
}
func IrikaMamakydword(portnumber uint16) uint32 {
	var result uint32 = IrikaAnatydword(portnumber)
	return result
}

var mamakycount uint16 = 65
var manoratracount uint16 = 66

func IrikaIvelanybyte(portnumber uint16, data uint8)
func IrikaAnatybyte(portnumber uint16) uint8

func IrikaIvelanyteny(portnumber uint16, data uint16)
func IrikaAnatyteny(portnumber uint16) uint16

func IrikaIvelanydword(portnumber uint16, data uint32)
func IrikaAnatydword(portnumber uint16) uint32
