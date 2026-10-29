// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package i_Swaziland.JSwzOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import i_Swaziland.JSwzOS.기억공간.ikhasi_imeneja;
import i_Swaziland.JSwzOS.isistimu_yefayela.파일서술자표;

/** Inqubo_inani 식별자와 라운드로빈 Hlela 대기열을 관리한다. */
public final class 배정기 {
    private final ikhasi_imeneja 쪽관리;
    private final Map<Integer, Inqubo_inani> Uhlu_Lokuqhubekayo = new HashMap<Integer, Inqubo_inani>();
    private final Queue<Inqubo_inani> 준비대기열 = new ArrayDeque<Inqubo_inani>();
    private int 다음식별자 = 1;

    public 배정기(ikhasi_imeneja 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Inqubo_inani 첫과정(파일서술자표 파일서술자) {
        Inqubo_inani 새과정 = new Inqubo_inani(abela_isivezi(), 0, 쪽관리.새주소공간(), 파일서술자);
        Uhlu_Lokuqhubekayo.put(Integer.valueOf(새과정.isivezi_inani()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Inqubo_inani 복제(Inqubo_inani 부모) {
        Inqubo_inani ingane_inani = new Inqubo_inani(
                abela_isivezi(),
                부모.isivezi_inani(),
                쪽관리.쓰기시복사복제(부모.ikheli_indawo()),
                부모.파일서술자().복제());
        ingane_inani.프로그램끝설정(부모.프로그램끝());
        Uhlu_Lokuqhubekayo.put(Integer.valueOf(ingane_inani.isivezi_inani()), ingane_inani);
        준비대기열.offer(ingane_inani);
        return ingane_inani;
    }

    public Inqubo_inani 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int thola_inkomba = 0; thola_inkomba < 검사수; thola_inkomba++) {
            Inqubo_inani 다음 = 준비대기열.poll();
            if (다음 != null && (다음.isimo_inani() == Inqubo_isimo.Hlela || 다음.isimo_inani() == Inqubo_isimo.yenza_umyalo)) {
                다음.isethi_isimo(Inqubo_isimo.yenza_umyalo);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(Inqubo_inani 부모, int ingane_isivezi, boolean 기다리지않음) {
        for (Inqubo_inani 후보 : Uhlu_Lokuqhubekayo.values()) {
            if (후보.부모식별자() != 부모.isivezi_inani()) {
                continue;
            }
            if (ingane_isivezi > 0 && 후보.isivezi_inani() != ingane_isivezi) {
                continue;
            }
            if (후보.isimo_inani() == Inqubo_isimo.phuma_i_app) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                Uhlu_Lokuqhubekayo.remove(Integer.valueOf(후보.isivezi_inani()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Inqubo_inani thola_Inqubo(int isivezi_inani) {
        return Uhlu_Lokuqhubekayo.get(Integer.valueOf(isivezi_inani));
    }

    private int abela_isivezi() {
        return 다음식별자++;
    }
}
