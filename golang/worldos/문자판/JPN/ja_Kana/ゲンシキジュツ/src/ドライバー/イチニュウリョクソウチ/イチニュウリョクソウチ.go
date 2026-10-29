/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package キーボード

import . "unsafe"

import . "ポート"
import . "ワリコミ"
import . "コンソール"

type Iマウスジショウhandler interface {
	Oトキマウスシタ(ボタン int8)
	Oトキマウスウエヘ(ボタン int8)
	Oトキマウスイドウ(x int8, y int8)
}

var iマウスジショウhandler Iマウスジショウhandler

type Tデフォルトマウスジショウhandler struct {
}

var コンソール_2 Tコンソール = Tコンソール{}
var previousx int16 = 0
var previousy int16 = 0
var xハイチ int16 = 0
var yハイチ int16 = 0

func (self Tデフォルトマウスジショウhandler) Oトキマウスシタ(ボタン int8) {
	buffer := []byte("+")
	コンソール_2.Mインサツxy(buffer, uint16(previousx), uint16(previousy))
}
func (self Tデフォルトマウスジショウhandler) Oトキマウスウエヘ(ボタン int8)	{}
func (self Tデフォルトマウスジショウhandler) Oトキマウスイドウ(x int8, y int8) {

	xハイチ += int16(x)
	if xハイチ < 0 {
		xハイチ = 0
	}
	if xハイチ >= 80 {
		xハイチ = 79
	}

	yハイチ -= int16(y)

	if yハイチ < 0 {
		yハイチ = 0
	}
	if yハイチ >= 25 {
		yハイチ = 24
	}

	buffer := []byte(" ")
	コンソール_2.Mインサツxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	コンソール_2.Mインサツxy(buffer, uint16(xハイチ), uint16(yハイチ))

	previousx = xハイチ
	previousy = yハイチ
}

type Tマウスドライバー struct {
	Tワリコミhandler
}

var ユウコウマウスドライバー *Tマウスドライバー
var ワリコミhandler func(uint32) uint32

var データポート_2 uint16 = 0x60
var コマンドポート_2 uint16 = 0x64

const ps2タイキスルセイゲン = 100000

func タイキスルps2ニュウリョクソラ() bool {
	for i := 0; i < ps2タイキスルセイゲン; i++ {
		if (Pポートヨミコミバイト(コマンドポート_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func タイキスルps2シュツリョクゼンタイテキ() bool {
	for i := 0; i < ps2タイキスルセイゲン; i++ {
		if (Pポートヨミコミバイト(コマンドポート_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func カキコミps2コマンド(アタイ uint8) bool {
	if !タイキスルps2ニュウリョクソラ() {
		return false
	}
	Pポートカキコミバイト(コマンドポート_2, アタイ)
	return true
}

func カキコミps2データ(アタイ uint8) bool {
	if !タイキスルps2ニュウリョクソラ() {
		return false
	}
	Pポートカキコミバイト(データポート_2, アタイ)
	return true
}

func ヨミコミps2データ() (uint8, bool) {
	if !タイキスルps2シュツリョクゼンタイテキ() {
		return 0, false
	}
	return Pポートヨミコミバイト(データポート_2), true
}

func ソウシンマウスコマンド(アタイ uint8) bool {
	if !カキコミps2コマンド(0xD4) || !カキコミps2データ(アタイ) {
		return false
	}
	ack, ok := ヨミコミps2データ()
	return ok && ack == 0xFA
}

func (self *Tマウスドライバー) Initドライバー(カンリシャ *Tワリコミカンリシャ, マウスジショウhandler Iマウスジショウhandler) {

	iマウスジショウhandler = Tデフォルトマウスジショウhandler{}

	if マウスジショウhandler != nil {
		iマウスジショウhandler = マウスジショウhandler
	}

	ユウコウマウスドライバー = self
	ワリコミhandler = トッテマウスワリコミ
	var address uintptr
	address = uintptr(Pointer(&ワリコミhandler))
	self.Init(0x2C, uintptr(Pointer(カンリシャ)), address)

	for i := 0; i < 32 && (Pポートヨミコミバイト(コマンドポート_2)&0x01) != 0; i++ {
		Pポートヨミコミバイト(データポート_2)
	}

	if !カキコミps2コマンド(0xA8) || !カキコミps2コマンド(0x20) {
		return
	}
	ジョウタイ, ok := ヨミコミps2データ()
	if !ok {
		return
	}
	ジョウタイ |= 0x02
	ジョウタイ &^= 0x20
	if !カキコミps2コマンド(0x60) || !カキコミps2データ(ジョウタイ) {
		return
	}

	if !ソウシンマウスコマンド(0xF6) || !ソウシンマウスコマンド(0xF4) {
		return
	}
	offset = 0

}

func トッテマウスワリコミ(esp uint32) uint32 {
	if ユウコウマウスドライバー == nil {
		Pポートヨミコミバイト(データポート_2)
		return esp
	}
	return ユウコウマウスドライバー.Hトッテワリコミ(esp)
}

var カウント uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var ボタン_2 int8
var ホリュウx int16
var ホリュウy int16
var ホリュウボタン int8
var ホリュウマウスジショウ bool

func (self *Tマウスドライバー) Hトッテワリコミ(esp uint32) uint32 {
	ジョウタイ := Pポートヨミコミバイト(コマンドポート_2)
	if (ジョウタイ&0x01) == 0 || (ジョウタイ&0x20) == 0 {
		return esp
	}

	データ := Pポートヨミコミバイト(データポート_2)

	if offset == 0 && (データ&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(データ)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetジョウタイ := uint8(buffer_2[0])

		if (packetジョウタイ & 0xC0) == 0 {
			ホリュウx += int16(buffer_2[1])
			ホリュウy += int16(buffer_2[2])
			if ホリュウx > 127 {
				ホリュウx = 127
			} else if ホリュウx < -127 {
				ホリュウx = -127
			}
			if ホリュウy > 127 {
				ホリュウy = 127
			} else if ホリュウy < -127 {
				ホリュウy = -127
			}
		}
		ホリュウボタン = int8(packetジョウタイ & 0x07)
		ホリュウマウスジショウ = true
	}

	return esp

}

func Pプロセスホリュウマウスジショウイチラン() {
	if iマウスジショウhandler == nil {
		return
	}

	Iワリコミdeactive()
	if !ホリュウマウスジショウ {
		Iワリコミユウコウ()
		return
	}
	x := int8(ホリュウx)
	y := int8(ホリュウy)
	シンキボタン := ホリュウボタン
	oldボタン := ボタン_2

	ホリュウx = 0
	ホリュウy = 0
	ホリュウマウスジショウ = false
	Iワリコミユウコウ()

	if x != 0 || y != 0 {
		iマウスジショウhandler.Oトキマウスイドウ(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		マスク := int8(0x1 << i)
		if (シンキボタン & マスク) != (oldボタン & マスク) {
			if (シンキボタン & マスク) != 0 {
				iマウスジショウhandler.Oトキマウスシタ(int8(i + 1))
			} else {
				iマウスジショウhandler.Oトキマウスウエヘ(int8(i + 1))
			}
		}
	}
	ボタン_2 = シンキボタン
}
