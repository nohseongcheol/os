// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.ҳаста;

import Тоҷикистон.JTjkOS.기억공간.ҳофиза_мудир;
import Тоҷикистон.JTjkOS.기억공간.саҳифа_мудир;
import Тоҷикистон.JTjkOS.입력.입력관리자;
import Тоҷикистон.JTjkOS.작업.Раванд_қимат;
import Тоҷикистон.JTjkOS.작업.배정기;
import Тоҷикистон.JTjkOS.체계호출.체계호출;
import Тоҷикистон.JTjkOS.системаи_файлӣ.파일서술자표;
import Тоҷикистон.JTjkOS.системаи_файлӣ.системаи_файлӣ;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ҳаста {
    private final 하드웨어 мобилӣ_қимат;
    private final ҳофиза_мудир 기억공간 = new ҳофиза_мудир(32 * 1024 * 1024);
    private final саҳифа_мудир 쪽관리 = new саҳифа_мудир();
    private final системаи_файлӣ системаи_файлӣ = new системаи_файлӣ();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Раванд_қимат 첫과정;
    private final 체계호출 체계호출;

    public ҳаста(하드웨어 мобилӣ_қимат) {
        this.мобилӣ_қимат = мобилӣ_қимат;
        첫과정 = 배정기.첫과정(new 파일서술자표(системаи_файлӣ));
        체계호출 = new 체계호출(системаи_файлӣ, 쪽관리, 배정기, мобилӣ_қимат, 입력관리);
    }

    public void порча() {
        мобилӣ_қимат.직렬출력("=== JTjkOS 관리 ҳаста_қимат ===\n");
    }

    public void 한단계실행() {
        мобилӣ_қимат.중앙처리장치멈춤();
    }

    public ҳофиза_мудир 기억공간() {
        return 기억공간;
    }

    public саҳифа_мудир 쪽관리() {
        return 쪽관리;
    }

    public системаи_файлӣ системаи_файлӣ() {
        return системаи_файлӣ;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Раванд_қимат 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
