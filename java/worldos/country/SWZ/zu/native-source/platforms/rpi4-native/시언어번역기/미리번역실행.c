#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long umshini_Amagama;
static umshini_Amagama 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Itekisi[]="AOT runtime error\n";bhala_ifayela_imininingwane(2,Itekisi,sizeof(Itekisi)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(umshini_Amagama *Isitaki_Indawo_yokugcina,int *깊이,umshini_Amagama inani){if(*깊이<0||*깊이>=128)자바실패();Isitaki_Indawo_yokugcina[(*깊이)++]=inani;}
umshini_Amagama 자바꺼내기(umshini_Amagama *Isitaki_Indawo_yokugcina,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Isitaki_Indawo_yokugcina[--*깊이];}
umshini_Amagama 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();umshini_Amagama*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (umshini_Amagama)자료위치;}
umshini_Amagama *자바색인(umshini_Amagama into_Ireferensi,int 개수){umshini_Amagama*자료위치=(umshini_Amagama*)into_Ireferensi;if(!자료위치||개수<0||(umshini_Amagama)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(umshini_Amagama into_Ireferensi){if(!into_Ireferensi)자바실패();return *(umshini_Amagama*)into_Ireferensi;}
int 자바나누기(int okuxhumanisa_u_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(okuxhumanisa_u_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:okuxhumanisa_u_x;return 나머지?okuxhumanisa_u_x%세로좌표:okuxhumanisa_u_x/세로좌표;}
static unsigned ubude_inani(const char*uchunge_imininingwane){unsigned 개수=0;if(!uchunge_imininingwane)자바실패();while(uchunge_imininingwane[개수])개수++;return 개수;}
void 자바출력(umshini_Amagama 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int inani=(int)자료위치;unsigned 부호없는값=inani<0?0-(unsigned)inani:inani;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(inani<0)둘째값[개수++]='-';while(개수)bhala_ifayela_imininingwane(1,둘째값+--개수,1);}
    else{const char*uchunge_imininingwane=자료위치?(const char*)자료위치:"null";bhala_ifayela_imininingwane(1,uchunge_imininingwane,ubude_inani(uchunge_imininingwane));}if(줄바꿈)bhala_ifayela_imininingwane(1,"\n",1);
}
umshini_Amagama 자바파일쓰기(umshini_Amagama Indlela_2,umshini_Amagama inani){const char*uchunge_imininingwane=(const char*)inani;unsigned 개수=ubude_inani(uchunge_imininingwane);int ifayela_isibambo=vula_ifayela((const char*)Indlela_2,쓰기전용|없으면만들기|내용비우기,0600);if(ifayela_isibambo<0)자바실패();int 반환값=bhala_ifayela_imininingwane(ifayela_isibambo,uchunge_imininingwane,개수);vala_ifayela(ifayela_isibambo);if(반환값!=(int)개수)자바실패();return 0;}
umshini_Amagama 자바파일읽기(umshini_Amagama Indlela_2){int ifayela_isibambo=vula_ifayela((const char*)Indlela_2,fundwayo_kuphela_inani,0);if(ifayela_isibambo<0)자바실패();int 개수=ifayela_linganisa(ifayela_isibambo);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(ifayela_isibambo,자료위치,개수);vala_ifayela(ifayela_isibambo);if(반환값!=개수)자바실패();자료위치[개수]=0;return (umshini_Amagama)자료위치;}
