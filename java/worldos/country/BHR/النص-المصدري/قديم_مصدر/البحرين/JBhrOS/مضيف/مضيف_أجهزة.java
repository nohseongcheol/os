// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package البحرين.JBhrOS.مضيف;

import java.util.HashMap;
import java.util.Map;
import البحرين.JBhrOS.نواة.أجهزة_قيمة;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 أجهزة_قيمة 대역이다. */
public final class مضيف_أجهزة implements أجهزة_قيمة {
    private final Map<Integer, Integer> أجهزة_منفذ_قيمة = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String محتوى_قيمة) {
        직렬기록.append(محتوى_قيمة);
        System.out.print(محتوى_قيمة);
    }

    @Override
    public int يقرأ_منفذ_بايت(int أجهزة_رقم_المنفذ) {
        Integer قيمة = أجهزة_منفذ_قيمة.get(Integer.valueOf(أجهزة_رقم_المنفذ));
        return قيمة == null ? 0 : قيمة.intValue();
    }

    @Override
    public void كتابة_منفذ_بايت(int أجهزة_رقم_المنفذ, int قيمة) {
        أجهزة_منفذ_قيمة.put(Integer.valueOf(أجهزة_رقم_المنفذ), Integer.valueOf(قيمة & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // مضيف 시험에서는 التالي_عنصر 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

