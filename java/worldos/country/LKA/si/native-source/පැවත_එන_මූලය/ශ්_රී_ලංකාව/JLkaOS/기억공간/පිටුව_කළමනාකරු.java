// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB පිටුව_අගය 연결과 ලිවීම 시 복사를 제공한다. */
public final class පිටුව_කළමනාකරු {
    public static final int පිටු_තරම = 4096;

    private static final class පිටුව_අගය {
        private byte[] දත්ත = new byte[පිටු_තරම];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class යොමුව_ස්ථානය {
        private final Map<Integer, පිටුව_අගය> පිටුව_වගුව = new HashMap<Integer, පිටුව_අගය>();
    }

    public යොමුව_ස්ථානය 새주소공간() {
        return new යොමුව_ස්ථානය();
    }

    public void සිතියම_පිටුව(යොමුව_ස්ථානය 공간, int අතාත්වික_යොමුව, boolean 쓰기가능) {
        int සූචිය = 쪽번호(අතාත්වික_යොමුව);
        පිටුව_අගය 새쪽 = new පිටුව_අගය();
        새쪽.쓰기가능 = 쓰기가능;
        공간.පිටුව_වගුව.put(Integer.valueOf(සූචිය), 새쪽);
    }

    public යොමුව_ස්ථානය 쓰기시복사복제(යොමුව_ස්ථානය 원본) {
        යොමුව_ස්ථානය 복제본 = new යොමුව_ස්ථානය();
        for (Map.Entry<Integer, පිටුව_අගය> පිවිසුම_අගය : 원본.පිටුව_වගුව.entrySet()) {
            පිටුව_අගය 공유쪽 = පිවිසුම_අගය.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.පිටුව_වගුව.put(පිවිසුම_අගය.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(යොමුව_ස්ථානය 공간, int අතාත්වික_යොමුව) {
        පිටුව_අගය ඉලක්කය = සොයන්න_පිටුව(공간, අතාත්වික_යොමුව);
        return ඉලක්කය.දත්ත[Math.floorMod(අතාත්වික_යොමුව, පිටු_තරම)];
    }

    public void ලියන්න_බයිටය_අගය(යොමුව_ස්ථානය 공간, int අතාත්වික_යොමුව, byte අගය) {
        int සූචිය = 쪽번호(අතාත්වික_යොමුව);
        පිටුව_අගය ඉලක්කය = සොයන්න_පිටුව(공간, අතාත්වික_යොමුව);
        if (!ඉලක්කය.쓰기가능) {
            if (!ඉලක්කය.쓰기시복사) {
                throw new IllegalStateException("කියවීම 전용 쪽입니다.");
            }
            ඉලක්කය = සාදන්න_පෞද්ගලික_පිටුව(공간, සූචිය, ඉලක්කය);
        }
        ඉලක්කය.දත්ත[Math.floorMod(අතාත්වික_යොමුව, පිටු_තරම)] = අගය;
    }

    public void 범위개인쓰기(යොමුව_ස්ථානය 공간, int ඇරඹුම_යොමුව, int ප්_රමාණය) {
        if (ප්_රමාණය < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int නිමා_කරන්න_යොමුව = Math.addExact(ඇරඹුම_යොමුව, ප්_රමාණය);
        for (int යොමුව = ඇරඹුම_යොමුව; යොමුව < නිමා_කරන්න_යොමුව; යොමුව = (쪽번호(යොමුව) + 1) * පිටු_තරම) {
            int සූචිය = 쪽번호(යොමුව);
            පිටුව_අගය ඉලක්කය = සොයන්න_පිටුව(공간, යොමුව);
            if (ඉලක්කය.쓰기시복사) {
                සාදන්න_පෞද්ගලික_පිටුව(공간, සූචිය, ඉලක්කය);
            } else {
                ඉලක්කය.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(යොමුව_ස්ථානය 공간, int ඇරඹුම_යොමුව, byte[] දත්ත) {
        for (int සූචිය = 0; සූචිය < දත්ත.length; සූචිය++) {
            ලියන්න_බයිටය_අගය(공간, ඇරඹුම_යොමුව + සූචිය, දත්ත[සූචිය]);
        }
    }

    private පිටුව_අගය සාදන්න_පෞද්ගලික_පිටුව(යොමුව_ස්ථානය 공간, int සූචිය, පිටුව_අගය 공유쪽) {
        පිටුව_අගය පෞද්ගලික_පිටුව = new පිටුව_අගය();
        පෞද්ගලික_පිටුව.දත්ත = Arrays.copyOf(공유쪽.දත්ත, 공유쪽.දත්ත.length);
        පෞද්ගලික_පිටුව.쓰기가능 = true;
        පෞද්ගලික_පිටුව.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.පිටුව_වගුව.put(Integer.valueOf(සූචිය), පෞද්ගලික_පිටුව);
        return පෞද්ගලික_පිටුව;
    }

    private පිටුව_අගය සොයන්න_පිටුව(යොමුව_ස්ථානය 공간, int යොමුව) {
        පිටුව_අගය ඉලක්කය = 공간.පිටුව_වගුව.get(Integer.valueOf(쪽번호(යොමුව)));
        if (ඉලක්කය == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ඉලක්කය;
    }

    private int 쪽번호(int යොමුව) {
        if (යොමුව < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return යොමුව / පිටු_තරම;
    }
}

