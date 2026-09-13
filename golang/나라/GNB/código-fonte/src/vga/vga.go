package vga

import . "unsafe"
import . "porto"

type TVídeoGráficosmatriz struct {
}

var micsporto uint16 = 0x3c2
var crtcÍndiceporto uint16 = 0x3d4
var crtcdadosporto uint16 = 0x3d5
var sequencerÍndiceporto uint16 = 0x3c4
var sequencerdadosporto uint16 = 0x3c5
var gráficoscontroladorÍndiceporto uint16 = 0x3ce
var gráficoscontroladordadosporto uint16 = 0x3cf
var atributocontroladorÍndiceporto uint16 = 0x3c0
var atributocontroladorlerporto uint16 = 0x3c1
var atributocontroladorescreverporto uint16 = 0x3c0
var atributocontroladorReporporto uint16 = 0x3da

func (próprio *TVídeoGráficosmatriz) Escreverregisto(registo []byte) {
	var regÍndice uint16 = 0

	Portoescreverocteto(micsporto, registo[regÍndice])
	regÍndice++

	var i uint8
	for i = 0; i < 5; i++ {
		Portoescreverocteto(sequencerÍndiceporto, i)
		Portoescreverocteto(sequencerdadosporto, registo[regÍndice])
		regÍndice++
	}

	Portoescreverocteto(crtcÍndiceporto, 0x03)

	Portoescreverocteto(crtcdadosporto, (Portolerocteto(crtcdadosporto) | 0x80))
	Portoescreverocteto(crtcÍndiceporto, 0x11)
	Portoescreverocteto(crtcdadosporto, (Portolerocteto(crtcdadosporto) & ^uint8(0x80)))

	registo[0x03] = registo[0x03] | 0x80
	registo[0x11] = registo[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Portoescreverocteto(crtcÍndiceporto, i)
		Portoescreverocteto(crtcdadosporto, registo[regÍndice])
		regÍndice++
	}

	for i = 0; i < 9; i++ {
		Portoescreverocteto(gráficoscontroladorÍndiceporto, i)
		Portoescreverocteto(gráficoscontroladordadosporto, registo[regÍndice])
		regÍndice++
	}

	for i = 0; i < 21; i++ {
		Portolerocteto(atributocontroladorReporporto)
		Portoescreverocteto(atributocontroladorÍndiceporto, i)
		Portoescreverocteto(atributocontroladorescreverporto, registo[regÍndice])
		regÍndice++
	}

	Portolerocteto(atributocontroladorReporporto)
	Portoescreverocteto(atributocontroladorÍndiceporto, 0x20)

}

func (próprio *TVídeoGráficosmatriz) Getquadrobuffersegment() uintptr {
	Portoescreverocteto(gráficoscontroladorÍndiceporto, 0x06)
	var segmentNúmero uint8 = ((Portolerocteto(gráficoscontroladordadosporto) >> 2) & 0x03)
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
func (próprio *TVídeoGráficosmatriz) Putpixel(x uint32, y uint32, corÍndice uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixelEndereço uintptr = próprio.Getquadrobuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixelEndereço)) = corÍndice

}
func (próprio *TVídeoGráficosmatriz) GetCorÍndice(r uint8, g uint8, b uint8) uint8 {
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
func (próprio *TVídeoGráficosmatriz) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	próprio.Putpixel(x, y, próprio.GetCorÍndice(r, g, b))
}
func (próprio *TVídeoGráficosmatriz) FillRectângulo(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			próprio.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (próprio *TVídeoGráficosmatriz) Suportemodo(largura uint32, altura uint32, corProfundidade uint32) bool {
	return largura == 320 && altura == 200 && corProfundidade == 8
}
func (próprio *TVídeoGráficosmatriz) Conjuntomodo(largura uint32, altura uint32, corProfundidade uint32) bool {
	if !próprio.Suportemodo(largura, altura, corProfundidade) {
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

	próprio.Escreverregisto(g320x200x256)

	return true
}
