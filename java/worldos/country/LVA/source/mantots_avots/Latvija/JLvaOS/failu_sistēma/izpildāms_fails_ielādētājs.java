// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.failu_sistēma;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Izpildīt_komanda 파일의 머리부와 적재 구역을 검증한다. */
public final class izpildāms_fails_ielādētājs {
    public static final class sadaļa_VALUE {
        private final int 종류;
        private final int atzīmēt_ar_karodziņu_VALUE;
        private final int adrese;
        private final int Fails_amats;
        private final int Izmērs;

        sadaļa_VALUE(int 종류, int atzīmēt_ar_karodziņu_VALUE, int adrese, int Fails_amats, int Izmērs) {
            this.종류 = 종류;
            this.atzīmēt_ar_karodziņu_VALUE = atzīmēt_ar_karodziņu_VALUE;
            this.adrese = adrese;
            this.Fails_amats = Fails_amats;
            this.Izmērs = Izmērs;
        }

        public int 종류() {
            return 종류;
        }

        public int atzīmēt_ar_karodziņu_VALUE() {
            return atzīmēt_ar_karodziņu_VALUE;
        }

        public int adrese() {
            return adrese;
        }

        public int Fails_amats() {
            return Fails_amats;
        }

        public int Izmērs() {
            return Izmērs;
        }
    }

    public static final class IMAGE {
        private final int Sākt_adrese;
        private final List<sadaļa_VALUE> 구역들;

        IMAGE(int Sākt_adrese, List<sadaļa_VALUE> 구역들) {
            this.Sākt_adrese = Sākt_adrese;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Sākt_adrese() {
            return Sākt_adrese;
        }

        public List<sadaļa_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] dati) {
        if (dati == null || dati.length < 52
                || dati[0] != 0x7f || dati[1] != 'E' || dati[2] != 'L' || dati[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (dati[4] != 1 || dati[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Sākt_adrese = parsēt_vesels_skaitlis(dati, 24);
        int sadaļa_tabula_amats = parsēt_vesels_skaitlis(dati, 32);
        int sadaļa_ievade_mainīt_izmērus = 짧은정수읽기(dati, 46);
        int sadaļa_COUNT = 짧은정수읽기(dati, 48);
        if (sadaļa_ievade_mainīt_izmērus < 40 || sadaļa_tabula_amats < 0
                || (long) sadaļa_tabula_amats + (long) sadaļa_ievade_mainīt_izmērus * sadaļa_COUNT > dati.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sadaļa_VALUE> 구역들 = new ArrayList<sadaļa_VALUE>();
        for (int INDEX = 0; INDEX < sadaļa_COUNT; INDEX++) {
            int Novietojums = sadaļa_tabula_amats + INDEX * sadaļa_ievade_mainīt_izmērus;
            int 종류 = parsēt_vesels_skaitlis(dati, Novietojums + 4);
            int atzīmēt_ar_karodziņu_VALUE = parsēt_vesels_skaitlis(dati, Novietojums + 8);
            int adrese = parsēt_vesels_skaitlis(dati, Novietojums + 12);
            int Fails_amats = parsēt_vesels_skaitlis(dati, Novietojums + 16);
            int Izmērs = parsēt_vesels_skaitlis(dati, Novietojums + 20);
            if (Izmērs < 0 || (종류 != 8 && ((long) Fails_amats + Izmērs > dati.length || Fails_amats < 0))) {
                throw new IllegalArgumentException("ELF sadaļa_VALUE dati 범위가 올바르지 않습니다.");
            }
            구역들.add(new sadaļa_VALUE(종류, atzīmēt_ar_karodziņu_VALUE, adrese, Fails_amats, Izmērs));
        }
        return new IMAGE(Sākt_adrese, 구역들);
    }

    private int parsēt_vesels_skaitlis(byte[] dati, int Novietojums) {
        if (Novietojums < 0 || Novietojums > dati.length - 4) {
            throw new IllegalArgumentException("ELF vesels_skaitlis 범위를 벗어났습니다.");
        }
        return (dati[Novietojums] & 0xff)
                | ((dati[Novietojums + 1] & 0xff) << 8)
                | ((dati[Novietojums + 2] & 0xff) << 16)
                | ((dati[Novietojums + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] dati, int Novietojums) {
        if (Novietojums < 0 || Novietojums > dati.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 vesels_skaitlis 범위를 벗어났습니다.");
        }
        return (dati[Novietojums] & 0xff) | ((dati[Novietojums + 1] & 0xff) << 8);
    }
}
