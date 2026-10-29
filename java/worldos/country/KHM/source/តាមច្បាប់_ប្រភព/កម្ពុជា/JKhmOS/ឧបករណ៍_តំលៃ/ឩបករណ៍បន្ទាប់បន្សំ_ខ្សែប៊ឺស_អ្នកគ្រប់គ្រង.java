// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.ឧបករណ៍_តំលៃ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ឧបករណ៍_តំលៃ 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ឩបករណ៍បន្ទាប់បន្សំ_ខ្សែប៊ឺស_អ្នកគ្រប់គ្រង {
    public static final class ឧបករណ៍_តំលៃ {
        private final int ក្រុមហ៊ុន_ផ្គត់ផ្គង់_ដ្រាយវឺ_អង្គសម្គាល់;
        private final int ឧបករណ៍_អង្គសម្គាល់;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ឧបករណ៍_តំលៃ(int ក្រុមហ៊ុន_ផ្គត់ផ្គង់_ដ្រាយវឺ_អង្គសម្គាល់, int ឧបករណ៍_អង្គសម្គាល់, int 입출력바탕, int 개입중단번호) {
            this.ក្រុមហ៊ុន_ផ្គត់ផ្គង់_ដ្រាយវឺ_អង្គសម្គាល់ = ក្រុមហ៊ុន_ផ្គត់ផ្គង់_ដ្រាយវឺ_អង្គសម្គាល់;
            this.ឧបករណ៍_អង្គសម្គាល់ = ឧបករណ៍_អង្គសម្គាល់;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int ក្រុមហ៊ុន_ផ្គត់ផ្គង់_ដ្រាយវឺ_អង្គសម្គាល់() { return ក្រុមហ៊ុន_ផ្គត់ផ្គង់_ដ្រាយវឺ_អង្គសម្គាល់; }
        public int ឧបករណ៍_អង្គសម្គាល់() { return ឧបករណ៍_អង្គសម្គាល់; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ឧបករណ៍_តំលៃ> ឧបករណ៍_បញ្ជី = new ArrayList<ឧបករណ៍_តំលៃ>();

    public void 발견(ឧបករណ៍_តំលៃ ឧបករណ៍_តំលៃ) {
        ឧបករណ៍_បញ្ជី.add(ឧបករណ៍_តំលៃ);
    }

    public List<ឧបករណ៍_តំលៃ> ឧបករណ៍_បញ្ជី() {
        return Collections.unmodifiableList(ឧបករណ៍_បញ្ជី);
    }

    public ឧបករណ៍_តំលៃ រក_ការបញ្ចូល(int ក្រុមហ៊ុន_ផ្គត់ផ្គង់_ដ្រាយវឺ_អង្គសម្គាល់, int ឧបករណ៍_អង្គសម្គាល់) {
        for (ឧបករណ៍_តំលៃ 후보 : ឧបករណ៍_បញ្ជី) {
            if (후보.ក្រុមហ៊ុន_ផ្គត់ផ្គង់_ដ្រាយវឺ_អង្គសម្គាល់ == ក្រុមហ៊ុន_ផ្គត់ផ្គង់_ដ្រាយវឺ_អង្គសម្គាល់ && 후보.ឧបករណ៍_អង្គសម្គាល់ == ឧបករណ៍_អង្គសម្គាល់) {
                return 후보;
            }
        }
        return null;
    }
}

