// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Noreg.JNorOS.기억공간.side_leiar;
import Noreg.JNorOS.filsystem.파일서술자표;

/** Prosess_VALUE 식별자와 라운드로빈 Klargjer 대기열을 관리한다. */
public final class Planleggjar {
    private final side_leiar 쪽관리;
    private final Map<Integer, Prosess_VALUE> Prosessliste = new HashMap<Integer, Prosess_VALUE>();
    private final Queue<Prosess_VALUE> 준비대기열 = new ArrayDeque<Prosess_VALUE>();
    private int Neste_identifikator = 1;

    public Planleggjar(side_leiar 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Prosess_VALUE 첫과정(파일서술자표 파일서술자) {
        Prosess_VALUE 새과정 = new Prosess_VALUE(tildele_identifikator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Prosessliste.put(Integer.valueOf(새과정.identifikator_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Prosess_VALUE 복제(Prosess_VALUE forelder_VALUE) {
        Prosess_VALUE underordna_VALUE = new Prosess_VALUE(
                tildele_identifikator(),
                forelder_VALUE.identifikator_VALUE(),
                쪽관리.쓰기시복사복제(forelder_VALUE.ADDRESS_område()),
                forelder_VALUE.파일서술자().복제());
        underordna_VALUE.sett_app_pause(forelder_VALUE.app_pause());
        Prosessliste.put(Integer.valueOf(underordna_VALUE.identifikator_VALUE()), underordna_VALUE);
        준비대기열.offer(underordna_VALUE);
        return underordna_VALUE;
    }

    public Prosess_VALUE Neste_Prosess() {
        int sjekk_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < sjekk_COUNT; INDEX++) {
            Prosess_VALUE Neste_vare = 준비대기열.poll();
            if (Neste_vare != null && (Neste_vare.status_VALUE() == Prosess_status.Klargjer || Neste_vare.status_VALUE() == Prosess_status.Utfør_kommando)) {
                Neste_vare.sett_status(Prosess_status.Utfør_kommando);
                준비대기열.offer(Neste_vare);
                return Neste_vare;
            }
        }
        return null;
    }

    public int 자식기다리기(Prosess_VALUE forelder_VALUE, int underordna_identifikator, boolean 기다리지않음) {
        for (Prosess_VALUE 후보 : Prosessliste.values()) {
            if (후보.forelder_identifikator() != forelder_VALUE.identifikator_VALUE()) {
                continue;
            }
            if (underordna_identifikator > 0 && 후보.identifikator_VALUE() != underordna_identifikator) {
                continue;
            }
            if (후보.status_VALUE() == Prosess_status.Utgang_app) {
                int forretningsmål = (후보.Utgang_CODE() & 0xff) << 8;
                Prosessliste.remove(Integer.valueOf(후보.identifikator_VALUE()));
                return forretningsmål;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Prosess_VALUE Søk_Prosess(int identifikator_VALUE) {
        return Prosessliste.get(Integer.valueOf(identifikator_VALUE));
    }

    private int tildele_identifikator() {
        return Neste_identifikator++;
    }
}
