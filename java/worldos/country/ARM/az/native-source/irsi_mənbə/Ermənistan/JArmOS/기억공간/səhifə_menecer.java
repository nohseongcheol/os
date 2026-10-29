// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ermənistan.JArmOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB səhifə_VALUE 연결과 Yazma 시 복사를 제공한다. */
public final class səhifə_menecer {
    public static final int səhifənin_ölçüsü = 4096;

    private static final class səhifə_VALUE {
        private byte[] verilənlər = new byte[səhifənin_ölçüsü];
        private int İstinad_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ünvan_məkan {
        private final Map<Integer, səhifə_VALUE> səhifə_cədvəl = new HashMap<Integer, səhifə_VALUE>();
    }

    public ünvan_məkan 새주소공간() {
        return new ünvan_məkan();
    }

    public void MAP_səhifə(ünvan_məkan 공간, int virtual_ünvan, boolean 쓰기가능) {
        int INDEX = 쪽번호(virtual_ünvan);
        səhifə_VALUE 새쪽 = new səhifə_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.səhifə_cədvəl.put(Integer.valueOf(INDEX), 새쪽);
    }

    public ünvan_məkan 쓰기시복사복제(ünvan_məkan 원본) {
        ünvan_məkan 복제본 = new ünvan_məkan();
        for (Map.Entry<Integer, səhifə_VALUE> daxiletmə_VALUE : 원본.səhifə_cədvəl.entrySet()) {
            səhifə_VALUE 공유쪽 = daxiletmə_VALUE.getValue();
            공유쪽.İstinad_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.səhifə_cədvəl.put(daxiletmə_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ünvan_məkan 공간, int virtual_ünvan) {
        səhifə_VALUE hədəf = FIND_səhifə(공간, virtual_ünvan);
        return hədəf.verilənlər[Math.floorMod(virtual_ünvan, səhifənin_ölçüsü)];
    }

    public void yazmaq_bayt_VALUE(ünvan_məkan 공간, int virtual_ünvan, byte VALUE) {
        int INDEX = 쪽번호(virtual_ünvan);
        səhifə_VALUE hədəf = FIND_səhifə(공간, virtual_ünvan);
        if (!hədəf.쓰기가능) {
            if (!hədəf.쓰기시복사) {
                throw new IllegalStateException("Oxuma 전용 쪽입니다.");
            }
            hədəf = yarat_özəl_səhifə(공간, INDEX, hədəf);
        }
        hədəf.verilənlər[Math.floorMod(virtual_ünvan, səhifənin_ölçüsü)] = VALUE;
    }

    public void 범위개인쓰기(ünvan_məkan 공간, int başlama_ünvanı, int Böyüklük) {
        if (Böyüklük < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int bitirmək_ünvan = Math.addExact(başlama_ünvanı, Böyüklük);
        for (int ünvan = başlama_ünvanı; ünvan < bitirmək_ünvan; ünvan = (쪽번호(ünvan) + 1) * səhifənin_ölçüsü) {
            int INDEX = 쪽번호(ünvan);
            səhifə_VALUE hədəf = FIND_səhifə(공간, ünvan);
            if (hədəf.쓰기시복사) {
                yarat_özəl_səhifə(공간, INDEX, hədəf);
            } else {
                hədəf.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ünvan_məkan 공간, int başlama_ünvanı, byte[] verilənlər) {
        for (int INDEX = 0; INDEX < verilənlər.length; INDEX++) {
            yazmaq_bayt_VALUE(공간, başlama_ünvanı + INDEX, verilənlər[INDEX]);
        }
    }

    private səhifə_VALUE yarat_özəl_səhifə(ünvan_məkan 공간, int INDEX, səhifə_VALUE 공유쪽) {
        səhifə_VALUE özəl_səhifə = new səhifə_VALUE();
        özəl_səhifə.verilənlər = Arrays.copyOf(공유쪽.verilənlər, 공유쪽.verilənlər.length);
        özəl_səhifə.쓰기가능 = true;
        özəl_səhifə.쓰기시복사 = false;
        공유쪽.İstinad_COUNT--;
        공간.səhifə_cədvəl.put(Integer.valueOf(INDEX), özəl_səhifə);
        return özəl_səhifə;
    }

    private səhifə_VALUE FIND_səhifə(ünvan_məkan 공간, int ünvan) {
        səhifə_VALUE hədəf = 공간.səhifə_cədvəl.get(Integer.valueOf(쪽번호(ünvan)));
        if (hədəf == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return hədəf;
    }

    private int 쪽번호(int ünvan) {
        if (ünvan < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ünvan / səhifənin_ölçüsü;
    }
}

