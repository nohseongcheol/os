#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char isalathisi_ixabiso[16];uint16_t uhlobo_udidi,umatshini_uhlobo;uint32_t 판번호;uint64_t ufako_nkcukacha_inqaku,inkqubo_Iheda_Ukulinganisa,icandelo_Iheda_Ukulinganisa;uint32_t 설정비트;uint16_t Ubukhulu,inkqubo_Iheda_isayizi,프로그램머리개수,icandelo_Iheda_isayizi,구역머리개수,icandelo_igama_itheyibhile; } Iheda_ixabiso;
typedef struct {uint32_t uhlobo_udidi,설정비트;uint64_t Ukulinganisa_ixabiso,idilesi,물리주소,파일영역크기,기억영역크기,맞춤;} isahlulo_ixabiso;
static unsigned char umfanekiso[16384];
static int papasha_ufako_nkcukacha(const char *Igama){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(Iheda_ixabiso))return -1;
    Iheda_ixabiso 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.uhlobo_udidi!=2||실행머리.umatshini_uhlobo!=183||실행머리.inkqubo_Iheda_isayizi!=sizeof(isahlulo_ixabiso)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.inkqubo_Iheda_Ukulinganisa>개수||실행머리.프로그램머리개수*sizeof(isahlulo_ixabiso)>개수-실행머리.inkqubo_Iheda_Ukulinganisa)return -1;
    실행머리.inkqubo_Iheda_Ukulinganisa=sizeof(실행머리);실행머리.icandelo_Iheda_Ukulinganisa=실행머리.구역머리개수=실행머리.icandelo_Iheda_isayizi=실행머리.icandelo_igama_itheyibhile=0;memcpy(umfanekiso,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(isahlulo_ixabiso),다음=4096;unsigned char ikhasi_uludwe[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        isahlulo_ixabiso 자료위치;Iheda_ixabiso 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.inkqubo_Iheda_Ukulinganisa+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Ukulinganisa_ixabiso>개수||자료위치.파일영역크기>개수-자료위치.Ukulinganisa_ixabiso||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.uhlobo_udidi==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.idilesi<0x02000000||자료위치.idilesi>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.idilesi)return -1;
            if((자료위치.설정비트&1)&&실행머리.ufako_nkcukacha_inqaku>=자료위치.idilesi&&실행머리.ufako_nkcukacha_inqaku-자료위치.idilesi<자료위치.파일영역크기&&!(실행머리.ufako_nkcukacha_inqaku&3))진입점정상=1;
            size_t 선행값=자료위치.idilesi&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(umfanekiso)||바이트들>sizeof(umfanekiso)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(umfanekiso));return -1;}
            if(바이트들)memcpy(umfanekiso+다음+선행값,원본자료+자료위치.Ukulinganisa_ixabiso,자료위치.파일영역크기);
            자료위치.idilesi-=선행값;자료위치.물리주소=자료위치.idilesi;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Ukulinganisa_ixabiso=다음;자료위치.맞춤=4096;
            for(uint64_t ikhasi_ixabiso=자료위치.idilesi;ikhasi_ixabiso<자료위치.idilesi+자료위치.기억영역크기;ikhasi_ixabiso+=4096){unsigned 색인=(ikhasi_ixabiso-0x02000000)/4096;if(색인>=sizeof(ikhasi_uludwe)||ikhasi_uludwe[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}ikhasi_uludwe[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.uhlobo_udidi==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(umfanekiso+부가정보,원본자료+자료위치.Ukulinganisa_ixabiso,자료위치.파일영역크기);자료위치.Ukulinganisa_ixabiso=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.uhlobo_udidi!=0&&자료위치.uhlobo_udidi!=6&&자료위치.uhlobo_udidi!=0x6474e551)return -1;
        memcpy(umfanekiso+실행머리.inkqubo_Iheda_Ukulinganisa+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t ifayile_isibambi=사용자호출(3,(uintptr_t)Igama,577,0600,0,0,0);if(ifayile_isibambi<0){printf("cc: cannot create output file, error %d\n",(int)ifayile_isibambi);return -1;}
    intptr_t 쓴수=사용자호출(1,ifayile_isibambi,(uintptr_t)umfanekiso,다음,0,0,0);사용자호출(4,ifayile_isibambi,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int qala_umsebenzisi_inkqubo(int imethodi_imo){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(imethodi_imo?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(imethodi_imo?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*uluhlu_lweekharektha_iingcombolo=tcc_new();if(!uluhlu_lweekharektha_iingcombolo)return 1;
    tcc_undefine_symbol(uluhlu_lweekharektha_iingcombolo,"__linux__");tcc_undefine_symbol(uluhlu_lweekharektha_iingcombolo,"__linux");tcc_undefine_symbol(uluhlu_lweekharektha_iingcombolo,"linux");
    tcc_undefine_symbol(uluhlu_lweekharektha_iingcombolo,"__unix__");tcc_undefine_symbol(uluhlu_lweekharektha_iingcombolo,"__unix");tcc_undefine_symbol(uluhlu_lweekharektha_iingcombolo,"unix");
    tcc_undefine_symbol(uluhlu_lweekharektha_iingcombolo,"__STDC_HOSTED__");tcc_define_symbol(uluhlu_lweekharektha_iingcombolo,"__STDC_HOSTED__","0");tcc_define_symbol(uluhlu_lweekharektha_iingcombolo,"__JKOROS__","1");
    tcc_set_options(uluhlu_lweekharektha_iingcombolo,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(uluhlu_lweekharektha_iingcombolo,"/sdk/include");
    int 반환값=tcc_set_output_type(uluhlu_lweekharektha_iingcombolo,TCC_OUTPUT_EXE);
    if(!반환값){if(imethodi_imo){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(uluhlu_lweekharektha_iingcombolo,원본자료):-1;}else 반환값=tcc_add_file(uluhlu_lweekharektha_iingcombolo,입력결과);}
    if(!반환값)반환값=tcc_add_file(uluhlu_lweekharektha_iingcombolo,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(uluhlu_lweekharektha_iingcombolo,"/sdk/lib/crt.o");
    if(!반환값&&imethodi_imo)반환값=tcc_add_file(uluhlu_lweekharektha_iingcombolo,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(uluhlu_lweekharektha_iingcombolo,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(uluhlu_lweekharektha_iingcombolo,"/@cc-output");
    if(!반환값)반환값=papasha_ufako_nkcukacha(출력결과);
    tcc_delete(uluhlu_lweekharektha_iingcombolo);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(imethodi_imo?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
