package ドライバー

type Iドライバー interface {
	Aユウコウニスル()
	Rリセット() int
	Dムコウニスル()
}

type Tドライバーカンリシャ struct {
}

var iドライバー [256]Iドライバー
var numberドライバー int

func (self *Tドライバーカンリシャ) Init() {
	numberドライバー = 0
}

func (self *Tドライバーカンリシャ) Aツイカドライバー(ドライバー_2 Iドライバー) {
	iドライバー[numberドライバー] = ドライバー_2
	numberドライバー++
}
func (self *Tドライバーカンリシャ) Aユウコウニスルスベテ() {
	for i := 0; i < numberドライバー; i++ {
		iドライバー[i].Aユウコウニスル()
	}
}
