package 영상도형배열

import . "unsafe"
import . "입출력접속"

type T영상도형제어기 struct {
}

var mics접속 uint16 = 0x3c2
var crtc찾기번호접속 uint16 = 0x3d4
var crtc자료접속 uint16 = 0x3d5
var sequencer찾기번호접속 uint16 = 0x3c4
var sequencer자료접속 uint16 = 0x3c5
var 그래픽제어기찾기번호접속 uint16 = 0x3ce
var 그래픽제어기자료접속 uint16 = 0x3cf
var 속성제어기찾기번호접속 uint16 = 0x3c0
var 속성제어기읽기접속 uint16 = 0x3c1
var 속성제어기쓰기접속 uint16 = 0x3c0
var 속성제어기재설정접속 uint16 = 0x3da

func (자신 *T영상도형제어기) M화면저장기쓰기(저장기 []byte) {
	var 저장기번호 uint16 = 0

	F입출력접속바이트쓰기(mics접속, 저장기[저장기번호])
	저장기번호++

	var i uint8
	for i = 0; i < 5; i++ {
		F입출력접속바이트쓰기(sequencer찾기번호접속, i)
		F입출력접속바이트쓰기(sequencer자료접속, 저장기[저장기번호])
		저장기번호++
	}

	F입출력접속바이트쓰기(crtc찾기번호접속, 0x03)

	F입출력접속바이트쓰기(crtc자료접속, (F입출력접속바이트읽기(crtc자료접속) | 0x80))
	F입출력접속바이트쓰기(crtc찾기번호접속, 0x11)
	F입출력접속바이트쓰기(crtc자료접속, (F입출력접속바이트읽기(crtc자료접속) & ^uint8(0x80)))

	저장기[0x03] = 저장기[0x03] | 0x80
	저장기[0x11] = 저장기[0x11] & ^uint8(0x80)

	for i = 0; i < 25; i++ {
		F입출력접속바이트쓰기(crtc찾기번호접속, i)
		F입출력접속바이트쓰기(crtc자료접속, 저장기[저장기번호])
		저장기번호++
	}

	for i = 0; i < 9; i++ {
		F입출력접속바이트쓰기(그래픽제어기찾기번호접속, i)
		F입출력접속바이트쓰기(그래픽제어기자료접속, 저장기[저장기번호])
		저장기번호++
	}

	for i = 0; i < 21; i++ {
		F입출력접속바이트읽기(속성제어기재설정접속)
		F입출력접속바이트쓰기(속성제어기찾기번호접속, i)
		F입출력접속바이트쓰기(속성제어기쓰기접속, 저장기[저장기번호])
		저장기번호++
	}

	F입출력접속바이트읽기(속성제어기재설정접속)
	F입출력접속바이트쓰기(속성제어기찾기번호접속, 0x20)

}

func (자신 *T영상도형제어기) M화면기억공간주소가져오기() uintptr {
	F입출력접속바이트쓰기(그래픽제어기찾기번호접속, 0x06)
	var 구간번호 uint8 = ((F입출력접속바이트읽기(그래픽제어기자료접속) >> 2) & 0x03)
	switch 구간번호 {
	case 0:
		return uintptr(0x00000)
	case 1:
		return uintptr(0xa0000)
	case 2:
		return uintptr(0xb0000)
	case 3:
		return uintptr(0xb8000)
	}

	return uintptr(0xB0000)
}
func (자신 *T영상도형제어기) M화소색상번호설정(x uint32, y uint32, 색상찾기번호 uint8) {
	if x < 0 || 320 <= x || y < 0 || 200 <= y {
		return
	}

	var 화소주소 uintptr = 자신.M화면기억공간주소가져오기() + uintptr(320*y+x)
	*(*uint8)(Pointer(화소주소)) = 색상찾기번호

}
func (자신 *T영상도형제어기) M색상번호가져오기(빨강 uint8, 초록 uint8, b uint8) uint8 {
	if 빨강 == 0x00 && 초록 == 0x00 && b == 0x00 {
		return 0x00
	}
	if 빨강 == 0x00 && 초록 == 0x00 && b == 0xA8 {
		return 0x01
	}
	if 빨강 == 0x00 && 초록 == 0xA8 && b == 0x00 {
		return 0x02
	}
	if 빨강 == 0xA8 && 초록 == 0x00 && b == 0x00 {
		return 0x04
	}
	if 빨강 == 0xFF && 초록 == 0xFF && b == 0xFF {
		return 0x3F
	}

	return 0x01
}
func (자신 *T영상도형제어기) M삼원색화소설정(x uint32, y uint32, 빨강 uint8, 초록 uint8, b uint8) {
	자신.M화소색상번호설정(x, y, 자신.M색상번호가져오기(빨강, 초록, b))
}
func (자신 *T영상도형제어기) M사각형채우기(x uint32, y uint32, 너비_2 uint32, h uint32, 빨강 uint8, 초록 uint8, b uint8) {
	for Y := y; Y < y+h; Y++ {
		for X := x; X < x+너비_2; X++ {
			자신.M삼원색화소설정(X, Y, 빨강, 초록, b)
		}
	}
}
func (자신 *T영상도형제어기) M화면방식지원확인(너비 uint32, 높이 uint32, 색상심도 uint32) bool {
	return 너비 == 320 && 높이 == 200 && 색상심도 == 8
}
func (자신 *T영상도형제어기) M화면방식설정(너비 uint32, 높이 uint32, 색상심도 uint32) bool {
	if !자신.M화면방식지원확인(너비, 높이, 색상심도) {
		return false
	}

	var 화면320곱하기200색상256설정 = []byte{

		0x63,

		0x03, 0x01, 0x0F, 0x00, 0x0E,

		0x5F, 0x4F, 0x50, 0x82, 0x54, 0x80, 0xBF, 0x1F,
		0x00, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x9C, 0x0E, 0x8F, 0x28, 0x40, 0x96, 0xB9, 0xA3,
		0xFF,

		0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x05, 0x0F,
		0xFF,

		0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
		0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
		0x41, 0x00, 0x0F, 0x00, 0x00}

	자신.M화면저장기쓰기(화면320곱하기200색상256설정)

	return true
}
