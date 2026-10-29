// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Беларусь.JBlrOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 стан_значэнне секцыя_значэнне 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Фон_значэнне;
        private final int 한계;
        private final int доступ_значэнне;

        조각(int Фон_значэнне, int 한계, int доступ_значэнне) {
            this.Фон_значэнне = Фон_значэнне;
            this.한계 = 한계;
            this.доступ_значэнне = доступ_значэнне;
        }

        public int Фон_значэнне() { return Фон_значэнне; }
        public int 한계() { return 한계; }
        public int доступ_значэнне() { return доступ_значэнне; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Фон_значэнне, int 한계, int доступ_значэнне) {
        조각들.add(new 조각(Фон_значэнне, 한계, доступ_значэнне));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void набор_значэнне_па_змаўчанні() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

