#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long inneal_Word;
static inneal_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";sgrìobh_faidhle_dàta(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(inneal_Word *stac_stòras,int *깊이,inneal_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();stac_stòras[(*깊이)++]=VALUE;}
inneal_Word 자바꺼내기(inneal_Word *stac_stòras,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return stac_stòras[--*깊이];}
inneal_Word 자바배열(int nì_COUNT){if(nì_COUNT<0||(unsigned)nì_COUNT+1>8192-사용량)자바실패();inneal_Word*dàta_suidhich=동적기억공간+사용량;사용량+=nì_COUNT+1;dàta_suidhich[0]=nì_COUNT;return (inneal_Word)dàta_suidhich;}
inneal_Word *자바색인(inneal_Word nì_fiosrachadh,int nì_COUNT){inneal_Word*dàta_suidhich=(inneal_Word*)nì_fiosrachadh;if(!dàta_suidhich||nì_COUNT<0||(inneal_Word)nì_COUNT>=dàta_suidhich[0])자바실패();return dàta_suidhich+nì_COUNT+1;}
int 자바길이(inneal_Word nì_fiosrachadh){if(!nì_fiosrachadh)자바실패();return *(inneal_Word*)nì_fiosrachadh;}
int 자바나누기(int co_chomharra_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(co_chomharra_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:co_chomharra_x;return 나머지?co_chomharra_x%세로좌표:co_chomharra_x/세로좌표;}
static unsigned faid_VALUE(const char*sreang_dàta){unsigned nì_COUNT=0;if(!sreang_dàta)자바실패();while(sreang_dàta[nì_COUNT])nì_COUNT++;return nì_COUNT;}
void 자바출력(inneal_Word dàta_suidhich,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned nì_COUNT=0;int VALUE=(int)dàta_suidhich;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[nì_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[nì_COUNT++]='-';while(nì_COUNT)sgrìobh_faidhle_dàta(1,SECOND_VALUE+--nì_COUNT,1);}
    else{const char*sreang_dàta=dàta_suidhich?(const char*)dàta_suidhich:"null";sgrìobh_faidhle_dàta(1,sreang_dàta,faid_VALUE(sreang_dàta));}if(줄바꿈)sgrìobh_faidhle_dàta(1,"\n",1);
}
inneal_Word 자바파일쓰기(inneal_Word Slighe,inneal_Word VALUE){const char*sreang_dàta=(const char*)VALUE;unsigned nì_COUNT=faid_VALUE(sreang_dàta);int faidhle_làmhrachan=fosgail_faidhle((const char*)Slighe,쓰기전용|없으면만들기|내용비우기,0600);if(faidhle_làmhrachan<0)자바실패();int 반환값=sgrìobh_faidhle_dàta(faidhle_làmhrachan,sreang_dàta,nì_COUNT);dùin_faidhle(faidhle_làmhrachan);if(반환값!=(int)nì_COUNT)자바실패();return 0;}
inneal_Word 자바파일읽기(inneal_Word Slighe){int faidhle_làmhrachan=fosgail_faidhle((const char*)Slighe,ri_leughadh_a_mhàin_VALUE,0);if(faidhle_làmhrachan<0)자바실패();int nì_COUNT=faidhle_atharraich_am_meud(faidhle_làmhrachan);if(nì_COUNT<0||nì_COUNT>16384||(unsigned)(nì_COUNT+8)/8>8192-사용량)자바실패();char*dàta_suidhich=(char*)(동적기억공간+사용량);사용량+=(nì_COUNT+8)/8;int 반환값=파일자료읽기(faidhle_làmhrachan,dàta_suidhich,nì_COUNT);dùin_faidhle(faidhle_làmhrachan);if(반환값!=nì_COUNT)자바실패();dàta_suidhich[nì_COUNT]=0;return (inneal_Word)dàta_suidhich;}
