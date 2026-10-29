#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char Identifikateur_VALUE[16];uint16_t TYPE_Kategorie,Computer_TYPE;uint32_t 판번호;uint64_t Agab_Punkt,App_En_tête_OFFSET,Beräich_En_tête_OFFSET;uint32_t 설정비트;uint16_t d_Gréisst_veränneren,App_En_tête_d_Gréisst_veränneren,App_En_tête_COUNT,Beräich_En_tête_d_Gréisst_veränneren,Beräich_En_tête_COUNT,Beräich_Numm_Tabell; } En_tête_VALUE;
typedef struct {uint32_t TYPE_Kategorie,설정비트;uint64_t OFFSET_VALUE,Adress,물리주소,파일영역크기,기억영역크기,맞춤;} Segment_VALUE;
static unsigned char Bild[16384];
static int publizéieren_Agab(const char *Numm){
    size_t Element_COUNT;const unsigned char*원본자료=시언어출력(&Element_COUNT);if(Element_COUNT<sizeof(En_tête_VALUE))return -1;
    En_tête_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_Kategorie!=2||실행머리.Computer_TYPE!=183||실행머리.App_En_tête_d_Gréisst_veränneren!=sizeof(Segment_VALUE)||!실행머리.App_En_tête_COUNT||실행머리.App_En_tête_COUNT>16||실행머리.App_En_tête_OFFSET>Element_COUNT||실행머리.App_En_tête_COUNT*sizeof(Segment_VALUE)>Element_COUNT-실행머리.App_En_tête_OFFSET)return -1;
    실행머리.App_En_tête_OFFSET=sizeof(실행머리);실행머리.Beräich_En_tête_OFFSET=실행머리.Beräich_En_tête_COUNT=실행머리.Beräich_En_tête_d_Gréisst_veränneren=실행머리.Beräich_Numm_Tabell=0;memcpy(Bild,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.App_En_tête_COUNT*sizeof(Segment_VALUE),Weider_Element=4096;unsigned char Säit_Lëscht[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.App_En_tête_COUNT;순번++){
        Segment_VALUE Daten_positionéieren;En_tête_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&Daten_positionéieren,원본자료+원본.App_En_tête_OFFSET+순번*sizeof(Daten_positionéieren),sizeof(Daten_positionéieren));
        if(Daten_positionéieren.OFFSET_VALUE>Element_COUNT||Daten_positionéieren.파일영역크기>Element_COUNT-Daten_positionéieren.OFFSET_VALUE||Daten_positionéieren.파일영역크기>Daten_positionéieren.기억영역크기)return -1;
        if(Daten_positionéieren.TYPE_Kategorie==1){
            if((Daten_positionéieren.설정비트&~7u)||!(Daten_positionéieren.설정비트&4)||(Daten_positionéieren.설정비트&3)==3||Daten_positionéieren.Adress<0x02000000||Daten_positionéieren.Adress>0x02c00000||Daten_positionéieren.기억영역크기>0x02c00000-Daten_positionéieren.Adress)return -1;
            if((Daten_positionéieren.설정비트&1)&&실행머리.Agab_Punkt>=Daten_positionéieren.Adress&&실행머리.Agab_Punkt-Daten_positionéieren.Adress<Daten_positionéieren.파일영역크기&&!(실행머리.Agab_Punkt&3))진입점정상=1;
            size_t 선행값=Daten_positionéieren.Adress&4095,바이트들=Daten_positionéieren.파일영역크기?선행값+Daten_positionéieren.파일영역크기:0;
            if(Weider_Element>sizeof(Bild)||바이트들>sizeof(Bild)-Weider_Element){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Weider_Element+바이트들),(unsigned)sizeof(Bild));return -1;}
            if(바이트들)memcpy(Bild+Weider_Element+선행값,원본자료+Daten_positionéieren.OFFSET_VALUE,Daten_positionéieren.파일영역크기);
            Daten_positionéieren.Adress-=선행값;Daten_positionéieren.물리주소=Daten_positionéieren.Adress;Daten_positionéieren.기억영역크기+=선행값;Daten_positionéieren.파일영역크기=바이트들;Daten_positionéieren.OFFSET_VALUE=Weider_Element;Daten_positionéieren.맞춤=4096;
            for(uint64_t Säit_VALUE=Daten_positionéieren.Adress;Säit_VALUE<Daten_positionéieren.Adress+Daten_positionéieren.기억영역크기;Säit_VALUE+=4096){unsigned LOOKUP_INDEX=(Säit_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(Säit_Lëscht)||Säit_Lëscht[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}Säit_Lëscht[LOOKUP_INDEX]=1;}
            Weider_Element+=(바이트들+4095)&~(size_t)4095;
        }else if(Daten_positionéieren.TYPE_Kategorie==4){if(Daten_positionéieren.파일영역크기>4096-부가정보)return -1;memcpy(Bild+부가정보,원본자료+Daten_positionéieren.OFFSET_VALUE,Daten_positionéieren.파일영역크기);Daten_positionéieren.OFFSET_VALUE=부가정보;부가정보+=Daten_positionéieren.파일영역크기;}
        else if(Daten_positionéieren.TYPE_Kategorie!=0&&Daten_positionéieren.TYPE_Kategorie!=6&&Daten_positionéieren.TYPE_Kategorie!=0x6474e551)return -1;
        memcpy(Bild+실행머리.App_En_tête_OFFSET+순번*sizeof(Daten_positionéieren),&Daten_positionéieren,sizeof(Daten_positionéieren));
    }
    if(!진입점정상)return -1;
    intptr_t Fichier_Handle=사용자호출(3,(uintptr_t)Numm,577,0600,0,0,0);if(Fichier_Handle<0){printf("cc: cannot create output file, error %d\n",(int)Fichier_Handle);return -1;}
    intptr_t 쓴수=사용자호출(1,Fichier_Handle,(uintptr_t)Bild,Weider_Element,0,0,0);사용자호출(4,Fichier_Handle,0,0,0,0,0);return 쓴수==(intptr_t)Weider_Element?0:-1;
}
int Start_Benotzer_App(int Method_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(Method_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(Method_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*Zeechefolleg_Daten=tcc_new();if(!Zeechefolleg_Daten)return 1;
    tcc_undefine_symbol(Zeechefolleg_Daten,"__linux__");tcc_undefine_symbol(Zeechefolleg_Daten,"__linux");tcc_undefine_symbol(Zeechefolleg_Daten,"linux");
    tcc_undefine_symbol(Zeechefolleg_Daten,"__unix__");tcc_undefine_symbol(Zeechefolleg_Daten,"__unix");tcc_undefine_symbol(Zeechefolleg_Daten,"unix");
    tcc_undefine_symbol(Zeechefolleg_Daten,"__STDC_HOSTED__");tcc_define_symbol(Zeechefolleg_Daten,"__STDC_HOSTED__","0");tcc_define_symbol(Zeechefolleg_Daten,"__JKOROS__","1");
    tcc_set_options(Zeechefolleg_Daten,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(Zeechefolleg_Daten,"/sdk/include");
    int 반환값=tcc_set_output_type(Zeechefolleg_Daten,TCC_OUTPUT_EXE);
    if(!반환값){if(Method_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(Zeechefolleg_Daten,원본자료):-1;}else 반환값=tcc_add_file(Zeechefolleg_Daten,입력결과);}
    if(!반환값)반환값=tcc_add_file(Zeechefolleg_Daten,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(Zeechefolleg_Daten,"/sdk/lib/crt.o");
    if(!반환값&&Method_MODE)반환값=tcc_add_file(Zeechefolleg_Daten,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(Zeechefolleg_Daten,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(Zeechefolleg_Daten,"/@cc-output");
    if(!반환값)반환값=publizéieren_Agab(출력결과);
    tcc_delete(Zeechefolleg_Daten);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(Method_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
