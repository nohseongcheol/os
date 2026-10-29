#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long mashine_Neno;
static mashine_Neno 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";andika_faili_data(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(mashine_Neno *Mpororo_Hifadhi,int *깊이,mashine_Neno thamani){if(*깊이<0||*깊이>=128)자바실패();Mpororo_Hifadhi[(*깊이)++]=thamani;}
mashine_Neno 자바꺼내기(mashine_Neno *Mpororo_Hifadhi,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Mpororo_Hifadhi[--*깊이];}
mashine_Neno 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();mashine_Neno*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (mashine_Neno)자료위치;}
mashine_Neno *자바색인(mashine_Neno kipengee_Marejeleo,int 개수){mashine_Neno*자료위치=(mashine_Neno*)kipengee_Marejeleo;if(!자료위치||개수<0||(mashine_Neno)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(mashine_Neno kipengee_Marejeleo){if(!kipengee_Marejeleo)자바실패();return *(mashine_Neno*)kipengee_Marejeleo;}
int 자바나누기(int jira_x,int Kitufe_cha_Y_kiratibu,int 나머지){if(!Kitufe_cha_Y_kiratibu)자바실패();if(jira_x==(-2147483647-1)&&Kitufe_cha_Y_kiratibu==-1)return 나머지?0:jira_x;return 나머지?jira_x%Kitufe_cha_Y_kiratibu:jira_x/Kitufe_cha_Y_kiratibu;}
static unsigned urefu_thamani(const char*tungo_data){unsigned 개수=0;if(!tungo_data)자바실패();while(tungo_data[개수])개수++;return 개수;}
void 자바출력(mashine_Neno 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int thamani=(int)자료위치;unsigned 부호없는값=thamani<0?0-(unsigned)thamani:thamani;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(thamani<0)둘째값[개수++]='-';while(개수)andika_faili_data(1,둘째값+--개수,1);}
    else{const char*tungo_data=자료위치?(const char*)자료위치:"null";andika_faili_data(1,tungo_data,urefu_thamani(tungo_data));}if(줄바꿈)andika_faili_data(1,"\n",1);
}
mashine_Neno 자바파일쓰기(mashine_Neno njia,mashine_Neno thamani){const char*tungo_data=(const char*)thamani;unsigned 개수=urefu_thamani(tungo_data);int faili_kishiko=unda_faili((const char*)njia,쓰기전용|없으면만들기|내용비우기,0600);if(faili_kishiko<0)자바실패();int 반환값=andika_faili_data(faili_kishiko,tungo_data,개수);funga_faili(faili_kishiko);if(반환값!=(int)개수)자바실패();return 0;}
mashine_Neno 자바파일읽기(mashine_Neno njia){int faili_kishiko=unda_faili((const char*)njia,soma_tu_thamani,0);if(faili_kishiko<0)자바실패();int 개수=faili_panga_ukubwa(faili_kishiko);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(faili_kishiko,자료위치,개수);funga_faili(faili_kishiko);if(반환값!=개수)자바실패();자료위치[개수]=0;return (mashine_Neno)자료위치;}
