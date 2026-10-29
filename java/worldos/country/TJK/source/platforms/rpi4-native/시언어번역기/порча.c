#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char идентификатор_қимат[16];uint16_t навъ_категория,компютер_навъ;uint32_t 판번호;uint64_t ворида_нуқта,барнома_Сарнавор_Интиқолшавӣ,қисмат_Сарнавор_Интиқолшавӣ;uint32_t 설정비트;uint16_t андоза_кардан,барнома_Сарнавор_андоза_кардан,프로그램머리개수,қисмат_Сарнавор_андоза_кардан,구역머리개수,қисмат_ном_ҷадвал; } Сарнавор_қимат;
typedef struct {uint32_t навъ_категория,설정비트;uint64_t Интиқолшавӣ_қимат,суроға,물리주소,파일영역크기,기억영역크기,맞춤;} сегмент_қимат;
static unsigned char расм[16384];
static int нашр_кардан_ворида(const char *Ном){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(Сарнавор_қимат))return -1;
    Сарнавор_қимат 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.навъ_категория!=2||실행머리.компютер_навъ!=183||실행머리.барнома_Сарнавор_андоза_кардан!=sizeof(сегмент_қимат)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.барнома_Сарнавор_Интиқолшавӣ>개수||실행머리.프로그램머리개수*sizeof(сегмент_қимат)>개수-실행머리.барнома_Сарнавор_Интиқолшавӣ)return -1;
    실행머리.барнома_Сарнавор_Интиқолшавӣ=sizeof(실행머리);실행머리.қисмат_Сарнавор_Интиқолшавӣ=실행머리.구역머리개수=실행머리.қисмат_Сарнавор_андоза_кардан=실행머리.қисмат_ном_ҷадвал=0;memcpy(расм,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(сегмент_қимат),다음=4096;unsigned char саҳифа_Рӯйхат[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        сегмент_қимат 자료위치;Сарнавор_қимат 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.барнома_Сарнавор_Интиқолшавӣ+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.Интиқолшавӣ_қимат>개수||자료위치.파일영역크기>개수-자료위치.Интиқолшавӣ_қимат||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.навъ_категория==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.суроға<0x02000000||자료위치.суроға>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.суроға)return -1;
            if((자료위치.설정비트&1)&&실행머리.ворида_нуқта>=자료위치.суроға&&실행머리.ворида_нуқта-자료위치.суроға<자료위치.파일영역크기&&!(실행머리.ворида_нуқта&3))진입점정상=1;
            size_t 선행값=자료위치.суроға&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(расм)||바이트들>sizeof(расм)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(расм));return -1;}
            if(바이트들)memcpy(расм+다음+선행값,원본자료+자료위치.Интиқолшавӣ_қимат,자료위치.파일영역크기);
            자료위치.суроға-=선행값;자료위치.물리주소=자료위치.суроға;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.Интиқолшавӣ_қимат=다음;자료위치.맞춤=4096;
            for(uint64_t саҳифа_қимат=자료위치.суроға;саҳифа_қимат<자료위치.суроға+자료위치.기억영역크기;саҳифа_қимат+=4096){unsigned 색인=(саҳифа_қимат-0x02000000)/4096;if(색인>=sizeof(саҳифа_Рӯйхат)||саҳифа_Рӯйхат[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}саҳифа_Рӯйхат[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.навъ_категория==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(расм+부가정보,원본자료+자료위치.Интиқолшавӣ_қимат,자료위치.파일영역크기);자료위치.Интиқолшавӣ_қимат=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.навъ_категория!=0&&자료위치.навъ_категория!=6&&자료위치.навъ_категория!=0x6474e551)return -1;
        memcpy(расм+실행머리.барнома_Сарнавор_Интиқолшавӣ+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t файл_дастак=사용자호출(3,(uintptr_t)Ном,577,0600,0,0,0);if(файл_дастак<0){printf("cc: cannot create output file, error %d\n",(int)файл_дастак);return -1;}
    intptr_t 쓴수=사용자호출(1,файл_дастак,(uintptr_t)расм,다음,0,0,0);사용자호출(4,файл_дастак,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int Оғоз_корбар_барнома(int сабк_ҳолат){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(сабк_ҳолат?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(сабк_ҳолат?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*сатр_иттилоот=tcc_new();if(!сатр_иттилоот)return 1;
    tcc_undefine_symbol(сатр_иттилоот,"__linux__");tcc_undefine_symbol(сатр_иттилоот,"__linux");tcc_undefine_symbol(сатр_иттилоот,"linux");
    tcc_undefine_symbol(сатр_иттилоот,"__unix__");tcc_undefine_symbol(сатр_иттилоот,"__unix");tcc_undefine_symbol(сатр_иттилоот,"unix");
    tcc_undefine_symbol(сатр_иттилоот,"__STDC_HOSTED__");tcc_define_symbol(сатр_иттилоот,"__STDC_HOSTED__","0");tcc_define_symbol(сатр_иттилоот,"__JKOROS__","1");
    tcc_set_options(сатр_иттилоот,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(сатр_иттилоот,"/sdk/include");
    int 반환값=tcc_set_output_type(сатр_иттилоот,TCC_OUTPUT_EXE);
    if(!반환값){if(сабк_ҳолат){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(сатр_иттилоот,원본자료):-1;}else 반환값=tcc_add_file(сатр_иттилоот,입력결과);}
    if(!반환값)반환값=tcc_add_file(сатр_иттилоот,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(сатр_иттилоот,"/sdk/lib/crt.o");
    if(!반환값&&сабк_ҳолат)반환값=tcc_add_file(сатр_иттилоот,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(сатр_иттилоот,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(сатр_иттилоот,"/@cc-output");
    if(!반환값)반환값=нашр_кардан_ворида(출력결과);
    tcc_delete(сатр_иттилоот);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(сабк_ҳолат?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
