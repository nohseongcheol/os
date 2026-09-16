/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aהפעל()
	Rאפס() int
	Dבטל()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var מספרdriver int

func (self *TDrivermanager) Init() {
	מספרdriver = 0
}

func (self *TDrivermanager) Aהוספהdriver(driver_2 IDriver) {
	idriver[מספרdriver] = driver_2
	מספרdriver++
}
func (self *TDrivermanager) Aהפעלהכל() {
	for i := 0; i < מספרdriver; i++ {
		idriver[i].Aהפעל()
	}
}
