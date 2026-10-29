/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Attiva()
	Ripristina() int
	Disattiva()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var numerodriver int

func (séstesso *TDrivermanager) Init() {
	numerodriver = 0
}

func (séstesso *TDrivermanager) Aggiungidriver(driver_2 IDriver) {
	idriver[numerodriver] = driver_2
	numerodriver++
}
func (séstesso *TDrivermanager) AttivaTutto() {
	for i := 0; i < numerodriver; i++ {
		idriver[i].Attiva()
	}
}
