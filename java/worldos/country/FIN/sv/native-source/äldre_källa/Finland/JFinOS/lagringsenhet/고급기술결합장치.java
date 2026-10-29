// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Finland.JFinOS.lagringsenhet;

import java.util.Arrays;

/** ATA 28비트 kommando 계층과 같은 512바이트 논리 avsnitt_värde 장치다. */
public final class 고급기술결합장치 {
    public static final int avsnitt_storlek = 512;
    private final byte[] data;
    private final boolean skrivskyddad_värde;

    public 고급기술결합장치(int avsnitt_ANTAL, boolean skrivskyddad_värde) {
        if (avsnitt_ANTAL <= 0) {
            throw new IllegalArgumentException("avsnitt_värde 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(avsnitt_ANTAL, avsnitt_storlek)];
        this.skrivskyddad_värde = skrivskyddad_värde;
    }

    public int avsnitt_ANTAL() {
        return data.length / avsnitt_storlek;
    }

    public void Läs(int avsnitt_INDEX, byte[] få_mål) {
        check_område(avsnitt_INDEX, få_mål);
        System.arraycopy(data, avsnitt_INDEX * avsnitt_storlek, få_mål, 0, avsnitt_storlek);
    }

    public void Skriv(int avsnitt_INDEX, byte[] 쓸자료) {
        if (skrivskyddad_värde) {
            throw new IllegalStateException("Läs 전용 장치입니다.");
        }
        check_område(avsnitt_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, data, avsnitt_INDEX * avsnitt_storlek, avsnitt_storlek);
    }

    public void radera_post() {
        if (skrivskyddad_värde) {
            throw new IllegalStateException("Läs 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void check_område(int avsnitt_INDEX, byte[] 임시공간) {
        if (avsnitt_INDEX < 0 || avsnitt_INDEX >= avsnitt_ANTAL() || 임시공간.length < avsnitt_storlek) {
            throw new IllegalArgumentException("ATA avsnitt_värde 범위가 올바르지 않습니다.");
        }
    }
}

