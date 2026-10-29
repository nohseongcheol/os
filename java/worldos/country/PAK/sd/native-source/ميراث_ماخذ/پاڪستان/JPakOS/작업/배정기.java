// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاڪستان.JPakOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import پاڪستان.JPakOS.기억공간.صفحو_مئنيجر;
import پاڪستان.JPakOS.فائل_سسٽم.파일서술자표;

/** عمل_قدر 식별자와 라운드로빈 تياري_ڪريو 대기열을 관리한다. */
public final class 배정기 {
    private final صفحو_مئنيجر 쪽관리;
    private final Map<Integer, عمل_قدر> عمل_جي_لسٽ = new HashMap<Integer, عمل_قدر>();
    private final Queue<عمل_قدر> 준비대기열 = new ArrayDeque<عمل_قدر>();
    private int 다음식별자 = 1;

    public 배정기(صفحو_مئنيجر 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public عمل_قدر 첫과정(파일서술자표 파일서술자) {
        عمل_قدر 새과정 = new عمل_قدر(مختص_ڪريو_سڃاڻپ_ڪندڙ(), 0, 쪽관리.새주소공간(), 파일서술자);
        عمل_جي_لسٽ.put(Integer.valueOf(새과정.سڃاڻپ_ڪندڙ_قدر()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public عمل_قدر 복제(عمل_قدر 부모) {
        عمل_قدر ٻار_قدر = new عمل_قدر(
                مختص_ڪريو_سڃاڻپ_ڪندڙ(),
                부모.سڃاڻپ_ڪندڙ_قدر(),
                쪽관리.쓰기시복사복제(부모.پتو_جڳهه()),
                부모.파일서술자().복제());
        ٻار_قدر.프로그램끝설정(부모.프로그램끝());
        عمل_جي_لسٽ.put(Integer.valueOf(ٻار_قدر.سڃاڻپ_ڪندڙ_قدر()), ٻار_قدر);
        준비대기열.offer(ٻار_قدر);
        return ٻار_قدر;
    }

    public عمل_قدر 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int ابتدائي = 0; ابتدائي < 검사수; ابتدائي++) {
            عمل_قدر 다음 = 준비대기열.poll();
            if (다음 != null && (다음.حالت_قدر() == عمل_حالت.تياري_ڪريو || 다음.حالت_قدر() == عمل_حالت.تعميل_ڪرڻ_حڪم)) {
                다음.سيٽ_حالت(عمل_حالت.تعميل_ڪرڻ_حڪم);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(عمل_قدر 부모, int ٻار_سڃاڻپ_ڪندڙ, boolean 기다리지않음) {
        for (عمل_قدر 후보 : عمل_جي_لسٽ.values()) {
            if (후보.부모식별자() != 부모.سڃاڻپ_ڪندڙ_قدر()) {
                continue;
            }
            if (ٻار_سڃاڻپ_ڪندڙ > 0 && 후보.سڃاڻپ_ڪندڙ_قدر() != ٻار_سڃاڻپ_ڪندڙ) {
                continue;
            }
            if (후보.حالت_قدر() == عمل_حالت.خارج_ڪريو_ائپ) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                عمل_جي_لسٽ.remove(Integer.valueOf(후보.سڃاڻپ_ڪندڙ_قدر()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public عمل_قدر ڳوليو_عمل(int سڃاڻپ_ڪندڙ_قدر) {
        return عمل_جي_لسٽ.get(Integer.valueOf(سڃاڻپ_ڪندڙ_قدر));
    }

    private int مختص_ڪريو_سڃاڻپ_ڪندڙ() {
        return 다음식별자++;
    }
}
