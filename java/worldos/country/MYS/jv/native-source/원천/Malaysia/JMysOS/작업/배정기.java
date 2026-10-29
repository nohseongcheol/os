// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malaysia.JMysOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Malaysia.JMysOS.기억공간.쪽관리자;
import Malaysia.JMysOS.파일체계.파일서술자표;

/** 과정 식별자와 라운드로빈 준비 대기열을 관리한다. */
public final class 배정기 {
    private final 쪽관리자 쪽관리;
    private final Map<Integer, 과정> 과정들 = new HashMap<Integer, 과정>();
    private final Queue<과정> 준비대기열 = new ArrayDeque<과정>();
    private int 다음식별자 = 1;

    public 배정기(쪽관리자 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public 과정 첫과정(파일서술자표 파일서술자) {
        과정 새과정 = new 과정(식별자할당(), 0, 쪽관리.새주소공간(), 파일서술자);
        과정들.put(Integer.valueOf(새과정.식별자()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public 과정 복제(과정 부모) {
        과정 자식 = new 과정(
                식별자할당(),
                부모.식별자(),
                쪽관리.쓰기시복사복제(부모.주소공간()),
                부모.파일서술자().복제());
        자식.프로그램끝설정(부모.프로그램끝());
        과정들.put(Integer.valueOf(자식.식별자()), 자식);
        준비대기열.offer(자식);
        return 자식;
    }

    public 과정 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int 번호 = 0; 번호 < 검사수; 번호++) {
            과정 다음 = 준비대기열.poll();
            if (다음 != null && (다음.상태() == 과정상태.준비 || 다음.상태() == 과정상태.실행)) {
                다음.상태설정(과정상태.실행);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(과정 부모, int 자식식별자, boolean 기다리지않음) {
        for (과정 후보 : 과정들.values()) {
            if (후보.부모식별자() != 부모.식별자()) {
                continue;
            }
            if (자식식별자 > 0 && 후보.식별자() != 자식식별자) {
                continue;
            }
            if (후보.상태() == 과정상태.종료) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                과정들.remove(Integer.valueOf(후보.식별자()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public 과정 과정찾기(int 식별자) {
        return 과정들.get(Integer.valueOf(식별자));
    }

    private int 식별자할당() {
        return 다음식별자++;
    }
}
