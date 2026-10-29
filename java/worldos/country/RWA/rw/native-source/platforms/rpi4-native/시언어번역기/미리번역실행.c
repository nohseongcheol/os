#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long imashini_Ijambo;
static imashini_Ijambo 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Umwandiko[]="AOT runtime error\n";kwandika_dosiye_amakurushingiro(2,Umwandiko,sizeof(Umwandiko)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(imashini_Ijambo *Ikirundo_Ububiko,int *깊이,imashini_Ijambo agaciro){if(*깊이<0||*깊이>=128)자바실패();Ikirundo_Ububiko[(*깊이)++]=agaciro;}
imashini_Ijambo 자바꺼내기(imashini_Ijambo *Ikirundo_Ububiko,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Ikirundo_Ububiko[--*깊이];}
imashini_Ijambo 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();imashini_Ijambo*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (imashini_Ijambo)자료위치;}
imashini_Ijambo *자바색인(imashini_Ijambo ikintu_Indanga,int 개수){imashini_Ijambo*자료위치=(imashini_Ijambo*)ikintu_Indanga;if(!자료위치||개수<0||(imashini_Ijambo)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(imashini_Ijambo ikintu_Indanga){if(!ikintu_Indanga)자바실패();return *(imashini_Ijambo*)ikintu_Indanga;}
int 자바나누기(int Ihuza_rya_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(Ihuza_rya_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:Ihuza_rya_x;return 나머지?Ihuza_rya_x%세로좌표:Ihuza_rya_x/세로좌표;}
static unsigned uburebure_agaciro(const char*igicenteruro_amakurushingiro){unsigned 개수=0;if(!igicenteruro_amakurushingiro)자바실패();while(igicenteruro_amakurushingiro[개수])개수++;return 개수;}
void 자바출력(imashini_Ijambo 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int agaciro=(int)자료위치;unsigned 부호없는값=agaciro<0?0-(unsigned)agaciro:agaciro;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(agaciro<0)둘째값[개수++]='-';while(개수)kwandika_dosiye_amakurushingiro(1,둘째값+--개수,1);}
    else{const char*igicenteruro_amakurushingiro=자료위치?(const char*)자료위치:"null";kwandika_dosiye_amakurushingiro(1,igicenteruro_amakurushingiro,uburebure_agaciro(igicenteruro_amakurushingiro));}if(줄바꿈)kwandika_dosiye_amakurushingiro(1,"\n",1);
}
imashini_Ijambo 자바파일쓰기(imashini_Ijambo Inzira,imashini_Ijambo agaciro){const char*igicenteruro_amakurushingiro=(const char*)agaciro;unsigned 개수=uburebure_agaciro(igicenteruro_amakurushingiro);int dosiye_umukondo=kurema_dosiye((const char*)Inzira,쓰기전용|없으면만들기|내용비우기,0600);if(dosiye_umukondo<0)자바실패();int 반환값=kwandika_dosiye_amakurushingiro(dosiye_umukondo,igicenteruro_amakurushingiro,개수);gufunga_dosiye(dosiye_umukondo);if(반환값!=(int)개수)자바실패();return 0;}
imashini_Ijambo 자바파일읽기(imashini_Ijambo Inzira){int dosiye_umukondo=kurema_dosiye((const char*)Inzira,soma_gusa_agaciro,0);if(dosiye_umukondo<0)자바실패();int 개수=dosiye_ingano(dosiye_umukondo);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(dosiye_umukondo,자료위치,개수);gufunga_dosiye(dosiye_umukondo);if(반환값!=개수)자바실패();자료위치[개수]=0;return (imashini_Ijambo)자료위치;}
