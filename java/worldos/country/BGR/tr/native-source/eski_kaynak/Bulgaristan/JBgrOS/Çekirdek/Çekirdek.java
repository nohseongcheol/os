// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bulgaristan.JBgrOS.Çekirdek;

import Bulgaristan.JBgrOS.Bellek_bölge.Bellek_yönetici;
import Bulgaristan.JBgrOS.Bellek_bölge.sayfa_yönetici;
import Bulgaristan.JBgrOS.artış_değer.artış_yönetici;
import Bulgaristan.JBgrOS.작업.işlem_değer;
import Bulgaristan.JBgrOS.작업.Scheduler;
import Bulgaristan.JBgrOS.sistem_çağrısı.sistem_çağrısı;
import Bulgaristan.JBgrOS.dosya_sistemi.Dosya_tanımlayıcı_tablo;
import Bulgaristan.JBgrOS.dosya_sistemi.dosya_sistemi;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class Çekirdek {
    private final donanım_değer cihaz_değer;
    private final Bellek_yönetici Bellek_bölge = new Bellek_yönetici(32 * 1024 * 1024);
    private final sayfa_yönetici 쪽관리 = new sayfa_yönetici();
    private final dosya_sistemi dosya_sistemi = new dosya_sistemi();
    private final Scheduler Scheduler = new Scheduler(쪽관리);
    private final artış_yönetici 입력관리 = new artış_yönetici(256);
    private final işlem_değer 첫과정;
    private final sistem_çağrısı sistem_çağrısı;

    public Çekirdek(donanım_değer cihaz_değer) {
        this.cihaz_değer = cihaz_değer;
        첫과정 = Scheduler.첫과정(new Dosya_tanımlayıcı_tablo(dosya_sistemi));
        sistem_çağrısı = new sistem_çağrısı(dosya_sistemi, 쪽관리, Scheduler, cihaz_değer, 입력관리);
    }

    public void çalıştır() {
        cihaz_değer.직렬출력("=== JBgrOS 관리 çekirdek_değer ===\n");
    }

    public void yürütmek_adım() {
        cihaz_değer.중앙처리장치멈춤();
    }

    public Bellek_yönetici Bellek_bölge() {
        return Bellek_bölge;
    }

    public sayfa_yönetici 쪽관리() {
        return 쪽관리;
    }

    public dosya_sistemi dosya_sistemi() {
        return dosya_sistemi;
    }

    public Scheduler Scheduler() {
        return Scheduler;
    }

    public artış_yönetici 입력관리() {
        return 입력관리;
    }

    public işlem_değer 첫과정() {
        return 첫과정;
    }

    public sistem_çağrısı sistem_çağrısı() {
        return sistem_çağrısı;
    }
}
