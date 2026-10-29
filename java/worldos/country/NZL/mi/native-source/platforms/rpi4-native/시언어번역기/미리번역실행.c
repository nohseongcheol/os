#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long mīhini_Word;
static mīhini_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Ngā_kupu[]="AOT runtime error\n";tuhi_kōnae_raraunga(2,Ngā_kupu,sizeof(Ngā_kupu)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(mīhini_Word *Huinga_Rokiroki,int *깊이,mīhini_Word uara){if(*깊이<0||*깊이>=128)자바실패();Huinga_Rokiroki[(*깊이)++]=uara;}
mīhini_Word 자바꺼내기(mīhini_Word *Huinga_Rokiroki,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Huinga_Rokiroki[--*깊이];}
mīhini_Word 자바배열(int tuemi_COUNT){if(tuemi_COUNT<0||(unsigned)tuemi_COUNT+1>8192-사용량)자바실패();mīhini_Word*raraunga_tūranga=동적기억공간+사용량;사용량+=tuemi_COUNT+1;raraunga_tūranga[0]=tuemi_COUNT;return (mīhini_Word)raraunga_tūranga;}
mīhini_Word *자바색인(mīhini_Word ahanoa_Pūranga_kōrero,int tuemi_COUNT){mīhini_Word*raraunga_tūranga=(mīhini_Word*)ahanoa_Pūranga_kōrero;if(!raraunga_tūranga||tuemi_COUNT<0||(mīhini_Word)tuemi_COUNT>=raraunga_tūranga[0])자바실패();return raraunga_tūranga+tuemi_COUNT+1;}
int 자바길이(mīhini_Word ahanoa_Pūranga_kōrero){if(!ahanoa_Pūranga_kōrero)자바실패();return *(mīhini_Word*)ahanoa_Pūranga_kōrero;}
int 자바나누기(int taunga_x,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(taunga_x==(-2147483647-1)&&세로좌표==-1)return 나머지?0:taunga_x;return 나머지?taunga_x%세로좌표:taunga_x/세로좌표;}
static unsigned roa_uara(const char*aho_raraunga){unsigned tuemi_COUNT=0;if(!aho_raraunga)자바실패();while(aho_raraunga[tuemi_COUNT])tuemi_COUNT++;return tuemi_COUNT;}
void 자바출력(mīhini_Word raraunga_tūranga,int 수치,int 줄바꿈){
    if(수치){char SECOND_uara[16];unsigned tuemi_COUNT=0;int uara=(int)raraunga_tūranga;unsigned 부호없는값=uara<0?0-(unsigned)uara:uara;do{SECOND_uara[tuemi_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(uara<0)SECOND_uara[tuemi_COUNT++]='-';while(tuemi_COUNT)tuhi_kōnae_raraunga(1,SECOND_uara+--tuemi_COUNT,1);}
    else{const char*aho_raraunga=raraunga_tūranga?(const char*)raraunga_tūranga:"null";tuhi_kōnae_raraunga(1,aho_raraunga,roa_uara(aho_raraunga));}if(줄바꿈)tuhi_kōnae_raraunga(1,"\n",1);
}
mīhini_Word 자바파일쓰기(mīhini_Word ara,mīhini_Word uara){const char*aho_raraunga=(const char*)uara;unsigned tuemi_COUNT=roa_uara(aho_raraunga);int kōnae_raweke=tiwhikete_kōnae((const char*)ara,쓰기전용|없으면만들기|내용비우기,0600);if(kōnae_raweke<0)자바실패();int 반환값=tuhi_kōnae_raraunga(kōnae_raweke,aho_raraunga,tuemi_COUNT);kati_kōnae(kōnae_raweke);if(반환값!=(int)tuemi_COUNT)자바실패();return 0;}
mīhini_Word 자바파일읽기(mīhini_Word ara){int kōnae_raweke=tiwhikete_kōnae((const char*)ara,pānui_anake_uara,0);if(kōnae_raweke<0)자바실패();int tuemi_COUNT=kōnae_rahi(kōnae_raweke);if(tuemi_COUNT<0||tuemi_COUNT>16384||(unsigned)(tuemi_COUNT+8)/8>8192-사용량)자바실패();char*raraunga_tūranga=(char*)(동적기억공간+사용량);사용량+=(tuemi_COUNT+8)/8;int 반환값=파일자료읽기(kōnae_raweke,raraunga_tūranga,tuemi_COUNT);kati_kōnae(kōnae_raweke);if(반환값!=tuemi_COUNT)자바실패();raraunga_tūranga[tuemi_COUNT]=0;return (mīhini_Word)raraunga_tūranga;}
