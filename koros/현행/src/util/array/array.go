package 어레이

import . "unsafe"
import . "콘솔"

var 엔오디이어레이 [100]uintptr

type T어레이 struct {
	S사이즈_에스아이지이 int
}

func (셀프 *T어레이) A에이디디(포인터 uintptr) {
	엔오디이어레이[셀프.S사이즈_에스아이지이] = 포인터
	셀프.S사이즈_에스아이지이++
}
func (셀프 *T어레이) G겟에이티(인덱스 int) Pointer {
	return Pointer(엔오디이어레이[인덱스])
}
func (셀프 *T어레이) I인덱스오에프(포인터 uintptr) int {
	아이 := 0
	for ; 아이 < 셀프.S사이즈_에스아이지이; 아이++ {
		if 포인터 == 엔오디이어레이[아이] {
			return 아이
		}
	}
	return -1
}

var 콘솔_이름 = T콘솔{}

func (셀프 *T어레이) P피알아이엔티() {
	콘솔_이름.M출력XY("array:", 1, 1)

	for 아이 := 0; 아이 < 셀프.S사이즈_에스아이지이; 아이++ {
		콘솔_이름.MUint32출력(uint32(엔오디이어레이[아이]))
		콘솔_이름.M출력(":")
	}
}
