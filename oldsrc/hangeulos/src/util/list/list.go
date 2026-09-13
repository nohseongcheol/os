/*
        Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import 메모리 "memorymanager"

type Node struct{
	자료포인터 uintptr
	이전 *Node
	다음 *Node
}
func (자신 *Node) New(자료포인터 uintptr){
	자신.자료포인터 = 자료포인터
}

type T링크드_리스트 struct{
	머리 *Node
	꼬리 *Node
	크기 int

	메모리 *메모리.T메모리_관리자
}
func (자신 *T링크드_리스트) M초기화(메모리 *메모리.T메모리_관리자){
	자신.머리 = nil
	자신.꼬리 = nil
	자신.크기 = 0

	자신.메모리 = 메모리
}
func (자신 *T링크드_리스트) M앞에밀어넣기(자료포인터 uintptr){
	새로운노드 := (*Node)(자신.메모리.Malloc(uint32(Sizeof(Node{}))))
	새로운노드.자료포인터  = 자료포인터
	새로운노드.다음 = 자신.머리
	자신.머리 = 새로운노드
	자신.크기++ 

	if 자신.머리.다음 == nil {
		자신.꼬리 = 자신.머리
	}
	
}
func (자신 *T링크드_리스트) M뒤에밀어넣기(자료포인터 uintptr){
	새로운노드 := (*Node)(자신.메모리.Malloc(uint32(Sizeof(Node{}))))
	새로운노드.자료포인터 = 자료포인터
	
	if 자신.크기 == 0{
		자신.M앞에밀어넣기(자료포인터)
	}else {
		자신.꼬리.다음 = 새로운노드
		자신.꼬리 = 새로운노드
		자신.크기++
	}
}
func (자신 *T링크드_리스트) PushAt(인텍스 int, 자료포인터 uintptr){
	if 인텍스 == 0 {
		자신.M앞에밀어넣기(자료포인터)
	}else{
		이전노드 := 자신.GetNodeAt(인텍스-1)
		다음노드 := 이전노드.다음	
		새로운노드 := (*Node)(자신.메모리.Malloc(uint32(Sizeof(Node{}))))
		새로운노드.자료포인터 = 자료포인터

		이전노드.다음 = 새로운노드
		새로운노드.다음  = 다음노드
		
		자신.크기++

		if 새로운노드.다음 == nil {
			자신.꼬리 = 새로운노드
		}
	}
}
func (자신 *T링크드_리스트) GetNodeAt(인텍스 int) *Node{
	x := 자신.머리
	for i:=0; i<인텍스; i++{
		x = x.다음
	}
	return x
}
func (자신 *T링크드_리스트) GetAt(인텍스 int) Pointer{
	자료포인터 := 자신.GetNodeAt(인텍스).자료포인터
	return Pointer(자료포인터)
}
func (자신 *T링크드_리스트) IndexOf(자료포인터 uintptr) int{
	n := 자신.머리
	i := 0
	for ; i<자신.크기; i++{
		if n.자료포인터 == 자료포인터 {
			return i
		}
		n = n.다음
	}
	return -1 
}
func (자신 *T링크드_리스트) M크기()int{
	return 자신.크기
}
