#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *시언어출력(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char ፈላዪ_ዋጋ_5b7b8b77[16];uint16_t ዓይነት_መደብ,ማሽን_ዓይነት;uint32_t 판번호;uint64_t ምእታው_ነጥቢ,መተግበሪ_ርእሲ_ሽፋን,ክፋል_ርእሲ_ሽፋን;uint32_t 설정비트;uint16_t መጠን,መተግበሪ_ርእሲ_መጠን,프로그램머리개수,ክፋል_ርእሲ_መጠን,구역머리개수,ክፋል_ሽም_ሰሌዳ; } ርእሲ_ዋጋ;
typedef struct {uint32_t ዓይነት_መደብ,설정비트;uint64_t ሽፋን_ዋጋ,ኣድራሻ,물리주소,파일영역크기,기억영역크기,맞춤;} ክፋል_ዋጋ_32e9301f;
static unsigned char ምስሊ[16384];
static int ሓትም_ምእታው(const char *ሽም){
    size_t 개수;const unsigned char*원본자료=시언어출력(&개수);if(개수<sizeof(ርእሲ_ዋጋ))return -1;
    ርእሲ_ዋጋ 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.ዓይነት_መደብ!=2||실행머리.ማሽን_ዓይነት!=183||실행머리.መተግበሪ_ርእሲ_መጠን!=sizeof(ክፋል_ዋጋ_32e9301f)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.መተግበሪ_ርእሲ_ሽፋን>개수||실행머리.프로그램머리개수*sizeof(ክፋል_ዋጋ_32e9301f)>개수-실행머리.መተግበሪ_ርእሲ_ሽፋን)return -1;
    실행머리.መተግበሪ_ርእሲ_ሽፋን=sizeof(실행머리);실행머리.ክፋል_ርእሲ_ሽፋን=실행머리.구역머리개수=실행머리.ክፋል_ርእሲ_መጠን=실행머리.ክፋል_ሽም_ሰሌዳ=0;memcpy(ምስሊ,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(ክፋል_ዋጋ_32e9301f),다음=4096;unsigned char ገጽ_ዝርዝር[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        ክፋል_ዋጋ_32e9301f 자료위치;ርእሲ_ዋጋ 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&자료위치,원본자료+원본.መተግበሪ_ርእሲ_ሽፋን+순번*sizeof(자료위치),sizeof(자료위치));
        if(자료위치.ሽፋን_ዋጋ>개수||자료위치.파일영역크기>개수-자료위치.ሽፋን_ዋጋ||자료위치.파일영역크기>자료위치.기억영역크기)return -1;
        if(자료위치.ዓይነት_መደብ==1){
            if((자료위치.설정비트&~7u)||!(자료위치.설정비트&4)||(자료위치.설정비트&3)==3||자료위치.ኣድራሻ<0x02000000||자료위치.ኣድራሻ>0x02c00000||자료위치.기억영역크기>0x02c00000-자료위치.ኣድራሻ)return -1;
            if((자료위치.설정비트&1)&&실행머리.ምእታው_ነጥቢ>=자료위치.ኣድራሻ&&실행머리.ምእታው_ነጥቢ-자료위치.ኣድራሻ<자료위치.파일영역크기&&!(실행머리.ምእታው_ነጥቢ&3))진입점정상=1;
            size_t 선행값=자료위치.ኣድራሻ&4095,바이트들=자료위치.파일영역크기?선행값+자료위치.파일영역크기:0;
            if(다음>sizeof(ምስሊ)||바이트들>sizeof(ምስሊ)-다음){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(다음+바이트들),(unsigned)sizeof(ምስሊ));return -1;}
            if(바이트들)memcpy(ምስሊ+다음+선행값,원본자료+자료위치.ሽፋን_ዋጋ,자료위치.파일영역크기);
            자료위치.ኣድራሻ-=선행값;자료위치.물리주소=자료위치.ኣድራሻ;자료위치.기억영역크기+=선행값;자료위치.파일영역크기=바이트들;자료위치.ሽፋን_ዋጋ=다음;자료위치.맞춤=4096;
            for(uint64_t ገጽ_ዋጋ=자료위치.ኣድራሻ;ገጽ_ዋጋ<자료위치.ኣድራሻ+자료위치.기억영역크기;ገጽ_ዋጋ+=4096){unsigned 색인=(ገጽ_ዋጋ-0x02000000)/4096;if(색인>=sizeof(ገጽ_ዝርዝር)||ገጽ_ዝርዝር[색인]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}ገጽ_ዝርዝር[색인]=1;}
            다음+=(바이트들+4095)&~(size_t)4095;
        }else if(자료위치.ዓይነት_መደብ==4){if(자료위치.파일영역크기>4096-부가정보)return -1;memcpy(ምስሊ+부가정보,원본자료+자료위치.ሽፋን_ዋጋ,자료위치.파일영역크기);자료위치.ሽፋን_ዋጋ=부가정보;부가정보+=자료위치.파일영역크기;}
        else if(자료위치.ዓይነት_መደብ!=0&&자료위치.ዓይነት_መደብ!=6&&자료위치.ዓይነት_መደብ!=0x6474e551)return -1;
        memcpy(ምስሊ+실행머리.መተግበሪ_ርእሲ_ሽፋን+순번*sizeof(자료위치),&자료위치,sizeof(자료위치));
    }
    if(!진입점정상)return -1;
    intptr_t ፋይል_መትሓዚ=사용자호출(3,(uintptr_t)ሽም,577,0600,0,0,0);if(ፋይል_መትሓዚ<0){printf("cc: cannot create output file, error %d\n",(int)ፋይል_መትሓዚ);return -1;}
    intptr_t 쓴수=사용자호출(1,ፋይል_መትሓዚ,(uintptr_t)ምስሊ,다음,0,0,0);사용자호출(4,ፋይል_መትሓዚ,0,0,0,0,0);return 쓴수==(intptr_t)다음?0:-1;
}
int ጀምር_ተጠቃሚ_መተግበሪ(int ሜላ_ኹነት){
    char 입력결과[256],선택항목[256],출력결과[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(ሜላ_ኹነት?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)입력결과,sizeof(입력결과),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(입력결과,"--version")||!strcmp(입력결과,"-version"))){printf(ሜላ_ኹነት?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)출력결과,sizeof(출력결과),0,0,0)<0)return 2;}
    if(!strcmp(입력결과,출력결과)){printf("cc: input and output must differ\n");return 2;}
    TCCState*ሕብረ_ቁምፊ_ሓበሬታ=tcc_new();if(!ሕብረ_ቁምፊ_ሓበሬታ)return 1;
    tcc_undefine_symbol(ሕብረ_ቁምፊ_ሓበሬታ,"__linux__");tcc_undefine_symbol(ሕብረ_ቁምፊ_ሓበሬታ,"__linux");tcc_undefine_symbol(ሕብረ_ቁምፊ_ሓበሬታ,"linux");
    tcc_undefine_symbol(ሕብረ_ቁምፊ_ሓበሬታ,"__unix__");tcc_undefine_symbol(ሕብረ_ቁምፊ_ሓበሬታ,"__unix");tcc_undefine_symbol(ሕብረ_ቁምፊ_ሓበሬታ,"unix");
    tcc_undefine_symbol(ሕብረ_ቁምፊ_ሓበሬታ,"__STDC_HOSTED__");tcc_define_symbol(ሕብረ_ቁምፊ_ሓበሬታ,"__STDC_HOSTED__","0");tcc_define_symbol(ሕብረ_ቁምፊ_ሓበሬታ,"__JKOROS__","1");
    tcc_set_options(ሕብረ_ቁምፊ_ሓበሬታ,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(ሕብረ_ቁምፊ_ሓበሬታ,"/sdk/include");
    int 반환값=tcc_set_output_type(ሕብረ_ቁምፊ_ሓበሬታ,TCC_OUTPUT_EXE);
    if(!반환값){if(ሜላ_ኹነት){const char*원본자료=자바미리번역원문(입력결과);반환값=원본자료?tcc_compile_string(ሕብረ_ቁምፊ_ሓበሬታ,원본자료):-1;}else 반환값=tcc_add_file(ሕብረ_ቁምፊ_ሓበሬታ,입력결과);}
    if(!반환값)반환값=tcc_add_file(ሕብረ_ቁምፊ_ሓበሬታ,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(ሕብረ_ቁምፊ_ሓበሬታ,"/sdk/lib/crt.o");
    if(!반환값&&ሜላ_ኹነት)반환값=tcc_add_file(ሕብረ_ቁምፊ_ሓበሬታ,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(ሕብረ_ቁምፊ_ሓበሬታ,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(ሕብረ_ቁምፊ_ሓበሬታ,"/@cc-output");
    if(!반환값)반환값=ሓትም_ምእታው(출력결과);
    tcc_delete(ሕብረ_ቁምፊ_ሓበሬታ);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(ሜላ_ኹነት?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",출력결과);return 0;
}
