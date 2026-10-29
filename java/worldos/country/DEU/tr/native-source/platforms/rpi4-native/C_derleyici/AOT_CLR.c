#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "Dosya_ABI.h"
typedef unsigned long makine_Word;
static makine_Word dinamik_bellek[8192];static unsigned 사용량;
void 자바실패(void){const char metin[]="AOT runtime error\n";yazma_Dosya_veri(2,metin,sizeof(metin)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(makine_Word *yığın_belleği,int *깊이,makine_Word değer){if(*깊이<0||*깊이>=128)자바실패();yığın_belleği[(*깊이)++]=değer;}
makine_Word 자바꺼내기(makine_Word *yığın_belleği,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return yığın_belleği[--*깊이];}
makine_Word 자바배열(int öğe_BAĞ_DEĞ_SAY){if(öğe_BAĞ_DEĞ_SAY<0||(unsigned)öğe_BAĞ_DEĞ_SAY+1>8192-사용량)자바실패();makine_Word*veri_konum=dinamik_bellek+사용량;사용량+=öğe_BAĞ_DEĞ_SAY+1;veri_konum[0]=öğe_BAĞ_DEĞ_SAY;return (makine_Word)veri_konum;}
makine_Word *자바색인(makine_Word nesne_Başvuru,int öğe_BAĞ_DEĞ_SAY){makine_Word*veri_konum=(makine_Word*)nesne_Başvuru;if(!veri_konum||öğe_BAĞ_DEĞ_SAY<0||(makine_Word)öğe_BAĞ_DEĞ_SAY>=veri_konum[0])자바실패();return veri_konum+öğe_BAĞ_DEĞ_SAY+1;}
int 자바길이(makine_Word nesne_Başvuru){if(!nesne_Başvuru)자바실패();return *(makine_Word*)nesne_Başvuru;}
int 자바나누기(int x_koordinatı,int Y_koordinat,int 나머지){if(!Y_koordinat)자바실패();if(x_koordinatı==(-2147483647-1)&&Y_koordinat==-1)return 나머지?0:x_koordinatı;return 나머지?x_koordinatı%Y_koordinat:x_koordinatı/Y_koordinat;}
static unsigned süre_değer(const char*dize_veri){unsigned öğe_BAĞ_DEĞ_SAY=0;if(!dize_veri)자바실패();while(dize_veri[öğe_BAĞ_DEĞ_SAY])öğe_BAĞ_DEĞ_SAY++;return öğe_BAĞ_DEĞ_SAY;}
void 자바출력(makine_Word veri_konum,int 수치,int 줄바꿈){
    if(수치){char SANİYE_değer[16];unsigned öğe_BAĞ_DEĞ_SAY=0;int değer=(int)veri_konum;unsigned 부호없는값=değer<0?0-(unsigned)değer:değer;do{SANİYE_değer[öğe_BAĞ_DEĞ_SAY++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(değer<0)SANİYE_değer[öğe_BAĞ_DEĞ_SAY++]='-';while(öğe_BAĞ_DEĞ_SAY)yazma_Dosya_veri(1,SANİYE_değer+--öğe_BAĞ_DEĞ_SAY,1);}
    else{const char*dize_veri=veri_konum?(const char*)veri_konum:"null";yazma_Dosya_veri(1,dize_veri,süre_değer(dize_veri));}if(줄바꿈)yazma_Dosya_veri(1,"\n",1);
}
makine_Word 자바파일쓰기(makine_Word yol,makine_Word değer){const char*dize_veri=(const char*)değer;unsigned öğe_BAĞ_DEĞ_SAY=süre_değer(dize_veri);int dosya_tanıtıcısı=açık_Dosya((const char*)yol,sadece_yazılabilir_değer|없으면만들기|kesmek_içindekiler,0600);if(dosya_tanıtıcısı<0)자바실패();int 반환값=yazma_Dosya_veri(dosya_tanıtıcısı,dize_veri,öğe_BAĞ_DEĞ_SAY);Kapat_Dosya(dosya_tanıtıcısı);if(반환값!=(int)öğe_BAĞ_DEĞ_SAY)자바실패();return 0;}
makine_Word 자바파일읽기(makine_Word yol){int dosya_tanıtıcısı=açık_Dosya((const char*)yol,salt_okunur_değer,0);if(dosya_tanıtıcısı<0)자바실패();int öğe_BAĞ_DEĞ_SAY=dosya_boyutu(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY<0||öğe_BAĞ_DEĞ_SAY>16384||(unsigned)(öğe_BAĞ_DEĞ_SAY+8)/8>8192-사용량)자바실패();char*veri_konum=(char*)(dinamik_bellek+사용량);사용량+=(öğe_BAĞ_DEĞ_SAY+8)/8;int 반환값=파일자료읽기(dosya_tanıtıcısı,veri_konum,öğe_BAĞ_DEĞ_SAY);Kapat_Dosya(dosya_tanıtıcısı);if(반환값!=öğe_BAĞ_DEĞ_SAY)자바실패();veri_konum[öğe_BAĞ_DEĞ_SAY]=0;return (makine_Word)veri_konum;}
