/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Pokreni()
	Ponovopostavi() int
	Obustavi()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var brojdriver int

func (isti *TDrivermanager) Init() {
	brojdriver = 0
}

func (isti *TDrivermanager) Dodajdriver(driver_2 IDriver) {
	idriver[brojdriver] = driver_2
	brojdriver++
}
func (isti *TDrivermanager) PokreniSve() {
	for i := 0; i < brojdriver; i++ {
		idriver[i].Pokreni()
	}
}
