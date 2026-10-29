// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Belanda.JNldOS.Memori_wilayah.halaman_Manajer;
import Belanda.JNldOS.sistem_berkas.파일서술자표;

/** Proses_VALUE 식별자와 라운드로빈 Siapkan 대기열을 관리한다. */
public final class Penjadwal {
    private final halaman_Manajer 쪽관리;
    private final Map<Integer, Proses_VALUE> Daftar_Proses = new HashMap<Integer, Proses_VALUE>();
    private final Queue<Proses_VALUE> 준비대기열 = new ArrayDeque<Proses_VALUE>();
    private int Berikutnya_pengidentifikasi = 1;

    public Penjadwal(halaman_Manajer 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proses_VALUE 첫과정(파일서술자표 파일서술자) {
        Proses_VALUE 새과정 = new Proses_VALUE(alokasi_pengidentifikasi(), 0, 쪽관리.새주소공간(), 파일서술자);
        Daftar_Proses.put(Integer.valueOf(새과정.pengidentifikasi_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proses_VALUE klon_VALUE(Proses_VALUE induk_VALUE) {
        Proses_VALUE turunan_VALUE = new Proses_VALUE(
                alokasi_pengidentifikasi(),
                induk_VALUE.pengidentifikasi_VALUE(),
                쪽관리.쓰기시복사복제(induk_VALUE.surel_SPACE()),
                induk_VALUE.파일서술자().klon_VALUE());
        turunan_VALUE.set_apl_putus(induk_VALUE.apl_putus());
        Daftar_Proses.put(Integer.valueOf(turunan_VALUE.pengidentifikasi_VALUE()), turunan_VALUE);
        준비대기열.offer(turunan_VALUE);
        return turunan_VALUE;
    }

    public Proses_VALUE Berikutnya_Proses() {
        int cek_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < cek_COUNT; INDEX++) {
            Proses_VALUE Berikutnya_item = 준비대기열.poll();
            if (Berikutnya_item != null && (Berikutnya_item.Status_VALUE() == Proses_Status.Siapkan || Berikutnya_item.Status_VALUE() == Proses_Status.Jalankan_perintah)) {
                Berikutnya_item.set_Status(Proses_Status.Jalankan_perintah);
                준비대기열.offer(Berikutnya_item);
                return Berikutnya_item;
            }
        }
        return null;
    }

    public int 자식기다리기(Proses_VALUE induk_VALUE, int turunan_pengidentifikasi, boolean 기다리지않음) {
        for (Proses_VALUE 후보 : Daftar_Proses.values()) {
            if (후보.induk_pengidentifikasi() != induk_VALUE.pengidentifikasi_VALUE()) {
                continue;
            }
            if (turunan_pengidentifikasi > 0 && 후보.pengidentifikasi_VALUE() != turunan_pengidentifikasi) {
                continue;
            }
            if (후보.Status_VALUE() == Proses_Status.Keluar_apl) {
                int hasil = (후보.Keluar_CODE() & 0xff) << 8;
                Daftar_Proses.remove(Integer.valueOf(후보.pengidentifikasi_VALUE()));
                return hasil;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proses_VALUE FIND_Proses(int pengidentifikasi_VALUE) {
        return Daftar_Proses.get(Integer.valueOf(pengidentifikasi_VALUE));
    }

    private int alokasi_pengidentifikasi() {
        return Berikutnya_pengidentifikasi++;
    }
}
