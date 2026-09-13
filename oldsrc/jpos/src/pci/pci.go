/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package pci

//import . "unsafe"
//import . "memorymanager"
//import . "amd_am79c973"
import . "port"
import . "interrupt"
import . "drivers/drivermanager"

/////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//		Register = 登録器
//		BaseAddress = 基準住所
//		BUS = 
//
/////////////////////////////////////////////////////////////////////////////////////////////////////////
type I周辺部品連結制御器_處理器 interface{
	M駆動装置を持つ同時(装置記述子 T周辺部品連結装置の識別子)
}
var i周辺部品連結制御器_處理器 I周辺部品連結制御器_處理器
type T基本周辺部品連結制御器_處理器 struct{
}
func (自身 T基本周辺部品連結制御器_處理器) M駆動装置を持つ同時(装置記述子 T周辺部品連結装置の識別子) {
}

type T基準住所_登録器 struct {		// BaseAddressRegister
	プリフェッチ가능 bool			// prefetchable
	住所 uint32				// address
	登録器_類型 uint8			// register type
}
type T周辺部品連結装置の識別子 struct {
	P入出力ポート基準 uint32
	P割り込み uint32
	
	バス uint16			// bus
	装置 uint16			// device
	関数 uint16			// function
	
	P売り手の識別子 uint16		// vendor id
	P装置_識別子 uint16		// device id

	種類_識別子 uint8		// class id
	補助種類_識別子 uint8		// subclass id
	接続_識別子 uint8		// interface id

	変更 uint8			// revision
	
}

func (自身 *T周辺部品連結装置の識別子) Init() {
}

//////////////////////////////////////////////////////////////////////////////
type T周辺部品連結制御器 struct {
	i周辺部品連結制御器_處理器 I周辺部品連結制御器_處理器
	データ入出力ポート Tダブルワード入出力ポート
	命令語入出力ポート Tダブルワード入出力ポート
}

func (自身 *T周辺部品連結制御器) M初期化(i周辺部品連結制御器_處理器 I周辺部品連結制御器_處理器) {
	自身.データ入出力ポート.M初期化(0xCFC)
	自身.命令語入出力ポート.M初期化(0xCF8)
	
	自身.i周辺部品連結制御器_處理器 = T基本周辺部品連結制御器_處理器{}
	if i周辺部品連結制御器_處理器 != nil{
		自身.i周辺部品連結制御器_處理器 = i周辺部品連結制御器_處理器
	}
}
func (自身 *T周辺部品連結制御器) M読み取り(バス uint16, 装置 uint16, 関数 uint16, registeroffset uint32) uint32{
	var id uint32 = 0
	id = 0x1<<31 | (uint32(バス & 0xFF) << 16)  | (uint32(装置 & 0x1f) << 11) | (uint32(関数 & 0x07) << 8) | uint32(registeroffset & 0xFC)

	自身.命令語入出力ポート.M作成(id)
	
	けっか1 := 自身.データ入出力ポート.M読み取り()
	けっか2 := (けっか1 >> (8*(registeroffset %4)))

	return けっか2
}

func (自身 *T周辺部品連結制御器) M作成(バス uint16, 装置 uint16, 関数 uint16, registeroffset uint32, 値 uint32) {
	var id uint32
	id = 0x1 << 31 | uint32((バス & 0xFF) << 16)  | uint32((装置 & 0x1f) << 11) | uint32((関数 & 0x07) << 8) | uint32(registeroffset & 0xFC)
	自身.命令語入出力ポート.M作成(id)
	自身.データ入出力ポート.M作成(値)
}
func (自身 *T周辺部品連結制御器) DeviceHasFunctions(バス uint16, 装置 uint16) bool{
	けっか := 自身.M読み取り(バス, 装置, 0, 0x0E)
	if (けっか & (1<<7)) != 0 {
		return true
	}else {
		return false
	}
}
func (自身 *T周辺部品連結制御器) M駆動装置を選択(駆動装置の管理者 *T駆動装置の管理者, 割り込み들 *T割り込み_管理者) {
	for バス:=0; バス<8; バス++ {
		for 装置:=0; 装置<32; 装置++ {

			var 関数個数 int = 1
			if 自身.DeviceHasFunctions(uint16(バス), uint16(装置)) == true {
				関数個数 = 8
			}else{
				関数個数 = 1
			}
		

			for 関数:=0; 関数<関数個数; 関数++ {
				var 装置記述子 T周辺部品連結装置の識別子
				装置記述子 = 自身.M装置技術者を取得する(uint16(バス), uint16(装置), uint16(関数))
				if 装置記述子.P売り手の識別子 == 0x0000 || 装置記述子.P売り手の識別子 == 0xFFFF {
					continue
				}
	
				for 基準住所_登録器_番号:=0; 基準住所_登録器_番号<6; 基準住所_登録器_番号++ {
					var 基準住所_登録器 T基準住所_登録器 = 自身.M基準住所登録器を取得する(uint16(バス), uint16(装置), uint16(関数), uint16(基準住所_登録器_番号))
					if 基準住所_登録器.住所 != 0 && (基準住所_登録器.登録器_類型 == 1) { // 基準住所_登録器.登録器_類型 == inputoutput
						装置記述子.P入出力ポート基準 = 基準住所_登録器.住所
					}
				
					自身.M駆動装置を取得する(装置記述子, 割り込み들)
			
				}

			}

		}
	}
}
func (自身 *T周辺部品連結制御器) M装置技術者を取得する(バス uint16, 装置 uint16, 関数 uint16) T周辺部品連結装置の識別子{
	var 周辺部品連結装置の識別子 T周辺部品連結装置の識別子
	周辺部品連結装置の識別子 = T周辺部品連結装置の識別子{}
	周辺部品連結装置の識別子.バス = バス
	周辺部品連結装置の識別子.装置 = 装置
	周辺部品連結装置の識別子.関数 = 関数

	周辺部品連結装置の識別子.P売り手の識別子 = uint16(自身.M読み取り(バス, 装置, 関数, 0x00))
	周辺部品連結装置の識別子.P装置_識別子 = uint16(自身.M読み取り(バス, 装置, 関数, 0x02))

	周辺部品連結装置の識別子.種類_識別子 = uint8(自身.M読み取り(バス, 装置, 関数, 0x0b))
	周辺部品連結装置の識別子.補助種類_識別子 = uint8(自身.M読み取り(バス, 装置, 関数, 0x0a))
	周辺部品連結装置の識別子.接続_識別子 = uint8(自身.M読み取り(バス, 装置, 関数, 0x09))

	周辺部品連結装置の識別子.変更 = uint8(自身.M読み取り(バス, 装置, 関数, 0x08))
	周辺部品連結装置の識別子.P割り込み = uint32(自身.M読み取り(バス, 装置, 関数, 0x3C))

	return 周辺部品連結装置の識別子
}
func (自身 *T周辺部品連結制御器) M基準住所登録器を取得する(バス uint16, 装置 uint16, 関数 uint16, bar uint16) T基準住所_登録器 {
	var けっか T基準住所_登録器
	
	頭文字_類型 := 自身.M読み取り(バス, 装置, 関数, 0x0E) & 0x7F
	var 最大基準住所_登録器 int = int(6-(4*頭文字_類型))
	if bar >= uint16(最大基準住所_登録器) {
		return けっか
	}

	基準住所登録器_値 := 自身.M読み取り(バス, 装置, 関数, uint32(0x10+4*bar))

	if (基準住所登録器_値 & 0x1) != 0 {
		けっか.登録器_類型 = 1
	} else {
		けっか.登録器_類型 = 0
	}

	if けっか.登録器_類型 == 0 { // memorymapping
	} else {
		けっか.住所 = 基準住所登録器_値 & ^uint32(0x3)
		けっか.プリフェッチ가능 = false
	}

	return けっか
}
func (自身 *T周辺部品連結制御器) M駆動装置を取得する(装置記述子 T周辺部品連結装置の識別子, interrupts *T割り込み_管理者) {//IDriver {
	//var iDriver IDriver = nil

	自身.i周辺部品連結制御器_處理器.M駆動装置を持つ同時(装置記述子)
	/*
	switch 装置記述子.P売り手の識別子 {
		case 0x1022:	 // AMD
			switch 装置記述子.P装置_識別子 {
				case 0x2000:
					//iDriver = *(*IDriver)(Pointer(ActiveMemoryManager.Malloc(100)))
					if iDriver != nil {
						//(IDriver) amd_am79c973.Init(&装置記述子, interrupts)
					}
					return iDriver
					break
			}
			break

		case 0x8086:	//INTEL
			break
	}

	switch 装置記述子.種類_識別子 {
		case 0x03:
			switch 装置記述子.補助種類_識別子 {
				case 0x00: // vga	
				break
			}
			break
	}
	return iDriver
	*/

}
