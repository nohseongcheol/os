// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Malta.JMltOS.기억공간.paġna_maniġer;
import Malta.JMltOS.sistema_tal_fajls.파일서술자표;

/** Proċess_VALUE 식별자와 라운드로빈 Ħejji 대기열을 관리한다. */
public final class Skedatur {
    private final paġna_maniġer 쪽관리;
    private final Map<Integer, Proċess_VALUE> Lista_tal_Proċess = new HashMap<Integer, Proċess_VALUE>();
    private final Queue<Proċess_VALUE> 준비대기열 = new ArrayDeque<Proċess_VALUE>();
    private int Li_Jmiss_identifikatur = 1;

    public Skedatur(paġna_maniġer 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proċess_VALUE 첫과정(파일서술자표 파일서술자) {
        Proċess_VALUE 새과정 = new Proċess_VALUE(alloka_identifikatur(), 0, 쪽관리.새주소공간(), 파일서술자);
        Lista_tal_Proċess.put(Integer.valueOf(새과정.identifikatur_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proċess_VALUE 복제(Proċess_VALUE 부모) {
        Proċess_VALUE tfal_VALUE = new Proċess_VALUE(
                alloka_identifikatur(),
                부모.identifikatur_VALUE(),
                쪽관리.쓰기시복사복제(부모.ADDRESS_SPACE()),
                부모.파일서술자().복제());
        tfal_VALUE.프로그램끝설정(부모.프로그램끝());
        Lista_tal_Proċess.put(Integer.valueOf(tfal_VALUE.identifikatur_VALUE()), tfal_VALUE);
        준비대기열.offer(tfal_VALUE);
        return tfal_VALUE;
    }

    public Proċess_VALUE Li_Jmiss_Proċess() {
        int ċekk_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < ċekk_COUNT; INDEX++) {
            Proċess_VALUE Li_Jmiss_element = 준비대기열.poll();
            if (Li_Jmiss_element != null && (Li_Jmiss_element.stat_VALUE() == Proċess_stat.Ħejji || Li_Jmiss_element.stat_VALUE() == Proċess_stat.eżegwixxa_kmand)) {
                Li_Jmiss_element.sett_stat(Proċess_stat.eżegwixxa_kmand);
                준비대기열.offer(Li_Jmiss_element);
                return Li_Jmiss_element;
            }
        }
        return null;
    }

    public int 자식기다리기(Proċess_VALUE 부모, int tfal_identifikatur, boolean 기다리지않음) {
        for (Proċess_VALUE 후보 : Lista_tal_Proċess.values()) {
            if (후보.부모식별자() != 부모.identifikatur_VALUE()) {
                continue;
            }
            if (tfal_identifikatur > 0 && 후보.identifikatur_VALUE() != tfal_identifikatur) {
                continue;
            }
            if (후보.stat_VALUE() == Proċess_stat.Ħruġ_programm) {
                int miżura = (후보.Ħruġ_CODE() & 0xff) << 8;
                Lista_tal_Proċess.remove(Integer.valueOf(후보.identifikatur_VALUE()));
                return miżura;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proċess_VALUE sab_Proċess(int identifikatur_VALUE) {
        return Lista_tal_Proċess.get(Integer.valueOf(identifikatur_VALUE));
    }

    private int alloka_identifikatur() {
        return Li_Jmiss_identifikatur++;
    }
}
