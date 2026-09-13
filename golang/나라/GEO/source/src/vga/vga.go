package vga

import . "unsafe"
import . "პორტი"

type Tვიდეოგრაფიკამასივი struct {
}

var micsპორტი uint16 = 0x3c2
var crtcინდექსიპორტი uint16 = 0x3d4
var crtcdataპორტი uint16 = 0x3d5
var sequencerინდექსიპორტი uint16 = 0x3c4
var sequencerdataპორტი uint16 = 0x3c5
var გრაფიკაcontrollerინდექსიპორტი uint16 = 0x3ce
var გრაფიკაcontrollerdataპორტი uint16 = 0x3cf
var ატრიბუტიcontrollerინდექსიპორტი uint16 = 0x3c0
var ატრიბუტიcontrollerკითხვაპორტი uint16 = 0x3c1
var ატრიბუტიcontrollerჩაწერაპორტი uint16 = 0x3c0
var ატრიბუტიcontrollerგანულებაპორტი uint16 = 0x3da

func (self *Tვიდეოგრაფიკამასივი) Wჩაწერაregister(register []byte) {
	var regინდექსი uint16 = 0

	Pპორტიჩაწერაbyte(micsპორტი, register[regინდექსი])
	regინდექსი++

	var i uint8
	for i = 0; i < 5; i++ {
		Pპორტიჩაწერაbyte(sequencerინდექსიპორტი, i)
		Pპორტიჩაწერაbyte(sequencerdataპორტი, register[regინდექსი])
		regინდექსი++
	}

	Pპორტიჩაწერაbyte(crtcინდექსიპორტი, 0x03)

	Pპორტიჩაწერაbyte(crtcdataპორტი, (Pპორტიკითხვაbyte(crtcdataპორტი) | 0x80))
	Pპორტიჩაწერაbyte(crtcინდექსიპორტი, 0x11)
	Pპორტიჩაწერაbyte(crtcdataპორტი, (Pპორტიკითხვაbyte(crtcdataპორტი) & ^uint8(0x80)))

	register[0x03] = register[0x03] | 0x80
	register[0x11] = register[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		Pპორტიჩაწერაbyte(crtcინდექსიპორტი, i)
		Pპორტიჩაწერაbyte(crtcdataპორტი, register[regინდექსი])
		regინდექსი++
	}

	for i = 0; i < 9; i++ {
		Pპორტიჩაწერაbyte(გრაფიკაcontrollerინდექსიპორტი, i)
		Pპორტიჩაწერაbyte(გრაფიკაcontrollerdataპორტი, register[regინდექსი])
		regინდექსი++
	}

	for i = 0; i < 21; i++ {
		Pპორტიკითხვაbyte(ატრიბუტიcontrollerგანულებაპორტი)
		Pპორტიჩაწერაbyte(ატრიბუტიcontrollerინდექსიპორტი, i)
		Pპორტიჩაწერაbyte(ატრიბუტიcontrollerჩაწერაპორტი, register[regინდექსი])
		regინდექსი++
	}

	Pპორტიკითხვაbyte(ატრიბუტიcontrollerგანულებაპორტი)
	Pპორტიჩაწერაbyte(ატრიბუტიcontrollerინდექსიპორტი, 0x20)

}

func (self *Tვიდეოგრაფიკამასივი) Getframebuffersegment() uintptr {
	Pპორტიჩაწერაbyte(გრაფიკაcontrollerინდექსიპორტი, 0x06)
	var segmentრიცხვი uint8 = ((Pპორტიკითხვაbyte(გრაფიკაcontrollerdataპორტი) >> 2) & 0x03)
	switch segmentრიცხვი {
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
func (self *Tვიდეოგრაფიკამასივი) Putpixel(x uint32, y uint32, ფერიინდექსი uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var pixeladdress uintptr = self.Getframebuffersegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(pixeladdress)) = ფერიინდექსი

}
func (self *Tვიდეოგრაფიკამასივი) Getფერიინდექსი(r uint8, g uint8, b uint8) uint8 {
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
func (self *Tვიდეოგრაფიკამასივი) Putpixelrgb(x uint32, y uint32, r uint8, g uint8, b uint8) {
	self.Putpixel(x, y, self.Getფერიინდექსი(r, g, b))
}
func (self *Tვიდეოგრაფიკამასივი) Fillrectangle(x uint32, y uint32, w uint32, h uint32, r uint8, g uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+w; X++ {
			self.Putpixelrgb(X, Y, r, g, b)
		}
	}
}
func (self *Tვიდეოგრაფიკამასივი) Supportრეჟიმი(სიგანე uint32, სიმაღლე uint32, ფერიdepth uint32) bool {
	return სიგანე == 320 && სიმაღლე == 200 && ფერიdepth == 8
}
func (self *Tვიდეოგრაფიკამასივი) Setრეჟიმი(სიგანე uint32, სიმაღლე uint32, ფერიdepth uint32) bool {
	if !self.Supportრეჟიმი(სიგანე, სიმაღლე, ფერიdepth) {
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

	self.Wჩაწერაregister(g320x200x256)

	return true
}
