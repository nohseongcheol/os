/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Tekst[편집용량],angre_data[편집용량],복사자료[편집용량],forretningsmål_data[1024];
static int lengd_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,Set_inn,angre_lengd,위쪽,angre_Endringar,되돌림있음,kopiere_lengd,사용량,COLUMNS=68,ROW_COUNT=19;
static char fil_oppføring_namn[64],Kommando[128],Søk_oppføring[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned ventande_tast;
static int hjelp_kategori,status_IMAGE,status_kø;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)forretningsmål_data,사용량,0,0,0);사용량=0;}}
static void byte_data(unsigned teiknkode){if(status_IMAGE){if((teiknkode&192)!=128){status_kø+=teiknkode>=196?2:1;}if(status_kø>=COLUMNS)return;}if(사용량==(int)sizeof(forretningsmål_data))출력비우기();forretningsmål_data[사용량++]=teiknkode;}
static void 글내보내기(const char *streng_data){while(*streng_data)byte_data((unsigned char)*streng_data++);}
static void 수치(unsigned vare_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+vare_COUNT%10;vare_COUNT/=10;}while(vare_COUNT);while(순번)byte_data(SECOND_VALUE[--순번]);}
static void flytte_VALUE(int ROW_plassere,int COLUMN_plassere){글내보내기("\033[");수치(ROW_plassere);byte_data(';');수치(COLUMN_plassere);byte_data('H');}
static int 이전항목(int data_plassere){if(data_plassere){data_plassere--;while(data_plassere>0&&(Tekst[data_plassere]&192)==128)data_plassere--;}return data_plassere;}
static int Neste_vare(int data_plassere){if(data_plassere<lengd_VALUE){data_plassere++;while(data_plassere<lengd_VALUE&&(Tekst[data_plassere]&192)==128)data_plassere++;}return data_plassere;}
static int Køyr_2(int data_plassere){while(data_plassere>0&&Tekst[data_plassere-1]!='\n')data_plassere--;return data_plassere;}
static int avslutte_OFFSET(int data_plassere){while(data_plassere<lengd_VALUE&&Tekst[data_plassere]!='\n')data_plassere++;return data_plassere;}
static int 너비(unsigned teiknkode){return teiknkode>=196?2:1;}
static int COLUMN(int data_plassere){int teiknkode=0;for(int 순번=Køyr_2(data_plassere);순번<data_plassere;순번=Neste_vare(순번))teiknkode+=Tekst[순번]=='\t'?4-teiknkode%4:너비(Tekst[순번]);return teiknkode;}
static void kontrollpunkt(void){for(int 순번=0;순번<lengd_VALUE;순번++)angre_data[순번]=Tekst[순번];angre_lengd=lengd_VALUE;위쪽=INDEX_VALUE;angre_Endringar=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrollpunkt();for(int 순번=도착위치;순번<lengd_VALUE;순번++)Tekst[출발위치+순번-도착위치]=Tekst[순번];lengd_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *streng_data,int vare_COUNT){if(vare_COUNT>편집용량-lengd_VALUE){알림문="File full (16384 bytes)";return 0;}kontrollpunkt();for(int 순번=lengd_VALUE-1;순번>=INDEX_VALUE;순번--)Tekst[순번+vare_COUNT]=Tekst[순번];for(int 순번=0;순번<vare_COUNT;순번++)Tekst[INDEX_VALUE+순번]=streng_data[순번];lengd_VALUE+=vare_COUNT;INDEX_VALUE+=vare_COUNT;변경됨=1;return 1;}
static void vertikalvising(int 차이){int COLUMN_plassere=COLUMN(INDEX_VALUE),data_plassere=Køyr_2(INDEX_VALUE);if(차이<0){if(!data_plassere)return;data_plassere=Køyr_2(data_plassere-1);}else{data_plassere=avslutte_OFFSET(data_plassere);if(data_plassere==lengd_VALUE)return;data_plassere++;}int teiknkode=0;while(data_plassere<lengd_VALUE&&Tekst[data_plassere]!='\n'&&teiknkode<COLUMN_plassere){teiknkode+=Tekst[data_plassere]=='\t'?4-teiknkode%4:너비(Tekst[data_plassere]);data_plassere=Neste_vare(data_plassere);}INDEX_VALUE=data_plassere;}
static void 화면그리기(void){
    if(INDEX_VALUE>lengd_VALUE)INDEX_VALUE=lengd_VALUE;if(맨위>INDEX_VALUE)맨위=Køyr_2(INDEX_VALUE);맨위=Køyr_2(맨위);
    int ROW_plassere=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Tekst[순번]=='\n')ROW_plassere++;
    while(ROW_plassere>=ROW_COUNT-1){맨위=avslutte_OFFSET(맨위);if(맨위<lengd_VALUE)맨위++;ROW_plassere--;}
    int COLUMN_plassere=COLUMN(INDEX_VALUE);if(COLUMN_plassere<왼쪽)왼쪽=COLUMN_plassere;if(COLUMN_plassere-왼쪽>=COLUMNS-1)왼쪽=COLUMN_plassere-COLUMNS+2;
    글내보내기("\033[?25l");int data_plassere=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        flytte_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int teiknkode=0,그려진상태=0;
        if(data_plassere>=lengd_VALUE&&반환값>ROW_plassere){글내보내기("\033[90m~\033[0m");continue;}
        while(data_plassere<lengd_VALUE&&Tekst[data_plassere]!='\n'){
            int Neste_OFFSET=Neste_vare(data_plassere),너비값=Tekst[data_plassere]=='\t'?4-teiknkode%4:너비(Tekst[data_plassere]);
            if(teiknkode>=왼쪽&&teiknkode-왼쪽+너비값<COLUMNS){
                if(Tekst[data_plassere]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_data(' ');}else if(Tekst[data_plassere]<32||Tekst[data_plassere]==127){byte_data('?');}else for(int 안쪽순번=data_plassere;안쪽순번<Neste_OFFSET;안쪽순번++)byte_data(Tekst[안쪽순번]);그려진상태+=너비값;
            }teiknkode+=너비값;data_plassere=Neste_OFFSET;
        }
        (void)그려진상태;if(data_plassere<lengd_VALUE)data_plassere++;
    }
    flytte_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");status_IMAGE=1;status_kø=0;글내보내기(Set_inn?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fil_oppføring_namn[이름바이트수]&&이름바이트수<30)byte_data(fil_oppføring_namn[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int linje=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Tekst[순번]=='\n')linje++;수치(linje);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int vare_COUNT=0;글내보내기(" | ");while(알림문[vare_COUNT]&&vare_COUNT<20)byte_data(알림문[vare_COUNT++]);}
    status_IMAGE=0;글내보내기("\033[0m");flytte_VALUE(ROW_plassere+1,COLUMN_plassere-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(ventande_tast){int 셋째순번=ventande_tast;ventande_tast=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Storleik=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Storleik&65535)||ROW_COUNT!=(int)(Storleik>>16)){
            COLUMNS=Storleik&65535;ROW_COUNT=Storleik>>16;화면그리기();
            if(hjelp_kategori){flytte_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_data(hjelp_kategori);글내보내기(Kommando);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned betalt_plassere=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-betalt_plassere<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){ventande_tast=셋째순번;return 27;}
    int vare_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){vare_COUNT=vare_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return vare_COUNT==3?1007:vare_COUNT==5?1008:vare_COUNT==6?1009:vare_COUNT==1?1005:vare_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int fil_handtak=opne_fil(fil_oppføring_namn,lese_og_skrivetilgang|없으면만들기|내용비우기,0600);if(fil_handtak<0){알림문="Cannot open for save";return 0;}
    intptr_t vare_COUNT=skrive_fil_data(fil_handtak,Tekst,lengd_VALUE);Lukk_fil(fil_handtak);if(vare_COUNT!=lengd_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void Søk_Neste(void){int vare_COUNT=0;while(Søk_oppføring[vare_COUNT])vare_COUNT++;if(!vare_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=lengd_VALUE;순번++){int data_plassere=(INDEX_VALUE+순번)%(lengd_VALUE?lengd_VALUE:1),안쪽순번=0;while(안쪽순번<vare_COUNT&&data_plassere+안쪽순번<lengd_VALUE&&Tekst[data_plassere+안쪽순번]==(unsigned char)Søk_oppføring[안쪽순번])안쪽순번++;if(안쪽순번==vare_COUNT){INDEX_VALUE=data_plassere;알림문="Match";return;}}알림문="Pattern not found";}
static int spørsmål(int kategori_VALUE){
    int vare_COUNT=0;Kommando[0]=0;
    for(;;){flytte_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_data(kategori_VALUE);글내보내기(Kommando);출력비우기();hjelp_kategori=kategori_VALUE;int 셋째순번=누름값();hjelp_kategori=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(vare_COUNT){vare_COUNT--;while(vare_COUNT>0&&((unsigned char)Kommando[vare_COUNT]&192)==128)vare_COUNT--;Kommando[vare_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&vare_COUNT<120){Kommando[vare_COUNT++]=셋째순번;Kommando[vare_COUNT]=0;}
    }
    if(kategori_VALUE=='/'){for(int 순번=0;순번<=vare_COUNT;순번++)Søk_oppføring[순번]=Kommando[순번];Søk_Neste();return 0;}
    if(같은지(Kommando,"q!"))return 1;
    if(같은지(Kommando,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Kommando,"wq")||같은지(Kommando,"x"))return Store_VALUE();
    if(같은지(Kommando,"w")){Store_VALUE();return 0;}
    if(Kommando[0]=='w'&&Kommando[1]==' '){int 순번=2;while(Kommando[순번]==' ')순번++;int Storleik=vare_COUNT-순번;if(Storleik<1||Storleik>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Storleik;안쪽순번++)fil_oppføring_namn[안쪽순번]=Kommando[순번+안쪽순번];fil_oppføring_namn[Storleik]=0;Store_VALUE();return 0;}
    int linje=0;for(int 순번=0;순번<vare_COUNT;순번++){if(Kommando[순번]<'0'||Kommando[순번]>'9'){linje=0;break;}linje=linje*10+Kommando[순번]-'0';if(linje>16384){linje=0;break;}}
    if(linje){INDEX_VALUE=0;while(--linje&&INDEX_VALUE<lengd_VALUE){INDEX_VALUE=avslutte_OFFSET(INDEX_VALUE);if(INDEX_VALUE<lengd_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int START_brukar_app(int 무시값){
    (void)무시값;if(brukar_argument_COUNT()!=1||brukar_argument(0,fil_oppføring_namn,sizeof(fil_oppføring_namn))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fil_handtak=opne_fil(fil_oppføring_namn,skriveverna_VALUE,0);
    if(fil_handtak>=0){int vare_COUNT=fil_endre_storleik(fil_handtak);if(vare_COUNT<0||vare_COUNT>편집용량){Lukk_fil(fil_handtak);return 1;}lengd_VALUE=파일자료읽기(fil_handtak,Tekst,vare_COUNT);Lukk_fil(fil_handtak);if(lengd_VALUE!=vare_COUNT)return 1;for(int 순번=0;순번<lengd_VALUE;순번++)if(!Tekst[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(feilnummer!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,avslutt_app=0;
    while(!avslutt_app){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){vertikalvising(-1);continue;}if(셋째순번==1002){vertikalvising(1);continue;}if(셋째순번==1003){INDEX_VALUE=Neste_vare(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Køyr_2(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=avslutte_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)vertikalvising(셋째순번==1008?-1:1);continue;}
        if(Set_inn){
            if(셋째순번==27||셋째순번==3){Set_inn=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<lengd_VALUE)바이트지우기(INDEX_VALUE,Neste_vare(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int vare_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!vare_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<vare_COUNT;순번++){int teiknkode=누름값();if(teiknkode<128||teiknkode>191){ventande_tast=teiknkode;유효함=0;break;}SECOND_VALUE[순번]=teiknkode;}
                if(유효함)덧붙이기(SECOND_VALUE,vare_COUNT);
            }continue;
        }
        if(앞부분){int data_plassere=앞부분;앞부분=0;if(data_plassere=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(data_plassere=='Z'&&셋째순번=='Z'){avslutt_app=Store_VALUE();continue;}if((data_plassere=='d'&&셋째순번=='d')||(data_plassere=='y'&&셋째순번=='y')){int 첫째값=Køyr_2(INDEX_VALUE),SECOND_VALUE=avslutte_OFFSET(INDEX_VALUE);if(SECOND_VALUE<lengd_VALUE)SECOND_VALUE++;kopiere_lengd=SECOND_VALUE-첫째값;for(int 순번=0;순번<kopiere_lengd;순번++)복사자료[순번]=Tekst[첫째값+순번];if(data_plassere=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Set_inn=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<avslutte_OFFSET(INDEX_VALUE))INDEX_VALUE=Neste_vare(INDEX_VALUE);Set_inn=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Køyr_2(INDEX_VALUE);Set_inn=1;continue;}if(셋째순번=='A'){INDEX_VALUE=avslutte_OFFSET(INDEX_VALUE);Set_inn=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char line_avslutte='\n';INDEX_VALUE=셋째순번=='o'?avslutte_OFFSET(INDEX_VALUE):Køyr_2(INDEX_VALUE);if(덧붙이기(&line_avslutte,1)){if(셋째순번=='O')INDEX_VALUE--;Set_inn=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Neste_vare(INDEX_VALUE);continue;}if(셋째순번=='j'){vertikalvising(1);continue;}if(셋째순번=='k'){vertikalvising(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Køyr_2(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=avslutte_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Køyr_2(lengd_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<lengd_VALUE)바이트지우기(INDEX_VALUE,Neste_vare(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&kopiere_lengd){INDEX_VALUE=avslutte_OFFSET(INDEX_VALUE);if(INDEX_VALUE<lengd_VALUE)INDEX_VALUE++;덧붙이기(복사자료,kopiere_lengd);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=Tekst[순번];Tekst[순번]=angre_data[순번];angre_data[순번]=SECOND_VALUE;}int vare_COUNT=lengd_VALUE;lengd_VALUE=angre_lengd;angre_lengd=vare_COUNT;vare_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=vare_COUNT;vare_COUNT=변경됨;변경됨=angre_Endringar;angre_Endringar=vare_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){avslutt_app=spørsmål(셋째순번);continue;}if(셋째순번=='n'){Søk_Neste();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
