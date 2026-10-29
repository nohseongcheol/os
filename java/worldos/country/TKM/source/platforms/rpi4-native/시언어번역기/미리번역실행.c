#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long kompýuter_Söz;
static kompýuter_Söz 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Metin[]="AOT runtime error\n";ýaz_faýl_maglumat(2,Metin,sizeof(Metin)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(kompýuter_Söz *Desse_Ammar,int *깊이,kompýuter_Söz baha){if(*깊이<0||*깊이>=128)자바실패();Desse_Ammar[(*깊이)++]=baha;}
kompýuter_Söz 자바꺼내기(kompýuter_Söz *Desse_Ammar,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Desse_Ammar[--*깊이];}
kompýuter_Söz 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();kompýuter_Söz*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (kompýuter_Söz)자료위치;}
kompýuter_Söz *자바색인(kompýuter_Söz obýekt_Salgylanma,int 개수){kompýuter_Söz*자료위치=(kompýuter_Söz*)obýekt_Salgylanma;if(!자료위치||개수<0||(kompýuter_Söz)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(kompýuter_Söz obýekt_Salgylanma){if(!obýekt_Salgylanma)자바실패();return *(kompýuter_Söz*)obýekt_Salgylanma;}
int 자바나누기(int x_koordinatasy,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(x_koordinatasy==(-2147483647-1)&&세로좌표==-1)return 나머지?0:x_koordinatasy;return 나머지?x_koordinatasy%세로좌표:x_koordinatasy/세로좌표;}
static unsigned dowamlylyk_baha(const char*setir_maglumat){unsigned 개수=0;if(!setir_maglumat)자바실패();while(setir_maglumat[개수])개수++;return 개수;}
void 자바출력(kompýuter_Söz 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int baha=(int)자료위치;unsigned 부호없는값=baha<0?0-(unsigned)baha:baha;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(baha<0)둘째값[개수++]='-';while(개수)ýaz_faýl_maglumat(1,둘째값+--개수,1);}
    else{const char*setir_maglumat=자료위치?(const char*)자료위치:"null";ýaz_faýl_maglumat(1,setir_maglumat,dowamlylyk_baha(setir_maglumat));}if(줄바꿈)ýaz_faýl_maglumat(1,"\n",1);
}
kompýuter_Söz 자바파일쓰기(kompýuter_Söz Ýol,kompýuter_Söz baha){const char*setir_maglumat=(const char*)baha;unsigned 개수=dowamlylyk_baha(setir_maglumat);int faýl_ryçag=aç_faýl((const char*)Ýol,쓰기전용|없으면만들기|내용비우기,0600);if(faýl_ryçag<0)자바실패();int 반환값=ýaz_faýl_maglumat(faýl_ryçag,setir_maglumat,개수);ýap_faýl(faýl_ryçag);if(반환값!=(int)개수)자바실패();return 0;}
kompýuter_Söz 자바파일읽기(kompýuter_Söz Ýol){int faýl_ryçag=aç_faýl((const char*)Ýol,diňe_okalýan_baha,0);if(faýl_ryçag<0)자바실패();int 개수=faýl_ölçegi_üýtget(faýl_ryçag);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(faýl_ryçag,자료위치,개수);ýap_faýl(faýl_ryçag);if(반환값!=개수)자바실패();자료위치[개수]=0;return (kompýuter_Söz)자료위치;}
