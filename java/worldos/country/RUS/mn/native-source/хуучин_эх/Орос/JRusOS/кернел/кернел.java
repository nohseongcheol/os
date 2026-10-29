// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Орос.JRusOS.кернел;

import Орос.JRusOS.기억공간.санах_ой_менежер;
import Орос.JRusOS.기억공간.хуудас_менежер;
import Орос.JRusOS.입력.입력관리자;
import Орос.JRusOS.작업.үйл_явц_утга;
import Орос.JRusOS.작업.배정기;
import Орос.JRusOS.체계호출.체계호출;
import Орос.JRusOS.файлын_систем.파일서술자표;
import Орос.JRusOS.файлын_систем.файлын_систем;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class кернел {
    private final 하드웨어 гар_утас_утга;
    private final санах_ой_менежер 기억공간 = new санах_ой_менежер(32 * 1024 * 1024);
    private final хуудас_менежер 쪽관리 = new хуудас_менежер();
    private final файлын_систем файлын_систем = new файлын_систем();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final үйл_явц_утга 첫과정;
    private final 체계호출 체계호출;

    public кернел(하드웨어 гар_утас_утга) {
        this.гар_утас_утга = гар_утас_утга;
        첫과정 = 배정기.첫과정(new 파일서술자표(файлын_систем));
        체계호출 = new 체계호출(файлын_систем, 쪽관리, 배정기, гар_утас_утга, 입력관리);
    }

    public void Ажиллуулах() {
        гар_утас_утга.직렬출력("=== JRusOS 관리 кернел_утга ===\n");
    }

    public void 한단계실행() {
        гар_утас_утга.중앙처리장치멈춤();
    }

    public санах_ой_менежер 기억공간() {
        return 기억공간;
    }

    public хуудас_менежер 쪽관리() {
        return 쪽관리;
    }

    public файлын_систем файлын_систем() {
        return файлын_систем;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public үйл_явц_утга 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
