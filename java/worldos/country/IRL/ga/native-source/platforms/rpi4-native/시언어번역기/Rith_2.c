#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char aitheantóir_VALUE[16];uint16_t TYPE_catagóir,meaisín_TYPE;uint32_t uimhir_an_leagain;uint64_t iontráil_pointe,clár_Ceanntásc_OFFSET,rannán_Ceanntásc_OFFSET;uint32_t 설정비트;uint16_t Méid,clár_Ceanntásc_socraigh_méid,clár_Ceanntásc_COUNT,rannán_Ceanntásc_socraigh_méid,rannán_Ceanntásc_COUNT,rannán_ainm_tábla; } Ceanntásc_VALUE;
typedef struct {uint32_t TYPE_catagóir,설정비트;uint64_t OFFSET_VALUE,ADDRESS,물리주소,파일영역크기,기억영역크기,맞춤;} deighleán_VALUE;
static unsigned char IMAGE[16384];
static int foilsigh_iontráil(const char *Ainm){
    size_t mír_COUNT;const unsigned char*원본자료=시언어출력(&mír_COUNT);if(mír_COUNT<sizeof(Ceanntásc_VALUE))return -1;
    Ceanntásc_VALUE 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.TYPE_catagóir!=2||실행머리.meaisín_TYPE!=183||실행머리.clár_Ceanntásc_socraigh_méid!=sizeof(deighleán_VALUE)||!실행머리.clár_Ceanntásc_COUNT||실행머리.clár_Ceanntásc_COUNT>16||실행머리.clár_Ceanntásc_OFFSET>mír_COUNT||실행머리.clár_Ceanntásc_COUNT*sizeof(deighleán_VALUE)>mír_COUNT-실행머리.clár_Ceanntásc_OFFSET)return -1;
    실행머리.clár_Ceanntásc_OFFSET=sizeof(실행머리);실행머리.rannán_Ceanntásc_OFFSET=실행머리.rannán_Ceanntásc_COUNT=실행머리.rannán_Ceanntásc_socraigh_méid=실행머리.rannán_ainm_tábla=0;memcpy(IMAGE,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.clár_Ceanntásc_COUNT*sizeof(deighleán_VALUE),Ar_aghaidh_mír=4096;unsigned char leathanach_Liosta[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.clár_Ceanntásc_COUNT;순번++){
        deighleán_VALUE sonraí_suíomh;Ceanntásc_VALUE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&sonraí_suíomh,원본자료+원본.clár_Ceanntásc_OFFSET+순번*sizeof(sonraí_suíomh),sizeof(sonraí_suíomh));
        if(sonraí_suíomh.OFFSET_VALUE>mír_COUNT||sonraí_suíomh.파일영역크기>mír_COUNT-sonraí_suíomh.OFFSET_VALUE||sonraí_suíomh.파일영역크기>sonraí_suíomh.기억영역크기)return -1;
        if(sonraí_suíomh.TYPE_catagóir==1){
            if((sonraí_suíomh.설정비트&~7u)||!(sonraí_suíomh.설정비트&4)||(sonraí_suíomh.설정비트&3)==3||sonraí_suíomh.ADDRESS<0x02000000||sonraí_suíomh.ADDRESS>0x02c00000||sonraí_suíomh.기억영역크기>0x02c00000-sonraí_suíomh.ADDRESS)return -1;
            if((sonraí_suíomh.설정비트&1)&&실행머리.iontráil_pointe>=sonraí_suíomh.ADDRESS&&실행머리.iontráil_pointe-sonraí_suíomh.ADDRESS<sonraí_suíomh.파일영역크기&&!(실행머리.iontráil_pointe&3))진입점정상=1;
            size_t 선행값=sonraí_suíomh.ADDRESS&4095,바이트들=sonraí_suíomh.파일영역크기?선행값+sonraí_suíomh.파일영역크기:0;
            if(Ar_aghaidh_mír>sizeof(IMAGE)||바이트들>sizeof(IMAGE)-Ar_aghaidh_mír){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Ar_aghaidh_mír+바이트들),(unsigned)sizeof(IMAGE));return -1;}
            if(바이트들)memcpy(IMAGE+Ar_aghaidh_mír+선행값,원본자료+sonraí_suíomh.OFFSET_VALUE,sonraí_suíomh.파일영역크기);
            sonraí_suíomh.ADDRESS-=선행값;sonraí_suíomh.물리주소=sonraí_suíomh.ADDRESS;sonraí_suíomh.기억영역크기+=선행값;sonraí_suíomh.파일영역크기=바이트들;sonraí_suíomh.OFFSET_VALUE=Ar_aghaidh_mír;sonraí_suíomh.맞춤=4096;
            for(uint64_t leathanach_VALUE=sonraí_suíomh.ADDRESS;leathanach_VALUE<sonraí_suíomh.ADDRESS+sonraí_suíomh.기억영역크기;leathanach_VALUE+=4096){unsigned LOOKUP_INDEX=(leathanach_VALUE-0x02000000)/4096;if(LOOKUP_INDEX>=sizeof(leathanach_Liosta)||leathanach_Liosta[LOOKUP_INDEX]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}leathanach_Liosta[LOOKUP_INDEX]=1;}
            Ar_aghaidh_mír+=(바이트들+4095)&~(size_t)4095;
        }else if(sonraí_suíomh.TYPE_catagóir==4){if(sonraí_suíomh.파일영역크기>4096-부가정보)return -1;memcpy(IMAGE+부가정보,원본자료+sonraí_suíomh.OFFSET_VALUE,sonraí_suíomh.파일영역크기);sonraí_suíomh.OFFSET_VALUE=부가정보;부가정보+=sonraí_suíomh.파일영역크기;}
        else if(sonraí_suíomh.TYPE_catagóir!=0&&sonraí_suíomh.TYPE_catagóir!=6&&sonraí_suíomh.TYPE_catagóir!=0x6474e551)return -1;
        memcpy(IMAGE+실행머리.clár_Ceanntásc_OFFSET+순번*sizeof(sonraí_suíomh),&sonraí_suíomh,sizeof(sonraí_suíomh));
    }
    if(!진입점정상)return -1;
    intptr_t comhad_hanla=사용자호출(3,(uintptr_t)Ainm,577,0600,0,0,0);if(comhad_hanla<0){printf("cc: cannot create output file, error %d\n",(int)comhad_hanla);return -1;}
    intptr_t 쓴수=사용자호출(1,comhad_hanla,(uintptr_t)IMAGE,Ar_aghaidh_mír,0,0,0);사용자호출(4,comhad_hanla,0,0,0,0,0);return 쓴수==(intptr_t)Ar_aghaidh_mír?0:-1;
}
int Start_úsáideoir_clár(int modh_mód){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(modh_mód?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(modh_mód?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*teaghrán_sonraí=tcc_new();if(!teaghrán_sonraí)return 1;
    tcc_undefine_symbol(teaghrán_sonraí,"__linux__");tcc_undefine_symbol(teaghrán_sonraí,"__linux");tcc_undefine_symbol(teaghrán_sonraí,"linux");
    tcc_undefine_symbol(teaghrán_sonraí,"__unix__");tcc_undefine_symbol(teaghrán_sonraí,"__unix");tcc_undefine_symbol(teaghrán_sonraí,"unix");
    tcc_undefine_symbol(teaghrán_sonraí,"__STDC_HOSTED__");tcc_define_symbol(teaghrán_sonraí,"__STDC_HOSTED__","0");tcc_define_symbol(teaghrán_sonraí,"__JKOROS__","1");
    tcc_set_options(teaghrán_sonraí,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(teaghrán_sonraí,"/sdk/include");
    int 반환값=tcc_set_output_type(teaghrán_sonraí,TCC_OUTPUT_EXE);
    if(!반환값){if(modh_mód){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(teaghrán_sonraí,원본자료):-1;}else 반환값=tcc_add_file(teaghrán_sonraí,입력결과);}
    if(!반환값)반환값=tcc_add_file(teaghrán_sonraí,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(teaghrán_sonraí,"/sdk/lib/crt.o");
    if(!반환값&&modh_mód)반환값=tcc_add_file(teaghrán_sonraí,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(teaghrán_sonraí,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(teaghrán_sonraí,"/@cc-output");
    if(!반환값)반환값=foilsigh_iontráil(출력결과);
    tcc_delete(teaghrán_sonraí);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(modh_mód?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
