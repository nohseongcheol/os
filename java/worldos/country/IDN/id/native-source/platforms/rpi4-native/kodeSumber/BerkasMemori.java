// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM berkas 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 galat 번호다.
 */
public final class BerkasMemori {
    static final int file_COUNT = 64;
    static int[] Nama_2 = new int[file_COUNT * 64];
    static int[] 이름길이 = new int[file_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Isi_VALUE = new int[file_COUNT * 4096];
    static int[] panjang_VALUE = new int[file_COUNT];
    static int[] Referensi_COUNT = new int[file_COUNT];
    static int[] gunakan_VALUE = new int[16];
    static int[] target = new int[16];
    static int[] posisi = new int[16];
    static int[] metode_MODE = new int[16];
    static int[] jalur = new int[64];
    static int jalur_panjang;

    public static int 파일한도() { return file_COUNT; }
    static int 자료읽기(int berkas, int posisi_INDEX) { return (Isi_VALUE[berkas * 4096 + posisi_INDEX / 4] >>> ((posisi_INDEX & 3) * 8)) & 255; }
    static void tulis_data(int berkas, int posisi_INDEX, int VALUE) {
        int slot_entri = berkas * 4096 + posisi_INDEX / 4, gerak_VALUE = (posisi_INDEX & 3) * 8;
        Isi_VALUE[slot_entri] = (Isi_VALUE[slot_entri] & ~(255 << gerak_VALUE)) | ((VALUE & 255) << gerak_VALUE);
    }

    public static int jalur_Mulai(int Ukuran) {
        jalur_panjang = 0;
        if (Ukuran < 1 || Ukuran > 63) return -36;
        jalur_panjang = Ukuran;
        for (int Loop_INDEX = 0; Loop_INDEX < Ukuran; Loop_INDEX++) jalur[Loop_INDEX] = 0;
        return 0;
    }
    public static int jalur_byte(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= jalur_panjang || VALUE < 1 || VALUE > 255) return -22;
        jalur[INDEX] = VALUE; return 0;
    }
    static int FIND_entri() {
        for (int file_INDEX = 0; file_INDEX < file_COUNT; file_INDEX++) if (이름길이[file_INDEX] > 0 && 이름길이[file_INDEX] == 정규길이 && 접두(Nama_2, file_INDEX * 64, 이름길이[file_INDEX], 정규, 정규길이)) return file_INDEX;
        return -1;
    }
    public static int Buka(int 플래그) {
        if (jalur_panjang == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < jalur_panjang; Loop_INDEX++) if (jalur[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int hasil = normalkan_VALUE(); if (hasil < 0) return hasil;
        if (FIND_Direktori(정규길이) >= 0) return -21;
        hasil = cek_induk(); if (hasil < 0) return hasil;
        int berkas = FIND_entri();
        if (berkas >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (berkas < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (gunakan_VALUE[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (berkas < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < file_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Referensi_COUNT[Loop_INDEX] == 0) { berkas = Loop_INDEX; break; }
            if (berkas < 0) return -28;
            이름길이[berkas] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nama_2[berkas * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            panjang_VALUE[berkas] = 0;
        }
        if ((플래그 & 0x200) != 0) panjang_VALUE[berkas] = 0;
        gunakan_VALUE[서술자] = 1; target[서술자] = berkas; posisi[서술자] = 0; metode_MODE[서술자] = 플래그;
        Referensi_COUNT[berkas]++;
        return 서술자 + 3;
    }
    static int periksa(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && gunakan_VALUE[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Baca(int 서술자) {
        int slot_entri = periksa(서술자);
        if (slot_entri < 0 || (metode_MODE[slot_entri] & 3) == 1) return -9;
        int berkas = target[slot_entri];
        if (posisi[slot_entri] >= panjang_VALUE[berkas]) return 256; // EOF와 aktual_data 0x00..0xff 구별
        return 자료읽기(berkas, posisi[slot_entri]++);
    }
    public static int Tulis(int 서술자, int VALUE) {
        int slot_entri = periksa(서술자);
        if (slot_entri < 0 || (metode_MODE[slot_entri] & 3) == 0) return -9;
        int berkas = target[slot_entri];
        if ((metode_MODE[slot_entri] & 0x400) != 0) posisi[slot_entri] = panjang_VALUE[berkas];
        if (posisi[slot_entri] >= 16384) return -28;
        while (panjang_VALUE[berkas] < posisi[slot_entri]) tulis_data(berkas, panjang_VALUE[berkas]++, 0);
        tulis_data(berkas, posisi[slot_entri]++, VALUE);
        if (panjang_VALUE[berkas] < posisi[slot_entri]) panjang_VALUE[berkas] = posisi[slot_entri];
        return 1;
    }
    public static int cari_posisi(int 서술자, int 거리, int Tugas_akar) {
        int slot_entri = periksa(서술자);
        if (slot_entri < 0) return -9;
        if (Tugas_akar < 0 || Tugas_akar > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Tugas_akar == 0 ? 0 : Tugas_akar == 1 ? posisi[slot_entri] : panjang_VALUE[target[slot_entri]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        posisi[slot_entri] = 새위치; return 새위치;
    }
    public static int Tutup(int 서술자) {
        int slot_entri = periksa(서술자);
        if (slot_entri < 0) return -9;
        Referensi_COUNT[target[slot_entri]]--; gunakan_VALUE[slot_entri] = 0; return 0;
    }
    public static int Ukuran(int 서술자) {
        int slot_entri = periksa(서술자); return slot_entri < 0 ? -9 : panjang_VALUE[target[slot_entri]];
    }
    public static int set_panjang(int 서술자, int Ukuran) {
        int slot_entri = periksa(서술자);
        if (slot_entri < 0 || (metode_MODE[slot_entri] & 3) == 0) return -9;
        if (Ukuran < 0 || Ukuran > 16384) return -22;
        int berkas = target[slot_entri];
        while (panjang_VALUE[berkas] < Ukuran) tulis_data(berkas, panjang_VALUE[berkas]++, 0);
        panjang_VALUE[berkas] = Ukuran; return 0;
    }
    public static int hapus_entri_c8dbc399() {
        if (jalur_panjang == 0) return -22;
        int hasil = normalkan_VALUE(); if (hasil < 0) return hasil;
        if (FIND_Direktori(정규길이) >= 0) return -21;
        hasil = cek_induk(); if (hasil < 0) return hasil;
        int berkas = FIND_entri();
        if (berkas < 0) return -2;
        이름길이[berkas] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void entri_Daftar() {
        jalur_Mulai(1); jalur_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= file_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Nama_2[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int posisi_INDEX) {
        return INDEX >= 0 && INDEX < file_COUNT && posisi_INDEX >= 0 && posisi_INDEX < 이름길이[INDEX] ? Nama_2[INDEX * 64 + posisi_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < file_COUNT ? panjang_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], saat_ini_item = new int[64], Direktori_nama = new int[16 * 64], Direktori_panjang = new int[16];
    static int 정규길이, saat_ini_panjang;
    static boolean 접두(int[] 이름들, int jalankan, int jalur_VALUE, int[] depan_VALUE, int spasi_baris_jalur) {
        if (jalur_VALUE < spasi_baris_jalur) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < spasi_baris_jalur; Loop_INDEX++) if (이름들[jalankan + Loop_INDEX] != depan_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normalkan_VALUE() {
        if (jalur_panjang == 0) return -22;
        정규길이 = jalur[0] == '/' ? 0 : saat_ini_panjang;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = saat_ini_item[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < jalur_panjang) {
            while (읽는자리 < jalur_panjang && jalur[읽는자리] == '/') 읽는자리++;
            int Mulai_posisi = 읽는자리; while (읽는자리 < jalur_panjang && jalur[읽는자리] != '/') { if (jalur[읽는자리] == 0) return -22; 읽는자리++; }
            int entri_COUNT = 읽는자리 - Mulai_posisi; if (entri_COUNT == 0 || entri_COUNT == 1 && jalur[Mulai_posisi] == '.') continue;
            if (entri_COUNT == 2 && jalur[Mulai_posisi] == '.' && jalur[Mulai_posisi + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + entri_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Mulai_posisi; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = jalur[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Direktori(int entri_COUNT) {
        if (entri_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Direktori_panjang[Loop_INDEX] == entri_COUNT && 접두(Direktori_nama, Loop_INDEX * 64, entri_COUNT, 정규, entri_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int cek_induk() {
        int entri_COUNT = 정규길이; while (entri_COUNT > 0 && 정규[entri_COUNT - 1] != '/') entri_COUNT--;
        return FIND_Direktori(entri_COUNT == 0 ? 0 : entri_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Buat_Direktori() {
        int 처리값 = normalkan_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktori(정규길이) >= 0 || FIND_entri() >= 0) return -17;
        처리값 = cek_induk(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Direktori_panjang[Loop_INDEX] == 0) {
            Direktori_panjang[Loop_INDEX] = 정규길이; for (int dalam_posisi = 0; dalam_posisi < 정규길이; dalam_posisi++) Direktori_nama[Loop_INDEX * 64 + dalam_posisi] = 정규[dalam_posisi]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalkan_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktori(정규길이) >= 0) return 2;
        return FIND_entri() >= 0 ? 1 : 0;
    }
    public static int ubah_Direktori() {
        int 처리값 = normalkan_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktori(정규길이) < 0) return -2;
        saat_ini_panjang = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < saat_ini_panjang; Loop_INDEX++) saat_ini_item[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int hapus_Direktori() {
        int 처리값 = normalkan_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_Direktori(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (saat_ini_panjang == 정규길이 && 접두(saat_ini_item, 0, saat_ini_panjang, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < file_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Nama_2, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Nama_2[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (Direktori_panjang[Loop_INDEX] > 정규길이 && 접두(Direktori_nama, Loop_INDEX * 64, Direktori_panjang[Loop_INDEX], 정규, 정규길이) && Direktori_nama[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        Direktori_panjang[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= file_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalkan_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Direktori(정규길이) >= 0) return -21;
        처리값 = cek_induk(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_entri(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nama_2[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int entri_Mulai(int[] data_ARRAY, int 시작점, int entri_COUNT) {
        if (!접두(data_ARRAY, 시작점, entri_COUNT, 정규, 정규길이)) return -1;
        int Mulai_posisi = 정규길이;
        if (Mulai_posisi > 0) { if (entri_COUNT <= Mulai_posisi || data_ARRAY[시작점 + Mulai_posisi] != '/') return -1; Mulai_posisi++; }
        if (entri_COUNT <= Mulai_posisi) return -1;
        for (int Loop_INDEX = Mulai_posisi; Loop_INDEX < entri_COUNT; Loop_INDEX++) if (data_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Mulai_posisi;
    }
    static void saat_ini_tulis() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < saat_ini_panjang; Loop_INDEX++) Papan.직렬쓰기(saat_ini_item[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalkan_VALUE(); if (처리값 < 0) return 처리값;
        int file_target = FIND_entri();
        if (file_target >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Papan.직렬쓰기(정규[Loop_INDEX]); 단말.Tulis("  "); 단말.수(panjang_VALUE[file_target]); 단말.Tulis("byte_VALUE(주기억 berkas)\n"); return 0; }
        if (FIND_Direktori(정규길이) < 0) return -2;
        for (int berikutnya_VALUE = 1; berikutnya_VALUE < 16; berikutnya_VALUE++) if (Direktori_panjang[berikutnya_VALUE] > 0) {
            int Mulai_posisi = entri_Mulai(Direktori_nama, berikutnya_VALUE * 64, Direktori_panjang[berikutnya_VALUE]); if (Mulai_posisi < 0) continue;
            for (int Loop_INDEX = Mulai_posisi; Loop_INDEX < Direktori_panjang[berikutnya_VALUE]; Loop_INDEX++) Papan.직렬쓰기(Direktori_nama[berikutnya_VALUE * 64 + Loop_INDEX]); 단말.Tulis("/\n");
        }
        for (int file_INDEX = 0; file_INDEX < file_COUNT; file_INDEX++) if (이름길이[file_INDEX] > 0) {
            int Mulai_posisi = entri_Mulai(Nama_2, file_INDEX * 64, 이름길이[file_INDEX]); if (Mulai_posisi < 0) continue;
            for (int Loop_INDEX = Mulai_posisi; Loop_INDEX < 이름길이[file_INDEX]; Loop_INDEX++) Papan.직렬쓰기(Nama_2[file_INDEX * 64 + Loop_INDEX]);
            단말.Tulis("  "); 단말.수(panjang_VALUE[file_INDEX]); 단말.Tulis("byte_VALUE(주기억 berkas)\n");
        }
        return 0;
    }
}
