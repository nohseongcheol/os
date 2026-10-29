// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.ማከማቻ_መሳሪያ;

import java.util.Arrays;

/** ATA 28비트 ትእዛዝ 계층과 같은 512바이트 논리 ክፍል_እሴት 장치다. */
public final class 고급기술결합장치 {
    public static final int ክፍል_መጠን_ቀይር = 512;
    private final byte[] ውሂብ;
    private final boolean ተነባቢ_ብቻ_እሴት;

    public 고급기술결합장치(int 구역수, boolean ተነባቢ_ብቻ_እሴት) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("ክፍል_እሴት 수가 올바르지 않습니다.");
        }
        ውሂብ = new byte[Math.multiplyExact(구역수, ክፍል_መጠን_ቀይር)];
        this.ተነባቢ_ብቻ_እሴት = ተነባቢ_ብቻ_እሴት;
    }

    public int 구역수() {
        return ውሂብ.length / ክፍል_መጠን_ቀይር;
    }

    public void ማንበቢያ(int ክፍል_መረጃ_ጠቆመ, byte[] 받을곳) {
        범위확인(ክፍል_መረጃ_ጠቆመ, 받을곳);
        System.arraycopy(ውሂብ, ክፍል_መረጃ_ጠቆመ * ክፍል_መጠን_ቀይር, 받을곳, 0, ክፍል_መጠን_ቀይር);
    }

    public void መጻፊያ(int ክፍል_መረጃ_ጠቆመ, byte[] 쓸자료) {
        if (ተነባቢ_ብቻ_እሴት) {
            throw new IllegalStateException("ማንበቢያ 전용 장치입니다.");
        }
        범위확인(ክፍል_መረጃ_ጠቆመ, 쓸자료);
        System.arraycopy(쓸자료, 0, ውሂብ, ክፍል_መረጃ_ጠቆመ * ክፍል_መጠን_ቀይር, ክፍል_መጠን_ቀይር);
    }

    public void አስወግድ_ምዝግብ_c8dbc399() {
        if (ተነባቢ_ብቻ_እሴት) {
            throw new IllegalStateException("ማንበቢያ 전용 장치입니다.");
        }
        Arrays.fill(ውሂብ, (byte) 0);
    }

    private void 범위확인(int ክፍል_መረጃ_ጠቆመ, byte[] 임시공간) {
        if (ክፍል_መረጃ_ጠቆመ < 0 || ክፍል_መረጃ_ጠቆመ >= 구역수() || 임시공간.length < ክፍል_መጠን_ቀይር) {
            throw new IllegalArgumentException("ATA ክፍል_እሴት 범위가 올바르지 않습니다.");
        }
    }
}

