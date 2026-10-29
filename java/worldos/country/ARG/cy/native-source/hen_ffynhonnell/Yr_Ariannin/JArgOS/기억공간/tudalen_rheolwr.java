// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yr_Ariannin.JArgOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB tudalen_VALUE 연결과 Ysgrifennu 시 복사를 제공한다. */
public final class tudalen_rheolwr {
    public static final int maint_tudalen = 4096;

    private static final class tudalen_VALUE {
        private byte[] data = new byte[maint_tudalen];
        private int cyfeiriad_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ADDRESS_lle {
        private final Map<Integer, tudalen_VALUE> tudalen_tabl = new HashMap<Integer, tudalen_VALUE>();
    }

    public ADDRESS_lle 새주소공간() {
        return new ADDRESS_lle();
    }

    public void MAP_tudalen(ADDRESS_lle 공간, int rhith_gyfeiriad, boolean 쓰기가능) {
        int INDEX = 쪽번호(rhith_gyfeiriad);
        tudalen_VALUE 새쪽 = new tudalen_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.tudalen_tabl.put(Integer.valueOf(INDEX), 새쪽);
    }

    public ADDRESS_lle 쓰기시복사복제(ADDRESS_lle 원본) {
        ADDRESS_lle 복제본 = new ADDRESS_lle();
        for (Map.Entry<Integer, tudalen_VALUE> cofnod_VALUE : 원본.tudalen_tabl.entrySet()) {
            tudalen_VALUE 공유쪽 = cofnod_VALUE.getValue();
            공유쪽.cyfeiriad_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.tudalen_tabl.put(cofnod_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ADDRESS_lle 공간, int rhith_gyfeiriad) {
        tudalen_VALUE targed = FIND_tudalen(공간, rhith_gyfeiriad);
        return targed.data[Math.floorMod(rhith_gyfeiriad, maint_tudalen)];
    }

    public void ysgrifennu_beit_VALUE(ADDRESS_lle 공간, int rhith_gyfeiriad, byte VALUE) {
        int INDEX = 쪽번호(rhith_gyfeiriad);
        tudalen_VALUE targed = FIND_tudalen(공간, rhith_gyfeiriad);
        if (!targed.쓰기가능) {
            if (!targed.쓰기시복사) {
                throw new IllegalStateException("Darllen 전용 쪽입니다.");
            }
            targed = Creu_preifat_tudalen(공간, INDEX, targed);
        }
        targed.data[Math.floorMod(rhith_gyfeiriad, maint_tudalen)] = VALUE;
    }

    public void 범위개인쓰기(ADDRESS_lle 공간, int cyfeiriad_cychwyn, int Maint) {
        if (Maint < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int gorffen_ADDRESS = Math.addExact(cyfeiriad_cychwyn, Maint);
        for (int ADDRESS = cyfeiriad_cychwyn; ADDRESS < gorffen_ADDRESS; ADDRESS = (쪽번호(ADDRESS) + 1) * maint_tudalen) {
            int INDEX = 쪽번호(ADDRESS);
            tudalen_VALUE targed = FIND_tudalen(공간, ADDRESS);
            if (targed.쓰기시복사) {
                Creu_preifat_tudalen(공간, INDEX, targed);
            } else {
                targed.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ADDRESS_lle 공간, int cyfeiriad_cychwyn, byte[] data) {
        for (int INDEX = 0; INDEX < data.length; INDEX++) {
            ysgrifennu_beit_VALUE(공간, cyfeiriad_cychwyn + INDEX, data[INDEX]);
        }
    }

    private tudalen_VALUE Creu_preifat_tudalen(ADDRESS_lle 공간, int INDEX, tudalen_VALUE 공유쪽) {
        tudalen_VALUE preifat_tudalen = new tudalen_VALUE();
        preifat_tudalen.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        preifat_tudalen.쓰기가능 = true;
        preifat_tudalen.쓰기시복사 = false;
        공유쪽.cyfeiriad_COUNT--;
        공간.tudalen_tabl.put(Integer.valueOf(INDEX), preifat_tudalen);
        return preifat_tudalen;
    }

    private tudalen_VALUE FIND_tudalen(ADDRESS_lle 공간, int ADDRESS) {
        tudalen_VALUE targed = 공간.tudalen_tabl.get(Integer.valueOf(쪽번호(ADDRESS)));
        if (targed == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return targed;
    }

    private int 쪽번호(int ADDRESS) {
        if (ADDRESS < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ADDRESS / maint_tudalen;
    }
}

