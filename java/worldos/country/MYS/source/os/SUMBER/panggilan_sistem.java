// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 ruang_pengguna penuding/길이는 capai_pemasukan 전에 검사한다. */
public final class panggilan_sistem {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_kepanjangan(int e_mel) {
        if (!실행관리.klip(e_mel, 4)) return -14;
        int kepanjangan_VALUE = 실행관리.수(e_mel);
        if (kepanjangan_VALUE < 0 || kepanjangan_VALUE > (실행관리.pengguna_tamat - e_mel - 4) / 4) return -14;
        return kepanjangan_VALUE;
    }

    public static int Proses_VALUE_pemasukan(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.buka_fail(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.tulis_fail(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.Tutup_fail(가);
        if (INDEX == 34) return 파일서술자관리.cari_fail(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.alih_keluar_fail_pemasukan_nama(가);
        if (INDEX == 39) return 파일서술자관리.set_fail_kepanjangan(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.cipta_peserta(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.ikat_e_mel(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.segerak();
        }
        if (INDEX == 1) {
            int kepanjangan_VALUE = ARRAY_kepanjangan(가);
            if (kepanjangan_VALUE < 0) return kepanjangan_VALUE;
            if (kepanjangan_VALUE > 4096) return -90;
            for (int aksara_VALUE = 0; aksara_VALUE < kepanjangan_VALUE; aksara_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + aksara_VALUE * 4) & 65535);
            return kepanjangan_VALUE;
        }
        if (INDEX == 2) return 실행관리.argumen_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argumen_COUNT ? 실행관리.argumen_e_mel[가] : 0;
        if (INDEX == 10) return rangkaian_tindan.Buka(가);
        if (INDEX == 11) {
            int kepanjangan_VALUE = ARRAY_kepanjangan(라);
            if (kepanjangan_VALUE < 0) return kepanjangan_VALUE;
            if (마 < 0 || 마 > kepanjangan_VALUE || 마 > 1024) return -90;
            for (int Kedudukan = 0; Kedudukan < 마; Kedudukan++) 임시자료[Kedudukan] = 실행관리.수(라 + 4 + Kedudukan * 4) & 255;
            return rangkaian_tindan.e_mel_9aee63bd(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int kepanjangan_VALUE = ARRAY_kepanjangan(나);
            if (kepanjangan_VALUE < 0) return kepanjangan_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int ukuran = rangkaian_tindan.받기(가, 임시자료, kepanjangan_VALUE < 1024 ? kepanjangan_VALUE : 1024, 다);
            if (ukuran >= 0) for (int Kedudukan = 0; Kedudukan < ukuran; Kedudukan++) 실행관리.수쓰기(나 + 4 + Kedudukan * 4, 임시자료[Kedudukan]);
            return ukuran;
        }
        if (INDEX == 13) return rangkaian_tindan.Tutup(가);
        if (INDEX == 14) return rangkaian_tindan.내주소;
        if (INDEX == 15) return rangkaian_tindan.rakan_e_mel(가);
        if (INDEX == 16) return rangkaian_tindan.rakan_nombor_port(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int nama_saiz = ARRAY_kepanjangan(가), data_saiz = ARRAY_kepanjangan(나);
            if (nama_saiz < 0 || data_saiz < 0) return -14;
            if (nama_saiz < 1 || nama_saiz > 64) return -22;
            int kepanjangan_VALUE = 0;
            while (kepanjangan_VALUE < nama_saiz && 실행관리.수(가 + 4 + kepanjangan_VALUE * 4) != 0) {
                Memori_sistem_fail.Nama[kepanjangan_VALUE] = 실행관리.수(가 + 4 + kepanjangan_VALUE * 4);
                kepanjangan_VALUE++;
            }
            if (!Memori_sistem_fail.cek_nama(Memori_sistem_fail.Nama, kepanjangan_VALUE)) return -22;
            if (INDEX == 20) {
                int Fail = Memori_sistem_fail.Cari_pemasukan(Memori_sistem_fail.Nama, kepanjangan_VALUE);
                if (Fail < 0) return Fail;
                int Saiz = Memori_sistem_fail.saiz_Senarai[Fail];
                if (Saiz > data_saiz) return -90;
                int e_mel = peranti_VALUE.fail_Memori() + Fail * Memori_sistem_fail.최대크기;
                for (int 수 = 0; 수 < Saiz; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, peranti_VALUE.기억읽기(e_mel + 수));
                return Saiz;
            }
            if (다 < 0 || 다 > data_saiz) return -22;
            if (다 > Memori_sistem_fail.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memori_sistem_fail.edit_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Memori_sistem_fail.stor_VALUE(Memori_sistem_fail.Nama, kepanjangan_VALUE, Memori_sistem_fail.edit_VALUE, 다);
        }
        return -38;
    }
}
