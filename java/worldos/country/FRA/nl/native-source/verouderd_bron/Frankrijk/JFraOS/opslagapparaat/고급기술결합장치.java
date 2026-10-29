// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frankrijk.JFraOS.opslagapparaat;

import java.util.Arrays;

/** ATA 28비트 opdracht 계층과 같은 512바이트 논리 sectie_WAARDE 장치다. */
public final class 고급기술결합장치 {
    public static final int sectie_formaat_wijzigen = 512;
    private final byte[] gegevens;
    private final boolean alleen_lezen_WAARDE;

    public 고급기술결합장치(int sectie_AANTAL, boolean alleen_lezen_WAARDE) {
        if (sectie_AANTAL <= 0) {
            throw new IllegalArgumentException("sectie_WAARDE 수가 올바르지 않습니다.");
        }
        gegevens = new byte[Math.multiplyExact(sectie_AANTAL, sectie_formaat_wijzigen)];
        this.alleen_lezen_WAARDE = alleen_lezen_WAARDE;
    }

    public int sectie_AANTAL() {
        return gegevens.length / sectie_formaat_wijzigen;
    }

    public void Lezen(int sectie_INDEX, byte[] ontvangen_doel) {
        cheque_bereik(sectie_INDEX, ontvangen_doel);
        System.arraycopy(gegevens, sectie_INDEX * sectie_formaat_wijzigen, ontvangen_doel, 0, sectie_formaat_wijzigen);
    }

    public void Schrijven(int sectie_INDEX, byte[] 쓸자료) {
        if (alleen_lezen_WAARDE) {
            throw new IllegalStateException("Lezen 전용 장치입니다.");
        }
        cheque_bereik(sectie_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, gegevens, sectie_INDEX * sectie_formaat_wijzigen, sectie_formaat_wijzigen);
    }

    public void wissen_invoer() {
        if (alleen_lezen_WAARDE) {
            throw new IllegalStateException("Lezen 전용 장치입니다.");
        }
        Arrays.fill(gegevens, (byte) 0);
    }

    private void cheque_bereik(int sectie_INDEX, byte[] 임시공간) {
        if (sectie_INDEX < 0 || sectie_INDEX >= sectie_AANTAL() || 임시공간.length < sectie_formaat_wijzigen) {
            throw new IllegalArgumentException("ATA sectie_WAARDE 범위가 올바르지 않습니다.");
        }
    }
}

