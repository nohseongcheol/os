/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣言_体系_体系呼出
#define _宣言_体系_体系呼出

long __syscall6(long 呼出番号, long 第一引数, long 第二引数, long 第三引数,
                      long 第四引数, long 第五引数, long 第六引数);
long __syscall_result(long 結果);

#endif
