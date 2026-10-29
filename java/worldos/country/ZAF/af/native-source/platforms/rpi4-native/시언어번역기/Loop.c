#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char waarde_VALUE[16];uint16_t TYPE_kategorie,masjien_TYPE;uint32_t 판번호;uint64_t inskrywing_p,program_Loopkop_OFFSET,seksie_Loopkop_OFFSET;uint32_t konfigurasie_Agtergrond_intelligente_oordragdiens;uint16_t Grootte,program_Loopkop_verstel,program_Loopkop_COUNT,seksie_Loopkop_verstel,seksie_Loopkop_COUNT,seksie_naam_tabel; } Loopkop_VALUE;
typedef struct {uint32_t TYPE_kategorie,konfigurasie_Agtergrond_intelligente_oordragdiens;uint64_t OFFSET_VALUE,adres,물리주소,파일영역크기,기억영역크기,맞춤;} segment_VALUE;
static unsigned char foto[16384];
static int publiseer_inskrywing(const char *Naam){
    size_t item_COUNT;const unsigned char*원본자료=시언어출력(&item_COUNT);if(item_COUNT<sizeof(Loopkop_VALUE))return -1;
    Loopkop_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_kategorie!=2||실행머리.masjien_TYPE!=183||실행머리.program_Loopkop_verstel!=sizeof(segment_VALUE)||!실행머리.program_Loopkop_COUNT||실행머리.program_Loopkop_COUNT>16||실행머리.program_Loopkop_OFFSET>item_COUNT||실행머리.program_Loopkop_COUNT*sizeof(segment_VALUE)>item_COUNT-실행머리.program_Loopkop_OFFSET)return -1;
    실행머리.program_Loopkop_OFFSET=sizeof(실행머리);실행머리.seksie_Loopkop_OFFSET=실행머리.seksie_Loopkop_COUNT=실행머리.seksie_Loopkop_verstel=실행머리.seksie_naam_tabel=0;memcpy(foto,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.program_Loopkop_COUNT*sizeof(segment_VALUE),Volgende_item=4096;unsigned char bladsy_Lys[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.program_Loopkop_COUNT;순번++){
        segment_VALUE data_plaas;Loopkop_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&data_plaas,원본자료+원본.program_Loopkop_OFFSET+순번*sizeof(data_plaas),sizeof(data_plaas));
        if(data_plaas.OFFSET_VALUE>item_COUNT||data_plaas.파일영역크기>item_COUNT-data_plaas.OFFSET_VALUE||data_plaas.파일영역크기>data_plaas.기억영역크기)return -1;
        if(data_plaas.TYPE_kategorie==1){
            if((data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens&~7u)||!(data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens&4)||(data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens&3)==3||data_plaas.adres<0x02000000||data_plaas.adres>0x02c00000||data_plaas.기억영역크기>0x02c00000-data_plaas.adres)return -1;
            if((data_plaas.konfigurasie_Agtergrond_intelligente_oordragdiens&1)&&실행머리.inskrywing_p>=data_plaas.adres&&실행머리.inskrywing_p-data_plaas.adres<data_plaas.파일영역크기&&!(실행머리.inskrywing_p&3))진입점정상=1;
            size_t 선행값=data_plaas.adres&4095,바이트들=data_plaas.파일영역크기?선행값+data_plaas.파일영역크기:0;
            if(Volgende_item>sizeof(foto)||바이트들>sizeof(foto)-Volgende_item){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Volgende_item+바이트들),(unsigned)sizeof(foto));return -1;}
            if(바이트들)memcpy(foto+Volgende_item+선행값,원본자료+data_plaas.OFFSET_VALUE,data_plaas.파일영역크기);
            data_plaas.adres-=선행값;data_plaas.물리주소=data_plaas.adres;data_plaas.기억영역크기+=선행값;data_plaas.파일영역크기=바이트들;data_plaas.OFFSET_VALUE=Volgende_item;data_plaas.맞춤=4096;
            for(uint64_t bladsy_VALUE=data_plaas.adres;bladsy_VALUE<data_plaas.adres+data_plaas.기억영역크기;bladsy_VALUE+=4096){unsigned LOOKUP_INDEX=(bladsy_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(bladsy_Lys)||bladsy_Lys[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}bladsy_Lys[LOOKUP_INDEX]=1;}
            Volgende_item+=(바이트들+4095)&~(size_t)4095;
        }else if(data_plaas.TYPE_kategorie==4){if(data_plaas.파일영역크기>4096-부가정보)return -1;memcpy(foto+부가정보,원본자료+data_plaas.OFFSET_VALUE,data_plaas.파일영역크기);data_plaas.OFFSET_VALUE=부가정보;부가정보+=data_plaas.파일영역크기;}
        else if(data_plaas.TYPE_kategorie!=0&&data_plaas.TYPE_kategorie!=6&&data_plaas.TYPE_kategorie!=0x6474e551)return -1;
        memcpy(foto+실행머리.program_Loopkop_OFFSET+순번*sizeof(data_plaas),&data_plaas,sizeof(data_plaas));
    }
    if(!진입점정상)return -1;
    intptr_t lêer_handvatsel=사용자호출(3,(uintptr_t)Naam,577,0600,0,0,0);if(lêer_handvatsel<0){printf("cc: cannot create output file, error %d\n",(int)lêer_handvatsel);return -1;}
    intptr_t 쓴수=사용자호출(1,lêer_handvatsel,(uintptr_t)foto,Volgende_item,0,0,0);사용자호출(4,lêer_handvatsel,0,0,0,0,0);return 쓴수==(intptr_t)Volgende_item?0:-1;
}
int BEGIN_gebruiker_program(int metode_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metode_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(metode_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*string_data=tcc_new();if(!string_data)return 1;
    tcc_undefine_symbol(string_data,"__linux__");tcc_undefine_symbol(string_data,"__linux");tcc_undefine_symbol(string_data,"linux");
    tcc_undefine_symbol(string_data,"__unix__");tcc_undefine_symbol(string_data,"__unix");tcc_undefine_symbol(string_data,"unix");
    tcc_undefine_symbol(string_data,"__STDC_HOSTED__");tcc_define_symbol(string_data,"__STDC_HOSTED__","0");tcc_define_symbol(string_data,"__JKOROS__","1");
    tcc_set_options(string_data,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(string_data,"/sdk/include");
    int 반환값=tcc_set_output_type(string_data,TCC_OUTPUT_EXE);
    if(!반환값){if(metode_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(string_data,원본자료):-1;}else 반환값=tcc_add_file(string_data,입력결과);}
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/crt.o");
    if(!반환값&&metode_MODE)반환값=tcc_add_file(string_data,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(string_data,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(string_data,"/@cc-output");
    if(!반환값)반환값=publiseer_inskrywing(출력결과);
    tcc_delete(string_data);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metode_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
