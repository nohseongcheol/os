// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.өзөк;

import Кыргызстан.JKgzOS.기억공간.эс_башкаруучу;
import Кыргызстан.JKgzOS.기억공간.бет_башкаруучу;
import Кыргызстан.JKgzOS.입력.입력관리자;
import Кыргызстан.JKgzOS.작업.Процесс_маани;
import Кыргызстан.JKgzOS.작업.배정기;
import Кыргызстан.JKgzOS.체계호출.체계호출;
import Кыргызстан.JKgzOS.файл_тутуму.파일서술자표;
import Кыргызстан.JKgzOS.файл_тутуму.файл_тутуму;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class өзөк {
    private final 하드웨어 түзмөк_маани;
    private final эс_башкаруучу 기억공간 = new эс_башкаруучу(32 * 1024 * 1024);
    private final бет_башкаруучу 쪽관리 = new бет_башкаруучу();
    private final файл_тутуму файл_тутуму = new файл_тутуму();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Процесс_маани 첫과정;
    private final 체계호출 체계호출;

    public өзөк(하드웨어 түзмөк_маани) {
        this.түзмөк_маани = түзмөк_маани;
        첫과정 = 배정기.첫과정(new 파일서술자표(файл_тутуму));
        체계호출 = new 체계호출(файл_тутуму, 쪽관리, 배정기, түзмөк_маани, 입력관리);
    }

    public void Жүргүзүү() {
        түзмөк_маани.직렬출력("=== JKgzOS 관리 өзөк_маани ===\n");
    }

    public void 한단계실행() {
        түзмөк_маани.중앙처리장치멈춤();
    }

    public эс_башкаруучу 기억공간() {
        return 기억공간;
    }

    public бет_башкаруучу 쪽관리() {
        return 쪽관리;
    }

    public файл_тутуму файл_тутуму() {
        return файл_тутуму;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Процесс_маани 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
