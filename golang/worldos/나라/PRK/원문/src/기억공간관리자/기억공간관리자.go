/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 기억공간관리자_2

import . "unsafe"

const M최대대기열크기 uint32 = 0x1FFFFFF
const Q대기열시작주소 uint32 = 0x1000000

type T기억공간조각 struct {
	다음	*T기억공간조각
	이전	*T기억공간조각
	할당됨	bool

	크기	uint32
}

type T기억공간관리자 struct {
}

var 첫기억조각 *T기억공간조각
var A활성기억공간관리자 *T기억공간관리자 = nil
var 기억공간조각크기 uint32

func (자신 *T기억공간관리자) F관문초기화(시작 uint32, 크기 uint32) {

	A활성기억공간관리자 = 자신

	기억공간조각크기 = uint32(Sizeof(T기억공간조각{}))

	if 크기 < 기억공간조각크기 {
		첫기억조각 = nil
	} else {
		첫기억조각 = (*T기억공간조각)(Pointer(uintptr(Q대기열시작주소) + uintptr(시작)))
		첫기억조각.할당됨 = false
		첫기억조각.이전 = nil
		첫기억조각.다음 = nil
		첫기억조각.크기 = 크기 - 기억공간조각크기
	}
}
func (자신 *T기억공간관리자) M등록해제() {
	if A활성기억공간관리자 == 자신 {
		A활성기억공간관리자 = nil
	}
}
func (자신 *T기억공간관리자) M기억공간할당(크기 uint32) Pointer {
	var 결과 *T기억공간조각 = nil

	var 조각 *T기억공간조각 = 첫기억조각
	for ; 조각 != nil && 결과 == nil; 조각 = 조각.다음 {
		if 조각.크기 > 크기 && !조각.할당됨 {
			결과 = 조각
		}
	}

	if 결과 == nil {
		return nil
	}

	if 결과.크기 >= (크기 + 기억공간조각크기 + 1) {

		var 임시 *T기억공간조각
		임시 = (*T기억공간조각)(Pointer(uintptr(uint32(uintptr(Pointer(결과))) + 기억공간조각크기 + 크기)))

		임시.할당됨 = false
		임시.크기 = 결과.크기 - 크기 - 기억공간조각크기
		임시.이전 = 결과
		임시.다음 = 결과.다음

		if 임시.다음 != nil {
			임시.다음.이전 = 임시
		}

		결과.크기 = 크기
		결과.다음 = 임시
	}
	결과.할당됨 = true

	return Pointer(uintptr(Pointer(결과)) + uintptr(기억공간조각크기))
}
func (자신 *T기억공간관리자) M기억쪽경계맞춰할당(크기 uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if 크기 == 0 || 크기 > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var 결과 *T기억공간조각
	var 차이 uint32
	for 조각 := 첫기억조각; 조각 != nil; 조각 = 조각.다음 {
		if 조각.할당됨 {
			continue
		}
		주소 := uint32(uintptr(Pointer(조각)) + uintptr(기억공간조각크기))
		차이 = (0x1000 - (주소 & 0xFFF)) & 0xFFF
		if 주소+차이 < 주소 {
			continue
		}
		if 차이 <= 조각.크기 && 크기 <= 조각.크기-차이 {
			결과 = 조각
			break
		}
	}
	if 결과 == nil {
		return nil, 0
	}
	크기 += 차이
	if 결과.크기-크기 >= 기억공간조각크기+1 {
		임시 := (*T기억공간조각)(Pointer(uintptr(Pointer(결과)) + uintptr(기억공간조각크기) + uintptr(크기)))
		임시.할당됨 = false
		임시.크기 = 결과.크기 - 크기 - 기억공간조각크기
		임시.이전 = 결과
		임시.다음 = 결과.다음
		if 임시.다음 != nil {
			임시.다음.이전 = 임시
		}
		결과.크기 = 크기
		결과.다음 = 임시
	}
	결과.할당됨 = true
	return Pointer(uintptr(Pointer(결과)) + uintptr(기억공간조각크기) + uintptr(차이)), 차이
}
func (자신 *T기억공간관리자) M기억공간해제(주소참조_2 Pointer) {
	var 조각 *T기억공간조각 = (*T기억공간조각)(Pointer(uintptr(주소참조_2) - uintptr(기억공간조각크기)))
	조각.할당됨 = false

	if 조각.이전 != nil && !조각.이전.할당됨 {
		조각.이전.다음 = 조각.다음
		조각.이전.크기 += 조각.크기 + 기억공간조각크기
		if 조각.다음 != nil {
			조각.다음.이전 = 조각.이전
		}
	}

	if 조각.다음 != nil && !조각.다음.할당됨 {
		조각.크기 += 조각.다음.크기 + 기억공간조각크기
		조각.다음 = 조각.다음.다음
		if 조각.다음 != nil {
			조각.다음.이전 = 조각
		}
	}
}
func N새로만들기(크기 int) Pointer {
	if A활성기억공간관리자 == nil {
		return nil
	}
	return A활성기억공간관리자.M기억공간할당(uint32(크기))
}
func F기억공간해제(주소참조_2 Pointer) {
	if A활성기억공간관리자 != nil {
		A활성기억공간관리자.M기억공간해제(주소참조_2)
	}
}
