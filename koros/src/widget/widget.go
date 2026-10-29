/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package widget

//import . "drivers/keyboard"
//import . "drivers/mouse"
import . "vga"

type I위젯 interface{
	M초기화(parent I위젯, x uint32, y uint32, 넓이 uint32, 높이 uint32, 적 uint32, 녹 uint32, 청 uint32)
	M포커스얻기(widget I위젯)
	ModelToScreen(x int32, y int32)	
	M색설정(적 uint32, 녹 uint32, 청 uint32)
	M그리기(영상도형배열 *T영상도형배열)
 	ContainsCoordinate(x uint32, y uint32) bool
	//M마우스누른동시(버튼 int8)
	//OnMouseUp(버튼 int8)
	//OnMouseMove(x int8, y int8)
}


type T위젯 struct {
	parent I위젯
	x uint32
	y uint32
	넓이 uint32
	높이 uint32

	적 uint32
	녹 uint32
	청 uint32
	
	Focussable bool
}
func (자신 *T위젯) M초기화(parent I위젯, x uint32, y uint32, 넓이 uint32, 높이 uint32, 적 uint32, 녹 uint32, 청 uint32) {

	자신.parent = parent
	
	자신.x = x
	자신.y = y
	자신.넓이 = 넓이
	자신.높이 = 높이
	
	자신.적 = 적
	자신.녹 = 녹 
	자신.청 = 청

	자신.Focussable = true
	

}
func (자신 *T위젯) M포커스얻기(widget I위젯){
	if 자신.parent != nil {
		자신.parent.M포커스얻기(widget)
	}
}
func (자신 *T위젯) ModelToScreen(x uint32, y uint32){
	if 자신.parent != nil {
		//자신.parent.ModelToScreen(x, y)
	}
	자신.x = x
	자신.y = y

	//*x += 자신.x
	//*y += 자신.y
}
func (자신 *T위젯) M색설정(적 uint32, 녹 uint32, 청 uint32){
	자신.적 = 적
	자신.녹 = 녹
	자신.청 = 청
}

func (자신 *T위젯) M그리기(영상도형배열 *T영상도형배열){
	영상도형배열.M사각형채우기(자신.x, 자신.y, 자신.넓이, 자신.높이, uint8(자신.적), uint8(자신.녹), uint8(자신.청))
}

func (자신 *T위젯) ContainsCoordinate(x uint32, y uint32) bool { 
	return 자신.x <= x && x < (자신.x+자신.넓이) && 자신.y <= y && y < (자신.y + 자신.높이)
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////
type T위젯마우스사건처리기_변수들 struct{
	마우스위젯 T위젯
	마우스_영상도형배열 T영상도형배열
	이전X위치 int16
	이전Y위치 int16
	현재X위치 int16
	현재Y위치 int16
}
func (자신 *T위젯마우스사건처리기_변수들) M초기화(){
	자신.이전X위치 = 0
	자신.이전Y위치 = 0
	자신.현재X위치 = 0
	자신.현재Y위치 = 0
}
var 변수들 T위젯마우스사건처리기_변수들

type T위젯마우스사건처리기 struct{
}
func (자신 *T위젯마우스사건처리기) M초기화(widget T위젯, 영상도형배열 T영상도형배열){
	변수들.마우스위젯 = widget
	변수들.마우스_영상도형배열 = 영상도형배열
	변수들.M초기화()
}
func (자신 *T위젯마우스사건처리기) M마우스누른동시(버튼 int8){

	변수들.마우스위젯.ModelToScreen(uint32(변수들.이전X위치), uint32(변수들.이전Y위치))
	변수들.마우스위젯.M색설정(0xA8, 0x00, 0x00)
	변수들.마우스위젯.M그리기(&변수들.마우스_영상도형배열)

	//변수들.마우스위젯.ModelToScreen(변수들.이전X위치, 변수들.이전Y위치)
	
	변수들.마우스위젯.M그리기(&변수들.마우스_영상도형배열)
	/*
	if 자신.Focussable {
		자신.M포커스얻기(자신)
	}
	*/
}

func (자신 *T위젯마우스사건처리기) M마우스떼는동시(버튼 int8) {
}

func (자신 *T위젯마우스사건처리기) M마우스움직인동시(x int8, y int8) {
        변수들.현재X위치 += int16(x)
        if 변수들.현재X위치 < 0 { 변수들.현재X위치=0 }
        if 변수들.현재X위치 >= 320 { 변수들.현재X위치 = 320 }

        변수들.현재Y위치 -= int16(y)

        if 변수들.현재Y위치 < 0 { 변수들.현재Y위치 = 0 }
        if 변수들.현재Y위치 >= 200 { 변수들.현재Y위치 = 200 }
	
	변수들.마우스위젯.ModelToScreen(uint32(변수들.이전X위치), uint32(변수들.이전Y위치))
	변수들.마우스위젯.M색설정(0x00, 0x00, 0x00)
	변수들.마우스위젯.M그리기(&변수들.마우스_영상도형배열)
	
	변수들.마우스위젯.ModelToScreen(uint32(변수들.현재X위치), uint32(변수들.현재Y위치))
	변수들.마우스위젯.M색설정(0x00, 0x00, 0xA8)
	변수들.마우스위젯.M그리기(&변수들.마우스_영상도형배열)

        변수들.이전X위치 = 변수들.현재X위치
        변수들.이전Y위치 = 변수들.현재Y위치

}
/////////////////////////////////////////////////////////////////////////////////////////////////////////
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
func (자신 *TCompositeWidget) M그리기(영상도형배열 *T영상도형배열) {
	자신.T위젯.M그리기(영상도형배열)
	for i:=자신.numChildren-1; i>=0; i-- {
		자신.children[i].M그리기(영상도형배열)
	}
}
func (자신 *TCompositeWidget) M마우스누른동시(x uint32, y uint32, 버튼 uint8){
	for i:=0; i<자신.numChildren; i++ {
		if 자신.children[i].ContainsCoordinate(x - 자신.T위젯.x, y - 자신.T위젯.y) {
			자신.children[i].M마우스누른동시(x-자신.x, y-자신.y, 버튼)
			break
		}
	}
}

func (자신 *TCompositeWidget) OnMouseUp(x uint32, y uint32, 버튼 uint8) { 
	for i:=0; i<자신.numChildren; i++ {
		if 자신.children[i].ContainsCoordinate(x - 자신.T위젯.x, y - 자신.T위젯.y) {
			자신.children[i].OnMouseUp(x-자신.x, y-자신.y, 버튼)
			break
		}
	}
}

func (자신 *TCompositeWidget) OnMouseMove(oldx uint32, oldy uint32, newx uint32, newy uint32) {
	var firstchild int = -1
        for i:=0; i<자신.numChildren; i++ {
                if 자신.children[i].ContainsCoordinate(oldx-자신.T위젯.x, oldy-자신.T위젯.y) {
                        자신.children[i].OnMouseMove(oldx-자신.x, oldy-자신.y, newx-자신.x, newy-자신.y)
			firstchild = i
                        break
                }
        }

        for i:=0; i<자신.numChildren; i++ {
                if 자신.children[i].ContainsCoordinate(newx-자신.T위젯.x, newy-자신.T위젯.y) {
			if firstchild != i {
                        	자신.children[i].OnMouseMove(oldx-자신.x, oldy-자신.y, newx-자신.x, newy-자신.y)
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
