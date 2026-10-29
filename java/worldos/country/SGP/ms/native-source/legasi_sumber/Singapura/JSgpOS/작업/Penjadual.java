// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Singapura.JSgpOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Singapura.JSgpOS.Memori_rantau.halaman_pengurus;
import Singapura.JSgpOS.sistem_fail.파일서술자표;

/** Proses_VALUE 식별자와 라운드로빈 Sediakan 대기열을 관리한다. */
public final class Penjadual {
    private final halaman_pengurus 쪽관리;
    private final Map<Integer, Proses_VALUE> Proses_Senarai = new HashMap<Integer, Proses_VALUE>();
    private final Queue<Proses_VALUE> 준비대기열 = new ArrayDeque<Proses_VALUE>();
    private int 다음식별자 = 1;

    public Penjadual(halaman_pengurus 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proses_VALUE 첫과정(파일서술자표 파일서술자) {
        Proses_VALUE 새과정 = new Proses_VALUE(식별자할당(), 0, 쪽관리.새주소공간(), 파일서술자);
        Proses_Senarai.put(Integer.valueOf(새과정.식별자()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proses_VALUE klon_VALUE(Proses_VALUE 부모) {
        Proses_VALUE anak_VALUE = new Proses_VALUE(
                식별자할당(),
                부모.식별자(),
                쪽관리.klon_COW(부모.e_mel_SPACE()),
                부모.파일서술자().klon_VALUE());
        anak_VALUE.set_aplikasi_putus(부모.aplikasi_putus());
        Proses_Senarai.put(Integer.valueOf(anak_VALUE.식별자()), anak_VALUE);
        준비대기열.offer(anak_VALUE);
        return anak_VALUE;
    }

    public Proses_VALUE Seterusnya_Proses() {
        int cek_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < cek_COUNT; INDEX++) {
            Proses_VALUE Seterusnya_item = 준비대기열.poll();
            if (Seterusnya_item != null && (Seterusnya_item.status_VALUE() == Proses_status.Sediakan || Seterusnya_item.status_VALUE() == Proses_status.laksanakan_perintah)) {
                Seterusnya_item.set_status(Proses_status.laksanakan_perintah);
                준비대기열.offer(Seterusnya_item);
                return Seterusnya_item;
            }
        }
        return null;
    }

    public int 자식기다리기(Proses_VALUE 부모, int 자식식별자, boolean 기다리지않음) {
        for (Proses_VALUE 후보 : Proses_Senarai.values()) {
            if (후보.부모식별자() != 부모.식별자()) {
                continue;
            }
            if (자식식별자 > 0 && 후보.식별자() != 자식식별자) {
                continue;
            }
            if (후보.status_VALUE() == Proses_status.Keluar_aplikasi) {
                int ukuran = (후보.Keluar_kod() & 0xff) << 8;
                Proses_Senarai.remove(Integer.valueOf(후보.식별자()));
                return ukuran;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proses_VALUE Cari_Proses(int 식별자) {
        return Proses_Senarai.get(Integer.valueOf(식별자));
    }

    private int 식별자할당() {
        return 다음식별자++;
    }
}
