#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long motšhine_Lefoko;
static motšhine_Lefoko 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";kwala_faele_tshedimosetso(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(motšhine_Lefoko *kokoanyodinepe_Polokelo,int *깊이,motšhine_Lefoko Boleng){if(*깊이<0||*깊이>=128)자바실패();kokoanyodinepe_Polokelo[(*깊이)++]=Boleng;}
motšhine_Lefoko 자바꺼내기(motšhine_Lefoko *kokoanyodinepe_Polokelo,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return kokoanyodinepe_Polokelo[--*깊이];}
motšhine_Lefoko 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();motšhine_Lefoko*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (motšhine_Lefoko)자료위치;}
motšhine_Lefoko *자바색인(motšhine_Lefoko selwana_Tshupiso,int 개수){motšhine_Lefoko*자료위치=(motšhine_Lefoko*)selwana_Tshupiso;if(!자료위치||개수<0||(motšhine_Lefoko)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(motšhine_Lefoko selwana_Tshupiso){if(!selwana_Tshupiso)자바실패();return *(motšhine_Lefoko*)selwana_Tshupiso;}
int 자바나누기(int kgokagano_ya_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(kgokagano_ya_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:kgokagano_ya_x;return 나머지?kgokagano_ya_x%세로좌표:kgokagano_ya_x/세로좌표;}
static unsigned boleele_Boleng(const char*dikwalwa_tshedimosetso){unsigned 개수=0;if(!dikwalwa_tshedimosetso)자바실패();while(dikwalwa_tshedimosetso[개수])개수++;return 개수;}
void 자바출력(motšhine_Lefoko 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int Boleng=(int)자료위치;unsigned 부호없는값=Boleng<0?0-(unsigned)Boleng:Boleng;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(Boleng<0)둘째값[개수++]='-';while(개수)kwala_faele_tshedimosetso(1,둘째값+--개수,1);}
    else{const char*dikwalwa_tshedimosetso=자료위치?(const char*)자료위치:"null";kwala_faele_tshedimosetso(1,dikwalwa_tshedimosetso,boleele_Boleng(dikwalwa_tshedimosetso));}if(줄바꿈)kwala_faele_tshedimosetso(1,"\n",1);
}
motšhine_Lefoko 자바파일쓰기(motšhine_Lefoko tsela,motšhine_Lefoko Boleng){const char*dikwalwa_tshedimosetso=(const char*)Boleng;unsigned 개수=boleele_Boleng(dikwalwa_tshedimosetso);int faele_mokgwakamogelo=bula_faele((const char*)tsela,쓰기전용|없으면만들기|내용비우기,0600);if(faele_mokgwakamogelo<0)자바실패();int 반환값=kwala_faele_tshedimosetso(faele_mokgwakamogelo,dikwalwa_tshedimosetso,개수);tswala_faele(faele_mokgwakamogelo);if(반환값!=(int)개수)자바실패();return 0;}
motšhine_Lefoko 자바파일읽기(motšhine_Lefoko tsela){int faele_mokgwakamogelo=bula_faele((const char*)tsela,puiso_fela_Boleng,0);if(faele_mokgwakamogelo<0)자바실패();int 개수=faele_lekanya(faele_mokgwakamogelo);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(faele_mokgwakamogelo,자료위치,개수);tswala_faele(faele_mokgwakamogelo);if(반환값!=개수)자바실패();자료위치[개수]=0;return (motšhine_Lefoko)자료위치;}
