// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Грција.JGrcOS.јадро;

import Грција.JGrcOS.기억공간.Меморија_управник;
import Грција.JGrcOS.기억공간.страница_управник;
import Грција.JGrcOS.입력.입력관리자;
import Грција.JGrcOS.작업.Процес_VALUE;
import Грција.JGrcOS.작업.Распоредувач;
import Грција.JGrcOS.체계호출.체계호출;
import Грција.JGrcOS.систем_на_датотеки.파일서술자표;
import Грција.JGrcOS.систем_на_датотеки.систем_на_датотеки;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class јадро {
    private final 하드웨어 уред_VALUE;
    private final Меморија_управник 기억공간 = new Меморија_управник(32 * 1024 * 1024);
    private final страница_управник 쪽관리 = new страница_управник();
    private final систем_на_датотеки систем_на_датотеки = new систем_на_датотеки();
    private final Распоредувач Распоредувач = new Распоредувач(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Процес_VALUE 첫과정;
    private final 체계호출 체계호출;

    public јадро(하드웨어 уред_VALUE) {
        this.уред_VALUE = уред_VALUE;
        첫과정 = Распоредувач.첫과정(new 파일서술자표(систем_на_датотеки));
        체계호출 = new 체계호출(систем_на_датотеки, 쪽관리, Распоредувач, уред_VALUE, 입력관리);
    }

    public void Изврши_2() {
        уред_VALUE.직렬출력("=== JGrcOS 관리 јадро_VALUE ===\n");
    }

    public void 한단계실행() {
        уред_VALUE.중앙처리장치멈춤();
    }

    public Меморија_управник 기억공간() {
        return 기억공간;
    }

    public страница_управник 쪽관리() {
        return 쪽관리;
    }

    public систем_на_датотеки систем_на_датотеки() {
        return систем_на_датотеки;
    }

    public Распоредувач Распоредувач() {
        return Распоредувач;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Процес_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
