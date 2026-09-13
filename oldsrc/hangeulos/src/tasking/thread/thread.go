/*
        Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "콘솔"
import . "작업관리자"
import 메모리 "memorymanager"

const (
	Blocked = 1
	Ready = 2
	Stopped = 3
	Started = 4
)
/*
const (
	Unknown = 1+itoa
	SleepMS
	ReceivePC
)
*/
const USER_STACK_SIZE=32*1024
const USER_STACK=((20*1024*1024) - USER_STACK_SIZE)

const THREAD_STACK_SIZE = 100*1024
//const THREAD_STACK_SIZE = 16*0x1000

type T쓰레드 struct{
	P시피유상태 *T시피유상태
	P스택 uint32
	P사용자스택 uint32
	P사용자스택크기 uint32


	P쓰레드_상태 uint8
	P블록된상태 uint8

	timeDelta uint32
	//FPUBuffer uint32
	
}
func (자신 *T쓰레드) New(){
}

type T쓰레드_헬퍼 struct{
	메모리 *메모리.T메모리_관리자
}
var 콘솔 = T콘솔{}
func (자신 *T쓰레드_헬퍼) M초기화(메모리 *메모리.T메모리_관리자){
	자신.메모리 = 메모리
	콘솔.M출력XY("thread:", 1, 16)
}
func (자신 *T쓰레드_헬퍼) M함수로부터_생성(entrypoint func(), isKernel bool) T쓰레드{
	결과 := T쓰레드{}


	결과.P스택 = uint32(uintptr(자신.메모리.Malloc(THREAD_STACK_SIZE*2)))

	결과.P시피유상태 = (*T시피유상태)(Pointer(uintptr(결과.P스택) + THREAD_STACK_SIZE - Sizeof(T시피유상태{})))
	결과.P시피유상태.Esp = 결과.P스택 + THREAD_STACK_SIZE
	결과.P시피유상태.Ebp = 결과.P시피유상태.Esp
	결과.P시피유상태.Eip = uint32(ValueOf(entrypoint).Pointer())
	결과.P사용자스택 = USER_STACK
	결과.P사용자스택크기 = USER_STACK_SIZE

	콘솔.MUint32출력(uint32(uintptr(Pointer(결과.P시피유상태))))
	콘솔.MUint32출력(결과.P시피유상태.Eip)

	if isKernel == true{
		결과.P시피유상태.Cs = SEG_KERNEL_CODE
		결과.P시피유상태.Ds = SEG_KERNEL_DATA
		결과.P시피유상태.Es = SEG_KERNEL_DATA
		결과. P쓰레드_상태 = Ready
	}else{
		결과.P시피유상태.Cs = SEG_USER_CODE
		결과.P시피유상태.Ds = SEG_USER_DATA
		결과.P시피유상태.Es = SEG_USER_DATA
		결과.P쓰레드_상태 = Started
	}
	결과.P시피유상태.Eflags = 0x202
	//결과.FPUBuffer  = uint32(uintptr(자신.메모리.Malloc(512)))

	return 결과 
}
