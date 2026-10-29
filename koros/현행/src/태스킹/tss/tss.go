package 티에스에스

import . "unsafe"
import . "gdt"
import . "콘솔"

var 콘솔_이름 = T콘솔{}

type T티에스에스엔트리 struct {
	P프리브티에스에스		uint32
	이에스피0			uint32
	에스에스0			uint32
	이에스피1			uint32
	에스에스1			uint32
	이에스피2			uint32
	에스에스2			uint32
	시에이알3			uint32
	이아이피			uint32
	이에프엘에이지에스_이에프엘에이지에스	uint32
	이에이엑스			uint32
	이시엑스			uint32
	이디엑스			uint32
	이비엑스			uint32
	E이에스피			uint32
	이비피			uint32
	이에스아이			uint32
	이디아이			uint32
	이에스			uint32
	시에스			uint32
	에스에스			uint32
	디에스			uint32
	에프에스			uint32
	지에스			uint32
	엘디티			uint32
	티알에이피			uint16
	아이오엠에이피			uint16
}

var 티에스에스인덱스 uint32 = 0
var 에프엘유에스에이치인덱스 uint32 = 0

func 에프엘유에스에이치티에스에스(uint32)
func (셀프 *T티에스에스엔트리) I아이엔에스티에이엘엘(지디티 *T공용서술자테이블, 아이디엑스 int, 커널에스에스 uint32, 커널이에스피 uint32) {

	콘솔_이름.M출력XY(([]byte)("tss:"), 20, 13)
	비에이에스이 := uint32(uintptr(Pointer(셀프)))
	콘솔_이름.MUint32출력(비에이에스이)
	콘솔_이름.M출력(":")

	지디티.S셋디스크립터(아이디엑스, 비에이에스이, uint32(Sizeof(T티에스에스엔트리{})), 0xE9, 0)
	셀프.에스에스0 = 커널에스에스
	셀프.이에스피0 = 커널이에스피
	셀프.아이오엠에이피 = uint16(Sizeof(T티에스에스엔트리{}))

	에프엘유에스에이치티에스에스(S에스이지태스크에스티에이티이)

}
func (셀프 *T티에스에스엔트리) S셋스택(커널에스에스 uint32, 커널이에스피 uint32) {
	셀프.에스에스0 = 커널에스에스
	셀프.이에스피0 = 커널이에스피
}
func (셀프 *T티에스에스엔트리) G겟이에스피0() uint32 {
	return 셀프.이에스피0
}
func (셀프 *T티에스에스엔트리) G겟에스에스0() uint32 {
	return 셀프.에스에스0
}
