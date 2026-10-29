/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Mäten[편집용량],баш_тарту_мәгълүмат[편집용량],복사자료[편집용량],үлчәм_мәгълүмат[1024];
static int озынлык_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,өстәү,баш_тарту_озынлык,위쪽,баш_тарту_Үзгәрешләр,되돌림있음,экземпляр_озынлык,사용량,COLUMNS=68,юл_COUNT=19;
static char файл_кертү_исем[64],команда[128],FIND_кертү[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned көтүчән_ачкыч;
static int ярдәм_категория,халәт_IMAGE,халәт_чират;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)үлчәм_мәгълүмат,사용량,0,0,0);사용량=0;}}
static void байт_мәгълүмат(unsigned символ_коды){if(халәт_IMAGE){if((символ_коды&192)!=128){халәт_чират+=символ_коды>=196?2:1;}if(халәт_чират>=COLUMNS)return;}if(사용량==(int)sizeof(үлчәм_мәгълүмат))출력비우기();үлчәм_мәгълүмат[사용량++]=символ_коды;}
static void 글내보내기(const char *юл_мәгълүмат){while(*юл_мәгълүмат)байт_мәгълүмат((unsigned char)*юл_мәгълүмат++);}
static void 수치(unsigned элемент_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+элемент_COUNT%10;элемент_COUNT/=10;}while(элемент_COUNT);while(순번)байт_мәгълүмат(SECOND_VALUE[--순번]);}
static void күчерү_VALUE(int юл_урнаштыру,int COLUMN_урнаштыру){글내보내기("\033[");수치(юл_урнаштыру);байт_мәгълүмат(';');수치(COLUMN_урнаштыру);байт_мәгълүмат('H');}
static int 이전항목(int мәгълүмат_урнаштыру){if(мәгълүмат_урнаштыру){мәгълүмат_урнаштыру--;while(мәгълүмат_урнаштыру>0&&(Mäten[мәгълүмат_урнаштыру]&192)==128)мәгълүмат_урнаштыру--;}return мәгълүмат_урнаштыру;}
static int Киләсе_элемент(int мәгълүмат_урнаштыру){if(мәгълүмат_урнаштыру<озынлык_VALUE){мәгълүмат_урнаштыру++;while(мәгълүмат_урнаштыру<озынлык_VALUE&&(Mäten[мәгълүмат_урнаштыру]&192)==128)мәгълүмат_урнаштыру++;}return мәгълүмат_урнаштыру;}
static int эшләтү(int мәгълүмат_урнаштыру){while(мәгълүмат_урнаштыру>0&&Mäten[мәгълүмат_урнаштыру-1]!='\n')мәгълүмат_урнаштыру--;return мәгълүмат_урнаштыру;}
static int тәмамлау_OFFSET(int мәгълүмат_урнаштыру){while(мәгълүмат_урнаштыру<озынлык_VALUE&&Mäten[мәгълүмат_урнаштыру]!='\n')мәгълүмат_урнаштыру++;return мәгълүмат_урнаштыру;}
static int 너비(unsigned символ_коды){return символ_коды>=196?2:1;}
static int COLUMN(int мәгълүмат_урнаштыру){int символ_коды=0;for(int 순번=эшләтү(мәгълүмат_урнаштыру);순번<мәгълүмат_урнаштыру;순번=Киләсе_элемент(순번))символ_коды+=Mäten[순번]=='\t'?4-символ_коды%4:너비(Mäten[순번]);return символ_коды;}
static void контроль_нокта(void){for(int 순번=0;순번<озынлык_VALUE;순번++)баш_тарту_мәгълүмат[순번]=Mäten[순번];баш_тарту_озынлык=озынлык_VALUE;위쪽=INDEX_VALUE;баш_тарту_Үзгәрешләр=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){контроль_нокта();for(int 순번=도착위치;순번<озынлык_VALUE;순번++)Mäten[출발위치+순번-도착위치]=Mäten[순번];озынлык_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *юл_мәгълүмат,int элемент_COUNT){if(элемент_COUNT>편집용량-озынлык_VALUE){알림문="File full (16384 bytes)";return 0;}контроль_нокта();for(int 순번=озынлык_VALUE-1;순번>=INDEX_VALUE;순번--)Mäten[순번+элемент_COUNT]=Mäten[순번];for(int 순번=0;순번<элемент_COUNT;순번++)Mäten[INDEX_VALUE+순번]=юл_мәгълүмат[순번];озынлык_VALUE+=элемент_COUNT;INDEX_VALUE+=элемент_COUNT;변경됨=1;return 1;}
static void Вертикаль(int 차이){int COLUMN_урнаштыру=COLUMN(INDEX_VALUE),мәгълүмат_урнаштыру=эшләтү(INDEX_VALUE);if(차이<0){if(!мәгълүмат_урнаштыру)return;мәгълүмат_урнаштыру=эшләтү(мәгълүмат_урнаштыру-1);}else{мәгълүмат_урнаштыру=тәмамлау_OFFSET(мәгълүмат_урнаштыру);if(мәгълүмат_урнаштыру==озынлык_VALUE)return;мәгълүмат_урнаштыру++;}int символ_коды=0;while(мәгълүмат_урнаштыру<озынлык_VALUE&&Mäten[мәгълүмат_урнаштыру]!='\n'&&символ_коды<COLUMN_урнаштыру){символ_коды+=Mäten[мәгълүмат_урнаштыру]=='\t'?4-символ_коды%4:너비(Mäten[мәгълүмат_урнаштыру]);мәгълүмат_урнаштыру=Киләсе_элемент(мәгълүмат_урнаштыру);}INDEX_VALUE=мәгълүмат_урнаштыру;}
static void 화면그리기(void){
    if(INDEX_VALUE>озынлык_VALUE)INDEX_VALUE=озынлык_VALUE;if(맨위>INDEX_VALUE)맨위=эшләтү(INDEX_VALUE);맨위=эшләтү(맨위);
    int юл_урнаштыру=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Mäten[순번]=='\n')юл_урнаштыру++;
    while(юл_урнаштыру>=юл_COUNT-1){맨위=тәмамлау_OFFSET(맨위);if(맨위<озынлык_VALUE)맨위++;юл_урнаштыру--;}
    int COLUMN_урнаштыру=COLUMN(INDEX_VALUE);if(COLUMN_урнаштыру<왼쪽)왼쪽=COLUMN_урнаштыру;if(COLUMN_урнаштыру-왼쪽>=COLUMNS-1)왼쪽=COLUMN_урнаштыру-COLUMNS+2;
    글내보내기("\033[?25l");int мәгълүмат_урнаштыру=맨위;
    for(int 반환값=0;반환값<юл_COUNT-1;반환값++){
        күчерү_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int символ_коды=0,그려진상태=0;
        if(мәгълүмат_урнаштыру>=озынлык_VALUE&&반환값>юл_урнаштыру){글내보내기("\033[90m~\033[0m");continue;}
        while(мәгълүмат_урнаштыру<озынлык_VALUE&&Mäten[мәгълүмат_урнаштыру]!='\n'){
            int Киләсе_OFFSET=Киләсе_элемент(мәгълүмат_урнаштыру),너비값=Mäten[мәгълүмат_урнаштыру]=='\t'?4-символ_коды%4:너비(Mäten[мәгълүмат_урнаштыру]);
            if(символ_коды>=왼쪽&&символ_коды-왼쪽+너비값<COLUMNS){
                if(Mäten[мәгълүмат_урнаштыру]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)байт_мәгълүмат(' ');}else if(Mäten[мәгълүмат_урнаштыру]<32||Mäten[мәгълүмат_урнаштыру]==127){байт_мәгълүмат('?');}else for(int 안쪽순번=мәгълүмат_урнаштыру;안쪽순번<Киләсе_OFFSET;안쪽순번++)байт_мәгълүмат(Mäten[안쪽순번]);그려진상태+=너비값;
            }символ_коды+=너비값;мәгълүмат_урнаштыру=Киләсе_OFFSET;
        }
        (void)그려진상태;if(мәгълүмат_урнаштыру<озынлык_VALUE)мәгълүмат_урнаштыру++;
    }
    күчерү_VALUE(юл_COUNT,1);글내보내기("\033[7m\033[2K");халәт_IMAGE=1;халәт_чират=0;글내보내기(өстәү?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(файл_кертү_исем[이름바이트수]&&이름바이트수<30)байт_мәгълүмат(файл_кертү_исем[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int юл=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Mäten[순번]=='\n')юл++;수치(юл);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int элемент_COUNT=0;글내보내기(" | ");while(알림문[элемент_COUNT]&&элемент_COUNT<20)байт_мәгълүмат(알림문[элемент_COUNT++]);}
    халәт_IMAGE=0;글내보내기("\033[0m");күчерү_VALUE(юл_урнаштыру+1,COLUMN_урнаштыру-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(көтүчән_ачкыч){int 셋째순번=көтүчән_ачкыч;көтүчән_ачкыч=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned үлчәмен_үзгәртү=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(үлчәмен_үзгәртү&65535)||юл_COUNT!=(int)(үлчәмен_үзгәртү>>16)){
            COLUMNS=үлчәмен_үзгәртү&65535;юл_COUNT=үлчәмен_үзгәртү>>16;화면그리기();
            if(ярдәм_категория){күчерү_VALUE(юл_COUNT,1);글내보내기("\033[0m\033[2K");байт_мәгълүмат(ярдәм_категория);글내보내기(команда);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned 현재위치=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-현재위치<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){көтүчән_ачкыч=셋째순번;return 27;}
    int элемент_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){элемент_COUNT=элемент_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return элемент_COUNT==3?1007:элемент_COUNT==5?1008:элемент_COUNT==6?1009:элемент_COUNT==1?1005:элемент_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int файл_дескриптор=ачу_файл(файл_кертү_исем,укымалы_язмалы|없으면만들기|내용비우기,0600);if(файл_дескриптор<0){알림문="Cannot open for save";return 0;}
    intptr_t элемент_COUNT=язу_файл_мәгълүмат(файл_дескриптор,Mäten,озынлык_VALUE);чик_файл(файл_дескриптор);if(элемент_COUNT!=озынлык_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Киләсе(void){int элемент_COUNT=0;while(FIND_кертү[элемент_COUNT])элемент_COUNT++;if(!элемент_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=озынлык_VALUE;순번++){int мәгълүмат_урнаштыру=(INDEX_VALUE+순번)%(озынлык_VALUE?озынлык_VALUE:1),안쪽순번=0;while(안쪽순번<элемент_COUNT&&мәгълүмат_урнаштыру+안쪽순번<озынлык_VALUE&&Mäten[мәгълүмат_урнаштыру+안쪽순번]==(unsigned char)FIND_кертү[안쪽순번])안쪽순번++;if(안쪽순번==элемент_COUNT){INDEX_VALUE=мәгълүмат_урнаштыру;알림문="Match";return;}}알림문="Pattern not found";}
static int тәкъдим(int категория_VALUE){
    int элемент_COUNT=0;команда[0]=0;
    for(;;){күчерү_VALUE(юл_COUNT,1);글내보내기("\033[0m\033[2K");байт_мәгълүмат(категория_VALUE);글내보내기(команда);출력비우기();ярдәм_категория=категория_VALUE;int 셋째순번=누름값();ярдәм_категория=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(элемент_COUNT){элемент_COUNT--;while(элемент_COUNT>0&&((unsigned char)команда[элемент_COUNT]&192)==128)элемент_COUNT--;команда[элемент_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&элемент_COUNT<120){команда[элемент_COUNT++]=셋째순번;команда[элемент_COUNT]=0;}
    }
    if(категория_VALUE=='/'){for(int 순번=0;순번<=элемент_COUNT;순번++)FIND_кертү[순번]=команда[순번];FIND_Киләсе();return 0;}
    if(같은지(команда,"q!"))return 1;
    if(같은지(команда,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(команда,"wq")||같은지(команда,"x"))return Store_VALUE();
    if(같은지(команда,"w")){Store_VALUE();return 0;}
    if(команда[0]=='w'&&команда[1]==' '){int 순번=2;while(команда[순번]==' ')순번++;int үлчәмен_үзгәртү=элемент_COUNT-순번;if(үлчәмен_үзгәртү<1||үлчәмен_үзгәртү>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<үлчәмен_үзгәртү;안쪽순번++)файл_кертү_исем[안쪽순번]=команда[순번+안쪽순번];файл_кертү_исем[үлчәмен_үзгәртү]=0;Store_VALUE();return 0;}
    int юл=0;for(int 순번=0;순번<элемент_COUNT;순번++){if(команда[순번]<'0'||команда[순번]>'9'){юл=0;break;}юл=юл*10+команда[순번]-'0';if(юл>16384){юл=0;break;}}
    if(юл){INDEX_VALUE=0;while(--юл&&INDEX_VALUE<озынлык_VALUE){INDEX_VALUE=тәмамлау_OFFSET(INDEX_VALUE);if(INDEX_VALUE<озынлык_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Start_кулланучы_кушымта(int 무시값){
    (void)무시값;if(кулланучы_аргумент_COUNT()!=1||кулланучы_аргумент(0,файл_кертү_исем,sizeof(файл_кертү_исем))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int файл_дескриптор=ачу_файл(файл_кертү_исем,укымалы_гына_VALUE,0);
    if(файл_дескриптор>=0){int элемент_COUNT=файл_үлчәмен_үзгәртү(файл_дескриптор);if(элемент_COUNT<0||элемент_COUNT>편집용량){чик_файл(файл_дескриптор);return 1;}озынлык_VALUE=파일자료읽기(файл_дескриптор,Mäten,элемент_COUNT);чик_файл(файл_дескриптор);if(озынлык_VALUE!=элемент_COUNT)return 1;for(int 순번=0;순번<озынлык_VALUE;순번++)if(!Mäten[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(오류번호!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;юл_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,чыгу_кушымта=0;
    while(!чыгу_кушымта){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Вертикаль(-1);continue;}if(셋째순번==1002){Вертикаль(1);continue;}if(셋째순번==1003){INDEX_VALUE=Киләсе_элемент(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=эшләтү(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=тәмамлау_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<юл_COUNT-2;순번++)Вертикаль(셋째순번==1008?-1:1);continue;}
        if(өстәү){
            if(셋째순번==27||셋째순번==3){өстәү=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<озынлык_VALUE)바이트지우기(INDEX_VALUE,Киләсе_элемент(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int элемент_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!элемент_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<элемент_COUNT;순번++){int символ_коды=누름값();if(символ_коды<128||символ_коды>191){көтүчән_ачкыч=символ_коды;유효함=0;break;}SECOND_VALUE[순번]=символ_коды;}
                if(유효함)덧붙이기(SECOND_VALUE,элемент_COUNT);
            }continue;
        }
        if(앞부분){int мәгълүмат_урнаштыру=앞부분;앞부분=0;if(мәгълүмат_урнаштыру=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(мәгълүмат_урнаштыру=='Z'&&셋째순번=='Z'){чыгу_кушымта=Store_VALUE();continue;}if((мәгълүмат_урнаштыру=='d'&&셋째순번=='d')||(мәгълүмат_урнаштыру=='y'&&셋째순번=='y')){int 첫째값=эшләтү(INDEX_VALUE),SECOND_VALUE=тәмамлау_OFFSET(INDEX_VALUE);if(SECOND_VALUE<озынлык_VALUE)SECOND_VALUE++;экземпляр_озынлык=SECOND_VALUE-첫째값;for(int 순번=0;순번<экземпляр_озынлык;순번++)복사자료[순번]=Mäten[첫째값+순번];if(мәгълүмат_урнаштыру=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){өстәү=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<тәмамлау_OFFSET(INDEX_VALUE))INDEX_VALUE=Киләсе_элемент(INDEX_VALUE);өстәү=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=эшләтү(INDEX_VALUE);өстәү=1;continue;}if(셋째순번=='A'){INDEX_VALUE=тәмамлау_OFFSET(INDEX_VALUE);өстәү=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char юл_тәмамлау='\n';INDEX_VALUE=셋째순번=='o'?тәмамлау_OFFSET(INDEX_VALUE):эшләтү(INDEX_VALUE);if(덧붙이기(&юл_тәмамлау,1)){if(셋째순번=='O')INDEX_VALUE--;өстәү=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Киләсе_элемент(INDEX_VALUE);continue;}if(셋째순번=='j'){Вертикаль(1);continue;}if(셋째순번=='k'){Вертикаль(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=эшләтү(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=тәмамлау_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=эшләтү(озынлык_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<озынлык_VALUE)바이트지우기(INDEX_VALUE,Киләсе_элемент(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&экземпляр_озынлык){INDEX_VALUE=тәмамлау_OFFSET(INDEX_VALUE);if(INDEX_VALUE<озынлык_VALUE)INDEX_VALUE++;덧붙이기(복사자료,экземпляр_озынлык);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=Mäten[순번];Mäten[순번]=баш_тарту_мәгълүмат[순번];баш_тарту_мәгълүмат[순번]=SECOND_VALUE;}int элемент_COUNT=озынлык_VALUE;озынлык_VALUE=баш_тарту_озынлык;баш_тарту_озынлык=элемент_COUNT;элемент_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=элемент_COUNT;элемент_COUNT=변경됨;변경됨=баш_тарту_Үзгәрешләр;баш_тарту_Үзгәрешләр=элемент_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){чыгу_кушымта=тәкъдим(셋째순번);continue;}if(셋째순번=='n'){FIND_Киләсе();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
