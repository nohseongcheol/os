#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char 식별자[16];uint16_t TIPO_Categoría,máquina_TIPO;uint32_t 판번호;uint64_t introdución_p,apl_Cabeceira_DESPRAZAMENTO,sección_Cabeceira_DESPRAZAMENTO;uint32_t configuración_Servizo_de_transferencia_intelixente_en_segundo_plano;uint16_t Tamaño,프로그램머리크기,apl_Cabeceira_CONTAR,구역머리크기,sección_Cabeceira_CONTAR,sección_nome_táboa; } Cabeceira_VALOR;
typedef struct {uint32_t TIPO_Categoría,configuración_Servizo_de_transferencia_intelixente_en_segundo_plano;uint64_t DESPRAZAMENTO_VALOR,ENDEREZO,물리주소,파일영역크기,기억영역크기,맞춤;} segmento_VALOR;
static unsigned char IMAXE[16384];
static int publicar_introdución(const char *Nome){
    size_t elemento_CONTAR;const unsigned char*원본자료=시언어출력(&elemento_CONTAR);if(elemento_CONTAR<sizeof(Cabeceira_VALOR))return -1;
    Cabeceira_VALOR 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TIPO_Categoría!=2||실행머리.máquina_TIPO!=183||실행머리.프로그램머리크기!=sizeof(segmento_VALOR)||!실행머리.apl_Cabeceira_CONTAR||실행머리.apl_Cabeceira_CONTAR>16||실행머리.apl_Cabeceira_DESPRAZAMENTO>elemento_CONTAR||실행머리.apl_Cabeceira_CONTAR*sizeof(segmento_VALOR)>elemento_CONTAR-실행머리.apl_Cabeceira_DESPRAZAMENTO)return -1;
    실행머리.apl_Cabeceira_DESPRAZAMENTO=sizeof(실행머리);실행머리.sección_Cabeceira_DESPRAZAMENTO=실행머리.sección_Cabeceira_CONTAR=실행머리.구역머리크기=실행머리.sección_nome_táboa=0;memcpy(IMAXE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.apl_Cabeceira_CONTAR*sizeof(segmento_VALOR),Seguinte_elemento=4096;unsigned char páxina_Lista[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.apl_Cabeceira_CONTAR;순번++){
        segmento_VALOR datos_cargo;Cabeceira_VALOR 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&datos_cargo,원본자료+원본.apl_Cabeceira_DESPRAZAMENTO+순번*sizeof(datos_cargo),sizeof(datos_cargo));
        if(datos_cargo.DESPRAZAMENTO_VALOR>elemento_CONTAR||datos_cargo.파일영역크기>elemento_CONTAR-datos_cargo.DESPRAZAMENTO_VALOR||datos_cargo.파일영역크기>datos_cargo.기억영역크기)return -1;
        if(datos_cargo.TIPO_Categoría==1){
            if((datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&~7u)||!(datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&4)||(datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&3)==3||datos_cargo.ENDEREZO<0x02000000||datos_cargo.ENDEREZO>0x02c00000||datos_cargo.기억영역크기>0x02c00000-datos_cargo.ENDEREZO)return -1;
            if((datos_cargo.configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&1)&&실행머리.introdución_p>=datos_cargo.ENDEREZO&&실행머리.introdución_p-datos_cargo.ENDEREZO<datos_cargo.파일영역크기&&!(실행머리.introdución_p&3))진입점정상=1;
            size_t 선행값=datos_cargo.ENDEREZO&4095,바이트들=datos_cargo.파일영역크기?선행값+datos_cargo.파일영역크기:0;
            if(Seguinte_elemento>sizeof(IMAXE)||바이트들>sizeof(IMAXE)-Seguinte_elemento){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Seguinte_elemento+바이트들),(unsigned)sizeof(IMAXE));return -1;}
            if(바이트들)memcpy(IMAXE+Seguinte_elemento+선행값,원본자료+datos_cargo.DESPRAZAMENTO_VALOR,datos_cargo.파일영역크기);
            datos_cargo.ENDEREZO-=선행값;datos_cargo.물리주소=datos_cargo.ENDEREZO;datos_cargo.기억영역크기+=선행값;datos_cargo.파일영역크기=바이트들;datos_cargo.DESPRAZAMENTO_VALOR=Seguinte_elemento;datos_cargo.맞춤=4096;
            for(uint64_t páxina_VALOR=datos_cargo.ENDEREZO;páxina_VALOR<datos_cargo.ENDEREZO+datos_cargo.기억영역크기;páxina_VALOR+=4096){unsigned Busca_ÍNDICE=(páxina_VALOR-0x02000000)/4096;if(Busca_ÍNDICE>=sizeof(páxina_Lista)||páxina_Lista[Busca_ÍNDICE]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}páxina_Lista[Busca_ÍNDICE]=1;}
            Seguinte_elemento+=(바이트들+4095)&~(size_t)4095;
        }else if(datos_cargo.TIPO_Categoría==4){if(datos_cargo.파일영역크기>4096-부가정보)return -1;memcpy(IMAXE+부가정보,원본자료+datos_cargo.DESPRAZAMENTO_VALOR,datos_cargo.파일영역크기);datos_cargo.DESPRAZAMENTO_VALOR=부가정보;부가정보+=datos_cargo.파일영역크기;}
        else if(datos_cargo.TIPO_Categoría!=0&&datos_cargo.TIPO_Categoría!=6&&datos_cargo.TIPO_Categoría!=0x6474e551)return -1;
        memcpy(IMAXE+실행머리.apl_Cabeceira_DESPRAZAMENTO+순번*sizeof(datos_cargo),&datos_cargo,sizeof(datos_cargo));
    }
    if(!진입점정상)return -1;
    intptr_t Ficheiro_agarradoira=사용자호출(3,(uintptr_t)Nome,577,0600,0,0,0);if(Ficheiro_agarradoira<0){printf("cc: cannot create output file, error %d\n",(int)Ficheiro_agarradoira);return -1;}
    intptr_t 쓴수=사용자호출(1,Ficheiro_agarradoira,(uintptr_t)IMAXE,Seguinte_elemento,0,0,0);사용자호출(4,Ficheiro_agarradoira,0,0,0,0,0);return 쓴수==(intptr_t)Seguinte_elemento?0:-1;
}
int START_usuario_apl(int 방식){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(방식?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(방식?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*cadea_datos=tcc_new();if(!cadea_datos)return 1;
    tcc_undefine_symbol(cadea_datos,"__linux__");tcc_undefine_symbol(cadea_datos,"__linux");tcc_undefine_symbol(cadea_datos,"linux");
    tcc_undefine_symbol(cadea_datos,"__unix__");tcc_undefine_symbol(cadea_datos,"__unix");tcc_undefine_symbol(cadea_datos,"unix");
    tcc_undefine_symbol(cadea_datos,"__STDC_HOSTED__");tcc_define_symbol(cadea_datos,"__STDC_HOSTED__","0");tcc_define_symbol(cadea_datos,"__JKOROS__","1");
    tcc_set_options(cadea_datos,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(cadea_datos,"/sdk/include");
    int 반환값=tcc_set_output_type(cadea_datos,TCC_OUTPUT_EXE);
    if(!반환값){if(방식){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(cadea_datos,원본자료):-1;}else 반환값=tcc_add_file(cadea_datos,입력결과);}
    if(!반환값)반환값=tcc_add_file(cadea_datos,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(cadea_datos,"/sdk/lib/crt.o");
    if(!반환값&&방식)반환값=tcc_add_file(cadea_datos,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(cadea_datos,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(cadea_datos,"/@cc-output");
    if(!반환값)반환값=publicar_introdución(출력결과);
    tcc_delete(cadea_datos);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(방식?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
