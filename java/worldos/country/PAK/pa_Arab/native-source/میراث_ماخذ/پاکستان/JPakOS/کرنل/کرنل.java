// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.کرنل;

import پاکستان.JPakOS.기억공간.میموری_مینیجر;
import پاکستان.JPakOS.기억공간.صفحہ_مینیجر;
import پاکستان.JPakOS.입력.입력관리자;
import پاکستان.JPakOS.작업.عمل_قدر;
import پاکستان.JPakOS.작업.배정기;
import پاکستان.JPakOS.체계호출.체계호출;
import پاکستان.JPakOS.فائل_سسٹم.파일서술자표;
import پاکستان.JPakOS.فائل_سسٹم.فائل_سسٹم;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class کرنل {
    private final 하드웨어 آلہ_قدر;
    private final میموری_مینیجر 기억공간 = new میموری_مینیجر(32 * 1024 * 1024);
    private final صفحہ_مینیجر 쪽관리 = new صفحہ_مینیجر();
    private final فائل_سسٹم فائل_سسٹم = new فائل_سسٹم();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final عمل_قدر 첫과정;
    private final 체계호출 체계호출;

    public کرنل(하드웨어 آلہ_قدر) {
        this.آلہ_قدر = آلہ_قدر;
        첫과정 = 배정기.첫과정(new 파일서술자표(فائل_سسٹم));
        체계호출 = new 체계호출(فائل_سسٹم, 쪽관리, 배정기, آلہ_قدر, 입력관리);
    }

    public void چلاؤ() {
        آلہ_قدر.직렬출력("=== JPakOS 관리 کرنل_قدر ===\n");
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

    public فائل_سسٹم فائل_سسٹم() {
        return فائل_سسٹم;
    }

    public 배정기 배정기() {
        return 배정기;
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
