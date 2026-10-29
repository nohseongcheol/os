// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Kernel;

import Lëtzebuerg.JLuxOS.기억공간.Späicher_Manager;
import Lëtzebuerg.JLuxOS.기억공간.Säit_Manager;
import Lëtzebuerg.JLuxOS.입력.입력관리자;
import Lëtzebuerg.JLuxOS.작업.Prozess_VALUE;
import Lëtzebuerg.JLuxOS.작업.Planifikateur;
import Lëtzebuerg.JLuxOS.체계호출.체계호출;
import Lëtzebuerg.JLuxOS.Fichierssystem.파일서술자표;
import Lëtzebuerg.JLuxOS.Fichierssystem.Fichierssystem;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class Kernel {
    private final 하드웨어 Mobil_VALUE;
    private final Späicher_Manager 기억공간 = new Späicher_Manager(32 * 1024 * 1024);
    private final Säit_Manager 쪽관리 = new Säit_Manager();
    private final Fichierssystem Fichierssystem = new Fichierssystem();
    private final Planifikateur Planifikateur = new Planifikateur(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Prozess_VALUE 첫과정;
    private final 체계호출 체계호출;

    public Kernel(하드웨어 Mobil_VALUE) {
        this.Mobil_VALUE = Mobil_VALUE;
        첫과정 = Planifikateur.첫과정(new 파일서술자표(Fichierssystem));
        체계호출 = new 체계호출(Fichierssystem, 쪽관리, Planifikateur, Mobil_VALUE, 입력관리);
    }

    public void Laf() {
        Mobil_VALUE.직렬출력("=== JLuxOS 관리 Kernel_VALUE ===\n");
    }

    public void 한단계실행() {
        Mobil_VALUE.중앙처리장치멈춤();
    }

    public Späicher_Manager 기억공간() {
        return 기억공간;
    }

    public Säit_Manager 쪽관리() {
        return 쪽관리;
    }

    public Fichierssystem Fichierssystem() {
        return Fichierssystem;
    }

    public Planifikateur Planifikateur() {
        return Planifikateur;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Prozess_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
