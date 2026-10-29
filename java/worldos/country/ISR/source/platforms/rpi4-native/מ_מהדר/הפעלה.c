#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *מ_פלט(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char מזהה_ערך[16];uint16_t כתב_אזור,מחשב_כתב;uint32_t מספר_גירסה;uint64_t נקודת_כניסה,תוכנית_כותרת_היסט,כותרת_מקטע_עליונה_היסט;uint32_t 설정비트;uint16_t גודל,תוכנית_כותרת_גודל,프로그램머리개수,כותרת_מקטע_עליונה_גודל,구역머리개수,מקטע_שם_טבלה; } כותרת_ערך;
typedef struct {uint32_t כתב_אזור,설정비트;uint64_t היסט_ערך,למען,물리주소,파일영역크기,기억영역크기,맞춤;} פלח_ערך;
static unsigned char תמונה[16384];
static int פרסם_ערך_98c1574d(const char *שם){
    size_t 개수;const unsigned char*원본자료=מ_פלט(&개수);if(개수<sizeof(כותרת_ערך))return -1;
    כותרת_ערך 실행머리;memcpy(&실행머리,원본자료,sizeof(실행머리));
    if(실행머리.כתב_אזור!=2||실행머리.מחשב_כתב!=183||실행머리.תוכנית_כותרת_גודל!=sizeof(פלח_ערך)||!실행머리.프로그램머리개수||실행머리.프로그램머리개수>16||실행머리.תוכנית_כותרת_היסט>개수||실행머리.프로그램머리개수*sizeof(פלח_ערך)>개수-실행머리.תוכנית_כותרת_היסט)return -1;
    실행머리.תוכנית_כותרת_היסט=sizeof(실행머리);실행머리.כותרת_מקטע_עליונה_היסט=실행머리.구역머리개수=실행머리.כותרת_מקטע_עליונה_גודל=실행머리.מקטע_שם_טבלה=0;memcpy(תמונה,&실행머리,sizeof(실행머리));
    size_t 부가정보=sizeof(실행머리)+실행머리.프로그램머리개수*sizeof(פלח_ערך),הבא_פריט=4096;unsigned char דף_רשימה[3072]={0};int 진입점정상=0;
    for(unsigned 순번=0;순번<실행머리.프로그램머리개수;순번++){
        פלח_ערך נתונים_עמדה;כותרת_ערך 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&נתונים_עמדה,원본자료+원본.תוכנית_כותרת_היסט+순번*sizeof(נתונים_עמדה),sizeof(נתונים_עמדה));
        if(נתונים_עמדה.היסט_ערך>개수||נתונים_עמדה.파일영역크기>개수-נתונים_עמדה.היסט_ערך||נתונים_עמדה.파일영역크기>נתונים_עמדה.기억영역크기)return -1;
        if(נתונים_עמדה.כתב_אזור==1){
            if((נתונים_עמדה.설정비트&~7u)||!(נתונים_עמדה.설정비트&4)||(נתונים_עמדה.설정비트&3)==3||נתונים_עמדה.למען<0x02000000||נתונים_עמדה.למען>0x02c00000||נתונים_עמדה.기억영역크기>0x02c00000-נתונים_עמדה.למען)return -1;
            if((נתונים_עמדה.설정비트&1)&&실행머리.נקודת_כניסה>=נתונים_עמדה.למען&&실행머리.נקודת_כניסה-נתונים_עמדה.למען<נתונים_עמדה.파일영역크기&&!(실행머리.נקודת_כניסה&3))진입점정상=1;
            size_t 선행값=נתונים_עמדה.למען&4095,바이트들=נתונים_עמדה.파일영역크기?선행값+נתונים_עמדה.파일영역크기:0;
            if(הבא_פריט>sizeof(תמונה)||바이트들>sizeof(תמונה)-הבא_פריט){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(הבא_פריט+바이트들),(unsigned)sizeof(תמונה));return -1;}
            if(바이트들)memcpy(תמונה+הבא_פריט+선행값,원본자료+נתונים_עמדה.היסט_ערך,נתונים_עמדה.파일영역크기);
            נתונים_עמדה.למען-=선행값;נתונים_עמדה.물리주소=נתונים_עמדה.למען;נתונים_עמדה.기억영역크기+=선행값;נתונים_עמדה.파일영역크기=바이트들;נתונים_עמדה.היסט_ערך=הבא_פריט;נתונים_עמדה.맞춤=4096;
            for(uint64_t דף_ערך=נתונים_עמדה.למען;דף_ערך<נתונים_עמדה.למען+נתונים_עמדה.기억영역크기;דף_ערך+=4096){unsigned חפושׂ_מדד=(דף_ערך-0x02000000)/4096;if(חפושׂ_מדד>=sizeof(דף_רשימה)||דף_רשימה[חפושׂ_מדד]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}דף_רשימה[חפושׂ_מדד]=1;}
            הבא_פריט+=(바이트들+4095)&~(size_t)4095;
        }else if(נתונים_עמדה.כתב_אזור==4){if(נתונים_עמדה.파일영역크기>4096-부가정보)return -1;memcpy(תמונה+부가정보,원본자료+נתונים_עמדה.היסט_ערך,נתונים_עמדה.파일영역크기);נתונים_עמדה.היסט_ערך=부가정보;부가정보+=נתונים_עמדה.파일영역크기;}
        else if(נתונים_עמדה.כתב_אזור!=0&&נתונים_עמדה.כתב_אזור!=6&&נתונים_עמדה.כתב_אזור!=0x6474e551)return -1;
        memcpy(תמונה+실행머리.תוכנית_כותרת_היסט+순번*sizeof(נתונים_עמדה),&נתונים_עמדה,sizeof(נתונים_עמדה));
    }
    if(!진입점정상)return -1;
    intptr_t קובץ_נקודת_אחיזה=사용자호출(3,(uintptr_t)שם,577,0600,0,0,0);if(קובץ_נקודת_אחיזה<0){printf("cc: cannot create output file, error %d\n",(int)קובץ_נקודת_אחיזה);return -1;}
    intptr_t 쓴수=사용자호출(1,קובץ_נקודת_אחיזה,(uintptr_t)תמונה,הבא_פריט,0,0,0);사용자호출(4,קובץ_נקודת_אחיזה,0,0,0,0,0);return 쓴수==(intptr_t)הבא_פריט?0:-1;
}
int התחל_משתמש_תוכנית(int פעולת_שירות_מצב){
    char קלט[256],선택항목[256],פלט[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(פעולת_שירות_מצב?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)קלט,sizeof(קלט),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(קלט,"--version")||!strcmp(קלט,"-version"))){printf(פעולת_שירות_מצב?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)פלט,sizeof(פלט),0,0,0)<0)return 2;}
    if(!strcmp(קלט,פלט)){printf("cc: input and output must differ\n");return 2;}
    TCCState*מחרוזת_נתונים=tcc_new();if(!מחרוזת_נתונים)return 1;
    tcc_undefine_symbol(מחרוזת_נתונים,"__linux__");tcc_undefine_symbol(מחרוזת_נתונים,"__linux");tcc_undefine_symbol(מחרוזת_נתונים,"linux");
    tcc_undefine_symbol(מחרוזת_נתונים,"__unix__");tcc_undefine_symbol(מחרוזת_נתונים,"__unix");tcc_undefine_symbol(מחרוזת_נתונים,"unix");
    tcc_undefine_symbol(מחרוזת_נתונים,"__STDC_HOSTED__");tcc_define_symbol(מחרוזת_נתונים,"__STDC_HOSTED__","0");tcc_define_symbol(מחרוזת_נתונים,"__JKOROS__","1");
    tcc_set_options(מחרוזת_נתונים,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(מחרוזת_נתונים,"/sdk/include");
    int 반환값=tcc_set_output_type(מחרוזת_נתונים,TCC_OUTPUT_EXE);
    if(!반환값){if(פעולת_שירות_מצב){const char*원본자료=자바미리번역원문(קלט);반환값=원본자료?tcc_compile_string(מחרוזת_נתונים,원본자료):-1;}else 반환값=tcc_add_file(מחרוזת_נתונים,קלט);}
    if(!반환값)반환값=tcc_add_file(מחרוזת_נתונים,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(מחרוזת_נתונים,"/sdk/lib/crt.o");
    if(!반환값&&פעולת_שירות_מצב)반환값=tcc_add_file(מחרוזת_נתונים,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(מחרוזת_נתונים,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(מחרוזת_נתונים,"/@cc-output");
    if(!반환값)반환값=פרסם_ערך_98c1574d(פלט);
    tcc_delete(מחרוזת_נתונים);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(פעולת_שירות_מצב?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",פלט);return 0;
}
