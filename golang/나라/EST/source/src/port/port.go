package port

var asukoht uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8biti struct {
	TPort
	lugeminecount		uint16
	kirjutaminecount	uint16
}

func (ise *TPort8biti) Init(portnumber uint16) {
	ise.portnumber = portnumber
	ise.lugeminecount = 65
	ise.kirjutaminecount = 65
}
func (ise *TPort8biti) Kirjutamine(data uint8) {
	PortVäljabyte(ise.portnumber, data)
}
func (ise *TPort8biti) Lugemine() uint8 {
	var tULEMUS = PortSissebyte(ise.portnumber)
	return tULEMUS
}
func PortKirjutaminebyte(portnumber uint16, data uint8) {
	PortVäljabyte(portnumber, data)
}
func PortLugeminebyte(portnumber uint16) uint8 {
	tULEMUS := PortSissebyte(portnumber)
	return tULEMUS
}

type TPort16biti struct {
	TPort
}

func (ise *TPort16biti) Init(portnumber uint16) {
	ise.TPort.portnumber = portnumber
}
func (ise *TPort16biti) Kirjutamine(data uint16) {
	PortVäljasõna(ise.TPort.portnumber, data)
}
func (ise *TPort16biti) Lugemine() uint16 {
	var tULEMUS = PortSissesõna(ise.TPort.portnumber)
	return tULEMUS
}
func PortKirjutaminesõna(portnumber uint16, data uint16) {
	PortVäljasõna(portnumber, data)
}
func PortLugeminesõna(portnumber uint16) uint16 {
	var tULEMUS uint16 = PortSissesõna(portnumber)
	return tULEMUS
}

type TPort32biti struct {
	TPort
}

func (ise *TPort32biti) Init(portnumber uint16) {
	ise.TPort.portnumber = portnumber
}
func (ise *TPort32biti) Kirjutamine(data uint32) {
	PortVäljadword(ise.TPort.portnumber, data)
}
func (ise *TPort32biti) Lugemine() {
	PortSissedword(ise.TPort.portnumber)
}
func PortKirjutaminedword(portnumber uint16, data uint32) {
	PortVäljadword(portnumber, data)
}
func PortLugeminedword(portnumber uint16) uint32 {
	var tULEMUS uint32 = PortSissedword(portnumber)
	return tULEMUS
}

var lugeminecount uint16 = 65
var kirjutaminecount uint16 = 66

func PortVäljabyte(portnumber uint16, data uint8)
func PortSissebyte(portnumber uint16) uint8

func PortVäljasõna(portnumber uint16, data uint16)
func PortSissesõna(portnumber uint16) uint16

func PortVäljadword(portnumber uint16, data uint32)
func PortSissedword(portnumber uint16) uint32
