/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣告_系統_系統呼叫
#define _宣告_系統_系統呼叫

long __syscall6(long 呼叫編號, long 第一引數, long 第二引數, long 第三引數,
                      long 第四引數, long 第五引數, long 第六引數);
long __syscall_result(long 結果);

#endif
