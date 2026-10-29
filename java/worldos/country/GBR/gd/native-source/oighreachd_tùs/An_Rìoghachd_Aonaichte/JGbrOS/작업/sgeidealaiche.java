// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import An_Rìoghachd_Aonaichte.JGbrOS.기억공간.duilleag_manaidsear;
import An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean.파일서술자표;

/** Pròiseas_VALUE 식별자와 라운드로빈 Ullaich 대기열을 관리한다. */
public final class sgeidealaiche {
    private final duilleag_manaidsear 쪽관리;
    private final Map<Integer, Pròiseas_VALUE> pròiseasan_mar_liostaichean = new HashMap<Integer, Pròiseas_VALUE>();
    private final Queue<Pròiseas_VALUE> 준비대기열 = new ArrayDeque<Pròiseas_VALUE>();
    private int air_adhart_aithnichear = 1;

    public sgeidealaiche(duilleag_manaidsear 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Pròiseas_VALUE 첫과정(파일서술자표 파일서술자) {
        Pròiseas_VALUE 새과정 = new Pròiseas_VALUE(sònraich_aithnichear(), 0, 쪽관리.새주소공간(), 파일서술자);
        pròiseasan_mar_liostaichean.put(Integer.valueOf(새과정.aithnichear_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Pròiseas_VALUE 복제(Pròiseas_VALUE 부모) {
        Pròiseas_VALUE duine_cloinne_VALUE = new Pròiseas_VALUE(
                sònraich_aithnichear(),
                부모.aithnichear_VALUE(),
                쪽관리.쓰기시복사복제(부모.ADDRESS_spàs()),
                부모.파일서술자().복제());
        duine_cloinne_VALUE.프로그램끝설정(부모.프로그램끝());
        pròiseasan_mar_liostaichean.put(Integer.valueOf(duine_cloinne_VALUE.aithnichear_VALUE()), duine_cloinne_VALUE);
        준비대기열.offer(duine_cloinne_VALUE);
        return duine_cloinne_VALUE;
    }

    public Pròiseas_VALUE air_adhart_Pròiseas() {
        int seic_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < seic_COUNT; INDEX++) {
            Pròiseas_VALUE air_adhart_nì = 준비대기열.poll();
            if (air_adhart_nì != null && (air_adhart_nì.cor_VALUE() == Pròiseas_cor.Ullaich || air_adhart_nì.cor_VALUE() == Pròiseas_cor.gnìomhaich_àithne)) {
                air_adhart_nì.seata_cor(Pròiseas_cor.gnìomhaich_àithne);
                준비대기열.offer(air_adhart_nì);
                return air_adhart_nì;
            }
        }
        return null;
    }

    public int 자식기다리기(Pròiseas_VALUE 부모, int duine_cloinne_aithnichear, boolean 기다리지않음) {
        for (Pròiseas_VALUE 후보 : pròiseasan_mar_liostaichean.values()) {
            if (후보.부모식별자() != 부모.aithnichear_VALUE()) {
                continue;
            }
            if (duine_cloinne_aithnichear > 0 && 후보.aithnichear_VALUE() != duine_cloinne_aithnichear) {
                continue;
            }
            if (후보.cor_VALUE() == Pròiseas_cor.fàg_ap) {
                int tomhas = (후보.fàg_CODE() & 0xff) << 8;
                pròiseasan_mar_liostaichean.remove(Integer.valueOf(후보.aithnichear_VALUE()));
                return tomhas;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Pròiseas_VALUE FIND_Pròiseas(int aithnichear_VALUE) {
        return pròiseasan_mar_liostaichean.get(Integer.valueOf(aithnichear_VALUE));
    }

    private int sònraich_aithnichear() {
        return air_adhart_aithnichear++;
    }
}
