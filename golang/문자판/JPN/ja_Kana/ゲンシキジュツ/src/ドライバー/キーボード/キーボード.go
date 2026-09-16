/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package キーボード

import . "unsafe"

import . "ポート"
import . "ワリコミ"

import . "コンソール"
import . "システムヨビダシ"

type Iキーボードジショウhandler interface {
	Oトキカギシタ(カギ byte)
	Oトキカギウエヘ(カギ byte)
}

var iキーボードジショウhandler Iキーボードジショウhandler
var デフォルトキーボードジショウhandler Tデフォルトキーボードジショウhandler

type Tデフォルトキーボードジショウhandler struct {
}

func (self *Tデフォルトキーボードジショウhandler) Oトキカギシタ(カギ byte) {
	アタイ16ススム := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = アタイ16ススム[((カギ >> 4) & 0xF)]
	buffer[18] = アタイ16ススム[カギ&0xF]

	コンソール_2 := Tコンソール{}
	コンソール_2.Mインサツ(buffer)

}
func (self *Tデフォルトキーボードジショウhandler) Oトキカギウエヘ(カギ byte) {
}

type Tキーボードドライバー struct {
	Tワリコミhandler
}

var ユウコウキーボードドライバー *Tキーボードドライバー
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

func (self *Tキーボードドライバー) Initドライバー(カンリシャ *Tワリコミカンリシャ, キーボードジショウhandler Iキーボードジショウhandler) {

	iキーボードジショウhandler = &デフォルトキーボードジショウhandler
	if キーボードジショウhandler != nil {
		iキーボードジショウhandler = キーボードジショウhandler
	}

	ユウコウキーボードドライバー = self
	ワリコミhandler = トッテキーボードワリコミ
	var address uintptr
	address = uintptr(Pointer(&ワリコミhandler))

	self.Init(0x21, uintptr(Pointer(カンリシャ)), address)

	for i := 0; i < 32 && (Pポートヨミコミバイト(コマンドポート_2)&0x01) != 0; i++ {
		Pポートヨミコミバイト(データポート_2)
	}

	if !カキコミps2コマンド(0xAE) || !カキコミps2コマンド(0x20) {
		return
	}
	ジョウタイ, ok := ヨミコミps2データ()
	if !ok {
		return
	}
	ジョウタイ |= 0x01
	ジョウタイ &^= 0x10
	if !カキコミps2コマンド(0x60) || !カキコミps2データ(ジョウタイ) {
		return
	}

	if !カキコミps2データ(0xF4) {
		return
	}
	ack, ok := ヨミコミps2データ()
	if !ok || ack != 0xFA {
		return
	}

}

func トッテキーボードワリコミ(esp uint32) uint32 {
	if ユウコウキーボードドライバー == nil {
		Pポートヨミコミバイト(データポート_2)
		return esp
	}
	return ユウコウキーボードドライバー.Hトッテワリコミ(esp)
}

const キーボードマチギョウレツサイズ = 64

var キーボードマチギョウレツ [キーボードマチギョウレツサイズ]byte
var キーボードマチギョウレツヨミコミ uint8
var キーボードマチギョウレツカキコミ uint8
var ヒダリshift bool
var ミギshift bool
var extendedスキャンcode bool

func マチギョウレツキーボードバイト(カギ byte) {
	ツギ := (キーボードマチギョウレツカキコミ + 1) % キーボードマチギョウレツサイズ
	if ツギ == キーボードマチギョウレツヨミコミ {
		return
	}
	キーボードマチギョウレツ[キーボードマチギョウレツカキコミ] = カギ
	キーボードマチギョウレツカキコミ = ツギ
}

func Pプロセスホリュウキーボードジショウイチラン() {
	for キーボードマチギョウレツヨミコミ != キーボードマチギョウレツカキコミ {
		カギ := キーボードマチギョウレツ[キーボードマチギョウレツヨミコミ]
		キーボードマチギョウレツヨミコミ = (キーボードマチギョウレツヨミコミ + 1) % キーボードマチギョウレツサイズ
		Stdinputバイト(カギ)
		if iキーボードジショウhandler != nil {
			iキーボードジショウhandler.Oトキカギシタ(カギ)
		}
	}
}

func スキャンcodetoバイト(スキャンcode uint8) (byte, bool) {
	shift := ヒダリshift || ミギshift

	if スキャンcode >= 0x02 && スキャンcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[スキャンcode-0x02], true
		}
		return "1234567890"[スキャンcode-0x02], true
	}
	if スキャンcode >= 0x10 && スキャンcode <= 0x19 {
		カギ := "qwertyuiop"[スキャンcode-0x10]
		if shift {
			カギ -= 'a' - 'A'
		}
		return カギ, true
	}
	if スキャンcode >= 0x1E && スキャンcode <= 0x26 {
		カギ := "asdfghjkl"[スキャンcode-0x1E]
		if shift {
			カギ -= 'a' - 'A'
		}
		return カギ, true
	}
	if スキャンcode >= 0x2C && スキャンcode <= 0x32 {
		カギ := "zxcvbnm"[スキャンcode-0x2C]
		if shift {
			カギ -= 'a' - 'A'
		}
		return カギ, true
	}

	switch スキャンcode {
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

func (self *Tキーボードドライバー) Hトッテワリコミ(esp uint32) uint32 {
	ジョウタイ := Pポートヨミコミバイト(コマンドポート_2)
	if (ジョウタイ&0x01) == 0 || (ジョウタイ&0x20) != 0 {
		return esp
	}

	スキャンcode := Pポートヨミコミバイト(データポート_2)
	if スキャンcode == 0xE0 {
		extendedスキャンcode = true
		return esp
	}
	if extendedスキャンcode {
		extendedスキャンcode = false
		return esp
	}

	released := (スキャンcode & 0x80) != 0
	basecode := スキャンcode & 0x7F
	if basecode == 0x2A {
		ヒダリshift = !released
		return esp
	}
	if basecode == 0x36 {
		ミギshift = !released
		return esp
	}
	if released {
		return esp
	}

	if カギ, ok := スキャンcodetoバイト(basecode); ok {
		マチギョウレツキーボードバイト(カギ)
	}

	return esp
}
