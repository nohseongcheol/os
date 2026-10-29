// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.stòras_uidheam;

import java.util.Arrays;

/** ATA 28비트 àithne 계층과 같은 512바이트 논리 earrann_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int earrann_atharraich_am_meud = 512;
    private final byte[] dàta;
    private final boolean ri_leughadh_a_mhàin_VALUE;

    public 고급기술결합장치(int earrann_COUNT, boolean ri_leughadh_a_mhàin_VALUE) {
        if (earrann_COUNT <= 0) {
            throw new IllegalArgumentException("earrann_VALUE 수가 올바르지 않습니다.");
        }
        dàta = new byte[Math.multiplyExact(earrann_COUNT, earrann_atharraich_am_meud)];
        this.ri_leughadh_a_mhàin_VALUE = ri_leughadh_a_mhàin_VALUE;
    }

    public int earrann_COUNT() {
        return dàta.length / earrann_atharraich_am_meud;
    }

    public void 읽기(int earrann_INDEX, byte[] 받을곳) {
        범위확인(earrann_INDEX, 받을곳);
        System.arraycopy(dàta, earrann_INDEX * earrann_atharraich_am_meud, 받을곳, 0, earrann_atharraich_am_meud);
    }

    public void sgrìobh(int earrann_INDEX, byte[] 쓸자료) {
        if (ri_leughadh_a_mhàin_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(earrann_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, dàta, earrann_INDEX * earrann_atharraich_am_meud, earrann_atharraich_am_meud);
    }

    public void 지우기() {
        if (ri_leughadh_a_mhàin_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(dàta, (byte) 0);
    }

    private void 범위확인(int earrann_INDEX, byte[] 임시공간) {
        if (earrann_INDEX < 0 || earrann_INDEX >= earrann_COUNT() || 임시공간.length < earrann_atharraich_am_meud) {
            throw new IllegalArgumentException("ATA earrann_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

