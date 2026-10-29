// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.usu;

import java.util.HashMap;
import java.util.Map;
import Naịjịrịa.JNgaOS.mkpụrụobī_kọmpùta.ngwaike_valuu;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 ngwaike_valuu 대역이다. */
public final class usu_ngwaike implements ngwaike_valuu {
    private final Map<Integer, Integer> ngwaike_pọọt_valuu = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String ndịnà_valuu) {
        직렬기록.append(ndịnà_valuu);
        System.out.print(ndịnà_valuu);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer valuu = ngwaike_pọọt_valuu.get(Integer.valueOf(포트번호));
        return valuu == null ? 0 : valuu.intValue();
    }

    @Override
    public void dee_pọọt_baịtị(int 포트번호, int valuu) {
        ngwaike_pọọt_valuu.put(Integer.valueOf(포트번호), Integer.valueOf(valuu & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // usu 시험에서는 다음 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

