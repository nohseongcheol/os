// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.kjarni;

import Ísland.JIslOS.기억공간.Minni_stjórnandi;
import Ísland.JIslOS.기억공간.síða_stjórnandi;
import Ísland.JIslOS.입력.입력관리자;
import Ísland.JIslOS.작업.Ferli_VALUE;
import Ísland.JIslOS.작업.Verkraðari;
import Ísland.JIslOS.체계호출.체계호출;
import Ísland.JIslOS.skrárkerfi.파일서술자표;
import Ísland.JIslOS.skrárkerfi.skrárkerfi;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kjarni {
    private final 하드웨어 tæki_VALUE;
    private final Minni_stjórnandi 기억공간 = new Minni_stjórnandi(32 * 1024 * 1024);
    private final síða_stjórnandi 쪽관리 = new síða_stjórnandi();
    private final skrárkerfi skrárkerfi = new skrárkerfi();
    private final Verkraðari Verkraðari = new Verkraðari(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Ferli_VALUE 첫과정;
    private final 체계호출 체계호출;

    public kjarni(하드웨어 tæki_VALUE) {
        this.tæki_VALUE = tæki_VALUE;
        첫과정 = Verkraðari.첫과정(new 파일서술자표(skrárkerfi));
        체계호출 = new 체계호출(skrárkerfi, 쪽관리, Verkraðari, tæki_VALUE, 입력관리);
    }

    public void Keyra_2() {
        tæki_VALUE.직렬출력("=== JIslOS 관리 kjarni_VALUE ===\n");
    }

    public void keyra_skref() {
        tæki_VALUE.중앙처리장치멈춤();
    }

    public Minni_stjórnandi 기억공간() {
        return 기억공간;
    }

    public síða_stjórnandi 쪽관리() {
        return 쪽관리;
    }

    public skrárkerfi skrárkerfi() {
        return skrárkerfi;
    }

    public Verkraðari Verkraðari() {
        return Verkraðari;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Ferli_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
