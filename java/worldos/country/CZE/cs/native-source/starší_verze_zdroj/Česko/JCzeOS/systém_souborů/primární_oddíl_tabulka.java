// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.systém_souborů;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 výchozí_hodnota 분할 영역을 읽는다. */
public final class primární_oddíl_tabulka {
    public static final class oddíl_HODNOTA {
        private final int Druh_HODNOTA;
        private final long START_oddíl;
        private final long oddíl_POČET;

        oddíl_HODNOTA(int Druh_HODNOTA, long START_oddíl, long oddíl_POČET) {
            this.Druh_HODNOTA = Druh_HODNOTA;
            this.START_oddíl = START_oddíl;
            this.oddíl_POČET = oddíl_POČET;
        }

        public int Druh_HODNOTA() { return Druh_HODNOTA; }
        public long START_oddíl() { return START_oddíl; }
        public long oddíl_POČET() { return oddíl_POČET; }
    }

    public List<oddíl_HODNOTA> Čtení(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<oddíl_HODNOTA> VÝSLEDEK = new ArrayList<oddíl_HODNOTA>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int pozice = 446 + INDEX * 16;
            int Druh_HODNOTA = 첫구역[pozice + 4] & 0xff;
            long Spustit_2 = ve_formátu_Little_Endian_integer(첫구역, pozice + 8);
            long Velikost = ve_formátu_Little_Endian_integer(첫구역, pozice + 12);
            if (Druh_HODNOTA != 0 && Velikost != 0) {
                VÝSLEDEK.add(new oddíl_HODNOTA(Druh_HODNOTA, Spustit_2, Velikost));
            }
        }
        return Collections.unmodifiableList(VÝSLEDEK);
    }

    private long ve_formátu_Little_Endian_integer(byte[] data, int pozice) {
        return (data[pozice] & 0xffL)
                | ((data[pozice + 1] & 0xffL) << 8)
                | ((data[pozice + 2] & 0xffL) << 16)
                | ((data[pozice + 3] & 0xffL) << 24);
    }
}

