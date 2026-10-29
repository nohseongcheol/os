#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long masin_Word;
static masin_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Tekst[]="AOT runtime error\n";biir_bara_denc_mbir(2,Tekst,sizeof(Tekst)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(masin_Word *Tegalo_Dencukaay,int *깊이,masin_Word xëyma){if(*깊이<0||*깊이>=128)자바실패();Tegalo_Dencukaay[(*깊이)++]=xëyma;}
masin_Word 자바꺼내기(masin_Word *Tegalo_Dencukaay,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Tegalo_Dencukaay[--*깊이];}
masin_Word 자바배열(int 개수){if(개수<0||(unsigned)개수+1>8192-사용량)자바실패();masin_Word*자료위치=동적기억공간+사용량;사용량+=개수+1;자료위치[0]=개수;return (masin_Word)자료위치;}
masin_Word *자바색인(masin_Word yëf_Royukaay,int 개수){masin_Word*자료위치=(masin_Word*)yëf_Royukaay;if(!자료위치||개수<0||(masin_Word)개수>=자료위치[0])자바실패();return 자료위치+개수+1;}
int 자바길이(masin_Word yëf_Royukaay){if(!yëf_Royukaay)자바실패();return *(masin_Word*)yëf_Royukaay;}
int 자바나누기(int rëddu_iks_yi,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(rëddu_iks_yi==(-2147483647-1)&&세로좌표==-1)return 나머지?0:rëddu_iks_yi;return 나머지?rëddu_iks_yi%세로좌표:rëddu_iks_yi/세로좌표;}
static unsigned diir_xëyma(const char*araf_yu_bennoo_mbir){unsigned 개수=0;if(!araf_yu_bennoo_mbir)자바실패();while(araf_yu_bennoo_mbir[개수])개수++;return 개수;}
void 자바출력(masin_Word 자료위치,int 수치,int 줄바꿈){
    if(수치){char 둘째값[16];unsigned 개수=0;int xëyma=(int)자료위치;unsigned 부호없는값=xëyma<0?0-(unsigned)xëyma:xëyma;do{둘째값[개수++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(xëyma<0)둘째값[개수++]='-';while(개수)biir_bara_denc_mbir(1,둘째값+--개수,1);}
    else{const char*araf_yu_bennoo_mbir=자료위치?(const char*)자료위치:"null";biir_bara_denc_mbir(1,araf_yu_bennoo_mbir,diir_xëyma(araf_yu_bennoo_mbir));}if(줄바꿈)biir_bara_denc_mbir(1,"\n",1);
}
masin_Word 자바파일쓰기(masin_Word Yoonu_jëmale,masin_Word xëyma){const char*araf_yu_bennoo_mbir=(const char*)xëyma;unsigned 개수=diir_xëyma(araf_yu_bennoo_mbir);int bara_denc_yombal=sos_bara_denc((const char*)Yoonu_jëmale,쓰기전용|없으면만들기|내용비우기,0600);if(bara_denc_yombal<0)자바실패();int 반환값=biir_bara_denc_mbir(bara_denc_yombal,araf_yu_bennoo_mbir,개수);Tej_bara_denc(bara_denc_yombal);if(반환값!=(int)개수)자바실패();return 0;}
masin_Word 자바파일읽기(masin_Word Yoonu_jëmale){int bara_denc_yombal=sos_bara_denc((const char*)Yoonu_jëmale,ngir_jaŋarek_la_xëyma,0);if(bara_denc_yombal<0)자바실패();int 개수=bara_denc_tolluwaay(bara_denc_yombal);if(개수<0||개수>16384||(unsigned)(개수+8)/8>8192-사용량)자바실패();char*자료위치=(char*)(동적기억공간+사용량);사용량+=(개수+8)/8;int 반환값=파일자료읽기(bara_denc_yombal,자료위치,개수);Tej_bara_denc(bara_denc_yombal);if(반환값!=개수)자바실패();자료위치[개수]=0;return (masin_Word)자료위치;}
