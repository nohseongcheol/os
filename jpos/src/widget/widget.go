package widget

//import . "drivers/keyboard"
//import . "drivers/mouse"
import . "vga"

type Iウィジェット interface{
	M初期化(parent Iウィジェット, x uint32, y uint32, 幅 uint32, 高 uint32, 赤 uint32, 緑 uint32, 青 uint32)
	Mフォーカスを得る(widget Iウィジェット)
	ModelToScreen(x int32, y int32)	
	M色設定(赤 uint32, 緑 uint32, 青 uint32)
	M描く(映像図形配列 *T映像図形配列)
 	ContainsCoordinate(x uint32, y uint32) bool
	//Mマウス押し同時(ボタン int8)
	//OnMouseUp(ボタン int8)
	//OnMouseMove(x int8, y int8)
}


type Tウィジェット struct {
	parent Iウィジェット
	x uint32
	y uint32
	幅 uint32
	高 uint32

	赤 uint32
	緑 uint32
	青 uint32
	
	Focussable bool
}
func (自身 *Tウィジェット) M初期化(parent Iウィジェット, x uint32, y uint32, 幅 uint32, 高 uint32, 赤 uint32, 緑 uint32, 青 uint32) {

	自身.parent = parent
	
	自身.x = x
	自身.y = y
	自身.幅 = 幅
	自身.高 = 高
	
	自身.赤 = 赤
	自身.緑 = 緑 
	自身.青 = 青

	自身.Focussable = true
	

}
func (自身 *Tウィジェット) Mフォーカスを得る(widget Iウィジェット){
	if 自身.parent != nil {
		自身.parent.Mフォーカスを得る(widget)
	}
}
func (自身 *Tウィジェット) ModelToScreen(x uint32, y uint32){
	if 自身.parent != nil {
		//自身.parent.ModelToScreen(x, y)
	}
	自身.x = x
	自身.y = y

	//*x += 自身.x
	//*y += 自身.y
}
func (自身 *Tウィジェット) M色設定(赤 uint32, 緑 uint32, 青 uint32){
	自身.赤 = 赤
	自身.緑 = 緑
	自身.青 = 青
}

func (自身 *Tウィジェット) M描く(映像図形配列 *T映像図形配列){
	映像図形配列.M사각형채우기(自身.x, 自身.y, 自身.幅, 自身.高, uint8(自身.赤), uint8(自身.緑), uint8(自身.青))
}

func (自身 *Tウィジェット) ContainsCoordinate(x uint32, y uint32) bool { 
	return 自身.x <= x && x < (自身.x+自身.幅) && 自身.y <= y && y < (自身.y + 自身.高)
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////
type Tウィジェットマウス事件處理器_変数たち struct{
	マウスウィジェット Tウィジェット
	マウス_映像図形配列 T映像図形配列
	以前X位置 int16
	以前Y位置 int16
	現在X位置 int16
	現在Y位置 int16
}
func (自身 *Tウィジェットマウス事件處理器_変数たち) M初期化(){
	自身.以前X位置 = 0
	自身.以前Y位置 = 0
	自身.現在X位置 = 0
	自身.現在Y位置 = 0
}
var 変数たち Tウィジェットマウス事件處理器_変数たち

type Tウィジェットマウス事件處理器 struct{
}
func (自身 *Tウィジェットマウス事件處理器) M初期化(widget Tウィジェット, 映像図形配列 T映像図形配列){
	変数たち.マウスウィジェット = widget
	変数たち.マウス_映像図形配列 = 映像図形配列
	変数たち.M初期化()
}
func (自身 *Tウィジェットマウス事件處理器) Mマウス押し同時(ボタン int8){

	変数たち.マウスウィジェット.ModelToScreen(uint32(変数たち.以前X位置), uint32(変数たち.以前Y位置))
	変数たち.マウスウィジェット.M色設定(0xA8, 0x00, 0x00)
	変数たち.マウスウィジェット.M描く(&変数たち.マウス_映像図形配列)

	//変数たち.マウスウィジェット.ModelToScreen(変数たち.以前X位置, 変数たち.以前Y位置)
	
	変数たち.マウスウィジェット.M描く(&変数たち.マウス_映像図形配列)
	/*
	if 自身.Focussable {
		自身.Mフォーカスを得る(自身)
	}
	*/
}

func (自身 *Tウィジェットマウス事件處理器) Mマウス離し同時(ボタン int8) {
}

func (自身 *Tウィジェットマウス事件處理器) Mマウス動かし同時(x int8, y int8) {
        変数たち.現在X位置 += int16(x)
        if 変数たち.現在X位置 < 0 { 変数たち.現在X位置=0 }
        if 変数たち.現在X位置 >= 320 { 変数たち.現在X位置 = 320 }

        変数たち.現在Y位置 -= int16(y)

        if 変数たち.現在Y位置 < 0 { 変数たち.現在Y位置 = 0 }
        if 変数たち.現在Y位置 >= 200 { 変数たち.現在Y位置 = 200 }
	
	変数たち.マウスウィジェット.ModelToScreen(uint32(変数たち.以前X位置), uint32(変数たち.以前Y位置))
	変数たち.マウスウィジェット.M色設定(0x00, 0x00, 0x00)
	変数たち.マウスウィジェット.M描く(&変数たち.マウス_映像図形配列)
	
	変数たち.マウスウィジェット.ModelToScreen(uint32(変数たち.現在X位置), uint32(変数たち.現在Y位置))
	変数たち.マウスウィジェット.M色設定(0x00, 0x00, 0xA8)
	変数たち.マウスウィジェット.M描く(&変数たち.マウス_映像図形配列)

        変数たち.以前X位置 = 変数たち.現在X位置
        変数たち.以前Y位置 = 変数たち.現在Y位置

}
