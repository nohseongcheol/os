// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 ruang_pengguna 과정의 파일서술자와 열린 Fail 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int baca_tulis_bendera = 2, cipta_pemasukan = 64, 독점생성 = 128, buang_TOC = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] buka_pemegang = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], sasaran = new int[서술자한도];
    static int[] fail_jawatan = new int[서술자한도], buka_Seting = new int[서술자한도], Rujukan_COUNT = new int[서술자한도];
    static int[] rangkaian_pemegang = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] laluan_nama = new int[64], pindah_data = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return buka_pemegang[파일서술자] - 1;
    }
    static int 빈서술자(int Jalan) {
        for (int INDEX = Jalan; INDEX < 서술자한도; INDEX++) if (buka_pemegang[INDEX] == 0) return INDEX;
        return -24;
    }
    static int 빈기술() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Rujukan_COUNT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Sambung(int 서술자, int 기술, int 파일종류, int fail_sasaran, int Tetapan) {
        buka_pemegang[서술자] = 기술 + 1; 서술자설정[서술자] = (Tetapan & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; sasaran[기술] = fail_sasaran; Rujukan_COUNT[기술] = 1;
        buka_Seting[기술] = Tetapan & (3 | 이어쓰기 | 기다리지않기); fail_jawatan[기술] = 0;
        rangkaian_pemegang[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Mula_Proses() {
        CLEAN_Proses();
        for (int INDEX = 0; INDEX < 3; INDEX++) Sambung(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void CLEAN_Proses() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (buka_pemegang[INDEX] != 0) Tutup_fail(INDEX);
    }
    static int Tutup_fail(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        buka_pemegang[서술자] = 0; 서술자설정[서술자] = 0;
        Rujukan_COUNT[기술]--;
        if (Rujukan_COUNT[기술] == 0) {
            if (종류[기술] == 2) Memori_sistem_fail.buka_COUNT[sasaran[기술]]--;
            if (종류[기술] == 3 && rangkaian_pemegang[기술] != 0) rangkaian_tindan.Tutup(rangkaian_pemegang[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bait_VALUE 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int e_mel) {
        if (!실행관리.klip(e_mel, 1)) return -14;
        int Kedudukan = peranti_VALUE.기억읽기(e_mel) == '/' ? 1 : 0;
        for (int kepanjangan_VALUE = 0; kepanjangan_VALUE < 64; kepanjangan_VALUE++) {
            if (!실행관리.klip(e_mel + Kedudukan + kepanjangan_VALUE, 1)) return -14;
            int VALUE = peranti_VALUE.기억읽기(e_mel + Kedudukan + kepanjangan_VALUE);
            laluan_nama[kepanjangan_VALUE] = VALUE;
            if (VALUE == 0) return kepanjangan_VALUE == 0 ? -2 : (Memori_sistem_fail.cek_nama(laluan_nama, kepanjangan_VALUE) ? kepanjangan_VALUE : -22);
            if (VALUE == '/') return -20;
        }
        return -36;
    }
    static int buka_fail(int nama_e_mel, int Tetapan, int 허가) {
        int kepanjangan_VALUE = 경로읽기(nama_e_mel);
        if (kepanjangan_VALUE < 0) return kepanjangan_VALUE;
        if ((Tetapan & ~(3 | cipta_pemasukan | 독점생성 | buang_TOC | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Tetapan & 3) == 3 || ((Tetapan & buang_TOC) != 0 && (Tetapan & 3) == 0)) return -22;
        int Fail = Memori_sistem_fail.Cari_pemasukan(laluan_nama, kepanjangan_VALUE);
        if (Fail >= 0 && (Tetapan & (cipta_pemasukan | 독점생성)) == (cipta_pemasukan | 독점생성)) return -17;
        if (Fail == -2 && (Tetapan & cipta_pemasukan) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fail == -2) {
            int ukuran = Memori_sistem_fail.stor_VALUE(laluan_nama, kepanjangan_VALUE, laluan_nama, 0);
            if (ukuran < 0) return ukuran;
            Fail = Memori_sistem_fail.Cari_pemasukan(laluan_nama, kepanjangan_VALUE);
            Memori_sistem_fail.허가들[Fail] = 허가 & 511;
        }
        if (Fail < 0) return Fail;
        if ((Tetapan & buang_TOC) != 0) Memori_sistem_fail.saiz_Senarai[Fail] = 0;
        Memori_sistem_fail.buka_COUNT[Fail]++;
        return Sambung(서술자, 기술, 2, Fail, Tetapan);
    }
    static int 파일읽기(int 서술자, int data_e_mel, int kepanjangan_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (buka_Seting[기술] & 3) == 1) return -9;
        if (kepanjangan_VALUE < 0) return -22;
        if (kepanjangan_VALUE == 0) return 0;
        if (!실행관리.klip(data_e_mel, kepanjangan_VALUE)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, data_e_mel, kepanjangan_VALUE, 0, 0);
        if (종류[기술] == 1) {
            int RECEIVED_COUNT = 0;
            while (RECEIVED_COUNT < kepanjangan_VALUE) {
                int VALUE = SMS_Terminal.직렬읽기();
                if (VALUE < 0) VALUE = papan_kekunci.Baca();
                if (VALUE < 0) {
                    if (RECEIVED_COUNT > 0) return RECEIVED_COUNT;
                    if ((buka_Seting[기술] & 기다리지않기) != 0) return -11;
                    if (peranti_VALUE.사용자남은밀리초() <= 10) return -11;
                    rangkaian_tindan.tentu_sahkan(); peranti_VALUE.잠시양보();
                } else {
                    peranti_VALUE.tulis_Memori(data_e_mel + RECEIVED_COUNT, VALUE); RECEIVED_COUNT++;
                }
            }
            return RECEIVED_COUNT;
        }
        int Fail = sasaran[기술], Kedudukan = fail_jawatan[기술];
        if (Kedudukan >= Memori_sistem_fail.saiz_Senarai[Fail]) return 0;
        if (kepanjangan_VALUE > Memori_sistem_fail.saiz_Senarai[Fail] - Kedudukan) kepanjangan_VALUE = Memori_sistem_fail.saiz_Senarai[Fail] - Kedudukan;
        int 원본주소 = peranti_VALUE.fail_Memori() + Fail * Memori_sistem_fail.최대크기 + Kedudukan;
        for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) peranti_VALUE.tulis_Memori(data_e_mel + INDEX, peranti_VALUE.기억읽기(원본주소 + INDEX));
        fail_jawatan[기술] += kepanjangan_VALUE;
        return kepanjangan_VALUE;
    }
    static int tulis_fail(int 서술자, int data_e_mel, int kepanjangan_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (buka_Seting[기술] & 3) == 0) return -9;
        if (kepanjangan_VALUE < 0) return -22;
        if (kepanjangan_VALUE == 0) return 0;
        if (!실행관리.klip(data_e_mel, kepanjangan_VALUE)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 destinasi_VALUE 주소가 필요하다.
        if (종류[기술] == 1) {
            if (kepanjangan_VALUE > 16384) kepanjangan_VALUE = 16384;
            for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) {
                int VALUE = peranti_VALUE.기억읽기(data_e_mel + INDEX);
                SMS_Terminal.직렬바이트(VALUE); SMS_Terminal.화면문자(VALUE);
            }
            return kepanjangan_VALUE;
        }
        int Fail = sasaran[기술], Saiz = Memori_sistem_fail.saiz_Senarai[Fail];
        int Kedudukan = (buka_Seting[기술] & 이어쓰기) != 0 ? Saiz : fail_jawatan[기술];
        if (Kedudukan >= Memori_sistem_fail.최대크기) return -27;
        if (kepanjangan_VALUE > Memori_sistem_fail.최대크기 - Kedudukan) kepanjangan_VALUE = Memori_sistem_fail.최대크기 - Kedudukan;
        int destinasi_e_mel = peranti_VALUE.fail_Memori() + Fail * Memori_sistem_fail.최대크기;
        for (int INDEX = Saiz; INDEX < Kedudukan; INDEX++) peranti_VALUE.tulis_Memori(destinasi_e_mel + INDEX, 0);
        for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) peranti_VALUE.tulis_Memori(destinasi_e_mel + Kedudukan + INDEX, peranti_VALUE.기억읽기(data_e_mel + INDEX));
        fail_jawatan[기술] = Kedudukan + kepanjangan_VALUE;
        if (Kedudukan + kepanjangan_VALUE > Saiz) Memori_sistem_fail.saiz_Senarai[Fail] = Kedudukan + kepanjangan_VALUE;
        return kepanjangan_VALUE;
    }
    static int cari_fail(int 서술자, int Ofset_VALUE, int projek_akar) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (projek_akar < 0 || projek_akar > 2) return -22;
        int latar_VALUE = projek_akar == 0 ? 0 : (projek_akar == 1 ? fail_jawatan[기술] : Memori_sistem_fail.saiz_Senarai[sasaran[기술]]);
        if (Ofset_VALUE > 0 && latar_VALUE > 2147483647 - Ofset_VALUE) return -75;
        if (Ofset_VALUE < 0 && Ofset_VALUE < -latar_VALUE) return -22;
        fail_jawatan[기술] = latar_VALUE + Ofset_VALUE;
        return fail_jawatan[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Tugaskan_VALUE, int Tetapan) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Tugaskan_VALUE ? -9 : -22;
        if (Tugaskan_VALUE && 서술자 == 새서술자) return 새서술자;
        if (Tugaskan_VALUE) { if (buka_pemegang[새서술자] != 0) Tutup_fail(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        buka_pemegang[새서술자] = 기술 + 1; 서술자설정[새서술자] = Tetapan; Rujukan_COUNT[기술]++;
        return 새서술자;
    }
    static int alih_keluar_fail_pemasukan_nama(int nama_e_mel) {
        int kepanjangan_VALUE = 경로읽기(nama_e_mel);
        if (kepanjangan_VALUE < 0) return kepanjangan_VALUE;
        int Fail = Memori_sistem_fail.Cari_pemasukan(laluan_nama, kepanjangan_VALUE);
        if (Fail < 0) return Fail;
        Memori_sistem_fail.이름들[Fail * 64] = 0;
        return 0;
    }
    static int set_fail_kepanjangan(int 서술자, int kepanjangan_VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (buka_Seting[기술] & 3) == 0 || kepanjangan_VALUE < 0) return -22;
        if (kepanjangan_VALUE > Memori_sistem_fail.최대크기) return -27;
        int Fail = sasaran[기술], e_mel = peranti_VALUE.fail_Memori() + Fail * Memori_sistem_fail.최대크기;
        for (int INDEX = Memori_sistem_fail.saiz_Senarai[Fail]; INDEX < kepanjangan_VALUE; INDEX++) peranti_VALUE.tulis_Memori(e_mel + INDEX, 0);
        Memori_sistem_fail.saiz_Senarai[Fail] = kepanjangan_VALUE;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int e_mel) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.klip(e_mel, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(e_mel + INDEX * 4, 0);
        int Fail = sasaran[기술], Saiz = 종류[기술] == 2 ? Memori_sistem_fail.saiz_Senarai[Fail] : 0;
        int 허가 = 종류[기술] == 2 ? Memori_sistem_fail.허가들[Fail] : 438;
        실행관리.수쓰기(e_mel, 1);
        실행관리.수쓰기(e_mel + 4, 종류[기술] == 2 ? Fail + 1 : 100 + 기술);
        실행관리.수쓰기(e_mel + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(e_mel + 12, 종류[기술] == 2 && Memori_sistem_fail.이름들[Fail * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(e_mel + 28, Saiz); 실행관리.수쓰기(e_mel + 32, 512);
        실행관리.수쓰기(e_mel + 36, (Saiz + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Perintah, int VALUE) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Perintah == 0 || Perintah == 1030) return 서술자복제(서술자, VALUE, false, Perintah == 1030 ? 1 : 0);
        if (Perintah == 1) return 서술자설정[서술자];
        if (Perintah == 2) { if ((VALUE & ~1) != 0) return -22; 서술자설정[서술자] = VALUE; return 0; }
        if (Perintah == 3) return buka_Seting[기술];
        if (Perintah == 4) {
            if ((VALUE & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            buka_Seting[기술] = (buka_Seting[기술] & 3) | (VALUE & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int cipta_peserta(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Sambung(서술자, 기술, 3, 0, baca_tulis_bendera);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int e_mel_32(int e_mel) {
        return peranti_VALUE.기억읽기(e_mel) << 24 | peranti_VALUE.기억읽기(e_mel + 1) << 16
            | peranti_VALUE.기억읽기(e_mel + 2) << 8 | peranti_VALUE.기억읽기(e_mel + 3);
    }
    static int cek_e_mel(int e_mel, int kepanjangan_VALUE) {
        if (kepanjangan_VALUE < 16) return -22;
        if (!실행관리.klip(e_mel, 16)) return -14;
        return 실행관리.짧은수(e_mel) == 2 ? 0 : -97;
    }
    static int ikat_e_mel(int 서술자, int e_mel, int kepanjangan_VALUE) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int ukuran = cek_e_mel(e_mel, kepanjangan_VALUE);
        if (ukuran < 0) return ukuran;
        if (rangkaian_pemegang[기술] != 0) return -22;
        int rangkaian_e_mel_df3458bb = e_mel_32(e_mel + 4);
        if (rangkaian_e_mel_df3458bb != 0 && rangkaian_e_mel_df3458bb != rangkaian_tindan.내주소) return -99;
        int nombor_port = peranti_VALUE.기억읽기(e_mel + 2) << 8 | peranti_VALUE.기억읽기(e_mel + 3);
        ukuran = rangkaian_tindan.Buka(nombor_port);
        if (ukuran < 0) return ukuran;
        rangkaian_pemegang[기술] = ukuran; sasaran[기술] = rangkaian_e_mel_df3458bb;
        return 0;
    }
    static int Auto_ikat(int 기술) {
        if (rangkaian_pemegang[기술] != 0) return 0;
        int ukuran = rangkaian_tindan.Buka(0);
        if (ukuran < 0) return ukuran;
        rangkaian_pemegang[기술] = ukuran;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 permintaan 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int data_e_mel, int kepanjangan_VALUE, int Tetapan, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Tetapan != 0) return -95;
        if (kepanjangan_VALUE < 0 || kepanjangan_VALUE > 1024) return -90;
        if (kepanjangan_VALUE != 0 && !실행관리.klip(data_e_mel, kepanjangan_VALUE)) return -14;
        if (!실행관리.klip(요청주소, 8)) return -14;
        int e_mel = 실행관리.수(요청주소);
        int ukuran = cek_e_mel(e_mel, 실행관리.수(요청주소 + 4));
        if (ukuran < 0) return ukuran;
        int nombor_port = peranti_VALUE.기억읽기(e_mel + 2) << 8 | peranti_VALUE.기억읽기(e_mel + 3);
        if (nombor_port == 0) return -22;
        ukuran = Auto_ikat(기술);
        if (ukuran < 0) return ukuran;
        for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) pindah_data[INDEX] = peranti_VALUE.기억읽기(data_e_mel + INDEX);
        return rangkaian_tindan.e_mel_9aee63bd(rangkaian_pemegang[기술], e_mel_32(e_mel + 4), nombor_port, pindah_data, kepanjangan_VALUE);
    }
    static void tulis_e_mel(int e_mel, int kepanjangan_VALUE, int rangkaian_e_mel_df3458bb, int nombor_port) {
        for (int INDEX = 0; INDEX < kepanjangan_VALUE && INDEX < 16; INDEX++) {
            int VALUE = 0;
            if (INDEX == 0) VALUE = 2;
            if (INDEX == 2) VALUE = nombor_port >>> 8;
            if (INDEX == 3) VALUE = nombor_port;
            if (INDEX >= 4 && INDEX < 8) VALUE = rangkaian_e_mel_df3458bb >>> (56 - INDEX * 8);
            peranti_VALUE.tulis_Memori(e_mel + INDEX, VALUE & 255);
        }
    }
    static int 자료전문받기(int 서술자, int data_e_mel, int kepanjangan_VALUE, int Tetapan, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Tetapan & ~64) != 0) return -95;
        if (kepanjangan_VALUE < 0) return -22;
        if (kepanjangan_VALUE != 0 && !실행관리.klip(data_e_mel, kepanjangan_VALUE)) return -14;
        int e_mel = 0, e_mel_kepanjangan_e_mel = 0, e_mel_kepanjangan = 0;
        if (요청주소 != 0) {
            if (!실행관리.klip(요청주소, 8)) return -14;
            e_mel = 실행관리.수(요청주소); e_mel_kepanjangan_e_mel = 실행관리.수(요청주소 + 4);
            if (e_mel != 0) {
                if (!실행관리.klip(e_mel_kepanjangan_e_mel, 4)) return -14;
                e_mel_kepanjangan = 실행관리.수(e_mel_kepanjangan_e_mel);
                if (e_mel_kepanjangan < 0) return -22;
                if (!실행관리.klip(e_mel, e_mel_kepanjangan < 16 ? e_mel_kepanjangan : 16)) return -14;
            }
        }
        int ukuran = Auto_ikat(기술);
        if (ukuran < 0) return ukuran;
        int Jalan = peranti_VALUE.밀리초();
        while (true) {
            ukuran = rangkaian_tindan.받기(rangkaian_pemegang[기술], pindah_data, 1024, 0);
            if (ukuran != -11) break;
            if ((Tetapan & 64) != 0 || (buka_Seting[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && peranti_VALUE.밀리초() - Jalan >= 수신대기밀리초[기술]) return -11;
            if (peranti_VALUE.사용자남은밀리초() <= 10) return -11;
            peranti_VALUE.잠시양보();
        }
        if (ukuran < 0) return ukuran;
        if (ukuran > kepanjangan_VALUE) ukuran = kepanjangan_VALUE;
        for (int INDEX = 0; INDEX < ukuran; INDEX++) peranti_VALUE.tulis_Memori(data_e_mel + INDEX, pindah_data[INDEX]);
        if (e_mel != 0) {
            tulis_e_mel(e_mel, e_mel_kepanjangan, rangkaian_tindan.rakan_e_mel(rangkaian_pemegang[기술]), rangkaian_tindan.rakan_nombor_port(rangkaian_pemegang[기술]));
            실행관리.수쓰기(e_mel_kepanjangan_e_mel, 16);
        }
        return ukuran;
    }
    static int 통신주소읽기(int 서술자, int e_mel, int kepanjangan_e_mel) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.klip(kepanjangan_e_mel, 4)) return -14;
        int kepanjangan_VALUE = 실행관리.수(kepanjangan_e_mel);
        if (kepanjangan_VALUE < 0) return -22;
        if (!실행관리.klip(e_mel, kepanjangan_VALUE < 16 ? kepanjangan_VALUE : 16)) return -14;
        int 칸 = rangkaian_tindan.INDEX(rangkaian_pemegang[기술]);
        tulis_e_mel(e_mel, kepanjangan_VALUE, sasaran[기술], 칸 < 0 ? 0 : rangkaian_tindan.접속번호들[칸]);
        실행관리.수쓰기(kepanjangan_e_mel, 16);
        return 0;
    }
    static int 수신대기정하기(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
