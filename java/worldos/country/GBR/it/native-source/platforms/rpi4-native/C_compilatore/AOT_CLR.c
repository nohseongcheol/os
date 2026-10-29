#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "File_ABI.h"
typedef unsigned long computer_Word;
static computer_Word memoria_dinamica[8192];static unsigned 사용량;
void 자바실패(void){const char testo[]="AOT runtime error\n";scrivere_File_dati(2,testo,sizeof(testo)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(computer_Word *memoria_a_pila,int *깊이,computer_Word VALORE){if(*깊이<0||*깊이>=128)자바실패();memoria_a_pila[(*깊이)++]=VALORE;}
computer_Word 자바꺼내기(computer_Word *memoria_a_pila,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return memoria_a_pila[--*깊이];}
computer_Word 자바배열(int articolo_CONTA_NUMERI){if(articolo_CONTA_NUMERI<0||(unsigned)articolo_CONTA_NUMERI+1>8192-사용량)자바실패();computer_Word*dati_funzione=memoria_dinamica+사용량;사용량+=articolo_CONTA_NUMERI+1;dati_funzione[0]=articolo_CONTA_NUMERI;return (computer_Word)dati_funzione;}
computer_Word *자바색인(computer_Word oggetto_fonti,int articolo_CONTA_NUMERI){computer_Word*dati_funzione=(computer_Word*)oggetto_fonti;if(!dati_funzione||articolo_CONTA_NUMERI<0||(computer_Word)articolo_CONTA_NUMERI>=dati_funzione[0])자바실패();return dati_funzione+articolo_CONTA_NUMERI+1;}
int 자바길이(computer_Word oggetto_fonti){if(!oggetto_fonti)자바실패();return *(computer_Word*)oggetto_fonti;}
int 자바나누기(int coordinata_x,int Y_coordinata,int 나머지){if(!Y_coordinata)자바실패();if(coordinata_x==(-2147483647-1)&&Y_coordinata==-1)return 나머지?0:coordinata_x;return 나머지?coordinata_x%Y_coordinata:coordinata_x/Y_coordinata;}
static unsigned durata_VALORE(const char*stringa_dati){unsigned articolo_CONTA_NUMERI=0;if(!stringa_dati)자바실패();while(stringa_dati[articolo_CONTA_NUMERI])articolo_CONTA_NUMERI++;return articolo_CONTA_NUMERI;}
void 자바출력(computer_Word dati_funzione,int 수치,int 줄바꿈){
    if(수치){char SECONDO_VALORE[16];unsigned articolo_CONTA_NUMERI=0;int VALORE=(int)dati_funzione;unsigned 부호없는값=VALORE<0?0-(unsigned)VALORE:VALORE;do{SECONDO_VALORE[articolo_CONTA_NUMERI++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALORE<0)SECONDO_VALORE[articolo_CONTA_NUMERI++]='-';while(articolo_CONTA_NUMERI)scrivere_File_dati(1,SECONDO_VALORE+--articolo_CONTA_NUMERI,1);}
    else{const char*stringa_dati=dati_funzione?(const char*)dati_funzione:"null";scrivere_File_dati(1,stringa_dati,durata_VALORE(stringa_dati));}if(줄바꿈)scrivere_File_dati(1,"\n",1);
}
computer_Word 자바파일쓰기(computer_Word percorso,computer_Word VALORE){const char*stringa_dati=(const char*)VALORE;unsigned articolo_CONTA_NUMERI=durata_VALORE(stringa_dati);int handle_di_file=aperto_File((const char*)percorso,sola_scrittura_VALORE|없으면만들기|tagliare_Sommario,0600);if(handle_di_file<0)자바실패();int 반환값=scrivere_File_dati(handle_di_file,stringa_dati,articolo_CONTA_NUMERI);Chiudi_File(handle_di_file);if(반환값!=(int)articolo_CONTA_NUMERI)자바실패();return 0;}
computer_Word 자바파일읽기(computer_Word percorso){int handle_di_file=aperto_File((const char*)percorso,di_sola_lettura_VALORE,0);if(handle_di_file<0)자바실패();int articolo_CONTA_NUMERI=dimensioni_del_file(handle_di_file);if(articolo_CONTA_NUMERI<0||articolo_CONTA_NUMERI>16384||(unsigned)(articolo_CONTA_NUMERI+8)/8>8192-사용량)자바실패();char*dati_funzione=(char*)(memoria_dinamica+사용량);사용량+=(articolo_CONTA_NUMERI+8)/8;int 반환값=파일자료읽기(handle_di_file,dati_funzione,articolo_CONTA_NUMERI);Chiudi_File(handle_di_file);if(반환값!=articolo_CONTA_NUMERI)자바실패();dati_funzione[articolo_CONTA_NUMERI]=0;return (computer_Word)dati_funzione;}
