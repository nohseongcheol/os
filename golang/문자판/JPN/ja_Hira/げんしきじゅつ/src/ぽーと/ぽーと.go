package ぽーと

var はいち uint16 = 1

type Tぽーと struct {
	portnumber uint16
}

type Tぽーと8bit struct {
	Tぽーと
	よみこみかうんと	uint16
	かきこみかうんと	uint16
}

func (self *Tぽーと8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.よみこみかうんと = 65
	self.かきこみかうんと = 65
}
func (self *Tぽーと8bit) Wかきこみ(でーた uint8) {
	Pぽーとそうしんばいと(self.portnumber, でーた)
}
func (self *Tぽーと8bit) Rよみこみ() uint8 {
	var せいせいさき = Pぽーとじゅしんばいと(self.portnumber)
	return せいせいさき
}
func Pぽーとかきこみばいと(portnumber uint16, でーた uint8) {
	Pぽーとそうしんばいと(portnumber, でーた)
}
func Pぽーとよみこみばいと(portnumber uint16) uint8 {
	せいせいさき := Pぽーとじゅしんばいと(portnumber)
	return せいせいさき
}

type Tぽーと16bit struct {
	Tぽーと
}

func (self *Tぽーと16bit) Init(portnumber uint16) {
	self.Tぽーと.portnumber = portnumber
}
func (self *Tぽーと16bit) Wかきこみ(でーた uint16) {
	Pぽーとそうしんご(self.Tぽーと.portnumber, でーた)
}
func (self *Tぽーと16bit) Rよみこみ() uint16 {
	var せいせいさき = Pぽーとじゅしんご(self.Tぽーと.portnumber)
	return せいせいさき
}
func Pぽーとかきこみご(portnumber uint16, でーた uint16) {
	Pぽーとそうしんご(portnumber, でーた)
}
func Pぽーとよみこみご(portnumber uint16) uint16 {
	var せいせいさき uint16 = Pぽーとじゅしんご(portnumber)
	return せいせいさき
}

type Tぽーと32bit struct {
	Tぽーと
}

func (self *Tぽーと32bit) Init(portnumber uint16) {
	self.Tぽーと.portnumber = portnumber
}
func (self *Tぽーと32bit) Wかきこみ(でーた uint32) {
	Pぽーとそうしんdword(self.Tぽーと.portnumber, でーた)
}
func (self *Tぽーと32bit) Rよみこみ() {
	Pぽーとじゅしんdword(self.Tぽーと.portnumber)
}
func Pぽーとかきこみdword(portnumber uint16, でーた uint32) {
	Pぽーとそうしんdword(portnumber, でーた)
}
func Pぽーとよみこみdword(portnumber uint16) uint32 {
	var せいせいさき uint32 = Pぽーとじゅしんdword(portnumber)
	return せいせいさき
}

var よみこみかうんと uint16 = 65
var かきこみかうんと uint16 = 66

func Pぽーとそうしんばいと(portnumber uint16, でーた uint8)
func Pぽーとじゅしんばいと(portnumber uint16) uint8

func Pぽーとそうしんご(portnumber uint16, でーた uint16)
func Pぽーとじゅしんご(portnumber uint16) uint16

func Pぽーとそうしんdword(portnumber uint16, でーた uint32)
func Pぽーとじゅしんdword(portnumber uint16) uint32
