package vga

import . "unsafe"
import . "port"
////////////////////////////////////////////////////////////////////////////////////
//
//	映像図形配列 = ビデオグラフィックアレイ = VideoGraphicsArray = VGA
//	Register = 登録器
//
////////////////////////////////////////////////////////////////////////////////////
type T映像図形配列 struct{
}
type T映像図形配列_変数たち struct{
	その他作業_バイト入出力ポート 			Tバイト入出力ポート		// Miscellaneous output register, read(0x03cc), write(0x03c2)
	陰極線管制御器_索引_バイト入出力ポート 		Tバイト入出力ポート		// crtcIndexPort, CRT Controller Register(address register)
	陰極線管制御器_資料_バイト入出力ポート 		Tバイト入出力ポート		// crtcDataPort, CRT Controller Register(DAta register)
	シーケンサ_索引_バイト入出力ポート 		Tバイト入出力ポート		// sequencerIndexPort
	シーケンサ_資料_バイト入出力ポート 		Tバイト入出力ポート		// sequencerDataPort
	グラフィック制御器_索引_バイト入出力ポート 	Tバイト入出力ポート		// graphicsControllerIndexPort
	グラフィック制御器_資料_バイト入出力ポート 	Tバイト入出力ポート		// graphicsControllerDataPort
	属性制御器_索引_バイト入出力ポート 		Tバイト入出力ポート		// attributeControllerIndexPort
	属性制御器_取得_バイト入出力ポート 		Tバイト入出力ポート		// attributeControllerReadPort
	属性制御器_作成_バイト入出力ポート 		Tバイト入出力ポート		// attributeControllerWritePort
	属性制御器_再設定_バイト入出力ポート 		Tバイト入出力ポート		// attributeControlllerResetPort
}
func (自身 *T映像図形配列_変数たち) M初期化(){
	自身.その他作業_バイト入出力ポート.M初期化(0x3c2)
	自身.陰極線管制御器_索引_バイト入出力ポート.M初期化(0x3d4)
	自身.陰極線管制御器_資料_バイト入出力ポート.M初期化(0x3d5)
	自身.シーケンサ_索引_バイト入出力ポート.M初期化(0x3c4)
	自身.シーケンサ_資料_バイト入出力ポート.M初期化(0x3c5)
	自身.グラフィック制御器_索引_バイト入出力ポート.M初期化(0x3ce)
	自身.グラフィック制御器_資料_バイト入出力ポート.M初期化(0x3cf)
	自身.属性制御器_索引_バイト入出力ポート.M初期化(0x3c0)
	自身.属性制御器_取得_バイト入出力ポート.M初期化(0x3c1)
	自身.属性制御器_作成_バイト入出力ポート.M初期化(0x3c0)
	自身.属性制御器_再設定_バイト入出力ポート.M初期化(0x3da)
}
var 変数たち T映像図形配列_変数たち

func (自身 *T映像図形配列) 登録器_作成(登録器 []byte){
	var regIndex uint16 = 0

	変数たち.M初期化()

	変数たち.その他作業_バイト入出力ポート.M作成(登録器[regIndex])
	regIndex++

	var i uint8
	for i=0; i<5; i++ {
		変数たち.シーケンサ_索引_バイト入出力ポート.M作成(i)
		変数たち.シーケンサ_資料_バイト入出力ポート.M作成(登録器[regIndex])
		regIndex++
	}
	
	変数たち.陰極線管制御器_索引_バイト入出力ポート.M作成(0x03)
	変数たち.陰極線管制御器_資料_バイト入出力ポート.M作成((変数たち.陰極線管制御器_資料_バイト入出力ポート.M読み取り() | 0x80))
	変数たち.陰極線管制御器_索引_バイト入出力ポート.M作成(0x11)
	変数たち.陰極線管制御器_資料_バイト入出力ポート.M作成((変数たち.陰極線管制御器_資料_バイト入出力ポート.M読み取り() & ^uint8(0x80)))

	登録器[0x03] = 登録器[0x03] | 0x80
	登録器[0x11] = 登録器[0x11] & ^uint8(0x80)

	for i=0; i<25; i++ {
		変数たち.陰極線管制御器_索引_バイト入出力ポート.M作成(i)
		変数たち.陰極線管制御器_資料_バイト入出力ポート.M作成(登録器[regIndex])
		regIndex++
	}

	for i=0; i<9; i++ {
		変数たち.グラフィック制御器_索引_バイト入出力ポート.M作成(i)
		変数たち.グラフィック制御器_資料_バイト入出力ポート.M作成(登録器[regIndex])
		regIndex++
	}
	
	for i=0; i<21; i++ {
		変数たち.属性制御器_再設定_バイト入出力ポート.M読み取り()
		変数たち.属性制御器_索引_バイト入出力ポート.M作成(i)
		変数たち.属性制御器_作成_バイト入出力ポート.M作成(登録器[regIndex])
		regIndex++
	}

	変数たち.属性制御器_再設定_バイト入出力ポート.M読み取り()
	変数たち.属性制御器_索引_バイト入出力ポート.M作成(0x20)
	
}

func (自身 *T映像図形配列) GetFrameBufferSegment() uintptr{
	変数たち.グラフィック制御器_索引_バイト入出力ポート.M作成(0x06)
	var segmentNumber uint8 = ((変数たち.グラフィック制御器_資料_バイト入出力ポート.M読み取り() >> 2) & 0x03)
	switch segmentNumber {
		case 0: return uintptr(0x00000)
		case 1: return uintptr(0xa0000)
		case 2: return uintptr(0xb0000)
		case 3: return uintptr(0xb8000)
	}
	
	return uintptr(0xB0000)
}
func (自身 *T映像図形配列) M画素入れ(x uint32, y uint32, colorIndex uint8){
	if x<0 || 320 <= x || y<0 || 200 <= y {
		return
	}

	var 画素住所 uintptr = 自身.GetFrameBufferSegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(画素住所)) = colorIndex

}
func (自身 *T映像図形配列) GetColorIndex(赤 uint8, 緑 uint8, 青 uint8) uint8{
	if 赤==0x00 && 緑==0x00 && 青==0x00 { return 0x00 } // black
	if 赤==0x00 && 緑==0x00 && 青==0xA8 { return 0x01 } // blue
	if 赤==0x00 && 緑==0xA8 && 青==0x00 { return 0x02 } // green
	if 赤==0xA8 && 緑==0x00 && 青==0x00 { return 0x04 } // red
	if 赤==0xFF && 緑==0xFF && 青==0xFF { return 0x3F } // white

	return 0x01
}
func (自身 *T映像図形配列) M画素_赤緑青_入れ(x uint32, y uint32, 赤 uint8, 緑 uint8, 青 uint8){
	自身.M画素入れ(x, y, 自身.GetColorIndex(赤, 緑, 青))
}
func (自身 *T映像図形配列) M사각형채우기(x uint32, y uint32, 幅 uint32, 高 uint32, 赤 uint8, 緑 uint8, 青 uint8) {
	for Y:=y; Y<y+高; Y++ {
		for X:=x; X<x+幅; X++ {
			自身.M画素_赤緑青_入れ(X, Y, 赤, 緑, 青)
		}
	}
}
func (自身 *T映像図形配列) M動作状態_支援の有無(幅 uint32, 高 uint32, 色深度 uint32) bool {
	return 幅==320 && 高==200 && 色深度==8
}
func (自身 *T映像図形配列) M動作状態_設定(幅 uint32, 高 uint32, 色深度 uint32) bool{
	if !自身.M動作状態_支援の有無(幅, 高, 色深度) {
		return false
	}

	var g_320x200x256 = []byte {
	/* MISC */
	0x63,
	/* SEQ */
	0x03, 0x01, 0x0F, 0x00, 0x0E,
	/* CRTC */
	0x5F, 0x4F, 0x50, 0x82, 0x54, 0x80, 0xBF, 0x1F,
	0x00, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x9C, 0x0E, 0x8F, 0x28,	0x40, 0x96, 0xB9, 0xA3,
	0xFF,
	/* GC */
	0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x05, 0x0F,
	0xFF,
	/* AC */
	0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
	0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
	0x41, 0x00, 0x0F, 0x00,	0x00 }


	自身.登録器_作成(g_320x200x256)

	return true	
}

