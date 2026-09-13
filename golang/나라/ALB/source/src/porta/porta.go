package porta

var pozicion uint16 = 1

type TPorta struct {
	portnumber uint16
}

type TPorta8bit struct {
	TPorta
	leximicount	uint16
	shkrimicount	uint16
}

func (vetvetja *TPorta8bit) Init(portnumber uint16) {
	vetvetja.portnumber = portnumber
	vetvetja.leximicount = 65
	vetvetja.shkrimicount = 65
}
func (vetvetja *TPorta8bit) Shkrimi(data uint8) {
	PortaZvogëlobyte(vetvetja.portnumber, data)
}
func (vetvetja *TPorta8bit) Leximi() uint8 {
	var result = PortaZmadhobyte(vetvetja.portnumber)
	return result
}
func PortaShkrimibyte(portnumber uint16, data uint8) {
	PortaZvogëlobyte(portnumber, data)
}
func PortaLeximibyte(portnumber uint16) uint8 {
	result := PortaZmadhobyte(portnumber)
	return result
}

type TPorta16bit struct {
	TPorta
}

func (vetvetja *TPorta16bit) Init(portnumber uint16) {
	vetvetja.TPorta.portnumber = portnumber
}
func (vetvetja *TPorta16bit) Shkrimi(data uint16) {
	PortaZvogëloFjalë(vetvetja.TPorta.portnumber, data)
}
func (vetvetja *TPorta16bit) Leximi() uint16 {
	var result = PortaZmadhoFjalë(vetvetja.TPorta.portnumber)
	return result
}
func PortaShkrimiFjalë(portnumber uint16, data uint16) {
	PortaZvogëloFjalë(portnumber, data)
}
func PortaLeximiFjalë(portnumber uint16) uint16 {
	var result uint16 = PortaZmadhoFjalë(portnumber)
	return result
}

type TPorta32bit struct {
	TPorta
}

func (vetvetja *TPorta32bit) Init(portnumber uint16) {
	vetvetja.TPorta.portnumber = portnumber
}
func (vetvetja *TPorta32bit) Shkrimi(data uint32) {
	PortaZvogëlodword(vetvetja.TPorta.portnumber, data)
}
func (vetvetja *TPorta32bit) Leximi() {
	PortaZmadhodword(vetvetja.TPorta.portnumber)
}
func PortaShkrimidword(portnumber uint16, data uint32) {
	PortaZvogëlodword(portnumber, data)
}
func PortaLeximidword(portnumber uint16) uint32 {
	var result uint32 = PortaZmadhodword(portnumber)
	return result
}

var leximicount uint16 = 65
var shkrimicount uint16 = 66

func PortaZvogëlobyte(portnumber uint16, data uint8)
func PortaZmadhobyte(portnumber uint16) uint8

func PortaZvogëloFjalë(portnumber uint16, data uint16)
func PortaZmadhoFjalë(portnumber uint16) uint16

func PortaZvogëlodword(portnumber uint16, data uint32)
func PortaZmadhodword(portnumber uint16) uint32
