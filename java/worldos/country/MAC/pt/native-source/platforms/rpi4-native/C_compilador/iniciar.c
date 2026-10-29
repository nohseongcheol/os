#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_saída(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identificador_VALOR[16];uint16_t TIPO_área,computador_TIPO;uint32_t número_de_versão;uint64_t ponto_de_entrada,app_Cabeçalho_DESLOC,cabeçalho_da_seção_DESLOC;uint32_t Configuração_BITS;uint16_t Tamanho,app_Cabeçalho_dimensionar,app_Cabeçalho_CONT_NÚM,cabeçalho_da_seção_dimensionar,cabeçalho_da_seção_CONT_NÚM,seção_nome_tabela; } Cabeçalho_VALOR;
typedef struct {uint32_t TIPO_área,Configuração_BITS;uint64_t DESLOC_VALOR,Endereço,물리주소,파일영역크기,기억영역크기,alinhar_limite;} segmento_VALOR;
static unsigned char foto[16384];
static int publicar_entrada(const char *Nome){
    size_t item_CONT_NÚM;const unsigned char*원본자료=C_saída(&item_CONT_NÚM);if(item_CONT_NÚM<sizeof(Cabeçalho_VALOR))return -1;
    Cabeçalho_VALOR executável_Cabeçalho;memcpy(&executável_Cabeçalho,원본자료,sizeof(executável_Cabeçalho));
    if(executável_Cabeçalho.TIPO_área!=2||executável_Cabeçalho.computador_TIPO!=183||executável_Cabeçalho.app_Cabeçalho_dimensionar!=sizeof(segmento_VALOR)||!executável_Cabeçalho.app_Cabeçalho_CONT_NÚM||executável_Cabeçalho.app_Cabeçalho_CONT_NÚM>16||executável_Cabeçalho.app_Cabeçalho_DESLOC>item_CONT_NÚM||executável_Cabeçalho.app_Cabeçalho_CONT_NÚM*sizeof(segmento_VALOR)>item_CONT_NÚM-executável_Cabeçalho.app_Cabeçalho_DESLOC)return -1;
    executável_Cabeçalho.app_Cabeçalho_DESLOC=sizeof(executável_Cabeçalho);executável_Cabeçalho.cabeçalho_da_seção_DESLOC=executável_Cabeçalho.cabeçalho_da_seção_CONT_NÚM=executável_Cabeçalho.cabeçalho_da_seção_dimensionar=executável_Cabeçalho.seção_nome_tabela=0;memcpy(foto,&executável_Cabeçalho,sizeof(executável_Cabeçalho));
    size_t 부가정보=sizeof(executável_Cabeçalho)+executável_Cabeçalho.app_Cabeçalho_CONT_NÚM*sizeof(segmento_VALOR),Avançar_item=4096;unsigned char página_Lista[3072]={0};int válido_ponto_de_entrada=0;
    for(unsigned 순번=0;순번<executável_Cabeçalho.app_Cabeçalho_CONT_NÚM;순번++){
        segmento_VALOR dados_cargo;Cabeçalho_VALOR 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&dados_cargo,원본자료+원본.app_Cabeçalho_DESLOC+순번*sizeof(dados_cargo),sizeof(dados_cargo));
        if(dados_cargo.DESLOC_VALOR>item_CONT_NÚM||dados_cargo.파일영역크기>item_CONT_NÚM-dados_cargo.DESLOC_VALOR||dados_cargo.파일영역크기>dados_cargo.기억영역크기)return -1;
        if(dados_cargo.TIPO_área==1){
            if((dados_cargo.Configuração_BITS&~7u)||!(dados_cargo.Configuração_BITS&4)||(dados_cargo.Configuração_BITS&3)==3||dados_cargo.Endereço<0x02000000||dados_cargo.Endereço>0x02c00000||dados_cargo.기억영역크기>0x02c00000-dados_cargo.Endereço)return -1;
            if((dados_cargo.Configuração_BITS&1)&&executável_Cabeçalho.ponto_de_entrada>=dados_cargo.Endereço&&executável_Cabeçalho.ponto_de_entrada-dados_cargo.Endereço<dados_cargo.파일영역크기&&!(executável_Cabeçalho.ponto_de_entrada&3))válido_ponto_de_entrada=1;
            size_t 선행값=dados_cargo.Endereço&4095,바이트들=dados_cargo.파일영역크기?선행값+dados_cargo.파일영역크기:0;
            if(Avançar_item>sizeof(foto)||바이트들>sizeof(foto)-Avançar_item){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Avançar_item+바이트들),(unsigned)sizeof(foto));return -1;}
            if(바이트들)memcpy(foto+Avançar_item+선행값,원본자료+dados_cargo.DESLOC_VALOR,dados_cargo.파일영역크기);
            dados_cargo.Endereço-=선행값;dados_cargo.물리주소=dados_cargo.Endereço;dados_cargo.기억영역크기+=선행값;dados_cargo.파일영역크기=바이트들;dados_cargo.DESLOC_VALOR=Avançar_item;dados_cargo.alinhar_limite=4096;
            for(uint64_t página_VALOR=dados_cargo.Endereço;página_VALOR<dados_cargo.Endereço+dados_cargo.기억영역크기;página_VALOR+=4096){unsigned PROC_ÍNDICE=(página_VALOR-0x02000000)/4096;if(PROC_ÍNDICE>=sizeof(página_Lista)||página_Lista[PROC_ÍNDICE]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}página_Lista[PROC_ÍNDICE]=1;}
            Avançar_item+=(바이트들+4095)&~(size_t)4095;
        }else if(dados_cargo.TIPO_área==4){if(dados_cargo.파일영역크기>4096-부가정보)return -1;memcpy(foto+부가정보,원본자료+dados_cargo.DESLOC_VALOR,dados_cargo.파일영역크기);dados_cargo.DESLOC_VALOR=부가정보;부가정보+=dados_cargo.파일영역크기;}
        else if(dados_cargo.TIPO_área!=0&&dados_cargo.TIPO_área!=6&&dados_cargo.TIPO_área!=0x6474e551)return -1;
        memcpy(foto+executável_Cabeçalho.app_Cabeçalho_DESLOC+순번*sizeof(dados_cargo),&dados_cargo,sizeof(dados_cargo));
    }
    if(!válido_ponto_de_entrada)return -1;
    intptr_t identificador_de_arquivo=사용자호출(3,(uintptr_t)Nome,577,0600,0,0,0);if(identificador_de_arquivo<0){printf("cc: cannot create output file, error %d\n",(int)identificador_de_arquivo);return -1;}
    intptr_t 쓴수=사용자호출(1,identificador_de_arquivo,(uintptr_t)foto,Avançar_item,0,0,0);사용자호출(4,identificador_de_arquivo,0,0,0,0,0);return 쓴수==(intptr_t)Avançar_item?0:-1;
}
int START_usuário_app(int método_MODO){
    char entrada[256],선택항목[256],saída[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(método_MODO?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)entrada,sizeof(entrada),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(entrada,"--version")||!strcmp(entrada,"-version"))){printf(método_MODO?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)saída,sizeof(saída),0,0,0)<0)return 2;}
    if(!strcmp(entrada,saída)){printf("cc: input and output must differ\n");return 2;}
    TCCState*cadeia_dados=tcc_new();if(!cadeia_dados)return 1;
    tcc_undefine_symbol(cadeia_dados,"__linux__");tcc_undefine_symbol(cadeia_dados,"__linux");tcc_undefine_symbol(cadeia_dados,"linux");
    tcc_undefine_symbol(cadeia_dados,"__unix__");tcc_undefine_symbol(cadeia_dados,"__unix");tcc_undefine_symbol(cadeia_dados,"unix");
    tcc_undefine_symbol(cadeia_dados,"__STDC_HOSTED__");tcc_define_symbol(cadeia_dados,"__STDC_HOSTED__","0");tcc_define_symbol(cadeia_dados,"__JKOROS__","1");
    tcc_set_options(cadeia_dados,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(cadeia_dados,"/sdk/include");
    int 반환값=tcc_set_output_type(cadeia_dados,TCC_OUTPUT_EXE);
    if(!반환값){if(método_MODO){const char*원본자료=자바미리번역원문(entrada);반환값=원본자료?tcc_compile_string(cadeia_dados,원본자료):-1;}else 반환값=tcc_add_file(cadeia_dados,entrada);}
    if(!반환값)반환값=tcc_add_file(cadeia_dados,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(cadeia_dados,"/sdk/lib/crt.o");
    if(!반환값&&método_MODO)반환값=tcc_add_file(cadeia_dados,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(cadeia_dados,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(cadeia_dados,"/@cc-output");
    if(!반환값)반환값=publicar_entrada(saída);
    tcc_delete(cadeia_dados);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(método_MODO?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",saída);return 0;
}
