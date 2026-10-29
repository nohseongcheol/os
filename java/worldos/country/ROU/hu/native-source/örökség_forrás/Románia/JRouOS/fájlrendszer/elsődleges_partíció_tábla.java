// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Románia.JRouOS.fájlrendszer;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 alapértelmezett_érték 분할 영역을 읽는다. */
public final class elsődleges_partíció_tábla {
    public static final class partíció_ÉRTÉK {
        private final int Altípus_ÉRTÉK;
        private final long START_szakasz;
        private final long szakasz_DARAB;

        partíció_ÉRTÉK(int Altípus_ÉRTÉK, long START_szakasz, long szakasz_DARAB) {
            this.Altípus_ÉRTÉK = Altípus_ÉRTÉK;
            this.START_szakasz = START_szakasz;
            this.szakasz_DARAB = szakasz_DARAB;
        }

        public int Altípus_ÉRTÉK() { return Altípus_ÉRTÉK; }
        public long START_szakasz() { return START_szakasz; }
        public long szakasz_DARAB() { return szakasz_DARAB; }
    }

    public List<partíció_ÉRTÉK> Olvasás(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partíció_ÉRTÉK> KR = new ArrayList<partíció_ÉRTÉK>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Pozíció = 446 + INDEX * 16;
            int Altípus_ÉRTÉK = 첫구역[Pozíció + 4] & 0xff;
            long Futtatás = növekvő_bájtsorrendű_egész_szám(첫구역, Pozíció + 8);
            long Méret = növekvő_bájtsorrendű_egész_szám(첫구역, Pozíció + 12);
            if (Altípus_ÉRTÉK != 0 && Méret != 0) {
                KR.add(new partíció_ÉRTÉK(Altípus_ÉRTÉK, Futtatás, Méret));
            }
        }
        return Collections.unmodifiableList(KR);
    }

    private long növekvő_bájtsorrendű_egész_szám(byte[] adat, int Pozíció) {
        return (adat[Pozíció] & 0xffL)
                | ((adat[Pozíció + 1] & 0xffL) << 8)
                | ((adat[Pozíció + 2] & 0xffL) << 16)
                | ((adat[Pozíció + 3] & 0xffL) << 24);
    }
}

