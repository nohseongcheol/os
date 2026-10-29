#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char Àfidámọ̀_iye[16];uint16_t irú_ìsọ̀rí,maṣíìnì_irú;uint32_t 판번호;uint64_t ìgbéwọlé_kókó,àtòjọ_ètò_àkọlé_Ìtayọ,abala_àkọlé_Ìtayọ;uint32_t 설정비트;uint16_t Ìwọ̀n,àtòjọ_ètò_àkọlé_ìwọn,프로그램머리개수,abala_àkọlé_ìwọn,구역머리개수,abala_orúkọ_atọ́ka; } àkọlé_iye;
typedef struct {uint32_t irú_ìsọ̀rí,설정비트;uint64_t Ìtayọ_iye,àdírẹ́ẹ̀sì,물리주소,파일영역크기,기억영역크기,맞춤;} abala_iye_32e9301f;
static unsigned char àwòrán[16384];
static int gbéjáde_ìgbéwọlé(const char *Orúkọ){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(àkọlé_iye))return -1;
    àkọlé_iye 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.irú_ìsọ̀rí!=2||실행머리.maṣíìnì_irú!=183||실행머리.àtòjọ_ètò_àkọlé_ìwọn!=sizeof(abala_iye_32e9301f)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.àtòjọ_ètò_àkọlé_Ìtayọ>개수||실행머리.프로그램머리개수*sizeof(abala_iye_32e9301f)>개수-실행머리.àtòjọ_ètò_àkọlé_Ìtayọ)return -1;
    실행머리.àtòjọ_ètò_àkọlé_Ìtayọ=sizeof(실행머리);실행머리.abala_àkọlé_Ìtayọ=실행머리.구역머리개수=실행머리.abala_àkọlé_ìwọn=실행머리.abala_orúkọ_atọ́ka=0;memcpy(àwòrán,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(abala_iye_32e9301f),다음=4096;unsigned char ojú_ìwé_Àtòkọ[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        abala_iye_32e9301f 자료위치;àkọlé_iye 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.àtòjọ_ètò_àkọlé_Ìtayọ+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Ìtayọ_iye>개수||자료위치.파일영역크기>개수-자료위치.Ìtayọ_iye||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.irú_ìsọ̀rí==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.àdírẹ́ẹ̀sì<0x02000000||자료위치.àdírẹ́ẹ̀sì>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.àdírẹ́ẹ̀sì)return -1;
            if((자료위치.설정비트&1)&&실행머리.ìgbéwọlé_kókó>=자료위치.àdírẹ́ẹ̀sì&&실행머리.ìgbéwọlé_kókó-자료위치.àdírẹ́ẹ̀sì<자료위치.파일영역크기&&!(실행머리.ìgbéwọlé_kókó&3))진입점정상=1;
            size_t 선행값=자료위치.àdírẹ́ẹ̀sì&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(àwòrán)||바이트들>sizeof(àwòrán)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(àwòrán));return -1;}
            if(바이트들)memcpy(àwòrán+다음+선행값,원본자료+자료위치.Ìtayọ_iye,자료위치.파일영역크기);
            자료위치.àdírẹ́ẹ̀sì-=선행값;자료위치.물리주소=자료위치.àdírẹ́ẹ̀sì;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Ìtayọ_iye=다음;자료위치.맞춤=4096;
            for(uint64_t ojú_ìwé_iye=자료위치.àdírẹ́ẹ̀sì;ojú_ìwé_iye<자료위치.àdírẹ́ẹ̀sì+자료위치.기억영역크기;ojú_ìwé_iye+=4096){unsigned 색인=(ojú_ìwé_iye-0x02000000)/4096;if(색인>=sizeof(ojú_ìwé_Àtòkọ)||ojú_ìwé_Àtòkọ[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}ojú_ìwé_Àtòkọ[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.irú_ìsọ̀rí==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(àwòrán+부가정보,원본자료+자료위치.Ìtayọ_iye,자료위치.파일영역크기);자료위치.Ìtayọ_iye=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.irú_ìsọ̀rí!=0&&자료위치.irú_ìsọ̀rí!=6&&자료위치.irú_ìsọ̀rí!=0x6474e551)return -1;
        memcpy(àwòrán+실행머리.àtòjọ_ètò_àkọlé_Ìtayọ+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t fáìlì_èkù=사용자호출(3,(uintptr_t)Orúkọ,577,0600,0,0,0);if(fáìlì_èkù<0){printf("cc: cannot create output file, error %d\n",(int)fáìlì_èkù);return -1;}
    intptr_t 쓴수=사용자호출(1,fáìlì_èkù,(uintptr_t)àwòrán,다음,0,0,0);사용자호출(4,fáìlì_èkù,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò(int ìlànà_móòdù){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(ìlànà_móòdù?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(ìlànà_móòdù?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*fọ́nrán_détà=tcc_new();if(!fọ́nrán_détà)return 1;
    tcc_undefine_symbol(fọ́nrán_détà,"__linux__");tcc_undefine_symbol(fọ́nrán_détà,"__linux");tcc_undefine_symbol(fọ́nrán_détà,"linux");
    tcc_undefine_symbol(fọ́nrán_détà,"__unix__");tcc_undefine_symbol(fọ́nrán_détà,"__unix");tcc_undefine_symbol(fọ́nrán_détà,"unix");
    tcc_undefine_symbol(fọ́nrán_détà,"__STDC_HOSTED__");tcc_define_symbol(fọ́nrán_détà,"__STDC_HOSTED__","0");tcc_define_symbol(fọ́nrán_détà,"__JKOROS__","1");
    tcc_set_options(fọ́nrán_détà,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(fọ́nrán_détà,"/sdk/include");
    int 반환값=tcc_set_output_type(fọ́nrán_détà,TCC_OUTPUT_EXE);
    if(!반환값){if(ìlànà_móòdù){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(fọ́nrán_détà,원본자료):-1;}else 반환값=tcc_add_file(fọ́nrán_détà,입력결과);}
    if(!반환값)반환값=tcc_add_file(fọ́nrán_détà,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(fọ́nrán_détà,"/sdk/lib/crt.o");
    if(!반환값&&ìlànà_móòdù)반환값=tcc_add_file(fọ́nrán_détà,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(fọ́nrán_détà,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(fọ́nrán_détà,"/@cc-output");
    if(!반환값)반환값=gbéjáde_ìgbéwọlé(출력결과);
    tcc_delete(fọ́nrán_détà);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(ìlànà_móòdù?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
