/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vga

import . "unsafe"
import . "puerto"

type TVídeoGráficosmatriz struct {
}

var micspuerto uint16 = 0x3c2
var crtcÍndicepuerto uint16 = 0x3d4
var crtcdatospuerto uint16 = 0x3d5
var sequencerÍndicepuerto uint16 = 0x3c4
var sequencerdatospuerto uint16 = 0x3c5
var gráficoscontroladorÍndicepuerto uint16 = 0x3ce
var gráficoscontroladordatospuerto uint16 = 0x3cf
var atributocontroladorÍndicepuerto uint16 = 0x3c0
var atributocontroladorleerpuerto uint16 = 0x3c1
var atributocontroladorescribirpuerto uint16 = 0x3c0
var atributocontroladorReiniciarpuerto uint16 = 0x3da

func (propio *TVídeoGráficosmatriz) Escribirregistro(registro []byte) {
	var regÍndice uint16 = 0

	Puertoescribirocteto(micspuerto, registro[regÍndice])
	regÍndice++

	var i uint8
	for i = 0; i < 5; i++ {
		Puertoescribirocteto(sequencerÍndicepuerto, i)
		Puertoescribirocteto(sequencerdatospuerto, registro[regÍndice])
		regÍndice++
	}

	Puertoescribirocteto(crtcÍndicepuerto, 0x03)

	Puertoescribirocteto(crtcdatospuerto, (Puertoleerocteto(crtcdatospuerto) | 0x80))
	Puertoescribirocteto(crtcÍndicepuerto, 0x11)
	Puertoescribirocteto(crtcdatospuerto, (Puertoleerocteto(crtcdatospuerto) & ^uint8(0x80)))

	registro[0x03] = registro[0x03] | 0x80
	registro[0x11] = registro[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Puertoescribirocteto(crtcÍndicepuerto, i)
		Puertoescribirocteto(crtcdatospuerto, registro[regÍndice])
		regÍndice++
	}

	for i = 0; i < 9; i++ {
		Puertoescribirocteto(gráficoscontroladorÍndicepuerto, i)
		Puertoescribirocteto(gráficoscontroladordatospuerto, registro[regÍndice])
		regÍndice++
	}

	for i = 0; i < 21; i++ {
		Puertoleerocteto(atributocontroladorReiniciarpuerto)
		Puertoescribirocteto(atributocontroladorÍndicepuerto, i)
		Puertoescribirocteto(atributocontroladorescribirpuerto, registro[regÍndice])
		regÍndice++
	}

	Puertoleerocteto(atributocontroladorReiniciarpuerto)
	Puertoescribirocteto(atributocontroladorÍndicepuerto, 0x20)

}

func (propio *TVídeoGráficosmatriz) Gettramabuffersegment() uintptr {
	Puertoescribirocteto(gráficoscontroladorÍndicepuerto, 0x06)
	var segmentNúmero uint8 = ((Puertoleerocteto(gráficoscontroladordatospuerto) >> 2) & 0x03)
	switch segmentNúmero {
	case 0:
		return uintptr(0x00000)
	case 1:
		return uintptr(0xa0000)
	case 2:
		return uintptr(0xb0000)
	case 3:
		return uintptr(0xb8000)
	}

	return uintptr(0xB0000)
}
func (propio *TVídeoGráficosmatriz) Putpixel(x uint32, y uint32, colorÍndice uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixelDirección uintptr = propio.Gettramabuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixelDirección)) = colorÍndice

}
func (propio *TVídeoGráficosmatriz) GetcolorÍndice(r uint8, g uint8, b uint8) uint8 {
	if r == 0x00 && g == 0x00 && b == 0x00 {
		return 0x00
	}
	if r == 0x00 && g == 0x00 && b == 0xA8 {
		return 0x01
	}
	if r == 0x00 && g == 0xA8 && b == 0x00 {
		return 0x02
	}
	if r == 0xA8 && g == 0x00 && b == 0x00 {
		return 0x04
	}
	if r == 0xFF && g == 0xFF && b == 0xFF {
		return 0x3F
	}

	return 0x01
}
func (propio *TVídeoGráficosmatriz) PutpixelRVARGB(x uint32, y uint32, r uint8, g uint8, b uint8) {
	propio.Putpixel(x, y, propio.GetcolorÍndice(r, g, b))
}
func (propio *TVídeoGráficosmatriz) FillRectángulo(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			propio.PutpixelRVARGB(X, Y, r, g, b)
		}
	}
}
func (propio *TVídeoGráficosmatriz) Detallemodo(ancho uint32, altura uint32, colorProfundidad uint32) bool {
	return ancho == 320 && altura == 200 && colorProfundidad == 8
}
func (propio *TVídeoGráficosmatriz) Establecermodo(ancho uint32, altura uint32, colorProfundidad uint32) bool {
	if !propio.Detallemodo(ancho, altura, colorProfundidad) {
		return false
	}

	var g320x200x256 = []byte{

		0x63,

		0x03, 0x01, 0x0F, 0x00, 0x0E,

		0x5F, 0x4F, 0x50, 0x82, 0x54, 0x80, 0xBF, 0x1F,
		0x00, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x9C, 0x0E, 0x8F, 0x28, 0x40, 0x96, 0xB9, 0xA3,
		0xFF,

		0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x05, 0x0F,
		0xFF,

		0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
		0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
		0x41, 0x00, 0x0F, 0x00, 0x00}

	propio.Escribirregistro(g320x200x256)

	return true
}
