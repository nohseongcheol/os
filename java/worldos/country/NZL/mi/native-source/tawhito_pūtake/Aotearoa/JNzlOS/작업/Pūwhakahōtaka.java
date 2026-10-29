// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Aotearoa.JNzlOS.기억공간.whārangi_pouwhakahaere;
import Aotearoa.JNzlOS.pūnaha_kōnae.파일서술자표;

/** Hātepe_uara 식별자와 라운드로빈 Whakarite 대기열을 관리한다. */
public final class Pūwhakahōtaka {
    private final whārangi_pouwhakahaere 쪽관리;
    private final Map<Integer, Hātepe_uara> Rārangi_Tukanga = new HashMap<Integer, Hātepe_uara>();
    private final Queue<Hātepe_uara> 준비대기열 = new ArrayDeque<Hātepe_uara>();
    private int Panuku_pūtāutu = 1;

    public Pūwhakahōtaka(whārangi_pouwhakahaere 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Hātepe_uara 첫과정(파일서술자표 파일서술자) {
        Hātepe_uara 새과정 = new Hātepe_uara(tiritiri_pūtāutu(), 0, 쪽관리.새주소공간(), 파일서술자);
        Rārangi_Tukanga.put(Integer.valueOf(새과정.pūtāutu_uara()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Hātepe_uara 복제(Hātepe_uara 부모) {
        Hātepe_uara tamaiti_uara = new Hātepe_uara(
                tiritiri_pūtāutu(),
                부모.pūtāutu_uara(),
                쪽관리.쓰기시복사복제(부모.ADDRESS_wāhi()),
                부모.파일서술자().복제());
        tamaiti_uara.프로그램끝설정(부모.프로그램끝());
        Rārangi_Tukanga.put(Integer.valueOf(tamaiti_uara.pūtāutu_uara()), tamaiti_uara);
        준비대기열.offer(tamaiti_uara);
        return tamaiti_uara;
    }

    public Hātepe_uara Panuku_Hātepe() {
        int taki_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < taki_COUNT; INDEX++) {
            Hātepe_uara Panuku_tuemi = 준비대기열.poll();
            if (Panuku_tuemi != null && (Panuku_tuemi.tūnga_uara() == Hātepe_tūnga.Whakarite || Panuku_tuemi.tūnga_uara() == Hātepe_tūnga.kawe_tono)) {
                Panuku_tuemi.huinga_tūnga(Hātepe_tūnga.kawe_tono);
                준비대기열.offer(Panuku_tuemi);
                return Panuku_tuemi;
            }
        }
        return null;
    }

    public int 자식기다리기(Hātepe_uara 부모, int tamaiti_pūtāutu, boolean 기다리지않음) {
        for (Hātepe_uara 후보 : Rārangi_Tukanga.values()) {
            if (후보.부모식별자() != 부모.pūtāutu_uara()) {
                continue;
            }
            if (tamaiti_pūtāutu > 0 && 후보.pūtāutu_uara() != tamaiti_pūtāutu) {
                continue;
            }
            if (후보.tūnga_uara() == Hātepe_tūnga.Putaatu_kaupapa) {
                int mēhua = (후보.Putaatu_CODE() & 0xff) << 8;
                Rārangi_Tukanga.remove(Integer.valueOf(후보.pūtāutu_uara()));
                return mēhua;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Hātepe_uara FIND_Hātepe(int pūtāutu_uara) {
        return Rārangi_Tukanga.get(Integer.valueOf(pūtāutu_uara));
    }

    private int tiritiri_pūtāutu() {
        return Panuku_pūtāutu++;
    }
}
