// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Greqi.JGrcOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Greqi.JGrcOS.기억공간.faqe_menaxher;
import Greqi.JGrcOS.sistemi_i_skedarëve.파일서술자표;

/** Proces_VALUE 식별자와 라운드로빈 Përgatit 대기열을 관리한다. */
public final class Planifikuesi {
    private final faqe_menaxher 쪽관리;
    private final Map<Integer, Proces_VALUE> Lista_e_procesit = new HashMap<Integer, Proces_VALUE>();
    private final Queue<Proces_VALUE> 준비대기열 = new ArrayDeque<Proces_VALUE>();
    private int Tjetër_identifikues = 1;

    public Planifikuesi(faqe_menaxher 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proces_VALUE 첫과정(파일서술자표 파일서술자) {
        Proces_VALUE 새과정 = new Proces_VALUE(caktoj_identifikues(), 0, 쪽관리.새주소공간(), 파일서술자);
        Lista_e_procesit.put(Integer.valueOf(새과정.identifikues_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proces_VALUE 복제(Proces_VALUE 부모) {
        Proces_VALUE fëmijë_VALUE = new Proces_VALUE(
                caktoj_identifikues(),
                부모.identifikues_VALUE(),
                쪽관리.쓰기시복사복제(부모.email_HAPËSIRË()),
                부모.파일서술자().복제());
        fëmijë_VALUE.프로그램끝설정(부모.프로그램끝());
        Lista_e_procesit.put(Integer.valueOf(fëmijë_VALUE.identifikues_VALUE()), fëmijë_VALUE);
        준비대기열.offer(fëmijë_VALUE);
        return fëmijë_VALUE;
    }

    public Proces_VALUE Tjetër_Proces() {
        int çek_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < çek_COUNT; INDEX++) {
            Proces_VALUE Tjetër_njësi = 준비대기열.poll();
            if (Tjetër_njësi != null && (Tjetër_njësi.status_VALUE() == Proces_status.Përgatit || Tjetër_njësi.status_VALUE() == Proces_status.zbatoj_komandë)) {
                Tjetër_njësi.bashkësi_status(Proces_status.zbatoj_komandë);
                준비대기열.offer(Tjetër_njësi);
                return Tjetër_njësi;
            }
        }
        return null;
    }

    public int 자식기다리기(Proces_VALUE 부모, int fëmijë_identifikues, boolean 기다리지않음) {
        for (Proces_VALUE 후보 : Lista_e_procesit.values()) {
            if (후보.부모식별자() != 부모.identifikues_VALUE()) {
                continue;
            }
            if (fëmijë_identifikues > 0 && 후보.identifikues_VALUE() != fëmijë_identifikues) {
                continue;
            }
            if (후보.status_VALUE() == Proces_status.dal_program) {
                int llogaritje = (후보.dal_kod() & 0xff) << 8;
                Lista_e_procesit.remove(Integer.valueOf(후보.identifikues_VALUE()));
                return llogaritje;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proces_VALUE FIND_Proces(int identifikues_VALUE) {
        return Lista_e_procesit.get(Integer.valueOf(identifikues_VALUE));
    }

    private int caktoj_identifikues() {
        return Tjetër_identifikues++;
    }
}
