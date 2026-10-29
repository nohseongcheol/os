#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long umatshini_Igama;
static umatshini_Igama 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Umbhalo[]="AOT runtime error\n";bhala_ifayile_iingcombolo(2,Umbhalo,sizeof(Umbhalo)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(umatshini_Igama *fumba_Ugcino,int *깊이,umatshini_Igama ixabiso){if(*깊이<0||*깊이>=128)자바실패();fumba_Ugcino[(*깊이)++]=ixabiso;}
umatshini_Igama 자바꺼내기(umatshini_Igama *fumba_Ugcino,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return fumba_Ugcino[--*깊이];}
umatshini_Igama 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();umatshini_Igama*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (umatshini_Igama)자료위치;}
umatshini_Igama *자바색인(umatshini_Igama into_Isalathiso,int 개수){umatshini_Igama*자료위치=(umatshini_Igama*)into_Isalathiso;if(!자료위치||개수<0||(umatshini_Igama)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(umatshini_Igama into_Isalathiso){if(!into_Isalathiso)자바실패();return *(umatshini_Igama*)into_Isalathiso;}
int 자바나누기(int isilungelelanisi_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(isilungelelanisi_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:isilungelelanisi_x;return 나머지?isilungelelanisi_x%세로좌표:isilungelelanisi_x/세로좌표;}
static unsigned ubude_ixabiso(const char*uluhlu_lweekharektha_iingcombolo){unsigned 개수=0;if(!uluhlu_lweekharektha_iingcombolo)자바실패();while(uluhlu_lweekharektha_iingcombolo[개수])개수++;return 개수;}
void 자바출력(umatshini_Igama 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int ixabiso=(int)자료위치;unsigned 부호없는값=ixabiso<0?0-(unsigned)ixabiso:ixabiso;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(ixabiso<0)둘째값[개수++]='-';while(개수)bhala_ifayile_iingcombolo(1,둘째값+--개수,1);}
    else{const char*uluhlu_lweekharektha_iingcombolo=자료위치?(const char*)자료위치:"null";bhala_ifayile_iingcombolo(1,uluhlu_lweekharektha_iingcombolo,ubude_ixabiso(uluhlu_lweekharektha_iingcombolo));}if(줄바꿈)bhala_ifayile_iingcombolo(1,"\n",1);
}
umatshini_Igama 자바파일쓰기(umatshini_Igama INDLELA,umatshini_Igama ixabiso){const char*uluhlu_lweekharektha_iingcombolo=(const char*)ixabiso;unsigned 개수=ubude_ixabiso(uluhlu_lweekharektha_iingcombolo);int ifayile_isibambi=vula_ifayile((const char*)INDLELA,쓰기전용|없으면만들기|내용비우기,0600);if(ifayile_isibambi<0)자바실패();int 반환값=bhala_ifayile_iingcombolo(ifayile_isibambi,uluhlu_lweekharektha_iingcombolo,개수);vala_ifayile(ifayile_isibambi);if(반환값!=(int)개수)자바실패();return 0;}
umatshini_Igama 자바파일읽기(umatshini_Igama INDLELA){int ifayile_isibambi=vula_ifayile((const char*)INDLELA,efundwayo_kuphela_ixabiso,0);if(ifayile_isibambi<0)자바실패();int 개수=ifayile_isayizi(ifayile_isibambi);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(ifayile_isibambi,자료위치,개수);vala_ifayile(ifayile_isibambi);if(반환값!=개수)자바실패();자료위치[개수]=0;return (umatshini_Igama)자료위치;}
