#include "../명명/기계연결이름.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "호출.h"
#include "Arquivo_ABI.h"
typedef unsigned long computador_Word;
static computador_Word memória_dinâmica[8192];static unsigned 사용량;
void 자바실패(void){const char texto[]="AOT runtime error\n";gravar_Arquivo_dados(2,texto,sizeof(texto)-1);사용자호출(6,1,0,0,0,0,0);for(;;){}}
void 자바쌓기(computador_Word *memória_de_pilha,int *깊이,computador_Word VALOR){if(*깊이<0||*깊이>=128)자바실패();memória_de_pilha[(*깊이)++]=VALOR;}
computador_Word 자바꺼내기(computador_Word *memória_de_pilha,int *깊이){if(*깊이<=0||*깊이>128)자바실패();return memória_de_pilha[--*깊이];}
computador_Word 자바배열(int item_CONT_NÚM){if(item_CONT_NÚM<0||(unsigned)item_CONT_NÚM+1>8192-사용량)자바실패();computador_Word*dados_cargo=memória_dinâmica+사용량;사용량+=item_CONT_NÚM+1;dados_cargo[0]=item_CONT_NÚM;return (computador_Word)dados_cargo;}
computador_Word *자바색인(computador_Word objeto_Referência,int item_CONT_NÚM){computador_Word*dados_cargo=(computador_Word*)objeto_Referência;if(!dados_cargo||item_CONT_NÚM<0||(computador_Word)item_CONT_NÚM>=dados_cargo[0])자바실패();return dados_cargo+item_CONT_NÚM+1;}
int 자바길이(computador_Word objeto_Referência){if(!objeto_Referência)자바실패();return *(computador_Word*)objeto_Referência;}
int 자바나누기(int coordenada_X,int Y_coordenada,int 나머지){if(!Y_coordenada)자바실패();if(coordenada_X==(-2147483647-1)&&Y_coordenada==-1)return 나머지?0:coordenada_X;return 나머지?coordenada_X%Y_coordenada:coordenada_X/Y_coordenada;}
static unsigned duração_VALOR(const char*cadeia_dados){unsigned item_CONT_NÚM=0;if(!cadeia_dados)자바실패();while(cadeia_dados[item_CONT_NÚM])item_CONT_NÚM++;return item_CONT_NÚM;}
void 자바출력(computador_Word dados_cargo,int 수치,int 줄바꿈){
    if(수치){char SEGUNDO_VALOR[16];unsigned item_CONT_NÚM=0;int VALOR=(int)dados_cargo;unsigned 부호없는값=VALOR<0?0-(unsigned)VALOR:VALOR;do{SEGUNDO_VALOR[item_CONT_NÚM++]='0'+부호없는값%10;부호없는값/=10;}while(부호없는값);if(VALOR<0)SEGUNDO_VALOR[item_CONT_NÚM++]='-';while(item_CONT_NÚM)gravar_Arquivo_dados(1,SEGUNDO_VALOR+--item_CONT_NÚM,1);}
    else{const char*cadeia_dados=dados_cargo?(const char*)dados_cargo:"null";gravar_Arquivo_dados(1,cadeia_dados,duração_VALOR(cadeia_dados));}if(줄바꿈)gravar_Arquivo_dados(1,"\n",1);
}
computador_Word 자바파일쓰기(computador_Word caminho,computador_Word VALOR){const char*cadeia_dados=(const char*)VALOR;unsigned item_CONT_NÚM=duração_VALOR(cadeia_dados);int identificador_de_arquivo=abrir_Arquivo((const char*)caminho,somente_gravação_VALOR|없으면만들기|cortar_Sumário,0600);if(identificador_de_arquivo<0)자바실패();int 반환값=gravar_Arquivo_dados(identificador_de_arquivo,cadeia_dados,item_CONT_NÚM);Close_Arquivo(identificador_de_arquivo);if(반환값!=(int)item_CONT_NÚM)자바실패();return 0;}
computador_Word 자바파일읽기(computador_Word caminho){int identificador_de_arquivo=abrir_Arquivo((const char*)caminho,somente_leitura_VALOR,0);if(identificador_de_arquivo<0)자바실패();int item_CONT_NÚM=tamanho_do_arquivo(identificador_de_arquivo);if(item_CONT_NÚM<0||item_CONT_NÚM>16384||(unsigned)(item_CONT_NÚM+8)/8>8192-사용량)자바실패();char*dados_cargo=(char*)(memória_dinâmica+사용량);사용량+=(item_CONT_NÚM+8)/8;int 반환값=leitura_Arquivo_dados(identificador_de_arquivo,dados_cargo,item_CONT_NÚM);Close_Arquivo(identificador_de_arquivo);if(반환값!=item_CONT_NÚM)자바실패();dados_cargo[item_CONT_NÚM]=0;return (computador_Word)dados_cargo;}
