// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Rumunija.JRouOS.uređaj_za_skladištenje;

import java.util.Arrays;

/** ATA 28비트 komanda 계층과 같은 512바이트 논리 odeljak_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int odeljak_promeniti_veličinu = 512;
    private final byte[] podaci;
    private final boolean samo_za_čitanje_VALUE;

    public 고급기술결합장치(int odeljak_COUNT, boolean samo_za_čitanje_VALUE) {
        if (odeljak_COUNT <= 0) {
            throw new IllegalArgumentException("odeljak_VALUE 수가 올바르지 않습니다.");
        }
        podaci = new byte[Math.multiplyExact(odeljak_COUNT, odeljak_promeniti_veličinu)];
        this.samo_za_čitanje_VALUE = samo_za_čitanje_VALUE;
    }

    public int odeljak_COUNT() {
        return podaci.length / odeljak_promeniti_veličinu;
    }

    public void 읽기(int odeljak_INDEX, byte[] primiti_odredište) {
        proveriti_opseg(odeljak_INDEX, primiti_odredište);
        System.arraycopy(podaci, odeljak_INDEX * odeljak_promeniti_veličinu, primiti_odredište, 0, odeljak_promeniti_veličinu);
    }

    public void 쓰기(int odeljak_INDEX, byte[] 쓸자료) {
        if (samo_za_čitanje_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        proveriti_opseg(odeljak_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, podaci, odeljak_INDEX * odeljak_promeniti_veličinu, odeljak_promeniti_veličinu);
    }

    public void obrisati_stavka() {
        if (samo_za_čitanje_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(podaci, (byte) 0);
    }

    private void proveriti_opseg(int odeljak_INDEX, byte[] 임시공간) {
        if (odeljak_INDEX < 0 || odeljak_INDEX >= odeljak_COUNT() || 임시공간.length < odeljak_promeniti_veličinu) {
            throw new IllegalArgumentException("ATA odeljak_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

