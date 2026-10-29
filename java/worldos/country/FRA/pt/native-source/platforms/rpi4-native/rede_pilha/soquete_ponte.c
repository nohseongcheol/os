#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "rede_pilha.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int externo[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_externo_par[8], limite_email[8];
static int externo_número(int identificador_de_arquivo) { return identificador_de_arquivo>=32 && identificador_de_arquivo<56 ? externo[identificador_de_arquivo-32]-1 : -1; }
static int colar_SMS(int identificador_de_arquivo,int TIPO_área) {
    if(identificador_de_arquivo<32||identificador_de_arquivo>=56)return -9;int Anterior_item=externo_número(identificador_de_arquivo);if(Anterior_item>=0)return Anterior_item;
    int item_CONT_NÚM=Criar_soquete_empresa(TIPO_área);if(item_CONT_NÚM>=0)externo[identificador_de_arquivo-32]=item_CONT_NÚM+1;return item_CONT_NÚM;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SEGUNDO_VALOR,int32_t ponto_de_código){return 되돌림전문만들기(첫째값,SEGUNDO_VALOR,ponto_de_código);}
int32_t 자바전문묶기(int32_t identificador_de_arquivo,int32_t endereço_na_Internet,int32_t número_da_porta){
    if(endereço_na_Internet==0x7f000001)return 되돌림전문묶기(identificador_de_arquivo,endereço_na_Internet,número_da_porta);
    if(endereço_na_Internet!=0&&endereço_na_Internet!=leitura_rede_Status(0,0))return -99;
    int 반환값=되돌림전문묶기(identificador_de_arquivo,0,número_da_porta);if(반환값<0)return 반환값;
    int item_CONT_NÚM=colar_SMS(identificador_de_arquivo,2);if(item_CONT_NÚM<0)return item_CONT_NÚM;반환값=NET_BIND(item_CONT_NÚM,leitura_rede_Status(0,0),되돌림전문접속번호(identificador_de_arquivo));if(!반환값)limite_email[identificador_de_arquivo-32]=endereço_na_Internet;return 반환값;
}
int32_t 자바전문보내기(int32_t identificador_de_arquivo,int32_t endereço_na_Internet,int32_t número_da_porta,int32_t Tamanho){
    if(endereço_na_Internet==0x7f000001)return 되돌림전문보내기(identificador_de_arquivo,endereço_na_Internet,número_da_porta,Tamanho);
    if(Tamanho<0||Tamanho>512)return -90;if(número_da_porta<1||número_da_porta>65535)return -22;
    if(되돌림전문접속번호(identificador_de_arquivo)<0)return -9;
    if(되돌림전문주소(identificador_de_arquivo)==0x7f000001)return -101;
    int item_CONT_NÚM=externo_número(identificador_de_arquivo);if(item_CONT_NÚM<0){int 반환값=0;if(되돌림전문접속번호(identificador_de_arquivo)==0)반환값=되돌림전문묶기(identificador_de_arquivo,0,0);if(반환값<0)return 반환값;item_CONT_NÚM=colar_SMS(identificador_de_arquivo,2);if(item_CONT_NÚM<0)return item_CONT_NÚM;반환값=NET_BIND(item_CONT_NÚM,leitura_rede_Status(0,0),되돌림전문접속번호(identificador_de_arquivo));if(반환값<0)return 반환값;}
    unsigned char dados[512];for(int 순번=0;순번<Tamanho;순번++)dados[순번]=자바전문얻기(순번);return enviar_datagrama(item_CONT_NÚM,dados,Tamanho,endereço_na_Internet,número_da_porta);
}
int32_t 자바전문받기(int32_t identificador_de_arquivo,int32_t Tamanho){
    int item_CONT_NÚM=externo_número(identificador_de_arquivo);if(item_CONT_NÚM<0)return 되돌림전문받기(identificador_de_arquivo,Tamanho);if(Tamanho<0||Tamanho>512)return -22;
    int local=되돌림전문받기(identificador_de_arquivo,Tamanho);if(local!=-11){UDP_externo_par[identificador_de_arquivo-32]=0;return local;}
    unsigned char dados[512];int 반환값=receber_datagrama(item_CONT_NÚM,dados,Tamanho);if(반환값>=0)UDP_externo_par[identificador_de_arquivo-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dados[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t identificador_de_arquivo){int item_CONT_NÚM=externo_número(identificador_de_arquivo);return item_CONT_NÚM<0?되돌림전문접속번호(identificador_de_arquivo):(int32_t)rede_número_da_porta(item_CONT_NÚM);}
int32_t 자바전문주소(int32_t identificador_de_arquivo){return externo_número(identificador_de_arquivo)<0?되돌림전문주소(identificador_de_arquivo):limite_email[identificador_de_arquivo-32];}
int32_t 자바전문상대(int32_t identificador_de_arquivo){int item_CONT_NÚM=externo_número(identificador_de_arquivo);return item_CONT_NÚM<0||!UDP_externo_par[identificador_de_arquivo-32]?되돌림전문상대(identificador_de_arquivo):(int32_t)par_número_da_porta(item_CONT_NÚM);}
int32_t 자바전문원격주소(int32_t identificador_de_arquivo){int item_CONT_NÚM=externo_número(identificador_de_arquivo);return item_CONT_NÚM<0||!UDP_externo_par[identificador_de_arquivo-32]?0x7f000001:(int32_t)NET_par_email(item_CONT_NÚM);}
int32_t 자바전문닫기(int32_t identificador_de_arquivo){int item_CONT_NÚM=externo_número(identificador_de_arquivo);if(item_CONT_NÚM>=0){Close_rede(item_CONT_NÚM);externo[identificador_de_arquivo-32]=0;}if(identificador_de_arquivo>=32&&identificador_de_arquivo<40)UDP_externo_par[identificador_de_arquivo-32]=limite_email[identificador_de_arquivo-32]=0;return 되돌림전문닫기(identificador_de_arquivo);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t identificador_de_arquivo,int32_t endereço_na_Internet,int32_t número_da_porta){
    if(endereço_na_Internet==0||endereço_na_Internet==0x7f000001){int 반환값=되돌림흐름묶기(identificador_de_arquivo,endereço_na_Internet,número_da_porta);if(!반환값)임의주소[identificador_de_arquivo-32]=endereço_na_Internet==0;return 반환값;}
    if(endereço_na_Internet!=leitura_rede_Status(0,0))return -99;int 반환값=되돌림흐름묶기(identificador_de_arquivo,0,número_da_porta);if(반환값<0)return 반환값;
    int item_CONT_NÚM=colar_SMS(identificador_de_arquivo,1);return item_CONT_NÚM<0?item_CONT_NÚM:NET_BIND(item_CONT_NÚM,endereço_na_Internet,되돌림흐름접속번호(identificador_de_arquivo));
}
int32_t 자바흐름듣기(int32_t identificador_de_arquivo,int32_t lista_de_pendências){
    int item_CONT_NÚM=externo_número(identificador_de_arquivo);if(item_CONT_NÚM<0){int 반환값=되돌림흐름듣기(identificador_de_arquivo,lista_de_pendências);if(반환값<0||!임의주소[identificador_de_arquivo-32])return 반환값;
        item_CONT_NÚM=colar_SMS(identificador_de_arquivo,1);if(item_CONT_NÚM<0)return item_CONT_NÚM;반환값=NET_BIND(item_CONT_NÚM,leitura_rede_Status(0,0),되돌림흐름접속번호(identificador_de_arquivo));if(반환값<0)return 반환값;양쪽수신창구[identificador_de_arquivo-32]=1;
    }return lista_de_pendências<1?-22:NET_escutar(item_CONT_NÚM);
}
int32_t 자바흐름연결(int32_t identificador_de_arquivo,int32_t endereço_na_Internet,int32_t número_da_porta){
    if(endereço_na_Internet==0x7f000001 && externo_número(identificador_de_arquivo)<0)return 되돌림흐름연결(identificador_de_arquivo,endereço_na_Internet,número_da_porta);
    if(되돌림흐름접속번호(identificador_de_arquivo)<0)return -9;int item_CONT_NÚM=colar_SMS(identificador_de_arquivo,1);return item_CONT_NÚM<0?item_CONT_NÚM:NET_Conexão(item_CONT_NÚM,endereço_na_Internet,número_da_porta);
}
int32_t 자바흐름연결받기(int32_t identificador_de_arquivo){
    int item_CONT_NÚM=externo_número(identificador_de_arquivo);if(item_CONT_NÚM<0)return 되돌림흐름연결받기(identificador_de_arquivo);
    if(양쪽수신창구[identificador_de_arquivo-32]){int local=되돌림흐름연결받기(identificador_de_arquivo);if(local!=-11)return local;}
    int par_VALOR=NET_aceitar(item_CONT_NÚM);if(par_VALOR<0)return par_VALOR;
    int meta=되돌림흐름만들기();if(meta<0){Close_rede(par_VALOR);return meta;}externo[meta-32]=par_VALOR+1;return meta;
}
int32_t 자바흐름읽기(int32_t identificador_de_arquivo,int32_t Tamanho){
    int item_CONT_NÚM=externo_número(identificador_de_arquivo);if(item_CONT_NÚM<0)return 되돌림흐름읽기(identificador_de_arquivo,Tamanho);if(Tamanho<0||Tamanho>512)return -22;
    unsigned char dados[512];int 반환값=NET_leitura(item_CONT_NÚM,dados,Tamanho);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dados[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t identificador_de_arquivo,int32_t Tamanho){
    int item_CONT_NÚM=externo_número(identificador_de_arquivo);if(item_CONT_NÚM<0)return 되돌림흐름쓰기(identificador_de_arquivo,Tamanho);if(Tamanho<0||Tamanho>512)return -22;
    unsigned char dados[512];for(int 순번=0;순번<Tamanho;순번++)dados[순번]=자바전문얻기(순번);return NET_gravar(item_CONT_NÚM,dados,Tamanho);
}
int32_t 자바흐름접속번호(int32_t identificador_de_arquivo){int item_CONT_NÚM=externo_número(identificador_de_arquivo);return item_CONT_NÚM<0?되돌림흐름접속번호(identificador_de_arquivo):(int32_t)rede_número_da_porta(item_CONT_NÚM);}
int32_t 자바흐름상대(int32_t identificador_de_arquivo){int item_CONT_NÚM=externo_número(identificador_de_arquivo);return item_CONT_NÚM<0?되돌림흐름상대(identificador_de_arquivo):(int32_t)par_número_da_porta(item_CONT_NÚM);}
int32_t 자바흐름주소(int32_t identificador_de_arquivo){return externo_número(identificador_de_arquivo)<0?0x7f000001:양쪽수신창구[identificador_de_arquivo-32]?0:leitura_rede_Status(0,0);}
int32_t 자바흐름닫기(int32_t identificador_de_arquivo){int item_CONT_NÚM=externo_número(identificador_de_arquivo);if(item_CONT_NÚM>=0){Close_rede(item_CONT_NÚM);externo[identificador_de_arquivo-32]=0;}if(identificador_de_arquivo>=40&&identificador_de_arquivo<56)임의주소[identificador_de_arquivo-32]=양쪽수신창구[identificador_de_arquivo-32]=0;return 되돌림흐름닫기(identificador_de_arquivo);}
