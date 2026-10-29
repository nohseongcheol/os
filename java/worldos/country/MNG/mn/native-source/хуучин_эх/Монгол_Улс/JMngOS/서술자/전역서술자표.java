// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол_Улс.JMngOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 төлөв_утга хэсэг_утга 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Дэвсгэр_утга;
        private final int 한계;
        private final int хандах_утга;

        조각(int Дэвсгэр_утга, int 한계, int хандах_утга) {
            this.Дэвсгэр_утга = Дэвсгэр_утга;
            this.한계 = 한계;
            this.хандах_утга = хандах_утга;
        }

        public int Дэвсгэр_утга() { return Дэвсгэр_утга; }
        public int 한계() { return 한계; }
        public int хандах_утга() { return хандах_утга; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Дэвсгэр_утга, int 한계, int хандах_утга) {
        조각들.add(new 조각(Дэвсгэр_утга, 한계, хандах_утга));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void багц_өгөгдмөл_утга() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

