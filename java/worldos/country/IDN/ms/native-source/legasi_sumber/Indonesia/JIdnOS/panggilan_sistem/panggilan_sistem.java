// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.JIdnOS.panggilan_sistem;

import Indonesia.JIdnOS.Memori_rantau.halaman_pengurus;
import Indonesia.JIdnOS.작업.Proses_VALUE;
import Indonesia.JIdnOS.작업.Penjadual;
import Indonesia.JIdnOS.sistem_fail.실행파일적재기;
import Indonesia.JIdnOS.sistem_fail.sistem_fail;
import Indonesia.JIdnOS.sistem_fail.fail_info;
import Indonesia.JIdnOS.kernel.하드웨어;
import Indonesia.JIdnOS.입력.입력관리자;
import Indonesia.JIdnOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class panggilan_sistem {
    public static final int baca_sahaja_bendera = 0;
    public static final int Cari_Mula = 0;
    public static final int 찾기현재 = 1;
    public static final int Cari_pemasukan_tamat = 2;

    private final sistem_fail sistem_fail;
    private final halaman_pengurus 쪽관리;
    private final Penjadual Penjadual;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 peranti_VALUE;
    private final 입력관리자 입력관리;

    public panggilan_sistem(sistem_fail sistem_fail, halaman_pengurus 쪽관리, Penjadual Penjadual, 하드웨어 peranti_VALUE, 입력관리자 입력관리) {
        this.sistem_fail = sistem_fail;
        this.쪽관리 = 쪽관리;
        this.Penjadual = Penjadual;
        this.peranti_VALUE = peranti_VALUE;
        this.입력관리 = 입력관리;
    }

    public int 과정식별자(Proses_VALUE 현재과정) {
        return 현재과정.식별자();
    }

    public int 부모과정식별자(Proses_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Buka(Proses_VALUE 현재과정, String Nama, int bendera_VALUE) {
        if (bendera_VALUE != baca_sahaja_bendera) {
            return -30;
        }
        return 현재과정.파일서술자().Buka(Nama);
    }

    public int Baca(Proses_VALUE 현재과정, int 서술자, byte[] 받을곳, int Saiz) {
        if (서술자 == 0) {
            if (Saiz <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 Peristiwa = 입력관리.Seterusnya_acara();
            if (Peristiwa == null || Peristiwa.jenis_peristiwa() != 입력사건.종류.Kunci_bawah) {
                return -11;
            }
            받을곳[0] = (byte) Peristiwa.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Baca(서술자, 받을곳, Saiz);
    }

    public int Tulis(Proses_VALUE 현재과정, int 서술자, byte[] data, int Saiz) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().teknologi_maklumat_buka(서술자) ? -30 : -9;
        }
        if (Saiz < 0 || Saiz > data.length) {
            return -22;
        }
        peranti_VALUE.직렬출력(new String(data, 0, Saiz, java.nio.charset.StandardCharsets.UTF_8));
        return Saiz;
    }

    public int Tutup(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Tutup(서술자);
    }

    public int alih_jawatan(Proses_VALUE 현재과정, int 서술자, int 거리, int projek_akar) {
        return 현재과정.파일서술자().alih_jawatan(서술자, 거리, projek_akar);
    }

    public int 서술자복제(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proses_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Nama, int kaedah_mod) {
        fail_info msinfo32_exe = sistem_fail.msinfo32_exe(Nama);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((kaedah_mod & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((kaedah_mod & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int tukar_senarai_tugas(String Nama) {
        return "/".equals(Nama) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int ID_pengguna() { return 0; }
    public int berkesan_ID_pengguna() { return 0; }
    public int 무리식별자() { return 0; }
    public int 유효무리식별자() { return 0; }

    public int segerak_fail(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Baca 전용이어서 밀어낼 자료가 없다.
    }

    public boolean teknologi_maklumat_Terminal(Proses_VALUE 현재과정, int 서술자) {
        fail_info msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int kawalan_fail(Proses_VALUE 현재과정, int 서술자, int Perintah, int parameter_argumen) {
        if (Perintah == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, parameter_argumen);
        }
        if (Perintah == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Perintah == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (parameter_argumen & 1) != 0);
        }
        if (Perintah == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : baca_sahaja_bendera;
        }
        if (Perintah == 4) {
            return parameter_argumen == baca_sahaja_bendera ? 0 : -30;
        }
        return -22;
    }

    public int cipta_pemasukan(String Nama, int keizinan_VALUE) {
        return -30;
    }

    public fail_info 서술자정보(Proses_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public sistem_Butiran sistem_Butiran() {
        return new sistem_Butiran("JIdnOS", "JIdnOS", "0.1", "Java managed kernel", "i386");
    }

    public fail_info fail_info(String Nama) {
        return sistem_fail.msinfo32_exe(Nama);
    }

    public Proses_VALUE klon_Proses(Proses_VALUE 부모) {
        return Penjadual.klon_VALUE(부모);
    }

    public int 자식기다리기(Proses_VALUE 부모, int 자식식별자, boolean 기다리지않음) {
        return Penjadual.자식기다리기(부모, 자식식별자, 기다리지않음);
    }

    public int aplikasi_putus(Proses_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.aplikasi_putus();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / halaman_pengurus.saiz_halaman;
        int 끝쪽 = (새끝 + halaman_pengurus.saiz_halaman - 1) / halaman_pengurus.saiz_halaman;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int e_mel = INDEX * halaman_pengurus.saiz_halaman;
                try {
                    쪽관리.바이트읽기(현재과정.e_mel_SPACE(), e_mel);
                } catch (IllegalStateException RALAT) {
                    쪽관리.MAP_halaman(현재과정.e_mel_SPACE(), e_mel, true);
                }
            }
        }
        현재과정.set_aplikasi_putus(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Proses_VALUE 현재과정, int tokokan_amaun) {
        int 이전끝 = 현재과정.aplikasi_putus();
        int ukuran = aplikasi_putus(현재과정, 이전끝 + tokokan_amaun);
        return ukuran < 0 ? ukuran : 이전끝;
    }

    public int laksanakan_perintah(Proses_VALUE 현재과정, byte[] fail_boleh_laku) {
        return laksanakan_perintah(현재과정, fail_boleh_laku, new String[0], new String[0]);
    }

    public int laksanakan_perintah(Proses_VALUE 현재과정, byte[] fail_boleh_laku, String[] parameter_argumen, String[] persekitaran) {
        실행파일적재기.imej imej_VALUE;
        try {
            imej_VALUE = 적재기.검사(fail_boleh_laku);
        } catch (IllegalArgumentException RALAT) {
            return -8;
        }
        if (parameter_argumen == null || persekitaran == null || parameter_argumen.length > 16 || persekitaran.length > 16) {
            return -7;
        }
        for (실행파일적재기.seksyen_VALUE seksyen_VALUE : imej_VALUE.구역들()) {
            if ((seksyen_VALUE.bendera_VALUE() & 2) == 0 || seksyen_VALUE.Saiz() == 0) {
                continue;
            }
            int 첫쪽 = seksyen_VALUE.e_mel() / halaman_pengurus.saiz_halaman;
            int 끝쪽 = (seksyen_VALUE.e_mel() + seksyen_VALUE.Saiz() + halaman_pengurus.saiz_halaman - 1) / halaman_pengurus.saiz_halaman;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int e_mel = INDEX * halaman_pengurus.saiz_halaman;
                try {
                    쪽관리.바이트읽기(현재과정.e_mel_SPACE(), e_mel);
                    쪽관리.Peribadi_julat_tulis(현재과정.e_mel_SPACE(), e_mel, halaman_pengurus.saiz_halaman);
                } catch (IllegalStateException RALAT) {
                    쪽관리.MAP_halaman(현재과정.e_mel_SPACE(), e_mel, true);
                }
            }
            for (int INDEX = 0; INDEX < seksyen_VALUE.Saiz(); INDEX++) {
                byte VALUE = seksyen_VALUE.종류() == 8 ? 0 : fail_boleh_laku[seksyen_VALUE.fail_jawatan() + INDEX];
                쪽관리.tulis_bait_VALUE(현재과정.e_mel_SPACE(), seksyen_VALUE.e_mel() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(imej_VALUE.alamat_mula(), parameter_argumen, persekitaran);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void keluar_aplikasi(Proses_VALUE 현재과정, int status_VALUE) {
        현재과정.Keluar_aplikasi(status_VALUE);
    }
}
