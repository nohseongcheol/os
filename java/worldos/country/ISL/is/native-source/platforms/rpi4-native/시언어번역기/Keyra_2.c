#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char auðkenni_VALUE[16];uint16_t TYPE_tegund,vél_TYPE;uint32_t útgáfa_númer;uint64_t færsla_P,forrit_Haus_OFFSET,hluti_Haus_OFFSET;uint32_t afbrigði_Background_Intelligent_Transfer_Service;uint16_t Stærð,forrit_Haus_breyta_stærð,forrit_Haus_COUNT,hluti_Haus_breyta_stærð,hluti_Haus_COUNT,hluti_heiti_tafla; } Haus_VALUE;
typedef struct {uint32_t TYPE_tegund,afbrigði_Background_Intelligent_Transfer_Service;uint64_t OFFSET_VALUE,slóð,물리주소,파일영역크기,기억영역크기,맞춤;} hluti_VALUE_32e9301f;
static unsigned char mynd[16384];
static int birta_færsla(const char *Heiti){
    size_t vara_COUNT;const unsigned char*원본자료=시언어출력(&vara_COUNT);if(vara_COUNT<sizeof(Haus_VALUE))return -1;
    Haus_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_tegund!=2||실행머리.vél_TYPE!=183||실행머리.forrit_Haus_breyta_stærð!=sizeof(hluti_VALUE_32e9301f)||!실행머리.forrit_Haus_COUNT||실행머리.forrit_Haus_COUNT>16||실행머리.forrit_Haus_OFFSET>vara_COUNT||실행머리.forrit_Haus_COUNT*sizeof(hluti_VALUE_32e9301f)>vara_COUNT-실행머리.forrit_Haus_OFFSET)return -1;
    실행머리.forrit_Haus_OFFSET=sizeof(실행머리);실행머리.hluti_Haus_OFFSET=실행머리.hluti_Haus_COUNT=실행머리.hluti_Haus_breyta_stærð=실행머리.hluti_heiti_tafla=0;memcpy(mynd,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.forrit_Haus_COUNT*sizeof(hluti_VALUE_32e9301f),Áfram_vara=4096;unsigned char síða_Listi[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.forrit_Haus_COUNT;순번++){
        hluti_VALUE_32e9301f gögn_staða;Haus_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&gögn_staða,원본자료+원본.forrit_Haus_OFFSET+순번*sizeof(gögn_staða),sizeof(gögn_staða));
        if(gögn_staða.OFFSET_VALUE>vara_COUNT||gögn_staða.파일영역크기>vara_COUNT-gögn_staða.OFFSET_VALUE||gögn_staða.파일영역크기>gögn_staða.기억영역크기)return -1;
        if(gögn_staða.TYPE_tegund==1){
            if((gögn_staða.afbrigði_Background_Intelligent_Transfer_Service&~7u)||!(gögn_staða.afbrigði_Background_Intelligent_Transfer_Service&4)||(gögn_staða.afbrigði_Background_Intelligent_Transfer_Service&3)==3||gögn_staða.slóð<0x02000000||gögn_staða.slóð>0x02c00000||gögn_staða.기억영역크기>0x02c00000-gögn_staða.slóð)return -1;
            if((gögn_staða.afbrigði_Background_Intelligent_Transfer_Service&1)&&실행머리.færsla_P>=gögn_staða.slóð&&실행머리.færsla_P-gögn_staða.slóð<gögn_staða.파일영역크기&&!(실행머리.færsla_P&3))진입점정상=1;
            size_t 선행값=gögn_staða.slóð&4095,바이트들=gögn_staða.파일영역크기?선행값+gögn_staða.파일영역크기:0;
            if(Áfram_vara>sizeof(mynd)||바이트들>sizeof(mynd)-Áfram_vara){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Áfram_vara+바이트들),(unsigned)sizeof(mynd));return -1;}
            if(바이트들)memcpy(mynd+Áfram_vara+선행값,원본자료+gögn_staða.OFFSET_VALUE,gögn_staða.파일영역크기);
            gögn_staða.slóð-=선행값;gögn_staða.물리주소=gögn_staða.slóð;gögn_staða.기억영역크기+=선행값;gögn_staða.파일영역크기=바이트들;gögn_staða.OFFSET_VALUE=Áfram_vara;gögn_staða.맞춤=4096;
            for(uint64_t síða_VALUE=gögn_staða.slóð;síða_VALUE<gögn_staða.slóð+gögn_staða.기억영역크기;síða_VALUE+=4096){unsigned LOOKUP_INDEX=(síða_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(síða_Listi)||síða_Listi[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}síða_Listi[LOOKUP_INDEX]=1;}
            Áfram_vara+=(바이트들+4095)&~(size_t)4095;
        }else if(gögn_staða.TYPE_tegund==4){if(gögn_staða.파일영역크기>4096-부가정보)return -1;memcpy(mynd+부가정보,원본자료+gögn_staða.OFFSET_VALUE,gögn_staða.파일영역크기);gögn_staða.OFFSET_VALUE=부가정보;부가정보+=gögn_staða.파일영역크기;}
        else if(gögn_staða.TYPE_tegund!=0&&gögn_staða.TYPE_tegund!=6&&gögn_staða.TYPE_tegund!=0x6474e551)return -1;
        memcpy(mynd+실행머리.forrit_Haus_OFFSET+순번*sizeof(gögn_staða),&gögn_staða,sizeof(gögn_staða));
    }
    if(!진입점정상)return -1;
    intptr_t skrá_hald=사용자호출(3,(uintptr_t)Heiti,577,0600,0,0,0);if(skrá_hald<0){printf("cc: cannot create output file, error %d\n",(int)skrá_hald);return -1;}
    intptr_t 쓴수=사용자호출(1,skrá_hald,(uintptr_t)mynd,Áfram_vara,0,0,0);사용자호출(4,skrá_hald,0,0,0,0,0);return 쓴수==(intptr_t)Áfram_vara?0:-1;
}
int Opna_notandi_forrit(int aðferð_MODE){
    char 입력결과[256],선택항목[256],úttak_54cd5e1d[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(aðferð_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(aðferð_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)úttak_54cd5e1d,sizeof(úttak_54cd5e1d),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,úttak_54cd5e1d)){printf("cc: input and output must differ\n");return 2;}
    TCCState*strengur_gögn=tcc_new();if(!strengur_gögn)return 1;
    tcc_undefine_symbol(strengur_gögn,"__linux__");tcc_undefine_symbol(strengur_gögn,"__linux");tcc_undefine_symbol(strengur_gögn,"linux");
    tcc_undefine_symbol(strengur_gögn,"__unix__");tcc_undefine_symbol(strengur_gögn,"__unix");tcc_undefine_symbol(strengur_gögn,"unix");
    tcc_undefine_symbol(strengur_gögn,"__STDC_HOSTED__");tcc_define_symbol(strengur_gögn,"__STDC_HOSTED__","0");tcc_define_symbol(strengur_gögn,"__JKOROS__","1");
    tcc_set_options(strengur_gögn,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(strengur_gögn,"/sdk/include");
    int 반환값=tcc_set_output_type(strengur_gögn,TCC_OUTPUT_EXE);
    if(!반환값){if(aðferð_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(strengur_gögn,원본자료):-1;}else 반환값=tcc_add_file(strengur_gögn,입력결과);}
    if(!반환값)반환값=tcc_add_file(strengur_gögn,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(strengur_gögn,"/sdk/lib/crt.o");
    if(!반환값&&aðferð_MODE)반환값=tcc_add_file(strengur_gögn,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(strengur_gögn,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(strengur_gögn,"/@cc-output");
    if(!반환값)반환값=birta_færsla(úttak_54cd5e1d);
    tcc_delete(strengur_gögn);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(aðferð_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",úttak_54cd5e1d);return 0;
}
