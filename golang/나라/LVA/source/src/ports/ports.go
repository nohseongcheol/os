package ports

var novietojums uint16 = 1

type TPorts struct {
	portnumber uint16
}

type TPorts8bit struct {
	TPorts
	lasītcount	uint16
	rakstītcount	uint16
}

func (pats *TPorts8bit) Init(portnumber uint16) {
	pats.portnumber = portnumber
	pats.lasītcount = 65
	pats.rakstītcount = 65
}
func (pats *TPorts8bit) Rakstīt(data uint8) {
	PortsIzejošābyte(pats.portnumber, data)
}
func (pats *TPorts8bit) Lasīt() uint8 {
	var result = PortsIenākošābyte(pats.portnumber)
	return result
}
func PortsRakstītbyte(portnumber uint16, data uint8) {
	PortsIzejošābyte(portnumber, data)
}
func PortsLasītbyte(portnumber uint16) uint8 {
	result := PortsIenākošābyte(portnumber)
	return result
}

type TPorts16bit struct {
	TPorts
}

func (pats *TPorts16bit) Init(portnumber uint16) {
	pats.TPorts.portnumber = portnumber
}
func (pats *TPorts16bit) Rakstīt(data uint16) {
	PortsIzejošāvārds(pats.TPorts.portnumber, data)
}
func (pats *TPorts16bit) Lasīt() uint16 {
	var result = PortsIenākošāvārds(pats.TPorts.portnumber)
	return result
}
func PortsRakstītvārds(portnumber uint16, data uint16) {
	PortsIzejošāvārds(portnumber, data)
}
func PortsLasītvārds(portnumber uint16) uint16 {
	var result uint16 = PortsIenākošāvārds(portnumber)
	return result
}

type TPorts32bit struct {
	TPorts
}

func (pats *TPorts32bit) Init(portnumber uint16) {
	pats.TPorts.portnumber = portnumber
}
func (pats *TPorts32bit) Rakstīt(data uint32) {
	PortsIzejošādword(pats.TPorts.portnumber, data)
}
func (pats *TPorts32bit) Lasīt() {
	PortsIenākošādword(pats.TPorts.portnumber)
}
func PortsRakstītdword(portnumber uint16, data uint32) {
	PortsIzejošādword(portnumber, data)
}
func PortsLasītdword(portnumber uint16) uint32 {
	var result uint32 = PortsIenākošādword(portnumber)
	return result
}

var lasītcount uint16 = 65
var rakstītcount uint16 = 66

func PortsIzejošābyte(portnumber uint16, data uint8)
func PortsIenākošābyte(portnumber uint16) uint8

func PortsIzejošāvārds(portnumber uint16, data uint16)
func PortsIenākošāvārds(portnumber uint16) uint16

func PortsIzejošādword(portnumber uint16, data uint32)
func PortsIenākošādword(portnumber uint16) uint32
