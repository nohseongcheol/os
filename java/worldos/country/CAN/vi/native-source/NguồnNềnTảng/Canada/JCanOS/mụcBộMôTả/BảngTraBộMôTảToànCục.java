// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.mụcBộMôTả;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Giữ cấu hình bảng mô tả toàn cục x86 và đoạn trạng thái tác vụ. */
public final class BảngTraBộMôTảToànCục {
    public static final class giáTrịĐoạn {
        private final int giáTrịNền;
        private final int giớiHạnRanhGiới;
        private final int giáTrịTruyCập;

        giáTrịĐoạn(int giáTrịNền, int giớiHạnRanhGiới, int giáTrịTruyCập) {
            this.giáTrịNền = giáTrịNền;
            this.giớiHạnRanhGiới = giớiHạnRanhGiới;
            this.giáTrịTruyCập = giáTrịTruyCập;
        }

        public int giáTrịNền() { return giáTrịNền; }
        public int giớiHạnRanhGiới() { return giớiHạnRanhGiới; }
        public int giáTrịTruyCập() { return giáTrịTruyCập; }
    }

    private final List<giáTrịĐoạn> danhSáchCácĐoạn = new ArrayList<giáTrịĐoạn>();

    public int thêmCuốiMục(int giáTrịNền, int giớiHạnRanhGiới, int giáTrịTruyCập) {
        danhSáchCácĐoạn.add(new giáTrịĐoạn(giáTrịNền, giớiHạnRanhGiới, giáTrịTruyCập));
        return (danhSáchCácĐoạn.size() - 1) * 8;
    }

    public List<giáTrịĐoạn> danhSáchCácĐoạn() {
        return Collections.unmodifiableList(danhSáchCácĐoạn);
    }

    public void đặtGiáTrịGiáTrịMặcĐịnh() {
        danhSáchCácĐoạn.clear();
        thêmCuốiMục(0, 0, 0);
        thêmCuốiMục(0, 0xfffff, 0x9a);
        thêmCuốiMục(0, 0xfffff, 0x92);
        thêmCuốiMục(0, 0xfffff, 0xfa);
        thêmCuốiMục(0, 0xfffff, 0xf2);
    }
}

