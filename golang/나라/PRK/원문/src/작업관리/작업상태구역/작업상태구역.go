package 작업상태구역

import . "unsafe"
import . "전역서술자표"
import . "단말"

var 단말_3 = T단말{}

type T작업상태구역항목 struct {
	P이전작업상태구역	uint32
	확장쌓임공간주소0	uint32
	ss0		uint32
	확장쌓임공간주소1	uint32
	ss1		uint32
	확장쌓임공간주소2	uint32
	ss2		uint32
	제어저장기3		uint32
	eip		uint32
	eflags		uint32
	eax		uint32
	ecx		uint32
	edx		uint32
	ebx		uint32
	E확장쌓임공간주소	uint32
	ebp		uint32
	esi		uint32
	edi		uint32
	es		uint32
	cs		uint32
	ss		uint32
	ds		uint32
	fs		uint32
	gs		uint32
	ldt		uint32
	trap		uint16
	iomap		uint16
}

var 작업상태구역찾기번호 uint32 = 0
var flush찾기번호 uint32 = 0

func 작업상태선택자적재(uint32)
func (자신 *T작업상태구역항목) M작업상태구역설치(전역서술자표 *T전역서술자표, 항목번호 int, 핵심ss uint32, 핵심확장쌓임공간주소 uint32) {

	단말_3.M지정좌표에출력(([]byte)("tss:"), 20, 13)
	기준 := uint32(uintptr(Pointer(자신)))
	단말_3.M부호없음정수32출력(기준)
	단말_3.M출력(":")

	전역서술자표.M서술자설정(항목번호, 기준, uint32(Sizeof(T작업상태구역항목{})), 0xE9, 0)
	자신.ss0 = 핵심ss
	자신.확장쌓임공간주소0 = 핵심확장쌓임공간주소
	자신.iomap = uint16(Sizeof(T작업상태구역항목{}))

	작업상태선택자적재(Seg작업상태)

}
func (자신 *T작업상태구역항목) M핵심쌓임공간설정(핵심ss uint32, 핵심확장쌓임공간주소 uint32) {
	자신.ss0 = 핵심ss
	자신.확장쌓임공간주소0 = 핵심확장쌓임공간주소
}
func (자신 *T작업상태구역항목) M핵심쌓임공간주소읽기() uint32 {
	return 자신.확장쌓임공간주소0
}
func (자신 *T작업상태구역항목) M핵심쌓임공간선택자읽기() uint32 {
	return 자신.ss0
}
