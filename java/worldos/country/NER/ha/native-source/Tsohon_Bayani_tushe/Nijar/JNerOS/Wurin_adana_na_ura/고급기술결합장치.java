// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijar.JNerOS.Wurin_adana_na_ura;

import java.util.Arrays;

/** ATA 28비트 Umarni 계층과 같은 512바이트 논리 Sashi_Daraja 장치다. */
public final class 고급기술결합장치 {
    public static final int Sashi_girma = 512;
    private final byte[] Tarin_bayani;
    private final boolean karanta_kawai_Daraja;

    public 고급기술결합장치(int 구역수, boolean karanta_kawai_Daraja) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("Sashi_Daraja 수가 올바르지 않습니다.");
        }
        Tarin_bayani = new byte[Math.multiplyExact(구역수, Sashi_girma)];
        this.karanta_kawai_Daraja = karanta_kawai_Daraja;
    }

    public int 구역수() {
        return Tarin_bayani.length / Sashi_girma;
    }

    public void Yi_Karatu(int Sashi_Indes, byte[] 받을곳) {
        범위확인(Sashi_Indes, 받을곳);
        System.arraycopy(Tarin_bayani, Sashi_Indes * Sashi_girma, 받을곳, 0, Sashi_girma);
    }

    public void Yi_Rubutu(int Sashi_Indes, byte[] 쓸자료) {
        if (karanta_kawai_Daraja) {
            throw new IllegalStateException("Yi_Karatu 전용 장치입니다.");
        }
        범위확인(Sashi_Indes, 쓸자료);
        System.arraycopy(쓸자료, 0, Tarin_bayani, Sashi_Indes * Sashi_girma, Sashi_girma);
    }

    public void share_Mashigar_bayanai() {
        if (karanta_kawai_Daraja) {
            throw new IllegalStateException("Yi_Karatu 전용 장치입니다.");
        }
        Arrays.fill(Tarin_bayani, (byte) 0);
    }

    private void 범위확인(int Sashi_Indes, byte[] 임시공간) {
        if (Sashi_Indes < 0 || Sashi_Indes >= 구역수() || 임시공간.length < Sashi_girma) {
            throw new IllegalArgumentException("ATA Sashi_Daraja 범위가 올바르지 않습니다.");
        }
    }
}

