#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long maskine_Ord;
static maskine_Ord heap_Lager[8192];static unsigned 사용량;
void 자바실패(void){const char Tekst[]="AOT runtime error\n";skrive_fil_data(2,Tekst,sizeof(Tekst)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(maskine_Ord *Stak_Lager,int *깊이,maskine_Ord VÆRDI){if(*깊이<0||*깊이>=128)자바실패();Stak_Lager[(*깊이)++]=VÆRDI;}
maskine_Ord 자바꺼내기(maskine_Ord *Stak_Lager,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Stak_Lager[--*깊이];}
maskine_Ord 자바배열(int vare_TÆL){if(vare_TÆL<0||(unsigned)vare_TÆL+1>8192-사용량)자바실패();maskine_Ord*data_placere=heap_Lager+사용량;사용량+=vare_TÆL+1;data_placere[0]=vare_TÆL;return (maskine_Ord)data_placere;}
maskine_Ord *자바색인(maskine_Ord objekt_referere,int vare_TÆL){maskine_Ord*data_placere=(maskine_Ord*)objekt_referere;if(!data_placere||vare_TÆL<0||(maskine_Ord)vare_TÆL>=data_placere[0])자바실패();return data_placere+vare_TÆL+1;}
int 자바길이(maskine_Ord objekt_referere){if(!objekt_referere)자바실패();return *(maskine_Ord*)objekt_referere;}
int 자바나누기(int X_koordinat,int Y_koordinat,int 나머지){if(!Y_koordinat)자바실패();if(X_koordinat==(-2147483647-1)&&Y_koordinat==-1)return 나머지?0:X_koordinat;return 나머지?X_koordinat%Y_koordinat:X_koordinat/Y_koordinat;}
static unsigned varighed_VÆRDI(const char*streng_data){unsigned vare_TÆL=0;if(!streng_data)자바실패();while(streng_data[vare_TÆL])vare_TÆL++;return vare_TÆL;}
void 자바출력(maskine_Ord data_placere,int 수치,int 줄바꿈){
    if(수치){char SEKUND_VÆRDI[16];unsigned vare_TÆL=0;int VÆRDI=(int)data_placere;unsigned 부호없는값=VÆRDI<0?0-(unsigned)VÆRDI:VÆRDI;do{SEKUND_VÆRDI[vare_TÆL++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VÆRDI<0)SEKUND_VÆRDI[vare_TÆL++]='-';while(vare_TÆL)skrive_fil_data(1,SEKUND_VÆRDI+--vare_TÆL,1);}
    else{const char*streng_data=data_placere?(const char*)data_placere:"null";skrive_fil_data(1,streng_data,varighed_VÆRDI(streng_data));}if(줄바꿈)skrive_fil_data(1,"\n",1);
}
maskine_Ord 자바파일쓰기(maskine_Ord Sti,maskine_Ord VÆRDI){const char*streng_data=(const char*)VÆRDI;unsigned vare_TÆL=varighed_VÆRDI(streng_data);int fil_handle=åben_fil((const char*)Sti,쓰기전용|없으면만들기|afkorte_Indhold,0600);if(fil_handle<0)자바실패();int 반환값=skrive_fil_data(fil_handle,streng_data,vare_TÆL);Luk_fil(fil_handle);if(반환값!=(int)vare_TÆL)자바실패();return 0;}
maskine_Ord 자바파일읽기(maskine_Ord Sti){int fil_handle=åben_fil((const char*)Sti,skrivebeskyttet_VÆRDI,0);if(fil_handle<0)자바실패();int vare_TÆL=filstørrelse(fil_handle);if(vare_TÆL<0||vare_TÆL>16384||(unsigned)(vare_TÆL+8)/8>8192-사용량)자바실패();char*data_placere=(char*)(heap_Lager+사용량);사용량+=(vare_TÆL+8)/8;int 반환값=파일자료읽기(fil_handle,data_placere,vare_TÆL);Luk_fil(fil_handle);if(반환값!=vare_TÆL)자바실패();data_placere[vare_TÆL]=0;return (maskine_Ord)data_placere;}
