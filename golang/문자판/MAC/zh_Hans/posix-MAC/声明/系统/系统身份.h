/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _声明_系统_系统身份
#define _声明_系统_系统身份

struct 系统身份信息 {
    char 系统名称[65];
    char 节点名称[65];
    char 系统发行版[65];
    char 系统修订版[65];
    char 机器类型[65];
};

#ifdef __cplusplus
extern "C" {
#endif
int 取得系统信息(struct 系统身份信息 *系统资料);
#ifdef __cplusplus
}
#endif

#endif
