package キーボード

import . "unsafe"

import . "ポート"
import . "割込み"

import . "コンソール"
import . "システム呼出し"

type Iキーボード事象handler interface {
	O時鍵下(鍵 byte)
	O時鍵上へ(鍵 byte)
}

var iキーボード事象handler Iキーボード事象handler
var デフォルトキーボード事象handler Tデフォルトキーボード事象handler

type Tデフォルトキーボード事象handler struct {
}

func (self *Tデフォルトキーボード事象handler) O時鍵下(鍵 byte) {
	値16進 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = 値16進[((鍵 >> 4) & 0xF)]
	buffer[18] = 値16進[鍵&0xF]

	コンソール_2 := Tコンソール{}
	コンソール_2.M印刷(buffer)

}
func (self *Tデフォルトキーボード事象handler) O時鍵上へ(鍵 byte) {
}

type Tキーボードドライバー struct {
	T割込みhandler
}

var 有効キーボードドライバー *Tキーボードドライバー
var 割込みhandler func(uint32) uint32

var データポート_2 uint16 = 0x60
var コマンドポート_2 uint16 = 0x64

const ps2待機する制限 = 100000

func 待機するps2入力空() bool {
	for i := 0; i < ps2待機する制限; i++ {
		if (Pポート読込みバイト(コマンドポート_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func 待機するps2出力全体的() bool {
	for i := 0; i < ps2待機する制限; i++ {
		if (Pポート読込みバイト(コマンドポート_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func 書込みps2コマンド(値 uint8) bool {
	if !待機するps2入力空() {
		return false
	}
	Pポート書込みバイト(コマンドポート_2, 値)
	return true
}

func 書込みps2データ(値 uint8) bool {
	if !待機するps2入力空() {
		return false
	}
	Pポート書込みバイト(データポート_2, 値)
	return true
}

func 読込みps2データ() (uint8, bool) {
	if !待機するps2出力全体的() {
		return 0, false
	}
	return Pポート読込みバイト(データポート_2), true
}

func (self *Tキーボードドライバー) Initドライバー(管理者 *T割込み管理者, キーボード事象handler Iキーボード事象handler) {

	iキーボード事象handler = &デフォルトキーボード事象handler
	if キーボード事象handler != nil {
		iキーボード事象handler = キーボード事象handler
	}

	有効キーボードドライバー = self
	割込みhandler = 取っ手キーボード割込み
	var address uintptr
	address = uintptr(Pointer(&割込みhandler))

	self.Init(0x21, uintptr(Pointer(管理者)), address)

	for i := 0; i < 32 && (Pポート読込みバイト(コマンドポート_2)&0x01) != 0; i++ {
		Pポート読込みバイト(データポート_2)
	}

	if !書込みps2コマンド(0xAE) || !書込みps2コマンド(0x20) {
		return
	}
	状態, ok := 読込みps2データ()
	if !ok {
		return
	}
	状態 |= 0x01
	状態 &^= 0x10
	if !書込みps2コマンド(0x60) || !書込みps2データ(状態) {
		return
	}

	if !書込みps2データ(0xF4) {
		return
	}
	ack, ok := 読込みps2データ()
	if !ok || ack != 0xFA {
		return
	}

}

func 取っ手キーボード割込み(esp uint32) uint32 {
	if 有効キーボードドライバー == nil {
		Pポート読込みバイト(データポート_2)
		return esp
	}
	return 有効キーボードドライバー.H取っ手割込み(esp)
}

const キーボード待ち行列サイズ = 64

var キーボード待ち行列 [キーボード待ち行列サイズ]byte
var キーボード待ち行列読込み uint8
var キーボード待ち行列書込み uint8
var 左shift bool
var 右shift bool
var extendedスキャンcode bool

func 待ち行列キーボードバイト(鍵 byte) {
	次 := (キーボード待ち行列書込み + 1) % キーボード待ち行列サイズ
	if 次 == キーボード待ち行列読込み {
		return
	}
	キーボード待ち行列[キーボード待ち行列書込み] = 鍵
	キーボード待ち行列書込み = 次
}

func Pプロセス保留キーボード事象一覧() {
	for キーボード待ち行列読込み != キーボード待ち行列書込み {
		鍵 := キーボード待ち行列[キーボード待ち行列読込み]
		キーボード待ち行列読込み = (キーボード待ち行列読込み + 1) % キーボード待ち行列サイズ
		Stdinputバイト(鍵)
		if iキーボード事象handler != nil {
			iキーボード事象handler.O時鍵下(鍵)
		}
	}
}

func スキャンcodetoバイト(スキャンcode uint8) (byte, bool) {
	shift := 左shift || 右shift

	if スキャンcode >= 0x02 && スキャンcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[スキャンcode-0x02], true
		}
		return "1234567890"[スキャンcode-0x02], true
	}
	if スキャンcode >= 0x10 && スキャンcode <= 0x19 {
		鍵 := "qwertyuiop"[スキャンcode-0x10]
		if shift {
			鍵 -= 'a' - 'A'
		}
		return 鍵, true
	}
	if スキャンcode >= 0x1E && スキャンcode <= 0x26 {
		鍵 := "asdfghjkl"[スキャンcode-0x1E]
		if shift {
			鍵 -= 'a' - 'A'
		}
		return 鍵, true
	}
	if スキャンcode >= 0x2C && スキャンcode <= 0x32 {
		鍵 := "zxcvbnm"[スキャンcode-0x2C]
		if shift {
			鍵 -= 'a' - 'A'
		}
		return 鍵, true
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

func (self *Tキーボードドライバー) H取っ手割込み(esp uint32) uint32 {
	状態 := Pポート読込みバイト(コマンドポート_2)
	if (状態&0x01) == 0 || (状態&0x20) != 0 {
		return esp
	}

	スキャンcode := Pポート読込みバイト(データポート_2)
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
		左shift = !released
		return esp
	}
	if basecode == 0x36 {
		右shift = !released
		return esp
	}
	if released {
		return esp
	}

	if 鍵, ok := スキャンcodetoバイト(basecode); ok {
		待ち行列キーボードバイト(鍵)
	}

	return esp
}
