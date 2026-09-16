/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package どらいばー

type Iどらいばー interface {
	Aゆうこうにする()
	Rりせっと() int
	Dむこうにする()
}

type Tどらいばーかんりしゃ struct {
}

var iどらいばー [256]Iどらいばー
var numberどらいばー int

func (self *Tどらいばーかんりしゃ) Init() {
	numberどらいばー = 0
}

func (self *Tどらいばーかんりしゃ) Aついかどらいばー(どらいばー_2 Iどらいばー) {
	iどらいばー[numberどらいばー] = どらいばー_2
	numberどらいばー++
}
func (self *Tどらいばーかんりしゃ) Aゆうこうにするすべて() {
	for i := 0; i < numberどらいばー; i++ {
		iどらいばー[i].Aゆうこうにする()
	}
}
