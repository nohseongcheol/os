// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عێراق.JIrqOS.کوورەک;

import عێراق.JIrqOS.기억공간.بیرگە_بەڕێوەبەر;
import عێراق.JIrqOS.기억공간.لاپەڕە_بەڕێوەبەر;
import عێراق.JIrqOS.입력.입력관리자;
import عێراق.JIrqOS.작업.پرۆسە_نرخ;
import عێراق.JIrqOS.작업.배정기;
import عێراق.JIrqOS.체계호출.체계호출;
import عێراق.JIrqOS.سیستمی_فایل.파일서술자표;
import عێراق.JIrqOS.سیستمی_فایل.سیستمی_فایل;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class کوورەک {
    private final 하드웨어 ئامێر_نرخ;
    private final بیرگە_بەڕێوەبەر 기억공간 = new بیرگە_بەڕێوەبەر(32 * 1024 * 1024);
    private final لاپەڕە_بەڕێوەبەر 쪽관리 = new لاپەڕە_بەڕێوەبەر();
    private final سیستمی_فایل سیستمی_فایل = new سیستمی_فایل();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final پرۆسە_نرخ 첫과정;
    private final 체계호출 체계호출;

    public کوورەک(하드웨어 ئامێر_نرخ) {
        this.ئامێر_نرخ = ئامێر_نرخ;
        첫과정 = 배정기.첫과정(new 파일서술자표(سیستمی_فایل));
        체계호출 = new 체계호출(سیستمی_فایل, 쪽관리, 배정기, ئامێر_نرخ, 입력관리);
    }

    public void ڕادان() {
        ئامێر_نرخ.직렬출력("=== JIrqOS 관리 کوورەک_نرخ ===\n");
    }

    public void 한단계실행() {
        ئامێر_نرخ.중앙처리장치멈춤();
    }

    public بیرگە_بەڕێوەبەر 기억공간() {
        return 기억공간;
    }

    public لاپەڕە_بەڕێوەبەر 쪽관리() {
        return 쪽관리;
    }

    public سیستمی_فایل سیستمی_فایل() {
        return سیستمی_فایل;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public پرۆسە_نرخ 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
