package 배열

import . "unsafe"
import . "단말"

var 연결항목배열 [100]uintptr

type T배열 struct {
	S크기_2 int
}

func (자신 *T배열) M자료추가(주소참조 uintptr) {
	연결항목배열[자신.S크기_2] = 주소참조
	자신.S크기_2++
}
func (자신 *T배열) M지정위치자료가져오기(찾기번호 int) Pointer {
	return Pointer(연결항목배열[찾기번호])
}
func (자신 *T배열) M자료위치찾기(주소참조 uintptr) int {
	i := 0
	for ; i < 자신.S크기_2; i++ {
		if 주소참조 == 연결항목배열[i] {
			return i
		}
	}
	return -1
}

var 단말_3 = T단말{}

func (자신 *T배열) P출력() {
	단말_3.M지정좌표에출력("array:", 1, 1)

	for i := 0; i < 자신.S크기_2; i++ {
		단말_3.M부호없음정수32출력(uint32(연결항목배열[i]))
		단말_3.M출력(":")
	}
}
