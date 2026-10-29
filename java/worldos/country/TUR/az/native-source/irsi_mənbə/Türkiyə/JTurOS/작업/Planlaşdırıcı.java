// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiyə.JTurOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Türkiyə.JTurOS.기억공간.səhifə_menecer;
import Türkiyə.JTurOS.fayl_sistemi.파일서술자표;

/** Proses_VALUE 식별자와 라운드로빈 Hazırla 대기열을 관리한다. */
public final class Planlaşdırıcı {
    private final səhifə_menecer 쪽관리;
    private final Map<Integer, Proses_VALUE> Proses_Siyahısı = new HashMap<Integer, Proses_VALUE>();
    private final Queue<Proses_VALUE> 준비대기열 = new ArrayDeque<Proses_VALUE>();
    private int Sonrakı_identifikator = 1;

    public Planlaşdırıcı(səhifə_menecer 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proses_VALUE 첫과정(파일서술자표 파일서술자) {
        Proses_VALUE 새과정 = new Proses_VALUE(ayırmaq_identifikator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Proses_Siyahısı.put(Integer.valueOf(새과정.identifikator_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proses_VALUE 복제(Proses_VALUE 부모) {
        Proses_VALUE uşaq_VALUE = new Proses_VALUE(
                ayırmaq_identifikator(),
                부모.identifikator_VALUE(),
                쪽관리.쓰기시복사복제(부모.ünvan_məkan()),
                부모.파일서술자().복제());
        uşaq_VALUE.프로그램끝설정(부모.프로그램끝());
        Proses_Siyahısı.put(Integer.valueOf(uşaq_VALUE.identifikator_VALUE()), uşaq_VALUE);
        준비대기열.offer(uşaq_VALUE);
        return uşaq_VALUE;
    }

    public Proses_VALUE Sonrakı_Proses() {
        int çek_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < çek_COUNT; INDEX++) {
            Proses_VALUE Sonrakı_element = 준비대기열.poll();
            if (Sonrakı_element != null && (Sonrakı_element.vəziyyət_VALUE() == Proses_vəziyyət.Hazırla || Sonrakı_element.vəziyyət_VALUE() == Proses_vəziyyət.icra_etmək_əmr)) {
                Sonrakı_element.Dəst_vəziyyət(Proses_vəziyyət.icra_etmək_əmr);
                준비대기열.offer(Sonrakı_element);
                return Sonrakı_element;
            }
        }
        return null;
    }

    public int 자식기다리기(Proses_VALUE 부모, int uşaq_identifikator, boolean 기다리지않음) {
        for (Proses_VALUE 후보 : Proses_Siyahısı.values()) {
            if (후보.부모식별자() != 부모.identifikator_VALUE()) {
                continue;
            }
            if (uşaq_identifikator > 0 && 후보.identifikator_VALUE() != uşaq_identifikator) {
                continue;
            }
            if (후보.vəziyyət_VALUE() == Proses_vəziyyət.Çıxış_proqram) {
                int ölçü = (후보.Çıxış_kod() & 0xff) << 8;
                Proses_Siyahısı.remove(Integer.valueOf(후보.identifikator_VALUE()));
                return ölçü;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proses_VALUE FIND_Proses(int identifikator_VALUE) {
        return Proses_Siyahısı.get(Integer.valueOf(identifikator_VALUE));
    }

    private int ayırmaq_identifikator() {
        return Sonrakı_identifikator++;
    }
}
