/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package きーぼーど

import . "unsafe"

import . "ぽーと"
import . "わりこみ"

import . "こんそーる"
import . "しすてむよびだし"

type Iきーぼーどじしょうhandler interface {
	Oときかぎした(かぎ byte)
	Oときかぎうえへ(かぎ byte)
}

var iきーぼーどじしょうhandler Iきーぼーどじしょうhandler
var でふぉるときーぼーどじしょうhandler Tでふぉるときーぼーどじしょうhandler

type Tでふぉるときーぼーどじしょうhandler struct {
}

func (self *Tでふぉるときーぼーどじしょうhandler) Oときかぎした(かぎ byte) {
	あたい16すすむ := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = あたい16すすむ[((かぎ >> 4) & 0xF)]
	buffer[18] = あたい16すすむ[かぎ&0xF]

	こんそーる_2 := Tこんそーる{}
	こんそーる_2.Mいんさつ(buffer)

}
func (self *Tでふぉるときーぼーどじしょうhandler) Oときかぎうえへ(かぎ byte) {
}

type Tきーぼーどどらいばー struct {
	Tわりこみhandler
}

var ゆうこうきーぼーどどらいばー *Tきーぼーどどらいばー
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

func (self *Tきーぼーどどらいばー) Initどらいばー(かんりしゃ *Tわりこみかんりしゃ, きーぼーどじしょうhandler Iきーぼーどじしょうhandler) {

	iきーぼーどじしょうhandler = &でふぉるときーぼーどじしょうhandler
	if きーぼーどじしょうhandler != nil {
		iきーぼーどじしょうhandler = きーぼーどじしょうhandler
	}

	ゆうこうきーぼーどどらいばー = self
	わりこみhandler = とってきーぼーどわりこみ
	var address uintptr
	address = uintptr(Pointer(&わりこみhandler))

	self.Init(0x21, uintptr(Pointer(かんりしゃ)), address)

	for i := 0; i < 32 && (Pぽーとよみこみばいと(こまんどぽーと_2)&0x01) != 0; i++ {
		Pぽーとよみこみばいと(でーたぽーと_2)
	}

	if !かきこみps2こまんど(0xAE) || !かきこみps2こまんど(0x20) {
		return
	}
	じょうたい, ok := よみこみps2でーた()
	if !ok {
		return
	}
	じょうたい |= 0x01
	じょうたい &^= 0x10
	if !かきこみps2こまんど(0x60) || !かきこみps2でーた(じょうたい) {
		return
	}

	if !かきこみps2でーた(0xF4) {
		return
	}
	ack, ok := よみこみps2でーた()
	if !ok || ack != 0xFA {
		return
	}

}

func とってきーぼーどわりこみ(esp uint32) uint32 {
	if ゆうこうきーぼーどどらいばー == nil {
		Pぽーとよみこみばいと(でーたぽーと_2)
		return esp
	}
	return ゆうこうきーぼーどどらいばー.Hとってわりこみ(esp)
}

const きーぼーどまちぎょうれつさいず = 64

var きーぼーどまちぎょうれつ [きーぼーどまちぎょうれつさいず]byte
var きーぼーどまちぎょうれつよみこみ uint8
var きーぼーどまちぎょうれつかきこみ uint8
var ひだりshift bool
var みぎshift bool
var extendedすきゃんcode bool

func まちぎょうれつきーぼーどばいと(かぎ byte) {
	つぎ := (きーぼーどまちぎょうれつかきこみ + 1) % きーぼーどまちぎょうれつさいず
	if つぎ == きーぼーどまちぎょうれつよみこみ {
		return
	}
	きーぼーどまちぎょうれつ[きーぼーどまちぎょうれつかきこみ] = かぎ
	きーぼーどまちぎょうれつかきこみ = つぎ
}

func Pぷろせすほりゅうきーぼーどじしょういちらん() {
	for きーぼーどまちぎょうれつよみこみ != きーぼーどまちぎょうれつかきこみ {
		かぎ := きーぼーどまちぎょうれつ[きーぼーどまちぎょうれつよみこみ]
		きーぼーどまちぎょうれつよみこみ = (きーぼーどまちぎょうれつよみこみ + 1) % きーぼーどまちぎょうれつさいず
		Stdinputばいと(かぎ)
		if iきーぼーどじしょうhandler != nil {
			iきーぼーどじしょうhandler.Oときかぎした(かぎ)
		}
	}
}

func すきゃんcodetoばいと(すきゃんcode uint8) (byte, bool) {
	shift := ひだりshift || みぎshift

	if すきゃんcode >= 0x02 && すきゃんcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[すきゃんcode-0x02], true
		}
		return "1234567890"[すきゃんcode-0x02], true
	}
	if すきゃんcode >= 0x10 && すきゃんcode <= 0x19 {
		かぎ := "qwertyuiop"[すきゃんcode-0x10]
		if shift {
			かぎ -= 'a' - 'A'
		}
		return かぎ, true
	}
	if すきゃんcode >= 0x1E && すきゃんcode <= 0x26 {
		かぎ := "asdfghjkl"[すきゃんcode-0x1E]
		if shift {
			かぎ -= 'a' - 'A'
		}
		return かぎ, true
	}
	if すきゃんcode >= 0x2C && すきゃんcode <= 0x32 {
		かぎ := "zxcvbnm"[すきゃんcode-0x2C]
		if shift {
			かぎ -= 'a' - 'A'
		}
		return かぎ, true
	}

	switch すきゃんcode {
	case 0x0C:
		if shift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (self *Tきーぼーどどらいばー) Hとってわりこみ(esp uint32) uint32 {
	じょうたい := Pぽーとよみこみばいと(こまんどぽーと_2)
	if (じょうたい&0x01) == 0 || (じょうたい&0x20) != 0 {
		return esp
	}

	すきゃんcode := Pぽーとよみこみばいと(でーたぽーと_2)
	if すきゃんcode == 0xE0 {
		extendedすきゃんcode = true
		return esp
	}
	if extendedすきゃんcode {
		extendedすきゃんcode = false
		return esp
	}

	released := (すきゃんcode & 0x80) != 0
	basecode := すきゃんcode & 0x7F
	if basecode == 0x2A {
		ひだりshift = !released
		return esp
	}
	if basecode == 0x36 {
		みぎshift = !released
		return esp
	}
	if released {
		return esp
	}

	if かぎ, ok := すきゃんcodetoばいと(basecode); ok {
		まちぎょうれつきーぼーどばいと(かぎ)
	}

	return esp
}
