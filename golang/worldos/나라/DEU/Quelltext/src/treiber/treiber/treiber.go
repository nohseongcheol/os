/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package treiber

type ITreiber interface {
	Aktivieren()
	Zurücksetzen() int
	Deaktivieren()
}

type TTreiberVerwalter struct {
}

var iTreiber [256]ITreiber
var nummerTreiber int

func (selbst *TTreiberVerwalter) Init() {
	nummerTreiber = 0
}

func (selbst *TTreiberVerwalter) HinzufügenTreiber(treiber_2 ITreiber) {
	iTreiber[nummerTreiber] = treiber_2
	nummerTreiber++
}
func (selbst *TTreiberVerwalter) AktivierenAlle() {
	for i := 0; i < nummerTreiber; i++ {
		iTreiber[i].Aktivieren()
	}
}
