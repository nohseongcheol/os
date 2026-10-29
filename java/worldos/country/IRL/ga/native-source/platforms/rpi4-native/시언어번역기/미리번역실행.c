#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long meaisín_Word;
static meaisín_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Téacs[]="AOT runtime error\n";scríobh_comhad_sonraí(2,Téacs,sizeof(Téacs)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(meaisín_Word *Cruach_Stóras,int *깊이,meaisín_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();Cruach_Stóras[(*깊이)++]=VALUE;}
meaisín_Word 자바꺼내기(meaisín_Word *Cruach_Stóras,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Cruach_Stóras[--*깊이];}
meaisín_Word 자바배열(int mír_COUNT){if(mír_COUNT<0||(unsigned)mír_COUNT+1>8192-사용량)자바실패();meaisín_Word*sonraí_suíomh=동적기억공간+사용량;사용량+=mír_COUNT+1;sonraí_suíomh[0]=mír_COUNT;return (meaisín_Word)sonraí_suíomh;}
meaisín_Word *자바색인(meaisín_Word oibiacht_Leabhair_thagartha,int mír_COUNT){meaisín_Word*sonraí_suíomh=(meaisín_Word*)oibiacht_Leabhair_thagartha;if(!sonraí_suíomh||mír_COUNT<0||(meaisín_Word)mír_COUNT>=sonraí_suíomh[0])자바실패();return sonraí_suíomh+mír_COUNT+1;}
int 자바길이(meaisín_Word oibiacht_Leabhair_thagartha){if(!oibiacht_Leabhair_thagartha)자바실패();return *(meaisín_Word*)oibiacht_Leabhair_thagartha;}
int 자바나누기(int x_chomhordanáid,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(x_chomhordanáid==(-2147483647-1)&&세로좌표==-1)return 나머지?0:x_chomhordanáid;return 나머지?x_chomhordanáid%세로좌표:x_chomhordanáid/세로좌표;}
static unsigned fad_VALUE(const char*teaghrán_sonraí){unsigned mír_COUNT=0;if(!teaghrán_sonraí)자바실패();while(teaghrán_sonraí[mír_COUNT])mír_COUNT++;return mír_COUNT;}
void 자바출력(meaisín_Word sonraí_suíomh,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned mír_COUNT=0;int VALUE=(int)sonraí_suíomh;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[mír_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[mír_COUNT++]='-';while(mír_COUNT)scríobh_comhad_sonraí(1,SECOND_VALUE+--mír_COUNT,1);}
    else{const char*teaghrán_sonraí=sonraí_suíomh?(const char*)sonraí_suíomh:"null";scríobh_comhad_sonraí(1,teaghrán_sonraí,fad_VALUE(teaghrán_sonraí));}if(줄바꿈)scríobh_comhad_sonraí(1,"\n",1);
}
meaisín_Word 자바파일쓰기(meaisín_Word CONAIR,meaisín_Word VALUE){const char*teaghrán_sonraí=(const char*)VALUE;unsigned mír_COUNT=fad_VALUE(teaghrán_sonraí);int comhad_hanla=oscail_comhad((const char*)CONAIR,쓰기전용|없으면만들기|내용비우기,0600);if(comhad_hanla<0)자바실패();int 반환값=scríobh_comhad_sonraí(comhad_hanla,teaghrán_sonraí,mír_COUNT);dún_comhad(comhad_hanla);if(반환값!=(int)mír_COUNT)자바실패();return 0;}
meaisín_Word 자바파일읽기(meaisín_Word CONAIR){int comhad_hanla=oscail_comhad((const char*)CONAIR,inléite_amháin_VALUE,0);if(comhad_hanla<0)자바실패();int mír_COUNT=comhad_socraigh_méid(comhad_hanla);if(mír_COUNT<0||mír_COUNT>16384||(unsigned)(mír_COUNT+8)/8>8192-사용량)자바실패();char*sonraí_suíomh=(char*)(동적기억공간+사용량);사용량+=(mír_COUNT+8)/8;int 반환값=파일자료읽기(comhad_hanla,sonraí_suíomh,mír_COUNT);dún_comhad(comhad_hanla);if(반환값!=mír_COUNT)자바실패();sonraí_suíomh[mír_COUNT]=0;return (meaisín_Word)sonraí_suíomh;}
