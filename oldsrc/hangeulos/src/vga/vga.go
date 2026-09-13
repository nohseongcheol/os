/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package vga

import . "unsafe"
import . "port"

type T비디오그래픽배열 struct{
}
type T비디오그래픽배열_변수들 struct{
	기타작업_포트 T바이트포트 				// Miscellaneous output register , read( 0x03cc), write(0x03c2)
	브라운관제어기_색인포트 T바이트포트			// Cathode Ray Tube Controller(CRTC) =  브라운관(브라운관)
	브라운관제어기_자료포트 T바이트포트
	순서기_색인포트 T바이트포트				// sequencerIndexPort
	순서기_자료포트 T바이트포트				// sequencerDataPort
	그래픽제어기_색인포트 T바이트포트			// graphicsControllerIndexPort
	그래픽제어기_자료포트 T바이트포트			// graphicsControllerDataPort
	속성제어기_색인포트 T바이트포트			// attributeControllerIndexPort
	속성제어기_읽기포트 T바이트포트			// attributeControllerReadPort
	속성제어기_쓰기포트 T바이트포트			// attributeControllerWritePort
	속성제어기_리셋포트 T바이트포트			// attributeControllerResetPort
}

func (자신 *T비디오그래픽배열_변수들)M초기화(){
	변수들.기타작업_포트.M초기화(0x3c2) 			// Miscellaneous output register , read( 0x03cc), write(0x03c2)
	변수들.브라운관제어기_색인포트.M초기화(0x3d4)		// Cathode Ray Tube Controller(CRTC) =  브라운관(브라운관)
	변수들.브라운관제어기_자료포트.M초기화(0x3d5)
	변수들.순서기_색인포트.M초기화(0x3c4)			// sequencerIndexPort
	변수들.순서기_자료포트.M초기화(0x3c5)			// sequencerDataPort
	변수들.그래픽제어기_색인포트.M초기화(0x3ce)		// graphicsControllerIndexPort
	변수들.그래픽제어기_자료포트.M초기화(0x3cf)		// graphicsControllerDataPort
	변수들.속성제어기_색인포트.M초기화(0x3c0)			// attributeControllerIndexPort
	변수들.속성제어기_읽기포트.M초기화(0x3c1)			// attributeControllerReadPort
	변수들.속성제어기_쓰기포트.M초기화(0x3c0)			// attributeControllerWritePort
	변수들.속성제어기_리셋포트.M초기화(0x3da)			// attributeControllerResetPort
}
var 변수들 T비디오그래픽배열_변수들


func (자신 *T비디오그래픽배열) M레지스터들_쓰기(레지스터들 []byte){
	var 인덱스 uint16 = 0


	변수들.M초기화()
	변수들.기타작업_포트.M쓰기(레지스터들[인덱스])
	인덱스++

	var i uint8
	for i=0; i<5; i++ {
		변수들.순서기_색인포트.M쓰기(i)
		변수들.순서기_자료포트.M쓰기(레지스터들[인덱스])
		인덱스++
	}
	
	변수들.브라운관제어기_색인포트.M쓰기(0x03)
	변수들.브라운관제어기_자료포트.M쓰기((변수들.브라운관제어기_자료포트.M읽기() | 0x80))
	변수들.브라운관제어기_색인포트.M쓰기(0x11)
	변수들.브라운관제어기_자료포트.M쓰기((변수들.브라운관제어기_자료포트.M읽기() & ^uint8(0x80)))

	레지스터들[0x03] = 레지스터들[0x03] | 0x80
	레지스터들[0x11] = 레지스터들[0x11] & ^uint8(0x80)

	for i=0; i<25; i++ {
		변수들.브라운관제어기_색인포트.M쓰기(i)
		변수들.브라운관제어기_자료포트.M쓰기(레지스터들[인덱스])
		인덱스++
	}

	for i=0; i<9; i++ {
		변수들.그래픽제어기_색인포트.M쓰기(i)
		변수들.그래픽제어기_자료포트.M쓰기(레지스터들[인덱스])
		인덱스++
	}
	
	for i=0; i<21; i++ {
		변수들.속성제어기_리셋포트.M읽기()
		변수들.속성제어기_색인포트.M쓰기(i)
		변수들.속성제어기_쓰기포트.M쓰기(레지스터들[인덱스])
		인덱스++
	}

	변수들.속성제어기_리셋포트.M읽기()
	변수들.속성제어기_색인포트.M쓰기(0x20)
	
}

func (자신 *T비디오그래픽배열) GetFrameBufferSegment() uintptr{
	변수들.그래픽제어기_색인포트.M쓰기(0x06)
	var segmentNumber uint8 = ((변수들.그래픽제어기_자료포트.M읽기() >> 2) & 0x03)
	switch segmentNumber {
		case 0: return uintptr(0x00000)
		case 1: return uintptr(0xa0000)
		case 2: return uintptr(0xb0000)
		case 3: return uintptr(0xb8000)
	}
	
	return uintptr(0xB0000)
}
func (자신 *T비디오그래픽배열) M화소_넣기(x uint32, y uint32, colorIndex uint8){
	if x<0 || 320 <= x || y<0 || 200 <= y {
		return
	}
	
	var 픽셀주소 uintptr = 자신.GetFrameBufferSegment() + uintptr(320*y+x)
	*(*uint8)(Pointer(픽셀주소)) = colorIndex

}
func (자신 *T비디오그래픽배열) GetColorIndex(적 uint8, 녹 uint8, 청 uint8) uint8{
	if 적==0x00 && 녹==0x00 && 청==0x00 { return 0x00 } // black
	if 적==0x00 && 녹==0x00 && 청==0xA8 { return 0x01 } // blue
	if 적==0x00 && 녹==0xA8 && 청==0x00 { return 0x02 } // green
	if 적==0xA8 && 녹==0x00 && 청==0x00 { return 0x04 } // red
	if 적==0xFF && 녹==0xFF && 청==0xFF { return 0x3F } // white

	return 0x01
}
func (자신 *T비디오그래픽배열) M화소_적녹청_넣기(x uint32, y uint32, 적 uint8, 녹 uint8, 청 uint8){
	자신.M화소_넣기(x, y, 자신.GetColorIndex(적, 녹, 청))
}
func (자신 *T비디오그래픽배열) M사각형채우기(x uint32, y uint32, 넓이 uint32, 높이 uint32, 적 uint8, 녹 uint8, 청 uint8) {
	for Y:=y; Y<y+높이; Y++ {
		for X:=x; X<x+넓이; X++ {
			자신.M화소_적녹청_넣기(X, Y, 적, 녹, 청)
		}
	}
}
func (자신 *T비디오그래픽배열) M모드_지원여부(넓이 uint32, 높이 uint32, 색심도 uint32) bool {
	return 넓이==320 && 높이==200 && 색심도==8
}
func (자신 *T비디오그래픽배열) M모드_설정(넓이 uint32, 높이 uint32, 색심도 uint32) bool{
	if !자신.M모드_지원여부(넓이, 높이, 색심도) {
		return false
	}

	var g_320x200x256 = []byte {
	/* MISC */
	0x63,
	/* SEQ */
	0x03, 0x01, 0x0F, 0x00, 0x0E,
	/* CRTC */
	0x5F, 0x4F, 0x50, 0x82, 0x54, 0x80, 0xBF, 0x1F,
	0x00, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x9C, 0x0E, 0x8F, 0x28,	0x40, 0x96, 0xB9, 0xA3,
	0xFF,
	/* GC */
	0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x05, 0x0F,
	0xFF,
	/* AC */
	0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
	0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
	0x41, 0x00, 0x0F, 0x00,	0x00 }


	자신.M레지스터들_쓰기(g_320x200x256)

	return true	
}

