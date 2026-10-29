// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Senegaal.JSenOS.기억공간.xët_doxalkat;
import Senegaal.JSenOS.barabu_boolebdenc_yu_ñu_bennal.파일서술자표;

/** yokkute_xëyma 식별자와 라운드로빈 jël_matuwaay 대기열을 관리한다. */
public final class 배정기 {
    private final xët_doxalkat 쪽관리;
    private final Map<Integer, yokkute_xëyma> Limu_jaar_jaar_yi = new HashMap<Integer, yokkute_xëyma>();
    private final Queue<yokkute_xëyma> 준비대기열 = new ArrayDeque<yokkute_xëyma>();
    private int 다음식별자 = 1;

    public 배정기(xët_doxalkat 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public yokkute_xëyma 첫과정(파일서술자표 파일서술자) {
        yokkute_xëyma 새과정 = new yokkute_xëyma(jagleel_raññeekaay(), 0, 쪽관리.새주소공간(), 파일서술자);
        Limu_jaar_jaar_yi.put(Integer.valueOf(새과정.raññeekaay_xëyma()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public yokkute_xëyma 복제(yokkute_xëyma 부모) {
        yokkute_xëyma xale_xëyma = new yokkute_xëyma(
                jagleel_raññeekaay(),
                부모.raññeekaay_xëyma(),
                쪽관리.쓰기시복사복제(부모.dëkkuwaay_Espace()),
                부모.파일서술자().복제());
        xale_xëyma.프로그램끝설정(부모.프로그램끝());
        Limu_jaar_jaar_yi.put(Integer.valueOf(xale_xëyma.raññeekaay_xëyma()), xale_xëyma);
        준비대기열.offer(xale_xëyma);
        return xale_xëyma;
    }

    public yokkute_xëyma 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int àlluwa_tur = 0; àlluwa_tur < 검사수; àlluwa_tur++) {
            yokkute_xëyma 다음 = 준비대기열.poll();
            if (다음 != null && (다음.nekkin_xëyma() == yokkute_nekkin.jël_matuwaay || 다음.nekkin_xëyma() == yokkute_nekkin.def_ndigel)) {
                다음.Boole_gi_nekkin(yokkute_nekkin.def_ndigel);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(yokkute_xëyma 부모, int xale_raññeekaay, boolean 기다리지않음) {
        for (yokkute_xëyma 후보 : Limu_jaar_jaar_yi.values()) {
            if (후보.부모식별자() != 부모.raññeekaay_xëyma()) {
                continue;
            }
            if (xale_raññeekaay > 0 && 후보.raññeekaay_xëyma() != xale_raññeekaay) {
                continue;
            }
            if (후보.nekkin_xëyma() == yokkute_nekkin.Génn_jëfekaay) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                Limu_jaar_jaar_yi.remove(Integer.valueOf(후보.raññeekaay_xëyma()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public yokkute_xëyma seet_yokkute(int raññeekaay_xëyma) {
        return Limu_jaar_jaar_yi.get(Integer.valueOf(raññeekaay_xëyma));
    }

    private int jagleel_raññeekaay() {
        return 다음식별자++;
    }
}
