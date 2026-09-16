/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package portti

var sijainti uint16 = 1

type TPortti struct {
	portnumber uint16
}

type TPortti8bit struct {
	TPortti
	lukucount	uint16
	kirjoituscount	uint16
}

func (itse *TPortti8bit) Init(portnumber uint16) {
	itse.portnumber = portnumber
	itse.lukucount = 65
	itse.kirjoituscount = 65
}
func (itse *TPortti8bit) Kirjoitus(data uint8) {
	PorttiLähteväbyte(itse.portnumber, data)
}
func (itse *TPortti8bit) Luku() uint8 {
	var tULOS = PorttiSaapuvabyte(itse.portnumber)
	return tULOS
}
func PorttiKirjoitusbyte(portnumber uint16, data uint8) {
	PorttiLähteväbyte(portnumber, data)
}
func PorttiLukubyte(portnumber uint16) uint8 {
	tULOS := PorttiSaapuvabyte(portnumber)
	return tULOS
}

type TPortti16bit struct {
	TPortti
}

func (itse *TPortti16bit) Init(portnumber uint16) {
	itse.TPortti.portnumber = portnumber
}
func (itse *TPortti16bit) Kirjoitus(data uint16) {
	PorttiLähteväsana(itse.TPortti.portnumber, data)
}
func (itse *TPortti16bit) Luku() uint16 {
	var tULOS = PorttiSaapuvasana(itse.TPortti.portnumber)
	return tULOS
}
func PorttiKirjoitussana(portnumber uint16, data uint16) {
	PorttiLähteväsana(portnumber, data)
}
func PorttiLukusana(portnumber uint16) uint16 {
	var tULOS uint16 = PorttiSaapuvasana(portnumber)
	return tULOS
}

type TPortti32bit struct {
	TPortti
}

func (itse *TPortti32bit) Init(portnumber uint16) {
	itse.TPortti.portnumber = portnumber
}
func (itse *TPortti32bit) Kirjoitus(data uint32) {
	PorttiLähtevädword(itse.TPortti.portnumber, data)
}
func (itse *TPortti32bit) Luku() {
	PorttiSaapuvadword(itse.TPortti.portnumber)
}
func PorttiKirjoitusdword(portnumber uint16, data uint32) {
	PorttiLähtevädword(portnumber, data)
}
func PorttiLukudword(portnumber uint16) uint32 {
	var tULOS uint32 = PorttiSaapuvadword(portnumber)
	return tULOS
}

var lukucount uint16 = 65
var kirjoituscount uint16 = 66

func PorttiLähteväbyte(portnumber uint16, data uint8)
func PorttiSaapuvabyte(portnumber uint16) uint8

func PorttiLähteväsana(portnumber uint16, data uint16)
func PorttiSaapuvasana(portnumber uint16) uint16

func PorttiLähtevädword(portnumber uint16, data uint32)
func PorttiSaapuvadword(portnumber uint16) uint32
