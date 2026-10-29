// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украіна.JUkrOS.ядро;

import Украіна.JUkrOS.기억공간.памяць_менеджар;
import Украіна.JUkrOS.기억공간.старонка_менеджар;
import Украіна.JUkrOS.입력.입력관리자;
import Украіна.JUkrOS.작업.Працэс_значэнне;
import Украіна.JUkrOS.작업.배정기;
import Украіна.JUkrOS.체계호출.체계호출;
import Украіна.JUkrOS.файлавая_сістэма.파일서술자표;
import Украіна.JUkrOS.файлавая_сістэма.файлавая_сістэма;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ядро {
    private final 하드웨어 прылада_значэнне;
    private final памяць_менеджар 기억공간 = new памяць_менеджар(32 * 1024 * 1024);
    private final старонка_менеджар 쪽관리 = new старонка_менеджар();
    private final файлавая_сістэма файлавая_сістэма = new файлавая_сістэма();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Працэс_значэнне 첫과정;
    private final 체계호출 체계호출;

    public ядро(하드웨어 прылада_значэнне) {
        this.прылада_значэнне = прылада_значэнне;
        첫과정 = 배정기.첫과정(new 파일서술자표(файлавая_сістэма));
        체계호출 = new 체계호출(файлавая_сістэма, 쪽관리, 배정기, прылада_значэнне, 입력관리);
    }

    public void Выканаць() {
        прылада_значэнне.직렬출력("=== JUkrOS 관리 ядро_значэнне ===\n");
    }

    public void 한단계실행() {
        прылада_значэнне.중앙처리장치멈춤();
    }

    public памяць_менеджар 기억공간() {
        return 기억공간;
    }

    public старонка_менеджар 쪽관리() {
        return 쪽관리;
    }

    public файлавая_сістэма файлавая_сістэма() {
        return файлавая_сістэма;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Працэс_значэнне 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
