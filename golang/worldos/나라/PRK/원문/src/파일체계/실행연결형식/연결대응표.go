/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 실행연결형식

import . "unsafe"
import . "단말"

import 기억관리 "기억공간관리자"

type T연결 struct {
	D동적	uintptr
	P이전	*T연결
	N다음	*T연결
}
type T연결대응표 struct {
	V첫항목	*T연결
	L종가	*T연결

	S크기_2	int

	기억관리	*기억관리.T기억공간관리자
}

func (자신 *T연결대응표) F관문초기화(기억관리 *기억관리.T기억공간관리자) {
	자신.기억관리 = 기억관리
}
func (자신 *T연결대응표) M연결대응표복제() T연결대응표 {
	var 연결대응표 T연결대응표

	연결대응표.F관문초기화(자신.기억관리)

	T연결 := 자신.V첫항목

	for ; T연결 != nil; T연결 = T연결.N다음 {
		연결대응표.M맨뒤에추가(T연결.D동적)
	}
	return 연결대응표
}
func (자신 *T연결대응표) M맨앞에추가(D동적 uintptr) {
	새로만들기연결 := (*T연결)(자신.기억관리.M기억공간할당(uint32(Sizeof(T연결{}))))
	새로만들기연결.D동적 = D동적
	새로만들기연결.N다음 = 자신.V첫항목
	자신.V첫항목 = 새로만들기연결
	자신.S크기_2++

	if 자신.V첫항목.N다음 == nil {
		자신.L종가 = 자신.V첫항목
	}
}
func (자신 *T연결대응표) M맨뒤에추가(D동적 uintptr) {
	if D동적 == 0 {
		return
	}

	if 자신.S크기_2 == 0 {
		자신.M맨앞에추가(D동적)
	} else {
		새로만들기연결 := (*T연결)(자신.기억관리.M기억공간할당(uint32(Sizeof(T연결{}))))
		새로만들기연결.D동적 = D동적
		새로만들기연결.N다음 = nil
		자신.L종가.N다음 = 새로만들기연결
		자신.L종가 = 새로만들기연결
		자신.S크기_2++
	}
}
func (자신 *T연결대응표) P출력(x uint16, y uint16) {
	T연결 := 자신.V첫항목
	단말_3 := T단말{}
	단말_3.M지정좌표에출력("linkmap : ", x, y)
	for ; T연결 != nil; T연결 = T연결.N다음 {
		단말_3.M부호없음정수32출력(uint32(T연결.D동적))
		단말_3.M출력("+")

	}
}
