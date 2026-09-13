package port

var položaj uint16 = 1

type TPort struct {
	portnumber uint16
}

type TPort8bit struct {
	TPort
	čitanjecount	uint16
	pišecount	uint16
}

func (isti *TPort8bit) Init(portnumber uint16) {
	isti.portnumber = portnumber
	isti.čitanjecount = 65
	isti.pišecount = 65
}
func (isti *TPort8bit) Piše(data uint8) {
	PortPoslatobyte(isti.portnumber, data)
}
func (isti *TPort8bit) Čitanje() uint8 {
	var iSHOD = PortPrimljenobyte(isti.portnumber)
	return iSHOD
}
func PortPišebyte(portnumber uint16, data uint8) {
	PortPoslatobyte(portnumber, data)
}
func Portčitanjebyte(portnumber uint16) uint8 {
	iSHOD := PortPrimljenobyte(portnumber)
	return iSHOD
}

type TPort16bit struct {
	TPort
}

func (isti *TPort16bit) Init(portnumber uint16) {
	isti.TPort.portnumber = portnumber
}
func (isti *TPort16bit) Piše(data uint16) {
	PortPoslatoreč(isti.TPort.portnumber, data)
}
func (isti *TPort16bit) Čitanje() uint16 {
	var iSHOD = PortPrimljenoreč(isti.TPort.portnumber)
	return iSHOD
}
func PortPišereč(portnumber uint16, data uint16) {
	PortPoslatoreč(portnumber, data)
}
func Portčitanjereč(portnumber uint16) uint16 {
	var iSHOD uint16 = PortPrimljenoreč(portnumber)
	return iSHOD
}

type TPort32bit struct {
	TPort
}

func (isti *TPort32bit) Init(portnumber uint16) {
	isti.TPort.portnumber = portnumber
}
func (isti *TPort32bit) Piše(data uint32) {
	PortPoslatodword(isti.TPort.portnumber, data)
}
func (isti *TPort32bit) Čitanje() {
	PortPrimljenodword(isti.TPort.portnumber)
}
func PortPišedword(portnumber uint16, data uint32) {
	PortPoslatodword(portnumber, data)
}
func Portčitanjedword(portnumber uint16) uint32 {
	var iSHOD uint32 = PortPrimljenodword(portnumber)
	return iSHOD
}

var čitanjecount uint16 = 65
var pišecount uint16 = 66

func PortPoslatobyte(portnumber uint16, data uint8)
func PortPrimljenobyte(portnumber uint16) uint8

func PortPoslatoreč(portnumber uint16, data uint16)
func PortPrimljenoreč(portnumber uint16) uint16

func PortPoslatodword(portnumber uint16, data uint32)
func PortPrimljenodword(portnumber uint16) uint32
