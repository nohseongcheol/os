package drivermanager

type IDriver interface{
	Activate()
	Reset() int
	Deactivate()
}

type T駆動装置の管理者_資料 struct{
	iDrivers[256] IDriver
	numDrivers int
}
var 資料 T駆動装置の管理者_資料

type T駆動装置の管理者 struct{
}


func (self *T駆動装置の管理者) M初期化() {
	資料.numDrivers = 0
}

func (self *T駆動装置の管理者) AddDriver(drv IDriver) {
	資料.iDrivers[資料.numDrivers] = drv
	資料.numDrivers++
}
func (self *T駆動装置の管理者) ActivateAll() {
	for i:=0; i<資料.numDrivers; i++ {
		資料.iDrivers[i].Activate()
	}
}
