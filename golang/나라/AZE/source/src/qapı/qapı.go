package qapı

var position uint16 = 1

type TQapı struct {
	portnumber uint16
}

type TQapı8bit struct {
	TQapı
	oxumacount	uint16
	yazmacount	uint16
}

func (self *TQapı8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.oxumacount = 65
	self.yazmacount = 65
}
func (self *TQapı8bit) Yazma(data uint8) {
	Qapıoutbyte(self.portnumber, data)
}
func (self *TQapı8bit) Oxuma() uint8 {
	var result = Qapıinbyte(self.portnumber)
	return result
}
func QapıYazmabyte(portnumber uint16, data uint8) {
	Qapıoutbyte(portnumber, data)
}
func QapıOxumabyte(portnumber uint16) uint8 {
	result := Qapıinbyte(portnumber)
	return result
}

type TQapı16bit struct {
	TQapı
}

func (self *TQapı16bit) Init(portnumber uint16) {
	self.TQapı.portnumber = portnumber
}
func (self *TQapı16bit) Yazma(data uint16) {
	Qapıoutword(self.TQapı.portnumber, data)
}
func (self *TQapı16bit) Oxuma() uint16 {
	var result = Qapıinword(self.TQapı.portnumber)
	return result
}
func QapıYazmaword(portnumber uint16, data uint16) {
	Qapıoutword(portnumber, data)
}
func QapıOxumaword(portnumber uint16) uint16 {
	var result uint16 = Qapıinword(portnumber)
	return result
}

type TQapı32bit struct {
	TQapı
}

func (self *TQapı32bit) Init(portnumber uint16) {
	self.TQapı.portnumber = portnumber
}
func (self *TQapı32bit) Yazma(data uint32) {
	Qapıoutdword(self.TQapı.portnumber, data)
}
func (self *TQapı32bit) Oxuma() {
	Qapıindword(self.TQapı.portnumber)
}
func QapıYazmadword(portnumber uint16, data uint32) {
	Qapıoutdword(portnumber, data)
}
func QapıOxumadword(portnumber uint16) uint32 {
	var result uint32 = Qapıindword(portnumber)
	return result
}

var oxumacount uint16 = 65
var yazmacount uint16 = 66

func Qapıoutbyte(portnumber uint16, data uint8)
func Qapıinbyte(portnumber uint16) uint8

func Qapıoutword(portnumber uint16, data uint16)
func Qapıinword(portnumber uint16) uint16

func Qapıoutdword(portnumber uint16, data uint32)
func Qapıindword(portnumber uint16) uint32
