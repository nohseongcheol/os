/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 进程

import . "unsafe"
import . "工具/列表"
import mem "内存管理器"
import . "任务管理/线程"
import . "任务管理/调度器"
import . "工具"

const Proc用户heap大小 = 1 * 1024 * 1024

type P进程 struct {
	id		uint32
	syscallid	int
	Is用户空格		bool
	参数		*[]byte

	T线程列表	Linked列表
	Threads	*Linked列表
	F文件名称	[]byte

	P页目录条目	uintptr
}

func (self *P进程) Init(mem *mem.T内存管理器) {
	self.T线程列表 = Linked列表{}
	self.Threads = &self.T线程列表
	self.Threads.Init(mem)
}

type P进程helper struct {
	进程_2	Linked列表
	mem	*mem.T内存管理器
	内核页目录条目	uintptr
}

func (self *P进程helper) Init(mem *mem.T内存管理器, 内核页目录条目 uintptr) {
	self.mem = mem
	self.进程_2 = Linked列表{}
	self.进程_2.Init(self.mem)
	self.内核页目录条目 = 内核页目录条目
}

func (self *P进程helper) C创建(条目point func(), 线程helper *T线程helper, P页目录条目 uint32, is内核 bool) P进程 {
	进程 := (*P进程)(self.mem.M分配内存(uint32(Sizeof(P进程{}))))
	if 进程 == nil {
		return P进程{}
	}
	进程.Init(self.mem)
	进程.id = Allocate进程号()
	进程.P页目录条目 = uintptr(P页目录条目)
	主要线程 := 线程helper.C创建指针from函数(条目point, P页目录条目, is内核)
	if 主要线程 != nil {
		主要线程.P进程号 = 进程.id
		主要线程.Parent进程号 = 0
		进程.Threads.M追加到表尾(uintptr(Pointer(主要线程)))
	}

	self.进程_2.M追加到表尾(uintptr(Pointer(进程)))

	return *进程
}

func (self *P进程helper) Spawn(条目point func(), 线程helper *T线程helper, 调度器 *S调度器, P页目录条目 uint32, is内核 bool) P进程 {
	进程 := self.C创建(条目point, 线程helper, P页目录条目, is内核)
	if 进程.Threads != nil && 进程.Threads.S大小_2 > 0 {
		线程 := (*T线程)(进程.Threads.Getat(0))
		if 线程 != nil && 调度器 != nil {
			调度器.A添加线程(线程)
		}
	}
	return 进程
}

func (self *P进程helper) 复制页目录(源条目 uintptr, 目的条目 uintptr) {
	源_2 := Getunsignedinteger32数组from指针(源条目, 1024, 1024)
	目的_2 := Getunsignedinteger32数组from指针(目的条目, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		目的_2[i] = 源_2[i]
	}
}
func (self *P进程helper) C创建from数据() P进程 {
	进程 := P进程{}
	return 进程
}
