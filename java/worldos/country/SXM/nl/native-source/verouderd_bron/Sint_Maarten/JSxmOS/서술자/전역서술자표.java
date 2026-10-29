// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sint_Maarten.JSxmOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Status_WAARDE sectie_WAARDE 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Achtergrond_WAARDE;
        private final int 한계;
        private final int toegang_WAARDE;

        조각(int Achtergrond_WAARDE, int 한계, int toegang_WAARDE) {
            this.Achtergrond_WAARDE = Achtergrond_WAARDE;
            this.한계 = 한계;
            this.toegang_WAARDE = toegang_WAARDE;
        }

        public int Achtergrond_WAARDE() { return Achtergrond_WAARDE; }
        public int 한계() { return 한계; }
        public int toegang_WAARDE() { return toegang_WAARDE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int toevoegen_invoer(int Achtergrond_WAARDE, int 한계, int toegang_WAARDE) {
        조각들.add(new 조각(Achtergrond_WAARDE, 한계, toegang_WAARDE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void set_standaardwaarde() {
        조각들.clear();
        toevoegen_invoer(0, 0, 0);
        toevoegen_invoer(0, 0xfffff, 0x9a);
        toevoegen_invoer(0, 0xfffff, 0x92);
        toevoegen_invoer(0, 0xfffff, 0xfa);
        toevoegen_invoer(0, 0xfffff, 0xf2);
    }
}

