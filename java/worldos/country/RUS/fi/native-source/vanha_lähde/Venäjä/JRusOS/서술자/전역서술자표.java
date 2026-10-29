// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Venäjä.JRusOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Tila_ARVO osa_ARVO 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Tausta_ARVO;
        private final int 한계;
        private final int pääsy_ARVO;

        조각(int Tausta_ARVO, int 한계, int pääsy_ARVO) {
            this.Tausta_ARVO = Tausta_ARVO;
            this.한계 = 한계;
            this.pääsy_ARVO = pääsy_ARVO;
        }

        public int Tausta_ARVO() { return Tausta_ARVO; }
        public int 한계() { return 한계; }
        public int pääsy_ARVO() { return pääsy_ARVO; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int liitä_merkintä(int Tausta_ARVO, int 한계, int pääsy_ARVO) {
        조각들.add(new 조각(Tausta_ARVO, 한계, pääsy_ARVO));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ryhmä_oletusarvo() {
        조각들.clear();
        liitä_merkintä(0, 0, 0);
        liitä_merkintä(0, 0xfffff, 0x9a);
        liitä_merkintä(0, 0xfffff, 0x92);
        liitä_merkintä(0, 0xfffff, 0xfa);
        liitä_merkintä(0, 0xfffff, 0xf2);
    }
}

