// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ουκρανία.JUkrOS.φιλοξενώ;

import java.util.HashMap;
import java.util.Map;
import Ουκρανία.JUkrOS.πυρήνας.υλικό_τιμή;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 υλικό_τιμή 대역이다. */
public final class φιλοξενώ_υλικό implements υλικό_τιμή {
    private final Map<Integer, Integer> υλικό_θύρα_τιμή = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Περιεχόμενο_τιμή) {
        직렬기록.append(Περιεχόμενο_τιμή);
        System.out.print(Περιεχόμενο_τιμή);
    }

    @Override
    public int 포트바이트읽기(int υλικό_αριθμός_θύρας) {
        Integer τιμή = υλικό_θύρα_τιμή.get(Integer.valueOf(υλικό_αριθμός_θύρας));
        return τιμή == null ? 0 : τιμή.intValue();
    }

    @Override
    public void 포트바이트쓰기(int υλικό_αριθμός_θύρας, int τιμή) {
        υλικό_θύρα_τιμή.put(Integer.valueOf(υλικό_αριθμός_θύρας), Integer.valueOf(τιμή & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // φιλοξενώ 시험에서는 Επόμενο_στοιχείο 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

