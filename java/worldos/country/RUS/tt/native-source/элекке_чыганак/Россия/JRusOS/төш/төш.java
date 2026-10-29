// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.төш;

import Россия.JRusOS.기억공간.Хәтер_идарәче;
import Россия.JRusOS.기억공간.бит_идарәче;
import Россия.JRusOS.입력.입력관리자;
import Россия.JRusOS.작업.Процесс_VALUE;
import Россия.JRusOS.작업.Планлаштыручы;
import Россия.JRusOS.체계호출.체계호출;
import Россия.JRusOS.файл_системасы.파일서술자표;
import Россия.JRusOS.файл_системасы.файл_системасы;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class төш {
    private final 하드웨어 мобиль_VALUE;
    private final Хәтер_идарәче 기억공간 = new Хәтер_идарәче(32 * 1024 * 1024);
    private final бит_идарәче 쪽관리 = new бит_идарәче();
    private final файл_системасы файл_системасы = new файл_системасы();
    private final Планлаштыручы Планлаштыручы = new Планлаштыручы(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Процесс_VALUE 첫과정;
    private final 체계호출 체계호출;

    public төш(하드웨어 мобиль_VALUE) {
        this.мобиль_VALUE = мобиль_VALUE;
        첫과정 = Планлаштыручы.첫과정(new 파일서술자표(файл_системасы));
        체계호출 = new 체계호출(файл_системасы, 쪽관리, Планлаштыручы, мобиль_VALUE, 입력관리);
    }

    public void эшләтү() {
        мобиль_VALUE.직렬출력("=== JRusOS 관리 төш_VALUE ===\n");
    }

    public void 한단계실행() {
        мобиль_VALUE.중앙처리장치멈춤();
    }

    public Хәтер_идарәче 기억공간() {
        return 기억공간;
    }

    public бит_идарәче 쪽관리() {
        return 쪽관리;
    }

    public файл_системасы файл_системасы() {
        return файл_системасы;
    }

    public Планлаштыручы Планлаштыручы() {
        return Планлаштыручы;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Процесс_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
