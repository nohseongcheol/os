/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 가상기억공간

import . "공통"

const (
	C핵심가상주소	= 3 * Gb
	U사용자쌓임공간크기	= 32 * Kb
	U사용자쌓임공간위	= 64 * Mb
	U사용자쌓임공간	= U사용자쌓임공간위 - U사용자쌓임공간크기
)

func F가상기억공간시험() {
	F자료형시험()
}
