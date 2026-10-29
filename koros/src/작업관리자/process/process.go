/*
        Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 프로세스

import . "unsafe"
import . "util/list"
import 메모리 "memorymanager"
import . "tasking/thread"

const PROC_USER_HEAP_SIZE=1*1024*1024

type T프로세스 struct{
	식별자 int
	시스템콜_식별자 int
	P사용자공간 bool
	args *[]byte

	//state T프로세스State	

	P쓰레드들 *T링크드_리스트
	P파일이름 [] byte
}
var 리스트 T링크드_리스트 = T링크드_리스트{}
func (자신 *T프로세스) M초기화(메모리 *메모리.T메모리_관리자){
	자신.P쓰레드들 = &리스트
	자신.P쓰레드들.M초기화(메모리)
}


type T프로세스_헬퍼 struct{
	프로세스들 T링크드_리스트
	메모리 *메모리.T메모리_관리자
}
func (자신 *T프로세스_헬퍼)M초기화(메모리 *메모리.T메모리_관리자){
	자신.메모리 = 메모리
	T프로세스들.M초기화(자신.메모리)
}
var T프로세스들 T링크드_리스트 = T링크드_리스트{}
var 현재_프로세스식별자 int=1
func (자신 *T프로세스_헬퍼) M생성(entryPoint func(), 쓰레드_헐퍼 *T쓰레드_헬퍼, isKernel bool) T프로세스{
	프로세스 := T프로세스{}
	프로세스.M초기화(자신.메모리)
	프로세스.식별자 = 현재_프로세스식별자
	현재_프로세스식별자++
	mainThread := 쓰레드_헐퍼.M함수로부터_생성(entryPoint, isKernel)
	프로세스.P쓰레드들.M뒤에밀어넣기(uintptr(Pointer(&mainThread)))
	
	T프로세스들.M뒤에밀어넣기(uintptr(Pointer(&프로세스)))
	return 프로세스
}
func (자신 *T프로세스_헬퍼) CreateFromData() T프로세스{
	프로세스 := T프로세스{}
	return 프로세스
}
