/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aktivovat()
	Inicializovat() int
	Deaktivovat()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var číslodriver int

func (self *TDrivermanager) Init() {
	číslodriver = 0
}

func (self *TDrivermanager) Přidatdriver(driver_2 IDriver) {
	idriver[číslodriver] = driver_2
	číslodriver++
}
func (self *TDrivermanager) AktivovatVše() {
	for i := 0; i < číslodriver; i++ {
		idriver[i].Aktivovat()
	}
}
