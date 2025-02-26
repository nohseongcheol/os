/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right rEserved
*/
package 작업관리자

import . "unsafe"
import . "reflect"
import . "gdt"
import mem "memorymanager"

type T시피유상태 struct{

	t1 uint32
	t2 uint32	

	Eax uint32 // accumulator
	Ebx uint32 // base
	Ecx uint32 // counter
	Edx uint32 // data

	Esi uint32
	Edi uint32
	Ebp uint32

	//Gs uint32
	//Fs uint32
	Es uint32
	Ds uint32	

	//error uint32
	
	Eip uint32

	Cs uint32
	Eflags uint32
	
	Esp uint32
	Ss uint32
}

type T작업 struct{
	스택 [4096] uint8
	시피유_상태 *T시피유상태
}
//var 스택 [256][4096] uint8
//var 시피유_상태 *T시피유상태

func (자신 *T작업) M초기화(gdt *T공용서술자표, mem *mem.T메모리_관리자, 진입점 func()){
	
	//자신.시피유_상태 = (*T시피유상태)(Pointer(uintptr(Pointer(&스택[작업번호])) + 4096 - Sizeof(T시피유상태{})))
	자신.시피유_상태 = (*T시피유상태)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(T시피유상태{})))

	자신.시피유_상태.Eax = 0
	자신.시피유_상태.Ebx = 0
	자신.시피유_상태.Ecx = 0
	자신.시피유_상태.Edx = 0


	자신.시피유_상태.Esi = 0
	자신.시피유_상태.Edi = 0

	자신.시피유_상태.Es = 0
	자신.시피유_상태.Ds = 0

	자신.시피유_상태.Eip = uint32(ValueOf(진입점).Pointer())

	자신.시피유_상태.Cs = SEG_KERNEL_CODE
	자신.시피유_상태.Eflags = 0x202

	var 스택주소 = uint32(uintptr(Pointer(자신.시피유_상태)))

	자신.시피유_상태.Esp = 스택주소
	자신.시피유_상태.Ebp = 스택주소

	자신.시피유_상태.Ss = 0

}
type T작업관리자 struct{
}
var 작업들 [256] T작업
var 작업갯수 int
var 현재작업 int
func (자신 * T작업관리자) M초기화() {
	작업갯수 = 0
	현재작업 = -1 
}

func (자신 *T작업관리자) M작업추가(작업 T작업) bool {
	if(작업갯수 >= 255){
		return false
	}
	작업들[작업갯수] = 작업
	작업갯수++
	return true
}
func (자신 *T작업관리자) M작업일정(시피유_상태 *T시피유상태) *T시피유상태{


	if 작업갯수 <= 0 {
		return 시피유_상태
	}
	
	if 현재작업 >= 0 {
		작업들[현재작업].시피유_상태 = 시피유_상태
	}
	
	현재작업++
	if 현재작업 >= 작업갯수 {
		현재작업 %= 작업갯수
	}

	return 작업들[현재작업].시피유_상태
}
