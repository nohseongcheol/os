/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aktivera()
	Återställ() int
	Inaktivera()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var nummerdriver int

func (själv *TDrivermanager) Init() {
	nummerdriver = 0
}

func (själv *TDrivermanager) Läggtilldriver(driver_2 IDriver) {
	idriver[nummerdriver] = driver_2
	nummerdriver++
}
func (själv *TDrivermanager) AktiveraAlla() {
	for i := 0; i < nummerdriver; i++ {
		idriver[i].Aktivera()
	}
}
