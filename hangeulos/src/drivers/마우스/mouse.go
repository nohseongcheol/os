/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package 마우스

import . "unsafe"

import . "port"
import . "interrupt"
import . "콘솔"

type I마우스이벤트처리기 interface {
        M마우스누른동시(버튼 int8)
        M마우스떼는동시(버튼 int8)
        M마우스움직인동시(x int8, y int8)
}
var i마우스이벤트처리기  I마우스이벤트처리기

type T기본마우스이벤트처리기 struct{
}

var 콘솔 T콘솔 = T콘솔{}
var x이전위치 int16 = 0
var y이전위치 int16 = 0
var x위치 int16 = 0
var y위치 int16 = 0

func (self T기본마우스이벤트처리기) M마우스누른동시(버튼 int8) {
        buf := []byte("+")
        콘솔.M출력XY(buf, uint16(x이전위치), uint16(y이전위치))
}
func (self T기본마우스이벤트처리기) M마우스떼는동시(버튼 int8) { }
func (self T기본마우스이벤트처리기) M마우스움직인동시(x int8, y int8) {

        x위치 += int16(x)
        if x위치 < 0 { x위치=0 }
        if x위치 >= 80 { x위치 = 79 }

        y위치 -= int16(y)

        if y위치 < 0 { y위치 = 0 }
        if y위치 >= 25 { y위치 = 24 }


        buf := []byte(" ")
        콘솔.M출력XY(buf, uint16(x이전위치), uint16(y이전위치))

        buf = []byte("0")
        콘솔.M출력XY(buf, uint16(x위치), uint16(y위치))

        x이전위치 = x위치
        y이전위치 = y위치
}


type T마우스드라이버 struct{
	*T인터럽트_처리기
}

var 함수포인터 func(*T마우스드라이버, uint32) uint32

var 데이터포트 T바이트포트
var 명령어포트 T바이트포트

func (자신 *T마우스드라이버) M초기화(인터럽트_관리자 *T인터럽트_관리자, 마우스이벤트처리기 I마우스이벤트처리기) {

	데이터포트.M초기화(0x60)
	명령어포트.M초기화(0x64)

	i마우스이벤트처리기 = T기본마우스이벤트처리기{}
	if 마우스이벤트처리기 != nil {
		i마우스이벤트처리기 = 마우스이벤트처리기
	}
	함수포인터 = (*T마우스드라이버).인터럽트처리
	var 주소 uintptr
	주소 = uintptr(Pointer(&함수포인터))
	자신.T인터럽트_처리기.M초기화(0x2C, uintptr(Pointer(인터럽트_관리자)), 주소)


	명령어포트.M쓰기(0xA8)
	명령어포트.M쓰기(0x20)

	
	명령어포트.M쓰기(0x60)

	var 상태 uint8
	상태 = (uint8(데이터포트.M읽기()) | 2 )
	데이터포트.M쓰기(상태) 
	
	명령어포트.M쓰기(0xD4) 
	데이터포트.M쓰기(0xF4) 

	데이터포트.M읽기()
	


}
var 임시버튼값 [3] int8
var 요소위치 uint8 = 0
var 마우스버튼들 int8
func (자신 *T마우스드라이버) 인터럽트처리(확장스택포인터 uint32) uint32{

	임시버튼값[요소위치] = (int8)(데이터포트.M읽기())
	요소위치 = (요소위치 + 1) % 3
	if 요소위치 == 0{
	
		x := 임시버튼값[1]
		y := 임시버튼값[2]

		i마우스이벤트처리기.M마우스움직인동시(x, y)

		var i uint8=0
		for i=0 ; i<3 ; i++ {
			if (임시버튼값[0] & (0x1<<i)) != (마우스버튼들 & (0x1<<i)) {
				if (마우스버튼들 & (0x1<<i)) == 0{
					i마우스이벤트처리기.M마우스누른동시(임시버튼값[0])
				}
			}
		}
		마우스버튼들 = 임시버튼값[0]
		
	}
	
	return 확장스택포인터

}

