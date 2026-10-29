// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 ruang_pengguna 과정의 파일서술자와 열린 berkas 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int baca_tulis_bendera = 2, Buat_entri = 64, 독점생성 = 128, bersihkan_Isi = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] buat_handel = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], target = new int[서술자한도];
    static int[] file_posisi = new int[서술자한도], buat_Pengaturan = new int[서술자한도], Referensi_COUNT = new int[서술자한도];
    static int[] jaringan_handel = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] jalur_nama = new int[64], Transfer_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return buat_handel[파일서술자] - 1;
    }
    static int 빈서술자(int jalankan) {
        for (int INDEX = jalankan; INDEX < 서술자한도; INDEX++) if (buat_handel[INDEX] == 0) return INDEX;
        return -24;
    }
    static int kosong_handel() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Referensi_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Sambung(int 서술자, int 기술, int 파일종류, int file_target, int Konfigurasi) {
        buat_handel[서술자] = 기술 + 1; 서술자설정[서술자] = (Konfigurasi & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; target[기술] = file_target; Referensi_COUNT[기술] = 1;
        buat_Pengaturan[기술] = Konfigurasi & (3 | 이어쓰기 | 기다리지않기); file_posisi[기술] = 0;
        jaringan_handel[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Mulai_Proses() {
        CLEAN_Proses();
        for (int INDEX = 0; INDEX < 3; INDEX++) Sambung(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proses() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (buat_handel[INDEX] != 0) Tutup_file(INDEX);
    }
    static int Tutup_file(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        buat_handel[서술자] = 0; 서술자설정[서술자] = 0;
        Referensi_COUNT[기술]--;
        if (Referensi_COUNT[기술] == 0) {
            if (종류[기술] == 2) Memori_sistem_berkas.buat_COUNT[target[기술]]--;
            if (종류[기술] == 3 && jaringan_handel[기술] != 0) jaringan_tumpuk.Tutup(jaringan_handel[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int surel) {
        if (!실행관리.klip(surel, 1)) return -14;
        int posisi = Ponsel_VALUE.기억읽기(surel) == '/' ? 1 : 0;
        for (int panjang_VALUE = 0; panjang_VALUE < 64; panjang_VALUE++) {
            if (!실행관리.klip(surel + posisi + panjang_VALUE, 1)) return -14;
            int VALUE = Ponsel_VALUE.기억읽기(surel + posisi + panjang_VALUE);
            jalur_nama[panjang_VALUE] = VALUE;
            if (VALUE == 0) return panjang_VALUE == 0 ? -2 : (Memori_sistem_berkas.cek_nama(jalur_nama, panjang_VALUE) ? panjang_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int buat_file(int nama_surel, int Konfigurasi, int 허가) {
        int panjang_VALUE = 경로읽기(nama_surel);
        if (panjang_VALUE < 0) return panjang_VALUE;
        if ((Konfigurasi & ~(3 | Buat_entri | 독점생성 | bersihkan_Isi | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Konfigurasi & 3) == 3 || ((Konfigurasi & bersihkan_Isi) != 0 && (Konfigurasi & 3) == 0)) return -22;
        int berkas = Memori_sistem_berkas.FIND_entri(jalur_nama, panjang_VALUE);
        if (berkas >= 0 && (Konfigurasi & (Buat_entri | 독점생성)) == (Buat_entri | 독점생성)) return -17;
        if (berkas == -2 && (Konfigurasi & Buat_entri) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = kosong_handel();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (berkas == -2) {
            int hasil = Memori_sistem_berkas.Store_VALUE(jalur_nama, panjang_VALUE, jalur_nama, 0);
            if (hasil < 0) return hasil;
            berkas = Memori_sistem_berkas.FIND_entri(jalur_nama, panjang_VALUE);
            Memori_sistem_berkas.허가들[berkas] = 허가 & 511;
        }
        if (berkas < 0) return berkas;
        if ((Konfigurasi & bersihkan_Isi) != 0) Memori_sistem_berkas.ukuran_Daftar[berkas] = 0;
        Memori_sistem_berkas.buat_COUNT[berkas]++;
        return Sambung(서술자, 기술, 2, berkas, Konfigurasi);
    }
    static int 파일읽기(int 서술자, int data_surel, int panjang_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (buat_Pengaturan[기술] & 3) == 1) return -9;
        if (panjang_VALUE < 0) return -22;
        if (panjang_VALUE == 0) return 0;
        if (!실행관리.klip(data_surel, panjang_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, data_surel, panjang_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < panjang_VALUE) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = keyboard.Baca();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((buat_Pengaturan[기술] & 기다리지않기) != 0) return -11;
                    if (Ponsel_VALUE.사용자남은밀리초() <= 10) return -11;
                    jaringan_tumpuk.periksa(); Ponsel_VALUE.잠시양보();
                } else {
                    Ponsel_VALUE.tulis_Memori(data_surel + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int berkas = target[기술], posisi = file_posisi[기술];
        if (posisi >= Memori_sistem_berkas.ukuran_Daftar[berkas]) return 0;
        if (panjang_VALUE > Memori_sistem_berkas.ukuran_Daftar[berkas] - posisi) panjang_VALUE = Memori_sistem_berkas.ukuran_Daftar[berkas] - posisi;
        int 원본주소 = Ponsel_VALUE.file_Memori() + berkas * Memori_sistem_berkas.최대크기 + posisi;
        for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) Ponsel_VALUE.tulis_Memori(data_surel + INDEX, Ponsel_VALUE.기억읽기(원본주소 + INDEX));
        file_posisi[기술] += panjang_VALUE;
        return panjang_VALUE;
    }
    static int tulis_file(int 서술자, int data_surel, int panjang_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (buat_Pengaturan[기술] & 3) == 0) return -9;
        if (panjang_VALUE < 0) return -22;
        if (panjang_VALUE == 0) return 0;
        if (!실행관리.klip(data_surel, panjang_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 tujuan_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (panjang_VALUE > 16384) panjang_VALUE = 16384;
            for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) {
                int VALUE = Ponsel_VALUE.기억읽기(data_surel + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return panjang_VALUE;
        }
        int berkas = target[기술], Ukuran = Memori_sistem_berkas.ukuran_Daftar[berkas];
        int posisi = (buat_Pengaturan[기술] & 이어쓰기) != 0 ? Ukuran : file_posisi[기술];
        if (posisi >= Memori_sistem_berkas.최대크기) return -27;
        if (panjang_VALUE > Memori_sistem_berkas.최대크기 - posisi) panjang_VALUE = Memori_sistem_berkas.최대크기 - posisi;
        int tujuan_surel = Ponsel_VALUE.file_Memori() + berkas * Memori_sistem_berkas.최대크기;
        for (int INDEX = Ukuran; INDEX < posisi; INDEX++) Ponsel_VALUE.tulis_Memori(tujuan_surel + INDEX, 0);
        for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) Ponsel_VALUE.tulis_Memori(tujuan_surel + posisi + INDEX, Ponsel_VALUE.기억읽기(data_surel + INDEX));
        file_posisi[기술] = posisi + panjang_VALUE;
        if (posisi + panjang_VALUE > Ukuran) Memori_sistem_berkas.ukuran_Daftar[berkas] = posisi + panjang_VALUE;
        return panjang_VALUE;
    }
    static int cari_file(int 서술자, int OFFSET_VALUE, int Tugas_akar) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Tugas_akar < 0 || Tugas_akar > 2) return -22;
        int wallpaper_VALUE = Tugas_akar == 0 ? 0 : (Tugas_akar == 1 ? file_posisi[기술] : Memori_sistem_berkas.ukuran_Daftar[target[기술]]);
        if (OFFSET_VALUE > 0 && wallpaper_VALUE > 2147483647 - OFFSET_VALUE) return -75;
        if (OFFSET_VALUE < 0 && OFFSET_VALUE < -wallpaper_VALUE) return -22;
        file_posisi[기술] = wallpaper_VALUE + OFFSET_VALUE;
        return file_posisi[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Tugaskan_VALUE, int Konfigurasi) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Tugaskan_VALUE ? -9 : -22;
        if (Tugaskan_VALUE && 서술자 == 새서술자) return 새서술자;
        if (Tugaskan_VALUE) { if (buat_handel[새서술자] != 0) Tutup_file(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        buat_handel[새서술자] = 기술 + 1; 서술자설정[새서술자] = Konfigurasi; Referensi_COUNT[기술]++;
        return 새서술자;
    }
    static int hapus_file_entri_nama(int nama_surel) {
        int panjang_VALUE = 경로읽기(nama_surel);
        if (panjang_VALUE < 0) return panjang_VALUE;
        int berkas = Memori_sistem_berkas.FIND_entri(jalur_nama, panjang_VALUE);
        if (berkas < 0) return berkas;
        Memori_sistem_berkas.이름들[berkas * 64] = 0;
        return 0;
    }
    static int set_file_panjang(int 서술자, int panjang_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (buat_Pengaturan[기술] & 3) == 0 || panjang_VALUE < 0) return -22;
        if (panjang_VALUE > Memori_sistem_berkas.최대크기) return -27;
        int berkas = target[기술], surel = Ponsel_VALUE.file_Memori() + berkas * Memori_sistem_berkas.최대크기;
        for (int INDEX = Memori_sistem_berkas.ukuran_Daftar[berkas]; INDEX < panjang_VALUE; INDEX++) Ponsel_VALUE.tulis_Memori(surel + INDEX, 0);
        Memori_sistem_berkas.ukuran_Daftar[berkas] = panjang_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int surel) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klip(surel, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(surel + INDEX * 4, 0);
        int berkas = target[기술], Ukuran = 종류[기술] == 2 ? Memori_sistem_berkas.ukuran_Daftar[berkas] : 0;
        int 허가 = 종류[기술] == 2 ? Memori_sistem_berkas.허가들[berkas] : 438;
        실행관리.수쓰기(surel, 1);
        실행관리.수쓰기(surel + 4, 종류[기술] == 2 ? berkas + 1 : 100 + 기술);
        실행관리.수쓰기(surel + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(surel + 12, 종류[기술] == 2 && Memori_sistem_berkas.이름들[berkas * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(surel + 28, Ukuran); 실행관리.수쓰기(surel + 32, 512);
        실행관리.수쓰기(surel + 36, (Ukuran + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int perintah, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (perintah == 0 || perintah == 1030) return 서술자복제(서술자, VALUE, false, perintah == 1030 ? 1 : 0);
        if (perintah == 1) return 서술자설정[서술자];
        if (perintah == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (perintah == 3) return buat_Pengaturan[기술];
        if (perintah == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            buat_Pengaturan[기술] = (buat_Pengaturan[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Buat_peserta(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = kosong_handel();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Sambung(서술자, 기술, 3, 0, baca_tulis_bendera);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int surel_32(int surel) {
        return Ponsel_VALUE.기억읽기(surel) << 24 | Ponsel_VALUE.기억읽기(surel + 1) << 16
            | Ponsel_VALUE.기억읽기(surel + 2) << 8 | Ponsel_VALUE.기억읽기(surel + 3);
    }
    static int cek_surel(int surel, int panjang_VALUE) {
        if (panjang_VALUE < 16) return -22;
        if (!실행관리.klip(surel, 16)) return -14;
        return 실행관리.짧은수(surel) == 2 ? 0 : -97;
    }
    static int ikat_surel(int 서술자, int surel, int panjang_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int hasil = cek_surel(surel, panjang_VALUE);
        if (hasil < 0) return hasil;
        if (jaringan_handel[기술] != 0) return -22;
        int jaringan_surel = surel_32(surel + 4);
        if (jaringan_surel != 0 && jaringan_surel != jaringan_tumpuk.내주소) return -99;
        int nomor_port = Ponsel_VALUE.기억읽기(surel + 2) << 8 | Ponsel_VALUE.기억읽기(surel + 3);
        hasil = jaringan_tumpuk.Buka(nomor_port);
        if (hasil < 0) return hasil;
        jaringan_handel[기술] = hasil; target[기술] = jaringan_surel;
        return 0;
    }
    static int Otomatis_ikat(int 기술) {
        if (jaringan_handel[기술] != 0) return 0;
        int hasil = jaringan_tumpuk.Buka(0);
        if (hasil < 0) return hasil;
        jaringan_handel[기술] = hasil;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 permintaan 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int data_surel, int panjang_VALUE, int Konfigurasi, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Konfigurasi != 0) return -95;
        if (panjang_VALUE < 0 || panjang_VALUE > 1024) return -90;
        if (panjang_VALUE != 0 && !실행관리.klip(data_surel, panjang_VALUE)) return -14;
        if (!실행관리.klip(요청주소, 8)) return -14;
        int surel = 실행관리.수(요청주소);
        int hasil = cek_surel(surel, 실행관리.수(요청주소 + 4));
        if (hasil < 0) return hasil;
        int nomor_port = Ponsel_VALUE.기억읽기(surel + 2) << 8 | Ponsel_VALUE.기억읽기(surel + 3);
        if (nomor_port == 0) return -22;
        hasil = Otomatis_ikat(기술);
        if (hasil < 0) return hasil;
        for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) Transfer_data[INDEX] = Ponsel_VALUE.기억읽기(data_surel + INDEX);
        return jaringan_tumpuk.kirim(jaringan_handel[기술], surel_32(surel + 4), nomor_port, Transfer_data, panjang_VALUE);
    }
    static void tulis_surel(int surel, int panjang_VALUE, int jaringan_surel, int nomor_port) {
        for (int INDEX = 0; INDEX < panjang_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = nomor_port >>> 8;
            if (INDEX == 3) VALUE = nomor_port;
            if (INDEX >= 4 && INDEX < 8) VALUE = jaringan_surel >>> (56 - INDEX * 8);
            Ponsel_VALUE.tulis_Memori(surel + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int data_surel, int panjang_VALUE, int Konfigurasi, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Konfigurasi & ~64) != 0) return -95;
        if (panjang_VALUE < 0) return -22;
        if (panjang_VALUE != 0 && !실행관리.klip(data_surel, panjang_VALUE)) return -14;
        int surel = 0, surel_panjang_surel = 0, surel_panjang = 0;
        if (요청주소 != 0) {
            if (!실행관리.klip(요청주소, 8)) return -14;
            surel = 실행관리.수(요청주소); surel_panjang_surel = 실행관리.수(요청주소 + 4);
            if (surel != 0) {
                if (!실행관리.klip(surel_panjang_surel, 4)) return -14;
                surel_panjang = 실행관리.수(surel_panjang_surel);
                if (surel_panjang < 0) return -22;
                if (!실행관리.klip(surel, surel_panjang < 16 ? surel_panjang : 16)) return -14;
            }
        }
        int hasil = Otomatis_ikat(기술);
        if (hasil < 0) return hasil;
        int jalankan = Ponsel_VALUE.밀리초();
        while (true) {
            hasil = jaringan_tumpuk.terima(jaringan_handel[기술], Transfer_data, 1024, 0);
            if (hasil != -11) break;
            if ((Konfigurasi & 64) != 0 || (buat_Pengaturan[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && Ponsel_VALUE.밀리초() - jalankan >= 수신대기밀리초[기술]) return -11;
            if (Ponsel_VALUE.사용자남은밀리초() <= 10) return -11;
            Ponsel_VALUE.잠시양보();
        }
        if (hasil < 0) return hasil;
        if (hasil > panjang_VALUE) hasil = panjang_VALUE;
        for (int INDEX = 0; INDEX < hasil; INDEX++) Ponsel_VALUE.tulis_Memori(data_surel + INDEX, Transfer_data[INDEX]);
        if (surel != 0) {
            tulis_surel(surel, surel_panjang, jaringan_tumpuk.serekan_surel(jaringan_handel[기술]), jaringan_tumpuk.serekan_nomor_port(jaringan_handel[기술]));
            실행관리.수쓰기(surel_panjang_surel, 16);
        }
        return hasil;
    }
    static int 통신주소읽기(int 서술자, int surel, int panjang_surel) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klip(panjang_surel, 4)) return -14;
        int panjang_VALUE = 실행관리.수(panjang_surel);
        if (panjang_VALUE < 0) return -22;
        if (!실행관리.klip(surel, panjang_VALUE < 16 ? panjang_VALUE : 16)) return -14;
        int slot_entri = jaringan_tumpuk.INDEX(jaringan_handel[기술]);
        tulis_surel(surel, panjang_VALUE, target[기술], slot_entri < 0 ? 0 : jaringan_tumpuk.접속번호들[slot_entri]);
        실행관리.수쓰기(panjang_surel, 16);
        return 0;
    }
    static int set_terima_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
