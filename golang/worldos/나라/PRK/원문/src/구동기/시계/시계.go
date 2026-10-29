/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 시계

import . "unsafe"

import . "개입중단"
import . "단말"

type I시계사건처리기 interface {
	M주기발생시()
}

var i시계사건처리기 I시계사건처리기

type T기본시계사건처리기 struct {
}

func (자신 *T기본시계사건처리기) M주기발생시() {
}

type T시계구동기 struct {
	T개입중단처리기
}

var 개입중단처리기 func(*T시계구동기, uint32) uint32

func (자신 *T시계구동기) F관문초기화(관리자 *T개입중단관리자, 자판사건처리기 I시계사건처리기) {
	i시계사건처리기 = &T기본시계사건처리기{}
	if 자판사건처리기 != nil {
		i시계사건처리기 = 자판사건처리기
	}

	개입중단처리기 = (*T시계구동기).H처리개입중단
	var 주소 uintptr
	주소 = uintptr(Pointer(&개입중단처리기))

	자신.T개입중단처리기.F관문초기화(0x20, uintptr(Pointer(관리자)), 주소)

}

var 주기발생횟수 uint32 = 0

func (자신 *T시계구동기) H처리개입중단(확장쌓임공간주소 uint32) uint32 {
	단말_3 := T단말{}
	단말_3.M지정좌표에정수32출력(주기발생횟수, 3, 1)
	주기발생횟수++

	return 확장쌓임공간주소
}
