#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char setlhaodi_Boleng[16];uint16_t tlanya_setlhopha,motšhine_tlanya;uint32_t 판번호;uint64_t tsenyo_ntlha,Tiriso_setlhogo_Baya_ka_Tekatekanyo,karolo_setlhogo_Baya_ka_Tekatekanyo;uint32_t 설정비트;uint16_t lekanya,Tiriso_setlhogo_lekanya,프로그램머리개수,karolo_setlhogo_lekanya,구역머리개수,karolo_leina_lenaneothalo; } setlhogo_Boleng;
typedef struct {uint32_t tlanya_setlhopha,설정비트;uint64_t Baya_ka_Tekatekanyo_Boleng,aterese,물리주소,파일영역크기,기억영역크기,맞춤;} karolo_Boleng_32e9301f;
static unsigned char Setshwantsho[16384];
static int phasalatsa_tsenyo(const char *leina){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(setlhogo_Boleng))return -1;
    setlhogo_Boleng 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.tlanya_setlhopha!=2||실행머리.motšhine_tlanya!=183||실행머리.Tiriso_setlhogo_lekanya!=sizeof(karolo_Boleng_32e9301f)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.Tiriso_setlhogo_Baya_ka_Tekatekanyo>개수||실행머리.프로그램머리개수*sizeof(karolo_Boleng_32e9301f)>개수-실행머리.Tiriso_setlhogo_Baya_ka_Tekatekanyo)return -1;
    실행머리.Tiriso_setlhogo_Baya_ka_Tekatekanyo=sizeof(실행머리);실행머리.karolo_setlhogo_Baya_ka_Tekatekanyo=실행머리.구역머리개수=실행머리.karolo_setlhogo_lekanya=실행머리.karolo_leina_lenaneothalo=0;memcpy(Setshwantsho,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(karolo_Boleng_32e9301f),다음=4096;unsigned char tsebe_lenaane[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        karolo_Boleng_32e9301f 자료위치;setlhogo_Boleng 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.Tiriso_setlhogo_Baya_ka_Tekatekanyo+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Baya_ka_Tekatekanyo_Boleng>개수||자료위치.파일영역크기>개수-자료위치.Baya_ka_Tekatekanyo_Boleng||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.tlanya_setlhopha==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.aterese<0x02000000||자료위치.aterese>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.aterese)return -1;
            if((자료위치.설정비트&1)&&실행머리.tsenyo_ntlha>=자료위치.aterese&&실행머리.tsenyo_ntlha-자료위치.aterese<자료위치.파일영역크기&&!(실행머리.tsenyo_ntlha&3))진입점정상=1;
            size_t 선행값=자료위치.aterese&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(Setshwantsho)||바이트들>sizeof(Setshwantsho)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(Setshwantsho));return -1;}
            if(바이트들)memcpy(Setshwantsho+다음+선행값,원본자료+자료위치.Baya_ka_Tekatekanyo_Boleng,자료위치.파일영역크기);
            자료위치.aterese-=선행값;자료위치.물리주소=자료위치.aterese;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Baya_ka_Tekatekanyo_Boleng=다음;자료위치.맞춤=4096;
            for(uint64_t tsebe_Boleng=자료위치.aterese;tsebe_Boleng<자료위치.aterese+자료위치.기억영역크기;tsebe_Boleng+=4096){unsigned 색인=(tsebe_Boleng-0x02000000)/4096;if(색인>=sizeof(tsebe_lenaane)||tsebe_lenaane[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}tsebe_lenaane[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.tlanya_setlhopha==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(Setshwantsho+부가정보,원본자료+자료위치.Baya_ka_Tekatekanyo_Boleng,자료위치.파일영역크기);자료위치.Baya_ka_Tekatekanyo_Boleng=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.tlanya_setlhopha!=0&&자료위치.tlanya_setlhopha!=6&&자료위치.tlanya_setlhopha!=0x6474e551)return -1;
        memcpy(Setshwantsho+실행머리.Tiriso_setlhogo_Baya_ka_Tekatekanyo+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t faele_mokgwakamogelo=사용자호출(3,(uintptr_t)leina,577,0600,0,0,0);if(faele_mokgwakamogelo<0){printf("cc: cannot create output file, error %d\n",(int)faele_mokgwakamogelo);return -1;}
    intptr_t 쓴수=사용자호출(1,faele_mokgwakamogelo,(uintptr_t)Setshwantsho,다음,0,0,0);사용자호출(4,faele_mokgwakamogelo,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int simolola_modirisi_Tiriso(int mokgwa_mokgwa){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(mokgwa_mokgwa?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(mokgwa_mokgwa?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*dikwalwa_tshedimosetso=tcc_new();if(!dikwalwa_tshedimosetso)return 1;
    tcc_undefine_symbol(dikwalwa_tshedimosetso,"__linux__");tcc_undefine_symbol(dikwalwa_tshedimosetso,"__linux");tcc_undefine_symbol(dikwalwa_tshedimosetso,"linux");
    tcc_undefine_symbol(dikwalwa_tshedimosetso,"__unix__");tcc_undefine_symbol(dikwalwa_tshedimosetso,"__unix");tcc_undefine_symbol(dikwalwa_tshedimosetso,"unix");
    tcc_undefine_symbol(dikwalwa_tshedimosetso,"__STDC_HOSTED__");tcc_define_symbol(dikwalwa_tshedimosetso,"__STDC_HOSTED__","0");tcc_define_symbol(dikwalwa_tshedimosetso,"__JKOROS__","1");
    tcc_set_options(dikwalwa_tshedimosetso,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(dikwalwa_tshedimosetso,"/sdk/include");
    int 반환값=tcc_set_output_type(dikwalwa_tshedimosetso,TCC_OUTPUT_EXE);
    if(!반환값){if(mokgwa_mokgwa){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(dikwalwa_tshedimosetso,원본자료):-1;}else 반환값=tcc_add_file(dikwalwa_tshedimosetso,입력결과);}
    if(!반환값)반환값=tcc_add_file(dikwalwa_tshedimosetso,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(dikwalwa_tshedimosetso,"/sdk/lib/crt.o");
    if(!반환값&&mokgwa_mokgwa)반환값=tcc_add_file(dikwalwa_tshedimosetso,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(dikwalwa_tshedimosetso,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(dikwalwa_tshedimosetso,"/@cc-output");
    if(!반환값)반환값=phasalatsa_tsenyo(출력결과);
    tcc_delete(dikwalwa_tshedimosetso);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(mokgwa_mokgwa?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
