// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package UGA.JUgaOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import UGA.JUgaOS.기억공간.paji_Umugenzuzi;
import UGA.JUgaOS.sisitemu_ya_dosiye.파일서술자표;

/** Inzira_agaciro 식별자와 라운드로빈 Gutegura 대기열을 관리한다. */
public final class 배정기 {
    private final paji_Umugenzuzi 쪽관리;
    private final Map<Integer, Inzira_agaciro> Utwambi_tw_igikorwa = new HashMap<Integer, Inzira_agaciro>();
    private final Queue<Inzira_agaciro> 준비대기열 = new ArrayDeque<Inzira_agaciro>();
    private int 다음식별자 = 1;

    public 배정기(paji_Umugenzuzi 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Inzira_agaciro 첫과정(파일서술자표 파일서술자) {
        Inzira_agaciro 새과정 = new Inzira_agaciro(kugenera_indanga(), 0, 쪽관리.새주소공간(), 파일서술자);
        Utwambi_tw_igikorwa.put(Integer.valueOf(새과정.indanga_agaciro()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Inzira_agaciro 복제(Inzira_agaciro 부모) {
        Inzira_agaciro ishami_agaciro_b642f4b4 = new Inzira_agaciro(
                kugenera_indanga(),
                부모.indanga_agaciro(),
                쪽관리.쓰기시복사복제(부모.aderesi_akanya()),
                부모.파일서술자().복제());
        ishami_agaciro_b642f4b4.프로그램끝설정(부모.프로그램끝());
        Utwambi_tw_igikorwa.put(Integer.valueOf(ishami_agaciro_b642f4b4.indanga_agaciro()), ishami_agaciro_b642f4b4);
        준비대기열.offer(ishami_agaciro_b642f4b4);
        return ishami_agaciro_b642f4b4;
    }

    public Inzira_agaciro 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int umugerekashakiro = 0; umugerekashakiro < 검사수; umugerekashakiro++) {
            Inzira_agaciro 다음 = 준비대기열.poll();
            if (다음 != null && (다음.imimerere_agaciro() == Inzira_imimerere.Gutegura || 다음.imimerere_agaciro() == Inzira_imimerere.gukora_ibwiriza)) {
                다음.itsinda_imimerere(Inzira_imimerere.gukora_ibwiriza);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(Inzira_agaciro 부모, int ishami_indanga, boolean 기다리지않음) {
        for (Inzira_agaciro 후보 : Utwambi_tw_igikorwa.values()) {
            if (후보.부모식별자() != 부모.indanga_agaciro()) {
                continue;
            }
            if (ishami_indanga > 0 && 후보.indanga_agaciro() != ishami_indanga) {
                continue;
            }
            if (후보.imimerere_agaciro() == Inzira_imimerere.gusohoka_porogaramu) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                Utwambi_tw_igikorwa.remove(Integer.valueOf(후보.indanga_agaciro()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Inzira_agaciro gushaka_Inzira(int indanga_agaciro) {
        return Utwambi_tw_igikorwa.get(Integer.valueOf(indanga_agaciro));
    }

    private int kugenera_indanga() {
        return 다음식별자++;
    }
}
