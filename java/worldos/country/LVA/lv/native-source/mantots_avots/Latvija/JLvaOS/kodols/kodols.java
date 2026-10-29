// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.kodols;

import Latvija.JLvaOS.atmiņa_reģions.기억공간관리자;
import Latvija.JLvaOS.atmiņa_reģions.쪽관리자;
import Latvija.JLvaOS.입력.입력관리자;
import Latvija.JLvaOS.작업.Process_VALUE;
import Latvija.JLvaOS.작업.plānotājs;
import Latvija.JLvaOS.체계호출.체계호출;
import Latvija.JLvaOS.failu_sistēma.파일서술자표;
import Latvija.JLvaOS.failu_sistēma.failu_sistēma;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kodols {
    private final 하드웨어 ierīce_VALUE;
    private final 기억공간관리자 atmiņa_reģions = new 기억공간관리자(32 * 1024 * 1024);
    private final 쪽관리자 쪽관리 = new 쪽관리자();
    private final failu_sistēma failu_sistēma = new failu_sistēma();
    private final plānotājs plānotājs = new plānotājs(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Process_VALUE 첫과정;
    private final 체계호출 체계호출;

    public kodols(하드웨어 ierīce_VALUE) {
        this.ierīce_VALUE = ierīce_VALUE;
        첫과정 = plānotājs.첫과정(new 파일서술자표(failu_sistēma));
        체계호출 = new 체계호출(failu_sistēma, 쪽관리, plānotājs, ierīce_VALUE, 입력관리);
    }

    public void Palaist() {
        ierīce_VALUE.직렬출력("=== JLvaOS 관리 kodols_VALUE ===\n");
    }

    public void Izpildīt_solis() {
        ierīce_VALUE.중앙처리장치멈춤();
    }

    public 기억공간관리자 atmiņa_reģions() {
        return atmiņa_reģions;
    }

    public 쪽관리자 쪽관리() {
        return 쪽관리;
    }

    public failu_sistēma failu_sistēma() {
        return failu_sistēma;
    }

    public plānotājs plānotājs() {
        return plānotājs;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Process_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
