// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package இந்தியா.JIndOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 நிலை_மதிப்பு_e10195a1 பிரிவு_மதிப்பு 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int பின்புல_மதிப்பு;
        private final int 한계;
        private final int அணுகு_மதிப்பு;

        조각(int பின்புல_மதிப்பு, int 한계, int அணுகு_மதிப்பு) {
            this.பின்புல_மதிப்பு = பின்புல_மதிப்பு;
            this.한계 = 한계;
            this.அணுகு_மதிப்பு = அணுகு_மதிப்பு;
        }

        public int பின்புல_மதிப்பு() { return பின்புல_மதிப்பு; }
        public int 한계() { return 한계; }
        public int அணுகு_மதிப்பு() { return அணுகு_மதிப்பு; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int பின்புல_மதிப்பு, int 한계, int அணுகு_மதிப்பு) {
        조각들.add(new 조각(பின்புல_மதிப்பு, 한계, அணுகு_மதிப்பு));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void அமை_இயல்புநிலை_மதிப்பு() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

