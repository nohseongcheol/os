package θύρα

var θέση uint16 = 1

type TΘύρα struct {
	portnumber uint16
}

type TΘύρα8bit struct {
	TΘύρα
	ανάγνωσηcount	uint16
	εγγραφήcount	uint16
}

func (self *TΘύρα8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.ανάγνωσηcount = 65
	self.εγγραφήcount = 65
}
func (self *TΘύρα8bit) Εγγραφή(data uint8) {
	ΘύραΈξωbyte(self.portnumber, data)
}
func (self *TΘύρα8bit) Ανάγνωση() uint8 {
	var result = Θύρασεbyte(self.portnumber)
	return result
}
func ΘύραΕγγραφήbyte(portnumber uint16, data uint8) {
	ΘύραΈξωbyte(portnumber, data)
}
func ΘύραΑνάγνωσηbyte(portnumber uint16) uint8 {
	result := Θύρασεbyte(portnumber)
	return result
}

type TΘύρα16bit struct {
	TΘύρα
}

func (self *TΘύρα16bit) Init(portnumber uint16) {
	self.TΘύρα.portnumber = portnumber
}
func (self *TΘύρα16bit) Εγγραφή(data uint16) {
	ΘύραΈξωλέξη(self.TΘύρα.portnumber, data)
}
func (self *TΘύρα16bit) Ανάγνωση() uint16 {
	var result = Θύρασελέξη(self.TΘύρα.portnumber)
	return result
}
func ΘύραΕγγραφήλέξη(portnumber uint16, data uint16) {
	ΘύραΈξωλέξη(portnumber, data)
}
func ΘύραΑνάγνωσηλέξη(portnumber uint16) uint16 {
	var result uint16 = Θύρασελέξη(portnumber)
	return result
}

type TΘύρα32bit struct {
	TΘύρα
}

func (self *TΘύρα32bit) Init(portnumber uint16) {
	self.TΘύρα.portnumber = portnumber
}
func (self *TΘύρα32bit) Εγγραφή(data uint32) {
	ΘύραΈξωdword(self.TΘύρα.portnumber, data)
}
func (self *TΘύρα32bit) Ανάγνωση() {
	Θύρασεdword(self.TΘύρα.portnumber)
}
func ΘύραΕγγραφήdword(portnumber uint16, data uint32) {
	ΘύραΈξωdword(portnumber, data)
}
func ΘύραΑνάγνωσηdword(portnumber uint16) uint32 {
	var result uint32 = Θύρασεdword(portnumber)
	return result
}

var ανάγνωσηcount uint16 = 65
var εγγραφήcount uint16 = 66

func ΘύραΈξωbyte(portnumber uint16, data uint8)
func Θύρασεbyte(portnumber uint16) uint8

func ΘύραΈξωλέξη(portnumber uint16, data uint16)
func Θύρασελέξη(portnumber uint16) uint16

func ΘύραΈξωdword(portnumber uint16, data uint32)
func Θύρασεdword(portnumber uint16) uint32
