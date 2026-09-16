/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtmem

import . "common"

const (
	KERNEL_VIRT_ADDR	= 3 * GB
	USER_STACK_SIZE		= 32 * KB
	USER_STACK_TOP		= 64 * MB
	USER_STACK		= USER_STACK_TOP - USER_STACK_SIZE
)

func VirtTest() {
	TypeTest()
}
