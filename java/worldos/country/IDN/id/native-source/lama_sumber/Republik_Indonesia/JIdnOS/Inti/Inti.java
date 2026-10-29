// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Republik_Indonesia.JIdnOS.Inti;

import Republik_Indonesia.JIdnOS.Memori_wilayah.Memori_Manajer;
import Republik_Indonesia.JIdnOS.Memori_wilayah.halaman_Manajer;
import Republik_Indonesia.JIdnOS.입력.입력관리자;
import Republik_Indonesia.JIdnOS.작업.Proses_VALUE;
import Republik_Indonesia.JIdnOS.작업.Penjadwal;
import Republik_Indonesia.JIdnOS.panggilan_sistem.panggilan_sistem;
import Republik_Indonesia.JIdnOS.sistem_berkas.파일서술자표;
import Republik_Indonesia.JIdnOS.sistem_berkas.sistem_berkas;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class Inti {
    private final 하드웨어 Ponsel_VALUE;
    private final Memori_Manajer Memori_wilayah = new Memori_Manajer(32 * 1024 * 1024);
    private final halaman_Manajer 쪽관리 = new halaman_Manajer();
    private final sistem_berkas sistem_berkas = new sistem_berkas();
    private final Penjadwal Penjadwal = new Penjadwal(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proses_VALUE 첫과정;
    private final panggilan_sistem panggilan_sistem;

    public Inti(하드웨어 Ponsel_VALUE) {
        this.Ponsel_VALUE = Ponsel_VALUE;
        첫과정 = Penjadwal.첫과정(new 파일서술자표(sistem_berkas));
        panggilan_sistem = new panggilan_sistem(sistem_berkas, 쪽관리, Penjadwal, Ponsel_VALUE, 입력관리);
    }

    public void jalankan() {
        Ponsel_VALUE.직렬출력("=== JIdnOS 관리 kernel_VALUE ===\n");
    }

    public void Jalankan_langkah() {
        Ponsel_VALUE.중앙처리장치멈춤();
    }

    public Memori_Manajer Memori_wilayah() {
        return Memori_wilayah;
    }

    public halaman_Manajer 쪽관리() {
        return 쪽관리;
    }

    public sistem_berkas sistem_berkas() {
        return sistem_berkas;
    }

    public Penjadwal Penjadwal() {
        return Penjadwal;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Proses_VALUE 첫과정() {
        return 첫과정;
    }

    public panggilan_sistem panggilan_sistem() {
        return panggilan_sistem;
    }
}
