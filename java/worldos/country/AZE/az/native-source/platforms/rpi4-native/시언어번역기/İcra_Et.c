#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identifikator_VALUE[16];uint16_t TYPE_sahə,maşın_TYPE;uint32_t versiya_nömrəsi;uint64_t daxiletmə_p,proqram_Başlıq_OFFSET,bölmə_Başlıq_OFFSET;uint32_t konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti;uint16_t Böyüklük,proqram_Başlıq_ölçünü_dəyişmək,proqram_Başlıq_COUNT,bölmə_Başlıq_ölçünü_dəyişmək,bölmə_Başlıq_COUNT,bölmə_ad_cədvəl; } Başlıq_VALUE;
typedef struct {uint32_t TYPE_sahə,konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti;uint64_t OFFSET_VALUE,ünvan,물리주소,파일영역크기,기억영역크기,맞춤;} seqment_VALUE;
static unsigned char IMAGE[16384];
static int dərc_et_daxiletmə(const char *Ad){
    size_t element_COUNT;const unsigned char*원본자료=시언어출력(&element_COUNT);if(element_COUNT<sizeof(Başlıq_VALUE))return -1;
    Başlıq_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_sahə!=2||실행머리.maşın_TYPE!=183||실행머리.proqram_Başlıq_ölçünü_dəyişmək!=sizeof(seqment_VALUE)||!실행머리.proqram_Başlıq_COUNT||실행머리.proqram_Başlıq_COUNT>16||실행머리.proqram_Başlıq_OFFSET>element_COUNT||실행머리.proqram_Başlıq_COUNT*sizeof(seqment_VALUE)>element_COUNT-실행머리.proqram_Başlıq_OFFSET)return -1;
    실행머리.proqram_Başlıq_OFFSET=sizeof(실행머리);실행머리.bölmə_Başlıq_OFFSET=실행머리.bölmə_Başlıq_COUNT=실행머리.bölmə_Başlıq_ölçünü_dəyişmək=실행머리.bölmə_ad_cədvəl=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.proqram_Başlıq_COUNT*sizeof(seqment_VALUE),Sonrakı_element=4096;unsigned char səhifə_Siyahı[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.proqram_Başlıq_COUNT;순번++){
        seqment_VALUE verilənlər_yerinə_qoymaq;Başlıq_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&verilənlər_yerinə_qoymaq,원본자료+원본.proqram_Başlıq_OFFSET+순번*sizeof(verilənlər_yerinə_qoymaq),sizeof(verilənlər_yerinə_qoymaq));
        if(verilənlər_yerinə_qoymaq.OFFSET_VALUE>element_COUNT||verilənlər_yerinə_qoymaq.파일영역크기>element_COUNT-verilənlər_yerinə_qoymaq.OFFSET_VALUE||verilənlər_yerinə_qoymaq.파일영역크기>verilənlər_yerinə_qoymaq.기억영역크기)return -1;
        if(verilənlər_yerinə_qoymaq.TYPE_sahə==1){
            if((verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&~7u)||!(verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&4)||(verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&3)==3||verilənlər_yerinə_qoymaq.ünvan<0x02000000||verilənlər_yerinə_qoymaq.ünvan>0x02c00000||verilənlər_yerinə_qoymaq.기억영역크기>0x02c00000-verilənlər_yerinə_qoymaq.ünvan)return -1;
            if((verilənlər_yerinə_qoymaq.konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&1)&&실행머리.daxiletmə_p>=verilənlər_yerinə_qoymaq.ünvan&&실행머리.daxiletmə_p-verilənlər_yerinə_qoymaq.ünvan<verilənlər_yerinə_qoymaq.파일영역크기&&!(실행머리.daxiletmə_p&3))진입점정상=1;
            size_t 선행값=verilənlər_yerinə_qoymaq.ünvan&4095,바이트들=verilənlər_yerinə_qoymaq.파일영역크기?선행값+verilənlər_yerinə_qoymaq.파일영역크기:0;
            if(Sonrakı_element>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Sonrakı_element){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Sonrakı_element+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Sonrakı_element+선행값,원본자료+verilənlər_yerinə_qoymaq.OFFSET_VALUE,verilənlər_yerinə_qoymaq.파일영역크기);
            verilənlər_yerinə_qoymaq.ünvan-=선행값;verilənlər_yerinə_qoymaq.물리주소=verilənlər_yerinə_qoymaq.ünvan;verilənlər_yerinə_qoymaq.기억영역크기+=선행값;verilənlər_yerinə_qoymaq.파일영역크기=바이트들;verilənlər_yerinə_qoymaq.OFFSET_VALUE=Sonrakı_element;verilənlər_yerinə_qoymaq.맞춤=4096;
            for(uint64_t səhifə_VALUE=verilənlər_yerinə_qoymaq.ünvan;səhifə_VALUE<verilənlər_yerinə_qoymaq.ünvan+verilənlər_yerinə_qoymaq.기억영역크기;səhifə_VALUE+=4096){unsigned LOOKUP_INDEX=(səhifə_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(səhifə_Siyahı)||səhifə_Siyahı[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}səhifə_Siyahı[LOOKUP_INDEX]=1;}
            Sonrakı_element+=(바이트들+4095)&~(size_t)4095;
        }else if(verilənlər_yerinə_qoymaq.TYPE_sahə==4){if(verilənlər_yerinə_qoymaq.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+verilənlər_yerinə_qoymaq.OFFSET_VALUE,verilənlər_yerinə_qoymaq.파일영역크기);verilənlər_yerinə_qoymaq.OFFSET_VALUE=부가정보;부가정보+=verilənlər_yerinə_qoymaq.파일영역크기;}
        else if(verilənlər_yerinə_qoymaq.TYPE_sahə!=0&&verilənlər_yerinə_qoymaq.TYPE_sahə!=6&&verilənlər_yerinə_qoymaq.TYPE_sahə!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.proqram_Başlıq_OFFSET+순번*sizeof(verilənlər_yerinə_qoymaq),&verilənlər_yerinə_qoymaq,sizeof(verilənlər_yerinə_qoymaq));
    }
    if(!진입점정상)return -1;
    intptr_t fayl_tutacaq=사용자호출(3,(uintptr_t)Ad,577,0600,0,0,0);if(fayl_tutacaq<0){printf("cc: cannot create output file, error %d\n",(int)fayl_tutacaq);return -1;}
    intptr_t 쓴수=사용자호출(1,fayl_tutacaq,(uintptr_t)IMAGE,Sonrakı_element,0,0,0);사용자호출(4,fayl_tutacaq,0,0,0,0,0);return 쓴수==(intptr_t)Sonrakı_element?0:-1;
}
int Başla_istifadəçi_proqram(int metod_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metod_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metod_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*sətir_verilənlər=tcc_new();if(!sətir_verilənlər)return 1;
    tcc_undefine_symbol(sətir_verilənlər,"__linux__");tcc_undefine_symbol(sətir_verilənlər,"__linux");tcc_undefine_symbol(sətir_verilənlər,"linux");
    tcc_undefine_symbol(sətir_verilənlər,"__unix__");tcc_undefine_symbol(sətir_verilənlər,"__unix");tcc_undefine_symbol(sətir_verilənlər,"unix");
    tcc_undefine_symbol(sətir_verilənlər,"__STDC_HOSTED__");tcc_define_symbol(sətir_verilənlər,"__STDC_HOSTED__","0");tcc_define_symbol(sətir_verilənlər,"__JKOROS__","1");
    tcc_set_options(sətir_verilənlər,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(sətir_verilənlər,"/sdk/include");
    int 반환값=tcc_set_output_type(sətir_verilənlər,TCC_OUTPUT_EXE);
    if(!반환값){if(metod_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(sətir_verilənlər,원본자료):-1;}else 반환값=tcc_add_file(sətir_verilənlər,입력결과);}
    if(!반환값)반환값=tcc_add_file(sətir_verilənlər,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(sətir_verilənlər,"/sdk/lib/crt.o");
    if(!반환값&&metod_MODE)반환값=tcc_add_file(sətir_verilənlər,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(sətir_verilənlər,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(sətir_verilənlər,"/@cc-output");
    if(!반환값)반환값=dərc_et_daxiletmə(출력결과);
    tcc_delete(sətir_verilənlər);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metod_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
