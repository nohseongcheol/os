// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 ruang_pengguna pointer/길이는 akses_entri 전에 검사한다. */
public final class panggilan_sistem {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_panjang(int surel) {
        if (!실행관리.klip(surel, 4)) return -14;
        int panjang_VALUE = 실행관리.수(surel);
        if (panjang_VALUE < 0 || panjang_VALUE > (실행관리.pengguna_mengakhiri - surel - 4) / 4) return -14;
        return panjang_VALUE;
    }

    public static int Proses_VALUE_entri(int INDEX, int 가, int SECOND_operand, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.buat_file(가, SECOND_operand, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, SECOND_operand, 다);
        if (INDEX == 32) return 파일서술자관리.tulis_file(가, SECOND_operand, 다);
        if (INDEX == 33) return 파일서술자관리.Tutup_file(가);
        if (INDEX == 34) return 파일서술자관리.cari_file(가, SECOND_operand, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SECOND_operand, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, SECOND_operand);
        if (INDEX == 38) return 파일서술자관리.hapus_file_entri_nama(가);
        if (INDEX == 39) return 파일서술자관리.set_file_panjang(가, SECOND_operand);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SECOND_operand, 다);
        if (INDEX == 41) return 파일서술자관리.Buat_peserta(가, SECOND_operand, 다);
        if (INDEX == 42) return 파일서술자관리.ikat_surel(가, SECOND_operand, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, SECOND_operand, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, SECOND_operand, 다);
        if (INDEX == 46) return 파일서술자관리.set_terima_TIMEOUT(가, SECOND_operand);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinkro();
        }
        if (INDEX == 1) {
            int panjang_VALUE = ARRAY_panjang(가);
            if (panjang_VALUE < 0) return panjang_VALUE;
            if (panjang_VALUE > 4096) return -90;
            for (int karakter_VALUE = 0; karakter_VALUE < panjang_VALUE; karakter_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + karakter_VALUE * 4) & 65535);
            return panjang_VALUE;
        }
        if (INDEX == 2) return 실행관리.argumen_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argumen_COUNT ? 실행관리.argumen_surel[가] : 0;
        if (INDEX == 10) return jaringan_tumpuk.Buka(가);
        if (INDEX == 11) {
            int panjang_VALUE = ARRAY_panjang(라);
            if (panjang_VALUE < 0) return panjang_VALUE;
            if (마 < 0 || 마 > panjang_VALUE || 마 > 1024) return -90;
            for (int posisi = 0; posisi < 마; posisi++) 임시자료[posisi] = 실행관리.수(라 + 4 + posisi * 4) & 255;
            return jaringan_tumpuk.kirim(가, SECOND_operand, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int panjang_VALUE = ARRAY_panjang(SECOND_operand);
            if (panjang_VALUE < 0) return panjang_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int hasil = jaringan_tumpuk.terima(가, 임시자료, panjang_VALUE < 1024 ? panjang_VALUE : 1024, 다);
            if (hasil >= 0) for (int posisi = 0; posisi < hasil; posisi++) 실행관리.수쓰기(SECOND_operand + 4 + posisi * 4, 임시자료[posisi]);
            return hasil;
        }
        if (INDEX == 13) return jaringan_tumpuk.Tutup(가);
        if (INDEX == 14) return jaringan_tumpuk.내주소;
        if (INDEX == 15) return jaringan_tumpuk.serekan_surel(가);
        if (INDEX == 16) return jaringan_tumpuk.serekan_nomor_port(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int nama_ukuran = ARRAY_panjang(가), data_ukuran = ARRAY_panjang(SECOND_operand);
            if (nama_ukuran < 0 || data_ukuran < 0) return -14;
            if (nama_ukuran < 1 || nama_ukuran > 64) return -22;
            int panjang_VALUE = 0;
            while (panjang_VALUE < nama_ukuran && 실행관리.수(가 + 4 + panjang_VALUE * 4) != 0) {
                Memori_sistem_berkas.Nama_2[panjang_VALUE] = 실행관리.수(가 + 4 + panjang_VALUE * 4);
                panjang_VALUE++;
            }
            if (!Memori_sistem_berkas.cek_nama(Memori_sistem_berkas.Nama_2, panjang_VALUE)) return -22;
            if (INDEX == 20) {
                int berkas = Memori_sistem_berkas.FIND_entri(Memori_sistem_berkas.Nama_2, panjang_VALUE);
                if (berkas < 0) return berkas;
                int Ukuran = Memori_sistem_berkas.ukuran_Daftar[berkas];
                if (Ukuran > data_ukuran) return -90;
                int surel = Ponsel_VALUE.file_Memori() + berkas * Memori_sistem_berkas.최대크기;
                for (int 수 = 0; 수 < Ukuran; 수++) 실행관리.수쓰기(SECOND_operand + 4 + 수 * 4, Ponsel_VALUE.기억읽기(surel + 수));
                return Ukuran;
            }
            if (다 < 0 || 다 > data_ukuran) return -22;
            if (다 > Memori_sistem_berkas.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memori_sistem_berkas.Edit_VALUE[수] = 실행관리.수(SECOND_operand + 4 + 수 * 4) & 255;
            return Memori_sistem_berkas.Store_VALUE(Memori_sistem_berkas.Nama_2, panjang_VALUE, Memori_sistem_berkas.Edit_VALUE, 다);
        }
        return -38;
    }
}
