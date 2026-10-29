/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 물리기억공간

import (
	. "공통"
	. "unsafe"
)

const (
	B구획크기		uint32	= 4 * 1024
	C바이트당사용표시수	uint32	= 8
)

type 다중시동기억공간표 struct {
	크기	uint32
	기준주소낮음	uint64
	기준주소높음	uint64
	길이낮음	uint64
	길이높음	uint64
	T종류	uint32
}

func F물리기억공간시험() {
}

var 기억공간연산 T기억공간연산 = T기억공간연산{}

type T물리기억공간관리자 struct {
	기억공간크기	uint32
	사용중구획	uint32
	최대구획	uint32
	기억공간배열	[]uint32
}

var (
	최대구획			uint32	= 0
	기억공간배열			[]uint32
	시동기기억공간정보	다중시동기억공간표
)

func (자신 *T물리기억공간관리자) M사용표시켜기(비트 uint32) uint32 {
	자신.기억공간배열[비트/32] = 자신.기억공간배열[비트/32] | (1 << (비트 % 32))
	return 자신.기억공간배열[비트/32]
}
func (자신 *T물리기억공간관리자) M사용표시뒤집기(비트 uint32) uint32 {
	자신.기억공간배열[비트/32] = 자신.기억공간배열[비트/32] ^ (1 << (비트 % 32))
	return 자신.기억공간배열[비트/32]
}
func (자신 *T물리기억공간관리자) M사용표시읽기(비트 uint32) uint32 {
	반환값 := 자신.기억공간배열[비트/32] & (1 << (비트 % 32))
	return 반환값
}
func (자신 *T물리기억공간관리자) M전체구획수가져오기() uint32 {
	return 자신.최대구획
}
func (자신 *T물리기억공간관리자) M사용중구획수가져오기() uint32 {
	return 자신.사용중구획
}
func (자신 *T물리기억공간관리자) M전체기억공간크기가져오기() uint32 {
	return 자신.기억공간크기
}
func (자신 *T물리기억공간관리자) M사용표시표바이트크기가져오기() uint32 {
	return 자신.기억공간크기 / B구획크기 / C바이트당사용표시수
}

func (자신 *T물리기억공간관리자) M첫빈구획찾기() uint32 {
	for i := uint32(0); i < 자신.M전체구획수가져오기(); i++ {
		if 자신.기억공간배열[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				비트 := uint32(1 << j)
				if (기억공간배열[i] & 비트) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (자신 *T물리기억공간관리자) M연속빈구획찾기(크기 uint32) uint32 {
	if 크기 == 0 {
		return 0xffffffff
	}
	if 크기 == 1 {
		return 자신.M첫빈구획찾기()
	}

	for i := uint32(0); i < 자신.M전체구획수가져오기(); i++ {
		if 자신.기억공간배열[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var 비트 uint32 = 1 << j

				if 자신.기억공간배열[j]&비트 == 0 {
					var 시작비트 uint32 = i * 32
					시작비트 += j

					var 해제 uint32 = 0
					for 개수 := uint32(0); 개수 <= 크기; 개수++ {
						if 자신.M사용표시읽기(시작비트+개수) == 0 {
							해제++
						}

						if 해제 == 크기 {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (자신 *T물리기억공간관리자) F관문초기화(크기 uint32, 사용표시표 []uint32) {
	자신.기억공간크기 = 크기
	자신.기억공간배열 = 사용표시표
	자신.최대구획 = 크기 / B구획크기
	자신.사용중구획 = 자신.최대구획
	기억공간연산.M기억공간채우기(uintptr(Pointer(&자신.기억공간배열)), 0xFF, 자신.사용중구획/C바이트당사용표시수)
}
func (자신 *T물리기억공간관리자) M구획할당() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (자신 *T물리기억공간관리자) M기억쪽경계로올림(주소_2 uint32) uint32 {
	if (주소_2 & 0xFFFFF000) != 주소_2 {
		주소_2 = 주소_2 & 0xFFFFF000
		주소_2 = 주소_2 + 0x1000
	}
	return 주소_2
}
func (자신 *T물리기억공간관리자) M기억쪽경계로내림(주소_2 uint32) uint32 {
	return 주소_2 & 0xFFFFF000
}
