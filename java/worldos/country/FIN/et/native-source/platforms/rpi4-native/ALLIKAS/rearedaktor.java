// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bait_VALUE 경계를 지키는 삽입/삭제, 방향키, Käsk LOG_kirje, Tab Lõpetatud_VALUE. */
public final class rearedaktor {
    static boolean käsurida;
    static int[] LOG_kirje = new int[16 * 1024], 기록길이 = new int[16], salv_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_kirje_lõpeta_kõne, Otsi_VALUE, 저장길이, Suurus, kursor_VALUE, 후보수, 후보길이, START_aken;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd turvaline_kest kauge_ekraan run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String kirje_Loend, int START_ametikoht, int lõpeta_kõne_ametikoht, int 입력길이) {
        int bait_COUNT=0;
        for(int asukohaindeks=START_ametikoht;asukohaindeks<lõpeta_kõne_ametikoht;asukohaindeks++) {
            int koodipunkt=kirje_Loend.charAt(asukohaindeks);
            if(koodipunkt>=0xd800 && koodipunkt<=0xdbff && asukohaindeks+1<lõpeta_kõne_ametikoht)koodipunkt=0x10000+((koodipunkt-0xd800)<<10)+kirje_Loend.charAt(++asukohaindeks)-0xdc00;
            int number=koodipunkt<128?1:koodipunkt<2048?2:koodipunkt<65536?3:4;
            if(bait_COUNT+number>62)return;
            for(int SEQUENCE_VALUE=number-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[bait_COUNT++]=number==1?koodipunkt:SEQUENCE_VALUE==number-1?(number==2?0xc0:number==3?0xe0:0xf0)|(koodipunkt>>(6*SEQUENCE_VALUE)):0x80|((koodipunkt>>(6*SEQUENCE_VALUE))&63);
        }
        if(bait_COUNT<입력길이)return;
        for(int asukohaindeks=0;asukohaindeks<입력길이;asukohaindeks++)if(명령후보[asukohaindeks]!=명령해석기.Joon[asukohaindeks])return;
        후보수++;후보길이=bait_COUNT+1;
        for(int asukohaindeks=0;asukohaindeks<bait_COUNT;asukohaindeks++)후보[asukohaindeks]=명령후보[asukohaindeks];후보[bait_COUNT]=' ';
    }
    static int esikaamera_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Joon[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Tagasi_VALUE(int 읽는자리) { if (읽는자리 < Suurus) { 읽는자리++; while (읽는자리 < Suurus && (명령해석기.Joon[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_ametikoht, int sihtkoht_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = START_ametikoht; Loop_INDEX < sihtkoht_VALUE_INDEX; Loop_INDEX++) { int bait_andmed = 명령해석기.Joon[Loop_INDEX]; if ((bait_andmed & 192) == 128) continue; 글칸수 += bait_andmed >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void uuesti_proovima_VALUE() {
        단말.Kirjutamine("\r\u001b[2K");
        단말.Kirjutamine(käsurida ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Joon 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Tahvel.terminal(13) & 65535; return COLUMNS - (käsurida ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_VALUE < START_aken) START_aken = kursor_VALUE;
        while (폭(START_aken, kursor_VALUE) > 보이는폭()) START_aken = Tagasi_VALUE(START_aken);
        int lõpeta_kõne_ametikoht = START_aken;
        while (lõpeta_kõne_ametikoht < Suurus && 폭(START_aken, Tagasi_VALUE(lõpeta_kõne_ametikoht)) <= 보이는폭()) lõpeta_kõne_ametikoht = Tagasi_VALUE(lõpeta_kõne_ametikoht);
        단말.Kirjutamine("\r\u001b["); 단말.number(käsurida ? 16 : 7); 단말.Kirjutamine("G\u001b[K");
        if (START_aken > 0) 단말.문자('<');
        for (int Loop_INDEX = START_aken; Loop_INDEX < lõpeta_kõne_ametikoht; Loop_INDEX++) Tahvel.직렬쓰기(명령해석기.Joon[Loop_INDEX]);
        단말.문자(lõpeta_kõne_ametikoht < Suurus ? '>' : ' ');
        단말.Kirjutamine("\u001b["); 단말.number(폭(kursor_VALUE, lõpeta_kõne_ametikoht) + 1); 단말.문자('D');
        가로보기 = START_aken > 0 || lõpeta_kõne_ametikoht < Suurus || 폭(0, Suurus) > 보이는폭();
    }
    static void Lisa_LOG() {
        if (!käsurida || Suurus == 0 || Suurus > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_kirje_lõpeta_kõne + 15) % 16; boolean 같은여부 = 기록길이[마지막자리] == Suurus;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Suurus; Loop_INDEX++) if (LOG_kirje[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.Joon[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        기록길이[LOG_kirje_lõpeta_kõne] = Suurus; for (int Loop_INDEX = 0; Loop_INDEX < Suurus; Loop_INDEX++) LOG_kirje[LOG_kirje_lõpeta_kõne * 1024 + Loop_INDEX] = 명령해석기.Joon[Loop_INDEX];
        LOG_kirje_lõpeta_kõne = (LOG_kirje_lõpeta_kõne + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!käsurida) return;
        if (Otsi_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Suurus; for (int Loop_INDEX = 0; Loop_INDEX < Suurus; Loop_INDEX++) salv_VALUE[Loop_INDEX] = 명령해석기.Joon[Loop_INDEX]; }
        int Edasi_ametikoht = Otsi_VALUE + DELTA_VALUE; if (Edasi_ametikoht < 0 || Edasi_ametikoht > LOG_COUNT) return; Otsi_VALUE = Edasi_ametikoht;
        if (Otsi_VALUE == 0) { Suurus = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Suurus; Loop_INDEX++) 명령해석기.Joon[Loop_INDEX] = salv_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_kirje_lõpeta_kõne + 16 - Otsi_VALUE) % 16; Suurus = 기록길이[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Suurus; Loop_INDEX++) 명령해석기.Joon[Loop_INDEX] = LOG_kirje[보관칸 * 1024 + Loop_INDEX]; }
        kursor_VALUE = Suurus; uuesti_proovima_VALUE();
    }
    static void saade_LOG() {
        for (int kirje_COUNT = 0; kirje_COUNT < LOG_COUNT; kirje_COUNT++) {
            int 보관칸 = (LOG_kirje_lõpeta_kõne + 16 - LOG_COUNT + kirje_COUNT) % 16; 단말.number(kirje_COUNT + 1); 단말.Kirjutamine("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < 기록길이[보관칸]; Loop_INDEX++) Tahvel.직렬쓰기(LOG_kirje[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] andmed_ARRAY, int START_ametikoht, int kirje_COUNT, int 접두말, int kokku_COUNT, boolean kaust_number) {
        if (kirje_COUNT < kokku_COUNT || kirje_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < kokku_COUNT; Loop_INDEX++) if (andmed_ARRAY[START_ametikoht + Loop_INDEX] != 명령해석기.Joon[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = kirje_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = andmed_ARRAY[START_ametikoht + Loop_INDEX]; 후보[kirje_COUNT] = kaust_number ? '/' : ' ';
    }
    static void Lõpetatud_VALUE() {
        if (!käsurida || kursor_VALUE != Suurus) return;
        int 시작점 = Suurus; while (시작점 > 0 && 명령해석기.Joon[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Suurus; Loop_INDEX++) if (명령해석기.Joon[Loop_INDEX] == '/' || 명령해석기.Joon[Loop_INDEX] == '"' || 명령해석기.Joon[Loop_INDEX] == 39 || 명령해석기.Joon[Loop_INDEX] == '\\') return;
        후보수 = 0; int kirje_COUNT = Suurus - 시작점;
        if (시작점 == 0) {
            for(int Loend_INDEX=0;Loend_INDEX<2;Loend_INDEX++) {
                String kirje_Loend=Loend_INDEX==0?명령들:관리명령.Lõpetatud_Word();
                int 읽는자리=0;
                while(읽는자리<kirje_Loend.length()) {
                    int lõpeta_kõne_ametikoht=읽는자리;while(lõpeta_kõne_ametikoht<kirje_Loend.length() && kirje_Loend.charAt(lõpeta_kõne_ametikoht)!=' ')lõpeta_kõne_ametikoht++;
                    명령후보넣기(kirje_Loend,읽는자리,lõpeta_kõne_ametikoht,kirje_COUNT);읽는자리=lõpeta_kõne_ametikoht+1;
                }
            }
        } else {
            Mälu_Failid.tee_START(1); Mälu_Failid.tee_bait(0, '.'); Mälu_Failid.normaliseerima_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Mälu_Failid.Fail_COUNT; Loop_INDEX++) {
                int START_ametikoht = Mälu_Failid.kirje_START(Mälu_Failid.Nimi_2, Loop_INDEX * 64, Mälu_Failid.이름길이[Loop_INDEX]);
                if (START_ametikoht >= 0) 후보넣기(Mälu_Failid.Nimi_2, Loop_INDEX * 64 + START_ametikoht, Mälu_Failid.이름길이[Loop_INDEX] - START_ametikoht, 시작점, kirje_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int START_ametikoht = Mälu_Failid.kirje_START(Mälu_Failid.kaust_nimetus, Loop_INDEX * 64, Mälu_Failid.폴더길이[Loop_INDEX]);
                if (START_ametikoht >= 0) 후보넣기(Mälu_Failid.kaust_nimetus, Loop_INDEX * 64 + START_ametikoht, Mälu_Failid.폴더길이[Loop_INDEX] - START_ametikoht, 시작점, kirje_COUNT, true);
            }
        }
        if (후보수 != 1) { Tahvel.직렬쓰기(7); return; }
        for (int Loop_INDEX = kirje_COUNT; Loop_INDEX < 후보길이 && Suurus < 명령해석기.Joon.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.Joon[Suurus++] = '\\';
            명령해석기.Joon[Suurus++] = 후보[Loop_INDEX];
        }
        kursor_VALUE = Suurus; uuesti_proovima_VALUE();
    }
    static int 탈출읽기() {
        int 시작점 = Tahvel.밀리초();
        while (Tahvel.밀리초() - 시작점 < 80) { int bait_andmed = Tahvel.직렬읽기(); if (bait_andmed >= 0) return bait_andmed; Tahvel.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int kirje_COUNT = 0, lõpeta_kõne_ametikoht = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bait_andmed = 탈출읽기(); if (bait_andmed < 0) return; if (bait_andmed >= '0' && bait_andmed <= '9') kirje_COUNT = kirje_COUNT * 10 + bait_andmed - '0'; else { lõpeta_kõne_ametikoht = bait_andmed; break; } }
        if (lõpeta_kõne_ametikoht == 'A') 기록이동(1);
        else if (lõpeta_kõne_ametikoht == 'B') 기록이동(-1);
        else if (lõpeta_kõne_ametikoht == 'C') { kursor_VALUE = Tagasi_VALUE(kursor_VALUE); uuesti_proovima_VALUE(); }
        else if (lõpeta_kõne_ametikoht == 'D') { kursor_VALUE = esikaamera_VALUE(kursor_VALUE); uuesti_proovima_VALUE(); }
        else if (lõpeta_kõne_ametikoht == 'H' || lõpeta_kõne_ametikoht == '~' && (kirje_COUNT == 1 || kirje_COUNT == 7)) { kursor_VALUE = 0; uuesti_proovima_VALUE(); }
        else if (lõpeta_kõne_ametikoht == 'F' || lõpeta_kõne_ametikoht == '~' && (kirje_COUNT == 4 || kirje_COUNT == 8)) { kursor_VALUE = Suurus; uuesti_proovima_VALUE(); }
        else if (lõpeta_kõne_ametikoht == '~' && kirje_COUNT == 3 && kursor_VALUE < Suurus) {
            int Edasi_ametikoht = Tagasi_VALUE(kursor_VALUE); for (int Loop_INDEX = Edasi_ametikoht; Loop_INDEX < Suurus; Loop_INDEX++) 명령해석기.Joon[Loop_INDEX - Edasi_ametikoht + kursor_VALUE] = 명령해석기.Joon[Loop_INDEX]; Suurus -= Edasi_ametikoht - kursor_VALUE; uuesti_proovima_VALUE();
        }
        else if (lõpeta_kõne_ametikoht == '~' && (kirje_COUNT == 5 || kirje_COUNT == 6)) Tahvel.terminal(kirje_COUNT == 5 ? 5 : 6);
        else if (lõpeta_kõne_ametikoht == '~' && kirje_COUNT == 24 && käsurida) { 명령해석기.terminal(true); }
    }
    static int Lugemine() {
        if (!aken_seanss.이어읽기) { Suurus = kursor_VALUE = Otsi_VALUE = START_aken = 0; 가로보기 = false; }
        else { aken_seanss.이어읽기 = false; uuesti_proovima_VALUE(); } boolean ületäide = false;
        while (true) {
            int bait_andmed = Tahvel.직렬읽기(); if (bait_andmed == -4096) return -3;
            if (Tahvel.terminal(14) != 0) uuesti_proovima_VALUE(); if (bait_andmed < 0) { Tahvel.YIELD_CPU(); continue; }
            if (bait_andmed == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bait_andmed == 13;
            if (bait_andmed == 27) { 탈출(); continue; }
            if (bait_andmed == 3) { 단말.Kirjutamine("^C\n"); return -1; }
            if (bait_andmed == 4 && Suurus == 0 && käsurida) { if (Tahvel.terminal(2) != 0) 명령해석기.terminal(true); return -1; }
            if (bait_andmed == 13 || bait_andmed == 10) { 단말.문자(10); if (!ületäide) Lisa_LOG(); return ületäide ? -2 : Suurus; }
            if (bait_andmed == 9 && käsurida) { Lõpetatud_VALUE(); continue; }
            if (bait_andmed == 1 || bait_andmed == 5) { kursor_VALUE = bait_andmed == 1 ? 0 : Suurus; uuesti_proovima_VALUE(); continue; }
            if (bait_andmed == 8 || bait_andmed == 127 || bait_andmed == 21) {
                if (bait_andmed == 21) { for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Suurus; Loop_INDEX++) 명령해석기.Joon[Loop_INDEX - kursor_VALUE] = 명령해석기.Joon[Loop_INDEX]; Suurus -= kursor_VALUE; kursor_VALUE = 0; }
                else if (kursor_VALUE > 0) { int 변경전 = esikaamera_VALUE(kursor_VALUE); for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Suurus; Loop_INDEX++) 명령해석기.Joon[Loop_INDEX - kursor_VALUE + 변경전] = 명령해석기.Joon[Loop_INDEX]; Suurus -= kursor_VALUE - 변경전; kursor_VALUE = 변경전; }
                uuesti_proovima_VALUE(); continue;
            }
            if (bait_andmed == 11) { Suurus = kursor_VALUE; uuesti_proovima_VALUE(); continue; }
            if (bait_andmed < 32 && bait_andmed != 9) continue;
            if (Suurus == 명령해석기.Joon.length) { ületäide = true; continue; }
            for (int Loop_INDEX = Suurus; Loop_INDEX > kursor_VALUE; Loop_INDEX--) 명령해석기.Joon[Loop_INDEX] = 명령해석기.Joon[Loop_INDEX - 1];
            명령해석기.Joon[kursor_VALUE++] = bait_andmed; Suurus++;
            if (kursor_VALUE == Suurus && !가로보기 && 폭(0, Suurus) <= 보이는폭()) Tahvel.직렬쓰기(bait_andmed);
            else if (kursor_VALUE == Suurus) 보이는줄(); else uuesti_proovima_VALUE();
        }
    }
}
