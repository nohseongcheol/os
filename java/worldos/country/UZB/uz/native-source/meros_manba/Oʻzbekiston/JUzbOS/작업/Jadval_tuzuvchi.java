// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Oʻzbekiston.JUzbOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Oʻzbekiston.JUzbOS.기억공간.sahifa_menejer;
import Oʻzbekiston.JUzbOS.fayllar_tizimi.파일서술자표;

/** Jarayon_VALUE 식별자와 라운드로빈 Tayyorlamoq 대기열을 관리한다. */
public final class Jadval_tuzuvchi {
    private final sahifa_menejer 쪽관리;
    private final Map<Integer, Jarayon_VALUE> Jarayon_ro_yxati = new HashMap<Integer, Jarayon_VALUE>();
    private final Queue<Jarayon_VALUE> 준비대기열 = new ArrayDeque<Jarayon_VALUE>();
    private int Keyingi_identifikator = 1;

    public Jadval_tuzuvchi(sahifa_menejer 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Jarayon_VALUE 첫과정(파일서술자표 파일서술자) {
        Jarayon_VALUE 새과정 = new Jarayon_VALUE(joylashtirmoq_identifikator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Jarayon_ro_yxati.put(Integer.valueOf(새과정.identifikator_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Jarayon_VALUE 복제(Jarayon_VALUE 부모) {
        Jarayon_VALUE farzand_VALUE = new Jarayon_VALUE(
                joylashtirmoq_identifikator(),
                부모.identifikator_VALUE(),
                쪽관리.쓰기시복사복제(부모.manzil_joy()),
                부모.파일서술자().복제());
        farzand_VALUE.프로그램끝설정(부모.프로그램끝());
        Jarayon_ro_yxati.put(Integer.valueOf(farzand_VALUE.identifikator_VALUE()), farzand_VALUE);
        준비대기열.offer(farzand_VALUE);
        return farzand_VALUE;
    }

    public Jarayon_VALUE Keyingi_Jarayon() {
        int chek_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < chek_COUNT; INDEX++) {
            Jarayon_VALUE Keyingi_element = 준비대기열.poll();
            if (Keyingi_element != null && (Keyingi_element.holat_VALUE_e10195a1() == Jarayon_holat.Tayyorlamoq || Keyingi_element.holat_VALUE_e10195a1() == Jarayon_holat.bajarmoq_buyruq)) {
                Keyingi_element.to_plam_holat(Jarayon_holat.bajarmoq_buyruq);
                준비대기열.offer(Keyingi_element);
                return Keyingi_element;
            }
        }
        return null;
    }

    public int 자식기다리기(Jarayon_VALUE 부모, int farzand_identifikator, boolean 기다리지않음) {
        for (Jarayon_VALUE 후보 : Jarayon_ro_yxati.values()) {
            if (후보.부모식별자() != 부모.identifikator_VALUE()) {
                continue;
            }
            if (farzand_identifikator > 0 && 후보.identifikator_VALUE() != farzand_identifikator) {
                continue;
            }
            if (후보.holat_VALUE_e10195a1() == Jarayon_holat.Chiqish_ilova) {
                int o_lchov = (후보.Chiqish_kod() & 0xff) << 8;
                Jarayon_ro_yxati.remove(Integer.valueOf(후보.identifikator_VALUE()));
                return o_lchov;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Jarayon_VALUE FIND_Jarayon(int identifikator_VALUE) {
        return Jarayon_ro_yxati.get(Integer.valueOf(identifikator_VALUE));
    }

    private int joylashtirmoq_identifikator() {
        return Keyingi_identifikator++;
    }
}
