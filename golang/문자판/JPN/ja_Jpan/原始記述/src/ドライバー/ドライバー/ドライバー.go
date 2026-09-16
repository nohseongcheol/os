/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ドライバー

type Iドライバー interface {
	A有効にする()
	Rリセット() int
	D無効にする()
}

type Tドライバー管理者 struct {
}

var iドライバー [256]Iドライバー
var numberドライバー int

func (self *Tドライバー管理者) Init() {
	numberドライバー = 0
}

func (self *Tドライバー管理者) A追加ドライバー(ドライバー_2 Iドライバー) {
	iドライバー[numberドライバー] = ドライバー_2
	numberドライバー++
}
func (self *Tドライバー管理者) A有効にするすべて() {
	for i := 0; i < numberドライバー; i++ {
		iドライバー[i].A有効にする()
	}
}
