#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char dynodwr_VALUE[16];uint16_t TYPE_ardal,peiriant_TYPE;uint32_t rhif_fersiwn;uint64_t cofnod_p,Rhaglen_Pennyn_OFFSET,adran_Pennyn_OFFSET;uint32_t 설정비트;uint16_t Maint,Rhaglen_Pennyn_newid_maint,Rhaglen_Pennyn_COUNT,adran_Pennyn_newid_maint,adran_Pennyn_COUNT,adran_enw_tabl; } Pennyn_VALUE;
typedef struct {uint32_t TYPE_ardal,설정비트;uint64_t OFFSET_VALUE,ADDRESS,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char llun[16384];
static int cyhoeddi_cofnod(const char *Enw){
    size_t eitem_COUNT;const unsigned char*원본자료=시언어출력(&eitem_COUNT);if(eitem_COUNT<sizeof(Pennyn_VALUE))return -1;
    Pennyn_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_ardal!=2||실행머리.peiriant_TYPE!=183||실행머리.Rhaglen_Pennyn_newid_maint!=sizeof(segment_VALUE)||!실행머리.Rhaglen_Pennyn_COUNT||실행머리.Rhaglen_Pennyn_COUNT>16||실행머리.Rhaglen_Pennyn_OFFSET>eitem_COUNT||실행머리.Rhaglen_Pennyn_COUNT*sizeof(segment_VALUE)>eitem_COUNT-실행머리.Rhaglen_Pennyn_OFFSET)return -1;
    실행머리.Rhaglen_Pennyn_OFFSET=sizeof(실행머리);실행머리.adran_Pennyn_OFFSET=실행머리.adran_Pennyn_COUNT=실행머리.adran_Pennyn_newid_maint=실행머리.adran_enw_tabl=0;memcpy(llun,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.Rhaglen_Pennyn_COUNT*sizeof(segment_VALUE),Nesaf_eitem=4096;unsigned char tudalen_Rhestr[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.Rhaglen_Pennyn_COUNT;순번++){
        segment_VALUE data_safle;Pennyn_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_safle,원본자료+원본.Rhaglen_Pennyn_OFFSET+순번*sizeof(data_safle),sizeof(data_safle));
        if(data_safle.OFFSET_VALUE>eitem_COUNT||data_safle.파일영역크기>eitem_COUNT-data_safle.OFFSET_VALUE||data_safle.파일영역크기>data_safle.기억영역크기)return -1;
        if(data_safle.TYPE_ardal==1){
            if((data_safle.설정비트&~7u)||!(data_safle.설정비트&4)||(data_safle.설정비트&3)==3||data_safle.ADDRESS<0x02000000||data_safle.ADDRESS>0x02c00000||data_safle.기억영역크기>0x02c00000-data_safle.ADDRESS)return -1;
            if((data_safle.설정비트&1)&&실행머리.cofnod_p>=data_safle.ADDRESS&&실행머리.cofnod_p-data_safle.ADDRESS<data_safle.파일영역크기&&!(실행머리.cofnod_p&3))진입점정상=1;
            size_t 선행값=data_safle.ADDRESS&4095,바이트들=data_safle.파일영역크기?선행값+data_safle.파일영역크기:0;
            if(Nesaf_eitem>sizeof(llun)||바이트들>sizeof(llun)-Nesaf_eitem){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Nesaf_eitem+바이트들),(unsigned)sizeof(llun));return -1;}
            if(바이트들)memcpy(llun+Nesaf_eitem+선행값,원본자료+data_safle.OFFSET_VALUE,data_safle.파일영역크기);
            data_safle.ADDRESS-=선행값;data_safle.물리주소=data_safle.ADDRESS;data_safle.기억영역크기+=선행값;data_safle.파일영역크기=바이트들;data_safle.OFFSET_VALUE=Nesaf_eitem;data_safle.맞춤=4096;
            for(uint64_t tudalen_VALUE=data_safle.ADDRESS;tudalen_VALUE<data_safle.ADDRESS+data_safle.기억영역크기;tudalen_VALUE+=4096){unsigned LOOKUP_INDEX=(tudalen_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(tudalen_Rhestr)||tudalen_Rhestr[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}tudalen_Rhestr[LOOKUP_INDEX]=1;}
            Nesaf_eitem+=(바이트들+4095)&~(size_t)4095;
        }else if(data_safle.TYPE_ardal==4){if(data_safle.파일영역크기>4096-부가정보)return -1;memcpy(llun+부가정보,원본자료+data_safle.OFFSET_VALUE,data_safle.파일영역크기);data_safle.OFFSET_VALUE=부가정보;부가정보+=data_safle.파일영역크기;}
        else if(data_safle.TYPE_ardal!=0&&data_safle.TYPE_ardal!=6&&data_safle.TYPE_ardal!=0x6474e551)return -1;
        memcpy(llun+실행머리.Rhaglen_Pennyn_OFFSET+순번*sizeof(data_safle),&data_safle,sizeof(data_safle));
    }
    if(!진입점정상)return -1;
    intptr_t ffeil_dolen=사용자호출(3,(uintptr_t)Enw,577,0600,0,0,0);if(ffeil_dolen<0){printf("cc: cannot create output file, error %d\n",(int)ffeil_dolen);return -1;}
    intptr_t 쓴수=사용자호출(1,ffeil_dolen,(uintptr_t)llun,Nesaf_eitem,0,0,0);사용자호출(4,ffeil_dolen,0,0,0,0,0);return 쓴수==(intptr_t)Nesaf_eitem?0:-1;
}
int START_defnyddiwr_Rhaglen(int dull_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(dull_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(dull_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*testun_data=tcc_new();if(!testun_data)return 1;
    tcc_undefine_symbol(testun_data,"__linux__");tcc_undefine_symbol(testun_data,"__linux");tcc_undefine_symbol(testun_data,"linux");
    tcc_undefine_symbol(testun_data,"__unix__");tcc_undefine_symbol(testun_data,"__unix");tcc_undefine_symbol(testun_data,"unix");
    tcc_undefine_symbol(testun_data,"__STDC_HOSTED__");tcc_define_symbol(testun_data,"__STDC_HOSTED__","0");tcc_define_symbol(testun_data,"__JKOROS__","1");
    tcc_set_options(testun_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(testun_data,"/sdk/include");
    int 반환값=tcc_set_output_type(testun_data,TCC_OUTPUT_EXE);
    if(!반환값){if(dull_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(testun_data,원본자료):-1;}else 반환값=tcc_add_file(testun_data,입력결과);}
    if(!반환값)반환값=tcc_add_file(testun_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(testun_data,"/sdk/lib/crt.o");
    if(!반환값&&dull_MODE)반환값=tcc_add_file(testun_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(testun_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(testun_data,"/@cc-output");
    if(!반환값)반환값=cyhoeddi_cofnod(출력결과);
    tcc_delete(testun_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(dull_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
