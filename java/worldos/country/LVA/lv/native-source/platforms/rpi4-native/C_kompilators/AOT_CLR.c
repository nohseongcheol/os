#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long mašīna_Word;
static mašīna_Word kaudze_Krātuve[8192];static unsigned 사용량;
void 자바실패(void){const char Teksts[]="AOT runtime error\n";rakstīšana_Fails_dati(2,Teksts,sizeof(Teksts)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(mašīna_Word *kopa_Krātuve,int *깊이,mašīna_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();kopa_Krātuve[(*깊이)++]=VALUE;}
mašīna_Word 자바꺼내기(mašīna_Word *kopa_Krātuve,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return kopa_Krātuve[--*깊이];}
mašīna_Word 자바배열(int krājums_COUNT){if(krājums_COUNT<0||(unsigned)krājums_COUNT+1>8192-사용량)자바실패();mašīna_Word*dati_amats=kaudze_Krātuve+사용량;사용량+=krājums_COUNT+1;dati_amats[0]=krājums_COUNT;return (mašīna_Word)dati_amats;}
mašīna_Word *자바색인(mašīna_Word objekts_Uzziņas,int krājums_COUNT){mašīna_Word*dati_amats=(mašīna_Word*)objekts_Uzziņas;if(!dati_amats||krājums_COUNT<0||(mašīna_Word)krājums_COUNT>=dati_amats[0])자바실패();return dati_amats+krājums_COUNT+1;}
int 자바길이(mašīna_Word objekts_Uzziņas){if(!objekts_Uzziņas)자바실패();return *(mašīna_Word*)objekts_Uzziņas;}
int 자바나누기(int x_koordināta,int 세로좌표,int 나머지){if(!세로좌표)자바실패();if(x_koordināta==(-2147483647-1)&&세로좌표==-1)return 나머지?0:x_koordināta;return 나머지?x_koordināta%세로좌표:x_koordināta/세로좌표;}
static unsigned 길이(const char*virkne_dati){unsigned krājums_COUNT=0;if(!virkne_dati)자바실패();while(virkne_dati[krājums_COUNT])krājums_COUNT++;return krājums_COUNT;}
void 자바출력(mašīna_Word dati_amats,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned krājums_COUNT=0;int VALUE=(int)dati_amats;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[krājums_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[krājums_COUNT++]='-';while(krājums_COUNT)rakstīšana_Fails_dati(1,SECOND_VALUE+--krājums_COUNT,1);}
    else{const char*virkne_dati=dati_amats?(const char*)dati_amats:"null";rakstīšana_Fails_dati(1,virkne_dati,길이(virkne_dati));}if(줄바꿈)rakstīšana_Fails_dati(1,"\n",1);
}
mašīna_Word 자바파일쓰기(mašīna_Word CEĻŠ,mašīna_Word VALUE){const char*virkne_dati=(const char*)VALUE;unsigned krājums_COUNT=길이(virkne_dati);int Fails_turis=atvērt_Fails((const char*)CEĻŠ,쓰기전용|없으면만들기|apraut_Satura_rādītājs,0600);if(Fails_turis<0)자바실패();int 반환값=rakstīšana_Fails_dati(Fails_turis,virkne_dati,krājums_COUNT);Aizvērt_Fails(Fails_turis);if(반환값!=(int)krājums_COUNT)자바실패();return 0;}
mašīna_Word 자바파일읽기(mašīna_Word CEĻŠ){int Fails_turis=atvērt_Fails((const char*)CEĻŠ,tikai_lasāms_VALUE,0);if(Fails_turis<0)자바실패();int krājums_COUNT=faila_lielums(Fails_turis);if(krājums_COUNT<0||krājums_COUNT>16384||(unsigned)(krājums_COUNT+8)/8>8192-사용량)자바실패();char*dati_amats=(char*)(kaudze_Krātuve+사용량);사용량+=(krājums_COUNT+8)/8;int 반환값=파일자료읽기(Fails_turis,dati_amats,krājums_COUNT);Aizvērt_Fails(Fails_turis);if(반환값!=krājums_COUNT)자바실패();dati_amats[krājums_COUNT]=0;return (mašīna_Word)dati_amats;}
