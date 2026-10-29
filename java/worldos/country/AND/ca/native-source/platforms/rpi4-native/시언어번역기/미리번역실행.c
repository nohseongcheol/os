#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long màquina_Word;
static màquina_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char SMS[]="AOT runtime error\n";escriure_arxiu_dades(2,SMS,sizeof(SMS)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(màquina_Word *Pila_Emmagatzematge,int *깊이,màquina_Word VALOR){if(*깊이<0||*깊이>=128)자바실패();Pila_Emmagatzematge[(*깊이)++]=VALOR;}
màquina_Word 자바꺼내기(màquina_Word *Pila_Emmagatzematge,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Pila_Emmagatzematge[--*깊이];}
màquina_Word 자바배열(int element_COMPT){if(element_COMPT<0||(unsigned)element_COMPT+1>8192-사용량)자바실패();màquina_Word*dades_càrrec=동적기억공간+사용량;사용량+=element_COMPT+1;dades_càrrec[0]=element_COMPT;return (màquina_Word)dades_càrrec;}
màquina_Word *자바색인(màquina_Word objecte_Referència,int element_COMPT){màquina_Word*dades_càrrec=(màquina_Word*)objecte_Referència;if(!dades_càrrec||element_COMPT<0||(màquina_Word)element_COMPT>=dades_càrrec[0])자바실패();return dades_càrrec+element_COMPT+1;}
int 자바길이(màquina_Word objecte_Referència){if(!objecte_Referència)자바실패();return *(màquina_Word*)objecte_Referència;}
int 자바나누기(int X_coordenada,int Y_coordenada,int 나머지){if(!Y_coordenada)자바실패();if(X_coordenada==(-2147483647-1)&&Y_coordenada==-1)return 나머지?0:X_coordenada;return 나머지?X_coordenada%Y_coordenada:X_coordenada/Y_coordenada;}
static unsigned durada_VALOR(const char*cadena_dades){unsigned element_COMPT=0;if(!cadena_dades)자바실패();while(cadena_dades[element_COMPT])element_COMPT++;return element_COMPT;}
void 자바출력(màquina_Word dades_càrrec,int 수치,int 줄바꿈){
    if(수치){char SEGON_VALOR[16];unsigned element_COMPT=0;int VALOR=(int)dades_càrrec;unsigned 부호없는값=VALOR<0?0-(unsigned)VALOR:VALOR;do{SEGON_VALOR[element_COMPT++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALOR<0)SEGON_VALOR[element_COMPT++]='-';while(element_COMPT)escriure_arxiu_dades(1,SEGON_VALOR+--element_COMPT,1);}
    else{const char*cadena_dades=dades_càrrec?(const char*)dades_càrrec:"null";escriure_arxiu_dades(1,cadena_dades,durada_VALOR(cadena_dades));}if(줄바꿈)escriure_arxiu_dades(1,"\n",1);
}
màquina_Word 자바파일쓰기(màquina_Word Camí,màquina_Word VALOR){const char*cadena_dades=(const char*)VALOR;unsigned element_COMPT=durada_VALOR(cadena_dades);int arxiu_control_7f4cdfd5=crear_arxiu((const char*)Camí,쓰기전용|없으면만들기|내용비우기,0600);if(arxiu_control_7f4cdfd5<0)자바실패();int 반환값=escriure_arxiu_dades(arxiu_control_7f4cdfd5,cadena_dades,element_COMPT);Tanca_arxiu(arxiu_control_7f4cdfd5);if(반환값!=(int)element_COMPT)자바실패();return 0;}
màquina_Word 자바파일읽기(màquina_Word Camí){int arxiu_control_7f4cdfd5=crear_arxiu((const char*)Camí,només_de_lectura_VALOR,0);if(arxiu_control_7f4cdfd5<0)자바실패();int element_COMPT=arxiu_canviar_la_mida(arxiu_control_7f4cdfd5);if(element_COMPT<0||element_COMPT>16384||(unsigned)(element_COMPT+8)/8>8192-사용량)자바실패();char*dades_càrrec=(char*)(동적기억공간+사용량);사용량+=(element_COMPT+8)/8;int 반환값=tancar_arxiu_dades(arxiu_control_7f4cdfd5,dades_càrrec,element_COMPT);Tanca_arxiu(arxiu_control_7f4cdfd5);if(반환값!=element_COMPT)자바실패();dades_càrrec[element_COMPT]=0;return (màquina_Word)dades_càrrec;}
