// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] file_tabel = new int[1024];
    static int 바이트해시(int VALUE, int data) { return (VALUE ^ data) * 16777619; }
    static void bersihkan_data() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Storage_Ponsel_koneksi.seksi_data[INDEX] = 0;
    }
    static int tabel_bilangan_bulat(int posisi) {
        return file_tabel[posisi] | file_tabel[posisi + 1] << 8 | file_tabel[posisi + 2] << 16 | file_tabel[posisi + 3] << 24;
    }
    static void tulis_tabel_bilangan_bulat(int posisi, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) file_tabel[posisi + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean cek_tabel() {
        for (int berkas = 0; berkas < 8; berkas++) {
            int panjang_VALUE = 0;
            for (int slot_entri = 0; slot_entri < 64; slot_entri++) Memori_sistem_berkas.Nama_2[slot_entri] = file_tabel[berkas * 72 + slot_entri];
            while (panjang_VALUE < 64 && Memori_sistem_berkas.Nama_2[panjang_VALUE] != 0) panjang_VALUE++;
            if (panjang_VALUE == 0) continue;
            if (!Memori_sistem_berkas.cek_nama(Memori_sistem_berkas.Nama_2, panjang_VALUE)
                || tabel_bilangan_bulat(berkas * 72 + 64) < 0 || tabel_bilangan_bulat(berkas * 72 + 64) > 16384) return false;
            for (int depan_VALUE = 0; depan_VALUE < berkas; depan_VALUE++) {
                boolean 같음 = file_tabel[depan_VALUE * 72 + panjang_VALUE] == 0;
                for (int slot_entri = 0; slot_entri < panjang_VALUE; slot_entri++) if (file_tabel[depan_VALUE * 72 + slot_entri] != Memori_sistem_berkas.Nama_2[slot_entri]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Mulai_seksi = 1 + 보존본 * 259;
        if (Storage_Ponsel_koneksi.Baca(Mulai_seksi) < 0 || Storage_Ponsel_koneksi.urai_bilangan_bulat(0) != 0x4a4b534e) return -1;
        int 세대 = Storage_Ponsel_koneksi.urai_bilangan_bulat(4), checksum = Storage_Ponsel_koneksi.urai_bilangan_bulat(8);
        if (세대 < 1 || Storage_Ponsel_koneksi.urai_bilangan_bulat(12) != (세대 ^ checksum ^ 0x4a4b534e)) return -1;
        int hash_file = 0x811c9dc5;
        for (int seksi_VALUE = 0; seksi_VALUE < 258; seksi_VALUE++) {
            if (Storage_Ponsel_koneksi.Baca(Mulai_seksi + 1 + seksi_VALUE) < 0) return -1;
            for (int slot_entri = 0; slot_entri < 512; slot_entri++) {
                int VALUE = Storage_Ponsel_koneksi.seksi_data[slot_entri];
                hash_file = 바이트해시(hash_file, VALUE);
                if (seksi_VALUE < 2) file_tabel[seksi_VALUE * 512 + slot_entri] = VALUE;
            }
        }
        return hash_file == checksum && cek_tabel() ? 세대 : -1;
    }
    static int muatSumber(int 보존본) {
        int Mulai_seksi = 1 + 보존본 * 259;
        for (int seksi_VALUE = 0; seksi_VALUE < 2; seksi_VALUE++) {
            if (Storage_Ponsel_koneksi.Baca(Mulai_seksi + 1 + seksi_VALUE) < 0) return -5;
            for (int slot_entri = 0; slot_entri < 512; slot_entri++) file_tabel[seksi_VALUE * 512 + slot_entri] = Storage_Ponsel_koneksi.seksi_data[slot_entri];
        }
        for (int berkas = 0; berkas < 8; berkas++) {
            for (int slot_entri = 0; slot_entri < 64; slot_entri++) Memori_sistem_berkas.이름들[berkas * 64 + slot_entri] = file_tabel[berkas * 72 + slot_entri];
            Memori_sistem_berkas.ukuran_Daftar[berkas] = file_tabel[berkas * 72] == 0 ? 0 : tabel_bilangan_bulat(berkas * 72 + 64);
            Memori_sistem_berkas.허가들[berkas] = tabel_bilangan_bulat(berkas * 72 + 68) & 511;
            for (int seksi_VALUE = 0; seksi_VALUE < 32; seksi_VALUE++) {
                if (Storage_Ponsel_koneksi.Baca(Mulai_seksi + 3 + berkas * 32 + seksi_VALUE) < 0) return -5;
                int surel = Ponsel_VALUE.file_Memori() + berkas * 16384 + seksi_VALUE * 512;
                for (int slot_entri = 0; slot_entri < 512; slot_entri++) Ponsel_VALUE.tulis_Memori(surel + slot_entri, Storage_Ponsel_koneksi.seksi_data[slot_entri]);
            }
        }
        return 0;
    }
    static void Siapkan() {
        if (Storage_Ponsel_koneksi.Baca(0) < 0 || Storage_Ponsel_koneksi.urai_bilangan_bulat(0) != 0x54534b4a
            || Storage_Ponsel_koneksi.urai_bilangan_bulat(4) != 0x3145524f || Storage_Ponsel_koneksi.urai_bilangan_bulat(8) != 2048
            || Storage_Ponsel_koneksi.urai_bilangan_bulat(12) != 0x3153464a) {
            SMS_Terminal.Tulis("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Storage_Ponsel_koneksi.teknologi_informasi_Aktif_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Tulis("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (muatSumber(현재보존본) < 0) {
            SMS_Terminal.Tulis("STORE read failed; halted to preserve files\n"); Ponsel_VALUE.정지();
        }
        SMS_Terminal.Tulis("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int sinkro() {
        if (!Storage_Ponsel_koneksi.teknologi_informasi_Aktif_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Berikutnya_item = 현재보존본 == 0 ? 1 : 0, Mulai_seksi = 1 + Berikutnya_item * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 Ponsel_VALUE 캐시를 비운다.
        bersihkan_data();
        if (Storage_Ponsel_koneksi.Tulis(Mulai_seksi) < 0 || Storage_Ponsel_koneksi.밀어쓰기() < 0) return -5;
        for (int slot_entri = 0; slot_entri < 1024; slot_entri++) file_tabel[slot_entri] = 0;
        for (int berkas = 0; berkas < 8; berkas++) if (Memori_sistem_berkas.이름들[berkas * 64] != 0) {
            for (int slot_entri = 0; slot_entri < 64; slot_entri++) file_tabel[berkas * 72 + slot_entri] = Memori_sistem_berkas.이름들[berkas * 64 + slot_entri];
            tulis_tabel_bilangan_bulat(berkas * 72 + 64, Memori_sistem_berkas.ukuran_Daftar[berkas]);
            tulis_tabel_bilangan_bulat(berkas * 72 + 68, Memori_sistem_berkas.허가들[berkas]);
        }
        int hash_file = 0x811c9dc5;
        for (int seksi_VALUE = 0; seksi_VALUE < 258; seksi_VALUE++) {
            for (int slot_entri = 0; slot_entri < 512; slot_entri++) {
                int VALUE = 0;
                if (seksi_VALUE < 2) VALUE = file_tabel[seksi_VALUE * 512 + slot_entri];
                else {
                    int berkas = (seksi_VALUE - 2) / 32, posisi = (seksi_VALUE - 2) % 32 * 512 + slot_entri;
                    if (file_tabel[berkas * 72] != 0 && posisi < Memori_sistem_berkas.ukuran_Daftar[berkas])
                        VALUE = Ponsel_VALUE.기억읽기(Ponsel_VALUE.file_Memori() + berkas * 16384 + posisi);
                }
                Storage_Ponsel_koneksi.seksi_data[slot_entri] = VALUE; hash_file = 바이트해시(hash_file, VALUE);
            }
            if (Storage_Ponsel_koneksi.Tulis(Mulai_seksi + 1 + seksi_VALUE) < 0) return -5;
        }
        if (Storage_Ponsel_koneksi.밀어쓰기() < 0) return -5;
        bersihkan_data(); Storage_Ponsel_koneksi.tulis_bilangan_bulat_VALUE(0, 0x4a4b534e);
        Storage_Ponsel_koneksi.tulis_bilangan_bulat_VALUE(4, 세대번호 + 1); Storage_Ponsel_koneksi.tulis_bilangan_bulat_VALUE(8, hash_file);
        Storage_Ponsel_koneksi.tulis_bilangan_bulat_VALUE(12, (세대번호 + 1) ^ hash_file ^ 0x4a4b534e);
        if (Storage_Ponsel_koneksi.Tulis(Mulai_seksi) < 0 || Storage_Ponsel_koneksi.밀어쓰기() < 0) return -5;
        현재보존본 = Berikutnya_item; 세대번호++;
        return 0;
    }
}
