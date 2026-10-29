// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.failų_sistema;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 numatytoji_reikšmė 분할 영역을 읽는다. */
public final class pirminis_skaidinys_lentelė {
    public static final class skaidinys_VALUE {
        private final int 종류;
        private final long Start_sekcija;
        private final long sekcija_COUNT;

        skaidinys_VALUE(int 종류, long Start_sekcija, long sekcija_COUNT) {
            this.종류 = 종류;
            this.Start_sekcija = Start_sekcija;
            this.sekcija_COUNT = sekcija_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_sekcija() { return Start_sekcija; }
        public long sekcija_COUNT() { return sekcija_COUNT; }
    }

    public List<skaidinys_VALUE> Skaitymas(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<skaidinys_VALUE> REZULTATAS = new ArrayList<skaidinys_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Pozicija = 446 + INDEX * 16;
            int 종류 = 첫구역[Pozicija + 4] & 0xff;
            long Paleisti = didėjantys_baitai_sveikasis_skaičius(첫구역, Pozicija + 8);
            long Dydis = didėjantys_baitai_sveikasis_skaičius(첫구역, Pozicija + 12);
            if (종류 != 0 && Dydis != 0) {
                REZULTATAS.add(new skaidinys_VALUE(종류, Paleisti, Dydis));
            }
        }
        return Collections.unmodifiableList(REZULTATAS);
    }

    private long didėjantys_baitai_sveikasis_skaičius(byte[] duomenys, int Pozicija) {
        return (duomenys[Pozicija] & 0xffL)
                | ((duomenys[Pozicija + 1] & 0xffL) << 8)
                | ((duomenys[Pozicija + 2] & 0xffL) << 16)
                | ((duomenys[Pozicija + 3] & 0xffL) << 24);
    }
}

