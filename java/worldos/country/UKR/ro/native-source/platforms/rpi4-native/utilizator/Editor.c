/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Editor_capacitate 16384
static unsigned char SMS[Editor_capacitate],anulare_date[Editor_capacitate],복사자료[Editor_capacitate],KR_date[1024];
static int lungime_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,Inserare,anulare_lungime,위쪽,anulare_Modificări,되돌림있음,copia_lungime,사용량,COLUMNS=68,ROW_COUNT=19;
static char Fișier_intrare_nume[64],Comandă[128],FIND_intrare[128];
static const char *înștiințare_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned în_așteptare_Cheie;
static int ajutor_zonă,Stare_IMAGE,Stare_coadă;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_date,사용량,0,0,0);사용량=0;}}
static void byte_date(unsigned cod_caracter){if(Stare_IMAGE){if((cod_caracter&192)!=128){Stare_coadă+=cod_caracter>=196?2:1;}if(Stare_coadă>=COLUMNS)return;}if(사용량==(int)sizeof(KR_date))출력비우기();KR_date[사용량++]=cod_caracter;}
static void 글내보내기(const char *șir_date){while(*șir_date)byte_date((unsigned char)*șir_date++);}
static void 수치(unsigned element_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+element_COUNT%10;element_COUNT/=10;}while(element_COUNT);while(순번)byte_date(SECOND_VALUE[--순번]);}
static void muta_VALUE_83b651b8(int ROW_poziție,int COLUMN_poziție){글내보내기("\033[");수치(ROW_poziție);byte_date(';');수치(COLUMN_poziție);byte_date('H');}
static int Anteriorul(int date_poziție){if(date_poziție){date_poziție--;while(date_poziție>0&&(SMS[date_poziție]&192)==128)date_poziție--;}return date_poziție;}
static int Următorul_element(int date_poziție){if(date_poziție<lungime_VALUE){date_poziție++;while(date_poziție<lungime_VALUE&&(SMS[date_poziție]&192)==128)date_poziție++;}return date_poziție;}
static int Pornește(int date_poziție){while(date_poziție>0&&SMS[date_poziție-1]!='\n')date_poziție--;return date_poziție;}
static int termina_un_apel_OFFSET(int date_poziție){while(date_poziție<lungime_VALUE&&SMS[date_poziție]!='\n')date_poziție++;return date_poziție;}
static int 너비(unsigned cod_caracter){return cod_caracter>=196?2:1;}
static int COLUMN(int date_poziție){int cod_caracter=0;for(int 순번=Pornește(date_poziție);순번<date_poziție;순번=Următorul_element(순번))cod_caracter+=SMS[순번]=='\t'?4-cod_caracter%4:너비(SMS[순번]);return cod_caracter;}
static void punct_de_control(void){for(int 순번=0;순번<lungime_VALUE;순번++)anulare_date[순번]=SMS[순번];anulare_lungime=lungime_VALUE;위쪽=INDEX_VALUE;anulare_Modificări=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){punct_de_control();for(int 순번=도착위치;순번<lungime_VALUE;순번++)SMS[출발위치+순번-도착위치]=SMS[순번];lungime_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int adăuga_VALUE(const unsigned char *șir_date,int element_COUNT){if(element_COUNT>Editor_capacitate-lungime_VALUE){înștiințare_SMS="File full (16384 bytes)";return 0;}punct_de_control();for(int 순번=lungime_VALUE-1;순번>=INDEX_VALUE;순번--)SMS[순번+element_COUNT]=SMS[순번];for(int 순번=0;순번<element_COUNT;순번++)SMS[INDEX_VALUE+순번]=șir_date[순번];lungime_VALUE+=element_COUNT;INDEX_VALUE+=element_COUNT;변경됨=1;return 1;}
static void Verticală(int 차이){int COLUMN_poziție=COLUMN(INDEX_VALUE),date_poziție=Pornește(INDEX_VALUE);if(차이<0){if(!date_poziție)return;date_poziție=Pornește(date_poziție-1);}else{date_poziție=termina_un_apel_OFFSET(date_poziție);if(date_poziție==lungime_VALUE)return;date_poziție++;}int cod_caracter=0;while(date_poziție<lungime_VALUE&&SMS[date_poziție]!='\n'&&cod_caracter<COLUMN_poziție){cod_caracter+=SMS[date_poziție]=='\t'?4-cod_caracter%4:너비(SMS[date_poziție]);date_poziție=Următorul_element(date_poziție);}INDEX_VALUE=date_poziție;}
static void 화면그리기(void){
    if(INDEX_VALUE>lungime_VALUE)INDEX_VALUE=lungime_VALUE;if(맨위>INDEX_VALUE)맨위=Pornește(INDEX_VALUE);맨위=Pornește(맨위);
    int ROW_poziție=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')ROW_poziție++;
    while(ROW_poziție>=ROW_COUNT-1){맨위=termina_un_apel_OFFSET(맨위);if(맨위<lungime_VALUE)맨위++;ROW_poziție--;}
    int COLUMN_poziție=COLUMN(INDEX_VALUE);if(COLUMN_poziție<왼쪽)왼쪽=COLUMN_poziție;if(COLUMN_poziție-왼쪽>=COLUMNS-1)왼쪽=COLUMN_poziție-COLUMNS+2;
    글내보내기("\033[?25l");int date_poziție=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        muta_VALUE_83b651b8(반환값+1,1);글내보내기("\033[0m\033[2K");int cod_caracter=0,그려진상태=0;
        if(date_poziție>=lungime_VALUE&&반환값>ROW_poziție){글내보내기("\033[90m~\033[0m");continue;}
        while(date_poziție<lungime_VALUE&&SMS[date_poziție]!='\n'){
            int Următorul_OFFSET=Următorul_element(date_poziție),너비값=SMS[date_poziție]=='\t'?4-cod_caracter%4:너비(SMS[date_poziție]);
            if(cod_caracter>=왼쪽&&cod_caracter-왼쪽+너비값<COLUMNS){
                if(SMS[date_poziție]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_date(' ');}else if(SMS[date_poziție]<32||SMS[date_poziție]==127){byte_date('?');}else for(int 안쪽순번=date_poziție;안쪽순번<Următorul_OFFSET;안쪽순번++)byte_date(SMS[안쪽순번]);그려진상태+=너비값;
            }cod_caracter+=너비값;date_poziție=Următorul_OFFSET;
        }
        (void)그려진상태;if(date_poziție<lungime_VALUE)date_poziție++;
    }
    muta_VALUE_83b651b8(ROW_COUNT,1);글내보내기("\033[7m\033[2K");Stare_IMAGE=1;Stare_coadă=0;글내보내기(Inserare?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Fișier_intrare_nume[이름바이트수]&&이름바이트수<30)byte_date(Fișier_intrare_nume[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Linie=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(SMS[순번]=='\n')Linie++;수치(Linie);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(înștiințare_SMS){int element_COUNT=0;글내보내기(" | ");while(înștiințare_SMS[element_COUNT]&&element_COUNT<20)byte_date(înștiințare_SMS[element_COUNT++]);}
    Stare_IMAGE=0;글내보내기("\033[0m");muta_VALUE_83b651b8(ROW_poziție+1,COLUMN_poziție-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(în_așteptare_Cheie){int 셋째순번=în_așteptare_Cheie;în_așteptare_Cheie=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Mărime=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Mărime&65535)||ROW_COUNT!=(int)(Mărime>>16)){
            COLUMNS=Mărime&65535;ROW_COUNT=Mărime>>16;화면그리기();
            if(ajutor_zonă){muta_VALUE_83b651b8(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_date(ajutor_zonă);글내보내기(Comandă);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned curent_poziție=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-curent_poziție<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){în_așteptare_Cheie=셋째순번;return 27;}
    int element_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){element_COUNT=element_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return element_COUNT==3?1007:element_COUNT==5?1008:element_COUNT==6?1009:element_COUNT==1?1005:element_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int Fișier_handle=crea_Fișier(Fișier_intrare_nume,citire_scriere|없으면만들기|trunchia_TOC,0600);if(Fișier_handle<0){înștiințare_SMS="Cannot open for save";return 0;}
    intptr_t element_COUNT=scriere_Fișier_date(Fișier_handle,SMS,lungime_VALUE);închide_Fișier(Fișier_handle);if(element_COUNT!=lungime_VALUE){înștiințare_SMS="Write failed";return 0;}변경됨=0;înștiințare_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Următorul(void){int element_COUNT=0;while(FIND_intrare[element_COUNT])element_COUNT++;if(!element_COUNT){înștiințare_SMS="No search pattern";return;}for(int 순번=1;순번<=lungime_VALUE;순번++){int date_poziție=(INDEX_VALUE+순번)%(lungime_VALUE?lungime_VALUE:1),안쪽순번=0;while(안쪽순번<element_COUNT&&date_poziție+안쪽순번<lungime_VALUE&&SMS[date_poziție+안쪽순번]==(unsigned char)FIND_intrare[안쪽순번])안쪽순번++;if(안쪽순번==element_COUNT){INDEX_VALUE=date_poziție;înștiințare_SMS="Match";return;}}înștiințare_SMS="Pattern not found";}
static int solicita(int zonă_VALUE){
    int element_COUNT=0;Comandă[0]=0;
    for(;;){muta_VALUE_83b651b8(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_date(zonă_VALUE);글내보내기(Comandă);출력비우기();ajutor_zonă=zonă_VALUE;int 셋째순번=누름값();ajutor_zonă=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(element_COUNT){element_COUNT--;while(element_COUNT>0&&((unsigned char)Comandă[element_COUNT]&192)==128)element_COUNT--;Comandă[element_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&element_COUNT<120){Comandă[element_COUNT++]=셋째순번;Comandă[element_COUNT]=0;}
    }
    if(zonă_VALUE=='/'){for(int 순번=0;순번<=element_COUNT;순번++)FIND_intrare[순번]=Comandă[순번];FIND_Următorul();return 0;}
    if(같은지(Comandă,"q!"))return 1;
    if(같은지(Comandă,"q")){if(!변경됨)return 1;înștiințare_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(Comandă,"wq")||같은지(Comandă,"x"))return Store_VALUE();
    if(같은지(Comandă,"w")){Store_VALUE();return 0;}
    if(Comandă[0]=='w'&&Comandă[1]==' '){int 순번=2;while(Comandă[순번]==' ')순번++;int Mărime=element_COUNT-순번;if(Mărime<1||Mărime>63){înștiințare_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Mărime;안쪽순번++)Fișier_intrare_nume[안쪽순번]=Comandă[순번+안쪽순번];Fișier_intrare_nume[Mărime]=0;Store_VALUE();return 0;}
    int Linie=0;for(int 순번=0;순번<element_COUNT;순번++){if(Comandă[순번]<'0'||Comandă[순번]>'9'){Linie=0;break;}Linie=Linie*10+Comandă[순번]-'0';if(Linie>16384){Linie=0;break;}}
    if(Linie){INDEX_VALUE=0;while(--Linie&&INDEX_VALUE<lungime_VALUE){INDEX_VALUE=termina_un_apel_OFFSET(INDEX_VALUE);if(INDEX_VALUE<lungime_VALUE)INDEX_VALUE++;}return 0;}
    înștiințare_SMS="Unknown vi command";return 0;
}
int buta_utilizator_program(int 무시값){
    (void)무시값;if(utilizator_argument_COUNT()!=1||utilizator_argument(0,Fișier_intrare_nume,sizeof(Fișier_intrare_nume))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Fișier_handle=crea_Fișier(Fișier_intrare_nume,doar_în_citire_VALUE,0);
    if(Fișier_handle>=0){int element_COUNT=dimensiune_fișier(Fișier_handle);if(element_COUNT<0||element_COUNT>Editor_capacitate){închide_Fișier(Fișier_handle);return 1;}lungime_VALUE=파일자료읽기(Fișier_handle,SMS,element_COUNT);închide_Fișier(Fișier_handle);if(lungime_VALUE!=element_COUNT)return 1;for(int 순번=0;순번<lungime_VALUE;순번++)if(!SMS[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(număr_de_eroare!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,ieșire_program=0;
    while(!ieșire_program){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();înștiințare_SMS=0;
        if(셋째순번==1001){Verticală(-1);continue;}if(셋째순번==1002){Verticală(1);continue;}if(셋째순번==1003){INDEX_VALUE=Următorul_element(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=Anteriorul(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Pornește(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=termina_un_apel_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Verticală(셋째순번==1008?-1:1);continue;}
        if(Inserare){
            if(셋째순번==27||셋째순번==3){Inserare=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(Anteriorul(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<lungime_VALUE)바이트지우기(INDEX_VALUE,Următorul_element(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int element_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!element_COUNT){înștiințare_SMS="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<element_COUNT;순번++){int cod_caracter=누름값();if(cod_caracter<128||cod_caracter>191){în_așteptare_Cheie=cod_caracter;유효함=0;break;}SECOND_VALUE[순번]=cod_caracter;}
                if(유효함)adăuga_VALUE(SECOND_VALUE,element_COUNT);
            }continue;
        }
        if(앞부분){int date_poziție=앞부분;앞부분=0;if(date_poziție=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(date_poziție=='Z'&&셋째순번=='Z'){ieșire_program=Store_VALUE();continue;}if((date_poziție=='d'&&셋째순번=='d')||(date_poziție=='y'&&셋째순번=='y')){int 첫째값=Pornește(INDEX_VALUE),SECOND_VALUE=termina_un_apel_OFFSET(INDEX_VALUE);if(SECOND_VALUE<lungime_VALUE)SECOND_VALUE++;copia_lungime=SECOND_VALUE-첫째값;for(int 순번=0;순번<copia_lungime;순번++)복사자료[순번]=SMS[첫째값+순번];if(date_poziție=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Inserare=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<termina_un_apel_OFFSET(INDEX_VALUE))INDEX_VALUE=Următorul_element(INDEX_VALUE);Inserare=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Pornește(INDEX_VALUE);Inserare=1;continue;}if(셋째순번=='A'){INDEX_VALUE=termina_un_apel_OFFSET(INDEX_VALUE);Inserare=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char linie_termina_un_apel='\n';INDEX_VALUE=셋째순번=='o'?termina_un_apel_OFFSET(INDEX_VALUE):Pornește(INDEX_VALUE);if(adăuga_VALUE(&linie_termina_un_apel,1)){if(셋째순번=='O')INDEX_VALUE--;Inserare=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=Anteriorul(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Următorul_element(INDEX_VALUE);continue;}if(셋째순번=='j'){Verticală(1);continue;}if(셋째순번=='k'){Verticală(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Pornește(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=termina_un_apel_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Pornește(lungime_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<lungime_VALUE)바이트지우기(INDEX_VALUE,Următorul_element(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&copia_lungime){INDEX_VALUE=termina_un_apel_OFFSET(INDEX_VALUE);if(INDEX_VALUE<lungime_VALUE)INDEX_VALUE++;adăuga_VALUE(복사자료,copia_lungime);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_capacitate;순번++){unsigned char SECOND_VALUE=SMS[순번];SMS[순번]=anulare_date[순번];anulare_date[순번]=SECOND_VALUE;}int element_COUNT=lungime_VALUE;lungime_VALUE=anulare_lungime;anulare_lungime=element_COUNT;element_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=element_COUNT;element_COUNT=변경됨;변경됨=anulare_Modificări;anulare_Modificări=element_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){ieșire_program=solicita(셋째순번);continue;}if(셋째순번=='n'){FIND_Următorul();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
