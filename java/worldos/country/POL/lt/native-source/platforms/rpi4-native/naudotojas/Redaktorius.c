/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Redaktorius_pajėgumas 16384
static unsigned char Tekstas[Redaktorius_pajėgumas],anuliuoti_duomenys[Redaktorius_pajėgumas],복사자료[Redaktorius_pajėgumas],KR_duomenys[1024];
static int 길이,INDEX_VALUE,맨위,왼쪽,변경됨,Įterpimas,되돌림길이,위쪽,anuliuoti_Keitimai,되돌림있음,복사길이,사용량,COLUMNS=68,ROW_COUNT=19;
static char Failas_įrašas_pavadinimas[64],Komanda[128],FIND_įrašas[128];
static const char *pranešimas_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned laukiama_Raktas;
static int žinynas_sritis,Būsena_IMAGE,Būsena_eilė;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_duomenys,사용량,0,0,0);사용량=0;}}
static void baitas_duomenys(unsigned simbolio_kodas){if(Būsena_IMAGE){if((simbolio_kodas&192)!=128){Būsena_eilė+=simbolio_kodas>=196?2:1;}if(Būsena_eilė>=COLUMNS)return;}if(사용량==(int)sizeof(KR_duomenys))출력비우기();KR_duomenys[사용량++]=simbolio_kodas;}
static void 글내보내기(const char *eilutė_duomenys){while(*eilutė_duomenys)baitas_duomenys((unsigned char)*eilutė_duomenys++);}
static void 수치(unsigned prekė_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+prekė_COUNT%10;prekė_COUNT/=10;}while(prekė_COUNT);while(순번)baitas_duomenys(SECOND_VALUE[--순번]);}
static void judėti_VALUE(int ROW_padėtis,int COLUMN_padėtis){글내보내기("\033[");수치(ROW_padėtis);baitas_duomenys(';');수치(COLUMN_padėtis);baitas_duomenys('H');}
static int 이전항목(int duomenys_padėtis){if(duomenys_padėtis){duomenys_padėtis--;while(duomenys_padėtis>0&&(Tekstas[duomenys_padėtis]&192)==128)duomenys_padėtis--;}return duomenys_padėtis;}
static int toliau_prekė(int duomenys_padėtis){if(duomenys_padėtis<길이){duomenys_padėtis++;while(duomenys_padėtis<길이&&(Tekstas[duomenys_padėtis]&192)==128)duomenys_padėtis++;}return duomenys_padėtis;}
static int Paleisti(int duomenys_padėtis){while(duomenys_padėtis>0&&Tekstas[duomenys_padėtis-1]!='\n')duomenys_padėtis--;return duomenys_padėtis;}
static int baigti_pokalbį_OFFSET(int duomenys_padėtis){while(duomenys_padėtis<길이&&Tekstas[duomenys_padėtis]!='\n')duomenys_padėtis++;return duomenys_padėtis;}
static int 너비(unsigned simbolio_kodas){return simbolio_kodas>=196?2:1;}
static int COLUMN(int duomenys_padėtis){int simbolio_kodas=0;for(int 순번=Paleisti(duomenys_padėtis);순번<duomenys_padėtis;순번=toliau_prekė(순번))simbolio_kodas+=Tekstas[순번]=='\t'?4-simbolio_kodas%4:너비(Tekstas[순번]);return simbolio_kodas;}
static void kontrolinis_taškas(void){for(int 순번=0;순번<길이;순번++)anuliuoti_duomenys[순번]=Tekstas[순번];되돌림길이=길이;위쪽=INDEX_VALUE;anuliuoti_Keitimai=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrolinis_taškas();for(int 순번=도착위치;순번<길이;순번++)Tekstas[출발위치+순번-도착위치]=Tekstas[순번];길이-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int sujungti_VALUE(const unsigned char *eilutė_duomenys,int prekė_COUNT){if(prekė_COUNT>Redaktorius_pajėgumas-길이){pranešimas_SMS="File full (16384 bytes)";return 0;}kontrolinis_taškas();for(int 순번=길이-1;순번>=INDEX_VALUE;순번--)Tekstas[순번+prekė_COUNT]=Tekstas[순번];for(int 순번=0;순번<prekė_COUNT;순번++)Tekstas[INDEX_VALUE+순번]=eilutė_duomenys[순번];길이+=prekė_COUNT;INDEX_VALUE+=prekė_COUNT;변경됨=1;return 1;}
static void segmentas(int 차이){int COLUMN_padėtis=COLUMN(INDEX_VALUE),duomenys_padėtis=Paleisti(INDEX_VALUE);if(차이<0){if(!duomenys_padėtis)return;duomenys_padėtis=Paleisti(duomenys_padėtis-1);}else{duomenys_padėtis=baigti_pokalbį_OFFSET(duomenys_padėtis);if(duomenys_padėtis==길이)return;duomenys_padėtis++;}int simbolio_kodas=0;while(duomenys_padėtis<길이&&Tekstas[duomenys_padėtis]!='\n'&&simbolio_kodas<COLUMN_padėtis){simbolio_kodas+=Tekstas[duomenys_padėtis]=='\t'?4-simbolio_kodas%4:너비(Tekstas[duomenys_padėtis]);duomenys_padėtis=toliau_prekė(duomenys_padėtis);}INDEX_VALUE=duomenys_padėtis;}
static void 화면그리기(void){
    if(INDEX_VALUE>길이)INDEX_VALUE=길이;if(맨위>INDEX_VALUE)맨위=Paleisti(INDEX_VALUE);맨위=Paleisti(맨위);
    int ROW_padėtis=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Tekstas[순번]=='\n')ROW_padėtis++;
    while(ROW_padėtis>=ROW_COUNT-1){맨위=baigti_pokalbį_OFFSET(맨위);if(맨위<길이)맨위++;ROW_padėtis--;}
    int COLUMN_padėtis=COLUMN(INDEX_VALUE);if(COLUMN_padėtis<왼쪽)왼쪽=COLUMN_padėtis;if(COLUMN_padėtis-왼쪽>=COLUMNS-1)왼쪽=COLUMN_padėtis-COLUMNS+2;
    글내보내기("\033[?25l");int duomenys_padėtis=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        judėti_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int simbolio_kodas=0,그려진상태=0;
        if(duomenys_padėtis>=길이&&반환값>ROW_padėtis){글내보내기("\033[90m~\033[0m");continue;}
        while(duomenys_padėtis<길이&&Tekstas[duomenys_padėtis]!='\n'){
            int toliau_OFFSET=toliau_prekė(duomenys_padėtis),너비값=Tekstas[duomenys_padėtis]=='\t'?4-simbolio_kodas%4:너비(Tekstas[duomenys_padėtis]);
            if(simbolio_kodas>=왼쪽&&simbolio_kodas-왼쪽+너비값<COLUMNS){
                if(Tekstas[duomenys_padėtis]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)baitas_duomenys(' ');}else if(Tekstas[duomenys_padėtis]<32||Tekstas[duomenys_padėtis]==127){baitas_duomenys('?');}else for(int 안쪽순번=duomenys_padėtis;안쪽순번<toliau_OFFSET;안쪽순번++)baitas_duomenys(Tekstas[안쪽순번]);그려진상태+=너비값;
            }simbolio_kodas+=너비값;duomenys_padėtis=toliau_OFFSET;
        }
        (void)그려진상태;if(duomenys_padėtis<길이)duomenys_padėtis++;
    }
    judėti_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");Būsena_IMAGE=1;Būsena_eilė=0;글내보내기(Įterpimas?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Failas_įrašas_pavadinimas[이름바이트수]&&이름바이트수<30)baitas_duomenys(Failas_įrašas_pavadinimas[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Eilutė=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Tekstas[순번]=='\n')Eilutė++;수치(Eilutė);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(pranešimas_SMS){int prekė_COUNT=0;글내보내기(" | ");while(pranešimas_SMS[prekė_COUNT]&&prekė_COUNT<20)baitas_duomenys(pranešimas_SMS[prekė_COUNT++]);}
    Būsena_IMAGE=0;글내보내기("\033[0m");judėti_VALUE(ROW_padėtis+1,COLUMN_padėtis-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(laukiama_Raktas){int 셋째순번=laukiama_Raktas;laukiama_Raktas=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Dydis=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Dydis&65535)||ROW_COUNT!=(int)(Dydis>>16)){
            COLUMNS=Dydis&65535;ROW_COUNT=Dydis>>16;화면그리기();
            if(žinynas_sritis){judėti_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");baitas_duomenys(žinynas_sritis);글내보내기(Komanda);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned dabartinis_padėtis=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-dabartinis_padėtis<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){laukiama_Raktas=셋째순번;return 27;}
    int prekė_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){prekė_COUNT=prekė_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return prekė_COUNT==3?1007:prekė_COUNT==5?1008:prekė_COUNT==6?1009:prekė_COUNT==1?1005:prekė_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int Failas_rodyklė=kurti_Failas(Failas_įrašas_pavadinimas,읽고쓰기|없으면만들기|trumpinti_Turinys,0600);if(Failas_rodyklė<0){pranešimas_SMS="Cannot open for save";return 0;}
    intptr_t prekė_COUNT=rašymas_Failas_duomenys(Failas_rodyklė,Tekstas,길이);Uždaryti_Failas(Failas_rodyklė);if(prekė_COUNT!=길이){pranešimas_SMS="Write failed";return 0;}변경됨=0;pranešimas_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_toliau(void){int prekė_COUNT=0;while(FIND_įrašas[prekė_COUNT])prekė_COUNT++;if(!prekė_COUNT){pranešimas_SMS="No search pattern";return;}for(int 순번=1;순번<=길이;순번++){int duomenys_padėtis=(INDEX_VALUE+순번)%(길이?길이:1),안쪽순번=0;while(안쪽순번<prekė_COUNT&&duomenys_padėtis+안쪽순번<길이&&Tekstas[duomenys_padėtis+안쪽순번]==(unsigned char)FIND_įrašas[안쪽순번])안쪽순번++;if(안쪽순번==prekė_COUNT){INDEX_VALUE=duomenys_padėtis;pranešimas_SMS="Match";return;}}pranešimas_SMS="Pattern not found";}
static int raginimas(int sritis_VALUE){
    int prekė_COUNT=0;Komanda[0]=0;
    for(;;){judėti_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");baitas_duomenys(sritis_VALUE);글내보내기(Komanda);출력비우기();žinynas_sritis=sritis_VALUE;int 셋째순번=누름값();žinynas_sritis=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(prekė_COUNT){prekė_COUNT--;while(prekė_COUNT>0&&((unsigned char)Komanda[prekė_COUNT]&192)==128)prekė_COUNT--;Komanda[prekė_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&prekė_COUNT<120){Komanda[prekė_COUNT++]=셋째순번;Komanda[prekė_COUNT]=0;}
    }
    if(sritis_VALUE=='/'){for(int 순번=0;순번<=prekė_COUNT;순번++)FIND_įrašas[순번]=Komanda[순번];FIND_toliau();return 0;}
    if(같은지(Komanda,"q!"))return 1;
    if(같은지(Komanda,"q")){if(!변경됨)return 1;pranešimas_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(Komanda,"wq")||같은지(Komanda,"x"))return Store_VALUE();
    if(같은지(Komanda,"w")){Store_VALUE();return 0;}
    if(Komanda[0]=='w'&&Komanda[1]==' '){int 순번=2;while(Komanda[순번]==' ')순번++;int Dydis=prekė_COUNT-순번;if(Dydis<1||Dydis>63){pranešimas_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Dydis;안쪽순번++)Failas_įrašas_pavadinimas[안쪽순번]=Komanda[순번+안쪽순번];Failas_įrašas_pavadinimas[Dydis]=0;Store_VALUE();return 0;}
    int Eilutė=0;for(int 순번=0;순번<prekė_COUNT;순번++){if(Komanda[순번]<'0'||Komanda[순번]>'9'){Eilutė=0;break;}Eilutė=Eilutė*10+Komanda[순번]-'0';if(Eilutė>16384){Eilutė=0;break;}}
    if(Eilutė){INDEX_VALUE=0;while(--Eilutė&&INDEX_VALUE<길이){INDEX_VALUE=baigti_pokalbį_OFFSET(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;}return 0;}
    pranešimas_SMS="Unknown vi command";return 0;
}
int Start_naudotojas_programa(int 무시값){
    (void)무시값;if(naudotojas_argumentas_COUNT()!=1||naudotojas_argumentas(0,Failas_įrašas_pavadinimas,sizeof(Failas_įrašas_pavadinimas))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Failas_rodyklė=kurti_Failas(Failas_įrašas_pavadinimas,tik_skaitomas_VALUE,0);
    if(Failas_rodyklė>=0){int prekė_COUNT=failo_dydis(Failas_rodyklė);if(prekė_COUNT<0||prekė_COUNT>Redaktorius_pajėgumas){Uždaryti_Failas(Failas_rodyklė);return 1;}길이=파일자료읽기(Failas_rodyklė,Tekstas,prekė_COUNT);Uždaryti_Failas(Failas_rodyklė);if(길이!=prekė_COUNT)return 1;for(int 순번=0;순번<길이;순번++)if(!Tekstas[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(klaidos_numeris!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,išeiti_programa=0;
    while(!išeiti_programa){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();pranešimas_SMS=0;
        if(셋째순번==1001){segmentas(-1);continue;}if(셋째순번==1002){segmentas(1);continue;}if(셋째순번==1003){INDEX_VALUE=toliau_prekė(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Paleisti(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=baigti_pokalbį_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)segmentas(셋째순번==1008?-1:1);continue;}
        if(Įterpimas){
            if(셋째순번==27||셋째순번==3){Įterpimas=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,toliau_prekė(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int prekė_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!prekė_COUNT){pranešimas_SMS="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<prekė_COUNT;순번++){int simbolio_kodas=누름값();if(simbolio_kodas<128||simbolio_kodas>191){laukiama_Raktas=simbolio_kodas;유효함=0;break;}SECOND_VALUE[순번]=simbolio_kodas;}
                if(유효함)sujungti_VALUE(SECOND_VALUE,prekė_COUNT);
            }continue;
        }
        if(앞부분){int duomenys_padėtis=앞부분;앞부분=0;if(duomenys_padėtis=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(duomenys_padėtis=='Z'&&셋째순번=='Z'){išeiti_programa=Store_VALUE();continue;}if((duomenys_padėtis=='d'&&셋째순번=='d')||(duomenys_padėtis=='y'&&셋째순번=='y')){int 첫째값=Paleisti(INDEX_VALUE),SECOND_VALUE=baigti_pokalbį_OFFSET(INDEX_VALUE);if(SECOND_VALUE<길이)SECOND_VALUE++;복사길이=SECOND_VALUE-첫째값;for(int 순번=0;순번<복사길이;순번++)복사자료[순번]=Tekstas[첫째값+순번];if(duomenys_padėtis=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Įterpimas=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<baigti_pokalbį_OFFSET(INDEX_VALUE))INDEX_VALUE=toliau_prekė(INDEX_VALUE);Įterpimas=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Paleisti(INDEX_VALUE);Įterpimas=1;continue;}if(셋째순번=='A'){INDEX_VALUE=baigti_pokalbį_OFFSET(INDEX_VALUE);Įterpimas=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char eilutė_baigti_pokalbį='\n';INDEX_VALUE=셋째순번=='o'?baigti_pokalbį_OFFSET(INDEX_VALUE):Paleisti(INDEX_VALUE);if(sujungti_VALUE(&eilutė_baigti_pokalbį,1)){if(셋째순번=='O')INDEX_VALUE--;Įterpimas=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=toliau_prekė(INDEX_VALUE);continue;}if(셋째순번=='j'){segmentas(1);continue;}if(셋째순번=='k'){segmentas(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Paleisti(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=baigti_pokalbį_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Paleisti(길이);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,toliau_prekė(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&복사길이){INDEX_VALUE=baigti_pokalbį_OFFSET(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;sujungti_VALUE(복사자료,복사길이);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Redaktorius_pajėgumas;순번++){unsigned char SECOND_VALUE=Tekstas[순번];Tekstas[순번]=anuliuoti_duomenys[순번];anuliuoti_duomenys[순번]=SECOND_VALUE;}int prekė_COUNT=길이;길이=되돌림길이;되돌림길이=prekė_COUNT;prekė_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=prekė_COUNT;prekė_COUNT=변경됨;변경됨=anuliuoti_Keitimai;anuliuoti_Keitimai=prekė_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){išeiti_programa=raginimas(셋째순번);continue;}if(셋째순번=='n'){FIND_toliau();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
