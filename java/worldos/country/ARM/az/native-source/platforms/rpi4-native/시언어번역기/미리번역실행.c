#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long maşın_Söz;
static maşın_Söz 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Mətn[]="AOT runtime error\n";yazmaq_fayl_verilənlər(2,Mətn,sizeof(Mətn)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(maşın_Söz *Yığın_Yaddaş,int *깊이,maşın_Söz VALUE){if(*깊이<0||*깊이>=128)자바실패();Yığın_Yaddaş[(*깊이)++]=VALUE;}
maşın_Söz 자바꺼내기(maşın_Söz *Yığın_Yaddaş,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Yığın_Yaddaş[--*깊이];}
maşın_Söz 자바배열(int element_COUNT){if(element_COUNT<0||(unsigned)element_COUNT+1>8192-사용량)자바실패();maşın_Söz*verilənlər_yerinə_qoymaq=동적기억공간+사용량;사용량+=element_COUNT+1;verilənlər_yerinə_qoymaq[0]=element_COUNT;return (maşın_Söz)verilənlər_yerinə_qoymaq;}
maşın_Söz *자바색인(maşın_Söz obyekt_İstinad,int element_COUNT){maşın_Söz*verilənlər_yerinə_qoymaq=(maşın_Söz*)obyekt_İstinad;if(!verilənlər_yerinə_qoymaq||element_COUNT<0||(maşın_Söz)element_COUNT>=verilənlər_yerinə_qoymaq[0])자바실패();return verilənlər_yerinə_qoymaq+element_COUNT+1;}
int 자바길이(maşın_Söz obyekt_İstinad){if(!obyekt_İstinad)자바실패();return *(maşın_Söz*)obyekt_İstinad;}
int 자바나누기(int x_koordinatı,int Y_koordinat,int 나머지){if(!Y_koordinat)자바실패();if(x_koordinatı==(-2147483647-1)&&Y_koordinat==-1)return 나머지?0:x_koordinatı;return 나머지?x_koordinatı%Y_koordinat:x_koordinatı/Y_koordinat;}
static unsigned uzunluq_VALUE(const char*sətir_verilənlər){unsigned element_COUNT=0;if(!sətir_verilənlər)자바실패();while(sətir_verilənlər[element_COUNT])element_COUNT++;return element_COUNT;}
void 자바출력(maşın_Söz verilənlər_yerinə_qoymaq,int 수치,int 줄바꿈){
    if(수치){char SECOND_VALUE[16];unsigned element_COUNT=0;int VALUE=(int)verilənlər_yerinə_qoymaq;unsigned 부호없는값=VALUE<0?0-(unsigned)VALUE:VALUE;do{SECOND_VALUE[element_COUNT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALUE<0)SECOND_VALUE[element_COUNT++]='-';while(element_COUNT)yazmaq_fayl_verilənlər(1,SECOND_VALUE+--element_COUNT,1);}
    else{const char*sətir_verilənlər=verilənlər_yerinə_qoymaq?(const char*)verilənlər_yerinə_qoymaq:"null";yazmaq_fayl_verilənlər(1,sətir_verilənlər,uzunluq_VALUE(sətir_verilənlər));}if(줄바꿈)yazmaq_fayl_verilənlər(1,"\n",1);
}
maşın_Söz 자바파일쓰기(maşın_Söz Cığır,maşın_Söz VALUE){const char*sətir_verilənlər=(const char*)VALUE;unsigned element_COUNT=uzunluq_VALUE(sətir_verilənlər);int fayl_tutacaq=açmaq_fayl((const char*)Cığır,쓰기전용|없으면만들기|내용비우기,0600);if(fayl_tutacaq<0)자바실패();int 반환값=yazmaq_fayl_verilənlər(fayl_tutacaq,sətir_verilənlər,element_COUNT);bağlamaq_fayl(fayl_tutacaq);if(반환값!=(int)element_COUNT)자바실패();return 0;}
maşın_Söz 자바파일읽기(maşın_Söz Cığır){int fayl_tutacaq=açmaq_fayl((const char*)Cığır,yalnız_oxunan_VALUE,0);if(fayl_tutacaq<0)자바실패();int element_COUNT=fayl_ölçünü_dəyişmək(fayl_tutacaq);if(element_COUNT<0||element_COUNT>16384||(unsigned)(element_COUNT+8)/8>8192-사용량)자바실패();char*verilənlər_yerinə_qoymaq=(char*)(동적기억공간+사용량);사용량+=(element_COUNT+8)/8;int 반환값=파일자료읽기(fayl_tutacaq,verilənlər_yerinə_qoymaq,element_COUNT);bağlamaq_fayl(fayl_tutacaq);if(반환값!=element_COUNT)자바실패();verilənlər_yerinə_qoymaq[element_COUNT]=0;return (maşın_Söz)verilənlər_yerinə_qoymaq;}
