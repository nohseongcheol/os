/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package 자판

import . "단말기"

type T기본자판사건처리기 struct{
}
func (자신 *T기본자판사건처리기) M키누른동시(값 byte){
        _16진수 := [16] byte{'0', '1', '2', '3',
                        '4', '5', '6', '7',
                        '8', '9', 'A', 'B',
                        'C', 'D', 'E', 'F'}

        임시문자열 := []byte("\n\n\n\n\n\nkeyboard :    ")
        임시문자열[17] = _16진수[((값 >>4)  & 0xF)]
        임시문자열[18] = _16진수[값 & 0xF]

        단말기 := new(T단말기)

        단말기.M출력(임시문자열)


}
func (자신 *T기본자판사건처리기) M키떼는동시(값 byte){
}

