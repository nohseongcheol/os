/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package きーぼーど

import . "unsafe"

import . "ぽーと"
import . "わりこみ"
import . "こんそーる"

type Iまうすじしょうhandler interface {
	Oときまうすした(ぼたん int8)
	Oときまうすうえへ(ぼたん int8)
	Oときまうすいどう(x int8, y int8)
}

var iまうすじしょうhandler Iまうすじしょうhandler

type Tでふぉるとまうすじしょうhandler struct {
}

var こんそーる_2 Tこんそーる = Tこんそーる{}
var previousx int16 = 0
var previousy int16 = 0
var xはいち int16 = 0
var yはいち int16 = 0

func (self Tでふぉるとまうすじしょうhandler) Oときまうすした(ぼたん int8) {
	buffer := []byte("+")
	こんそーる_2.Mいんさつxy(buffer, uint16(previousx), uint16(previousy))
}
func (self Tでふぉるとまうすじしょうhandler) Oときまうすうえへ(ぼたん int8)	{}
func (self Tでふぉるとまうすじしょうhandler) Oときまうすいどう(x int8, y int8) {

	xはいち += int16(x)
	if xはいち < 0 {
		xはいち = 0
	}
	if xはいち >= 80 {
		xはいち = 79
	}

	yはいち -= int16(y)

	if yはいち < 0 {
		yはいち = 0
	}
	if yはいち >= 25 {
		yはいち = 24
	}

	buffer := []byte(" ")
	こんそーる_2.Mいんさつxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	こんそーる_2.Mいんさつxy(buffer, uint16(xはいち), uint16(yはいち))

	previousx = xはいち
	previousy = yはいち
}

type Tまうすどらいばー struct {
	Tわりこみhandler
}

var ゆうこうまうすどらいばー *Tまうすどらいばー
var わりこみhandler func(uint32) uint32

var でーたぽーと_2 uint16 = 0x60
var こまんどぽーと_2 uint16 = 0x64

const ps2たいきするせいげん = 100000

func たいきするps2にゅうりょくそら() bool {
	for i := 0; i < ps2たいきするせいげん; i++ {
		if (Pぽーとよみこみばいと(こまんどぽーと_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func たいきするps2しゅつりょくぜんたいてき() bool {
	for i := 0; i < ps2たいきするせいげん; i++ {
		if (Pぽーとよみこみばいと(こまんどぽーと_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func かきこみps2こまんど(あたい uint8) bool {
	if !たいきするps2にゅうりょくそら() {
		return false
	}
	Pぽーとかきこみばいと(こまんどぽーと_2, あたい)
	return true
}

func かきこみps2でーた(あたい uint8) bool {
	if !たいきするps2にゅうりょくそら() {
		return false
	}
	Pぽーとかきこみばいと(でーたぽーと_2, あたい)
	return true
}

func よみこみps2でーた() (uint8, bool) {
	if !たいきするps2しゅつりょくぜんたいてき() {
		return 0, false
	}
	return Pぽーとよみこみばいと(でーたぽーと_2), true
}

func そうしんまうすこまんど(あたい uint8) bool {
	if !かきこみps2こまんど(0xD4) || !かきこみps2でーた(あたい) {
		return false
	}
	ack, ok := よみこみps2でーた()
	return ok && ack == 0xFA
}

func (self *Tまうすどらいばー) Initどらいばー(かんりしゃ *Tわりこみかんりしゃ, まうすじしょうhandler Iまうすじしょうhandler) {

	iまうすじしょうhandler = Tでふぉるとまうすじしょうhandler{}

	if まうすじしょうhandler != nil {
		iまうすじしょうhandler = まうすじしょうhandler
	}

	ゆうこうまうすどらいばー = self
	わりこみhandler = とってまうすわりこみ
	var address uintptr
	address = uintptr(Pointer(&わりこみhandler))
	self.Init(0x2C, uintptr(Pointer(かんりしゃ)), address)

	for i := 0; i < 32 && (Pぽーとよみこみばいと(こまんどぽーと_2)&0x01) != 0; i++ {
		Pぽーとよみこみばいと(でーたぽーと_2)
	}

	if !かきこみps2こまんど(0xA8) || !かきこみps2こまんど(0x20) {
		return
	}
	じょうたい, ok := よみこみps2でーた()
	if !ok {
		return
	}
	じょうたい |= 0x02
	じょうたい &^= 0x20
	if !かきこみps2こまんど(0x60) || !かきこみps2でーた(じょうたい) {
		return
	}

	if !そうしんまうすこまんど(0xF6) || !そうしんまうすこまんど(0xF4) {
		return
	}
	offset = 0

}

func とってまうすわりこみ(esp uint32) uint32 {
	if ゆうこうまうすどらいばー == nil {
		Pぽーとよみこみばいと(でーたぽーと_2)
		return esp
	}
	return ゆうこうまうすどらいばー.Hとってわりこみ(esp)
}

var かうんと uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var ぼたん_2 int8
var ほりゅうx int16
var ほりゅうy int16
var ほりゅうぼたん int8
var ほりゅうまうすじしょう bool

func (self *Tまうすどらいばー) Hとってわりこみ(esp uint32) uint32 {
	じょうたい := Pぽーとよみこみばいと(こまんどぽーと_2)
	if (じょうたい&0x01) == 0 || (じょうたい&0x20) == 0 {
		return esp
	}

	でーた := Pぽーとよみこみばいと(でーたぽーと_2)

	if offset == 0 && (でーた&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(でーた)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetじょうたい := uint8(buffer_2[0])

		if (packetじょうたい & 0xC0) == 0 {
			ほりゅうx += int16(buffer_2[1])
			ほりゅうy += int16(buffer_2[2])
			if ほりゅうx > 127 {
				ほりゅうx = 127
			} else if ほりゅうx < -127 {
				ほりゅうx = -127
			}
			if ほりゅうy > 127 {
				ほりゅうy = 127
			} else if ほりゅうy < -127 {
				ほりゅうy = -127
			}
		}
		ほりゅうぼたん = int8(packetじょうたい & 0x07)
		ほりゅうまうすじしょう = true
	}

	return esp

}

func Pぷろせすほりゅうまうすじしょういちらん() {
	if iまうすじしょうhandler == nil {
		return
	}

	Iわりこみdeactive()
	if !ほりゅうまうすじしょう {
		Iわりこみゆうこう()
		return
	}
	x := int8(ほりゅうx)
	y := int8(ほりゅうy)
	しんきぼたん := ほりゅうぼたん
	oldぼたん := ぼたん_2

	ほりゅうx = 0
	ほりゅうy = 0
	ほりゅうまうすじしょう = false
	Iわりこみゆうこう()

	if x != 0 || y != 0 {
		iまうすじしょうhandler.Oときまうすいどう(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		ますく := int8(0x1 << i)
		if (しんきぼたん & ますく) != (oldぼたん & ますく) {
			if (しんきぼたん & ますく) != 0 {
				iまうすじしょうhandler.Oときまうすした(int8(i + 1))
			} else {
				iまうすじしょうhandler.Oときまうすうえへ(int8(i + 1))
			}
		}
	}
	ぼたん_2 = しんきぼたん
}
