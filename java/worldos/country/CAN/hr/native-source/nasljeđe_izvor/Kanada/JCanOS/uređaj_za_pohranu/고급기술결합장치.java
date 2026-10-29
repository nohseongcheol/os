// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.uređaj_za_pohranu;

import java.util.Arrays;

/** ATA 28비트 Naredba 계층과 같은 512바이트 논리 sekcija_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int sekcija_promijeniti_veličinu = 512;
    private final byte[] podaci;
    private final boolean samo_za_čitanje_VALUE;

    public 고급기술결합장치(int sekcija_COUNT, boolean samo_za_čitanje_VALUE) {
        if (sekcija_COUNT <= 0) {
            throw new IllegalArgumentException("sekcija_VALUE 수가 올바르지 않습니다.");
        }
        podaci = new byte[Math.multiplyExact(sekcija_COUNT, sekcija_promijeniti_veličinu)];
        this.samo_za_čitanje_VALUE = samo_za_čitanje_VALUE;
    }

    public int sekcija_COUNT() {
        return podaci.length / sekcija_promijeniti_veličinu;
    }

    public void Čitaj(int sekcija_INDEX, byte[] primiti_odredište) {
        범위확인(sekcija_INDEX, primiti_odredište);
        System.arraycopy(podaci, sekcija_INDEX * sekcija_promijeniti_veličinu, primiti_odredište, 0, sekcija_promijeniti_veličinu);
    }

    public void Zapisuj(int sekcija_INDEX, byte[] 쓸자료) {
        if (samo_za_čitanje_VALUE) {
            throw new IllegalStateException("Čitaj 전용 장치입니다.");
        }
        범위확인(sekcija_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, podaci, sekcija_INDEX * sekcija_promijeniti_veličinu, sekcija_promijeniti_veličinu);
    }

    public void izbrisati_unos() {
        if (samo_za_čitanje_VALUE) {
            throw new IllegalStateException("Čitaj 전용 장치입니다.");
        }
        Arrays.fill(podaci, (byte) 0);
    }

    private void 범위확인(int sekcija_INDEX, byte[] 임시공간) {
        if (sekcija_INDEX < 0 || sekcija_INDEX >= sekcija_COUNT() || 임시공간.length < sekcija_promijeniti_veličinu) {
            throw new IllegalArgumentException("ATA sekcija_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

