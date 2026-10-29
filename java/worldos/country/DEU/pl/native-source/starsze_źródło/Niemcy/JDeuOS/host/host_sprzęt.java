// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Niemcy.JDeuOS.host;

import java.util.HashMap;
import java.util.Map;
import Niemcy.JDeuOS.jądro.sprzęt_WARTOŚĆ;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 sprzęt_WARTOŚĆ 대역이다. */
public final class host_sprzęt implements sprzęt_WARTOŚĆ {
    private final Map<Integer, Integer> sprzęt_port_WARTOŚĆ = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String treść_WARTOŚĆ_cb0f2404) {
        직렬기록.append(treść_WARTOŚĆ_cb0f2404);
        System.out.print(treść_WARTOŚĆ_cb0f2404);
    }

    @Override
    public int 포트바이트읽기(int sprzęt_numer_portu) {
        Integer WARTOŚĆ = sprzęt_port_WARTOŚĆ.get(Integer.valueOf(sprzęt_numer_portu));
        return WARTOŚĆ == null ? 0 : WARTOŚĆ.intValue();
    }

    @Override
    public void zapis_port_bajt(int sprzęt_numer_portu, int WARTOŚĆ) {
        sprzęt_port_WARTOŚĆ.put(Integer.valueOf(sprzęt_numer_portu), Integer.valueOf(WARTOŚĆ & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // host 시험에서는 Dalej_towar 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

