// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Owganystan.JAfgOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Owganystan.JAfgOS.기억공간.sahypa_iş_dolandyryjy;
import Owganystan.JAfgOS.faýl_ulgamy.파일서술자표;

/** Proses_baha 식별자와 라운드로빈 Taýýarla 대기열을 관리한다. */
public final class 배정기 {
    private final sahypa_iş_dolandyryjy 쪽관리;
    private final Map<Integer, Proses_baha> Proses_sanawy = new HashMap<Integer, Proses_baha>();
    private final Queue<Proses_baha> 준비대기열 = new ArrayDeque<Proses_baha>();
    private int 다음식별자 = 1;

    public 배정기(sahypa_iş_dolandyryjy 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proses_baha 첫과정(파일서술자표 파일서술자) {
        Proses_baha 새과정 = new Proses_baha(bölüp_aýyr_tanaýjy(), 0, 쪽관리.새주소공간(), 파일서술자);
        Proses_sanawy.put(Integer.valueOf(새과정.tanaýjy_baha()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proses_baha 복제(Proses_baha 부모) {
        Proses_baha çaga_baha = new Proses_baha(
                bölüp_aýyr_tanaýjy(),
                부모.tanaýjy_baha(),
                쪽관리.쓰기시복사복제(부모.salgy_ýer()),
                부모.파일서술자().복제());
        çaga_baha.프로그램끝설정(부모.프로그램끝());
        Proses_sanawy.put(Integer.valueOf(çaga_baha.tanaýjy_baha()), çaga_baha);
        준비대기열.offer(çaga_baha);
        return çaga_baha;
    }

    public Proses_baha 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int indeks = 0; indeks < 검사수; indeks++) {
            Proses_baha 다음 = 준비대기열.poll();
            if (다음 != null && (다음.ýagdaý_baha() == Proses_ýagdaý.Taýýarla || 다음.ýagdaý_baha() == Proses_ýagdaý.ýerine_ýetir_buýruk)) {
                다음.köplük_ýagdaý(Proses_ýagdaý.ýerine_ýetir_buýruk);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(Proses_baha 부모, int çaga_tanaýjy, boolean 기다리지않음) {
        for (Proses_baha 후보 : Proses_sanawy.values()) {
            if (후보.부모식별자() != 부모.tanaýjy_baha()) {
                continue;
            }
            if (çaga_tanaýjy > 0 && 후보.tanaýjy_baha() != çaga_tanaýjy) {
                continue;
            }
            if (후보.ýagdaý_baha() == Proses_ýagdaý.çyk_programma) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                Proses_sanawy.remove(Integer.valueOf(후보.tanaýjy_baha()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proses_baha tap_Proses(int tanaýjy_baha) {
        return Proses_sanawy.get(Integer.valueOf(tanaýjy_baha));
    }

    private int bölüp_aýyr_tanaýjy() {
        return 다음식별자++;
    }
}
