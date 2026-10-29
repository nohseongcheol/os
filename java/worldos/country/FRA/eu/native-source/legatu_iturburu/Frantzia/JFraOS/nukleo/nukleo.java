// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frantzia.JFraOS.nukleo;

import Frantzia.JFraOS.기억공간.Memoria_kudeatzaile;
import Frantzia.JFraOS.기억공간.orri_kudeatzaile;
import Frantzia.JFraOS.입력.입력관리자;
import Frantzia.JFraOS.작업.prozesu_balio;
import Frantzia.JFraOS.작업.Antolatzailea;
import Frantzia.JFraOS.체계호출.체계호출;
import Frantzia.JFraOS.fitxategi_sistema.파일서술자표;
import Frantzia.JFraOS.fitxategi_sistema.fitxategi_sistema;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class nukleo {
    private final 하드웨어 gailu_balio;
    private final Memoria_kudeatzaile 기억공간 = new Memoria_kudeatzaile(32 * 1024 * 1024);
    private final orri_kudeatzaile 쪽관리 = new orri_kudeatzaile();
    private final fitxategi_sistema fitxategi_sistema = new fitxategi_sistema();
    private final Antolatzailea Antolatzailea = new Antolatzailea(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final prozesu_balio 첫과정;
    private final 체계호출 체계호출;

    public nukleo(하드웨어 gailu_balio) {
        this.gailu_balio = gailu_balio;
        첫과정 = Antolatzailea.첫과정(new 파일서술자표(fitxategi_sistema));
        체계호출 = new 체계호출(fitxategi_sistema, 쪽관리, Antolatzailea, gailu_balio, 입력관리);
    }

    public void Exekutatu_2() {
        gailu_balio.직렬출력("=== JFraOS 관리 nukleo_balio ===\n");
    }

    public void exekutatu_urrats() {
        gailu_balio.중앙처리장치멈춤();
    }

    public Memoria_kudeatzaile 기억공간() {
        return 기억공간;
    }

    public orri_kudeatzaile 쪽관리() {
        return 쪽관리;
    }

    public fitxategi_sistema fitxategi_sistema() {
        return fitxategi_sistema;
    }

    public Antolatzailea Antolatzailea() {
        return Antolatzailea;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public prozesu_balio 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
