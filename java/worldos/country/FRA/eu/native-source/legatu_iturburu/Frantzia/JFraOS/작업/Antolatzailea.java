// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frantzia.JFraOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Frantzia.JFraOS.기억공간.orri_kudeatzaile;
import Frantzia.JFraOS.fitxategi_sistema.파일서술자표;

/** prozesu_balio 식별자와 라운드로빈 준비 대기열을 관리한다. */
public final class Antolatzailea {
    private final orri_kudeatzaile 쪽관리;
    private final Map<Integer, prozesu_balio> prozesu_Zerrenda = new HashMap<Integer, prozesu_balio>();
    private final Queue<prozesu_balio> 준비대기열 = new ArrayDeque<prozesu_balio>();
    private int Hurrengoa_identifikatzaile = 1;

    public Antolatzailea(orri_kudeatzaile 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public prozesu_balio 첫과정(파일서술자표 파일서술자) {
        prozesu_balio 새과정 = new prozesu_balio(esleitu_identifikatzaile(), 0, 쪽관리.새주소공간(), 파일서술자);
        prozesu_Zerrenda.put(Integer.valueOf(새과정.identifikatzaile_balio()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public prozesu_balio klon_balio(prozesu_balio 부모) {
        prozesu_balio haur_balio = new prozesu_balio(
                esleitu_identifikatzaile(),
                부모.identifikatzaile_balio(),
                쪽관리.쓰기시복사복제(부모.helbide_gune()),
                부모.파일서술자().klon_balio());
        haur_balio.sorta_aplik_atseden(부모.aplik_atseden());
        prozesu_Zerrenda.put(Integer.valueOf(haur_balio.identifikatzaile_balio()), haur_balio);
        준비대기열.offer(haur_balio);
        return haur_balio;
    }

    public prozesu_balio Hurrengoa_prozesu() {
        int txeke_ZENBATU = 준비대기열.size();
        for (int INDIZE = 0; INDIZE < txeke_ZENBATU; INDIZE++) {
            prozesu_balio Hurrengoa_elementu = 준비대기열.poll();
            if (Hurrengoa_elementu != null && (Hurrengoa_elementu.Egoera_balio() == prozesu_Egoera.준비 || Hurrengoa_elementu.Egoera_balio() == prozesu_Egoera.exekutatu_komando)) {
                Hurrengoa_elementu.sorta_Egoera(prozesu_Egoera.exekutatu_komando);
                준비대기열.offer(Hurrengoa_elementu);
                return Hurrengoa_elementu;
            }
        }
        return null;
    }

    public int 자식기다리기(prozesu_balio 부모, int haur_identifikatzaile, boolean 기다리지않음) {
        for (prozesu_balio 후보 : prozesu_Zerrenda.values()) {
            if (후보.부모식별자() != 부모.identifikatzaile_balio()) {
                continue;
            }
            if (haur_identifikatzaile > 0 && 후보.identifikatzaile_balio() != haur_identifikatzaile) {
                continue;
            }
            if (후보.Egoera_balio() == prozesu_Egoera.irten_aplik) {
                int EMAITZA = (후보.irten_KODE() & 0xff) << 8;
                prozesu_Zerrenda.remove(Integer.valueOf(후보.identifikatzaile_balio()));
                return EMAITZA;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public prozesu_balio Bilatu_prozesu(int identifikatzaile_balio) {
        return prozesu_Zerrenda.get(Integer.valueOf(identifikatzaile_balio));
    }

    private int esleitu_identifikatzaile() {
        return Hurrengoa_identifikatzaile++;
    }
}
