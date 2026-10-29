// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gammbi.JGmbOS.저장장치;

import java.util.Arrays;

/** ATA 28비트 ginol 계층과 같은 512바이트 논리 taƴre_njaru 장치다. */
public final class 고급기술결합장치 {
    public static final int taƴre_waylude_etannde = 512;
    private final byte[] keɓe;
    private final boolean janngotooɗo_tan_njaru;

    public 고급기술결합장치(int 구역수, boolean janngotooɗo_tan_njaru) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("taƴre_njaru 수가 올바르지 않습니다.");
        }
        keɓe = new byte[Math.multiplyExact(구역수, taƴre_waylude_etannde)];
        this.janngotooɗo_tan_njaru = janngotooɗo_tan_njaru;
    }

    public int 구역수() {
        return keɓe.length / taƴre_waylude_etannde;
    }

    public void 읽기(int taƴre_joopirdu, byte[] 받을곳) {
        범위확인(taƴre_joopirdu, 받을곳);
        System.arraycopy(keɓe, taƴre_joopirdu * taƴre_waylude_etannde, 받을곳, 0, taƴre_waylude_etannde);
    }

    public void winndude(int taƴre_joopirdu, byte[] 쓸자료) {
        if (janngotooɗo_tan_njaru) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(taƴre_joopirdu, 쓸자료);
        System.arraycopy(쓸자료, 0, keɓe, taƴre_joopirdu * taƴre_waylude_etannde, taƴre_waylude_etannde);
    }

    public void 지우기() {
        if (janngotooɗo_tan_njaru) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(keɓe, (byte) 0);
    }

    private void 범위확인(int taƴre_joopirdu, byte[] 임시공간) {
        if (taƴre_joopirdu < 0 || taƴre_joopirdu >= 구역수() || 임시공간.length < taƴre_waylude_etannde) {
            throw new IllegalArgumentException("ATA taƴre_njaru 범위가 올바르지 않습니다.");
        }
    }
}

