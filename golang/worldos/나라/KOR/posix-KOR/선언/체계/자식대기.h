#ifndef _선언_체계_자식대기
#define _선언_체계_자식대기

#include <체계/자료형.h>

#define 준비안되면기다리지않기 1
#define 종료값꺼내기(끝난상태) (((끝난상태) >> 8) & 0xff)
#define 정상종료인지확인(끝난상태) (((끝난상태) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
실행과정번호형 자식기다리기(int *끝난상태);
실행과정번호형 지정자식기다리기(실행과정번호형 실행과정번호, int *끝난상태, int 선택사항);
#ifdef __cplusplus
}
#endif

#endif
