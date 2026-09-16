/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 자판

import . "unsafe"

import . "입출력접속"
import . "개입중단"

import . "단말"
import . "체계호출"

type I자판사건처리기 interface {
	M키누름시(키 byte)
	M키놓음시(키 byte)
}

var i자판사건처리기 I자판사건처리기
var 기본자판사건처리기 T기본자판사건처리기

type T기본자판사건처리기 struct {
}

func (자신 *T기본자판사건처리기) M키누름시(키 byte) {
	값16진수 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	임시공간 := []byte("\n\n\n\n\n\nkeyboard :    ")

	임시공간[17] = 값16진수[((키 >> 4) & 0xF)]
	임시공간[18] = 값16진수[키&0xF]

	단말_3 := T단말{}
	단말_3.M출력(임시공간)

}
func (자신 *T기본자판사건처리기) M키놓음시(키 byte) {
}

type T자판구동기 struct {
	T개입중단처리기
}

var 활성자판구동기 *T자판구동기
var 개입중단처리기 func(uint32) uint32

var 자료접속_2 uint16 = 0x60
var 명령접속_2 uint16 = 0x64

const 자판접속대기한도 = 100000

func 자판접속입력여유대기() bool {
	for i := 0; i < 자판접속대기한도; i++ {
		if (F입출력접속바이트읽기(명령접속_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func 자판접속출력자료대기() bool {
	for i := 0; i < 자판접속대기한도; i++ {
		if (F입출력접속바이트읽기(명령접속_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func 자판접속명령쓰기(값 uint8) bool {
	if !자판접속입력여유대기() {
		return false
	}
	F입출력접속바이트쓰기(명령접속_2, 값)
	return true
}

func 자판접속자료쓰기(값 uint8) bool {
	if !자판접속입력여유대기() {
		return false
	}
	F입출력접속바이트쓰기(자료접속_2, 값)
	return true
}

func 자판접속자료읽기() (uint8, bool) {
	if !자판접속출력자료대기() {
		return 0, false
	}
	return F입출력접속바이트읽기(자료접속_2), true
}

func (자신 *T자판구동기) M구동기초기화(관리자 *T개입중단관리자, 자판사건처리기 I자판사건처리기) {

	i자판사건처리기 = &기본자판사건처리기
	if 자판사건처리기 != nil {
		i자판사건처리기 = 자판사건처리기
	}

	활성자판구동기 = 자신
	개입중단처리기 = 자판개입중단처리
	var 주소 uintptr
	주소 = uintptr(Pointer(&개입중단처리기))

	자신.F관문초기화(0x21, uintptr(Pointer(관리자)), 주소)

	for i := 0; i < 32 && (F입출력접속바이트읽기(명령접속_2)&0x01) != 0; i++ {
		F입출력접속바이트읽기(자료접속_2)
	}

	if !자판접속명령쓰기(0xAE) || !자판접속명령쓰기(0x20) {
		return
	}
	상태, 확인 := 자판접속자료읽기()
	if !확인 {
		return
	}
	상태 |= 0x01
	상태 &^= 0x10
	if !자판접속명령쓰기(0x60) || !자판접속자료쓰기(상태) {
		return
	}

	if !자판접속자료쓰기(0xF4) {
		return
	}
	응답부호, 확인 := 자판접속자료읽기()
	if !확인 || 응답부호 != 0xFA {
		return
	}

}

func 자판개입중단처리(확장쌓임공간주소 uint32) uint32 {
	if 활성자판구동기 == nil {
		F입출력접속바이트읽기(자료접속_2)
		return 확장쌓임공간주소
	}
	return 활성자판구동기.H처리개입중단(확장쌓임공간주소)
}

const 자판대기열크기 = 64

var 자판대기열 [자판대기열크기]byte
var 자판대기열읽기 uint8
var 자판대기열쓰기 uint8
var 왼쪽글자전환 bool
var 오른쪽글자전환 bool
var 확장검사코드 bool

func 자판바이트대기열추가(키 byte) {
	다음 := (자판대기열쓰기 + 1) % 자판대기열크기
	if 다음 == 자판대기열읽기 {
		return
	}
	자판대기열[자판대기열쓰기] = 키
	자판대기열쓰기 = 다음
}

func F대기중자판사건처리() {
	for 자판대기열읽기 != 자판대기열쓰기 {
		키 := 자판대기열[자판대기열읽기]
		자판대기열읽기 = (자판대기열읽기 + 1) % 자판대기열크기
		F표준입력에바이트추가(키)
		if i자판사건처리기 != nil {
			i자판사건처리기.M키누름시(키)
		}
	}
}

func 자판주사부호를문자로변환(검사코드 uint8) (byte, bool) {
	글자전환여부 := 왼쪽글자전환 || 오른쪽글자전환

	if 검사코드 >= 0x02 && 검사코드 <= 0x0B {
		if 글자전환여부 {
			return "!@#$%^&*()"[검사코드-0x02], true
		}
		return "1234567890"[검사코드-0x02], true
	}
	if 검사코드 >= 0x10 && 검사코드 <= 0x19 {
		키 := "qwertyuiop"[검사코드-0x10]
		if 글자전환여부 {
			키 -= 'a' - 'A'
		}
		return 키, true
	}
	if 검사코드 >= 0x1E && 검사코드 <= 0x26 {
		키 := "asdfghjkl"[검사코드-0x1E]
		if 글자전환여부 {
			키 -= 'a' - 'A'
		}
		return 키, true
	}
	if 검사코드 >= 0x2C && 검사코드 <= 0x32 {
		키 := "zxcvbnm"[검사코드-0x2C]
		if 글자전환여부 {
			키 -= 'a' - 'A'
		}
		return 키, true
	}

	switch 검사코드 {
	case 0x0C:
		if 글자전환여부 {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if 글자전환여부 {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if 글자전환여부 {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if 글자전환여부 {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if 글자전환여부 {
			return ':', true
		}
		return ';', true
	case 0x28:
		if 글자전환여부 {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if 글자전환여부 {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if 글자전환여부 {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if 글자전환여부 {
			return '<', true
		}
		return ',', true
	case 0x34:
		if 글자전환여부 {
			return '>', true
		}
		return '.', true
	case 0x35:
		if 글자전환여부 {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (자신 *T자판구동기) H처리개입중단(확장쌓임공간주소 uint32) uint32 {
	상태 := F입출력접속바이트읽기(명령접속_2)
	if (상태&0x01) == 0 || (상태&0x20) != 0 {
		return 확장쌓임공간주소
	}

	검사코드 := F입출력접속바이트읽기(자료접속_2)
	if 검사코드 == 0xE0 {
		확장검사코드 = true
		return 확장쌓임공간주소
	}
	if 확장검사코드 {
		확장검사코드 = false
		return 확장쌓임공간주소
	}

	해제여부 := (검사코드 & 0x80) != 0
	기준코드 := 검사코드 & 0x7F
	if 기준코드 == 0x2A {
		왼쪽글자전환 = !해제여부
		return 확장쌓임공간주소
	}
	if 기준코드 == 0x36 {
		오른쪽글자전환 = !해제여부
		return 확장쌓임공간주소
	}
	if 해제여부 {
		return 확장쌓임공간주소
	}

	if 키, 확인 := 자판주사부호를문자로변환(기준코드); 확인 {
		자판바이트대기열추가(키)
	}

	return 확장쌓임공간주소
}
