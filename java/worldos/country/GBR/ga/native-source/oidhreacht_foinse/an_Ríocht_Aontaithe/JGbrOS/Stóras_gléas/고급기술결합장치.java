// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.Stóras_gléas;

import java.util.Arrays;

/** ATA 28비트 Ordú 계층과 같은 512바이트 논리 rannán_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int rannán_socraigh_méid = 512;
    private final byte[] sonraí;
    private final boolean inléite_amháin_VALUE;

    public 고급기술결합장치(int rannán_COUNT, boolean inléite_amháin_VALUE) {
        if (rannán_COUNT <= 0) {
            throw new IllegalArgumentException("rannán_VALUE 수가 올바르지 않습니다.");
        }
        sonraí = new byte[Math.multiplyExact(rannán_COUNT, rannán_socraigh_méid)];
        this.inléite_amháin_VALUE = inléite_amháin_VALUE;
    }

    public int rannán_COUNT() {
        return sonraí.length / rannán_socraigh_méid;
    }

    public void Léigh(int rannán_INDEX, byte[] 받을곳) {
        범위확인(rannán_INDEX, 받을곳);
        System.arraycopy(sonraí, rannán_INDEX * rannán_socraigh_méid, 받을곳, 0, rannán_socraigh_méid);
    }

    public void Scríobh(int rannán_INDEX, byte[] 쓸자료) {
        if (inléite_amháin_VALUE) {
            throw new IllegalStateException("Léigh 전용 장치입니다.");
        }
        범위확인(rannán_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, sonraí, rannán_INDEX * rannán_socraigh_méid, rannán_socraigh_méid);
    }

    public void 지우기() {
        if (inléite_amháin_VALUE) {
            throw new IllegalStateException("Léigh 전용 장치입니다.");
        }
        Arrays.fill(sonraí, (byte) 0);
    }

    private void 범위확인(int rannán_INDEX, byte[] 임시공간) {
        if (rannán_INDEX < 0 || rannán_INDEX >= rannán_COUNT() || 임시공간.length < rannán_socraigh_méid) {
            throw new IllegalArgumentException("ATA rannán_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

