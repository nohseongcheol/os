// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ዞን_እሴት ክፍል_እሴት 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int ልጣፍ_እሴት;
        private final int 한계;
        private final int መዳረሻ_እሴት;

        조각(int ልጣፍ_እሴት, int 한계, int መዳረሻ_እሴት) {
            this.ልጣፍ_እሴት = ልጣፍ_እሴት;
            this.한계 = 한계;
            this.መዳረሻ_እሴት = መዳረሻ_እሴት;
        }

        public int ልጣፍ_እሴት() { return ልጣፍ_እሴት; }
        public int 한계() { return 한계; }
        public int መዳረሻ_እሴት() { return መዳረሻ_እሴት; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int ልጣፍ_እሴት, int 한계, int መዳረሻ_እሴት) {
        조각들.add(new 조각(ልጣፍ_እሴት, 한계, መዳረሻ_እሴት));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ስብስብ_ነባሪ_እሴት() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

