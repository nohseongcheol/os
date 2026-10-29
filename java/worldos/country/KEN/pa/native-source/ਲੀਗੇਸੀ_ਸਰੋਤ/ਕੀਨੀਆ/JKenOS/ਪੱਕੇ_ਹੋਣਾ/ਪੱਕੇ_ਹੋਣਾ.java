// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਕੀਨੀਆ.JKenOS.ਪੱਕੇ_ਹੋਣਾ;

import ਕੀਨੀਆ.JKenOS.기억공간.ਮੈਮਰੀ_ਪ੍ਰਬੰਧਕ;
import ਕੀਨੀਆ.JKenOS.기억공간.ਪੰਨਾ_ਪ੍ਰਬੰਧਕ;
import ਕੀਨੀਆ.JKenOS.입력.입력관리자;
import ਕੀਨੀਆ.JKenOS.작업.ਕਾਰਵਾਈ_ਕੀਮਤ;
import ਕੀਨੀਆ.JKenOS.작업.ਸ਼ੈਡਿਊਲਰ;
import ਕੀਨੀਆ.JKenOS.체계호출.체계호출;
import ਕੀਨੀਆ.JKenOS.ਫਾਈਲ_ਸਿਸਟਮ.파일서술자표;
import ਕੀਨੀਆ.JKenOS.ਫਾਈਲ_ਸਿਸਟਮ.ਫਾਈਲ_ਸਿਸਟਮ;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ਪੱਕੇ_ਹੋਣਾ {
    private final 하드웨어 ਤਜਵੀਜ_ਕੀਮਤ;
    private final ਮੈਮਰੀ_ਪ੍ਰਬੰਧਕ 기억공간 = new ਮੈਮਰੀ_ਪ੍ਰਬੰਧਕ(32 * 1024 * 1024);
    private final ਪੰਨਾ_ਪ੍ਰਬੰਧਕ 쪽관리 = new ਪੰਨਾ_ਪ੍ਰਬੰਧਕ();
    private final ਫਾਈਲ_ਸਿਸਟਮ ਫਾਈਲ_ਸਿਸਟਮ = new ਫਾਈਲ_ਸਿਸਟਮ();
    private final ਸ਼ੈਡਿਊਲਰ ਸ਼ੈਡਿਊਲਰ = new ਸ਼ੈਡਿਊਲਰ(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final ਕਾਰਵਾਈ_ਕੀਮਤ 첫과정;
    private final 체계호출 체계호출;

    public ਪੱਕੇ_ਹੋਣਾ(하드웨어 ਤਜਵੀਜ_ਕੀਮਤ) {
        this.ਤਜਵੀਜ_ਕੀਮਤ = ਤਜਵੀਜ_ਕੀਮਤ;
        첫과정 = ਸ਼ੈਡਿਊਲਰ.첫과정(new 파일서술자표(ਫਾਈਲ_ਸਿਸਟਮ));
        체계호출 = new 체계호출(ਫਾਈਲ_ਸਿਸਟਮ, 쪽관리, ਸ਼ੈਡਿਊਲਰ, ਤਜਵੀਜ_ਕੀਮਤ, 입력관리);
    }

    public void ਚਲਾਓ_2() {
        ਤਜਵੀਜ_ਕੀਮਤ.직렬출력("=== JKenOS 관리 ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ ===\n");
    }

    public void 한단계실행() {
        ਤਜਵੀਜ_ਕੀਮਤ.중앙처리장치멈춤();
    }

    public ਮੈਮਰੀ_ਪ੍ਰਬੰਧਕ 기억공간() {
        return 기억공간;
    }

    public ਪੰਨਾ_ਪ੍ਰਬੰਧਕ 쪽관리() {
        return 쪽관리;
    }

    public ਫਾਈਲ_ਸਿਸਟਮ ਫਾਈਲ_ਸਿਸਟਮ() {
        return ਫਾਈਲ_ਸਿਸਟਮ;
    }

    public ਸ਼ੈਡਿਊਲਰ ਸ਼ੈਡਿਊਲਰ() {
        return ਸ਼ੈਡਿਊਲਰ;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public ਕਾਰਵਾਈ_ਕੀਮਤ 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
