// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Grønland.JGrlOS.lagerenhed;

import java.util.Arrays;

/** ATA 28비트 Kommando 계층과 같은 512바이트 논리 sektion_VÆRDI 장치다. */
public final class 고급기술결합장치 {
    public static final int sektion_tilpasse_størrelse = 512;
    private final byte[] data;
    private final boolean skrivebeskyttet_VÆRDI;

    public 고급기술결합장치(int sektion_TÆL, boolean skrivebeskyttet_VÆRDI) {
        if (sektion_TÆL <= 0) {
            throw new IllegalArgumentException("sektion_VÆRDI 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(sektion_TÆL, sektion_tilpasse_størrelse)];
        this.skrivebeskyttet_VÆRDI = skrivebeskyttet_VÆRDI;
    }

    public int sektion_TÆL() {
        return data.length / sektion_tilpasse_størrelse;
    }

    public void Læse(int sektion_INDEKS, byte[] modtage_destination) {
        check_område(sektion_INDEKS, modtage_destination);
        System.arraycopy(data, sektion_INDEKS * sektion_tilpasse_størrelse, modtage_destination, 0, sektion_tilpasse_størrelse);
    }

    public void Skrive(int sektion_INDEKS, byte[] 쓸자료) {
        if (skrivebeskyttet_VÆRDI) {
            throw new IllegalStateException("Læse 전용 장치입니다.");
        }
        check_område(sektion_INDEKS, 쓸자료);
        System.arraycopy(쓸자료, 0, data, sektion_INDEKS * sektion_tilpasse_størrelse, sektion_tilpasse_størrelse);
    }

    public void slette_post() {
        if (skrivebeskyttet_VÆRDI) {
            throw new IllegalStateException("Læse 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void check_område(int sektion_INDEKS, byte[] 임시공간) {
        if (sektion_INDEKS < 0 || sektion_INDEKS >= sektion_TÆL() || 임시공간.length < sektion_tilpasse_størrelse) {
            throw new IllegalArgumentException("ATA sektion_VÆRDI 범위가 올바르지 않습니다.");
        }
    }
}

