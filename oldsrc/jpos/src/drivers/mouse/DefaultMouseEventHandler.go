/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package mouse

import . "console"

type T基本マウス事件處理器_資料 struct{
	端末機 T端末機

	x以前位置 int
	y以前位置 int
	x位置 int
	y位置 int
}
var 處理器_資料 T基本マウス事件處理器_資料

type T基本マウス事件處理器 struct{
}

func (自身 T基本マウス事件處理器) Mマウス押し同時(ボタン int8) {
        buf := []byte("+")
        處理器_資料.端末機.M出力(buf, 處理器_資料.x以前位置, 處理器_資料.y以前位置)
}
func (自身 T基本マウス事件處理器) Mマウス離し同時(ボタン int8) { }
func (自身 T基本マウス事件處理器) Mマウス動かし同時(x int8, y int8) {

        處理器_資料.x位置 += int(x)
        if 處理器_資料.x位置 < 0 { 處理器_資料.x位置=0 }
        if 處理器_資料.x位置 >= 80 { 處理器_資料.x位置 = 79 }

        處理器_資料.y位置 -= int(y)

        if 處理器_資料.y位置 < 0 { 處理器_資料.y位置 = 0 }
        if 處理器_資料.y位置 >= 25 { 處理器_資料.y位置 = 24 }


        buf := []byte(" ")
        處理器_資料.端末機.M出力(buf, 處理器_資料.x以前位置, 處理器_資料.y以前位置)

        buf = []byte("0")
        處理器_資料.端末機.M出力(buf, 處理器_資料.x位置, 處理器_資料.y位置)

        處理器_資料.x以前位置 = 處理器_資料.x位置
        處理器_資料.y以前位置 = 處理器_資料.y位置
}

