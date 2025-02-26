/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package 기억공간관리자

import . "unsafe"

const 최대_대기행렬_크기 uint32 = 10*1024*1024
var 대기행렬 [최대_대기행렬_크기]byte

type T기억공간덩어리 struct {
	다음 *T기억공간덩어리
	이전 *T기억공간덩어리
	할당됨 bool

	크기 uint32
}

type T기억공간관리자 struct {
}
var 첫번째 *T기억공간덩어리
var 활성기억공간관리자 *T기억공간관리자 = nil
var 기억공간덩어리크기 uint32
func (자신 *T기억공간관리자) M초기화(시작 uint32, 크기 uint32) {
	활성기억공간관리자 = 자신

	기억공간덩어리크기 = uint32(Sizeof(T기억공간덩어리{}))

	if 크기 < 기억공간덩어리크기 {
		첫번째 = nil
	}else {
		첫번째 = (*T기억공간덩어리)(Pointer(uintptr(Pointer(&대기행렬)) + uintptr(시작)))
		첫번째.할당됨 = false
		첫번째.이전 = nil
		첫번째.다음 = nil
		첫번째.크기 = 크기 - 기억공간덩어리크기
	}
	
	첫번째 = (*T기억공간덩어리)(Pointer(uintptr(Pointer(&대기행렬)) + uintptr(시작)))
}
func (자신 *T기억공간관리자) Destroy() {
	if 활성기억공간관리자 == 자신 {
		활성기억공간관리자 = nil
	}
}
func (자신 *T기억공간관리자) MM할당(크기 uint32) Pointer{
	var 결과 *T기억공간덩어리 = nil

	var 덩어리 *T기억공간덩어리 = 첫번째
	for ; 덩어리!=nil && 결과==nil; 덩어리=덩어리.다음 {
		if 덩어리.크기 > 크기 && !덩어리.할당됨 {
			결과 = 덩어리
		}
	}
	
	if 결과 == nil {
		return nil
	}

	if 결과.크기 >= (크기+기억공간덩어리크기+1) {
		var 임시 *T기억공간덩어리
		임시 = (*T기억공간덩어리)(Pointer(uintptr(uint32(uintptr(Pointer(결과)))+기억공간덩어리크기+크기)))
		
		임시.할당됨 = false
		임시.크기 = 결과.크기 - 크기 - 기억공간덩어리크기
		임시.이전 = 결과
		임시.다음 = 결과.다음

		if 임시.다음 != nil {
			임시.다음.이전 = 임시
		}

		결과.크기 = 크기
		결과.다음 = 임시
	}
	결과.할당됨 = true
		
	return Pointer(uintptr(Pointer(결과)) + uintptr(기억공간덩어리크기))
}
func (자신 *T기억공간관리자) M해제(ptr Pointer) {
	var 덩어리 *T기억공간덩어리 = (*T기억공간덩어리)(Pointer(uintptr(ptr) - uintptr(기억공간덩어리크기)))
	덩어리.할당됨 = false
	
	if 덩어리.이전 != nil && !덩어리.이전.할당됨 {
		덩어리.이전.다음 = 덩어리.다음
		덩어리.이전.크기 += 덩어리.크기 + 기억공간덩어리크기
		if 덩어리.다음 != nil {
			덩어리.다음.이전 = 덩어리.이전
		}
	}

	if 덩어리.다음 != nil && !덩어리.다음.할당됨 {
		덩어리.크기 += 덩어리.다음.크기 + 기억공간덩어리크기
		덩어리.다음 = 덩어리.다음.다음
		if 덩어리.다음 != nil {
			덩어리.다음.이전 = 덩어리
		}
	}
}
func New(크기 int) Pointer{
	if 활성기억공간관리자 == nil {
		return nil
	}
	return 활성기억공간관리자.MM할당(uint32(크기))
}
func Delete(ptr Pointer) {
	if 활성기억공간관리자 == nil {
		활성기억공간관리자.M해제(ptr)
	}
}
