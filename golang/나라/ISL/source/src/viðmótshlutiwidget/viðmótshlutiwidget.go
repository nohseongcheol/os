package viðmótshlutiwidget

import . "vga"

type IViðmótshlutiwidget interface {
	Init(foreldri IViðmótshlutiwidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	GetVirkni(viðmótshlutiwidget IViðmótshlutiwidget)
	Set_local_coordinates(x int32, y int32)
	SetjaLitur(r uint32, g uint32, b uint32)
	Draw(vga *TVideóMyndefniFylki)
	Containscoordinate(x uint32, y uint32) bool
}

type TViðmótshlutiwidget struct {
	foreldri	IViðmótshlutiwidget
	x		uint32
	y		uint32
	w		uint32
	h		uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (sjálft *TViðmótshlutiwidget) Init(foreldri IViðmótshlutiwidget, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	sjálft.foreldri = foreldri

	sjálft.x = x
	sjálft.y = y
	sjálft.w = w
	sjálft.h = h

	sjálft.r = r
	sjálft.g = g
	sjálft.b = b

	sjálft.Focussable = true

}
func (sjálft *TViðmótshlutiwidget) GetVirkni(viðmótshlutiwidget IViðmótshlutiwidget) {
	if sjálft.foreldri != nil {
		sjálft.foreldri.GetVirkni(viðmótshlutiwidget)
	}
}
func (sjálft *TViðmótshlutiwidget) Set_local_coordinates(x uint32, y uint32) {
	if sjálft.foreldri != nil {

	}
	sjálft.x = x
	sjálft.y = y

}
func (sjálft *TViðmótshlutiwidget) SetjaLitur(r uint32, g uint32, b uint32) {
	sjálft.r = r
	sjálft.g = g
	sjálft.b = b
}

func (sjálft *TViðmótshlutiwidget) Draw(vga *TVideóMyndefniFylki) {
	vga.Fillrectangle(sjálft.x, sjálft.y, sjálft.w, sjálft.h, uint8(sjálft.r), uint8(sjálft.g), uint8(sjálft.b))
}

func (sjálft *TViðmótshlutiwidget) Containscoordinate(x uint32, y uint32) bool {
	return sjálft.x <= x && x < (sjálft.x+sjálft.w) && sjálft.y <= y && y < (sjálft.y+sjálft.h)
}

type TViðmótshlutiwidgetMúseventhandler struct {
}

var músViðmótshlutiwidget TViðmótshlutiwidget
var músvga TVideóMyndefniFylki
var previousx int16 = 0
var previousy int16 = 0
var xStaða int16 = 0
var yStaða int16 = 0

func (sjálft *TViðmótshlutiwidgetMúseventhandler) Init(viðmótshlutiwidget TViðmótshlutiwidget, vga TVideóMyndefniFylki) {
	músViðmótshlutiwidget = viðmótshlutiwidget
	músvga = vga
}
func (sjálft *TViðmótshlutiwidgetMúseventhandler) NotaMúsNiður(hnappur int8) {

	músViðmótshlutiwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	músViðmótshlutiwidget.SetjaLitur(0xA8, 0x00, 0x00)
	músViðmótshlutiwidget.Draw(&músvga)

	músViðmótshlutiwidget.Draw(&músvga)

}

func (sjálft *TViðmótshlutiwidgetMúseventhandler) NotaMúsUpp(hnappur int8) {
}

func (sjálft *TViðmótshlutiwidgetMúseventhandler) NotaMúsFæra(x int8, y int8) {
	xStaða += int16(x)
	if xStaða < 0 {
		xStaða = 0
	}
	if xStaða >= 320 {
		xStaða = 320
	}

	yStaða -= int16(y)

	if yStaða < 0 {
		yStaða = 0
	}
	if yStaða >= 200 {
		yStaða = 200
	}

	músViðmótshlutiwidget.Set_local_coordinates(uint32(previousx), uint32(previousy))
	músViðmótshlutiwidget.SetjaLitur(0x00, 0x00, 0x00)
	músViðmótshlutiwidget.Draw(&músvga)

	músViðmótshlutiwidget.Set_local_coordinates(uint32(xStaða), uint32(yStaða))
	músViðmótshlutiwidget.SetjaLitur(0x00, 0x00, 0xA8)
	músViðmótshlutiwidget.Draw(&músvga)

	previousx = xStaða
	previousy = yStaða

}
