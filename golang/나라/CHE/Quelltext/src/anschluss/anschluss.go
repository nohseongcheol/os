/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package anschluss

var position uint16 = 1

type TAnschluss struct {
	portnumber uint16
}

type TAnschluss8bit struct {
	TAnschluss
	lesenAnzahl	uint16
	schreibenAnzahl	uint16
}

func (selbst *TAnschluss8bit) Init(portnumber uint16) {
	selbst.portnumber = portnumber
	selbst.lesenAnzahl = 65
	selbst.schreibenAnzahl = 65
}
func (selbst *TAnschluss8bit) Schreiben(daten uint8) {
	AnschlussAusByte(selbst.portnumber, daten)
}
func (selbst *TAnschluss8bit) Lesen() uint8 {
	var ergebnis = AnschlussEinByte(selbst.portnumber)
	return ergebnis
}
func AnschlussSchreibenByte(portnumber uint16, daten uint8) {
	AnschlussAusByte(portnumber, daten)
}
func AnschlussLesenByte(portnumber uint16) uint8 {
	ergebnis := AnschlussEinByte(portnumber)
	return ergebnis
}

type TAnschluss16bit struct {
	TAnschluss
}

func (selbst *TAnschluss16bit) Init(portnumber uint16) {
	selbst.TAnschluss.portnumber = portnumber
}
func (selbst *TAnschluss16bit) Schreiben(daten uint16) {
	AnschlussAusWort(selbst.TAnschluss.portnumber, daten)
}
func (selbst *TAnschluss16bit) Lesen() uint16 {
	var ergebnis = AnschlussEinWort(selbst.TAnschluss.portnumber)
	return ergebnis
}
func AnschlussSchreibenWort(portnumber uint16, daten uint16) {
	AnschlussAusWort(portnumber, daten)
}
func AnschlussLesenWort(portnumber uint16) uint16 {
	var ergebnis uint16 = AnschlussEinWort(portnumber)
	return ergebnis
}

type TAnschluss32bit struct {
	TAnschluss
}

func (selbst *TAnschluss32bit) Init(portnumber uint16) {
	selbst.TAnschluss.portnumber = portnumber
}
func (selbst *TAnschluss32bit) Schreiben(daten uint32) {
	AnschlussAusdword(selbst.TAnschluss.portnumber, daten)
}
func (selbst *TAnschluss32bit) Lesen() {
	AnschlussEindword(selbst.TAnschluss.portnumber)
}
func AnschlussSchreibendword(portnumber uint16, daten uint32) {
	AnschlussAusdword(portnumber, daten)
}
func AnschlussLesendword(portnumber uint16) uint32 {
	var ergebnis uint32 = AnschlussEindword(portnumber)
	return ergebnis
}

var lesenAnzahl uint16 = 65
var schreibenAnzahl uint16 = 66

func AnschlussAusByte(portnumber uint16, daten uint8)
func AnschlussEinByte(portnumber uint16) uint8

func AnschlussAusWort(portnumber uint16, daten uint16)
func AnschlussEinWort(portnumber uint16) uint16

func AnschlussAusdword(portnumber uint16, daten uint32)
func AnschlussEindword(portnumber uint16) uint32
