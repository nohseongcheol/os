// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nàìjíríà.JNgaOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Nàìjíríà.JNgaOS.기억공간.ojú_ìwé_alákòóso;
import Nàìjíríà.JNgaOS.ìlànà_ètò_fáìlì.파일서술자표;

/** Ìlànà_iye 식별자와 라운드로빈 gbaradì 대기열을 관리한다. */
public final class 배정기 {
    private final ojú_ìwé_alákòóso 쪽관리;
    private final Map<Integer, Ìlànà_iye> Àtòjọ_Iṣẹ́ = new HashMap<Integer, Ìlànà_iye>();
    private final Queue<Ìlànà_iye> 준비대기열 = new ArrayDeque<Ìlànà_iye>();
    private int 다음식별자 = 1;

    public 배정기(ojú_ìwé_alákòóso 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Ìlànà_iye 첫과정(파일서술자표 파일서술자) {
        Ìlànà_iye 새과정 = new Ìlànà_iye(pín_Àfidámọ̀(), 0, 쪽관리.새주소공간(), 파일서술자);
        Àtòjọ_Iṣẹ́.put(Integer.valueOf(새과정.Àfidámọ̀_iye()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Ìlànà_iye 복제(Ìlànà_iye 부모) {
        Ìlànà_iye ọmọ_iye = new Ìlànà_iye(
                pín_Àfidámọ̀(),
                부모.Àfidámọ̀_iye(),
                쪽관리.쓰기시복사복제(부모.àdírẹ́ẹ̀sì_àlàfo()),
                부모.파일서술자().복제());
        ọmọ_iye.프로그램끝설정(부모.프로그램끝());
        Àtòjọ_Iṣẹ́.put(Integer.valueOf(ọmọ_iye.Àfidámọ̀_iye()), ọmọ_iye);
        준비대기열.offer(ọmọ_iye);
        return ọmọ_iye;
    }

    public Ìlànà_iye 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 검사수; wá_atọ̀ka_àkóónú++) {
            Ìlànà_iye 다음 = 준비대기열.poll();
            if (다음 != null && (다음.ipò_iye() == Ìlànà_ipò.gbaradì || 다음.ipò_iye() == Ìlànà_ipò.ṣiṣẹ́_àṣẹ)) {
                다음.ọ̀wọ̀_ipò(Ìlànà_ipò.ṣiṣẹ́_àṣẹ);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(Ìlànà_iye 부모, int ọmọ_Àfidámọ̀, boolean 기다리지않음) {
        for (Ìlànà_iye 후보 : Àtòjọ_Iṣẹ́.values()) {
            if (후보.부모식별자() != 부모.Àfidámọ̀_iye()) {
                continue;
            }
            if (ọmọ_Àfidámọ̀ > 0 && 후보.Àfidámọ̀_iye() != ọmọ_Àfidámọ̀) {
                continue;
            }
            if (후보.ipò_iye() == Ìlànà_ipò.jáde_àtòjọ_ètò) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                Àtòjọ_Iṣẹ́.remove(Integer.valueOf(후보.Àfidámọ̀_iye()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Ìlànà_iye wá_Ìlànà(int Àfidámọ̀_iye) {
        return Àtòjọ_Iṣẹ́.get(Integer.valueOf(Àfidámọ̀_iye));
    }

    private int pín_Àfidámọ̀() {
        return 다음식별자++;
    }
}
