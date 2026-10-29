// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hoa_Kỳ.JUsaOS.Chủ;

import java.util.HashMap;
import java.util.Map;
import Hoa_Kỳ.JUsaOS.Nhân.giáTrịPhầnCứng;

/** Phần cứng thay thế để kiểm thử tất định nhân được quản lý trên JVM thông thường. */
public final class PhầnCứngChủ implements giáTrịPhầnCứng {
    private final Map<Integer, Integer> giáTrịCổngPhầnCứng = new HashMap<Integer, Integer>();
    private final StringBuilder nhậtKýNốiTiếp = new StringBuilder();

    @Override
    public void đầuRaNốiTiếp(String giáTrịNộiDung) {
        nhậtKýNốiTiếp.append(giáTrịNộiDung);
        System.out.print(giáTrịNộiDung);
    }

    @Override
    public int đọcByteCổng(int sốCổngPhầnCứng) {
        Integer giáTrị = giáTrịCổngPhầnCứng.get(Integer.valueOf(sốCổngPhầnCứng));
        return giáTrị == null ? 0 : giáTrị.intValue();
    }

    @Override
    public void ghiByteCổng(int sốCổngPhầnCứng, int giáTrị) {
        giáTrịCổngPhầnCứng.put(Integer.valueOf(sốCổngPhầnCứng), Integer.valueOf(giáTrị & 0xff));
    }

    @Override
    public void cPUDừngHẳn() {
        // Trong phép thử trên máy chủ, trả về ngay thay vì chờ sự kiện tiếp theo.
    }

    public String nhậtKýNốiTiếp() {
        return nhậtKýNốiTiếp.toString();
    }
}

