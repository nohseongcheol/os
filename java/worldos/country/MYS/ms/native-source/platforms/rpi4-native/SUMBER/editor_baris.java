// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bait_VALUE 경계를 지키는 삽입/삭제, 방향키, Perintah LOG_baris, Tab Selesai_VALUE. */
public final class editor_baris {
    static boolean baris_perintah;
    static int[] LOG_baris = new int[16 * 1024], LOG_kepanjangan = new int[16], stor_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_baris_tamat, Cari_VALUE, 저장길이, Saiz, kursor_VALUE, 후보수, 후보길이, Mula_tetingkap;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd selamat_cangkerang jauh_papar run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String pemasukan_Senarai, int Mula_jawatan, int tamat_jawatan, int 입력길이) {
        int bait_COUNT=0;
        for(int jawatan_INDEX=Mula_jawatan;jawatan_INDEX<tamat_jawatan;jawatan_INDEX++) {
            int titik_kod=pemasukan_Senarai.charAt(jawatan_INDEX);
            if(titik_kod>=0xd800 && titik_kod<=0xdbff && jawatan_INDEX+1<tamat_jawatan)titik_kod=0x10000+((titik_kod-0xd800)<<10)+pemasukan_Senarai.charAt(++jawatan_INDEX)-0xdc00;
            int 수=titik_kod<128?1:titik_kod<2048?2:titik_kod<65536?3:4;
            if(bait_COUNT+수>62)return;
            for(int jujukan_VALUE=수-1;jujukan_VALUE>=0;jujukan_VALUE--)명령후보[bait_COUNT++]=수==1?titik_kod:jujukan_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(titik_kod>>(6*jujukan_VALUE)):0x80|((titik_kod>>(6*jujukan_VALUE))&63);
        }
        if(bait_COUNT<입력길이)return;
        for(int jawatan_INDEX=0;jawatan_INDEX<입력길이;jawatan_INDEX++)if(명령후보[jawatan_INDEX]!=pentafsir_perintah.baris[jawatan_INDEX])return;
        후보수++;후보길이=bait_COUNT+1;
        for(int jawatan_INDEX=0;jawatan_INDEX<bait_COUNT;jawatan_INDEX++)후보[jawatan_INDEX]=명령후보[jawatan_INDEX];후보[bait_COUNT]=' ';
    }
    static int hadapan_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (pentafsir_perintah.baris[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_VALUE(int 읽는자리) { if (읽는자리 < Saiz) { 읽는자리++; while (읽는자리 < Saiz && (pentafsir_perintah.baris[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Mula_jawatan, int destinasi_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Mula_jawatan; Loop_INDEX < destinasi_VALUE_INDEX; Loop_INDEX++) { int bait_data = pentafsir_perintah.baris[Loop_INDEX]; if ((bait_data & 192) == 128) continue; 글칸수 += bait_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Tulis("\r\u001b[2K");
        단말.Tulis(baris_perintah ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 baris 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Papan.Terminal(13) & 65535; return COLUMNS - (baris_perintah ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_VALUE < Mula_tetingkap) Mula_tetingkap = kursor_VALUE;
        while (폭(Mula_tetingkap, kursor_VALUE) > 보이는폭()) Mula_tetingkap = BACK_VALUE(Mula_tetingkap);
        int tamat_jawatan = Mula_tetingkap;
        while (tamat_jawatan < Saiz && 폭(Mula_tetingkap, BACK_VALUE(tamat_jawatan)) <= 보이는폭()) tamat_jawatan = BACK_VALUE(tamat_jawatan);
        단말.Tulis("\r\u001b["); 단말.수(baris_perintah ? 16 : 7); 단말.Tulis("G\u001b[K");
        if (Mula_tetingkap > 0) 단말.문자('<');
        for (int Loop_INDEX = Mula_tetingkap; Loop_INDEX < tamat_jawatan; Loop_INDEX++) Papan.직렬쓰기(pentafsir_perintah.baris[Loop_INDEX]);
        단말.문자(tamat_jawatan < Saiz ? '>' : ' ');
        단말.Tulis("\u001b["); 단말.수(폭(kursor_VALUE, tamat_jawatan) + 1); 단말.문자('D');
        가로보기 = Mula_tetingkap > 0 || tamat_jawatan < Saiz || 폭(0, Saiz) > 보이는폭();
    }
    static void Tambah_LOG() {
        if (!baris_perintah || Saiz == 0 || Saiz > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_baris_tamat + 15) % 16; boolean 같은여부 = LOG_kepanjangan[마지막자리] == Saiz;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Saiz; Loop_INDEX++) if (LOG_baris[마지막자리 * 1024 + Loop_INDEX] != pentafsir_perintah.baris[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_kepanjangan[LOG_baris_tamat] = Saiz; for (int Loop_INDEX = 0; Loop_INDEX < Saiz; Loop_INDEX++) LOG_baris[LOG_baris_tamat * 1024 + Loop_INDEX] = pentafsir_perintah.baris[Loop_INDEX];
        LOG_baris_tamat = (LOG_baris_tamat + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!baris_perintah) return;
        if (Cari_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Saiz; for (int Loop_INDEX = 0; Loop_INDEX < Saiz; Loop_INDEX++) stor_VALUE[Loop_INDEX] = pentafsir_perintah.baris[Loop_INDEX]; }
        int Seterusnya_jawatan = Cari_VALUE + DELTA_VALUE; if (Seterusnya_jawatan < 0 || Seterusnya_jawatan > LOG_COUNT) return; Cari_VALUE = Seterusnya_jawatan;
        if (Cari_VALUE == 0) { Saiz = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Saiz; Loop_INDEX++) pentafsir_perintah.baris[Loop_INDEX] = stor_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_baris_tamat + 16 - Cari_VALUE) % 16; Saiz = LOG_kepanjangan[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Saiz; Loop_INDEX++) pentafsir_perintah.baris[Loop_INDEX] = LOG_baris[보관칸 * 1024 + Loop_INDEX]; }
        kursor_VALUE = Saiz; 다시();
    }
    static void tayang_LOG() {
        for (int pemasukan_COUNT = 0; pemasukan_COUNT < LOG_COUNT; pemasukan_COUNT++) {
            int 보관칸 = (LOG_baris_tamat + 16 - LOG_COUNT + pemasukan_COUNT) % 16; 단말.수(pemasukan_COUNT + 1); 단말.Tulis("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_kepanjangan[보관칸]; Loop_INDEX++) Papan.직렬쓰기(LOG_baris[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_ARRAY, int Mula_jawatan, int pemasukan_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (pemasukan_COUNT < 총수 || pemasukan_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (data_ARRAY[Mula_jawatan + Loop_INDEX] != pentafsir_perintah.baris[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = pemasukan_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = data_ARRAY[Mula_jawatan + Loop_INDEX]; 후보[pemasukan_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void Selesai_VALUE() {
        if (!baris_perintah || kursor_VALUE != Saiz) return;
        int 시작점 = Saiz; while (시작점 > 0 && pentafsir_perintah.baris[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Saiz; Loop_INDEX++) if (pentafsir_perintah.baris[Loop_INDEX] == '/' || pentafsir_perintah.baris[Loop_INDEX] == '"' || pentafsir_perintah.baris[Loop_INDEX] == 39 || pentafsir_perintah.baris[Loop_INDEX] == '\\') return;
        후보수 = 0; int pemasukan_COUNT = Saiz - 시작점;
        if (시작점 == 0) {
            for(int Senarai_INDEX=0;Senarai_INDEX<2;Senarai_INDEX++) {
                String pemasukan_Senarai=Senarai_INDEX==0?명령들:관리명령.Selesai_Word();
                int 읽는자리=0;
                while(읽는자리<pemasukan_Senarai.length()) {
                    int tamat_jawatan=읽는자리;while(tamat_jawatan<pemasukan_Senarai.length() && pemasukan_Senarai.charAt(tamat_jawatan)!=' ')tamat_jawatan++;
                    명령후보넣기(pemasukan_Senarai,읽는자리,tamat_jawatan,pemasukan_COUNT);읽는자리=tamat_jawatan+1;
                }
            }
        } else {
            Memori_Fail.laluan_Mula(1); Memori_Fail.laluan_bait(0, '.'); Memori_Fail.menormalkan_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Memori_Fail.fail_COUNT; Loop_INDEX++) {
                int Mula_jawatan = Memori_Fail.pemasukan_Mula(Memori_Fail.Nama, Loop_INDEX * 64, Memori_Fail.이름길이[Loop_INDEX]);
                if (Mula_jawatan >= 0) 후보넣기(Memori_Fail.Nama, Loop_INDEX * 64 + Mula_jawatan, Memori_Fail.이름길이[Loop_INDEX] - Mula_jawatan, 시작점, pemasukan_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Mula_jawatan = Memori_Fail.pemasukan_Mula(Memori_Fail.direktori_nama, Loop_INDEX * 64, Memori_Fail.direktori_kepanjangan[Loop_INDEX]);
                if (Mula_jawatan >= 0) 후보넣기(Memori_Fail.direktori_nama, Loop_INDEX * 64 + Mula_jawatan, Memori_Fail.direktori_kepanjangan[Loop_INDEX] - Mula_jawatan, 시작점, pemasukan_COUNT, true);
            }
        }
        if (후보수 != 1) { Papan.직렬쓰기(7); return; }
        for (int Loop_INDEX = pemasukan_COUNT; Loop_INDEX < 후보길이 && Saiz < pentafsir_perintah.baris.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) pentafsir_perintah.baris[Saiz++] = '\\';
            pentafsir_perintah.baris[Saiz++] = 후보[Loop_INDEX];
        }
        kursor_VALUE = Saiz; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = Papan.밀리초();
        while (Papan.밀리초() - 시작점 < 80) { int bait_data = Papan.직렬읽기(); if (bait_data >= 0) return bait_data; Papan.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int pemasukan_COUNT = 0, tamat_jawatan = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bait_data = 탈출읽기(); if (bait_data < 0) return; if (bait_data >= '0' && bait_data <= '9') pemasukan_COUNT = pemasukan_COUNT * 10 + bait_data - '0'; else { tamat_jawatan = bait_data; break; } }
        if (tamat_jawatan == 'A') 기록이동(1);
        else if (tamat_jawatan == 'B') 기록이동(-1);
        else if (tamat_jawatan == 'C') { kursor_VALUE = BACK_VALUE(kursor_VALUE); 다시(); }
        else if (tamat_jawatan == 'D') { kursor_VALUE = hadapan_VALUE(kursor_VALUE); 다시(); }
        else if (tamat_jawatan == 'H' || tamat_jawatan == '~' && (pemasukan_COUNT == 1 || pemasukan_COUNT == 7)) { kursor_VALUE = 0; 다시(); }
        else if (tamat_jawatan == 'F' || tamat_jawatan == '~' && (pemasukan_COUNT == 4 || pemasukan_COUNT == 8)) { kursor_VALUE = Saiz; 다시(); }
        else if (tamat_jawatan == '~' && pemasukan_COUNT == 3 && kursor_VALUE < Saiz) {
            int Seterusnya_jawatan = BACK_VALUE(kursor_VALUE); for (int Loop_INDEX = Seterusnya_jawatan; Loop_INDEX < Saiz; Loop_INDEX++) pentafsir_perintah.baris[Loop_INDEX - Seterusnya_jawatan + kursor_VALUE] = pentafsir_perintah.baris[Loop_INDEX]; Saiz -= Seterusnya_jawatan - kursor_VALUE; 다시();
        }
        else if (tamat_jawatan == '~' && (pemasukan_COUNT == 5 || pemasukan_COUNT == 6)) Papan.Terminal(pemasukan_COUNT == 5 ? 5 : 6);
        else if (tamat_jawatan == '~' && pemasukan_COUNT == 24 && baris_perintah) { pentafsir_perintah.Terminal(true); }
    }
    static int Baca() {
        if (!tetingkap_sesi.이어읽기) { Saiz = kursor_VALUE = Cari_VALUE = Mula_tetingkap = 0; 가로보기 = false; }
        else { tetingkap_sesi.이어읽기 = false; 다시(); } boolean limpahan = false;
        while (true) {
            int bait_data = Papan.직렬읽기(); if (bait_data == -4096) return -3;
            if (Papan.Terminal(14) != 0) 다시(); if (bait_data < 0) { Papan.YIELD_CPU(); continue; }
            if (bait_data == 10 && pentafsir_perintah.앞줄) { pentafsir_perintah.앞줄 = false; continue; } pentafsir_perintah.앞줄 = bait_data == 13;
            if (bait_data == 27) { 탈출(); continue; }
            if (bait_data == 3) { 단말.Tulis("^C\n"); return -1; }
            if (bait_data == 4 && Saiz == 0 && baris_perintah) { if (Papan.Terminal(2) != 0) pentafsir_perintah.Terminal(true); return -1; }
            if (bait_data == 13 || bait_data == 10) { 단말.문자(10); if (!limpahan) Tambah_LOG(); return limpahan ? -2 : Saiz; }
            if (bait_data == 9 && baris_perintah) { Selesai_VALUE(); continue; }
            if (bait_data == 1 || bait_data == 5) { kursor_VALUE = bait_data == 1 ? 0 : Saiz; 다시(); continue; }
            if (bait_data == 8 || bait_data == 127 || bait_data == 21) {
                if (bait_data == 21) { for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Saiz; Loop_INDEX++) pentafsir_perintah.baris[Loop_INDEX - kursor_VALUE] = pentafsir_perintah.baris[Loop_INDEX]; Saiz -= kursor_VALUE; kursor_VALUE = 0; }
                else if (kursor_VALUE > 0) { int 변경전 = hadapan_VALUE(kursor_VALUE); for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Saiz; Loop_INDEX++) pentafsir_perintah.baris[Loop_INDEX - kursor_VALUE + 변경전] = pentafsir_perintah.baris[Loop_INDEX]; Saiz -= kursor_VALUE - 변경전; kursor_VALUE = 변경전; }
                다시(); continue;
            }
            if (bait_data == 11) { Saiz = kursor_VALUE; 다시(); continue; }
            if (bait_data < 32 && bait_data != 9) continue;
            if (Saiz == pentafsir_perintah.baris.length) { limpahan = true; continue; }
            for (int Loop_INDEX = Saiz; Loop_INDEX > kursor_VALUE; Loop_INDEX--) pentafsir_perintah.baris[Loop_INDEX] = pentafsir_perintah.baris[Loop_INDEX - 1];
            pentafsir_perintah.baris[kursor_VALUE++] = bait_data; Saiz++;
            if (kursor_VALUE == Saiz && !가로보기 && 폭(0, Saiz) <= 보이는폭()) Papan.직렬쓰기(bait_data);
            else if (kursor_VALUE == Saiz) 보이는줄(); else 다시();
        }
    }
}
