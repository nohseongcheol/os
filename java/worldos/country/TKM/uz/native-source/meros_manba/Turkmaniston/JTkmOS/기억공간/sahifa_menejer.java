// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkmaniston.JTkmOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB sahifa_VALUE 연결과 Yozish 시 복사를 제공한다. */
public final class sahifa_menejer {
    public static final int sahifa_o_lchami = 4096;

    private static final class sahifa_VALUE {
        private byte[] ma_lumotlar = new byte[sahifa_o_lchami];
        private int Ma_lumotnomalar_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class manzil_joy {
        private final Map<Integer, sahifa_VALUE> sahifa_jadval = new HashMap<Integer, sahifa_VALUE>();
    }

    public manzil_joy 새주소공간() {
        return new manzil_joy();
    }

    public void MAP_sahifa(manzil_joy 공간, int virtual_manzil, boolean 쓰기가능) {
        int INDEX = 쪽번호(virtual_manzil);
        sahifa_VALUE 새쪽 = new sahifa_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.sahifa_jadval.put(Integer.valueOf(INDEX), 새쪽);
    }

    public manzil_joy 쓰기시복사복제(manzil_joy 원본) {
        manzil_joy 복제본 = new manzil_joy();
        for (Map.Entry<Integer, sahifa_VALUE> kiritish_VALUE : 원본.sahifa_jadval.entrySet()) {
            sahifa_VALUE 공유쪽 = kiritish_VALUE.getValue();
            공유쪽.Ma_lumotnomalar_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.sahifa_jadval.put(kiritish_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(manzil_joy 공간, int virtual_manzil) {
        sahifa_VALUE nishon = FIND_sahifa(공간, virtual_manzil);
        return nishon.ma_lumotlar[Math.floorMod(virtual_manzil, sahifa_o_lchami)];
    }

    public void yozmoq_bayt_VALUE(manzil_joy 공간, int virtual_manzil, byte VALUE) {
        int INDEX = 쪽번호(virtual_manzil);
        sahifa_VALUE nishon = FIND_sahifa(공간, virtual_manzil);
        if (!nishon.쓰기가능) {
            if (!nishon.쓰기시복사) {
                throw new IllegalStateException("Oʻqish 전용 쪽입니다.");
            }
            nishon = Yaratish_Shaxsiy_sahifa(공간, INDEX, nishon);
        }
        nishon.ma_lumotlar[Math.floorMod(virtual_manzil, sahifa_o_lchami)] = VALUE;
    }

    public void 범위개인쓰기(manzil_joy 공간, int Start_manzil, int Hajmi) {
        if (Hajmi < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int to_xtatmoq_manzil = Math.addExact(Start_manzil, Hajmi);
        for (int manzil = Start_manzil; manzil < to_xtatmoq_manzil; manzil = (쪽번호(manzil) + 1) * sahifa_o_lchami) {
            int INDEX = 쪽번호(manzil);
            sahifa_VALUE nishon = FIND_sahifa(공간, manzil);
            if (nishon.쓰기시복사) {
                Yaratish_Shaxsiy_sahifa(공간, INDEX, nishon);
            } else {
                nishon.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(manzil_joy 공간, int Start_manzil, byte[] ma_lumotlar) {
        for (int INDEX = 0; INDEX < ma_lumotlar.length; INDEX++) {
            yozmoq_bayt_VALUE(공간, Start_manzil + INDEX, ma_lumotlar[INDEX]);
        }
    }

    private sahifa_VALUE Yaratish_Shaxsiy_sahifa(manzil_joy 공간, int INDEX, sahifa_VALUE 공유쪽) {
        sahifa_VALUE Shaxsiy_sahifa = new sahifa_VALUE();
        Shaxsiy_sahifa.ma_lumotlar = Arrays.copyOf(공유쪽.ma_lumotlar, 공유쪽.ma_lumotlar.length);
        Shaxsiy_sahifa.쓰기가능 = true;
        Shaxsiy_sahifa.쓰기시복사 = false;
        공유쪽.Ma_lumotnomalar_COUNT--;
        공간.sahifa_jadval.put(Integer.valueOf(INDEX), Shaxsiy_sahifa);
        return Shaxsiy_sahifa;
    }

    private sahifa_VALUE FIND_sahifa(manzil_joy 공간, int manzil) {
        sahifa_VALUE nishon = 공간.sahifa_jadval.get(Integer.valueOf(쪽번호(manzil)));
        if (nishon == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return nishon;
    }

    private int 쪽번호(int manzil) {
        if (manzil < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return manzil / sahifa_o_lchami;
    }
}

