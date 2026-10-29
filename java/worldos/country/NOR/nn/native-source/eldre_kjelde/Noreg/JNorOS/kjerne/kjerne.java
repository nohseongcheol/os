// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.kjerne;

import Noreg.JNorOS.기억공간.Minne_leiar;
import Noreg.JNorOS.기억공간.side_leiar;
import Noreg.JNorOS.입력.입력관리자;
import Noreg.JNorOS.작업.Prosess_VALUE;
import Noreg.JNorOS.작업.Planleggjar;
import Noreg.JNorOS.체계호출.체계호출;
import Noreg.JNorOS.filsystem.파일서술자표;
import Noreg.JNorOS.filsystem.filsystem;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kjerne {
    private final 하드웨어 mobil_VALUE;
    private final Minne_leiar 기억공간 = new Minne_leiar(32 * 1024 * 1024);
    private final side_leiar 쪽관리 = new side_leiar();
    private final filsystem filsystem = new filsystem();
    private final Planleggjar Planleggjar = new Planleggjar(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Prosess_VALUE 첫과정;
    private final 체계호출 체계호출;

    public kjerne(하드웨어 mobil_VALUE) {
        this.mobil_VALUE = mobil_VALUE;
        첫과정 = Planleggjar.첫과정(new 파일서술자표(filsystem));
        체계호출 = new 체계호출(filsystem, 쪽관리, Planleggjar, mobil_VALUE, 입력관리);
    }

    public void Køyr_2() {
        mobil_VALUE.직렬출력("=== JNorOS 관리 kjerne_VALUE ===\n");
    }

    public void 한단계실행() {
        mobil_VALUE.중앙처리장치멈춤();
    }

    public Minne_leiar 기억공간() {
        return 기억공간;
    }

    public side_leiar 쪽관리() {
        return 쪽관리;
    }

    public filsystem filsystem() {
        return filsystem;
    }

    public Planleggjar Planleggjar() {
        return Planleggjar;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Prosess_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
