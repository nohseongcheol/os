/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Faollashtirish()
	Tiklash() int
	Faolsizlantirish()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var rAQAMdriver int

func (self *TDrivermanager) Init() {
	rAQAMdriver = 0
}

func (self *TDrivermanager) Qoʻshishdriver(driver_2 IDriver) {
	idriver[rAQAMdriver] = driver_2
	rAQAMdriver++
}
func (self *TDrivermanager) FaollashtirishHammasi() {
	for i := 0; i < rAQAMdriver; i++ {
		idriver[i].Faollashtirish()
	}
}
