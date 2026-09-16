/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package thành_phần_màn_hình

import . "vga"

type IThành_phần_màn_hình interface {
	Init(mẹ IThành_phần_màn_hình, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32)
	Getfocus(thành_phần_màn_hình IThành_phần_màn_hình)
	Đặt_tọa_độ_cục_bộ(x int32, y int32)
	ĐặtMàu(r uint32, g uint32, b uint32)
	Draw(vga *TẢnhđộngĐồhoạMảng)
	Containscoordinate(x uint32, y uint32) bool
}

type TThành_phần_màn_hình struct {
	mẹ	IThành_phần_màn_hình
	x	uint32
	y	uint32
	w	uint32
	h	uint32

	r	uint32
	g	uint32
	b	uint32

	Focussable	bool
}

func (mình *TThành_phần_màn_hình) Init(mẹ IThành_phần_màn_hình, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {

	mình.mẹ = mẹ

	mình.x = x
	mình.y = y
	mình.w = w
	mình.h = h

	mình.r = r
	mình.g = g
	mình.b = b

	mình.Focussable = true

}
func (mình *TThành_phần_màn_hình) Getfocus(thành_phần_màn_hình IThành_phần_màn_hình) {
	if mình.mẹ != nil {
		mình.mẹ.Getfocus(thành_phần_màn_hình)
	}
}
func (mình *TThành_phần_màn_hình) Đặt_tọa_độ_cục_bộ(x uint32, y uint32) {
	if mình.mẹ != nil {

	}
	mình.x = x
	mình.y = y

}
func (mình *TThành_phần_màn_hình) ĐặtMàu(r uint32, g uint32, b uint32) {
	mình.r = r
	mình.g = g
	mình.b = b
}

func (mình *TThành_phần_màn_hình) Draw(vga *TẢnhđộngĐồhoạMảng) {
	vga.FillChữnhật(mình.x, mình.y, mình.w, mình.h, uint8(mình.r), uint8(mình.g), uint8(mình.b))
}

func (mình *TThành_phần_màn_hình) Containscoordinate(x uint32, y uint32) bool {
	return mình.x <= x && x < (mình.x+mình.w) && mình.y <= y && y < (mình.y+mình.h)
}

type TWidgetChuộtSựkiệnhandler struct {
}

var chuộtwidget TThành_phần_màn_hình
var chuộtvga TẢnhđộngĐồhoạMảng
var previousx int16 = 0
var previousy int16 = 0
var xVịtrí int16 = 0
var yVịtrí int16 = 0

func (mình *TWidgetChuộtSựkiệnhandler) Init(thành_phần_màn_hình TThành_phần_màn_hình, vga TẢnhđộngĐồhoạMảng) {
	chuộtwidget = thành_phần_màn_hình
	chuộtvga = vga
}
func (mình *TWidgetChuộtSựkiệnhandler) BậtChuộtdown(nút int8) {

	chuộtwidget.Đặt_tọa_độ_cục_bộ(uint32(previousx), uint32(previousy))
	chuộtwidget.ĐặtMàu(0xA8, 0x00, 0x00)
	chuộtwidget.Draw(&chuộtvga)

	chuộtwidget.Draw(&chuộtvga)

}

func (mình *TWidgetChuộtSựkiệnhandler) BậtChuộtLên(nút int8) {
}

func (mình *TWidgetChuộtSựkiệnhandler) BậtChuộtDichuyển(x int8, y int8) {
	xVịtrí += int16(x)
	if xVịtrí < 0 {
		xVịtrí = 0
	}
	if xVịtrí >= 320 {
		xVịtrí = 320
	}

	yVịtrí -= int16(y)

	if yVịtrí < 0 {
		yVịtrí = 0
	}
	if yVịtrí >= 200 {
		yVịtrí = 200
	}

	chuộtwidget.Đặt_tọa_độ_cục_bộ(uint32(previousx), uint32(previousy))
	chuộtwidget.ĐặtMàu(0x00, 0x00, 0x00)
	chuộtwidget.Draw(&chuộtvga)

	chuộtwidget.Đặt_tọa_độ_cục_bộ(uint32(xVịtrí), uint32(yVịtrí))
	chuộtwidget.ĐặtMàu(0x00, 0x00, 0xA8)
	chuộtwidget.Draw(&chuộtvga)

	previousx = xVịtrí
	previousy = yVịtrí

}
