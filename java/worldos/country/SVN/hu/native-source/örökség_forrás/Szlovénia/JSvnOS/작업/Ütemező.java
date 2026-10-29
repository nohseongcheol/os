// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Szlovénia.JSvnOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Szlovénia.JSvnOS.Memória_régió.lap_kezelő;
import Szlovénia.JSvnOS.fájlrendszer.파일서술자표;

/** folyamat_ÉRTÉK 식별자와 라운드로빈 Előkészítés 대기열을 관리한다. */
public final class Ütemező {
    private final lap_kezelő 쪽관리;
    private final Map<Integer, folyamat_ÉRTÉK> Folyamatlista = new HashMap<Integer, folyamat_ÉRTÉK>();
    private final Queue<folyamat_ÉRTÉK> 준비대기열 = new ArrayDeque<folyamat_ÉRTÉK>();
    private int Tovább_azonosító = 1;

    public Ütemező(lap_kezelő 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public folyamat_ÉRTÉK 첫과정(파일서술자표 파일서술자) {
        folyamat_ÉRTÉK 새과정 = new folyamat_ÉRTÉK(kioszt_azonosító(), 0, 쪽관리.새주소공간(), 파일서술자);
        Folyamatlista.put(Integer.valueOf(새과정.azonosító_ÉRTÉK()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public folyamat_ÉRTÉK klón_ÉRTÉK(folyamat_ÉRTÉK szülő_ÉRTÉK) {
        folyamat_ÉRTÉK gyermek_ÉRTÉK = new folyamat_ÉRTÉK(
                kioszt_azonosító(),
                szülő_ÉRTÉK.azonosító_ÉRTÉK(),
                쪽관리.쓰기시복사복제(szülő_ÉRTÉK.címtartomány()),
                szülő_ÉRTÉK.파일서술자().klón_ÉRTÉK());
        gyermek_ÉRTÉK.halmaz_app_szünet(szülő_ÉRTÉK.app_szünet());
        Folyamatlista.put(Integer.valueOf(gyermek_ÉRTÉK.azonosító_ÉRTÉK()), gyermek_ÉRTÉK);
        준비대기열.offer(gyermek_ÉRTÉK);
        return gyermek_ÉRTÉK;
    }

    public folyamat_ÉRTÉK Tovább_folyamat() {
        int csekk_DARAB = 준비대기열.size();
        for (int INDEX = 0; INDEX < csekk_DARAB; INDEX++) {
            folyamat_ÉRTÉK Tovább_cikk = 준비대기열.poll();
            if (Tovább_cikk != null && (Tovább_cikk.Állapot_ÉRTÉK() == folyamat_Állapot.Előkészítés || Tovább_cikk.Állapot_ÉRTÉK() == folyamat_Állapot.végrehajt_parancs)) {
                Tovább_cikk.halmaz_Állapot(folyamat_Állapot.végrehajt_parancs);
                준비대기열.offer(Tovább_cikk);
                return Tovább_cikk;
            }
        }
        return null;
    }

    public int 자식기다리기(folyamat_ÉRTÉK szülő_ÉRTÉK, int gyermek_azonosító, boolean 기다리지않음) {
        for (folyamat_ÉRTÉK 후보 : Folyamatlista.values()) {
            if (후보.szülő_azonosító() != szülő_ÉRTÉK.azonosító_ÉRTÉK()) {
                continue;
            }
            if (gyermek_azonosító > 0 && 후보.azonosító_ÉRTÉK() != gyermek_azonosító) {
                continue;
            }
            if (후보.Állapot_ÉRTÉK() == folyamat_Állapot.kilép_app) {
                int KR = (후보.kilép_KÓD() & 0xff) << 8;
                Folyamatlista.remove(Integer.valueOf(후보.azonosító_ÉRTÉK()));
                return KR;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public folyamat_ÉRTÉK keres_folyamat(int azonosító_ÉRTÉK) {
        return Folyamatlista.get(Integer.valueOf(azonosító_ÉRTÉK));
    }

    private int kioszt_azonosító() {
        return Tovább_azonosító++;
    }
}
