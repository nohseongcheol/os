#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char aithnichear_VALUE[16];uint16_t TYPE_roinn_seòrsa,inneal_TYPE;uint32_t 판번호;uint64_t cur_a_steach_puing,ap_bann_cinn_OFFSET,earrann_bann_cinn_OFFSET;uint32_t 설정비트;uint16_t atharraich_am_meud,ap_bann_cinn_atharraich_am_meud,ap_bann_cinn_COUNT,earrann_bann_cinn_atharraich_am_meud,earrann_bann_cinn_COUNT,earrann_ainm_clàr; } bann_cinn_VALUE;
typedef struct {uint32_t TYPE_roinn_seòrsa,설정비트;uint64_t OFFSET_VALUE,ADDRESS,물리주소,파일영역크기,기억영역크기,맞춤;} gearradh_VALUE;
static unsigned char IMAGE[16384];
static int foillsich_cur_a_steach(const char *Ainm){
    size_t nì_COUNT;const unsigned char*원본자료=시언어출력(&nì_COUNT);if(nì_COUNT<sizeof(bann_cinn_VALUE))return -1;
    bann_cinn_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_roinn_seòrsa!=2||실행머리.inneal_TYPE!=183||실행머리.ap_bann_cinn_atharraich_am_meud!=sizeof(gearradh_VALUE)||!실행머리.ap_bann_cinn_COUNT||실행머리.ap_bann_cinn_COUNT>16||실행머리.ap_bann_cinn_OFFSET>nì_COUNT||실행머리.ap_bann_cinn_COUNT*sizeof(gearradh_VALUE)>nì_COUNT-실행머리.ap_bann_cinn_OFFSET)return -1;
    실행머리.ap_bann_cinn_OFFSET=sizeof(실행머리);실행머리.earrann_bann_cinn_OFFSET=실행머리.earrann_bann_cinn_COUNT=실행머리.earrann_bann_cinn_atharraich_am_meud=실행머리.earrann_ainm_clàr=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.ap_bann_cinn_COUNT*sizeof(gearradh_VALUE),air_adhart_nì=4096;unsigned char duilleag_Liosta[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.ap_bann_cinn_COUNT;순번++){
        gearradh_VALUE dàta_suidhich;bann_cinn_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&dàta_suidhich,원본자료+원본.ap_bann_cinn_OFFSET+순번*sizeof(dàta_suidhich),sizeof(dàta_suidhich));
        if(dàta_suidhich.OFFSET_VALUE>nì_COUNT||dàta_suidhich.파일영역크기>nì_COUNT-dàta_suidhich.OFFSET_VALUE||dàta_suidhich.파일영역크기>dàta_suidhich.기억영역크기)return -1;
        if(dàta_suidhich.TYPE_roinn_seòrsa==1){
            if((dàta_suidhich.설정비트&~7u)||!(dàta_suidhich.설정비트&4)||(dàta_suidhich.설정비트&3)==3||dàta_suidhich.ADDRESS<0x02000000||dàta_suidhich.ADDRESS>0x02c00000||dàta_suidhich.기억영역크기>0x02c00000-dàta_suidhich.ADDRESS)return -1;
            if((dàta_suidhich.설정비트&1)&&실행머리.cur_a_steach_puing>=dàta_suidhich.ADDRESS&&실행머리.cur_a_steach_puing-dàta_suidhich.ADDRESS<dàta_suidhich.파일영역크기&&!(실행머리.cur_a_steach_puing&3))진입점정상=1;
            size_t 선행값=dàta_suidhich.ADDRESS&4095,바이트들=dàta_suidhich.파일영역크기?선행값+dàta_suidhich.파일영역크기:0;
            if(air_adhart_nì>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-air_adhart_nì){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(air_adhart_nì+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+air_adhart_nì+선행값,원본자료+dàta_suidhich.OFFSET_VALUE,dàta_suidhich.파일영역크기);
            dàta_suidhich.ADDRESS-=선행값;dàta_suidhich.물리주소=dàta_suidhich.ADDRESS;dàta_suidhich.기억영역크기+=선행값;dàta_suidhich.파일영역크기=바이트들;dàta_suidhich.OFFSET_VALUE=air_adhart_nì;dàta_suidhich.맞춤=4096;
            for(uint64_t duilleag_VALUE=dàta_suidhich.ADDRESS;duilleag_VALUE<dàta_suidhich.ADDRESS+dàta_suidhich.기억영역크기;duilleag_VALUE+=4096){unsigned LOOKUP_INDEX=(duilleag_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(duilleag_Liosta)||duilleag_Liosta[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}duilleag_Liosta[LOOKUP_INDEX]=1;}
            air_adhart_nì+=(바이트들+4095)&~(size_t)4095;
        }else if(dàta_suidhich.TYPE_roinn_seòrsa==4){if(dàta_suidhich.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+dàta_suidhich.OFFSET_VALUE,dàta_suidhich.파일영역크기);dàta_suidhich.OFFSET_VALUE=부가정보;부가정보+=dàta_suidhich.파일영역크기;}
        else if(dàta_suidhich.TYPE_roinn_seòrsa!=0&&dàta_suidhich.TYPE_roinn_seòrsa!=6&&dàta_suidhich.TYPE_roinn_seòrsa!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.ap_bann_cinn_OFFSET+순번*sizeof(dàta_suidhich),&dàta_suidhich,sizeof(dàta_suidhich));
    }
    if(!진입점정상)return -1;
    intptr_t faidhle_làmhrachan=사용자호출(3,(uintptr_t)Ainm,577,0600,0,0,0);if(faidhle_làmhrachan<0){printf("cc: cannot create output file, error %d\n",(int)faidhle_làmhrachan);return -1;}
    intptr_t 쓴수=사용자호출(1,faidhle_làmhrachan,(uintptr_t)IMAGE,air_adhart_nì,0,0,0);사용자호출(4,faidhle_làmhrachan,0,0,0,0,0);return 쓴수==(intptr_t)air_adhart_nì?0:-1;
}
int Start_cleachdaiche_ap(int dòigh_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(dòigh_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(dòigh_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*sreang_dàta=tcc_new();if(!sreang_dàta)return 1;
    tcc_undefine_symbol(sreang_dàta,"__linux__");tcc_undefine_symbol(sreang_dàta,"__linux");tcc_undefine_symbol(sreang_dàta,"linux");
    tcc_undefine_symbol(sreang_dàta,"__unix__");tcc_undefine_symbol(sreang_dàta,"__unix");tcc_undefine_symbol(sreang_dàta,"unix");
    tcc_undefine_symbol(sreang_dàta,"__STDC_HOSTED__");tcc_define_symbol(sreang_dàta,"__STDC_HOSTED__","0");tcc_define_symbol(sreang_dàta,"__JKOROS__","1");
    tcc_set_options(sreang_dàta,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(sreang_dàta,"/sdk/include");
    int 반환값=tcc_set_output_type(sreang_dàta,TCC_OUTPUT_EXE);
    if(!반환값){if(dòigh_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(sreang_dàta,원본자료):-1;}else 반환값=tcc_add_file(sreang_dàta,입력결과);}
    if(!반환값)반환값=tcc_add_file(sreang_dàta,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(sreang_dàta,"/sdk/lib/crt.o");
    if(!반환값&&dòigh_MODE)반환값=tcc_add_file(sreang_dàta,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(sreang_dàta,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(sreang_dàta,"/@cc-output");
    if(!반환값)반환값=foillsich_cur_a_steach(출력결과);
    tcc_delete(sreang_dàta);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(dòigh_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
