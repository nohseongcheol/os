package 전역서술자표

import . "unsafe"
import "reflect"
import . "단말"

const (
	Seg핵심코드	uint32	= 0x08
	Seg핵심자료	uint32	= 0x10
	Seg핵심gs	uint32	= 0x18

	Seg사용자코드	uint32	= 0x23
	Seg사용자자료	uint32	= 0x2B
	Seg사용자gs	uint32	= 0x33
	Seg작업상태		uint32	= 0x3B
)

func 전역서술자표함수(x uintptr)
func 가져오기전역서술자표() *T전역서술자표서술자

var 가져오기서술자 T전역서술자표서술자

type T구간서술자 struct {
	제한낮음_2		uint16
	기준낮음_2		uint16
	기준높음_2		uint8
	종류_2		uint8
	표시값들제한높음	uint8
	기준매우높음		uint8
}

func (자신_2 *T구간서술자) F관문초기화(기준_2 uint32, 제한_2 uint32, 종류_2 uint8, 표시값들_2 uint8) {

	자신_2.기준낮음_2 = uint16(기준_2 & 0xFFFF)
	자신_2.기준높음_2 = uint8((기준_2 >> 16) & 0xFF)
	자신_2.기준매우높음 = uint8((기준_2 >> 24) & 0xFF)

	자신_2.제한낮음_2 = uint16(제한_2 & 0xFFFF)
	자신_2.표시값들제한높음 = uint8((제한_2 >> 24) & 0x0F)
	자신_2.표시값들제한높음 |= (표시값들_2 & 0xF0)

	자신_2.종류_2 = 종류_2

}

type T전역서술자표자료 struct {
	구간서술자 [255]T구간서술자
}

var 자료_2 T전역서술자표자료

type T전역서술자표 struct {
}

func (자신_2 *T전역서술자표) F관문초기화() {

	var 전역서술자표항목 T구간서술자

	전역서술자표서술자 = *가져오기전역서술자표()
	이전전역서술자표주소 := uintptr(uint32(전역서술자표서술자.G전역서술자표주소낮음) |
		uint32(전역서술자표서술자.G전역서술자표주소높음)<<16)
	이전전역서술자표길이 := int(uintptr(전역서술자표서술자.G전역서술자표크기+1) / Sizeof(전역서술자표항목))
	이전전역서술자표 := *(*[]T구간서술자)(Pointer(&reflect.SliceHeader{
		Len:	이전전역서술자표길이,
		Cap:	이전전역서술자표길이,
		Data:	이전전역서술자표주소,
	}))
	copy(자료_2.구간서술자[:], 이전전역서술자표)

	자료_2.구간서술자[4].F관문초기화(0, 64*1024*1024, 0xFA, 0xCF)
	자료_2.구간서술자[5].F관문초기화(0, 64*1024*1024, 0xF2, 0xCF)
	자료_2.구간서술자[6].F관문초기화(0x61f004, 0xffffff, 0xF2, 0x4F)

	목적지_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	기준주소 := (*uint32)(Pointer(&목적지_3[2]))
	(*기준주소) = uint32(uintptr(Pointer(&자료_2)))

	크기_2 := (*uint16)(Pointer(&목적지_3[0]))
	(*크기_2) = (uint16)((Sizeof(자료_2)))

	전역서술자표함수(uintptr(Pointer(&목적지_3)))

	단말_2 := new(T단말)
	단말_2.M지정좌표에출력("gdt:", 1, 4)
	단말_2.M부호없음정수32출력(uint32(uintptr(Pointer(&자료_2.구간서술자[3]))))

}
func (자신_2 *T전역서술자표) M서술자설정(항목번호 int, 기준_2 uint32, 제한_2 uint32, 종류_2 uint8, 표시값들_2 uint8) {
	자료_2.구간서술자[항목번호].F관문초기화(기준_2, 제한_2, 종류_2, 표시값들_2)
}

const (
	Kcs찾기번호	= 1
	Kds찾기번호	= 2
	Kgs찾기번호	= 3

	Kcs선택자	= Kcs찾기번호 * 8
	Kds선택자	= Kds찾기번호 * 8
	Kgs선택자	= Kgs찾기번호 * 8

	Seggran바이트	= 0 << 7
	Seggran4k기억쪽	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Seg체계	= 0 << 4
	Seg보통	= 1 << 4

	Segnoexec	= 0 << 3
	Seg실행		= 1 << 3

	Priv핵심	= 0 << 5
	Priv사용자	= 3 << 5

	Segbig방식	= 1 << 6

	P현재	= 1 << 7

	Udesc32seg	= 1 << 0
	Udesc내용		= 3 << 1
	Udescrx전용	= 1 << 3
	Udesc제한안pages	= 1 << 4
	Udescsegnot현재	= 1 << 5
	Udescusable	= 1 << 6

	G전역서술자표항목	= 256
	V실행흐름지역시작		= 16
)

var (
	전역서술자표표		= [G전역서술자표항목]T전역서술자표항목_2{}
	전역서술자표서술자	T전역서술자표서술자
	전역서술자표표길이	= 0
)

type T전역서술자표항목_2 struct {
	제한낮음		uint16
	기준낮음		uint16
	기준mid		uint8
	접근		uint8
	제한높음그리고표시값들	uint8
	기준높음		uint8
}

func (e *T전역서술자표항목_2) M존재여부확인() bool {
	return e.접근&P현재 != 0
}

func (e *T전역서술자표항목_2) M서술자채우기(기준 uint32, 제한 uint32, 접근 uint8, 표시값들 uint8) {
	e.제한높음그리고표시값들 = uint8((제한 >> 16) & 0x000F)
	e.제한높음그리고표시값들 |= 표시값들
	e.접근 = 접근
	e.기준mid = uint8(기준 >> 16)
	e.기준높음 = uint8(기준 >> 24)
	e.기준낮음 = uint16(기준 & 0xFFFF)
	e.제한낮음 = uint16(제한 & 0x0000FFFF)
}

func (e *T전역서술자표항목_2) M서술자지우기() {
	e.제한높음그리고표시값들 = 0
	e.접근 = 0
	e.기준mid = 0
	e.기준높음 = 0
	e.기준낮음 = 0
	e.제한낮음 = 0

}

type T전역서술자표서술자 struct {
	G전역서술자표크기	uint16
	G전역서술자표주소낮음	uint16
	G전역서술자표주소높음	uint16
}
type T사용자서술자 struct {
	E항목번호	uint32
	B기준주소	uint32
	L제한	uint32
	F표시값들	uint8
}

func M실행흐름지역구간설정(찾기번호 uint32, 서술자 *T사용자서술자, 표 []T전역서술자표항목_2) bool {
	if 찾기번호 < V실행흐름지역시작 || 찾기번호 > uint32(len(전역서술자표표)) {
		return false
	}

	if 서술자.F표시값들 == Udescrx전용|Udescsegnot현재 {

		표[찾기번호].M서술자지우기()
		return true
	}

	표시값들 := uint8(Seggran바이트)
	if 서술자.F표시값들&Udesc제한안pages != 0 {
		표시값들 = Seggran4k기억쪽
	}
	접근 := uint8(Priv사용자 | Seg보통 | P현재)
	if 서술자.F표시값들&Udescrx전용 != 0 {
		접근 |= Seg실행
	} else {
		접근 |= Segw
	}
	if 접근&Seg보통 != 0 {
		표시값들 |= Segbig방식
	}

	표[찾기번호].M서술자채우기(서술자.B기준주소, 서술자.L제한, 접근, 표시값들)
	실행흐름지역구간적재(표)

	return true
}

func 실행흐름지역구간적재(표 []T전역서술자표항목_2) {
	copy(전역서술자표표[V실행흐름지역시작:], 표[V실행흐름지역시작:])
}
func F실행흐름지역구간적재(표 []T구간서술자) {
	copy(자료_2.구간서술자[V실행흐름지역시작:], 표[V실행흐름지역시작:])
}
