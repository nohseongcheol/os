// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VALUE 경계를 지키는 삽입/삭제, 방향키, perintah LOG_baris, Tab Selesai_VALUE. */
public final class editor_baris {
    static boolean baris_perintah;
    static int[] LOG_baris = new int[16 * 1024], LOG_panjang = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_baris_mengakhiri, Cari_VALUE, 저장길이, Ukuran, kursor_VALUE, 후보수, 후보길이, Mulai_jendela;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd aman_shell jarak_jauh_tampilan run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String entri_Daftar, int Mulai_posisi, int mengakhiri_posisi, int 입력길이) {
        int byte_COUNT=0;
        for(int posisi_INDEX=Mulai_posisi;posisi_INDEX<mengakhiri_posisi;posisi_INDEX++) {
            int kode_karakter=entri_Daftar.charAt(posisi_INDEX);
            if(kode_karakter>=0xd800 && kode_karakter<=0xdbff && posisi_INDEX+1<mengakhiri_posisi)kode_karakter=0x10000+((kode_karakter-0xd800)<<10)+entri_Daftar.charAt(++posisi_INDEX)-0xdc00;
            int 수=kode_karakter<128?1:kode_karakter<2048?2:kode_karakter<65536?3:4;
            if(byte_COUNT+수>62)return;
            for(int urutan_VALUE_e9fa7815=수-1;urutan_VALUE_e9fa7815>=0;urutan_VALUE_e9fa7815--)명령후보[byte_COUNT++]=수==1?kode_karakter:urutan_VALUE_e9fa7815==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(kode_karakter>>(6*urutan_VALUE_e9fa7815)):0x80|((kode_karakter>>(6*urutan_VALUE_e9fa7815))&63);
        }
        if(byte_COUNT<입력길이)return;
        for(int posisi_INDEX=0;posisi_INDEX<입력길이;posisi_INDEX++)if(명령후보[posisi_INDEX]!=PenafsirPerintah.baris_masukan[posisi_INDEX])return;
        후보수++;후보길이=byte_COUNT+1;
        for(int posisi_INDEX=0;posisi_INDEX<byte_COUNT;posisi_INDEX++)후보[posisi_INDEX]=명령후보[posisi_INDEX];후보[byte_COUNT]=' ';
    }
    static int depan_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (PenafsirPerintah.baris_masukan[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_VALUE(int 읽는자리) { if (읽는자리 < Ukuran) { 읽는자리++; while (읽는자리 < Ukuran && (PenafsirPerintah.baris_masukan[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Mulai_posisi, int tujuan_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Mulai_posisi; Loop_INDEX < tujuan_VALUE_INDEX; Loop_INDEX++) { int byte_data = PenafsirPerintah.baris_masukan[Loop_INDEX]; if ((byte_data & 192) == 128) continue; 글칸수 += byte_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void coba_lagi_VALUE() {
        단말.Tulis("\r\u001b[2K");
        단말.Tulis(baris_perintah ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 baris_masukan 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Papan.terminal(13) & 65535; return COLUMNS - (baris_perintah ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_VALUE < Mulai_jendela) Mulai_jendela = kursor_VALUE;
        while (폭(Mulai_jendela, kursor_VALUE) > 보이는폭()) Mulai_jendela = BACK_VALUE(Mulai_jendela);
        int mengakhiri_posisi = Mulai_jendela;
        while (mengakhiri_posisi < Ukuran && 폭(Mulai_jendela, BACK_VALUE(mengakhiri_posisi)) <= 보이는폭()) mengakhiri_posisi = BACK_VALUE(mengakhiri_posisi);
        단말.Tulis("\r\u001b["); 단말.수(baris_perintah ? 16 : 7); 단말.Tulis("G\u001b[K");
        if (Mulai_jendela > 0) 단말.문자('<');
        for (int Loop_INDEX = Mulai_jendela; Loop_INDEX < mengakhiri_posisi; Loop_INDEX++) Papan.직렬쓰기(PenafsirPerintah.baris_masukan[Loop_INDEX]);
        단말.문자(mengakhiri_posisi < Ukuran ? '>' : ' ');
        단말.Tulis("\u001b["); 단말.수(폭(kursor_VALUE, mengakhiri_posisi) + 1); 단말.문자('D');
        가로보기 = Mulai_jendela > 0 || mengakhiri_posisi < Ukuran || 폭(0, Ukuran) > 보이는폭();
    }
    static void tambah_LOG() {
        if (!baris_perintah || Ukuran == 0 || Ukuran > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_baris_mengakhiri + 15) % 16; boolean 같은여부 = LOG_panjang[마지막자리] == Ukuran;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Ukuran; Loop_INDEX++) if (LOG_baris[마지막자리 * 1024 + Loop_INDEX] != PenafsirPerintah.baris_masukan[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_panjang[LOG_baris_mengakhiri] = Ukuran; for (int Loop_INDEX = 0; Loop_INDEX < Ukuran; Loop_INDEX++) LOG_baris[LOG_baris_mengakhiri * 1024 + Loop_INDEX] = PenafsirPerintah.baris_masukan[Loop_INDEX];
        LOG_baris_mengakhiri = (LOG_baris_mengakhiri + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!baris_perintah) return;
        if (Cari_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Ukuran; for (int Loop_INDEX = 0; Loop_INDEX < Ukuran; Loop_INDEX++) Store_VALUE[Loop_INDEX] = PenafsirPerintah.baris_masukan[Loop_INDEX]; }
        int Berikutnya_posisi = Cari_VALUE + DELTA_VALUE; if (Berikutnya_posisi < 0 || Berikutnya_posisi > LOG_COUNT) return; Cari_VALUE = Berikutnya_posisi;
        if (Cari_VALUE == 0) { Ukuran = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Ukuran; Loop_INDEX++) PenafsirPerintah.baris_masukan[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_baris_mengakhiri + 16 - Cari_VALUE) % 16; Ukuran = LOG_panjang[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Ukuran; Loop_INDEX++) PenafsirPerintah.baris_masukan[Loop_INDEX] = LOG_baris[보관칸 * 1024 + Loop_INDEX]; }
        kursor_VALUE = Ukuran; coba_lagi_VALUE();
    }
    static void show_LOG() {
        for (int entri_COUNT = 0; entri_COUNT < LOG_COUNT; entri_COUNT++) {
            int 보관칸 = (LOG_baris_mengakhiri + 16 - LOG_COUNT + entri_COUNT) % 16; 단말.수(entri_COUNT + 1); 단말.Tulis("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_panjang[보관칸]; Loop_INDEX++) Papan.직렬쓰기(LOG_baris[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_ARRAY, int Mulai_posisi, int entri_COUNT, int 접두말, int total_COUNT, boolean 폴더번호) {
        if (entri_COUNT < total_COUNT || entri_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < total_COUNT; Loop_INDEX++) if (data_ARRAY[Mulai_posisi + Loop_INDEX] != PenafsirPerintah.baris_masukan[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = entri_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = data_ARRAY[Mulai_posisi + Loop_INDEX]; 후보[entri_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void Selesai_VALUE() {
        if (!baris_perintah || kursor_VALUE != Ukuran) return;
        int 시작점 = Ukuran; while (시작점 > 0 && PenafsirPerintah.baris_masukan[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Ukuran; Loop_INDEX++) if (PenafsirPerintah.baris_masukan[Loop_INDEX] == '/' || PenafsirPerintah.baris_masukan[Loop_INDEX] == '"' || PenafsirPerintah.baris_masukan[Loop_INDEX] == 39 || PenafsirPerintah.baris_masukan[Loop_INDEX] == '\\') return;
        후보수 = 0; int entri_COUNT = Ukuran - 시작점;
        if (시작점 == 0) {
            for(int indeks_daftar=0;indeks_daftar<2;indeks_daftar++) {
                String entri_Daftar=indeks_daftar==0?명령들:관리명령.Selesai_Kata();
                int 읽는자리=0;
                while(읽는자리<entri_Daftar.length()) {
                    int mengakhiri_posisi=읽는자리;while(mengakhiri_posisi<entri_Daftar.length() && entri_Daftar.charAt(mengakhiri_posisi)!=' ')mengakhiri_posisi++;
                    명령후보넣기(entri_Daftar,읽는자리,mengakhiri_posisi,entri_COUNT);읽는자리=mengakhiri_posisi+1;
                }
            }
        } else {
            BerkasMemori.jalur_Mulai(1); BerkasMemori.jalur_byte(0, '.'); BerkasMemori.normalkan_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < BerkasMemori.file_COUNT; Loop_INDEX++) {
                int Mulai_posisi = BerkasMemori.entri_Mulai(BerkasMemori.Nama_2, Loop_INDEX * 64, BerkasMemori.이름길이[Loop_INDEX]);
                if (Mulai_posisi >= 0) 후보넣기(BerkasMemori.Nama_2, Loop_INDEX * 64 + Mulai_posisi, BerkasMemori.이름길이[Loop_INDEX] - Mulai_posisi, 시작점, entri_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Mulai_posisi = BerkasMemori.entri_Mulai(BerkasMemori.Direktori_nama, Loop_INDEX * 64, BerkasMemori.Direktori_panjang[Loop_INDEX]);
                if (Mulai_posisi >= 0) 후보넣기(BerkasMemori.Direktori_nama, Loop_INDEX * 64 + Mulai_posisi, BerkasMemori.Direktori_panjang[Loop_INDEX] - Mulai_posisi, 시작점, entri_COUNT, true);
            }
        }
        if (후보수 != 1) { Papan.직렬쓰기(7); return; }
        for (int Loop_INDEX = entri_COUNT; Loop_INDEX < 후보길이 && Ukuran < PenafsirPerintah.baris_masukan.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) PenafsirPerintah.baris_masukan[Ukuran++] = '\\';
            PenafsirPerintah.baris_masukan[Ukuran++] = 후보[Loop_INDEX];
        }
        kursor_VALUE = Ukuran; coba_lagi_VALUE();
    }
    static int 탈출읽기() {
        int 시작점 = Papan.밀리초();
        while (Papan.밀리초() - 시작점 < 80) { int byte_data = Papan.직렬읽기(); if (byte_data >= 0) return byte_data; Papan.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int entri_COUNT = 0, mengakhiri_posisi = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int byte_data = 탈출읽기(); if (byte_data < 0) return; if (byte_data >= '0' && byte_data <= '9') entri_COUNT = entri_COUNT * 10 + byte_data - '0'; else { mengakhiri_posisi = byte_data; break; } }
        if (mengakhiri_posisi == 'A') 기록이동(1);
        else if (mengakhiri_posisi == 'B') 기록이동(-1);
        else if (mengakhiri_posisi == 'C') { kursor_VALUE = BACK_VALUE(kursor_VALUE); coba_lagi_VALUE(); }
        else if (mengakhiri_posisi == 'D') { kursor_VALUE = depan_VALUE(kursor_VALUE); coba_lagi_VALUE(); }
        else if (mengakhiri_posisi == 'H' || mengakhiri_posisi == '~' && (entri_COUNT == 1 || entri_COUNT == 7)) { kursor_VALUE = 0; coba_lagi_VALUE(); }
        else if (mengakhiri_posisi == 'F' || mengakhiri_posisi == '~' && (entri_COUNT == 4 || entri_COUNT == 8)) { kursor_VALUE = Ukuran; coba_lagi_VALUE(); }
        else if (mengakhiri_posisi == '~' && entri_COUNT == 3 && kursor_VALUE < Ukuran) {
            int Berikutnya_posisi = BACK_VALUE(kursor_VALUE); for (int Loop_INDEX = Berikutnya_posisi; Loop_INDEX < Ukuran; Loop_INDEX++) PenafsirPerintah.baris_masukan[Loop_INDEX - Berikutnya_posisi + kursor_VALUE] = PenafsirPerintah.baris_masukan[Loop_INDEX]; Ukuran -= Berikutnya_posisi - kursor_VALUE; coba_lagi_VALUE();
        }
        else if (mengakhiri_posisi == '~' && (entri_COUNT == 5 || entri_COUNT == 6)) Papan.terminal(entri_COUNT == 5 ? 5 : 6);
        else if (mengakhiri_posisi == '~' && entri_COUNT == 24 && baris_perintah) { PenafsirPerintah.terminal(true); }
    }
    static int Baca() {
        if (!jendela_sesi.이어읽기) { Ukuran = kursor_VALUE = Cari_VALUE = Mulai_jendela = 0; 가로보기 = false; }
        else { jendela_sesi.이어읽기 = false; coba_lagi_VALUE(); } boolean luapan = false;
        while (true) {
            int byte_data = Papan.직렬읽기(); if (byte_data == -4096) return -3;
            if (Papan.terminal(14) != 0) coba_lagi_VALUE(); if (byte_data < 0) { Papan.YIELD_CPU(); continue; }
            if (byte_data == 10 && PenafsirPerintah.앞줄) { PenafsirPerintah.앞줄 = false; continue; } PenafsirPerintah.앞줄 = byte_data == 13;
            if (byte_data == 27) { 탈출(); continue; }
            if (byte_data == 3) { 단말.Tulis("^C\n"); return -1; }
            if (byte_data == 4 && Ukuran == 0 && baris_perintah) { if (Papan.terminal(2) != 0) PenafsirPerintah.terminal(true); return -1; }
            if (byte_data == 13 || byte_data == 10) { 단말.문자(10); if (!luapan) tambah_LOG(); return luapan ? -2 : Ukuran; }
            if (byte_data == 9 && baris_perintah) { Selesai_VALUE(); continue; }
            if (byte_data == 1 || byte_data == 5) { kursor_VALUE = byte_data == 1 ? 0 : Ukuran; coba_lagi_VALUE(); continue; }
            if (byte_data == 8 || byte_data == 127 || byte_data == 21) {
                if (byte_data == 21) { for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Ukuran; Loop_INDEX++) PenafsirPerintah.baris_masukan[Loop_INDEX - kursor_VALUE] = PenafsirPerintah.baris_masukan[Loop_INDEX]; Ukuran -= kursor_VALUE; kursor_VALUE = 0; }
                else if (kursor_VALUE > 0) { int 변경전 = depan_VALUE(kursor_VALUE); for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Ukuran; Loop_INDEX++) PenafsirPerintah.baris_masukan[Loop_INDEX - kursor_VALUE + 변경전] = PenafsirPerintah.baris_masukan[Loop_INDEX]; Ukuran -= kursor_VALUE - 변경전; kursor_VALUE = 변경전; }
                coba_lagi_VALUE(); continue;
            }
            if (byte_data == 11) { Ukuran = kursor_VALUE; coba_lagi_VALUE(); continue; }
            if (byte_data < 32 && byte_data != 9) continue;
            if (Ukuran == PenafsirPerintah.baris_masukan.length) { luapan = true; continue; }
            for (int Loop_INDEX = Ukuran; Loop_INDEX > kursor_VALUE; Loop_INDEX--) PenafsirPerintah.baris_masukan[Loop_INDEX] = PenafsirPerintah.baris_masukan[Loop_INDEX - 1];
            PenafsirPerintah.baris_masukan[kursor_VALUE++] = byte_data; Ukuran++;
            if (kursor_VALUE == Ukuran && !가로보기 && 폭(0, Ukuran) <= 보이는폭()) Papan.직렬쓰기(byte_data);
            else if (kursor_VALUE == Ukuran) 보이는줄(); else coba_lagi_VALUE();
        }
    }
}
