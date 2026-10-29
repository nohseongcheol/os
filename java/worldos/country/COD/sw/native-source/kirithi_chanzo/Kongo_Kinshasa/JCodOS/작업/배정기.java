// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kongo_Kinshasa.JCodOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Kongo_Kinshasa.JCodOS.기억공간.ukurasa_msimamizi;
import Kongo_Kinshasa.JCodOS.mfumo_ya_mafaili.파일서술자표;

/** Mchakato_thamani 식별자와 라운드로빈 Andaa 대기열을 관리한다. */
public final class 배정기 {
    private final ukurasa_msimamizi 쪽관리;
    private final Map<Integer, Mchakato_thamani> Orodha_ya_Mchakato = new HashMap<Integer, Mchakato_thamani>();
    private final Queue<Mchakato_thamani> 준비대기열 = new ArrayDeque<Mchakato_thamani>();
    private int 다음식별자 = 1;

    public 배정기(ukurasa_msimamizi 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Mchakato_thamani 첫과정(파일서술자표 파일서술자) {
        Mchakato_thamani 새과정 = new Mchakato_thamani(tengea_kitambulishi(), 0, 쪽관리.새주소공간(), 파일서술자);
        Orodha_ya_Mchakato.put(Integer.valueOf(새과정.kitambulishi_thamani()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Mchakato_thamani 복제(Mchakato_thamani 부모) {
        Mchakato_thamani mtoto_thamani = new Mchakato_thamani(
                tengea_kitambulishi(),
                부모.kitambulishi_thamani(),
                쪽관리.쓰기시복사복제(부모.anwani_eneo()),
                부모.파일서술자().복제());
        mtoto_thamani.프로그램끝설정(부모.프로그램끝());
        Orodha_ya_Mchakato.put(Integer.valueOf(mtoto_thamani.kitambulishi_thamani()), mtoto_thamani);
        준비대기열.offer(mtoto_thamani);
        return mtoto_thamani;
    }

    public Mchakato_thamani 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int kielezo = 0; kielezo < 검사수; kielezo++) {
            Mchakato_thamani 다음 = 준비대기열.poll();
            if (다음 != null && (다음.hali_thamani() == Mchakato_hali.Andaa || 다음.hali_thamani() == Mchakato_hali.tekeleza_amri)) {
                다음.seti_hali(Mchakato_hali.tekeleza_amri);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(Mchakato_thamani 부모, int mtoto_kitambulishi, boolean 기다리지않음) {
        for (Mchakato_thamani 후보 : Orodha_ya_Mchakato.values()) {
            if (후보.부모식별자() != 부모.kitambulishi_thamani()) {
                continue;
            }
            if (mtoto_kitambulishi > 0 && 후보.kitambulishi_thamani() != mtoto_kitambulishi) {
                continue;
            }
            if (후보.hali_thamani() == Mchakato_hali.toka_programu) {
                int 결과 = (후보.toka_msimbo() & 0xff) << 8;
                Orodha_ya_Mchakato.remove(Integer.valueOf(후보.kitambulishi_thamani()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Mchakato_thamani gundua_Mchakato(int kitambulishi_thamani) {
        return Orodha_ya_Mchakato.get(Integer.valueOf(kitambulishi_thamani));
    }

    private int tengea_kitambulishi() {
        return 다음식별자++;
    }
}
