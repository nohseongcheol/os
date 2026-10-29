/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 虚拟内存

import . "通用"

const (
	K内核virtaddress	= 3 * Gb
	U用户stack大小	= 32 * Kb
	U用户stack上	= 64 * M毫巴
	U用户stack	= U用户stack上 - U用户stack大小
)

func Virt测试() {
	T类型测试()
}
