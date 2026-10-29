// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package NAM.JNamOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import NAM.JNamOS.기억공간.tsebe_motsamaisi;
import NAM.JNamOS.setsamaisadifaele.파일서술자표;

/** Thulaganyo_Boleng 식별자와 라운드로빈 Baakanya 대기열을 관리한다. */
public final class 배정기 {
    private final tsebe_motsamaisi 쪽관리;
    private final Map<Integer, Thulaganyo_Boleng> Lenaanetsamaiso = new HashMap<Integer, Thulaganyo_Boleng>();
    private final Queue<Thulaganyo_Boleng> 준비대기열 = new ArrayDeque<Thulaganyo_Boleng>();
    private int 다음식별자 = 1;

    public 배정기(tsebe_motsamaisi 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Thulaganyo_Boleng 첫과정(파일서술자표 파일서술자) {
        Thulaganyo_Boleng 새과정 = new Thulaganyo_Boleng(abela_setlhaodi(), 0, 쪽관리.새주소공간(), 파일서술자);
        Lenaanetsamaiso.put(Integer.valueOf(새과정.setlhaodi_Boleng()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Thulaganyo_Boleng 복제(Thulaganyo_Boleng 부모) {
        Thulaganyo_Boleng ngwana_Boleng = new Thulaganyo_Boleng(
                abela_setlhaodi(),
                부모.setlhaodi_Boleng(),
                쪽관리.쓰기시복사복제(부모.aterese_sebaka()),
                부모.파일서술자().복제());
        ngwana_Boleng.프로그램끝설정(부모.프로그램끝());
        Lenaanetsamaiso.put(Integer.valueOf(ngwana_Boleng.setlhaodi_Boleng()), ngwana_Boleng);
        준비대기열.offer(ngwana_Boleng);
        return ngwana_Boleng;
    }

    public Thulaganyo_Boleng 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int tshupane = 0; tshupane < 검사수; tshupane++) {
            Thulaganyo_Boleng 다음 = 준비대기열.poll();
            if (다음 != null && (다음.kemo_Boleng() == Thulaganyo_kemo.Baakanya || 다음.kemo_Boleng() == Thulaganyo_kemo.diragatsa_Taelo)) {
                다음.sete_kemo(Thulaganyo_kemo.diragatsa_Taelo);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(Thulaganyo_Boleng 부모, int ngwana_setlhaodi, boolean 기다리지않음) {
        for (Thulaganyo_Boleng 후보 : Lenaanetsamaiso.values()) {
            if (후보.부모식별자() != 부모.setlhaodi_Boleng()) {
                continue;
            }
            if (ngwana_setlhaodi > 0 && 후보.setlhaodi_Boleng() != ngwana_setlhaodi) {
                continue;
            }
            if (후보.kemo_Boleng() == Thulaganyo_kemo.tswaya_Tiriso) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                Lenaanetsamaiso.remove(Integer.valueOf(후보.setlhaodi_Boleng()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Thulaganyo_Boleng batla_Thulaganyo(int setlhaodi_Boleng) {
        return Lenaanetsamaiso.get(Integer.valueOf(setlhaodi_Boleng));
    }

    private int abela_setlhaodi() {
        return 다음식별자++;
    }
}
