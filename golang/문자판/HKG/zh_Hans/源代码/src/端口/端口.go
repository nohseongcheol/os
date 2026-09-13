package 端口

var 位置 uint16 = 1

type T端口 struct {
	portnumber uint16
}

type T端口8bit struct {
	T端口
	读取计数	uint16
	写入计数	uint16
}

func (self *T端口8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.读取计数 = 65
	self.写入计数 = 65
}
func (self *T端口8bit) W写入(数据 uint8) {
	P端口出字节(self.portnumber, 数据)
}
func (self *T端口8bit) R读取() uint8 {
	var 结果 = P端口进字节(self.portnumber)
	return 结果
}
func P端口写入字节(portnumber uint16, 数据 uint8) {
	P端口出字节(portnumber, 数据)
}
func P端口读取字节(portnumber uint16) uint8 {
	结果 := P端口进字节(portnumber)
	return 结果
}

type T端口16bit struct {
	T端口
}

func (self *T端口16bit) Init(portnumber uint16) {
	self.T端口.portnumber = portnumber
}
func (self *T端口16bit) W写入(数据 uint16) {
	P端口出字(self.T端口.portnumber, 数据)
}
func (self *T端口16bit) R读取() uint16 {
	var 结果 = P端口进字(self.T端口.portnumber)
	return 结果
}
func P端口写入字(portnumber uint16, 数据 uint16) {
	P端口出字(portnumber, 数据)
}
func P端口读取字(portnumber uint16) uint16 {
	var 结果 uint16 = P端口进字(portnumber)
	return 结果
}

type T端口32bit struct {
	T端口
}

func (self *T端口32bit) Init(portnumber uint16) {
	self.T端口.portnumber = portnumber
}
func (self *T端口32bit) W写入(数据 uint32) {
	P端口出dword(self.T端口.portnumber, 数据)
}
func (self *T端口32bit) R读取() {
	P端口进dword(self.T端口.portnumber)
}
func P端口写入dword(portnumber uint16, 数据 uint32) {
	P端口出dword(portnumber, 数据)
}
func P端口读取dword(portnumber uint16) uint32 {
	var 结果 uint32 = P端口进dword(portnumber)
	return 结果
}

var 读取计数 uint16 = 65
var 写入计数 uint16 = 66

func P端口出字节(portnumber uint16, 数据 uint8)
func P端口进字节(portnumber uint16) uint8

func P端口出字(portnumber uint16, 数据 uint16)
func P端口进字(portnumber uint16) uint16

func P端口出dword(portnumber uint16, 数据 uint32)
func P端口进dword(portnumber uint16) uint32
