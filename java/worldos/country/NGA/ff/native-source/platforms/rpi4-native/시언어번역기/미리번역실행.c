#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long 기계낱말;
static 기계낱말 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char binndi[]="AOT runtime error\n";winndude_fiilde_keɓe(2,binndi,sizeof(binndi)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(기계낱말 *쌓임공간,int *깊이,기계낱말 njaru){if(*깊이<0||*깊이>=128)자바실패();쌓임공간[(*깊이)++]=njaru;}
기계낱말 자바꺼내기(기계낱말 *쌓임공간,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return 쌓임공간[--*깊이];}
기계낱말 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();기계낱말*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (기계낱말)자료위치;}
기계낱말 *자바색인(기계낱말 객체참조,int 개수){기계낱말*자료위치=(기계낱말*)객체참조;if(!자료위치||개수<0||(기계낱말)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(기계낱말 객체참조){if(!객체참조)자바실패();return *(기계낱말*)객체참조;}
int 자바나누기(int 가로좌표,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(가로좌표==(-2147483647-1)&&세로좌표==-1)return 나머지?0:가로좌표;return 나머지?가로좌표%세로좌표:가로좌표/세로좌표;}
static unsigned njuuteendi_njaru(const char*ɓoggol_keɓe){unsigned 개수=0;if(!ɓoggol_keɓe)자바실패();while(ɓoggol_keɓe[개수])개수++;return 개수;}
void 자바출력(기계낱말 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int njaru=(int)자료위치;unsigned 부호없는값=njaru<0?0-(unsigned)njaru:njaru;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(njaru<0)둘째값[개수++]='-';while(개수)winndude_fiilde_keɓe(1,둘째값+--개수,1);}
    else{const char*ɓoggol_keɓe=자료위치?(const char*)자료위치:"null";winndude_fiilde_keɓe(1,ɓoggol_keɓe,njuuteendi_njaru(ɓoggol_keɓe));}if(줄바꿈)winndude_fiilde_keɓe(1,"\n",1);
}
기계낱말 자바파일쓰기(기계낱말 laawol,기계낱말 njaru){const char*ɓoggol_keɓe=(const char*)njaru;unsigned 개수=njuuteendi_njaru(ɓoggol_keɓe);int fiilde_jaggoode=udditde_fiilde((const char*)laawol,쓰기전용|없으면만들기|내용비우기,0600);if(fiilde_jaggoode<0)자바실패();int 반환값=winndude_fiilde_keɓe(fiilde_jaggoode,ɓoggol_keɓe,개수);uddude_fiilde(fiilde_jaggoode);if(반환값!=(int)개수)자바실패();return 0;}
기계낱말 자바파일읽기(기계낱말 laawol){int fiilde_jaggoode=udditde_fiilde((const char*)laawol,janngotooɗo_tan_njaru,0);if(fiilde_jaggoode<0)자바실패();int 개수=fiilde_waylude_etannde(fiilde_jaggoode);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(fiilde_jaggoode,자료위치,개수);uddude_fiilde(fiilde_jaggoode);if(반환값!=개수)자바실패();자료위치[개수]=0;return (기계낱말)자료위치;}
