#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long maṣíìnì_Ọ̀rọ̀;
static maṣíìnì_Ọ̀rọ̀ 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";kọ_fáìlì_détà(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(maṣíìnì_Ọ̀rọ̀ *kójọ_Ibi_ìpamọ́,int *깊이,maṣíìnì_Ọ̀rọ̀ iye){if(*깊이<0||*깊이>=128)자바실패();kójọ_Ibi_ìpamọ́[(*깊이)++]=iye;}
maṣíìnì_Ọ̀rọ̀ 자바꺼내기(maṣíìnì_Ọ̀rọ̀ *kójọ_Ibi_ìpamọ́,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return kójọ_Ibi_ìpamọ́[--*깊이];}
maṣíìnì_Ọ̀rọ̀ 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();maṣíìnì_Ọ̀rọ̀*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (maṣíìnì_Ọ̀rọ̀)자료위치;}
maṣíìnì_Ọ̀rọ̀ *자바색인(maṣíìnì_Ọ̀rọ̀ nǹkan_Ìtọ́ka,int 개수){maṣíìnì_Ọ̀rọ̀*자료위치=(maṣíìnì_Ọ̀rọ̀*)nǹkan_Ìtọ́ka;if(!자료위치||개수<0||(maṣíìnì_Ọ̀rọ̀)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(maṣíìnì_Ọ̀rọ̀ nǹkan_Ìtọ́ka){if(!nǹkan_Ìtọ́ka)자바실패();return *(maṣíìnì_Ọ̀rọ̀*)nǹkan_Ìtọ́ka;}
int 자바나누기(int ibi_ìtọ́kasí_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(ibi_ìtọ́kasí_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:ibi_ìtọ́kasí_x;return 나머지?ibi_ìtọ́kasí_x%세로좌표:ibi_ìtọ́kasí_x/세로좌표;}
static unsigned gígùn_iye(const char*fọ́nrán_détà){unsigned 개수=0;if(!fọ́nrán_détà)자바실패();while(fọ́nrán_détà[개수])개수++;return 개수;}
void 자바출력(maṣíìnì_Ọ̀rọ̀ 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int iye=(int)자료위치;unsigned 부호없는값=iye<0?0-(unsigned)iye:iye;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(iye<0)둘째값[개수++]='-';while(개수)kọ_fáìlì_détà(1,둘째값+--개수,1);}
    else{const char*fọ́nrán_détà=자료위치?(const char*)자료위치:"null";kọ_fáìlì_détà(1,fọ́nrán_détà,gígùn_iye(fọ́nrán_détà));}if(줄바꿈)kọ_fáìlì_détà(1,"\n",1);
}
maṣíìnì_Ọ̀rọ̀ 자바파일쓰기(maṣíìnì_Ọ̀rọ̀ ọ̀nà,maṣíìnì_Ọ̀rọ̀ iye){const char*fọ́nrán_détà=(const char*)iye;unsigned 개수=gígùn_iye(fọ́nrán_détà);int fáìlì_èkù=ṣí_fáìlì((const char*)ọ̀nà,쓰기전용|없으면만들기|내용비우기,0600);if(fáìlì_èkù<0)자바실패();int 반환값=kọ_fáìlì_détà(fáìlì_èkù,fọ́nrán_détà,개수);pa_dé_fáìlì(fáìlì_èkù);if(반환값!=(int)개수)자바실패();return 0;}
maṣíìnì_Ọ̀rọ̀ 자바파일읽기(maṣíìnì_Ọ̀rọ̀ ọ̀nà){int fáìlì_èkù=ṣí_fáìlì((const char*)ọ̀nà,kàn_kàá_iye,0);if(fáìlì_èkù<0)자바실패();int 개수=fáìlì_ìwọn(fáìlì_èkù);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(fáìlì_èkù,자료위치,개수);pa_dé_fáìlì(fáìlì_èkù);if(반환값!=개수)자바실패();자료위치[개수]=0;return (maṣíìnì_Ọ̀rọ̀)자료위치;}
