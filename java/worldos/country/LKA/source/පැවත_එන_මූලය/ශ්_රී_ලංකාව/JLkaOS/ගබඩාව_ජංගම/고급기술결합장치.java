// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.ගබඩාව_ජංගම;

import java.util.Arrays;

/** ATA 28비트 විධානය 계층과 같은 512바이트 논리 අංශය_අගය 장치다. */
public final class 고급기술결합장치 {
    public static final int අංශය_ප්_රමාණනය = 512;
    private final byte[] දත්ත;
    private final boolean කියවීම්_පමණි_අගය;

    public 고급기술결합장치(int 구역수, boolean කියවීම්_පමණි_අගය) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("අංශය_අගය 수가 올바르지 않습니다.");
        }
        දත්ත = new byte[Math.multiplyExact(구역수, අංශය_ප්_රමාණනය)];
        this.කියවීම්_පමණි_අගය = කියවීම්_පමණි_අගය;
    }

    public int 구역수() {
        return දත්ත.length / අංශය_ප්_රමාණනය;
    }

    public void කියවීම(int අංශය_සූචිය, byte[] 받을곳) {
        범위확인(අංශය_සූචිය, 받을곳);
        System.arraycopy(දත්ත, අංශය_සූචිය * අංශය_ප්_රමාණනය, 받을곳, 0, අංශය_ප්_රමාණනය);
    }

    public void ලිවීම(int අංශය_සූචිය, byte[] 쓸자료) {
        if (කියවීම්_පමණි_අගය) {
            throw new IllegalStateException("කියවීම 전용 장치입니다.");
        }
        범위확인(අංශය_සූචිය, 쓸자료);
        System.arraycopy(쓸자료, 0, දත්ත, අංශය_සූචිය * අංශය_ප්_රමාණනය, අංශය_ප්_රමාණනය);
    }

    public void 지우기() {
        if (කියවීම්_පමණි_අගය) {
            throw new IllegalStateException("කියවීම 전용 장치입니다.");
        }
        Arrays.fill(දත්ත, (byte) 0);
    }

    private void 범위확인(int අංශය_සූචිය, byte[] 임시공간) {
        if (අංශය_සූචිය < 0 || අංශය_සූචිය >= 구역수() || 임시공간.length < අංශය_ප්_රමාණනය) {
            throw new IllegalArgumentException("ATA අංශය_අගය 범위가 올바르지 않습니다.");
        }
    }
}

