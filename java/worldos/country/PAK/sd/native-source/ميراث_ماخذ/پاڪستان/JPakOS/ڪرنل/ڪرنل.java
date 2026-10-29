// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاڪستان.JPakOS.ڪرنل;

import پاڪستان.JPakOS.기억공간.ميموري_مئنيجر;
import پاڪستان.JPakOS.기억공간.صفحو_مئنيجر;
import پاڪستان.JPakOS.입력.입력관리자;
import پاڪستان.JPakOS.작업.عمل_قدر;
import پاڪستان.JPakOS.작업.배정기;
import پاڪستان.JPakOS.체계호출.체계호출;
import پاڪستان.JPakOS.فائل_سسٽم.파일서술자표;
import پاڪستان.JPakOS.فائل_سسٽم.فائل_سسٽم;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ڪرنل {
    private final 하드웨어 آلو_قدر;
    private final ميموري_مئنيجر 기억공간 = new ميموري_مئنيجر(32 * 1024 * 1024);
    private final صفحو_مئنيجر 쪽관리 = new صفحو_مئنيجر();
    private final فائل_سسٽم فائل_سسٽم = new فائل_سسٽم();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final عمل_قدر 첫과정;
    private final 체계호출 체계호출;

    public ڪرنل(하드웨어 آلو_قدر) {
        this.آلو_قدر = آلو_قدر;
        첫과정 = 배정기.첫과정(new 파일서술자표(فائل_سسٽم));
        체계호출 = new 체계호출(فائل_سسٽم, 쪽관리, 배정기, آلو_قدر, 입력관리);
    }

    public void هلائڻ() {
        آلو_قدر.직렬출력("=== JPakOS 관리 ڪرنل_قدر ===\n");
    }

    public void 한단계실행() {
        آلو_قدر.중앙처리장치멈춤();
    }

    public ميموري_مئنيجر 기억공간() {
        return 기억공간;
    }

    public صفحو_مئنيجر 쪽관리() {
        return 쪽관리;
    }

    public فائل_سسٽم فائل_سسٽم() {
        return فائل_سسٽم;
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
