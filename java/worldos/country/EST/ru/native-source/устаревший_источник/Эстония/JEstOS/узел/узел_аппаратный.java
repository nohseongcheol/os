// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Эстония.JEstOS.узел;

import java.util.HashMap;
import java.util.Map;
import Эстония.JEstOS.Ядро.аппаратный_ЗНАЧЕН;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 аппаратный_ЗНАЧЕН 대역이다. */
public final class узел_аппаратный implements аппаратный_ЗНАЧЕН {
    private final Map<Integer, Integer> аппаратный_порт_ЗНАЧЕН = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String контент_ЗНАЧЕН) {
        직렬기록.append(контент_ЗНАЧЕН);
        System.out.print(контент_ЗНАЧЕН);
    }

    @Override
    public int чтение_порт_байт(int аппаратный_номер_порта) {
        Integer ЗНАЧЕН = аппаратный_порт_ЗНАЧЕН.get(Integer.valueOf(аппаратный_номер_порта));
        return ЗНАЧЕН == null ? 0 : ЗНАЧЕН.intValue();
    }

    @Override
    public void запись_порт_байт(int аппаратный_номер_порта, int ЗНАЧЕН) {
        аппаратный_порт_ЗНАЧЕН.put(Integer.valueOf(аппаратный_номер_порта), Integer.valueOf(ЗНАЧЕН & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // узел 시험에서는 Далее_товар 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

