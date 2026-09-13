package キーボード

import . "unsafe"

import . "ポート"
import . "割込み"
import . "コンソール"

type Iマウス事象handler interface {
	O時マウス下(ボタン int8)
	O時マウス上へ(ボタン int8)
	O時マウス移動(x int8, y int8)
}

var iマウス事象handler Iマウス事象handler

type Tデフォルトマウス事象handler struct {
}

var コンソール_2 Tコンソール = Tコンソール{}
var previousx int16 = 0
var previousy int16 = 0
var x配置 int16 = 0
var y配置 int16 = 0

func (self Tデフォルトマウス事象handler) O時マウス下(ボタン int8) {
	buffer := []byte("+")
	コンソール_2.M印刷xy(buffer, uint16(previousx), uint16(previousy))
}
func (self Tデフォルトマウス事象handler) O時マウス上へ(ボタン int8)	{}
func (self Tデフォルトマウス事象handler) O時マウス移動(x int8, y int8) {

	x配置 += int16(x)
	if x配置 < 0 {
		x配置 = 0
	}
	if x配置 >= 80 {
		x配置 = 79
	}

	y配置 -= int16(y)

	if y配置 < 0 {
		y配置 = 0
	}
	if y配置 >= 25 {
		y配置 = 24
	}

	buffer := []byte(" ")
	コンソール_2.M印刷xy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	コンソール_2.M印刷xy(buffer, uint16(x配置), uint16(y配置))

	previousx = x配置
	previousy = y配置
}

type Tマウスドライバー struct {
	T割込みhandler
}

var 有効マウスドライバー *Tマウスドライバー
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

func 送信マウスコマンド(値 uint8) bool {
	if !書込みps2コマンド(0xD4) || !書込みps2データ(値) {
		return false
	}
	ack, ok := 読込みps2データ()
	return ok && ack == 0xFA
}

func (self *Tマウスドライバー) Initドライバー(管理者 *T割込み管理者, マウス事象handler Iマウス事象handler) {

	iマウス事象handler = Tデフォルトマウス事象handler{}

	if マウス事象handler != nil {
		iマウス事象handler = マウス事象handler
	}

	有効マウスドライバー = self
	割込みhandler = 取っ手マウス割込み
	var address uintptr
	address = uintptr(Pointer(&割込みhandler))
	self.Init(0x2C, uintptr(Pointer(管理者)), address)

	for i := 0; i < 32 && (Pポート読込みバイト(コマンドポート_2)&0x01) != 0; i++ {
		Pポート読込みバイト(データポート_2)
	}

	if !書込みps2コマンド(0xA8) || !書込みps2コマンド(0x20) {
		return
	}
	状態, ok := 読込みps2データ()
	if !ok {
		return
	}
	状態 |= 0x02
	状態 &^= 0x20
	if !書込みps2コマンド(0x60) || !書込みps2データ(状態) {
		return
	}

	if !送信マウスコマンド(0xF6) || !送信マウスコマンド(0xF4) {
		return
	}
	offset = 0

}

func 取っ手マウス割込み(esp uint32) uint32 {
	if 有効マウスドライバー == nil {
		Pポート読込みバイト(データポート_2)
		return esp
	}
	return 有効マウスドライバー.H取っ手割込み(esp)
}

var カウント uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var ボタン_2 int8
var 保留x int16
var 保留y int16
var 保留ボタン int8
var 保留マウス事象 bool

func (self *Tマウスドライバー) H取っ手割込み(esp uint32) uint32 {
	状態 := Pポート読込みバイト(コマンドポート_2)
	if (状態&0x01) == 0 || (状態&0x20) == 0 {
		return esp
	}

	データ := Pポート読込みバイト(データポート_2)

	if offset == 0 && (データ&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(データ)
	offset = (offset + 1) % 3
	if offset == 0 {
		packet状態 := uint8(buffer_2[0])

		if (packet状態 & 0xC0) == 0 {
			保留x += int16(buffer_2[1])
			保留y += int16(buffer_2[2])
			if 保留x > 127 {
				保留x = 127
			} else if 保留x < -127 {
				保留x = -127
			}
			if 保留y > 127 {
				保留y = 127
			} else if 保留y < -127 {
				保留y = -127
			}
		}
		保留ボタン = int8(packet状態 & 0x07)
		保留マウス事象 = true
	}

	return esp

}

func Pプロセス保留マウス事象一覧() {
	if iマウス事象handler == nil {
		return
	}

	I割込みdeactive()
	if !保留マウス事象 {
		I割込み有効()
		return
	}
	x := int8(保留x)
	y := int8(保留y)
	新規ボタン := 保留ボタン
	oldボタン := ボタン_2

	保留x = 0
	保留y = 0
	保留マウス事象 = false
	I割込み有効()

	if x != 0 || y != 0 {
		iマウス事象handler.O時マウス移動(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		マスク := int8(0x1 << i)
		if (新規ボタン & マスク) != (oldボタン & マスク) {
			if (新規ボタン & マスク) != 0 {
				iマウス事象handler.O時マウス下(int8(i + 1))
			} else {
				iマウス事象handler.O時マウス上へ(int8(i + 1))
			}
		}
	}
	ボタン_2 = 新規ボタン
}
