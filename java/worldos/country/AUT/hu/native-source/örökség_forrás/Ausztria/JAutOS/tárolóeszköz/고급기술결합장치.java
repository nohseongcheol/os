// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ausztria.JAutOS.tárolóeszköz;

import java.util.Arrays;

/** ATA 28비트 Parancs 계층과 같은 512바이트 논리 szakasz_ÉRTÉK 장치다. */
public final class 고급기술결합장치 {
    public static final int szakasz_méretez = 512;
    private final byte[] adat;
    private final boolean írásvédett_ÉRTÉK;

    public 고급기술결합장치(int szakasz_DARAB, boolean írásvédett_ÉRTÉK) {
        if (szakasz_DARAB <= 0) {
            throw new IllegalArgumentException("szakasz_ÉRTÉK 수가 올바르지 않습니다.");
        }
        adat = new byte[Math.multiplyExact(szakasz_DARAB, szakasz_méretez)];
        this.írásvédett_ÉRTÉK = írásvédett_ÉRTÉK;
    }

    public int szakasz_DARAB() {
        return adat.length / szakasz_méretez;
    }

    public void Olvasás(int szakasz_INDEX, byte[] fogad_cél) {
        csekk_tartomány(szakasz_INDEX, fogad_cél);
        System.arraycopy(adat, szakasz_INDEX * szakasz_méretez, fogad_cél, 0, szakasz_méretez);
    }

    public void Írás(int szakasz_INDEX, byte[] 쓸자료) {
        if (írásvédett_ÉRTÉK) {
            throw new IllegalStateException("Olvasás 전용 장치입니다.");
        }
        csekk_tartomány(szakasz_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, adat, szakasz_INDEX * szakasz_méretez, szakasz_méretez);
    }

    public void töröl_bejegyzés() {
        if (írásvédett_ÉRTÉK) {
            throw new IllegalStateException("Olvasás 전용 장치입니다.");
        }
        Arrays.fill(adat, (byte) 0);
    }

    private void csekk_tartomány(int szakasz_INDEX, byte[] 임시공간) {
        if (szakasz_INDEX < 0 || szakasz_INDEX >= szakasz_DARAB() || 임시공간.length < szakasz_méretez) {
            throw new IllegalArgumentException("ATA szakasz_ÉRTÉK 범위가 올바르지 않습니다.");
        }
    }
}

