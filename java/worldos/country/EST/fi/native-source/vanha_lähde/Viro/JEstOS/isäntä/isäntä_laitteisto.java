// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Viro.JEstOS.isäntä;

import java.util.HashMap;
import java.util.Map;
import Viro.JEstOS.ydin.laitteisto_ARVO;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 laitteisto_ARVO 대역이다. */
public final class isäntä_laitteisto implements laitteisto_ARVO {
    private final Map<Integer, Integer> laitteisto_portti_ARVO = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Sisältö_ARVO) {
        직렬기록.append(Sisältö_ARVO);
        System.out.print(Sisältö_ARVO);
    }

    @Override
    public int lukea_portti_tavu(int laitteisto_portin_numero) {
        Integer ARVO = laitteisto_portti_ARVO.get(Integer.valueOf(laitteisto_portin_numero));
        return ARVO == null ? 0 : ARVO.intValue();
    }

    @Override
    public void kirjoitus_portti_tavu(int laitteisto_portin_numero, int ARVO) {
        laitteisto_portti_ARVO.put(Integer.valueOf(laitteisto_portin_numero), Integer.valueOf(ARVO & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // isäntä 시험에서는 Seuraava_kohde 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

