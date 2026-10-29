// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Словаччина.JSvkOS.хост;

import java.util.HashMap;
import java.util.Map;
import Словаччина.JSvkOS.Ядро.обладнання_значення;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 обладнання_значення 대역이다. */
public final class хост_обладнання implements обладнання_значення {
    private final Map<Integer, Integer> обладнання_порт_значення = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Вміст_значення) {
        직렬기록.append(Вміст_значення);
        System.out.print(Вміст_значення);
    }

    @Override
    public int 포트바이트읽기(int обладнання_номер_порту) {
        Integer значення = обладнання_порт_значення.get(Integer.valueOf(обладнання_номер_порту));
        return значення == null ? 0 : значення.intValue();
    }

    @Override
    public void записування_порт_байт(int обладнання_номер_порту, int значення) {
        обладнання_порт_значення.put(Integer.valueOf(обладнання_номер_порту), Integer.valueOf(значення & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // хост 시험에서는 Далі_елемент 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

