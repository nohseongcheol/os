// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijeriyaa.JNgaOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Nijeriyaa.JNgaOS.기억공간.hello_kisnoowo;
import Nijeriyaa.JNgaOS.yuɓɓo_piille.파일서술자표;

/** Yuɓɓo_golle_njaru 식별자와 라운드로빈 Heblu 대기열을 관리한다. */
public final class 배정기 {
    private final hello_kisnoowo 쪽관리;
    private final Map<Integer, Yuɓɓo_golle_njaru> Yuɓɓo_golle_Doggol = new HashMap<Integer, Yuɓɓo_golle_njaru>();
    private final Queue<Yuɓɓo_golle_njaru> 준비대기열 = new ArrayDeque<Yuɓɓo_golle_njaru>();
    private int 다음식별자 = 1;

    public 배정기(hello_kisnoowo 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Yuɓɓo_golle_njaru 첫과정(파일서술자표 파일서술자) {
        Yuɓɓo_golle_njaru 새과정 = new Yuɓɓo_golle_njaru(식별자할당(), 0, 쪽관리.새주소공간(), 파일서술자);
        Yuɓɓo_golle_Doggol.put(Integer.valueOf(새과정.식별자()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Yuɓɓo_golle_njaru 복제(Yuɓɓo_golle_njaru 부모) {
        Yuɓɓo_golle_njaru 자식 = new Yuɓɓo_golle_njaru(
                식별자할당(),
                부모.식별자(),
                쪽관리.쓰기시복사복제(부모.ñiiɓirde_wonorde()),
                부모.파일서술자().복제());
        자식.프로그램끝설정(부모.프로그램끝());
        Yuɓɓo_golle_Doggol.put(Integer.valueOf(자식.식별자()), 자식);
        준비대기열.offer(자식);
        return 자식;
    }

    public Yuɓɓo_golle_njaru 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int joopirdu = 0; joopirdu < 검사수; joopirdu++) {
            Yuɓɓo_golle_njaru 다음 = 준비대기열.poll();
            if (다음 != null && (다음.ngonka_njaru() == Yuɓɓo_golle_ngonka.Heblu || 다음.ngonka_njaru() == Yuɓɓo_golle_ngonka.실행)) {
                다음.상태설정(Yuɓɓo_golle_ngonka.실행);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(Yuɓɓo_golle_njaru 부모, int 자식식별자, boolean 기다리지않음) {
        for (Yuɓɓo_golle_njaru 후보 : Yuɓɓo_golle_Doggol.values()) {
            if (후보.부모식별자() != 부모.식별자()) {
                continue;
            }
            if (자식식별자 > 0 && 후보.식별자() != 자식식별자) {
                continue;
            }
            if (후보.ngonka_njaru() == Yuɓɓo_golle_ngonka.yaltude_tafirde) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                Yuɓɓo_golle_Doggol.remove(Integer.valueOf(후보.식별자()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Yuɓɓo_golle_njaru yiylaade_Yuɓɓo_golle(int 식별자) {
        return Yuɓɓo_golle_Doggol.get(Integer.valueOf(식별자));
    }

    private int 식별자할당() {
        return 다음식별자++;
    }
}
