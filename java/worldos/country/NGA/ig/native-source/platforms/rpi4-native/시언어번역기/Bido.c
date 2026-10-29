#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char ihe_nkọwapụta_valuu[16];uint16_t pinye_otu,ngwa_komputa_pinye;uint32_t 판번호;uint64_t ndebà_akara,app_isi_Nnokwata,nkebì_isi_Nnokwata;uint32_t 설정비트;uint16_t Ụhara,app_isi_ụha,프로그램머리개수,nkebì_isi_ụha,구역머리개수,nkebì_akara_ahà_tebùl; } isi_valuu;
typedef struct {uint32_t pinye_otu,설정비트;uint64_t Nnokwata_valuu,àdreèsì,물리주소,파일영역크기,기억영역크기,맞춤;} mwezuga_valuu;
static unsigned char foto[16384];
static int detuo_ndebà(const char *Aha){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(isi_valuu))return -1;
    isi_valuu 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.pinye_otu!=2||실행머리.ngwa_komputa_pinye!=183||실행머리.app_isi_ụha!=sizeof(mwezuga_valuu)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.app_isi_Nnokwata>개수||실행머리.프로그램머리개수*sizeof(mwezuga_valuu)>개수-실행머리.app_isi_Nnokwata)return -1;
    실행머리.app_isi_Nnokwata=sizeof(실행머리);실행머리.nkebì_isi_Nnokwata=실행머리.구역머리개수=실행머리.nkebì_isi_ụha=실행머리.nkebì_akara_ahà_tebùl=0;memcpy(foto,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(mwezuga_valuu),다음=4096;unsigned char ihuakwụkwọ_ndepụta[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        mwezuga_valuu 자료위치;isi_valuu 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.app_isi_Nnokwata+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Nnokwata_valuu>개수||자료위치.파일영역크기>개수-자료위치.Nnokwata_valuu||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.pinye_otu==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.àdreèsì<0x02000000||자료위치.àdreèsì>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.àdreèsì)return -1;
            if((자료위치.설정비트&1)&&실행머리.ndebà_akara>=자료위치.àdreèsì&&실행머리.ndebà_akara-자료위치.àdreèsì<자료위치.파일영역크기&&!(실행머리.ndebà_akara&3))진입점정상=1;
            size_t 선행값=자료위치.àdreèsì&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(foto)||바이트들>sizeof(foto)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(foto));return -1;}
            if(바이트들)memcpy(foto+다음+선행값,원본자료+자료위치.Nnokwata_valuu,자료위치.파일영역크기);
            자료위치.àdreèsì-=선행값;자료위치.물리주소=자료위치.àdreèsì;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Nnokwata_valuu=다음;자료위치.맞춤=4096;
            for(uint64_t ihuakwụkwọ_valuu=자료위치.àdreèsì;ihuakwụkwọ_valuu<자료위치.àdreèsì+자료위치.기억영역크기;ihuakwụkwọ_valuu+=4096){unsigned 색인=(ihuakwụkwọ_valuu-0x02000000)/4096;if(색인>=sizeof(ihuakwụkwọ_ndepụta)||ihuakwụkwọ_ndepụta[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}ihuakwụkwọ_ndepụta[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.pinye_otu==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(foto+부가정보,원본자료+자료위치.Nnokwata_valuu,자료위치.파일영역크기);자료위치.Nnokwata_valuu=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.pinye_otu!=0&&자료위치.pinye_otu!=6&&자료위치.pinye_otu!=0x6474e551)return -1;
        memcpy(foto+실행머리.app_isi_Nnokwata+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t ọbọakwụkwọ_ebenjìaka=사용자호출(3,(uintptr_t)Aha,577,0600,0,0,0);if(ọbọakwụkwọ_ebenjìaka<0){printf("cc: cannot create output file, error %d\n",(int)ọbọakwụkwọ_ebenjìaka);return -1;}
    intptr_t 쓴수=사용자호출(1,ọbọakwụkwọ_ebenjìaka,(uintptr_t)foto,다음,0,0,0);사용자호출(4,ọbọakwụkwọ_ebenjìaka,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int Mbido_òjìàrụ_app(int usoro_moòdù){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(usoro_moòdù?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(usoro_moòdù?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*ùsòròokwū_datà=tcc_new();if(!ùsòròokwū_datà)return 1;
    tcc_undefine_symbol(ùsòròokwū_datà,"__linux__");tcc_undefine_symbol(ùsòròokwū_datà,"__linux");tcc_undefine_symbol(ùsòròokwū_datà,"linux");
    tcc_undefine_symbol(ùsòròokwū_datà,"__unix__");tcc_undefine_symbol(ùsòròokwū_datà,"__unix");tcc_undefine_symbol(ùsòròokwū_datà,"unix");
    tcc_undefine_symbol(ùsòròokwū_datà,"__STDC_HOSTED__");tcc_define_symbol(ùsòròokwū_datà,"__STDC_HOSTED__","0");tcc_define_symbol(ùsòròokwū_datà,"__JKOROS__","1");
    tcc_set_options(ùsòròokwū_datà,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(ùsòròokwū_datà,"/sdk/include");
    int 반환값=tcc_set_output_type(ùsòròokwū_datà,TCC_OUTPUT_EXE);
    if(!반환값){if(usoro_moòdù){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(ùsòròokwū_datà,원본자료):-1;}else 반환값=tcc_add_file(ùsòròokwū_datà,입력결과);}
    if(!반환값)반환값=tcc_add_file(ùsòròokwū_datà,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(ùsòròokwū_datà,"/sdk/lib/crt.o");
    if(!반환값&&usoro_moòdù)반환값=tcc_add_file(ùsòròokwū_datà,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(ùsòròokwū_datà,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(ùsòròokwū_datà,"/@cc-output");
    if(!반환값)반환값=detuo_ndebà(출력결과);
    tcc_delete(ùsòròokwū_datà);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(usoro_moòdù?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
