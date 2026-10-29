// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Späicher_Mobil;

import java.util.Arrays;

/** ATA 28비트 Befeel 계층과 같은 512바이트 논리 Beräich_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int Beräich_d_Gréisst_veränneren = 512;
    private final byte[] Daten;
    private final boolean schreifgeschützt_VALUE;

    public 고급기술결합장치(int Beräich_COUNT, boolean schreifgeschützt_VALUE) {
        if (Beräich_COUNT <= 0) {
            throw new IllegalArgumentException("Beräich_VALUE 수가 올바르지 않습니다.");
        }
        Daten = new byte[Math.multiplyExact(Beräich_COUNT, Beräich_d_Gréisst_veränneren)];
        this.schreifgeschützt_VALUE = schreifgeschützt_VALUE;
    }

    public int Beräich_COUNT() {
        return Daten.length / Beräich_d_Gréisst_veränneren;
    }

    public void 읽기(int Beräich_INDEX, byte[] 받을곳) {
        범위확인(Beräich_INDEX, 받을곳);
        System.arraycopy(Daten, Beräich_INDEX * Beräich_d_Gréisst_veränneren, 받을곳, 0, Beräich_d_Gréisst_veränneren);
    }

    public void schreiwen(int Beräich_INDEX, byte[] 쓸자료) {
        if (schreifgeschützt_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(Beräich_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, Daten, Beräich_INDEX * Beräich_d_Gréisst_veränneren, Beräich_d_Gréisst_veränneren);
    }

    public void 지우기() {
        if (schreifgeschützt_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(Daten, (byte) 0);
    }

    private void 범위확인(int Beräich_INDEX, byte[] 임시공간) {
        if (Beräich_INDEX < 0 || Beräich_INDEX >= Beräich_COUNT() || 임시공간.length < Beräich_d_Gréisst_veränneren) {
            throw new IllegalArgumentException("ATA Beräich_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

