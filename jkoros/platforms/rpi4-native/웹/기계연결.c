#include "../명명/기계연결이름.h"
#include "브라우저.h"
#include "../기계/화면정보.h"
extern uintptr_t 보드터미널(uintptr_t),보드밀리초(void),보드화면기억공간(void),보드글자쓰기(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
int 웹현재창(void){return (int)보드터미널(10)-1;}
void 웹화면준비(void){보드화면기억공간();보드터미널(301);}
void 웹화면새로(void){보드터미널(3);}
unsigned 웹화면너비(void){return 보드화면너비();}
unsigned 웹화면높이(void){return 보드화면높이();}
void 웹사각(int 가,int 나,int 폭,int 높이,uint32_t 색){보드사각그림(가,나,폭,높이,색);}
void 웹글자(int 가,int 나,unsigned 글,uint32_t 색,uint32_t 바탕){터미널글자그림(가,나,글,색,바탕);}
void 웹출력(unsigned 글){보드글자쓰기(글);}
uintptr_t 웹밀리초(void){return 보드밀리초();}

extern void 보드웹입력살피기(void);
void 웹입력살피기(void){보드웹입력살피기();}
int 웹범위(int *가,int *나,int *폭,int *높이){return 보드그림범위(가,나,폭,높이);}

void 웹가리개옮기기(int 가,int 나){보드포인터(가,나,1);}
