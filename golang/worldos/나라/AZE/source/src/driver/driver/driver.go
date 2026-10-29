/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Activate()
	Sıfırla() int
	Deactivate()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var numberdriver int

func (self *TDrivermanager) Init() {
	numberdriver = 0
}

func (self *TDrivermanager) ƏlavəEtdriver(driver_2 IDriver) {
	idriver[numberdriver] = driver_2
	numberdriver++
}
func (self *TDrivermanager) ActivateHamısı() {
	for i := 0; i < numberdriver; i++ {
		idriver[i].Activate()
	}
}
