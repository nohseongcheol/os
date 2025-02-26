/*
        Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "콘솔"
import . "gdt"
import . "port"
import . "util/list"
import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "작업관리자"
import 메모리 "memorymanager"

const SCHEDULER_FREQUENCY=30
const KERNEL_HEAP_START=1024*1024

var 리스트 T링크드_리스트 = T링크드_리스트{}
type T스케줄러_자료 struct{
	주파수 uint32
	틱갯수 uint32

	강제전환 bool
	활성화됨 bool
	//리스트 T링크드_리스트

	현재쓰레드 *T쓰레드

	tss TSSEntry
}
var 스케줄러_자료 T스케줄러_자료 = T스케줄러_자료{}
func (자신 *T스케줄러_자료) M초기화(){
	스케줄러_자료.틱갯수 = 0
	스케줄러_자료.주파수 = SCHEDULER_FREQUENCY
	스케줄러_자료.현재쓰레드 = nil
	스케줄러_자료.활성화됨 = false 
	스케줄러_자료.강제전환 = false

}
var 콘솔 = T콘솔{}
func (자신 *T스케줄러_자료) M다음준비쓰레드_받기() *T쓰레드{
	var 현재쓰레드_인덱스 int = 0


	if 스케줄러_자료.현재쓰레드 != nil {
		현재쓰레드_인덱스 = 리스트.IndexOf(uintptr(Pointer(스케줄러_자료.현재쓰레드)))
	} else {
		현재쓰레드_인덱스 = 0
	}

	현재쓰레드_인덱스++

	if 현재쓰레드_인덱스 >= 리스트.M크기(){
		현재쓰레드_인덱스 = 0
	}

	for ; (*T쓰레드)(리스트.GetAt(현재쓰레드_인덱스)).P쓰레드_상태 == Blocked;  {
		현재쓰레드_인덱스++
		if 현재쓰레드_인덱스 >= 리스트.M크기() {
			현재쓰레드_인덱스 = 0
			break
		}
	}


	쓰레드 := (*T쓰레드)(리스트.GetAt(현재쓰레드_인덱스))


	return 쓰레드
	
}
func (자신 *T스케줄러) M쓰레드_추가(쓰레드 *T쓰레드){
	리스트.M뒤에밀어넣기(uintptr(Pointer(쓰레드)))
}


type T스케줄러 struct{
	T인터럽트_처리기

}
func (자신 *T스케줄러) M초기화(관리자 *T인터럽트_관리자, 메모리 *메모리.T메모리_관리자, tss TSSEntry){
	//스케줄러_자료 = T스케줄러_자료{}
	스케줄러_자료.M초기화()
	스케줄러_자료.tss = tss

	//스케줄러_자료.리스트 = T링크드_리스트{}
	리스트.M초기화(메모리)

	인터럽트_처리기 = M인터럽트_처리
	var 주소 uintptr
	주소 = uintptr(Pointer(&인터럽트_처리기))
	자신.T인터럽트_처리기.M초기화(0x20, uintptr(Pointer(관리자)), 주소)
}

func (자신 *T스케줄러)M활성화됨(enabled bool){
	스케줄러_자료.활성화됨 = enabled
}


func fxsave(uint32)
func fxrstor(uint32)


var 인터럽트_처리기 func(uint32) uint32
func M인터럽트_처리(esp uint32) uint32{

	스케줄러_자료.틱갯수++
	콘솔.M출력XY("sche1:", 1, 17)
	콘솔.MUint32출력(uint32(리스트.M크기()))
	콘솔.MUint32출력(uint32(스케줄러_자료.틱갯수))
	콘솔.MUint32출력(esp)

	if 스케줄러_자료.틱갯수 == 스케줄러_자료.주파수{
		스케줄러_자료.틱갯수 = 0

		if 리스트.M크기() > 0 && 스케줄러_자료.활성화됨 == true{
			var 다음쓰레드 = 스케줄러_자료.M다음준비쓰레드_받기()

			if esp >= KERNEL_HEAP_START{
				스케줄러_자료.현재쓰레드.P시피유상태 = (*T시피유상태)(Pointer(uintptr(esp)))
				//fxsave(스케줄러_자료.현재쓰레드.FPUBuffer)
			}

			//fxrstor(스케줄러_자료.현재쓰레드.FPUBuffer)
			
			스케줄러_자료.현재쓰레드 = 다음쓰레드

			if 다음쓰레드.P쓰레드_상태 == Started{
				다음쓰레드.P쓰레드_상태 = Ready
				InitalThreadUserJump(다음쓰레드)
			} 

			esp = uint32(uintptr(Pointer(다음쓰레드.P시피유상태)))
			
			스케줄러_자료.tss.M스택_설정(SEG_KERNEL_DATA, 다음쓰레드.P스택+THREAD_STACK_SIZE) 

		}
	}
	
	return esp


}

func enter_usermode(uint32, uint32, uint32)
func enter_usermode_sysexit(uint32, uint32, uint32)
func JumpUserMode()
func DisableInt()

func InitalThreadUserJump(쓰레드 *T쓰레드){

	DisableInt()

	스케줄러_자료.tss.M스택_설정(SEG_KERNEL_DATA, 쓰레드.P스택 + THREAD_STACK_SIZE)
	//스케줄러_자료.tss.M스택_설정(SEG_USER_DATA, 쓰레드.P스택 + THREAD_STACK_SIZE)
	스케줄러_자료.현재쓰레드 = 쓰레드
	스케줄러_자료.활성화됨 = true

	esp := uint32(uintptr(Pointer(쓰레드.P시피유상태)))
	//esp = 쓰레드.P스택 + THREAD_STACK_SIZE
	//cpu := (*T시피유상태)(Pointer(uintptr(esp)))

	eip := 쓰레드.P시피유상태.Eip
	user_esp := 쓰레드.P사용자스택+쓰레드.P사용자스택크기
	eflags := 쓰레드.P시피유상태.Eflags
	cs := 쓰레드.P시피유상태.Cs

	콘솔.M출력("tss[")
	콘솔.MUint32출력(eip)
	콘솔.M출력(":")
	콘솔.MUint32출력(user_esp)
	콘솔.M출력(":")
	콘솔.MUint32출력(eflags)
	콘솔.M출력(":")
	콘솔.MUint32출력(cs)
	콘솔.M출력(":")

	콘솔.MUint32출력(esp)
	콘솔.M출력("]")

	//PortOutByte(0x20, 0x20)
	바이트포트 := T바이트포트{}
	바이트포트.M초기화(0x20)
	바이트포트.M쓰기(0x20)


	enter_usermode(eip, user_esp, eflags)	
	//enter_usermode_sysexit(eip, user_esp, eflags)
	//JumpUserMode()
}
