package vrata

var položaj uint16 = 1

type TVrata struct {
	portnumber uint16
}

type TVrata8bit struct {
	TVrata
	branjecount	uint16
	pisanjecount	uint16
}

func (sam *TVrata8bit) Init(portnumber uint16) {
	sam.portnumber = portnumber
	sam.branjecount = 65
	sam.pisanjecount = 65
}
func (sam *TVrata8bit) Pisanje(data uint8) {
	VrataIzhodnobyte(sam.portnumber, data)
}
func (sam *TVrata8bit) Branje() uint8 {
	var rEZULTAT = VrataVhodnobyte(sam.portnumber)
	return rEZULTAT
}
func VrataPisanjebyte(portnumber uint16, data uint8) {
	VrataIzhodnobyte(portnumber, data)
}
func VrataBranjebyte(portnumber uint16) uint8 {
	rEZULTAT := VrataVhodnobyte(portnumber)
	return rEZULTAT
}

type TVrata16bit struct {
	TVrata
}

func (sam *TVrata16bit) Init(portnumber uint16) {
	sam.TVrata.portnumber = portnumber
}
func (sam *TVrata16bit) Pisanje(data uint16) {
	VrataIzhodnobeseda(sam.TVrata.portnumber, data)
}
func (sam *TVrata16bit) Branje() uint16 {
	var rEZULTAT = VrataVhodnobeseda(sam.TVrata.portnumber)
	return rEZULTAT
}
func VrataPisanjebeseda(portnumber uint16, data uint16) {
	VrataIzhodnobeseda(portnumber, data)
}
func VrataBranjebeseda(portnumber uint16) uint16 {
	var rEZULTAT uint16 = VrataVhodnobeseda(portnumber)
	return rEZULTAT
}

type TVrata32bit struct {
	TVrata
}

func (sam *TVrata32bit) Init(portnumber uint16) {
	sam.TVrata.portnumber = portnumber
}
func (sam *TVrata32bit) Pisanje(data uint32) {
	VrataIzhodnodword(sam.TVrata.portnumber, data)
}
func (sam *TVrata32bit) Branje() {
	VrataVhodnodword(sam.TVrata.portnumber)
}
func VrataPisanjedword(portnumber uint16, data uint32) {
	VrataIzhodnodword(portnumber, data)
}
func VrataBranjedword(portnumber uint16) uint32 {
	var rEZULTAT uint32 = VrataVhodnodword(portnumber)
	return rEZULTAT
}

var branjecount uint16 = 65
var pisanjecount uint16 = 66

func VrataIzhodnobyte(portnumber uint16, data uint8)
func VrataVhodnobyte(portnumber uint16) uint8

func VrataIzhodnobeseda(portnumber uint16, data uint16)
func VrataVhodnobeseda(portnumber uint16) uint16

func VrataIzhodnodword(portnumber uint16, data uint32)
func VrataVhodnodword(portnumber uint16) uint32
