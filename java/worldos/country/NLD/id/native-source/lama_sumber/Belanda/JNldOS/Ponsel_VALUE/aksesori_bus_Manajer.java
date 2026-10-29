// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.Ponsel_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI Ponsel_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class aksesori_bus_Manajer {
    public static final class Ponsel_VALUE {
        private final int vendor_pengidentifikasi;
        private final int Ponsel_pengidentifikasi;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public Ponsel_VALUE(int vendor_pengidentifikasi, int Ponsel_pengidentifikasi, int 입출력바탕, int 개입중단번호) {
            this.vendor_pengidentifikasi = vendor_pengidentifikasi;
            this.Ponsel_pengidentifikasi = Ponsel_pengidentifikasi;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int vendor_pengidentifikasi() { return vendor_pengidentifikasi; }
        public int Ponsel_pengidentifikasi() { return Ponsel_pengidentifikasi; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<Ponsel_VALUE> Perangkat_Daftar = new ArrayList<Ponsel_VALUE>();

    public void 발견(Ponsel_VALUE Ponsel_VALUE) {
        Perangkat_Daftar.add(Ponsel_VALUE);
    }

    public List<Ponsel_VALUE> Perangkat_Daftar() {
        return Collections.unmodifiableList(Perangkat_Daftar);
    }

    public Ponsel_VALUE FIND_entri(int vendor_pengidentifikasi, int Ponsel_pengidentifikasi) {
        for (Ponsel_VALUE 후보 : Perangkat_Daftar) {
            if (후보.vendor_pengidentifikasi == vendor_pengidentifikasi && 후보.Ponsel_pengidentifikasi == Ponsel_pengidentifikasi) {
                return 후보;
            }
        }
        return null;
    }
}

