#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char pūtāutu_uara[16];uint16_t TYPE_kāwai,mīhini_TYPE;uint32_t 판번호;uint64_t tāurunga_ira,kaupapa_Pane_OFFSET,wāhanga_Pane_OFFSET;uint32_t 설정비트;uint16_t rahi,kaupapa_Pane_rahi,kaupapa_Pane_COUNT,wāhanga_Pane_rahi,wāhanga_Pane_COUNT,wāhanga_ingoa_ripanga; } Pane_uara;
typedef struct {uint32_t TYPE_kāwai,설정비트;uint64_t OFFSET_uara,ADDRESS,물리주소,파일영역크기,기억영역크기,맞춤;} tapahanga_uara;
static unsigned char IMAGE[16384];
static int whakaputa_tāurunga(const char *Ingoa){
    size_t tuemi_COUNT;const unsigned char*원본자료=시언어출력(&tuemi_COUNT);if(tuemi_COUNT<sizeof(Pane_uara))return -1;
    Pane_uara 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_kāwai!=2||실행머리.mīhini_TYPE!=183||실행머리.kaupapa_Pane_rahi!=sizeof(tapahanga_uara)||!실행머리.kaupapa_Pane_COUNT||실행머리.kaupapa_Pane_COUNT>16||실행머리.kaupapa_Pane_OFFSET>tuemi_COUNT||실행머리.kaupapa_Pane_COUNT*sizeof(tapahanga_uara)>tuemi_COUNT-실행머리.kaupapa_Pane_OFFSET)return -1;
    실행머리.kaupapa_Pane_OFFSET=sizeof(실행머리);실행머리.wāhanga_Pane_OFFSET=실행머리.wāhanga_Pane_COUNT=실행머리.wāhanga_Pane_rahi=실행머리.wāhanga_ingoa_ripanga=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.kaupapa_Pane_COUNT*sizeof(tapahanga_uara),Panuku_tuemi=4096;unsigned char whārangi_Rārangi[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.kaupapa_Pane_COUNT;순번++){
        tapahanga_uara raraunga_tūranga;Pane_uara 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&raraunga_tūranga,원본자료+원본.kaupapa_Pane_OFFSET+순번*sizeof(raraunga_tūranga),sizeof(raraunga_tūranga));
        if(raraunga_tūranga.OFFSET_uara>tuemi_COUNT||raraunga_tūranga.파일영역크기>tuemi_COUNT-raraunga_tūranga.OFFSET_uara||raraunga_tūranga.파일영역크기>raraunga_tūranga.기억영역크기)return -1;
        if(raraunga_tūranga.TYPE_kāwai==1){
            if((raraunga_tūranga.설정비트&~7u)||!(raraunga_tūranga.설정비트&4)||(raraunga_tūranga.설정비트&3)==3||raraunga_tūranga.ADDRESS<0x02000000||raraunga_tūranga.ADDRESS>0x02c00000||raraunga_tūranga.기억영역크기>0x02c00000-raraunga_tūranga.ADDRESS)return -1;
            if((raraunga_tūranga.설정비트&1)&&실행머리.tāurunga_ira>=raraunga_tūranga.ADDRESS&&실행머리.tāurunga_ira-raraunga_tūranga.ADDRESS<raraunga_tūranga.파일영역크기&&!(실행머리.tāurunga_ira&3))진입점정상=1;
            size_t 선행값=raraunga_tūranga.ADDRESS&4095,바이트들=raraunga_tūranga.파일영역크기?선행값+raraunga_tūranga.파일영역크기:0;
            if(Panuku_tuemi>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Panuku_tuemi){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Panuku_tuemi+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Panuku_tuemi+선행값,원본자료+raraunga_tūranga.OFFSET_uara,raraunga_tūranga.파일영역크기);
            raraunga_tūranga.ADDRESS-=선행값;raraunga_tūranga.물리주소=raraunga_tūranga.ADDRESS;raraunga_tūranga.기억영역크기+=선행값;raraunga_tūranga.파일영역크기=바이트들;raraunga_tūranga.OFFSET_uara=Panuku_tuemi;raraunga_tūranga.맞춤=4096;
            for(uint64_t whārangi_uara=raraunga_tūranga.ADDRESS;whārangi_uara<raraunga_tūranga.ADDRESS+raraunga_tūranga.기억영역크기;whārangi_uara+=4096){unsigned Rapu_INDEX=(whārangi_uara-0x02000000)/4096;if(Rapu_INDEX>=sizeof(whārangi_Rārangi)||whārangi_Rārangi[Rapu_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}whārangi_Rārangi[Rapu_INDEX]=1;}
            Panuku_tuemi+=(바이트들+4095)&~(size_t)4095;
        }else if(raraunga_tūranga.TYPE_kāwai==4){if(raraunga_tūranga.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+raraunga_tūranga.OFFSET_uara,raraunga_tūranga.파일영역크기);raraunga_tūranga.OFFSET_uara=부가정보;부가정보+=raraunga_tūranga.파일영역크기;}
        else if(raraunga_tūranga.TYPE_kāwai!=0&&raraunga_tūranga.TYPE_kāwai!=6&&raraunga_tūranga.TYPE_kāwai!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.kaupapa_Pane_OFFSET+순번*sizeof(raraunga_tūranga),&raraunga_tūranga,sizeof(raraunga_tūranga));
    }
    if(!진입점정상)return -1;
    intptr_t kōnae_raweke=사용자호출(3,(uintptr_t)Ingoa,577,0600,0,0,0);if(kōnae_raweke<0){printf("cc: cannot create output file, error %d\n",(int)kōnae_raweke);return -1;}
    intptr_t 쓴수=사용자호출(1,kōnae_raweke,(uintptr_t)IMAGE,Panuku_tuemi,0,0,0);사용자호출(4,kōnae_raweke,0,0,0,0,0);return 쓴수==(intptr_t)Panuku_tuemi?0:-1;
}
int Start_kaiwhakamahi_kaupapa(int aratuka_MODE){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(aratuka_MODE?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(aratuka_MODE?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*aho_raraunga=tcc_new();if(!aho_raraunga)return 1;
    tcc_undefine_symbol(aho_raraunga,"__linux__");tcc_undefine_symbol(aho_raraunga,"__linux");tcc_undefine_symbol(aho_raraunga,"linux");
    tcc_undefine_symbol(aho_raraunga,"__unix__");tcc_undefine_symbol(aho_raraunga,"__unix");tcc_undefine_symbol(aho_raraunga,"unix");
    tcc_undefine_symbol(aho_raraunga,"__STDC_HOSTED__");tcc_define_symbol(aho_raraunga,"__STDC_HOSTED__","0");tcc_define_symbol(aho_raraunga,"__JKOROS__","1");
    tcc_set_options(aho_raraunga,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(aho_raraunga,"/sdk/include");
    int 반환값=tcc_set_output_type(aho_raraunga,TCC_OUTPUT_EXE);
    if(!반환값){if(aratuka_MODE){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(aho_raraunga,원본자료):-1;}else 반환값=tcc_add_file(aho_raraunga,입력결과);}
    if(!반환값)반환값=tcc_add_file(aho_raraunga,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(aho_raraunga,"/sdk/lib/crt.o");
    if(!반환값&&aratuka_MODE)반환값=tcc_add_file(aho_raraunga,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(aho_raraunga,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(aho_raraunga,"/@cc-output");
    if(!반환값)반환값=whakaputa_tāurunga(출력결과);
    tcc_delete(aho_raraunga);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(aratuka_MODE?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
