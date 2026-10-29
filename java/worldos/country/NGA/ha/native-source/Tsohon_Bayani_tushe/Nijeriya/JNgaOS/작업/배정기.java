// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijeriya.JNgaOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Nijeriya.JNgaOS.기억공간.shafi_Manaja;
import Nijeriya.JNgaOS.tsarin_fayil_a_kwamfuta.파일서술자표;

/** haryar_aikin_na_ura_Daraja 식별자와 라운드로빈 Shirya 대기열을 관리한다. */
public final class 배정기 {
    private final shafi_Manaja 쪽관리;
    private final Map<Integer, haryar_aikin_na_ura_Daraja> Jerin_gudanar_da_Aiyuka = new HashMap<Integer, haryar_aikin_na_ura_Daraja>();
    private final Queue<haryar_aikin_na_ura_Daraja> 준비대기열 = new ArrayDeque<haryar_aikin_na_ura_Daraja>();
    private int 다음식별자 = 1;

    public 배정기(shafi_Manaja 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public haryar_aikin_na_ura_Daraja 첫과정(파일서술자표 파일서술자) {
        haryar_aikin_na_ura_Daraja 새과정 = new haryar_aikin_na_ura_Daraja(kasafta_mai_ganewa(), 0, 쪽관리.새주소공간(), 파일서술자);
        Jerin_gudanar_da_Aiyuka.put(Integer.valueOf(새과정.mai_ganewa_Daraja()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public haryar_aikin_na_ura_Daraja 복제(haryar_aikin_na_ura_Daraja 부모) {
        haryar_aikin_na_ura_Daraja yaro_Daraja = new haryar_aikin_na_ura_Daraja(
                kasafta_mai_ganewa(),
                부모.mai_ganewa_Daraja(),
                쪽관리.쓰기시복사복제(부모.imel_wuri()),
                부모.파일서술자().복제());
        yaro_Daraja.프로그램끝설정(부모.프로그램끝());
        Jerin_gudanar_da_Aiyuka.put(Integer.valueOf(yaro_Daraja.mai_ganewa_Daraja()), yaro_Daraja);
        준비대기열.offer(yaro_Daraja);
        return yaro_Daraja;
    }

    public haryar_aikin_na_ura_Daraja 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int Indes = 0; Indes < 검사수; Indes++) {
            haryar_aikin_na_ura_Daraja 다음 = 준비대기열.poll();
            if (다음 != null && (다음.Matsayi_Daraja() == haryar_aikin_na_ura_Matsayi.Shirya || 다음.Matsayi_Daraja() == haryar_aikin_na_ura_Matsayi.gudanar_Umarni)) {
                다음.zubi_Matsayi(haryar_aikin_na_ura_Matsayi.gudanar_Umarni);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(haryar_aikin_na_ura_Daraja 부모, int yaro_mai_ganewa, boolean 기다리지않음) {
        for (haryar_aikin_na_ura_Daraja 후보 : Jerin_gudanar_da_Aiyuka.values()) {
            if (후보.부모식별자() != 부모.mai_ganewa_Daraja()) {
                continue;
            }
            if (yaro_mai_ganewa > 0 && 후보.mai_ganewa_Daraja() != yaro_mai_ganewa) {
                continue;
            }
            if (후보.Matsayi_Daraja() == haryar_aikin_na_ura_Matsayi.Mafita_Shiri) {
                int 결과 = (후보.Mafita_lambar_sirri() & 0xff) << 8;
                Jerin_gudanar_da_Aiyuka.remove(Integer.valueOf(후보.mai_ganewa_Daraja()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public haryar_aikin_na_ura_Daraja nema_haryar_aikin_na_ura(int mai_ganewa_Daraja) {
        return Jerin_gudanar_da_Aiyuka.get(Integer.valueOf(mai_ganewa_Daraja));
    }

    private int kasafta_mai_ganewa() {
        return 다음식별자++;
    }
}
