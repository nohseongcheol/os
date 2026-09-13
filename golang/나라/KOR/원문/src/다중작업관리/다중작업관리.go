package 다중작업관리

import . "unsafe"
import . "단말"
import . "reflect"
import 기억관리 "기억공간관리자"
import . "전역서술자표"

var M통신시험 uint8

func halt()

type T중앙처리장치상태 struct {
	p1	uint32
	p2	uint32

	Eax	uint32
	Ebx	uint32
	Ecx	uint32
	Edx	uint32

	Esi	uint32
	Edi	uint32
	Ebp	uint32

	Gs	uint32
	Fs	uint32
	Es	uint32
	Ds	uint32

	Eip	uint32

	Cs	uint32
	Eflags	uint32

	E확장쌓임공간주소	uint32
	Ss		uint32
}

type T작업 struct {
	쌓임공간		[4096]uint8
	중앙처리장치상태	*T중앙처리장치상태
}

func (자신 *T작업) F관문초기화(전역서술자표 *T전역서술자표, 기억관리 *기억관리.T기억공간관리자, 진입함수_2 func()) {

	자신.중앙처리장치상태 = (*T중앙처리장치상태)(Pointer(uintptr(기억관리.M기억공간할당(1024*1024)) + 1024*1024 - Sizeof(T중앙처리장치상태{})))

	자신.중앙처리장치상태.Eax = 0
	자신.중앙처리장치상태.Ebx = 0
	자신.중앙처리장치상태.Ecx = 0
	자신.중앙처리장치상태.Edx = 0

	자신.중앙처리장치상태.Esi = 0
	자신.중앙처리장치상태.Edi = 0

	자신.중앙처리장치상태.Gs = 0
	자신.중앙처리장치상태.Fs = 0
	자신.중앙처리장치상태.Es = 0
	자신.중앙처리장치상태.Ds = 0

	자신.중앙처리장치상태.Eip = uint32(ValueOf(진입함수_2).Pointer())
	자신.중앙처리장치상태.Cs = Seg핵심코드
	자신.중앙처리장치상태.Eflags = 0x202

	var 쌓임공간주소 = uint32(uintptr(Pointer(자신.중앙처리장치상태)))

	자신.중앙처리장치상태.E확장쌓임공간주소 = 쌓임공간주소
	자신.중앙처리장치상태.Ebp = 쌓임공간주소
	자신.중앙처리장치상태.Ss = 0

}

type T작업관리자 struct {
}

var 작업_2 [256]T작업
var 번호작업 int
var 현재작업 int

func (자신 *T작업관리자) F관문초기화() {
	번호작업 = 0
	현재작업 = -1
}

func (자신 *T작업관리자) M작업추가(작업 T작업) bool {
	if 번호작업 >= 255 {
		return false
	}
	작업_2[번호작업] = 작업
	번호작업++
	return true
}

func (자신 *T작업관리자) M다음작업선택(중앙처리장치상태 *T중앙처리장치상태) *T중앙처리장치상태 {

	단말_3 := T단말{}
	for i := 0; i < 번호작업; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(작업_2[i].중앙처리장치상태)))

		단말_3.M지정좌표에정수32출력(x, 10, uint16(15+i))
	}
	if 번호작업 <= 0 {
		return 중앙처리장치상태
	}

	if 현재작업 >= 0 {
		작업_2[현재작업].중앙처리장치상태 = 중앙처리장치상태
	}

	현재작업++
	if 현재작업 >= 번호작업 {
		현재작업 %= 번호작업

	}

	return 작업_2[현재작업].중앙처리장치상태
}
