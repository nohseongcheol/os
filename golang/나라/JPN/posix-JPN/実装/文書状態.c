/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <体系/文書状態.h>
#include <体系/体系情報.h>
#include <体系/体系呼出.h>

enum { 体系呼出_文書状態 = 106, 体系呼出_連結自体の状態を得る = 107, 体系呼出_開いた文書の状態を得る = 108, 体系呼出_体系情報を得る = 122 };

int 文書状態(const char *経路, struct 文書状態 *緩衝領域)
{
    return (int)__syscall_result(
        __syscall6(体系呼出_文書状態, (long)経路, (long)緩衝領域, 0, 0, 0, 0));
}

int 連結自体の状態を得る(const char *経路, struct 文書状態 *緩衝領域)
{
    return (int)__syscall_result(
        __syscall6(体系呼出_連結自体の状態を得る, (long)経路, (long)緩衝領域, 0, 0, 0, 0));
}

int 開いた文書の状態を得る(int 文書記述番号, struct 文書状態 *緩衝領域)
{
    return (int)__syscall_result(
        __syscall6(体系呼出_開いた文書の状態を得る, 文書記述番号, (long)緩衝領域, 0, 0, 0, 0));
}

int 体系情報を得る(struct 体系情報 *名前)
{
    return (int)__syscall_result(
        __syscall6(体系呼出_体系情報を得る, (long)名前, 0, 0, 0, 0, 0));
}
