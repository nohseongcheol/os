// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Soome.JFinOS.Mälu_regioon.쪽관리자;
import Soome.JFinOS.failisüsteem.파일서술자표;

/** Joonis_VALUE 식별자와 라운드로빈 Ettevalmistamine 대기열을 관리한다. */
public final class plaanija {
    private final 쪽관리자 쪽관리;
    private final Map<Integer, Joonis_VALUE> Joonisloend = new HashMap<Integer, Joonis_VALUE>();
    private final Queue<Joonis_VALUE> 준비대기열 = new ArrayDeque<Joonis_VALUE>();
    private int Edasi_identifikaator = 1;

    public plaanija(쪽관리자 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Joonis_VALUE 첫과정(파일서술자표 파일서술자) {
        Joonis_VALUE 새과정 = new Joonis_VALUE(lisama_identifikaator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Joonisloend.put(Integer.valueOf(새과정.identifikaator_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Joonis_VALUE kloon_VALUE(Joonis_VALUE ema_VALUE) {
        Joonis_VALUE laps_VALUE = new Joonis_VALUE(
                lisama_identifikaator(),
                ema_VALUE.identifikaator_VALUE(),
                쪽관리.쓰기시복사복제(ema_VALUE.ADDRESS_ruum()),
                ema_VALUE.파일서술자().kloon_VALUE());
        laps_VALUE.hulk_programm_vaheaeg(ema_VALUE.programm_vaheaeg());
        Joonisloend.put(Integer.valueOf(laps_VALUE.identifikaator_VALUE()), laps_VALUE);
        준비대기열.offer(laps_VALUE);
        return laps_VALUE;
    }

    public Joonis_VALUE Edasi_Joonis() {
        int tšekk_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < tšekk_COUNT; INDEX++) {
            Joonis_VALUE Edasi_kaup = 준비대기열.poll();
            if (Edasi_kaup != null && (Edasi_kaup.Olek_VALUE() == Joonis_Olek.Ettevalmistamine || Edasi_kaup.Olek_VALUE() == Joonis_Olek.Täida_käsk)) {
                Edasi_kaup.hulk_Olek(Joonis_Olek.Täida_käsk);
                준비대기열.offer(Edasi_kaup);
                return Edasi_kaup;
            }
        }
        return null;
    }

    public int 자식기다리기(Joonis_VALUE ema_VALUE, int laps_identifikaator, boolean 기다리지않음) {
        for (Joonis_VALUE 후보 : Joonisloend.values()) {
            if (후보.ema_identifikaator() != ema_VALUE.identifikaator_VALUE()) {
                continue;
            }
            if (laps_identifikaator > 0 && 후보.identifikaator_VALUE() != laps_identifikaator) {
                continue;
            }
            if (후보.Olek_VALUE() == Joonis_Olek.Välju_programm) {
                int TULEMUS = (후보.Välju_CODE() & 0xff) << 8;
                Joonisloend.remove(Integer.valueOf(후보.identifikaator_VALUE()));
                return TULEMUS;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Joonis_VALUE FIND_Joonis(int identifikaator_VALUE) {
        return Joonisloend.get(Integer.valueOf(identifikaator_VALUE));
    }

    private int lisama_identifikaator() {
        return Edasi_identifikaator++;
    }
}
