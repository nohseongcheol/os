#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char sešupi_boleng[16];uint16_t thaepa_legoro,motšhene_thaepa;uint32_t 판번호;uint64_t go_tsenya_tshedimošo_ntlha,tirišo_Hlogo_E_Šetšego,karolo_Hlogo_E_Šetšego;uint32_t 설정비트;uint16_t Bogolo,tirišo_Hlogo_bogolo,프로그램머리개수,karolo_Hlogo_bogolo,구역머리개수,karolo_leina_tafola; } Hlogo_boleng;
typedef struct {uint32_t thaepa_legoro,설정비트;uint64_t E_Šetšego_boleng,atrese,물리주소,파일영역크기,기억영역크기,맞춤;} karolwana_boleng;
static unsigned char seswantšho[16384];
static int tšweletša_go_tsenya_tshedimošo(const char *Leina){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(Hlogo_boleng))return -1;
    Hlogo_boleng 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.thaepa_legoro!=2||실행머리.motšhene_thaepa!=183||실행머리.tirišo_Hlogo_bogolo!=sizeof(karolwana_boleng)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.tirišo_Hlogo_E_Šetšego>개수||실행머리.프로그램머리개수*sizeof(karolwana_boleng)>개수-실행머리.tirišo_Hlogo_E_Šetšego)return -1;
    실행머리.tirišo_Hlogo_E_Šetšego=sizeof(실행머리);실행머리.karolo_Hlogo_E_Šetšego=실행머리.구역머리개수=실행머리.karolo_Hlogo_bogolo=실행머리.karolo_leina_tafola=0;memcpy(seswantšho,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(karolwana_boleng),다음=4096;unsigned char letlakala_Lenaneo[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        karolwana_boleng 자료위치;Hlogo_boleng 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.tirišo_Hlogo_E_Šetšego+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.E_Šetšego_boleng>개수||자료위치.파일영역크기>개수-자료위치.E_Šetšego_boleng||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.thaepa_legoro==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.atrese<0x02000000||자료위치.atrese>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.atrese)return -1;
            if((자료위치.설정비트&1)&&실행머리.go_tsenya_tshedimošo_ntlha>=자료위치.atrese&&실행머리.go_tsenya_tshedimošo_ntlha-자료위치.atrese<자료위치.파일영역크기&&!(실행머리.go_tsenya_tshedimošo_ntlha&3))진입점정상=1;
            size_t 선행값=자료위치.atrese&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(seswantšho)||바이트들>sizeof(seswantšho)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(seswantšho));return -1;}
            if(바이트들)memcpy(seswantšho+다음+선행값,원본자료+자료위치.E_Šetšego_boleng,자료위치.파일영역크기);
            자료위치.atrese-=선행값;자료위치.물리주소=자료위치.atrese;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.E_Šetšego_boleng=다음;자료위치.맞춤=4096;
            for(uint64_t letlakala_boleng=자료위치.atrese;letlakala_boleng<자료위치.atrese+자료위치.기억영역크기;letlakala_boleng+=4096){unsigned 색인=(letlakala_boleng-0x02000000)/4096;if(색인>=sizeof(letlakala_Lenaneo)||letlakala_Lenaneo[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}letlakala_Lenaneo[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.thaepa_legoro==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(seswantšho+부가정보,원본자료+자료위치.E_Šetšego_boleng,자료위치.파일영역크기);자료위치.E_Šetšego_boleng=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.thaepa_legoro!=0&&자료위치.thaepa_legoro!=6&&자료위치.thaepa_legoro!=0x6474e551)return -1;
        memcpy(seswantšho+실행머리.tirišo_Hlogo_E_Šetšego+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t faele_tshwaro=사용자호출(3,(uintptr_t)Leina,577,0600,0,0,0);if(faele_tshwaro<0){printf("cc: cannot create output file, error %d\n",(int)faele_tshwaro);return -1;}
    intptr_t 쓴수=사용자호출(1,faele_tshwaro,(uintptr_t)seswantšho,다음,0,0,0);사용자호출(4,faele_tshwaro,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int Thomišo_mošomiši_tirišo(int mokgwa_mokgwa){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(mokgwa_mokgwa?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(mokgwa_mokgwa?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*molokoloko_data=tcc_new();if(!molokoloko_data)return 1;
    tcc_undefine_symbol(molokoloko_data,"__linux__");tcc_undefine_symbol(molokoloko_data,"__linux");tcc_undefine_symbol(molokoloko_data,"linux");
    tcc_undefine_symbol(molokoloko_data,"__unix__");tcc_undefine_symbol(molokoloko_data,"__unix");tcc_undefine_symbol(molokoloko_data,"unix");
    tcc_undefine_symbol(molokoloko_data,"__STDC_HOSTED__");tcc_define_symbol(molokoloko_data,"__STDC_HOSTED__","0");tcc_define_symbol(molokoloko_data,"__JKOROS__","1");
    tcc_set_options(molokoloko_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(molokoloko_data,"/sdk/include");
    int 반환값=tcc_set_output_type(molokoloko_data,TCC_OUTPUT_EXE);
    if(!반환값){if(mokgwa_mokgwa){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(molokoloko_data,원본자료):-1;}else 반환값=tcc_add_file(molokoloko_data,입력결과);}
    if(!반환값)반환값=tcc_add_file(molokoloko_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(molokoloko_data,"/sdk/lib/crt.o");
    if(!반환값&&mokgwa_mokgwa)반환값=tcc_add_file(molokoloko_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(molokoloko_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(molokoloko_data,"/@cc-output");
    if(!반환값)반환값=tšweletša_go_tsenya_tshedimošo(출력결과);
    tcc_delete(molokoloko_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(mokgwa_mokgwa?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
