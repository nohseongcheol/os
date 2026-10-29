#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long ngwa_komputa_Mkpụrụokwu;
static ngwa_komputa_Mkpụrụokwu 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";dee_ọbọakwụkwọ_datà(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(ngwa_komputa_Mkpụrụokwu *ikpo_Nchekwa,int *깊이,ngwa_komputa_Mkpụrụokwu valuu){if(*깊이<0||*깊이>=128)자바실패();ikpo_Nchekwa[(*깊이)++]=valuu;}
ngwa_komputa_Mkpụrụokwu 자바꺼내기(ngwa_komputa_Mkpụrụokwu *ikpo_Nchekwa,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return ikpo_Nchekwa[--*깊이];}
ngwa_komputa_Mkpụrụokwu 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();ngwa_komputa_Mkpụrụokwu*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (ngwa_komputa_Mkpụrụokwu)자료위치;}
ngwa_komputa_Mkpụrụokwu *자바색인(ngwa_komputa_Mkpụrụokwu ihe_Nrụtụ_aka,int 개수){ngwa_komputa_Mkpụrụokwu*자료위치=(ngwa_komputa_Mkpụrụokwu*)ihe_Nrụtụ_aka;if(!자료위치||개수<0||(ngwa_komputa_Mkpụrụokwu)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(ngwa_komputa_Mkpụrụokwu ihe_Nrụtụ_aka){if(!ihe_Nrụtụ_aka)자바실패();return *(ngwa_komputa_Mkpụrụokwu*)ihe_Nrụtụ_aka;}
int 자바나누기(int ngakọrịta_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(ngakọrịta_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:ngakọrịta_x;return 나머지?ngakọrịta_x%세로좌표:ngakọrịta_x/세로좌표;}
static unsigned ogologo_valuu(const char*ùsòròokwū_datà){unsigned 개수=0;if(!ùsòròokwū_datà)자바실패();while(ùsòròokwū_datà[개수])개수++;return 개수;}
void 자바출력(ngwa_komputa_Mkpụrụokwu 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int valuu=(int)자료위치;unsigned 부호없는값=valuu<0?0-(unsigned)valuu:valuu;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(valuu<0)둘째값[개수++]='-';while(개수)dee_ọbọakwụkwọ_datà(1,둘째값+--개수,1);}
    else{const char*ùsòròokwū_datà=자료위치?(const char*)자료위치:"null";dee_ọbọakwụkwọ_datà(1,ùsòròokwū_datà,ogologo_valuu(ùsòròokwū_datà));}if(줄바꿈)dee_ọbọakwụkwọ_datà(1,"\n",1);
}
ngwa_komputa_Mkpụrụokwu 자바파일쓰기(ngwa_komputa_Mkpụrụokwu ụzọ_ozi,ngwa_komputa_Mkpụrụokwu valuu){const char*ùsòròokwū_datà=(const char*)valuu;unsigned 개수=ogologo_valuu(ùsòròokwū_datà);int ọbọakwụkwọ_ebenjìaka=mepee_ọbọakwụkwọ((const char*)ụzọ_ozi,쓰기전용|없으면만들기|내용비우기,0600);if(ọbọakwụkwọ_ebenjìaka<0)자바실패();int 반환값=dee_ọbọakwụkwọ_datà(ọbọakwụkwọ_ebenjìaka,ùsòròokwū_datà,개수);mmechi_ọbọakwụkwọ(ọbọakwụkwọ_ebenjìaka);if(반환값!=(int)개수)자바실패();return 0;}
ngwa_komputa_Mkpụrụokwu 자바파일읽기(ngwa_komputa_Mkpụrụokwu ụzọ_ozi){int ọbọakwụkwọ_ebenjìaka=mepee_ọbọakwụkwọ((const char*)ụzọ_ozi,ọgụgụ_naanị_valuu,0);if(ọbọakwụkwọ_ebenjìaka<0)자바실패();int 개수=ọbọakwụkwọ_ụha(ọbọakwụkwọ_ebenjìaka);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(ọbọakwụkwọ_ebenjìaka,자료위치,개수);mmechi_ọbọakwụkwọ(ọbọakwụkwọ_ebenjìaka);if(반환값!=개수)자바실패();자료위치[개수]=0;return (ngwa_komputa_Mkpụrụokwu)자료위치;}
