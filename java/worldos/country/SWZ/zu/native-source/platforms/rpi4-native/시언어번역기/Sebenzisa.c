#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char isivezi_inani[16];uint16_t thayipha_umunxa,umshini_thayipha;uint32_t 판번호;uint64_t okufakwayo_iphoyinti,i_app_Unhlokweni_I_ofisethi,isigaba_Unhlokweni_I_ofisethi;uint32_t 설정비트;uint16_t Ubungako,i_app_Unhlokweni_linganisa,프로그램머리개수,isigaba_Unhlokweni_linganisa,구역머리개수,isigaba_igama_ithebula; } Unhlokweni_inani;
typedef struct {uint32_t thayipha_umunxa,설정비트;uint64_t I_ofisethi_inani,ikheli,물리주소,파일영역크기,기억영역크기,맞춤;} isegimenti_inani;
static unsigned char isithombe[16384];
static int shicilela_okufakwayo(const char *Igama){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(Unhlokweni_inani))return -1;
    Unhlokweni_inani 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.thayipha_umunxa!=2||실행머리.umshini_thayipha!=183||실행머리.i_app_Unhlokweni_linganisa!=sizeof(isegimenti_inani)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.i_app_Unhlokweni_I_ofisethi>개수||실행머리.프로그램머리개수*sizeof(isegimenti_inani)>개수-실행머리.i_app_Unhlokweni_I_ofisethi)return -1;
    실행머리.i_app_Unhlokweni_I_ofisethi=sizeof(실행머리);실행머리.isigaba_Unhlokweni_I_ofisethi=실행머리.구역머리개수=실행머리.isigaba_Unhlokweni_linganisa=실행머리.isigaba_igama_ithebula=0;memcpy(isithombe,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(isegimenti_inani),다음=4096;unsigned char ikhasi_Uhlu[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        isegimenti_inani 자료위치;Unhlokweni_inani 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.i_app_Unhlokweni_I_ofisethi+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.I_ofisethi_inani>개수||자료위치.파일영역크기>개수-자료위치.I_ofisethi_inani||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.thayipha_umunxa==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.ikheli<0x02000000||자료위치.ikheli>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.ikheli)return -1;
            if((자료위치.설정비트&1)&&실행머리.okufakwayo_iphoyinti>=자료위치.ikheli&&실행머리.okufakwayo_iphoyinti-자료위치.ikheli<자료위치.파일영역크기&&!(실행머리.okufakwayo_iphoyinti&3))진입점정상=1;
            size_t 선행값=자료위치.ikheli&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(isithombe)||바이트들>sizeof(isithombe)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(isithombe));return -1;}
            if(바이트들)memcpy(isithombe+다음+선행값,원본자료+자료위치.I_ofisethi_inani,자료위치.파일영역크기);
            자료위치.ikheli-=선행값;자료위치.물리주소=자료위치.ikheli;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.I_ofisethi_inani=다음;자료위치.맞춤=4096;
            for(uint64_t ikhasi_inani=자료위치.ikheli;ikhasi_inani<자료위치.ikheli+자료위치.기억영역크기;ikhasi_inani+=4096){unsigned 색인=(ikhasi_inani-0x02000000)/4096;if(색인>=sizeof(ikhasi_Uhlu)||ikhasi_Uhlu[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}ikhasi_Uhlu[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.thayipha_umunxa==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(isithombe+부가정보,원본자료+자료위치.I_ofisethi_inani,자료위치.파일영역크기);자료위치.I_ofisethi_inani=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.thayipha_umunxa!=0&&자료위치.thayipha_umunxa!=6&&자료위치.thayipha_umunxa!=0x6474e551)return -1;
        memcpy(isithombe+실행머리.i_app_Unhlokweni_I_ofisethi+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t ifayela_isibambo=사용자호출(3,(uintptr_t)Igama,577,0600,0,0,0);if(ifayela_isibambo<0){printf("cc: cannot create output file, error %d\n",(int)ifayela_isibambo);return -1;}
    intptr_t 쓴수=사용자호출(1,ifayela_isibambo,(uintptr_t)isithombe,다음,0,0,0);사용자호출(4,ifayela_isibambo,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int qala_umsebenzisi_i_app(int indlela_inqubo){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(indlela_inqubo?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(indlela_inqubo?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*uchunge_imininingwane=tcc_new();if(!uchunge_imininingwane)return 1;
    tcc_undefine_symbol(uchunge_imininingwane,"__linux__");tcc_undefine_symbol(uchunge_imininingwane,"__linux");tcc_undefine_symbol(uchunge_imininingwane,"linux");
    tcc_undefine_symbol(uchunge_imininingwane,"__unix__");tcc_undefine_symbol(uchunge_imininingwane,"__unix");tcc_undefine_symbol(uchunge_imininingwane,"unix");
    tcc_undefine_symbol(uchunge_imininingwane,"__STDC_HOSTED__");tcc_define_symbol(uchunge_imininingwane,"__STDC_HOSTED__","0");tcc_define_symbol(uchunge_imininingwane,"__JKOROS__","1");
    tcc_set_options(uchunge_imininingwane,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(uchunge_imininingwane,"/sdk/include");
    int 반환값=tcc_set_output_type(uchunge_imininingwane,TCC_OUTPUT_EXE);
    if(!반환값){if(indlela_inqubo){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(uchunge_imininingwane,원본자료):-1;}else 반환값=tcc_add_file(uchunge_imininingwane,입력결과);}
    if(!반환값)반환값=tcc_add_file(uchunge_imininingwane,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(uchunge_imininingwane,"/sdk/lib/crt.o");
    if(!반환값&&indlela_inqubo)반환값=tcc_add_file(uchunge_imininingwane,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(uchunge_imininingwane,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(uchunge_imininingwane,"/@cc-output");
    if(!반환값)반환값=shicilela_okufakwayo(출력결과);
    tcc_delete(uchunge_imininingwane);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(indlela_inqubo?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
