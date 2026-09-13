/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package gdt

import . "unsafe"

func 공용서술자표_올리기(x uintptr)

const (
	SEG_KERNEL_CODE uint32 = 0x08
	SEG_KERNEL_DATA uint32 = 0x10
	SEG_USER_CODE uint32 = 0x1B
	SEG_USER_DATA uint32 = 0x23
	SEG_TASK_STATE uint32 = 0x2B
)

///////////////////////////////////////////////////////////////////////////////////////////
//
//		세그먼트설명자 = Segment Descriptor
//
///////////////////////////////////////////////////////////////////////////////////////////
type T세그먼트설명자 struct{
	리미트_낮은 		uint16	// limit low
	베이스_낮은 		uint16	// base low
	베이스_높은 		uint8	// base high
	타입 			uint8	// type
	플래그들_리미트_높은 	uint8	// flags limit high
	베이스_매우높은		uint8	// base very high
}

func (자신 *T세그먼트설명자) M초기화(베이스 uint32, 리미트 uint32, 타입 uint8, 플래그들 uint8) {
	자신.베이스_낮은 = uint16(베이스 & 0xFFFF)
	자신.베이스_높은 = uint8((베이스 >> 16) & 0xFF)
	자신.베이스_매우높은 = uint8((베이스 >> 24) & 0xFF)

	자신.리미트_낮은 = uint16(리미트 & 0xFFFF)
	자신.플래그들_리미트_높은 = uint8((리미트 >> 24) & 0x0F)
	자신.플래그들_리미트_높은 |= (플래그들 & 0xF0)

	자신.타입 = 타입
}
///////////////////////////////////////////////////////////////////////////////////////////
//
//		공용서술자표 = global descriptor table
//
///////////////////////////////////////////////////////////////////////////////////////////
type T공용서술자표_자료 struct{
	세그먼트설명자[255] T세그먼트설명자	
}
var 자료 T공용서술자표_자료

type T공용서술자표 struct{
}
func (자신 *T공용서술자표) M초기화(){


	자료.세그먼트설명자[0].M초기화(0, 0, 0, 0xCF)
	자료.세그먼트설명자[1].M초기화(0, 64*1024*1024, 0x9A, 0xCF)
	자료.세그먼트설명자[2].M초기화(0, 64*1024*1024, 0x92, 0xCF)
	자료.세그먼트설명자[3].M초기화(0, 64*1024*1024, 0xFA, 0xCF)
	자료.세그먼트설명자[4].M초기화(0, 64*1024*1024, 0xF2, 0xCF)


	타겟 := [6]uint8{0,0,0,0,0,0}
	기준주소 := (*uint32)(Pointer(&타겟[2]))
	(*기준주소) = uint32(uintptr(Pointer(&자료)))
	
	크기 := (*uint16)(Pointer(&타겟[0]))
	(*크기) = (uint16)((Sizeof(자료)))

	공용서술자표_올리기(uintptr(Pointer(&타겟)))

}
func (자신 *T공용서술자표) M설명자_설정(idx int, 베이스 uint32, 리미트 uint32, 타입 uint8, 플래그들 uint8){
	자료.세그먼트설명자[idx].M초기화(베이스, 리미트, 타입, 플래그들)
}
