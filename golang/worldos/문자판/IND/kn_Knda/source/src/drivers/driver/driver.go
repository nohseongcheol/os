/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Activate()
	Reset() int
	Deactivate()
}

type TDriverManager struct {
}

var iDrivers [256]IDriver
var numDrivers int

func (self *TDriverManager) Vಆರಂಭಿಸು() {
	numDrivers = 0
}

func (self *TDriverManager) AddDriver(drv IDriver) {
	iDrivers[numDrivers] = drv
	numDrivers++
}
func (self *TDriverManager) ActivateAll() {
	for i := 0; i < numDrivers; i++ {
		iDrivers[i].Activate()
	}
}
