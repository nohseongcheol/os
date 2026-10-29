// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.ଆୟୋଜକ;

import java.util.HashMap;
import java.util.Map;
import ଭାରତ.JIndOS.କେନ୍ଦ୍ରିକ.ହାର୍ଡୱେର୍_ମୂଲ୍ୟ;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 ହାର୍ଡୱେର୍_ମୂଲ୍ୟ 대역이다. */
public final class ଆୟୋଜକ_ହାର୍ଡୱେର୍ implements ହାର୍ଡୱେର୍_ମୂଲ୍ୟ {
    private final Map<Integer, Integer> ହାର୍ଡୱେର୍_ପୋର୍ଟ_ମୂଲ୍ୟ = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String ବିଷୟ_ମୂଲ୍ୟ) {
        직렬기록.append(ବିଷୟ_ମୂଲ୍ୟ);
        System.out.print(ବିଷୟ_ମୂଲ୍ୟ);
    }

    @Override
    public int 포트바이트읽기(int ହାର୍ଡୱେର୍_ପୋର୍ଟ୍_ନମ୍ଵର୍) {
        Integer ମୂଲ୍ୟ = ହାର୍ଡୱେର୍_ପୋର୍ଟ_ମୂଲ୍ୟ.get(Integer.valueOf(ହାର୍ଡୱେର୍_ପୋର୍ଟ୍_ନମ୍ଵର୍));
        return ମୂଲ୍ୟ == null ? 0 : ମୂଲ୍ୟ.intValue();
    }

    @Override
    public void ଲିଖନ_ପୋର୍ଟ_ବାଇଟ୍(int ହାର୍ଡୱେର୍_ପୋର୍ଟ୍_ନମ୍ଵର୍, int ମୂଲ୍ୟ) {
        ହାର୍ଡୱେର୍_ପୋର୍ଟ_ମୂଲ୍ୟ.put(Integer.valueOf(ହାର୍ଡୱେର୍_ପୋର୍ଟ୍_ନମ୍ଵର୍), Integer.valueOf(ମୂଲ୍ୟ & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // ଆୟୋଜକ 시험에서는 ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

