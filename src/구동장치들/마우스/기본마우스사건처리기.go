/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package 마우스

import . "단말기"

type T기본마우스사건처리기_자료 struct{
	단말기 T단말기

	x이전위치 int
	y이전위치 int
	x위치 int
	y위치 int
}
var 처리기_자료 T기본마우스사건처리기_자료

type T기본마우스사건처리기 struct{
}

func (self T기본마우스사건처리기) M마우스누른동시(버튼 int8) {
        buf := []byte("+")
        처리기_자료.단말기.M출력(buf, 처리기_자료.x이전위치, 처리기_자료.y이전위치)
}
func (self T기본마우스사건처리기) M마우스떼는동시(버튼 int8) { }
func (self T기본마우스사건처리기) M마우스움직인동시(x int8, y int8) {

        처리기_자료.x위치 += int(x)
        if 처리기_자료.x위치 < 0 { 처리기_자료.x위치=0 }
        if 처리기_자료.x위치 >= 80 { 처리기_자료.x위치 = 79 }

        처리기_자료.y위치 -= int(y)

        if 처리기_자료.y위치 < 0 { 처리기_자료.y위치 = 0 }
        if 처리기_자료.y위치 >= 25 { 처리기_자료.y위치 = 24 }


        buf := []byte(" ")
        처리기_자료.단말기.M출력(buf, 처리기_자료.x이전위치, 처리기_자료.y이전위치)

        buf = []byte("0")
        처리기_자료.단말기.M출력(buf, 처리기_자료.x위치, 처리기_자료.y위치)

        처리기_자료.x이전위치 = 처리기_자료.x위치
        처리기_자료.y이전위치 = 처리기_자료.y위치
}

