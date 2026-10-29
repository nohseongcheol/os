/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Įjungti()
	Atstatyti() int
	Išjungti()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var skaičiusdriver int

func (self *TDrivermanager) Init() {
	skaičiusdriver = 0
}

func (self *TDrivermanager) Pridėtidriver(driver_2 IDriver) {
	idriver[skaičiusdriver] = driver_2
	skaičiusdriver++
}
func (self *TDrivermanager) ĮjungtiVisi() {
	for i := 0; i < skaičiusdriver; i++ {
		idriver[i].Įjungti()
	}
}
