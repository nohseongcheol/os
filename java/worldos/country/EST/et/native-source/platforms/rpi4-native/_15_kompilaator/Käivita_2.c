#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *_15_toodang(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikaator_VALUE[16];uint16_t TYPE_ala,arvuti_TYPE;uint32_t versiooninumber;uint64_t kirje_p,programm_Päis_nihe,jaotise_päis_nihe;uint32_t konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus;uint16_t Suurus,programm_Päis_suurust_muutma,programm_Päis_COUNT,jaotise_päis_suurust_muutma,jaotise_päis_COUNT,jaotis_nimetus_tabel; } Päis_VALUE;
typedef struct {uint32_t TYPE_ala,konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus;uint64_t nihe_VALUE,ADDRESS,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char pilt[16384];
static int avaldama_kirje(const char *Nimi_2){
    size_t kaup_COUNT;const unsigned char*원본자료=_15_toodang(&kaup_COUNT);if(kaup_COUNT<sizeof(Päis_VALUE))return -1;
    Päis_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_ala!=2||실행머리.arvuti_TYPE!=183||실행머리.programm_Päis_suurust_muutma!=sizeof(segment_VALUE)||!실행머리.programm_Päis_COUNT||실행머리.programm_Päis_COUNT>16||실행머리.programm_Päis_nihe>kaup_COUNT||실행머리.programm_Päis_COUNT*sizeof(segment_VALUE)>kaup_COUNT-실행머리.programm_Päis_nihe)return -1;
    실행머리.programm_Päis_nihe=sizeof(실행머리);실행머리.jaotise_päis_nihe=실행머리.jaotise_päis_COUNT=실행머리.jaotise_päis_suurust_muutma=실행머리.jaotis_nimetus_tabel=0;memcpy(pilt,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.programm_Päis_COUNT*sizeof(segment_VALUE),Edasi_kaup=4096;unsigned char leht_Loend[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.programm_Päis_COUNT;순번++){
        segment_VALUE andmed_ametikoht;Päis_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&andmed_ametikoht,원본자료+원본.programm_Päis_nihe+순번*sizeof(andmed_ametikoht),sizeof(andmed_ametikoht));
        if(andmed_ametikoht.nihe_VALUE>kaup_COUNT||andmed_ametikoht.파일영역크기>kaup_COUNT-andmed_ametikoht.nihe_VALUE||andmed_ametikoht.파일영역크기>andmed_ametikoht.기억영역크기)return -1;
        if(andmed_ametikoht.TYPE_ala==1){
            if((andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&~7u)||!(andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&4)||(andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&3)==3||andmed_ametikoht.ADDRESS<0x02000000||andmed_ametikoht.ADDRESS>0x02c00000||andmed_ametikoht.기억영역크기>0x02c00000-andmed_ametikoht.ADDRESS)return -1;
            if((andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&1)&&실행머리.kirje_p>=andmed_ametikoht.ADDRESS&&실행머리.kirje_p-andmed_ametikoht.ADDRESS<andmed_ametikoht.파일영역크기&&!(실행머리.kirje_p&3))진입점정상=1;
            size_t 선행값=andmed_ametikoht.ADDRESS&4095,바이트들=andmed_ametikoht.파일영역크기?선행값+andmed_ametikoht.파일영역크기:0;
            if(Edasi_kaup>sizeof(pilt)||바이트들>sizeof(pilt)-Edasi_kaup){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Edasi_kaup+바이트들),(unsigned)sizeof(pilt));return -1;}
            if(바이트들)memcpy(pilt+Edasi_kaup+선행값,원본자료+andmed_ametikoht.nihe_VALUE,andmed_ametikoht.파일영역크기);
            andmed_ametikoht.ADDRESS-=선행값;andmed_ametikoht.물리주소=andmed_ametikoht.ADDRESS;andmed_ametikoht.기억영역크기+=선행값;andmed_ametikoht.파일영역크기=바이트들;andmed_ametikoht.nihe_VALUE=Edasi_kaup;andmed_ametikoht.맞춤=4096;
            for(uint64_t leht_VALUE=andmed_ametikoht.ADDRESS;leht_VALUE<andmed_ametikoht.ADDRESS+andmed_ametikoht.기억영역크기;leht_VALUE+=4096){unsigned LOOKUP_INDEX=(leht_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(leht_Loend)||leht_Loend[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}leht_Loend[LOOKUP_INDEX]=1;}
            Edasi_kaup+=(바이트들+4095)&~(size_t)4095;
        }else if(andmed_ametikoht.TYPE_ala==4){if(andmed_ametikoht.파일영역크기>4096-부가정보)return -1;memcpy(pilt+부가정보,원본자료+andmed_ametikoht.nihe_VALUE,andmed_ametikoht.파일영역크기);andmed_ametikoht.nihe_VALUE=부가정보;부가정보+=andmed_ametikoht.파일영역크기;}
        else if(andmed_ametikoht.TYPE_ala!=0&&andmed_ametikoht.TYPE_ala!=6&&andmed_ametikoht.TYPE_ala!=0x6474e551)return -1;
        memcpy(pilt+실행머리.programm_Päis_nihe+순번*sizeof(andmed_ametikoht),&andmed_ametikoht,sizeof(andmed_ametikoht));
    }
    if(!진입점정상)return -1;
    intptr_t Fail_pide=사용자호출(3,(uintptr_t)Nimi_2,577,0600,0,0,0);if(Fail_pide<0){printf("cc: cannot create output file, error %d\n",(int)Fail_pide);return -1;}
    intptr_t 쓴수=사용자호출(1,Fail_pide,(uintptr_t)pilt,Edasi_kaup,0,0,0);사용자호출(4,Fail_pide,0,0,0,0,0);return 쓴수==(intptr_t)Edasi_kaup?0:-1;
}
int START_kasutaja_programm(int meetod_MODE){
    char 입력결과[256],선택항목[256],toodang[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(meetod_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(meetod_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)toodang,sizeof(toodang),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,toodang)){printf("cc: input and output must differ\n");return 2;}
    TCCState*string_andmed=tcc_new();if(!string_andmed)return 1;
    tcc_undefine_symbol(string_andmed,"__linux__");tcc_undefine_symbol(string_andmed,"__linux");tcc_undefine_symbol(string_andmed,"linux");
    tcc_undefine_symbol(string_andmed,"__unix__");tcc_undefine_symbol(string_andmed,"__unix");tcc_undefine_symbol(string_andmed,"unix");
    tcc_undefine_symbol(string_andmed,"__STDC_HOSTED__");tcc_define_symbol(string_andmed,"__STDC_HOSTED__","0");tcc_define_symbol(string_andmed,"__JKOROS__","1");
    tcc_set_options(string_andmed,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(string_andmed,"/sdk/include");
    int 반환값=tcc_set_output_type(string_andmed,TCC_OUTPUT_EXE);
    if(!반환값){if(meetod_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(string_andmed,원본자료):-1;}else 반환값=tcc_add_file(string_andmed,입력결과);}
    if(!반환값)반환값=tcc_add_file(string_andmed,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(string_andmed,"/sdk/lib/crt.o");
    if(!반환값&&meetod_MODE)반환값=tcc_add_file(string_andmed,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(string_andmed,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(string_andmed,"/@cc-output");
    if(!반환값)반환값=avaldama_kirje(toodang);
    tcc_delete(string_andmed);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(meetod_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",toodang);return 0;
}
