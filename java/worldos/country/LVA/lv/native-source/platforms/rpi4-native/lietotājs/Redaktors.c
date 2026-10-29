/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Redaktors_noslodze 16384
static unsigned char Teksts[Redaktors_noslodze],atsaukt_dati[Redaktors_noslodze],복사자료[Redaktors_noslodze],mērs_dati[1024];
static int 길이,INDEX_VALUE,맨위,왼쪽,변경됨,ievietot,되돌림길이,위쪽,atsaukt_Izmaiņas,되돌림있음,복사길이,사용량,COLUMNS=68,ROW_COUNT=19;
static char Fails_ievade_nosaukums[64],Komanda[128],FIND_ievade[128];
static const char *informēšana_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned gaida_Atslēga;
static int palīdzība_joma,Statuss_IMAGE,Statuss_rinda;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)mērs_dati,사용량,0,0,0);사용량=0;}}
static void byte_dati(unsigned koda_punkts){if(Statuss_IMAGE){if((koda_punkts&192)!=128){Statuss_rinda+=koda_punkts>=196?2:1;}if(Statuss_rinda>=COLUMNS)return;}if(사용량==(int)sizeof(mērs_dati))출력비우기();mērs_dati[사용량++]=koda_punkts;}
static void 글내보내기(const char *virkne_dati){while(*virkne_dati)byte_dati((unsigned char)*virkne_dati++);}
static void 수치(unsigned krājums_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+krājums_COUNT%10;krājums_COUNT/=10;}while(krājums_COUNT);while(순번)byte_dati(SECOND_VALUE[--순번]);}
static void pārvietot_VALUE(int ROW_amats,int COLUMN_amats){글내보내기("\033[");수치(ROW_amats);byte_dati(';');수치(COLUMN_amats);byte_dati('H');}
static int 이전항목(int dati_amats){if(dati_amats){dati_amats--;while(dati_amats>0&&(Teksts[dati_amats]&192)==128)dati_amats--;}return dati_amats;}
static int Tālāk_krājums(int dati_amats){if(dati_amats<길이){dati_amats++;while(dati_amats<길이&&(Teksts[dati_amats]&192)==128)dati_amats++;}return dati_amats;}
static int Palaist(int dati_amats){while(dati_amats>0&&Teksts[dati_amats-1]!='\n')dati_amats--;return dati_amats;}
static int beigt_zvanu_Nobīde(int dati_amats){while(dati_amats<길이&&Teksts[dati_amats]!='\n')dati_amats++;return dati_amats;}
static int 너비(unsigned koda_punkts){return koda_punkts>=196?2:1;}
static int COLUMN(int dati_amats){int koda_punkts=0;for(int 순번=Palaist(dati_amats);순번<dati_amats;순번=Tālāk_krājums(순번))koda_punkts+=Teksts[순번]=='\t'?4-koda_punkts%4:너비(Teksts[순번]);return koda_punkts;}
static void kontrolpunkts(void){for(int 순번=0;순번<길이;순번++)atsaukt_dati[순번]=Teksts[순번];되돌림길이=길이;위쪽=INDEX_VALUE;atsaukt_Izmaiņas=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrolpunkts();for(int 순번=도착위치;순번<길이;순번++)Teksts[출발위치+순번-도착위치]=Teksts[순번];길이-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int Pievienot_VALUE(const unsigned char *virkne_dati,int krājums_COUNT){if(krājums_COUNT>Redaktors_noslodze-길이){informēšana_SMS="File full (16384 bytes)";return 0;}kontrolpunkts();for(int 순번=길이-1;순번>=INDEX_VALUE;순번--)Teksts[순번+krājums_COUNT]=Teksts[순번];for(int 순번=0;순번<krājums_COUNT;순번++)Teksts[INDEX_VALUE+순번]=virkne_dati[순번];길이+=krājums_COUNT;INDEX_VALUE+=krājums_COUNT;변경됨=1;return 1;}
static void vertikāle(int 차이){int COLUMN_amats=COLUMN(INDEX_VALUE),dati_amats=Palaist(INDEX_VALUE);if(차이<0){if(!dati_amats)return;dati_amats=Palaist(dati_amats-1);}else{dati_amats=beigt_zvanu_Nobīde(dati_amats);if(dati_amats==길이)return;dati_amats++;}int koda_punkts=0;while(dati_amats<길이&&Teksts[dati_amats]!='\n'&&koda_punkts<COLUMN_amats){koda_punkts+=Teksts[dati_amats]=='\t'?4-koda_punkts%4:너비(Teksts[dati_amats]);dati_amats=Tālāk_krājums(dati_amats);}INDEX_VALUE=dati_amats;}
static void 화면그리기(void){
    if(INDEX_VALUE>길이)INDEX_VALUE=길이;if(맨위>INDEX_VALUE)맨위=Palaist(INDEX_VALUE);맨위=Palaist(맨위);
    int ROW_amats=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Teksts[순번]=='\n')ROW_amats++;
    while(ROW_amats>=ROW_COUNT-1){맨위=beigt_zvanu_Nobīde(맨위);if(맨위<길이)맨위++;ROW_amats--;}
    int COLUMN_amats=COLUMN(INDEX_VALUE);if(COLUMN_amats<왼쪽)왼쪽=COLUMN_amats;if(COLUMN_amats-왼쪽>=COLUMNS-1)왼쪽=COLUMN_amats-COLUMNS+2;
    글내보내기("\033[?25l");int dati_amats=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        pārvietot_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int koda_punkts=0,그려진상태=0;
        if(dati_amats>=길이&&반환값>ROW_amats){글내보내기("\033[90m~\033[0m");continue;}
        while(dati_amats<길이&&Teksts[dati_amats]!='\n'){
            int Tālāk_Nobīde=Tālāk_krājums(dati_amats),너비값=Teksts[dati_amats]=='\t'?4-koda_punkts%4:너비(Teksts[dati_amats]);
            if(koda_punkts>=왼쪽&&koda_punkts-왼쪽+너비값<COLUMNS){
                if(Teksts[dati_amats]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_dati(' ');}else if(Teksts[dati_amats]<32||Teksts[dati_amats]==127){byte_dati('?');}else for(int 안쪽순번=dati_amats;안쪽순번<Tālāk_Nobīde;안쪽순번++)byte_dati(Teksts[안쪽순번]);그려진상태+=너비값;
            }koda_punkts+=너비값;dati_amats=Tālāk_Nobīde;
        }
        (void)그려진상태;if(dati_amats<길이)dati_amats++;
    }
    pārvietot_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");Statuss_IMAGE=1;Statuss_rinda=0;글내보내기(ievietot?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Fails_ievade_nosaukums[이름바이트수]&&이름바이트수<30)byte_dati(Fails_ievade_nosaukums[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Līniju=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Teksts[순번]=='\n')Līniju++;수치(Līniju);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(informēšana_SMS){int krājums_COUNT=0;글내보내기(" | ");while(informēšana_SMS[krājums_COUNT]&&krājums_COUNT<20)byte_dati(informēšana_SMS[krājums_COUNT++]);}
    Statuss_IMAGE=0;글내보내기("\033[0m");pārvietot_VALUE(ROW_amats+1,COLUMN_amats-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(gaida_Atslēga){int 셋째순번=gaida_Atslēga;gaida_Atslēga=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Izmērs=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Izmērs&65535)||ROW_COUNT!=(int)(Izmērs>>16)){
            COLUMNS=Izmērs&65535;ROW_COUNT=Izmērs>>16;화면그리기();
            if(palīdzība_joma){pārvietot_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_dati(palīdzība_joma);글내보내기(Komanda);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned pašreizējais_amats=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-pašreizējais_amats<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){gaida_Atslēga=셋째순번;return 27;}
    int krājums_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){krājums_COUNT=krājums_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return krājums_COUNT==3?1007:krājums_COUNT==5?1008:krājums_COUNT==6?1009:krājums_COUNT==1?1005:krājums_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int Fails_turis=atvērt_Fails(Fails_ievade_nosaukums,읽고쓰기|없으면만들기|apraut_Satura_rādītājs,0600);if(Fails_turis<0){informēšana_SMS="Cannot open for save";return 0;}
    intptr_t krājums_COUNT=rakstīšana_Fails_dati(Fails_turis,Teksts,길이);Aizvērt_Fails(Fails_turis);if(krājums_COUNT!=길이){informēšana_SMS="Write failed";return 0;}변경됨=0;informēšana_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Tālāk(void){int krājums_COUNT=0;while(FIND_ievade[krājums_COUNT])krājums_COUNT++;if(!krājums_COUNT){informēšana_SMS="No search pattern";return;}for(int 순번=1;순번<=길이;순번++){int dati_amats=(INDEX_VALUE+순번)%(길이?길이:1),안쪽순번=0;while(안쪽순번<krājums_COUNT&&dati_amats+안쪽순번<길이&&Teksts[dati_amats+안쪽순번]==(unsigned char)FIND_ievade[안쪽순번])안쪽순번++;if(안쪽순번==krājums_COUNT){INDEX_VALUE=dati_amats;informēšana_SMS="Match";return;}}informēšana_SMS="Pattern not found";}
static int uzvedne(int joma_VALUE){
    int krājums_COUNT=0;Komanda[0]=0;
    for(;;){pārvietot_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_dati(joma_VALUE);글내보내기(Komanda);출력비우기();palīdzība_joma=joma_VALUE;int 셋째순번=누름값();palīdzība_joma=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(krājums_COUNT){krājums_COUNT--;while(krājums_COUNT>0&&((unsigned char)Komanda[krājums_COUNT]&192)==128)krājums_COUNT--;Komanda[krājums_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&krājums_COUNT<120){Komanda[krājums_COUNT++]=셋째순번;Komanda[krājums_COUNT]=0;}
    }
    if(joma_VALUE=='/'){for(int 순번=0;순번<=krājums_COUNT;순번++)FIND_ievade[순번]=Komanda[순번];FIND_Tālāk();return 0;}
    if(같은지(Komanda,"q!"))return 1;
    if(같은지(Komanda,"q")){if(!변경됨)return 1;informēšana_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(Komanda,"wq")||같은지(Komanda,"x"))return Store_VALUE();
    if(같은지(Komanda,"w")){Store_VALUE();return 0;}
    if(Komanda[0]=='w'&&Komanda[1]==' '){int 순번=2;while(Komanda[순번]==' ')순번++;int Izmērs=krājums_COUNT-순번;if(Izmērs<1||Izmērs>63){informēšana_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Izmērs;안쪽순번++)Fails_ievade_nosaukums[안쪽순번]=Komanda[순번+안쪽순번];Fails_ievade_nosaukums[Izmērs]=0;Store_VALUE();return 0;}
    int Līniju=0;for(int 순번=0;순번<krājums_COUNT;순번++){if(Komanda[순번]<'0'||Komanda[순번]>'9'){Līniju=0;break;}Līniju=Līniju*10+Komanda[순번]-'0';if(Līniju>16384){Līniju=0;break;}}
    if(Līniju){INDEX_VALUE=0;while(--Līniju&&INDEX_VALUE<길이){INDEX_VALUE=beigt_zvanu_Nobīde(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;}return 0;}
    informēšana_SMS="Unknown vi command";return 0;
}
int Sākt_lietotājs_programma(int 무시값){
    (void)무시값;if(lietotājs_arg_COUNT()!=1||lietotājs_arg(0,Fails_ievade_nosaukums,sizeof(Fails_ievade_nosaukums))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Fails_turis=atvērt_Fails(Fails_ievade_nosaukums,tikai_lasāms_VALUE,0);
    if(Fails_turis>=0){int krājums_COUNT=faila_lielums(Fails_turis);if(krājums_COUNT<0||krājums_COUNT>Redaktors_noslodze){Aizvērt_Fails(Fails_turis);return 1;}길이=파일자료읽기(Fails_turis,Teksts,krājums_COUNT);Aizvērt_Fails(Fails_turis);if(길이!=krājums_COUNT)return 1;for(int 순번=0;순번<길이;순번++)if(!Teksts[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(kļūdas_numurs!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,iziet_programma=0;
    while(!iziet_programma){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();informēšana_SMS=0;
        if(셋째순번==1001){vertikāle(-1);continue;}if(셋째순번==1002){vertikāle(1);continue;}if(셋째순번==1003){INDEX_VALUE=Tālāk_krājums(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Palaist(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=beigt_zvanu_Nobīde(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)vertikāle(셋째순번==1008?-1:1);continue;}
        if(ievietot){
            if(셋째순번==27||셋째순번==3){ievietot=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,Tālāk_krājums(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int krājums_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!krājums_COUNT){informēšana_SMS="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<krājums_COUNT;순번++){int koda_punkts=누름값();if(koda_punkts<128||koda_punkts>191){gaida_Atslēga=koda_punkts;유효함=0;break;}SECOND_VALUE[순번]=koda_punkts;}
                if(유효함)Pievienot_VALUE(SECOND_VALUE,krājums_COUNT);
            }continue;
        }
        if(앞부분){int dati_amats=앞부분;앞부분=0;if(dati_amats=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(dati_amats=='Z'&&셋째순번=='Z'){iziet_programma=Store_VALUE();continue;}if((dati_amats=='d'&&셋째순번=='d')||(dati_amats=='y'&&셋째순번=='y')){int 첫째값=Palaist(INDEX_VALUE),SECOND_VALUE=beigt_zvanu_Nobīde(INDEX_VALUE);if(SECOND_VALUE<길이)SECOND_VALUE++;복사길이=SECOND_VALUE-첫째값;for(int 순번=0;순번<복사길이;순번++)복사자료[순번]=Teksts[첫째값+순번];if(dati_amats=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){ievietot=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<beigt_zvanu_Nobīde(INDEX_VALUE))INDEX_VALUE=Tālāk_krājums(INDEX_VALUE);ievietot=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Palaist(INDEX_VALUE);ievietot=1;continue;}if(셋째순번=='A'){INDEX_VALUE=beigt_zvanu_Nobīde(INDEX_VALUE);ievietot=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char līnija_beigt_zvanu='\n';INDEX_VALUE=셋째순번=='o'?beigt_zvanu_Nobīde(INDEX_VALUE):Palaist(INDEX_VALUE);if(Pievienot_VALUE(&līnija_beigt_zvanu,1)){if(셋째순번=='O')INDEX_VALUE--;ievietot=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Tālāk_krājums(INDEX_VALUE);continue;}if(셋째순번=='j'){vertikāle(1);continue;}if(셋째순번=='k'){vertikāle(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Palaist(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=beigt_zvanu_Nobīde(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Palaist(길이);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,Tālāk_krājums(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&복사길이){INDEX_VALUE=beigt_zvanu_Nobīde(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;Pievienot_VALUE(복사자료,복사길이);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Redaktors_noslodze;순번++){unsigned char SECOND_VALUE=Teksts[순번];Teksts[순번]=atsaukt_dati[순번];atsaukt_dati[순번]=SECOND_VALUE;}int krājums_COUNT=길이;길이=되돌림길이;되돌림길이=krājums_COUNT;krājums_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=krājums_COUNT;krājums_COUNT=변경됨;변경됨=atsaukt_Izmaiņas;atsaukt_Izmaiņas=krājums_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){iziet_programma=uzvedne(셋째순번);continue;}if(셋째순번=='n'){FIND_Tālāk();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
