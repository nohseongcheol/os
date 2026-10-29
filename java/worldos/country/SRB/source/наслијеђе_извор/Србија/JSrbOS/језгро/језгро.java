// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.језгро;

import Србија.JSrbOS.기억공간.Меморија_менаџер;
import Србија.JSrbOS.기억공간.страница_менаџер;
import Србија.JSrbOS.입력.입력관리자;
import Србија.JSrbOS.작업.Процес_вриједност;
import Србија.JSrbOS.작업.Планер;
import Србија.JSrbOS.체계호출.체계호출;
import Србија.JSrbOS.фајл_систем.파일서술자표;
import Србија.JSrbOS.фајл_систем.фајл_систем;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class језгро {
    private final 하드웨어 уређај_вриједност;
    private final Меморија_менаџер 기억공간 = new Меморија_менаџер(32 * 1024 * 1024);
    private final страница_менаџер 쪽관리 = new страница_менаџер();
    private final фајл_систем фајл_систем = new фајл_систем();
    private final Планер Планер = new Планер(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Процес_вриједност 첫과정;
    private final 체계호출 체계호출;

    public језгро(하드웨어 уређај_вриједност) {
        this.уређај_вриједност = уређај_вриједност;
        첫과정 = Планер.첫과정(new 파일서술자표(фајл_систем));
        체계호출 = new 체계호출(фајл_систем, 쪽관리, Планер, уређај_вриједност, 입력관리);
    }

    public void Покрени() {
        уређај_вриједност.직렬출력("=== JSrbOS 관리 језгро_вриједност ===\n");
    }

    public void Изврши_корак() {
        уређај_вриједност.중앙처리장치멈춤();
    }

    public Меморија_менаџер 기억공간() {
        return 기억공간;
    }

    public страница_менаџер 쪽관리() {
        return 쪽관리;
    }

    public фајл_систем фајл_систем() {
        return фајл_систем;
    }

    public Планер Планер() {
        return Планер;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Процес_вриједност 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
