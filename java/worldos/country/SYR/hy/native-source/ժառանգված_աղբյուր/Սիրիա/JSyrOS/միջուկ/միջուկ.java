// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Սիրիա.JSyrOS.միջուկ;

import Սիրիա.JSyrOS.기억공간.Հիշողություն_կառավարիչ;
import Սիրիա.JSyrOS.기억공간.էջ_կառավարիչ;
import Սիրիա.JSyrOS.입력.입력관리자;
import Սիրիա.JSyrOS.작업.Ընթացք_արժեք;
import Սիրիա.JSyrOS.작업.Ծրագրող;
import Սիրիա.JSyrOS.체계호출.체계호출;
import Սիրիա.JSyrOS.նիշքային_համակարգ.파일서술자표;
import Սիրիա.JSyrOS.նիշքային_համակարգ.նիշքային_համակարգ;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class միջուկ {
    private final 하드웨어 սարք_արժեք;
    private final Հիշողություն_կառավարիչ 기억공간 = new Հիշողություն_կառավարիչ(32 * 1024 * 1024);
    private final էջ_կառավարիչ 쪽관리 = new էջ_կառավարիչ();
    private final նիշքային_համակարգ նիշքային_համակարգ = new նիշքային_համակարգ();
    private final Ծրագրող Ծրագրող = new Ծրագրող(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Ընթացք_արժեք 첫과정;
    private final 체계호출 체계호출;

    public միջուկ(하드웨어 սարք_արժեք) {
        this.սարք_արժեք = սարք_արժեք;
        첫과정 = Ծրագրող.첫과정(new 파일서술자표(նիշքային_համակարգ));
        체계호출 = new 체계호출(նիշքային_համակարգ, 쪽관리, Ծրագրող, սարք_արժեք, 입력관리);
    }

    public void Գործարկել() {
        սարք_արժեք.직렬출력("=== JSyrOS 관리 միջուկ_արժեք ===\n");
    }

    public void 한단계실행() {
        սարք_արժեք.중앙처리장치멈춤();
    }

    public Հիշողություն_կառավարիչ 기억공간() {
        return 기억공간;
    }

    public էջ_կառավարիչ 쪽관리() {
        return 쪽관리;
    }

    public նիշքային_համակարգ նիշքային_համակարգ() {
        return նիշքային_համակարգ;
    }

    public Ծրագրող Ծրագրող() {
        return Ծրագրող;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Ընթացք_արժեք 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
