// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Lëtzebuerg.JLuxOS.기억공간.Säit_Manager;
import Lëtzebuerg.JLuxOS.Fichierssystem.파일서술자표;

/** Prozess_VALUE 식별자와 라운드로빈 Préparéieren 대기열을 관리한다. */
public final class Planifikateur {
    private final Säit_Manager 쪽관리;
    private final Map<Integer, Prozess_VALUE> Prozesslëscht = new HashMap<Integer, Prozess_VALUE>();
    private final Queue<Prozess_VALUE> 준비대기열 = new ArrayDeque<Prozess_VALUE>();
    private int Weider_Identifikateur = 1;

    public Planifikateur(Säit_Manager 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Prozess_VALUE 첫과정(파일서술자표 파일서술자) {
        Prozess_VALUE 새과정 = new Prozess_VALUE(zouweisen_Identifikateur(), 0, 쪽관리.새주소공간(), 파일서술자);
        Prozesslëscht.put(Integer.valueOf(새과정.Identifikateur_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Prozess_VALUE 복제(Prozess_VALUE 부모) {
        Prozess_VALUE Kand_VALUE = new Prozess_VALUE(
                zouweisen_Identifikateur(),
                부모.Identifikateur_VALUE(),
                쪽관리.쓰기시복사복제(부모.Adress_Plaz()),
                부모.파일서술자().복제());
        Kand_VALUE.프로그램끝설정(부모.프로그램끝());
        Prozesslëscht.put(Integer.valueOf(Kand_VALUE.Identifikateur_VALUE()), Kand_VALUE);
        준비대기열.offer(Kand_VALUE);
        return Kand_VALUE;
    }

    public Prozess_VALUE Weider_Prozess() {
        int Scheck_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < Scheck_COUNT; INDEX++) {
            Prozess_VALUE Weider_Element = 준비대기열.poll();
            if (Weider_Element != null && (Weider_Element.Status_VALUE() == Prozess_Status.Préparéieren || Weider_Element.Status_VALUE() == Prozess_Status.ausféieren_Befeel)) {
                Weider_Element.Saz_Status(Prozess_Status.ausféieren_Befeel);
                준비대기열.offer(Weider_Element);
                return Weider_Element;
            }
        }
        return null;
    }

    public int 자식기다리기(Prozess_VALUE 부모, int Kand_Identifikateur, boolean 기다리지않음) {
        for (Prozess_VALUE 후보 : Prozesslëscht.values()) {
            if (후보.부모식별자() != 부모.Identifikateur_VALUE()) {
                continue;
            }
            if (Kand_Identifikateur > 0 && 후보.Identifikateur_VALUE() != Kand_Identifikateur) {
                continue;
            }
            if (후보.Status_VALUE() == Prozess_Status.Schluss_App) {
                int Mooss = (후보.Schluss_CODE() & 0xff) << 8;
                Prozesslëscht.remove(Integer.valueOf(후보.Identifikateur_VALUE()));
                return Mooss;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Prozess_VALUE FIND_Prozess(int Identifikateur_VALUE) {
        return Prozesslëscht.get(Integer.valueOf(Identifikateur_VALUE));
    }

    private int zouweisen_Identifikateur() {
        return Weider_Identifikateur++;
    }
}
