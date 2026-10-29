#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikues_VALUE[16];uint16_t TYPE_kategori,makinë_TYPE;uint32_t 판번호;uint64_t futje_p,program_Kreu_OFFSET,seksion_Kreu_OFFSET;uint32_t konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond;uint16_t Madhësi,program_Kreu_ndryshoj_përmasat,program_Kreu_COUNT,seksion_Kreu_ndryshoj_përmasat,seksion_Kreu_COUNT,seksion_emër_tabelë; } Kreu_VALUE;
typedef struct {uint32_t TYPE_kategori,konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond;uint64_t OFFSET_VALUE,email,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char IMAGE[16384];
static int publikoj_futje(const char *Emër){
    size_t njësi_COUNT;const unsigned char*원본자료=시언어출력(&njësi_COUNT);if(njësi_COUNT<sizeof(Kreu_VALUE))return -1;
    Kreu_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_kategori!=2||실행머리.makinë_TYPE!=183||실행머리.program_Kreu_ndryshoj_përmasat!=sizeof(segment_VALUE)||!실행머리.program_Kreu_COUNT||실행머리.program_Kreu_COUNT>16||실행머리.program_Kreu_OFFSET>njësi_COUNT||실행머리.program_Kreu_COUNT*sizeof(segment_VALUE)>njësi_COUNT-실행머리.program_Kreu_OFFSET)return -1;
    실행머리.program_Kreu_OFFSET=sizeof(실행머리);실행머리.seksion_Kreu_OFFSET=실행머리.seksion_Kreu_COUNT=실행머리.seksion_Kreu_ndryshoj_përmasat=실행머리.seksion_emër_tabelë=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.program_Kreu_COUNT*sizeof(segment_VALUE),Tjetër_njësi=4096;unsigned char faqe_Listë[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.program_Kreu_COUNT;순번++){
        segment_VALUE të_dhëna_pozicioni;Kreu_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&të_dhëna_pozicioni,원본자료+원본.program_Kreu_OFFSET+순번*sizeof(të_dhëna_pozicioni),sizeof(të_dhëna_pozicioni));
        if(të_dhëna_pozicioni.OFFSET_VALUE>njësi_COUNT||të_dhëna_pozicioni.파일영역크기>njësi_COUNT-të_dhëna_pozicioni.OFFSET_VALUE||të_dhëna_pozicioni.파일영역크기>të_dhëna_pozicioni.기억영역크기)return -1;
        if(të_dhëna_pozicioni.TYPE_kategori==1){
            if((të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&~7u)||!(të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&4)||(të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&3)==3||të_dhëna_pozicioni.email<0x02000000||të_dhëna_pozicioni.email>0x02c00000||të_dhëna_pozicioni.기억영역크기>0x02c00000-të_dhëna_pozicioni.email)return -1;
            if((të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&1)&&실행머리.futje_p>=të_dhëna_pozicioni.email&&실행머리.futje_p-të_dhëna_pozicioni.email<të_dhëna_pozicioni.파일영역크기&&!(실행머리.futje_p&3))진입점정상=1;
            size_t 선행값=të_dhëna_pozicioni.email&4095,바이트들=të_dhëna_pozicioni.파일영역크기?선행값+të_dhëna_pozicioni.파일영역크기:0;
            if(Tjetër_njësi>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Tjetër_njësi){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Tjetër_njësi+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Tjetër_njësi+선행값,원본자료+të_dhëna_pozicioni.OFFSET_VALUE,të_dhëna_pozicioni.파일영역크기);
            të_dhëna_pozicioni.email-=선행값;të_dhëna_pozicioni.물리주소=të_dhëna_pozicioni.email;të_dhëna_pozicioni.기억영역크기+=선행값;të_dhëna_pozicioni.파일영역크기=바이트들;të_dhëna_pozicioni.OFFSET_VALUE=Tjetër_njësi;të_dhëna_pozicioni.맞춤=4096;
            for(uint64_t faqe_VALUE=të_dhëna_pozicioni.email;faqe_VALUE<të_dhëna_pozicioni.email+të_dhëna_pozicioni.기억영역크기;faqe_VALUE+=4096){unsigned LOOKUP_INDEX=(faqe_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(faqe_Listë)||faqe_Listë[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}faqe_Listë[LOOKUP_INDEX]=1;}
            Tjetër_njësi+=(바이트들+4095)&~(size_t)4095;
        }else if(të_dhëna_pozicioni.TYPE_kategori==4){if(të_dhëna_pozicioni.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+të_dhëna_pozicioni.OFFSET_VALUE,të_dhëna_pozicioni.파일영역크기);të_dhëna_pozicioni.OFFSET_VALUE=부가정보;부가정보+=të_dhëna_pozicioni.파일영역크기;}
        else if(të_dhëna_pozicioni.TYPE_kategori!=0&&të_dhëna_pozicioni.TYPE_kategori!=6&&të_dhëna_pozicioni.TYPE_kategori!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.program_Kreu_OFFSET+순번*sizeof(të_dhëna_pozicioni),&të_dhëna_pozicioni,sizeof(të_dhëna_pozicioni));
    }
    if(!진입점정상)return -1;
    intptr_t skedar_dorezë=사용자호출(3,(uintptr_t)Emër,577,0600,0,0,0);if(skedar_dorezë<0){printf("cc: cannot create output file, error %d\n",(int)skedar_dorezë);return -1;}
    intptr_t 쓴수=사용자호출(1,skedar_dorezë,(uintptr_t)IMAGE,Tjetër_njësi,0,0,0);사용자호출(4,skedar_dorezë,0,0,0,0,0);return 쓴수==(intptr_t)Tjetër_njësi?0:-1;
}
int nis_përdorues_program(int metoda_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metoda_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metoda_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*varg_të_dhëna=tcc_new();if(!varg_të_dhëna)return 1;
    tcc_undefine_symbol(varg_të_dhëna,"__linux__");tcc_undefine_symbol(varg_të_dhëna,"__linux");tcc_undefine_symbol(varg_të_dhëna,"linux");
    tcc_undefine_symbol(varg_të_dhëna,"__unix__");tcc_undefine_symbol(varg_të_dhëna,"__unix");tcc_undefine_symbol(varg_të_dhëna,"unix");
    tcc_undefine_symbol(varg_të_dhëna,"__STDC_HOSTED__");tcc_define_symbol(varg_të_dhëna,"__STDC_HOSTED__","0");tcc_define_symbol(varg_të_dhëna,"__JKOROS__","1");
    tcc_set_options(varg_të_dhëna,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(varg_të_dhëna,"/sdk/include");
    int 반환값=tcc_set_output_type(varg_të_dhëna,TCC_OUTPUT_EXE);
    if(!반환값){if(metoda_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(varg_të_dhëna,원본자료):-1;}else 반환값=tcc_add_file(varg_të_dhëna,입력결과);}
    if(!반환값)반환값=tcc_add_file(varg_të_dhëna,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(varg_të_dhëna,"/sdk/lib/crt.o");
    if(!반환값&&metoda_MODE)반환값=tcc_add_file(varg_të_dhëna,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(varg_të_dhëna,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(varg_të_dhëna,"/@cc-output");
    if(!반환값)반환값=publikoj_futje(출력결과);
    tcc_delete(varg_të_dhëna);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metoda_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
