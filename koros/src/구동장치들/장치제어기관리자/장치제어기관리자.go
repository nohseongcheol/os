/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package 장치제어기관리자

type IDriver interface{
	Activate()
	Reset() int
	Deactivate()
}

type T장치제어기_관리자_자료 struct{
	iDrivers[256] IDriver
	numDrivers int
}
var 자료 T장치제어기_관리자_자료

type T장치제어기_관리자 struct{
}


func (self *T장치제어기_관리자) M초기화() {
	자료.numDrivers = 0
}

func (self *T장치제어기_관리자) AddDriver(drv IDriver) {
	자료.iDrivers[자료.numDrivers] = drv
	자료.numDrivers++
}
func (self *T장치제어기_관리자) ActivateAll() {
	for i:=0; i<자료.numDrivers; i++ {
		자료.iDrivers[i].Activate()
	}
}
