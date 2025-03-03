/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package 자판

import . "console"

type T基本キーボード事件處理器 struct{
}
func (自身 *T基本キーボード事件處理器) Mキーが押し下げられた時(値 byte){
        _16進法 := [16] byte{'0', '1', '2', '3',
                        '4', '5', '6', '7',
                        '8', '9', 'A', 'B',
                        'C', 'D', 'E', 'F'}

        臨時文字列 := []byte("\n\n\n\n\n\nkeyboard :    ")
        臨時文字列[17] = _16進法[((値 >>4)  & 0xF)]
        臨時文字列[18] = _16進法[値 & 0xF]

        端末機 := new(T端末機)

        端末機.M出力(臨時文字列)


}
func (自身 *T基本キーボード事件處理器) Mキーを離された時(値 byte){
}

