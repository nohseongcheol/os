/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package widget

import . "vga"

type I위젯 interface{
	M초기화(부모 I위젯, x위치 uint32, y위치 uint32, 넓이 uint32, 높이 uint32, 적 uint32, 녹 uint32, 청 uint32)
	M포커스얻기(위젯 I위젯)
	M모델에서_화면으로(x int32, y int32)	
	M색설정(적 uint32, 녹 uint32, 청 uint32)
	M그리기(비디오그래픽배열 *T비디오그래픽배열)
 	M좌표포함여부(x uint32, y uint32) bool
}


type T위젯 struct {
	부모 I위젯
	x위치 uint32
	y위치 uint32
	넓이 uint32
	높이 uint32

	적 uint32
	녹 uint32
	청 uint32
	
	초점잡힘여부 bool
}
func (자신 *T위젯) M초기화(부모 I위젯, x위치 uint32, y위치 uint32, 넓이 uint32, 높이 uint32, 적 uint32, 녹 uint32, 청 uint32) {

	자신.부모 = 부모
	
	자신.x위치 = x위치
	자신.y위치 = y위치
	자신.넓이 = 넓이
	자신.높이 = 높이
	
	자신.적 = 적
	자신.녹 = 녹
	자신.청 = 청

	자신.초점잡힘여부 = true
	

}
func (자신 *T위젯) M포커스얻기(위젯 I위젯){
	if 자신.부모 != nil {
		자신.부모.M포커스얻기(위젯)
	}
}
func (자신 *T위젯) M모델에서_화면으로(x위치 uint32, y위치 uint32){
	if 자신.부모 != nil {
		//자신.부모.M모델에서_화면으로(x, y)
	}
	자신.x위치 = x위치
	자신.y위치 = y위치

}
func (자신 *T위젯) M색설정(적 uint32, 녹 uint32, 청 uint32){
	자신.적 = 적
	자신.녹 = 녹
	자신.청 = 청
}

func (자신 *T위젯) M그리기(비디오그래픽배열  *T비디오그래픽배열){
	비디오그래픽배열.M사각형채우기(자신.x위치, 자신.y위치, 자신.넓이, 자신.높이, uint8(자신.적), uint8(자신.녹), uint8(자신.청))
}

func (자신 *T위젯) M좌표포함여부(x uint32, y uint32) bool { 
	return 자신.x위치 <= x && x < (자신.x위치+자신.넓이) && 자신.y위치 <= y && y < (자신.y위치 + 자신.높이)
}

type T위젯마우스사건처리기 struct{
}
var 마우스_위젯 T위젯
var 마우스_비디오그래픽배열 T비디오그래픽배열
var 이전x위치 int16 = 0
var 이전y위치 int16 = 0
var x위치 int16 = 0
var y위치 int16 = 0

func (자신 *T위젯마우스사건처리기) M초기화(위젯 T위젯, 비디오그래픽배열 T비디오그래픽배열){
	마우스_위젯 = 위젯
	마우스_비디오그래픽배열 = 비디오그래픽배열
}
func (자신 *T위젯마우스사건처리기) M마우스누른동시(버튼 int8){

	마우스_위젯.M모델에서_화면으로(uint32(이전x위치), uint32(이전y위치))
	마우스_위젯.M색설정(0xA8, 0x00, 0x00)
	마우스_위젯.M그리기(&마우스_비디오그래픽배열)

	
	마우스_위젯.M그리기(&마우스_비디오그래픽배열)
}

func (자신 *T위젯마우스사건처리기) M마우스떼는동시(버튼 int8) {
}

func (자신 *T위젯마우스사건처리기) M마우스움직인동시(x int8, y int8) {
        x위치 += int16(x)
        if x위치 < 0 { x위치=0 }
        if x위치 >= 320 { x위치 = 320 }

        y위치 -= int16(y)

        if y위치 < 0 { y위치 = 0 }
        if y위치 >= 200 { y위치 = 200 }
	
	마우스_위젯.M모델에서_화면으로(uint32(이전x위치), uint32(이전y위치))
	마우스_위젯.M색설정(0x00, 0x00, 0x00)
	마우스_위젯.M그리기(&마우스_비디오그래픽배열)
	
	마우스_위젯.M모델에서_화면으로(uint32(x위치), uint32(y위치))
	마우스_위젯.M색설정(0x00, 0x00, 0xA8)
	마우스_위젯.M그리기(&마우스_비디오그래픽배열)

        이전x위치 = x위치
        이전y위치 = y위치

}
/*
type ICompositeWidget interface {
}
type TCompositeWidget struct {
	*T위젯
	children[100] I위젯 
	numChildren int
	FocussedChild I위젯
}

func (자신 *TCompositeWidget) M초기화(parent I위젯, x uint32, y uint32, w uint32, h uint32, r uint32, g uint32, b uint32) {
	자신.T위젯.M초기화(parent, x, y, w, h, r, g, b)

	자신.FocussedChild = nil
	자신.numChildren = 0

}
func (자신 *TCompositeWidget) M포커스얻기(widget I위젯) {
	자신.FocussedChild = widget
	if 자신.T위젯.parent != nil {
		자신.T위젯.parent.M포커스얻기(자신.T위젯)
	}
}
func (자신 *TCompositeWidget) AddChild(child I위젯) bool{
	if 자신.numChildren >= 100 {
		return false
	}
	자신.children[자신.numChildren] = child
	자신.numChildren++
	return true
}
func (자신 *TCompositeWidget) M그리기(vga *T비디오그래픽배열) {
	자신.T위젯.M그리기(vga)
	for i:=자신.numChildren-1; i>=0; i-- {
		자신.children[i].M그리기(vga)
	}
}
func (자신 *TCompositeWidget) M마우스누른동시(x uint32, y uint32, 버튼 uint8){
	for i:=0; i<자신.numChildren; i++ {
		if 자신.children[i].M좌표포함여부(x - 자신.T위젯.x, y - 자신.T위젯.y) {
			자신.children[i].M마우스누른동시(x-자신.x위치, y-자신.y위치, 버튼)
			break
		}
	}
}

func (자신 *TCompositeWidget) OnMouseUp(x uint32, y uint32, 버튼 uint8) { 
	for i:=0; i<자신.numChildren; i++ {
		if 자신.children[i].M좌표포함여부(x - 자신.T위젯.x, y - 자신.T위젯.y) {
			자신.children[i].OnMouseUp(x-자신.x위치, y-자신.y위치, 버튼)
			break
		}
	}
}

func (자신 *TCompositeWidget) OnMouseMove(oldx uint32, oldy uint32, newx uint32, newy uint32) {
	var firstchild int = -1
        for i:=0; i<자신.numChildren; i++ {
                if 자신.children[i].M좌표포함여부(oldx-자신.T위젯.x, oldy-자신.T위젯.y) {
                        자신.children[i].OnMouseMove(oldx-자신.x위치, oldy-자신.y위치, newx-자신.x위치, newy-자신.y위치)
			firstchild = i
                        break
                }
        }

        for i:=0; i<자신.numChildren; i++ {
                if 자신.children[i].M좌표포함여부(newx-자신.T위젯.x, newy-자신.T위젯.y) {
			if firstchild != i {
                        	자신.children[i].OnMouseMove(oldx-자신.x위치, oldy-자신.y위치, newx-자신.x위치, newy-자신.y위치)
			}
                        break 
                }
        }

	
}

func (자신 *TCompositeWidget) OnKeyDown(key byte) {
	if 자신.FocussedChild != nil {
		자신.FocussedChild.OnKeyDown(key)
	}
}

func (자신 *TCompositeWidget) OnKeyUp(key byte) {
}
*/
