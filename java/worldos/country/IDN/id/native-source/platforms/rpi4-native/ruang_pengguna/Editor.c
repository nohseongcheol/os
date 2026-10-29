/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Editor_kapasitas 16384
static unsigned char teks[Editor_kapasitas],batalkan_data[Editor_kapasitas],복사자료[Editor_kapasitas],KR_data[1024];
static int panjang_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,Sisipan,batalkan_panjang,위쪽,batalkan_Perubahan,되돌림있음,salin_panjang,사용량,COLUMNS=68,ROW_COUNT=19;
static char file_entri_nama[64],perintah[128],FIND_entri[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned sedang_diproses_Kunci;
static int bantuan_area,Status_foto,Status_antrean;
static void rata(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_data,사용량,0,0,0);사용량=0;}}
static void byte_data(unsigned kode_karakter){if(Status_foto){if((kode_karakter&192)!=128){Status_antrean+=kode_karakter>=196?2:1;}if(Status_antrean>=COLUMNS)return;}if(사용량==(int)sizeof(KR_data))rata();KR_data[사용량++]=kode_karakter;}
static void 글내보내기(const char *string_data){while(*string_data)byte_data((unsigned char)*string_data++);}
static void 수치(unsigned item_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+item_COUNT%10;item_COUNT/=10;}while(item_COUNT);while(순번)byte_data(SECOND_VALUE[--순번]);}
static void gerak_VALUE(int ROW_posisi,int kolom_posisi){글내보내기("\033[");수치(ROW_posisi);byte_data(';');수치(kolom_posisi);byte_data('H');}
static int 이전항목(int data_posisi){if(data_posisi){data_posisi--;while(data_posisi>0&&(teks[data_posisi]&192)==128)data_posisi--;}return data_posisi;}
static int Berikutnya_item(int data_posisi){if(data_posisi<panjang_VALUE){data_posisi++;while(data_posisi<panjang_VALUE&&(teks[data_posisi]&192)==128)data_posisi++;}return data_posisi;}
static int jalankan(int data_posisi){while(data_posisi>0&&teks[data_posisi-1]!='\n')data_posisi--;return data_posisi;}
static int mengakhiri_OFFSET(int data_posisi){while(data_posisi<panjang_VALUE&&teks[data_posisi]!='\n')data_posisi++;return data_posisi;}
static int 너비(unsigned kode_karakter){return kode_karakter>=196?2:1;}
static int kolom(int data_posisi){int kode_karakter=0;for(int 순번=jalankan(data_posisi);순번<data_posisi;순번=Berikutnya_item(순번))kode_karakter+=teks[순번]=='\t'?4-kode_karakter%4:너비(teks[순번]);return kode_karakter;}
static void titik_pemeriksaan(void){for(int 순번=0;순번<panjang_VALUE;순번++)batalkan_data[순번]=teks[순번];batalkan_panjang=panjang_VALUE;위쪽=INDEX_VALUE;batalkan_Perubahan=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){titik_pemeriksaan();for(int 순번=도착위치;순번<panjang_VALUE;순번++)teks[출발위치+순번-도착위치]=teks[순번];panjang_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int tambah_VALUE(const unsigned char *string_data,int item_COUNT){if(item_COUNT>Editor_kapasitas-panjang_VALUE){알림문="File full (16384 bytes)";return 0;}titik_pemeriksaan();for(int 순번=panjang_VALUE-1;순번>=INDEX_VALUE;순번--)teks[순번+item_COUNT]=teks[순번];for(int 순번=0;순번<item_COUNT;순번++)teks[INDEX_VALUE+순번]=string_data[순번];panjang_VALUE+=item_COUNT;INDEX_VALUE+=item_COUNT;변경됨=1;return 1;}
static void Vertikal(int 차이){int kolom_posisi=kolom(INDEX_VALUE),data_posisi=jalankan(INDEX_VALUE);if(차이<0){if(!data_posisi)return;data_posisi=jalankan(data_posisi-1);}else{data_posisi=mengakhiri_OFFSET(data_posisi);if(data_posisi==panjang_VALUE)return;data_posisi++;}int kode_karakter=0;while(data_posisi<panjang_VALUE&&teks[data_posisi]!='\n'&&kode_karakter<kolom_posisi){kode_karakter+=teks[data_posisi]=='\t'?4-kode_karakter%4:너비(teks[data_posisi]);data_posisi=Berikutnya_item(data_posisi);}INDEX_VALUE=data_posisi;}
static void 화면그리기(void){
    if(INDEX_VALUE>panjang_VALUE)INDEX_VALUE=panjang_VALUE;if(맨위>INDEX_VALUE)맨위=jalankan(INDEX_VALUE);맨위=jalankan(맨위);
    int ROW_posisi=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(teks[순번]=='\n')ROW_posisi++;
    while(ROW_posisi>=ROW_COUNT-1){맨위=mengakhiri_OFFSET(맨위);if(맨위<panjang_VALUE)맨위++;ROW_posisi--;}
    int kolom_posisi=kolom(INDEX_VALUE);if(kolom_posisi<왼쪽)왼쪽=kolom_posisi;if(kolom_posisi-왼쪽>=COLUMNS-1)왼쪽=kolom_posisi-COLUMNS+2;
    글내보내기("\033[?25l");int data_posisi=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        gerak_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int kode_karakter=0,그려진상태=0;
        if(data_posisi>=panjang_VALUE&&반환값>ROW_posisi){글내보내기("\033[90m~\033[0m");continue;}
        while(data_posisi<panjang_VALUE&&teks[data_posisi]!='\n'){
            int Berikutnya_OFFSET=Berikutnya_item(data_posisi),너비값=teks[data_posisi]=='\t'?4-kode_karakter%4:너비(teks[data_posisi]);
            if(kode_karakter>=왼쪽&&kode_karakter-왼쪽+너비값<COLUMNS){
                if(teks[data_posisi]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_data(' ');}else if(teks[data_posisi]<32||teks[data_posisi]==127){byte_data('?');}else for(int 안쪽순번=data_posisi;안쪽순번<Berikutnya_OFFSET;안쪽순번++)byte_data(teks[안쪽순번]);그려진상태+=너비값;
            }kode_karakter+=너비값;data_posisi=Berikutnya_OFFSET;
        }
        (void)그려진상태;if(data_posisi<panjang_VALUE)data_posisi++;
    }
    gerak_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");Status_foto=1;Status_antrean=0;글내보내기(Sisipan?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(file_entri_nama[이름바이트수]&&이름바이트수<30)byte_data(file_entri_nama[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int baris_masukan=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(teks[순번]=='\n')baris_masukan++;수치(baris_masukan);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int item_COUNT=0;글내보내기(" | ");while(알림문[item_COUNT]&&item_COUNT<20)byte_data(알림문[item_COUNT++]);}
    Status_foto=0;글내보내기("\033[0m");gerak_VALUE(ROW_posisi+1,kolom_posisi-왼쪽+1);글내보내기("\033[?25h");rata();
}
static int 누름값(void){
    if(sedang_diproses_Kunci){int 셋째순번=sedang_diproses_Kunci;sedang_diproses_Kunci=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Ukuran=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Ukuran&65535)||ROW_COUNT!=(int)(Ukuran>>16)){
            COLUMNS=Ukuran&65535;ROW_COUNT=Ukuran>>16;화면그리기();
            if(bantuan_area){gerak_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_data(bantuan_area);글내보내기(perintah);rata();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned saat_ini_posisi=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-saat_ini_posisi<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){sedang_diproses_Kunci=셋째순번;return 27;}
    int item_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){item_COUNT=item_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return item_COUNT==3?1007:item_COUNT==5?1008:item_COUNT==6?1009:item_COUNT==1?1005:item_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int file_handel=buat_file(file_entri_nama,baca_tulis|없으면만들기|내용비우기,0600);if(file_handel<0){알림문="Cannot open for save";return 0;}
    intptr_t item_COUNT=tulis_file_data(file_handel,teks,panjang_VALUE);Tutup_file(file_handel);if(item_COUNT!=panjang_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Berikutnya(void){int item_COUNT=0;while(FIND_entri[item_COUNT])item_COUNT++;if(!item_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=panjang_VALUE;순번++){int data_posisi=(INDEX_VALUE+순번)%(panjang_VALUE?panjang_VALUE:1),안쪽순번=0;while(안쪽순번<item_COUNT&&data_posisi+안쪽순번<panjang_VALUE&&teks[data_posisi+안쪽순번]==(unsigned char)FIND_entri[안쪽순번])안쪽순번++;if(안쪽순번==item_COUNT){INDEX_VALUE=data_posisi;알림문="Match";return;}}알림문="Pattern not found";}
static int minta(int area_VALUE){
    int item_COUNT=0;perintah[0]=0;
    for(;;){gerak_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");byte_data(area_VALUE);글내보내기(perintah);rata();bantuan_area=area_VALUE;int 셋째순번=누름값();bantuan_area=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(item_COUNT){item_COUNT--;while(item_COUNT>0&&((unsigned char)perintah[item_COUNT]&192)==128)item_COUNT--;perintah[item_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&item_COUNT<120){perintah[item_COUNT++]=셋째순번;perintah[item_COUNT]=0;}
    }
    if(area_VALUE=='/'){for(int 순번=0;순번<=item_COUNT;순번++)FIND_entri[순번]=perintah[순번];FIND_Berikutnya();return 0;}
    if(같은지(perintah,"q!"))return 1;
    if(같은지(perintah,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(perintah,"wq")||같은지(perintah,"x"))return Store_VALUE();
    if(같은지(perintah,"w")){Store_VALUE();return 0;}
    if(perintah[0]=='w'&&perintah[1]==' '){int 순번=2;while(perintah[순번]==' ')순번++;int Ukuran=item_COUNT-순번;if(Ukuran<1||Ukuran>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Ukuran;안쪽순번++)file_entri_nama[안쪽순번]=perintah[순번+안쪽순번];file_entri_nama[Ukuran]=0;Store_VALUE();return 0;}
    int baris_masukan=0;for(int 순번=0;순번<item_COUNT;순번++){if(perintah[순번]<'0'||perintah[순번]>'9'){baris_masukan=0;break;}baris_masukan=baris_masukan*10+perintah[순번]-'0';if(baris_masukan>16384){baris_masukan=0;break;}}
    if(baris_masukan){INDEX_VALUE=0;while(--baris_masukan&&INDEX_VALUE<panjang_VALUE){INDEX_VALUE=mengakhiri_OFFSET(INDEX_VALUE);if(INDEX_VALUE<panjang_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int Mulai_pengguna_apl(int 무시값){
    (void)무시값;if(pengguna_argumen_COUNT()!=1||pengguna_argumen(0,file_entri_nama,sizeof(file_entri_nama))<0){글내보내기("Usage: vi FILE\n");rata();return 2;}
    int file_handel=buat_file(file_entri_nama,baca_saja_VALUE,0);
    if(file_handel>=0){int item_COUNT=ukuran_file(file_handel);if(item_COUNT<0||item_COUNT>Editor_kapasitas){Tutup_file(file_handel);return 1;}panjang_VALUE=파일자료읽기(file_handel,teks,item_COUNT);Tutup_file(file_handel);if(panjang_VALUE!=item_COUNT)return 1;for(int 순번=0;순번<panjang_VALUE;순번++)if(!teks[순번]){글내보내기("vi: NUL byte in text file\n");rata();return 1;}}
    else if(nomor_kesalahan!=2){글내보내기("vi: cannot read file\n");rata();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");rata();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");rata();
    int 앞부분=0,berhenti_apl=0;
    while(!berhenti_apl){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Vertikal(-1);continue;}if(셋째순번==1002){Vertikal(1);continue;}if(셋째순번==1003){INDEX_VALUE=Berikutnya_item(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=jalankan(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=mengakhiri_OFFSET(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Vertikal(셋째순번==1008?-1:1);continue;}
        if(Sisipan){
            if(셋째순번==27||셋째순번==3){Sisipan=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<panjang_VALUE)바이트지우기(INDEX_VALUE,Berikutnya_item(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int item_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!item_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<item_COUNT;순번++){int kode_karakter=누름값();if(kode_karakter<128||kode_karakter>191){sedang_diproses_Kunci=kode_karakter;유효함=0;break;}SECOND_VALUE[순번]=kode_karakter;}
                if(유효함)tambah_VALUE(SECOND_VALUE,item_COUNT);
            }continue;
        }
        if(앞부분){int data_posisi=앞부분;앞부분=0;if(data_posisi=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(data_posisi=='Z'&&셋째순번=='Z'){berhenti_apl=Store_VALUE();continue;}if((data_posisi=='d'&&셋째순번=='d')||(data_posisi=='y'&&셋째순번=='y')){int 첫째값=jalankan(INDEX_VALUE),SECOND_VALUE=mengakhiri_OFFSET(INDEX_VALUE);if(SECOND_VALUE<panjang_VALUE)SECOND_VALUE++;salin_panjang=SECOND_VALUE-첫째값;for(int 순번=0;순번<salin_panjang;순번++)복사자료[순번]=teks[첫째값+순번];if(data_posisi=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Sisipan=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<mengakhiri_OFFSET(INDEX_VALUE))INDEX_VALUE=Berikutnya_item(INDEX_VALUE);Sisipan=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=jalankan(INDEX_VALUE);Sisipan=1;continue;}if(셋째순번=='A'){INDEX_VALUE=mengakhiri_OFFSET(INDEX_VALUE);Sisipan=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char baris_mengakhiri='\n';INDEX_VALUE=셋째순번=='o'?mengakhiri_OFFSET(INDEX_VALUE):jalankan(INDEX_VALUE);if(tambah_VALUE(&baris_mengakhiri,1)){if(셋째순번=='O')INDEX_VALUE--;Sisipan=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Berikutnya_item(INDEX_VALUE);continue;}if(셋째순번=='j'){Vertikal(1);continue;}if(셋째순번=='k'){Vertikal(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=jalankan(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=mengakhiri_OFFSET(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=jalankan(panjang_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<panjang_VALUE)바이트지우기(INDEX_VALUE,Berikutnya_item(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&salin_panjang){INDEX_VALUE=mengakhiri_OFFSET(INDEX_VALUE);if(INDEX_VALUE<panjang_VALUE)INDEX_VALUE++;tambah_VALUE(복사자료,salin_panjang);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_kapasitas;순번++){unsigned char SECOND_VALUE=teks[순번];teks[순번]=batalkan_data[순번];batalkan_data[순번]=SECOND_VALUE;}int item_COUNT=panjang_VALUE;panjang_VALUE=batalkan_panjang;batalkan_panjang=item_COUNT;item_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=item_COUNT;item_COUNT=변경됨;변경됨=batalkan_Perubahan;batalkan_Perubahan=item_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){berhenti_apl=minta(셋째순번);continue;}if(셋째순번=='n'){FIND_Berikutnya();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");rata();사용자호출(16,2,0,0,0,0,0);return 0;
}
