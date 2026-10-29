// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import ᑲᓇᑕᒥ.JCanOS.기억공간.mappigaq_aulattiji;
import ᑲᓇᑕᒥ.JCanOS.inikkuvik.파일서술자표;

/** Pivallianiq_atuutilik 식별자와 라운드로빈 Parnalli 대기열을 관리한다. */
public final class 배정기 {
    private final mappigaq_aulattiji 쪽관리;
    private final Map<Integer, Pivallianiq_atuutilik> Pivallianiq_Titiqpalliagaq = new HashMap<Integer, Pivallianiq_atuutilik>();
    private final Queue<Pivallianiq_atuutilik> 준비대기열 = new ArrayDeque<Pivallianiq_atuutilik>();
    private int 다음식별자 = 1;

    public 배정기(mappigaq_aulattiji 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Pivallianiq_atuutilik 첫과정(파일서술자표 파일서술자) {
        Pivallianiq_atuutilik 새과정 = new Pivallianiq_atuutilik(식별자할당(), 0, 쪽관리.새주소공간(), 파일서술자);
        Pivallianiq_Titiqpalliagaq.put(Integer.valueOf(새과정.식별자()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Pivallianiq_atuutilik 복제(Pivallianiq_atuutilik 부모) {
        Pivallianiq_atuutilik surusiq_atuutilik = new Pivallianiq_atuutilik(
                식별자할당(),
                부모.식별자(),
                쪽관리.쓰기시복사복제(부모.turaarut_SPACEBAR()),
                부모.파일서술자().복제());
        surusiq_atuutilik.프로그램끝설정(부모.프로그램끝());
        Pivallianiq_Titiqpalliagaq.put(Integer.valueOf(surusiq_atuutilik.식별자()), surusiq_atuutilik);
        준비대기열.offer(surusiq_atuutilik);
        return surusiq_atuutilik;
    }

    public Pivallianiq_atuutilik 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 검사수; nalunaiqsimavik++) {
            Pivallianiq_atuutilik 다음 = 준비대기열.poll();
            if (다음 != null && (다음.qanuilinganiq_atuutilik() == Pivallianiq_qanuilinganiq.Parnalli || 다음.qanuilinganiq_atuutilik() == Pivallianiq_qanuilinganiq.실행)) {
                다음.attiqsimaniit_qanuilinganiq(Pivallianiq_qanuilinganiq.실행);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(Pivallianiq_atuutilik 부모, int 자식식별자, boolean 기다리지않음) {
        for (Pivallianiq_atuutilik 후보 : Pivallianiq_Titiqpalliagaq.values()) {
            if (후보.부모식별자() != 부모.식별자()) {
                continue;
            }
            if (자식식별자 > 0 && 후보.식별자() != 자식식별자) {
                continue;
            }
            if (후보.qanuilinganiq_atuutilik() == Pivallianiq_qanuilinganiq.taima_pilirijjut) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                Pivallianiq_Titiqpalliagaq.remove(Integer.valueOf(후보.식별자()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Pivallianiq_atuutilik nanili_Pivallianiq(int 식별자) {
        return Pivallianiq_Titiqpalliagaq.get(Integer.valueOf(식별자));
    }

    private int 식별자할당() {
        return 다음식별자++;
    }
}
