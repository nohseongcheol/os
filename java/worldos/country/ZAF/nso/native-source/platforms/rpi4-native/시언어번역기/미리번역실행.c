#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long motšhene_Thalokontšu;
static motšhene_Thalokontšu 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Sengwalwa[]="AOT runtime error\n";ngwala_faele_data(2,Sengwalwa,sizeof(Sengwalwa)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(motšhene_Thalokontšu *kgoboko_Bobolokelo,int *깊이,motšhene_Thalokontšu boleng){if(*깊이<0||*깊이>=128)자바실패();kgoboko_Bobolokelo[(*깊이)++]=boleng;}
motšhene_Thalokontšu 자바꺼내기(motšhene_Thalokontšu *kgoboko_Bobolokelo,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return kgoboko_Bobolokelo[--*깊이];}
motšhene_Thalokontšu 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();motšhene_Thalokontšu*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (motšhene_Thalokontšu)자료위치;}
motšhene_Thalokontšu *자바색인(motšhene_Thalokontšu selo_Dipadišo,int 개수){motšhene_Thalokontšu*자료위치=(motšhene_Thalokontšu*)selo_Dipadišo;if(!자료위치||개수<0||(motšhene_Thalokontšu)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(motšhene_Thalokontšu selo_Dipadišo){if(!selo_Dipadišo)자바실패();return *(motšhene_Thalokontšu*)selo_Dipadišo;}
int 자바나누기(int kamano_ya_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(kamano_ya_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:kamano_ya_x;return 나머지?kamano_ya_x%세로좌표:kamano_ya_x/세로좌표;}
static unsigned botelele_boleng(const char*molokoloko_data){unsigned 개수=0;if(!molokoloko_data)자바실패();while(molokoloko_data[개수])개수++;return 개수;}
void 자바출력(motšhene_Thalokontšu 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int boleng=(int)자료위치;unsigned 부호없는값=boleng<0?0-(unsigned)boleng:boleng;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(boleng<0)둘째값[개수++]='-';while(개수)ngwala_faele_data(1,둘째값+--개수,1);}
    else{const char*molokoloko_data=자료위치?(const char*)자료위치:"null";ngwala_faele_data(1,molokoloko_data,botelele_boleng(molokoloko_data));}if(줄바꿈)ngwala_faele_data(1,"\n",1);
}
motšhene_Thalokontšu 자바파일쓰기(motšhene_Thalokontšu Tsejana,motšhene_Thalokontšu boleng){const char*molokoloko_data=(const char*)boleng;unsigned 개수=botelele_boleng(molokoloko_data);int faele_tshwaro=bula_faele((const char*)Tsejana,쓰기전용|없으면만들기|내용비우기,0600);if(faele_tshwaro<0)자바실패();int 반환값=ngwala_faele_data(faele_tshwaro,molokoloko_data,개수);tswalela_faele(faele_tshwaro);if(반환값!=(int)개수)자바실패();return 0;}
motšhene_Thalokontšu 자바파일읽기(motšhene_Thalokontšu Tsejana){int faele_tshwaro=bula_faele((const char*)Tsejana,balwago_fela_boleng,0);if(faele_tshwaro<0)자바실패();int 개수=faele_bogolo(faele_tshwaro);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(faele_tshwaro,자료위치,개수);tswalela_faele(faele_tshwaro);if(반환값!=개수)자바실패();자료위치[개수]=0;return (motšhene_Thalokontšu)자료위치;}
