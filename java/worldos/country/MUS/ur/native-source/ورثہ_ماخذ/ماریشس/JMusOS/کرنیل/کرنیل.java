// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ماریشس.JMusOS.کرنیل;

import ماریشس.JMusOS.기억공간.میموری_مینیجر;
import ماریشس.JMusOS.기억공간.صفحہ_مینیجر;
import ماریشس.JMusOS.입력.입력관리자;
import ماریشس.JMusOS.작업.عمل_قدر;
import ماریشس.JMusOS.작업.میقات_کار;
import ماریشس.JMusOS.체계호출.체계호출;
import ماریشس.JMusOS.فائل_نظام.파일서술자표;
import ماریشس.JMusOS.فائل_نظام.فائل_نظام;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class کرنیل {
    private final 하드웨어 آلہ_قدر;
    private final میموری_مینیجر 기억공간 = new میموری_مینیجر(32 * 1024 * 1024);
    private final صفحہ_مینیجر 쪽관리 = new صفحہ_مینیجر();
    private final فائل_نظام فائل_نظام = new فائل_نظام();
    private final میقات_کار میقات_کار = new میقات_کار(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final عمل_قدر 첫과정;
    private final 체계호출 체계호출;

    public کرنیل(하드웨어 آلہ_قدر) {
        this.آلہ_قدر = آلہ_قدر;
        첫과정 = میقات_کار.첫과정(new 파일서술자표(فائل_نظام));
        체계호출 = new 체계호출(فائل_نظام, 쪽관리, میقات_کار, آلہ_قدر, 입력관리);
    }

    public void چلائیں() {
        آلہ_قدر.직렬출력("=== JMusOS 관리 کرنیل_قدر ===\n");
    }

    public void 한단계실행() {
        آلہ_قدر.중앙처리장치멈춤();
    }

    public میموری_مینیجر 기억공간() {
        return 기억공간;
    }

    public صفحہ_مینیجر 쪽관리() {
        return 쪽관리;
    }

    public فائل_نظام فائل_نظام() {
        return فائل_نظام;
    }

    public میقات_کار میقات_کار() {
        return میقات_کار;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public عمل_قدر 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
