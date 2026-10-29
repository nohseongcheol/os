// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ಕರ್ನಲ್;

import ಭಾರತ.JIndOS.기억공간.ಮೆಮೊರಿ_ವ್ಯವಸ್ಥಾಪಕ;
import ಭಾರತ.JIndOS.기억공간.ಪುಟ_ವ್ಯವಸ್ಥಾಪಕ;
import ಭಾರತ.JIndOS.입력.입력관리자;
import ಭಾರತ.JIndOS.작업.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ;
import ಭಾರತ.JIndOS.작업.ಶೆಡ್ಯೂಲರ್;
import ಭಾರತ.JIndOS.체계호출.체계호출;
import ಭಾರತ.JIndOS.ಫೈಲ್_ಸಿಸ್ಟಂ.파일서술자표;
import ಭಾರತ.JIndOS.ಫೈಲ್_ಸಿಸ್ಟಂ.ಫೈಲ್_ಸಿಸ್ಟಂ;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ಕರ್ನಲ್ {
    private final 하드웨어 ಸಾಧನ_ಮೌಲ್ಯ;
    private final ಮೆಮೊರಿ_ವ್ಯವಸ್ಥಾಪಕ 기억공간 = new ಮೆಮೊರಿ_ವ್ಯವಸ್ಥಾಪಕ(32 * 1024 * 1024);
    private final ಪುಟ_ವ್ಯವಸ್ಥಾಪಕ 쪽관리 = new ಪುಟ_ವ್ಯವಸ್ಥಾಪಕ();
    private final ಫೈಲ್_ಸಿಸ್ಟಂ ಫೈಲ್_ಸಿಸ್ಟಂ = new ಫೈಲ್_ಸಿಸ್ಟಂ();
    private final ಶೆಡ್ಯೂಲರ್ ಶೆಡ್ಯೂಲರ್ = new ಶೆಡ್ಯೂಲರ್(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ 첫과정;
    private final 체계호출 체계호출;

    public ಕರ್ನಲ್(하드웨어 ಸಾಧನ_ಮೌಲ್ಯ) {
        this.ಸಾಧನ_ಮೌಲ್ಯ = ಸಾಧನ_ಮೌಲ್ಯ;
        첫과정 = ಶೆಡ್ಯೂಲರ್.첫과정(new 파일서술자표(ಫೈಲ್_ಸಿಸ್ಟಂ));
        체계호출 = new 체계호출(ಫೈಲ್_ಸಿಸ್ಟಂ, 쪽관리, ಶೆಡ್ಯೂಲರ್, ಸಾಧನ_ಮೌಲ್ಯ, 입력관리);
    }

    public void ಚಲಾಯಿಸು_2() {
        ಸಾಧನ_ಮೌಲ್ಯ.직렬출력("=== JIndOS 관리 ಕರ್ನಲ್_ಮೌಲ್ಯ ===\n");
    }

    public void 한단계실행() {
        ಸಾಧನ_ಮೌಲ್ಯ.중앙처리장치멈춤();
    }

    public ಮೆಮೊರಿ_ವ್ಯವಸ್ಥಾಪಕ 기억공간() {
        return 기억공간;
    }

    public ಪುಟ_ವ್ಯವಸ್ಥಾಪಕ 쪽관리() {
        return 쪽관리;
    }

    public ಫೈಲ್_ಸಿಸ್ಟಂ ಫೈಲ್_ಸಿಸ್ಟಂ() {
        return ಫೈಲ್_ಸಿಸ್ಟಂ;
    }

    public ಶೆಡ್ಯೂಲರ್ ಶೆಡ್ಯೂಲರ್() {
        return ಶೆಡ್ಯೂಲರ್;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
