/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <字符分类.h>

/* Single-byte C/POSIX locale; these are not Unicode character classifiers. */
int 检查是否大写字母(int 字符值) { return 字符值 >= 'A' && 字符值 <= 'Z'; }
int 检查是否小写字母(int 字符值) { return 字符值 >= 'a' && 字符值 <= 'z'; }
int 检查是否字母(int 字符值) { return 检查是否大写字母(字符值) || 检查是否小写字母(字符值); }
int 检查是否十进数字(int 字符值) { return 字符值 >= '0' && 字符值 <= '9'; }
int 检查是否字母或数字(int 字符值) { return 检查是否字母(字符值) || 检查是否十进数字(字符值); }
int 检查是否水平空白(int 字符值) { return 字符值 == ' ' || 字符值 == '\t'; }
int 检查是否空白字符(int 字符值) { return 字符值 == ' ' || (字符值 >= '\t' && 字符值 <= '\r'); }
int 检查是否控制字符(int 字符值) { return (字符值 >= 0 && 字符值 < 32) || 字符值 == 127; }
int 检查是否可印字符(int 字符值) { return 字符值 >= 32 && 字符值 <= 126; }
int 检查是否非空白可印字符(int 字符值) { return 字符值 >= 33 && 字符值 <= 126; }
int 检查是否标点符号(int 字符值) { return 检查是否非空白可印字符(字符值) && !检查是否字母或数字(字符值); }
int 检查是否十六进数字(int 字符值) { return 检查是否十进数字(字符值) || (字符值 >= 'a' && 字符值 <= 'f') || (字符值 >= 'A' && 字符值 <= 'F'); }
int 转换为小写(int 字符值) { return 检查是否大写字母(字符值) ? 字符值 + ('a' - 'A') : 字符值; }
int 转换为大写(int 字符值) { return 检查是否小写字母(字符值) ? 字符值 - ('a' - 'A') : 字符值; }
