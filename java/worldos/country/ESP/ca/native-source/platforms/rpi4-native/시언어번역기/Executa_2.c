#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identificador_VALOR[16];uint16_t TIPUS_Categoria,màquina_TIPUS;uint32_t 판번호;uint64_t introducció_p,programa_Capçalera_DESPLAÇAMENT,capçalera_de_la_secció_DESPLAÇAMENT;uint32_t configuració_Servei_de_transferència_intel_ligent_en_segon_terme;uint16_t Mida,programa_Capçalera_canviar_la_mida,programa_Capçalera_COMPT,capçalera_de_la_secció_canviar_la_mida,capçalera_de_la_secció_COMPT,secció_nom_taula; } Capçalera_VALOR;
typedef struct {uint32_t TIPUS_Categoria,configuració_Servei_de_transferència_intel_ligent_en_segon_terme;uint64_t DESPLAÇAMENT_VALOR,Adreça,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALOR;
static unsigned char IMATGE[16384];
static int publicar_introducció(const char *Nom){
    size_t element_COMPT;const unsigned char*원본자료=시언어출력(&element_COMPT);if(element_COMPT<sizeof(Capçalera_VALOR))return -1;
    Capçalera_VALOR 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TIPUS_Categoria!=2||실행머리.màquina_TIPUS!=183||실행머리.programa_Capçalera_canviar_la_mida!=sizeof(segment_VALOR)||!실행머리.programa_Capçalera_COMPT||실행머리.programa_Capçalera_COMPT>16||실행머리.programa_Capçalera_DESPLAÇAMENT>element_COMPT||실행머리.programa_Capçalera_COMPT*sizeof(segment_VALOR)>element_COMPT-실행머리.programa_Capçalera_DESPLAÇAMENT)return -1;
    실행머리.programa_Capçalera_DESPLAÇAMENT=sizeof(실행머리);실행머리.capçalera_de_la_secció_DESPLAÇAMENT=실행머리.capçalera_de_la_secció_COMPT=실행머리.capçalera_de_la_secció_canviar_la_mida=실행머리.secció_nom_taula=0;memcpy(IMATGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.programa_Capçalera_COMPT*sizeof(segment_VALOR),Següent_element=4096;unsigned char pàgina_Llista[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.programa_Capçalera_COMPT;순번++){
        segment_VALOR dades_càrrec;Capçalera_VALOR 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&dades_càrrec,원본자료+원본.programa_Capçalera_DESPLAÇAMENT+순번*sizeof(dades_càrrec),sizeof(dades_càrrec));
        if(dades_càrrec.DESPLAÇAMENT_VALOR>element_COMPT||dades_càrrec.파일영역크기>element_COMPT-dades_càrrec.DESPLAÇAMENT_VALOR||dades_càrrec.파일영역크기>dades_càrrec.기억영역크기)return -1;
        if(dades_càrrec.TIPUS_Categoria==1){
            if((dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme&~7u)||!(dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme&4)||(dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme&3)==3||dades_càrrec.Adreça<0x02000000||dades_càrrec.Adreça>0x02c00000||dades_càrrec.기억영역크기>0x02c00000-dades_càrrec.Adreça)return -1;
            if((dades_càrrec.configuració_Servei_de_transferència_intel_ligent_en_segon_terme&1)&&실행머리.introducció_p>=dades_càrrec.Adreça&&실행머리.introducció_p-dades_càrrec.Adreça<dades_càrrec.파일영역크기&&!(실행머리.introducció_p&3))진입점정상=1;
            size_t 선행값=dades_càrrec.Adreça&4095,바이트들=dades_càrrec.파일영역크기?선행값+dades_càrrec.파일영역크기:0;
            if(Següent_element>sizeof(IMATGE)||바이트들>sizeof(IMATGE)-Següent_element){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Següent_element+바이트들),(unsigned)sizeof(IMATGE));return -1;}
            if(바이트들)memcpy(IMATGE+Següent_element+선행값,원본자료+dades_càrrec.DESPLAÇAMENT_VALOR,dades_càrrec.파일영역크기);
            dades_càrrec.Adreça-=선행값;dades_càrrec.물리주소=dades_càrrec.Adreça;dades_càrrec.기억영역크기+=선행값;dades_càrrec.파일영역크기=바이트들;dades_càrrec.DESPLAÇAMENT_VALOR=Següent_element;dades_càrrec.맞춤=4096;
            for(uint64_t pàgina_VALOR=dades_càrrec.Adreça;pàgina_VALOR<dades_càrrec.Adreça+dades_càrrec.기억영역크기;pàgina_VALOR+=4096){unsigned Cerca_INDEX=(pàgina_VALOR-0x02000000)/4096;if(Cerca_INDEX>=sizeof(pàgina_Llista)||pàgina_Llista[Cerca_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}pàgina_Llista[Cerca_INDEX]=1;}
            Següent_element+=(바이트들+4095)&~(size_t)4095;
        }else if(dades_càrrec.TIPUS_Categoria==4){if(dades_càrrec.파일영역크기>4096-부가정보)return -1;memcpy(IMATGE+부가정보,원본자료+dades_càrrec.DESPLAÇAMENT_VALOR,dades_càrrec.파일영역크기);dades_càrrec.DESPLAÇAMENT_VALOR=부가정보;부가정보+=dades_càrrec.파일영역크기;}
        else if(dades_càrrec.TIPUS_Categoria!=0&&dades_càrrec.TIPUS_Categoria!=6&&dades_càrrec.TIPUS_Categoria!=0x6474e551)return -1;
        memcpy(IMATGE+실행머리.programa_Capçalera_DESPLAÇAMENT+순번*sizeof(dades_càrrec),&dades_càrrec,sizeof(dades_càrrec));
    }
    if(!진입점정상)return -1;
    intptr_t arxiu_control_7f4cdfd5=사용자호출(3,(uintptr_t)Nom,577,0600,0,0,0);if(arxiu_control_7f4cdfd5<0){printf("cc: cannot create output file, error %d\n",(int)arxiu_control_7f4cdfd5);return -1;}
    intptr_t 쓴수=사용자호출(1,arxiu_control_7f4cdfd5,(uintptr_t)IMATGE,Següent_element,0,0,0);사용자호출(4,arxiu_control_7f4cdfd5,0,0,0,0,0);return 쓴수==(intptr_t)Següent_element?0:-1;
}
int Inici_usuari_programa(int 방식){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(방식?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(방식?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*cadena_dades=tcc_new();if(!cadena_dades)return 1;
    tcc_undefine_symbol(cadena_dades,"__linux__");tcc_undefine_symbol(cadena_dades,"__linux");tcc_undefine_symbol(cadena_dades,"linux");
    tcc_undefine_symbol(cadena_dades,"__unix__");tcc_undefine_symbol(cadena_dades,"__unix");tcc_undefine_symbol(cadena_dades,"unix");
    tcc_undefine_symbol(cadena_dades,"__STDC_HOSTED__");tcc_define_symbol(cadena_dades,"__STDC_HOSTED__","0");tcc_define_symbol(cadena_dades,"__JKOROS__","1");
    tcc_set_options(cadena_dades,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(cadena_dades,"/sdk/include");
    int 반환값=tcc_set_output_type(cadena_dades,TCC_OUTPUT_EXE);
    if(!반환값){if(방식){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(cadena_dades,원본자료):-1;}else 반환값=tcc_add_file(cadena_dades,입력결과);}
    if(!반환값)반환값=tcc_add_file(cadena_dades,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(cadena_dades,"/sdk/lib/crt.o");
    if(!반환값&&방식)반환값=tcc_add_file(cadena_dades,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(cadena_dades,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(cadena_dades,"/@cc-output");
    if(!반환값)반환값=publicar_introducció(출력결과);
    tcc_delete(cadena_dades);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(방식?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
