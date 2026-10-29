// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Trung_Quốc.JChnOS.VùngNhớ;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** Đảm nhiệm cấp phát căn chỉnh, giải phóng và gộp vùng bộ nhớ vật lý. */
public final class BộQuảnLýBộNhớ {
    private final byte[] VùngNhớ;
    private final TreeMap<Integer, Integer> miềnRỗng = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> miềnĐãDùng = new TreeMap<Integer, Integer>();

    public BộQuảnLýBộNhớ(int cỡTổngCộng) {
        if (cỡTổngCộng < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        VùngNhớ = new byte[cỡTổngCộng];
        miềnRỗng.put(Integer.valueOf(4096), Integer.valueOf(cỡTổngCộng - 4096));
    }

    public synchronized int cấpPhátLưuTrữ(int cỡ) {
        return cấpPhátĐãCănChỉnh(cỡ, 1);
    }

    public synchronized int cấpPhátĐãCănChỉnh(int cỡ, int giáTrịCănChỉnh) {
        if (cỡ <= 0 || giáTrịCănChỉnh <= 0 || (giáTrịCănChỉnh & (giáTrịCănChỉnh - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> giáTrịMục : miềnRỗng.entrySet()) {
            int chạy = giáTrịMục.getKey().intValue();
            int cỡMiền = giáTrịMục.getValue().intValue();
            int bắtChạyĐãCănChỉnh = (chạy + giáTrịCănChỉnh - 1) & -giáTrịCănChỉnh;
            int cỡGiáTrịPhíaTrước = bắtChạyĐãCănChỉnh - chạy;
            int cỡCuốiCùng = cỡMiền - cỡGiáTrịPhíaTrước - cỡ;
            if (cỡCuốiCùng < 0) {
                continue;
            }
            miềnRỗng.remove(Integer.valueOf(chạy));
            if (cỡGiáTrịPhíaTrước > 0) {
                miềnRỗng.put(Integer.valueOf(chạy), Integer.valueOf(cỡGiáTrịPhíaTrước));
            }
            if (cỡCuốiCùng > 0) {
                miềnRỗng.put(Integer.valueOf(bắtChạyĐãCănChỉnh + cỡ), Integer.valueOf(cỡCuốiCùng));
            }
            miềnĐãDùng.put(Integer.valueOf(bắtChạyĐãCănChỉnh), Integer.valueOf(cỡ));
            Arrays.fill(VùngNhớ, bắtChạyĐãCănChỉnh, bắtChạyĐãCănChỉnh + cỡ, (byte) 0);
            return bắtChạyĐãCănChỉnh;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void giảiPhóngLưuTrữ(int địaChỉ) {
        Integer đốiTượngCỡ = miềnĐãDùng.remove(Integer.valueOf(địaChỉ));
        if (đốiTượngCỡ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int chạy = địaChỉ;
        int cỡ = đốiTượngCỡ.intValue();
        Map.Entry<Integer, Integer> giáTrịPhíaTrước = miềnRỗng.lowerEntry(Integer.valueOf(chạy));
        if (giáTrịPhíaTrước != null && giáTrịPhíaTrước.getKey().intValue() + giáTrịPhíaTrước.getValue().intValue() == chạy) {
            chạy = giáTrịPhíaTrước.getKey().intValue();
            cỡ += giáTrịPhíaTrước.getValue().intValue();
            miềnRỗng.remove(giáTrịPhíaTrước.getKey());
        }
        Map.Entry<Integer, Integer> giáTrịLùi = miềnRỗng.ceilingEntry(Integer.valueOf(chạy));
        if (giáTrịLùi != null && chạy + cỡ == giáTrịLùi.getKey().intValue()) {
            cỡ += giáTrịLùi.getValue().intValue();
            miềnRỗng.remove(giáTrịLùi.getKey());
        }
        miềnRỗng.put(Integer.valueOf(chạy), Integer.valueOf(cỡ));
    }

    public synchronized byte đọcGiáTrịByte(int địaChỉ) {
        kiểmTraKhoảng(địaChỉ, 1);
        return VùngNhớ[địaChỉ];
    }

    public synchronized void ghiGiáTrịByte(int địaChỉ, byte giáTrị) {
        kiểmTraKhoảng(địaChỉ, 1);
        VùngNhớ[địaChỉ] = giáTrị;
    }

    public synchronized int cỡTổngCộng() {
        return VùngNhớ.length;
    }

    public synchronized int cỡĐãDùng() {
        int giáTrịTổngCộng = 0;
        for (Integer cỡ : miềnĐãDùng.values()) {
            giáTrịTổngCộng += cỡ.intValue();
        }
        return giáTrịTổngCộng;
    }

    private void kiểmTraKhoảng(int địaChỉ, int cỡ) {
        if (địaChỉ < 0 || cỡ < 0 || địaChỉ > VùngNhớ.length - cỡ) {
            throw new IndexOutOfBoundsException("VùngNhớ 범위를 벗어났습니다.");
        }
    }
}

