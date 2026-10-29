// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Azərbaycan.JAzeOS.nüvə;

import Azərbaycan.JAzeOS.기억공간.Yaddaş_menecer;
import Azərbaycan.JAzeOS.기억공간.səhifə_menecer;
import Azərbaycan.JAzeOS.입력.입력관리자;
import Azərbaycan.JAzeOS.작업.Proses_VALUE;
import Azərbaycan.JAzeOS.작업.Planlaşdırıcı;
import Azərbaycan.JAzeOS.체계호출.체계호출;
import Azərbaycan.JAzeOS.fayl_sistemi.파일서술자표;
import Azərbaycan.JAzeOS.fayl_sistemi.fayl_sistemi;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class nüvə {
    private final 하드웨어 cihaz_VALUE;
    private final Yaddaş_menecer 기억공간 = new Yaddaş_menecer(32 * 1024 * 1024);
    private final səhifə_menecer 쪽관리 = new səhifə_menecer();
    private final fayl_sistemi fayl_sistemi = new fayl_sistemi();
    private final Planlaşdırıcı Planlaşdırıcı = new Planlaşdırıcı(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proses_VALUE 첫과정;
    private final 체계호출 체계호출;

    public nüvə(하드웨어 cihaz_VALUE) {
        this.cihaz_VALUE = cihaz_VALUE;
        첫과정 = Planlaşdırıcı.첫과정(new 파일서술자표(fayl_sistemi));
        체계호출 = new 체계호출(fayl_sistemi, 쪽관리, Planlaşdırıcı, cihaz_VALUE, 입력관리);
    }

    public void İcra_Et() {
        cihaz_VALUE.직렬출력("=== JAzeOS 관리 nüvə_VALUE ===\n");
    }

    public void 한단계실행() {
        cihaz_VALUE.중앙처리장치멈춤();
    }

    public Yaddaş_menecer 기억공간() {
        return 기억공간;
    }

    public səhifə_menecer 쪽관리() {
        return 쪽관리;
    }

    public fayl_sistemi fayl_sistemi() {
        return fayl_sistemi;
    }

    public Planlaşdırıcı Planlaşdırıcı() {
        return Planlaşdırıcı;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Proses_VALUE 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
