/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package driver

type IDriver interface{
	Activate()
	Reset() int
	Deactivate()
}

type T드라이버관리자 struct{
}

var iDrivers[256] IDriver
var numDrivers int

func (self *T드라이버관리자) M초기화() {
	numDrivers = 0
}

func (self *T드라이버관리자) AddDriver(drv IDriver) {
	iDrivers[numDrivers] = drv
	numDrivers++
}
func (self *T드라이버관리자) ActivateAll() {
	for i:=0; i<numDrivers; i++ {
		iDrivers[i].Activate()
	}
}
