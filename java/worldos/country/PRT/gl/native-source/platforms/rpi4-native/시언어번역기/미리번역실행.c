#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "파일규약.h"
typedef unsigned long máquina_Word;
static máquina_Word 동적기억공간[8192];static unsigned 사용량;
void 자바실패(void){const char Texto[]="AOT runtime error\n";escribir_Ficheiro_datos(2,Texto,sizeof(Texto)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(máquina_Word *Montón_Almacenamento,int *깊이,máquina_Word VALOR){if(*깊이<0||*깊이>=128)자바실패();Montón_Almacenamento[(*깊이)++]=VALOR;}
máquina_Word 자바꺼내기(máquina_Word *Montón_Almacenamento,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return Montón_Almacenamento[--*깊이];}
máquina_Word 자바배열(int elemento_CONTAR){if(elemento_CONTAR<0||(unsigned)elemento_CONTAR+1>8192-사용량)자바실패();máquina_Word*datos_cargo=동적기억공간+사용량;사용량+=elemento_CONTAR+1;datos_cargo[0]=elemento_CONTAR;return (máquina_Word)datos_cargo;}
máquina_Word *자바색인(máquina_Word obxecto_Material_de_referencia,int elemento_CONTAR){máquina_Word*datos_cargo=(máquina_Word*)obxecto_Material_de_referencia;if(!datos_cargo||elemento_CONTAR<0||(máquina_Word)elemento_CONTAR>=datos_cargo[0])자바실패();return datos_cargo+elemento_CONTAR+1;}
int 자바길이(máquina_Word obxecto_Material_de_referencia){if(!obxecto_Material_de_referencia)자바실패();return *(máquina_Word*)obxecto_Material_de_referencia;}
int 자바나누기(int X_coordenada,int Y_coordenada,int 나머지){if(!Y_coordenada)자바실패();if(X_coordenada==(-2147483647-1)&&Y_coordenada==-1)return 나머지?0:X_coordenada;return 나머지?X_coordenada%Y_coordenada:X_coordenada/Y_coordenada;}
static unsigned duración_VALOR(const char*cadea_datos){unsigned elemento_CONTAR=0;if(!cadea_datos)자바실패();while(cadea_datos[elemento_CONTAR])elemento_CONTAR++;return elemento_CONTAR;}
void 자바출력(máquina_Word datos_cargo,int 수치,int 줄바꿈){
    if(수치){char SEGUNDO_VALOR[16];unsigned elemento_CONTAR=0;int VALOR=(int)datos_cargo;unsigned 부호없는값=VALOR<0?0-(unsigned)VALOR:VALOR;do{SEGUNDO_VALOR[elemento_CONTAR++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALOR<0)SEGUNDO_VALOR[elemento_CONTAR++]='-';while(elemento_CONTAR)escribir_Ficheiro_datos(1,SEGUNDO_VALOR+--elemento_CONTAR,1);}
    else{const char*cadea_datos=datos_cargo?(const char*)datos_cargo:"null";escribir_Ficheiro_datos(1,cadea_datos,duración_VALOR(cadea_datos));}if(줄바꿈)escribir_Ficheiro_datos(1,"\n",1);
}
máquina_Word 자바파일쓰기(máquina_Word CAMIÑO,máquina_Word VALOR){const char*cadea_datos=(const char*)VALOR;unsigned elemento_CONTAR=duración_VALOR(cadea_datos);int Ficheiro_agarradoira=abrir_Ficheiro((const char*)CAMIÑO,쓰기전용|없으면만들기|내용비우기,0600);if(Ficheiro_agarradoira<0)자바실패();int 반환값=escribir_Ficheiro_datos(Ficheiro_agarradoira,cadea_datos,elemento_CONTAR);peche_Ficheiro(Ficheiro_agarradoira);if(반환값!=(int)elemento_CONTAR)자바실패();return 0;}
máquina_Word 자바파일읽기(máquina_Word CAMIÑO){int Ficheiro_agarradoira=abrir_Ficheiro((const char*)CAMIÑO,só_de_lectura_VALOR,0);if(Ficheiro_agarradoira<0)자바실패();int elemento_CONTAR=파일크기(Ficheiro_agarradoira);if(elemento_CONTAR<0||elemento_CONTAR>16384||(unsigned)(elemento_CONTAR+8)/8>8192-사용량)자바실패();char*datos_cargo=(char*)(동적기억공간+사용량);사용량+=(elemento_CONTAR+8)/8;int 반환값=파일자료읽기(Ficheiro_agarradoira,datos_cargo,elemento_CONTAR);peche_Ficheiro(Ficheiro_agarradoira);if(반환값!=elemento_CONTAR)자바실패();datos_cargo[elemento_CONTAR]=0;return (máquina_Word)datos_cargo;}
