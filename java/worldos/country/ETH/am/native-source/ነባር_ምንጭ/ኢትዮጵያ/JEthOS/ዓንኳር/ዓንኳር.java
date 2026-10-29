// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.ዓንኳር;

import ኢትዮጵያ.JEthOS.기억공간.ማስቀመጫ_አስተዳዳሪ;
import ኢትዮጵያ.JEthOS.기억공간.ገጽ_አስተዳዳሪ;
import ኢትዮጵያ.JEthOS.입력.입력관리자;
import ኢትዮጵያ.JEthOS.작업.ሂደት_እሴት;
import ኢትዮጵያ.JEthOS.작업.መርሀግብር_ኣውጭ;
import ኢትዮጵያ.JEthOS.체계호출.체계호출;
import ኢትዮጵያ.JEthOS.የፋይል_ስርዓት.파일서술자표;
import ኢትዮጵያ.JEthOS.የፋይል_ስርዓት.የፋይል_ስርዓት;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ዓንኳር {
    private final 하드웨어 መሳሪያ_እሴት;
    private final ማስቀመጫ_አስተዳዳሪ 기억공간 = new ማስቀመጫ_አስተዳዳሪ(32 * 1024 * 1024);
    private final ገጽ_አስተዳዳሪ 쪽관리 = new ገጽ_አስተዳዳሪ();
    private final የፋይል_ስርዓት የፋይል_ስርዓት = new የፋይል_ስርዓት();
    private final መርሀግብር_ኣውጭ መርሀግብር_ኣውጭ = new መርሀግብር_ኣውጭ(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final ሂደት_እሴት 첫과정;
    private final 체계호출 체계호출;

    public ዓንኳር(하드웨어 መሳሪያ_እሴት) {
        this.መሳሪያ_እሴት = መሳሪያ_እሴት;
        첫과정 = መርሀግብር_ኣውጭ.첫과정(new 파일서술자표(የፋይል_ስርዓት));
        체계호출 = new 체계호출(የፋይል_ስርዓት, 쪽관리, መርሀግብር_ኣውጭ, መሳሪያ_እሴት, 입력관리);
    }

    public void ማስኬጃ() {
        መሳሪያ_እሴት.직렬출력("=== JEthOS 관리 ዓንኳር_እሴት ===\n");
    }

    public void 한단계실행() {
        መሳሪያ_እሴት.중앙처리장치멈춤();
    }

    public ማስቀመጫ_አስተዳዳሪ 기억공간() {
        return 기억공간;
    }

    public ገጽ_አስተዳዳሪ 쪽관리() {
        return 쪽관리;
    }

    public የፋይል_ስርዓት የፋይል_ስርዓት() {
        return የፋይል_ስርዓት;
    }

    public መርሀግብር_ኣውጭ መርሀግብር_ኣውጭ() {
        return መርሀግብር_ኣውጭ;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public ሂደት_እሴት 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
