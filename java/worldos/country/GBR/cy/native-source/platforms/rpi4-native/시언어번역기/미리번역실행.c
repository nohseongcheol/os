#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long peiriant_Word;
static peiriant_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Testun[]="AOT runtime error\n";ysgrifennu_ffeil_data(2,Testun,sizeof(Testun)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(peiriant_Word *pentwr_Storio,int *깊이,peiriant_Word VALUE){if(*깊이<0||*깊이>=128)자바실패();pentwr_Storio[(*깊이)++]=VALUE;}
peiriant_Word 자바꺼내기(peiriant_Word *pentwr_Storio,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return pentwr_Storio[--*깊이];}
peiriant_Word 자바배열(int eitem_COUNT){if(eitem_COUNT<0||(unsigned)eitem_COUNT+1>8192-사용량)자바실패();peiriant_Word*data_safle=동적기억공간+사용량;사용량+=eitem_COUNT+1;data_safle[0]=eitem_COUNT;return (peiriant_Word)data_safle;}
peiriant_Word *자바색인(peiriant_Word gwrthrych_cyfeiriad,int eitem_COUNT){peiriant_Word*data_safle=(peiriant_Word*)gwrthrych_cyfeiriad;if(!data_safle||eitem_COUNT<0||(peiriant_Word)eitem_COUNT>=data_safle[0])자바실패();return data_safle+eitem_COUNT+1;}
int 자바길이(peiriant_Word gwrthrych_cyfeiriad){if(!gwrthrych_cyfeiriad)자바실패();return *(peiriant_Word*)gwrthrych_cyfeiriad;}
int 자바나누기(int cyfesuryn_x,int Y_cyfesuryn,int 나머지){if(!Y_cyfesuryn)자바실패();if(cyfesuryn_x==(-2147483647-1)&&Y_cyfesuryn==-1)return 나머지?0:cyfesuryn_x;return 나머지?cyfesuryn_x%Y_cyfesuryn:cyfesuryn_x/Y_cyfesuryn;}
static unsigned hyd_VALUE(const char*testun_data){unsigned eitem_COUNT=0;if(!testun_data)자바실패();while(testun_data[eitem_COUNT])eitem_COUNT++;return eitem_COUNT;}
void 자바출력(peiriant_Word data_safle,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned eitem_COUNT=0;int VALUE=(int)data_safle;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[eitem_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[eitem_COUNT++]='-';while(eitem_COUNT)ysgrifennu_ffeil_data(1,SECOND_VALUE+--eitem_COUNT,1);}
    else{const char*testun_data=data_safle?(const char*)data_safle:"null";ysgrifennu_ffeil_data(1,testun_data,hyd_VALUE(testun_data));}if(줄바꿈)ysgrifennu_ffeil_data(1,"\n",1);
}
peiriant_Word 자바파일쓰기(peiriant_Word LLWYBR,peiriant_Word VALUE){const char*testun_data=(const char*)VALUE;unsigned eitem_COUNT=hyd_VALUE(testun_data);int ffeil_dolen=agor_ffeil((const char*)LLWYBR,쓰기전용|없으면만들기|내용비우기,0600);if(ffeil_dolen<0)자바실패();int 반환값=ysgrifennu_ffeil_data(ffeil_dolen,testun_data,eitem_COUNT);cau_ffeil(ffeil_dolen);if(반환값!=(int)eitem_COUNT)자바실패();return 0;}
peiriant_Word 자바파일읽기(peiriant_Word LLWYBR){int ffeil_dolen=agor_ffeil((const char*)LLWYBR,darllen_yn_unig_VALUE,0);if(ffeil_dolen<0)자바실패();int eitem_COUNT=ffeil_newid_maint(ffeil_dolen);if(eitem_COUNT<0||eitem_COUNT>16384||(unsigned)(eitem_COUNT+8)/8>8192-사용량)자바실패();char*data_safle=(char*)(동적기억공간+사용량);사용량+=(eitem_COUNT+8)/8;int 반환값=파일자료읽기(ffeil_dolen,data_safle,eitem_COUNT);cau_ffeil(ffeil_dolen);if(반환값!=eitem_COUNT)자바실패();data_safle[eitem_COUNT]=0;return (peiriant_Word)data_safle;}
