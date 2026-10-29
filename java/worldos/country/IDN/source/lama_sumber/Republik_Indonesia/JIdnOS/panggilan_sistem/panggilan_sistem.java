// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republik_Indonesia.JIdnOS.panggilan_sistem;

import Republik_Indonesia.JIdnOS.Memori_wilayah.halaman_Manajer;
import Republik_Indonesia.JIdnOS.작업.Proses_VALUE;
import Republik_Indonesia.JIdnOS.작업.Penjadwal;
import Republik_Indonesia.JIdnOS.sistem_berkas.실행파일적재기;
import Republik_Indonesia.JIdnOS.sistem_berkas.sistem_berkas;
import Republik_Indonesia.JIdnOS.sistem_berkas.file_info;
import Republik_Indonesia.JIdnOS.Inti.하드웨어;
import Republik_Indonesia.JIdnOS.입력.입력관리자;
import Republik_Indonesia.JIdnOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class panggilan_sistem {
    public static final int baca_saja_bendera = 0;
    public static final int Cari_Mulai = 0;
    public static final int Cari_saat_ini = 1;
    public static final int FIND_entri_mengakhiri = 2;

    private final sistem_berkas sistem_berkas;
    private final halaman_Manajer 쪽관리;
    private final Penjadwal Penjadwal;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 Ponsel_VALUE;
    private final 입력관리자 입력관리;

    public panggilan_sistem(sistem_berkas sistem_berkas, halaman_Manajer 쪽관리, Penjadwal Penjadwal, 하드웨어 Ponsel_VALUE, 입력관리자 입력관리) {
        this.sistem_berkas = sistem_berkas;
        this.쪽관리 = 쪽관리;
        this.Penjadwal = Penjadwal;
        this.Ponsel_VALUE = Ponsel_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Proses_pengidentifikasi(Proses_VALUE saat_ini_Proses) {
        return saat_ini_Proses.pengidentifikasi_VALUE();
    }

    public int induk_Proses_pengidentifikasi(Proses_VALUE saat_ini_Proses) {
        return saat_ini_Proses.induk_pengidentifikasi();
    }

    public int Buka(Proses_VALUE saat_ini_Proses, String Nama_2, int bendera_VALUE) {
        if (bendera_VALUE != baca_saja_bendera) {
            return -30;
        }
        return saat_ini_Proses.파일서술자().Buka(Nama_2);
    }

    public int Baca(Proses_VALUE saat_ini_Proses, int 서술자, byte[] terima_tujuan, int Ukuran) {
        if (서술자 == 0) {
            if (Ukuran <= 0 || terima_tujuan.length == 0) {
                return 0;
            }
            입력사건 Even = 입력관리.Berikutnya_acara();
            if (Even == null || Even.jenis_kejadian() != 입력사건.종류.Kunci_tidak_berfungsi) {
                return -11;
            }
            terima_tujuan[0] = (byte) Even.첫째값();
            return 1;
        }
        return saat_ini_Proses.파일서술자().Baca(서술자, terima_tujuan, Ukuran);
    }

    public int Tulis(Proses_VALUE saat_ini_Proses, int 서술자, byte[] data, int Ukuran) {
        if (서술자 != 1 && 서술자 != 2) {
            return saat_ini_Proses.파일서술자().teknologi_informasi_buat(서술자) ? -30 : -9;
        }
        if (Ukuran < 0 || Ukuran > data.length) {
            return -22;
        }
        Ponsel_VALUE.직렬출력(new String(data, 0, Ukuran, java.nio.charset.StandardCharsets.UTF_8));
        return Ukuran;
    }

    public int Tutup(Proses_VALUE saat_ini_Proses, int 서술자) {
        return saat_ini_Proses.파일서술자().Tutup(서술자);
    }

    public int gerak_posisi(Proses_VALUE saat_ini_Proses, int 서술자, int 거리, int Tugas_akar) {
        return saat_ini_Proses.파일서술자().gerak_posisi(서술자, 거리, Tugas_akar);
    }

    public int 서술자복제(Proses_VALUE saat_ini_Proses, int 서술자) {
        return saat_ini_Proses.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proses_VALUE saat_ini_Proses, int 서술자, int 새서술자) {
        return saat_ini_Proses.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Nama_2, int metode_MODE) {
        file_info msinfo32_exe = sistem_berkas.msinfo32_exe(Nama_2);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metode_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metode_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_daftar_tugas(String Nama_2) {
        return "/".equals(Nama_2) ? 0 : -20;
    }

    public String saat_ini_daftar_tugas(int terima_ukuran) {
        return terima_ukuran >= 2 ? "/" : null;
    }

    public int ID_pengguna() { return 0; }
    public int efektif_ID_pengguna() { return 0; }
    public int grup_pengidentifikasi() { return 0; }
    public int efektif_grup_pengidentifikasi() { return 0; }

    public int sinkro_file(Proses_VALUE saat_ini_Proses, int 서술자) {
        return saat_ini_Proses.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // saat_ini_item 파일체계는 Baca 전용이어서 밀어낼 자료가 없다.
    }

    public boolean teknologi_informasi_Terminal(Proses_VALUE saat_ini_Proses, int 서술자) {
        file_info msinfo32_exe = saat_ini_Proses.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int kendali_berkas(Proses_VALUE saat_ini_Proses, int 서술자, int perintah, int parameter_argumen) {
        if (perintah == 0) {
            return saat_ini_Proses.파일서술자().복제서술자(서술자, parameter_argumen);
        }
        if (perintah == 1) {
            return saat_ini_Proses.파일서술자().실행시닫기값(서술자);
        }
        if (perintah == 2) {
            return saat_ini_Proses.파일서술자().실행시닫기설정(서술자, (parameter_argumen & 1) != 0);
        }
        if (perintah == 3) {
            return saat_ini_Proses.파일서술자().msinfo32_exe(서술자) == null ? -9 : baca_saja_bendera;
        }
        if (perintah == 4) {
            return parameter_argumen == baca_saja_bendera ? 0 : -30;
        }
        return -22;
    }

    public int Buat_entri(String Nama_2, int izin_VALUE) {
        return -30;
    }

    public file_info 서술자정보(Proses_VALUE saat_ini_Proses, int 서술자) {
        return saat_ini_Proses.파일서술자().msinfo32_exe(서술자);
    }

    public sistem_Detail sistem_Detail() {
        return new sistem_Detail("JIdnOS", "JIdnOS", "0.1", "Java managed kernel", "i386");
    }

    public file_info file_info(String Nama_2) {
        return sistem_berkas.msinfo32_exe(Nama_2);
    }

    public Proses_VALUE klon_Proses(Proses_VALUE induk_VALUE) {
        return Penjadwal.klon_VALUE(induk_VALUE);
    }

    public int 자식기다리기(Proses_VALUE induk_VALUE, int turunan_pengidentifikasi, boolean 기다리지않음) {
        return Penjadwal.자식기다리기(induk_VALUE, turunan_pengidentifikasi, 기다리지않음);
    }

    public int apl_putus(Proses_VALUE saat_ini_Proses, int 새끝) {
        int 이전끝 = saat_ini_Proses.apl_putus();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / halaman_Manajer.ukuran_halaman;
        int 끝쪽 = (새끝 + halaman_Manajer.ukuran_halaman - 1) / halaman_Manajer.ukuran_halaman;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int surel = INDEX * halaman_Manajer.ukuran_halaman;
                try {
                    쪽관리.바이트읽기(saat_ini_Proses.surel_SPACE(), surel);
                } catch (IllegalStateException galat) {
                    쪽관리.MAP_halaman(saat_ini_Proses.surel_SPACE(), surel, true);
                }
            }
        }
        saat_ini_Proses.set_apl_putus(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Proses_VALUE saat_ini_Proses, int tahapan_jumlah) {
        int 이전끝 = saat_ini_Proses.apl_putus();
        int hasil = apl_putus(saat_ini_Proses, 이전끝 + tahapan_jumlah);
        return hasil < 0 ? hasil : 이전끝;
    }

    public int Jalankan_perintah(Proses_VALUE saat_ini_Proses, byte[] 실행파일) {
        return Jalankan_perintah(saat_ini_Proses, 실행파일, new String[0], new String[0]);
    }

    public int Jalankan_perintah(Proses_VALUE saat_ini_Proses, byte[] 실행파일, String[] parameter_argumen, String[] lingkungan) {
        실행파일적재기.foto foto_VALUE;
        try {
            foto_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException galat) {
            return -8;
        }
        if (parameter_argumen == null || lingkungan == null || parameter_argumen.length > 16 || lingkungan.length > 16) {
            return -7;
        }
        for (실행파일적재기.seksi_VALUE seksi_VALUE : foto_VALUE.구역들()) {
            if ((seksi_VALUE.bendera_VALUE() & 2) == 0 || seksi_VALUE.Ukuran() == 0) {
                continue;
            }
            int 첫쪽 = seksi_VALUE.surel() / halaman_Manajer.ukuran_halaman;
            int 끝쪽 = (seksi_VALUE.surel() + seksi_VALUE.Ukuran() + halaman_Manajer.ukuran_halaman - 1) / halaman_Manajer.ukuran_halaman;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int surel = INDEX * halaman_Manajer.ukuran_halaman;
                try {
                    쪽관리.바이트읽기(saat_ini_Proses.surel_SPACE(), surel);
                    쪽관리.privat_rentang_tulis(saat_ini_Proses.surel_SPACE(), surel, halaman_Manajer.ukuran_halaman);
                } catch (IllegalStateException galat) {
                    쪽관리.MAP_halaman(saat_ini_Proses.surel_SPACE(), surel, true);
                }
            }
            for (int INDEX = 0; INDEX < seksi_VALUE.Ukuran(); INDEX++) {
                byte VALUE = seksi_VALUE.종류() == 8 ? 0 : 실행파일[seksi_VALUE.file_posisi() + INDEX];
                쪽관리.tulis_byte_VALUE(saat_ini_Proses.surel_SPACE(), seksi_VALUE.surel() + INDEX, VALUE);
            }
        }
        saat_ini_Proses.실행문맥설정(foto_VALUE.alamat_permulaan(), parameter_argumen, lingkungan);
        saat_ini_Proses.파일서술자().실행시닫기();
        return 0;
    }

    public void berhenti_apl(Proses_VALUE saat_ini_Proses, int Status_VALUE) {
        saat_ini_Proses.Keluar_apl(Status_VALUE);
    }
}
