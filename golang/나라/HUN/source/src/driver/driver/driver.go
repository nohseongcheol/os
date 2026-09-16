/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aktiválás()
	Visszaállítás() int
	Deaktiválás()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var számdriver int

func (self *TDrivermanager) Init() {
	számdriver = 0
}

func (self *TDrivermanager) Hozzáadásdriver(driver_2 IDriver) {
	idriver[számdriver] = driver_2
	számdriver++
}
func (self *TDrivermanager) AktiválásÖsszes() {
	for i := 0; i < számdriver; i++ {
		idriver[i].Aktiválás()
	}
}
