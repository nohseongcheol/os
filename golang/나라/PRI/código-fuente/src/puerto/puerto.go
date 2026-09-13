package puerto

var posición uint16 = 1

type TPuerto struct {
	portnumber uint16
}

type TPuerto8bit struct {
	TPuerto
	leerRecuento		uint16
	escribirRecuento	uint16
}

func (propio *TPuerto8bit) Init(portnumber uint16) {
	propio.portnumber = portnumber
	propio.leerRecuento = 65
	propio.escribirRecuento = 65
}
func (propio *TPuerto8bit) Escribir(datos uint8) {
	PuertoSalidaocteto(propio.portnumber, datos)
}
func (propio *TPuerto8bit) Leer() uint8 {
	var rESULTADO = PuertoEntradaocteto(propio.portnumber)
	return rESULTADO
}
func Puertoescribirocteto(portnumber uint16, datos uint8) {
	PuertoSalidaocteto(portnumber, datos)
}
func Puertoleerocteto(portnumber uint16) uint8 {
	rESULTADO := PuertoEntradaocteto(portnumber)
	return rESULTADO
}

type TPuerto16bit struct {
	TPuerto
}

func (propio *TPuerto16bit) Init(portnumber uint16) {
	propio.TPuerto.portnumber = portnumber
}
func (propio *TPuerto16bit) Escribir(datos uint16) {
	PuertoSalidapalabra(propio.TPuerto.portnumber, datos)
}
func (propio *TPuerto16bit) Leer() uint16 {
	var rESULTADO = PuertoEntradapalabra(propio.TPuerto.portnumber)
	return rESULTADO
}
func Puertoescribirpalabra(portnumber uint16, datos uint16) {
	PuertoSalidapalabra(portnumber, datos)
}
func Puertoleerpalabra(portnumber uint16) uint16 {
	var rESULTADO uint16 = PuertoEntradapalabra(portnumber)
	return rESULTADO
}

type TPuerto32bit struct {
	TPuerto
}

func (propio *TPuerto32bit) Init(portnumber uint16) {
	propio.TPuerto.portnumber = portnumber
}
func (propio *TPuerto32bit) Escribir(datos uint32) {
	PuertoSalidadword(propio.TPuerto.portnumber, datos)
}
func (propio *TPuerto32bit) Leer() {
	PuertoEntradadword(propio.TPuerto.portnumber)
}
func Puertoescribirdword(portnumber uint16, datos uint32) {
	PuertoSalidadword(portnumber, datos)
}
func Puertoleerdword(portnumber uint16) uint32 {
	var rESULTADO uint32 = PuertoEntradadword(portnumber)
	return rESULTADO
}

var leerRecuento uint16 = 65
var escribirRecuento uint16 = 66

func PuertoSalidaocteto(portnumber uint16, datos uint8)
func PuertoEntradaocteto(portnumber uint16) uint8

func PuertoSalidapalabra(portnumber uint16, datos uint16)
func PuertoEntradapalabra(portnumber uint16) uint16

func PuertoSalidadword(portnumber uint16, datos uint32)
func PuertoEntradadword(portnumber uint16) uint32
