// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.ឯកសារនៃប្រព័ន្ធ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian អនុវត្ត_ពាក្យបញ្ជា 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class ផ្នែក_តំលៃ {
        private final int 종류;
        private final int ទង់_តំលៃ;
        private final int អ៊ីម៉ែល;
        private final int ឯកសារ_កំណត់ទីតាំង;
        private final int ដាក់ទំហំ;

        ផ្នែក_តំលៃ(int 종류, int ទង់_តំលៃ, int អ៊ីម៉ែល, int ឯកសារ_កំណត់ទីតាំង, int ដាក់ទំហំ) {
            this.종류 = 종류;
            this.ទង់_តំលៃ = ទង់_តំលៃ;
            this.អ៊ីម៉ែល = អ៊ីម៉ែល;
            this.ឯកសារ_កំណត់ទីតាំង = ឯកសារ_កំណត់ទីតាំង;
            this.ដាក់ទំហំ = ដាក់ទំហំ;
        }

        public int 종류() {
            return 종류;
        }

        public int ទង់_តំលៃ() {
            return ទង់_តំលៃ;
        }

        public int អ៊ីម៉ែល() {
            return អ៊ីម៉ែល;
        }

        public int ឯកសារ_កំណត់ទីតាំង() {
            return ឯកសារ_កំណត់ទីតាំង;
        }

        public int ដាក់ទំហំ() {
            return ដាក់ទំហំ;
        }
    }

    public static final class រូបថត {
        private final int ផ្តើម_អ៊ីម៉ែល;
        private final List<ផ្នែក_តំលៃ> 구역들;

        រូបថត(int ផ្តើម_អ៊ីម៉ែល, List<ផ្នែក_តំលៃ> 구역들) {
            this.ផ្តើម_អ៊ីម៉ែល = ផ្តើម_អ៊ីម៉ែល;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ផ្តើម_អ៊ីម៉ែល() {
            return ផ្តើម_អ៊ីម៉ែល;
        }

        public List<ផ្នែក_តំលៃ> 구역들() {
            return 구역들;
        }
    }

    public រូបថត 검사(byte[] ទិន្នន័យ) {
        if (ទិន្នន័យ == null || ទិន្នន័យ.length < 52
                || ទិន្នន័យ[0] != 0x7f || ទិន្នន័យ[1] != 'E' || ទិន្នន័យ[2] != 'L' || ទិន្នន័យ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ទិន្នន័យ[4] != 1 || ទិន្នន័យ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ផ្តើម_អ៊ីម៉ែល = ញែក_ចំនួនគត់(ទិន្នន័យ, 24);
        int ផ្នែក_តារាង_កំណត់ទីតាំង = ញែក_ចំនួនគត់(ទិន្នន័យ, 32);
        int ផ្នែក_ការបញ្ចូល_ដាក់ទំហំ = 짧은정수읽기(ទិន្នន័យ, 46);
        int 구역수 = 짧은정수읽기(ទិន្នន័យ, 48);
        if (ផ្នែក_ការបញ្ចូល_ដាក់ទំហំ < 40 || ផ្នែក_តារាង_កំណត់ទីតាំង < 0
                || (long) ផ្នែក_តារាង_កំណត់ទីតាំង + (long) ផ្នែក_ការបញ្ចូល_ដាក់ទំហំ * 구역수 > ទិន្នន័យ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ផ្នែក_តំលៃ> 구역들 = new ArrayList<ផ្នែក_តំលៃ>();
        for (int សន្ទស្សន៏ = 0; សន្ទស្សន៏ < 구역수; សន្ទស្សន៏++) {
            int កំណត់ទីតាំង = ផ្នែក_តារាង_កំណត់ទីតាំង + សន្ទស្សន៏ * ផ្នែក_ការបញ្ចូល_ដាក់ទំហំ;
            int 종류 = ញែក_ចំនួនគត់(ទិន្នន័យ, កំណត់ទីតាំង + 4);
            int ទង់_តំលៃ = ញែក_ចំនួនគត់(ទិន្នន័យ, កំណត់ទីតាំង + 8);
            int អ៊ីម៉ែល = ញែក_ចំនួនគត់(ទិន្នន័យ, កំណត់ទីតាំង + 12);
            int ឯកសារ_កំណត់ទីតាំង = ញែក_ចំនួនគត់(ទិន្នន័យ, កំណត់ទីតាំង + 16);
            int ដាក់ទំហំ = ញែក_ចំនួនគត់(ទិន្នន័យ, កំណត់ទីតាំង + 20);
            if (ដាក់ទំហំ < 0 || (종류 != 8 && ((long) ឯកសារ_កំណត់ទីតាំង + ដាក់ទំហំ > ទិន្នន័យ.length || ឯកសារ_កំណត់ទីតាំង < 0))) {
                throw new IllegalArgumentException("ELF ផ្នែក_តំលៃ ទិន្នន័យ 범위가 올바르지 않습니다.");
            }
            구역들.add(new ផ្នែក_តំលៃ(종류, ទង់_តំលៃ, អ៊ីម៉ែល, ឯកសារ_កំណត់ទីតាំង, ដាក់ទំហំ));
        }
        return new រូបថត(ផ្តើម_អ៊ីម៉ែល, 구역들);
    }

    private int ញែក_ចំនួនគត់(byte[] ទិន្នន័យ, int កំណត់ទីតាំង) {
        if (កំណត់ទីតាំង < 0 || កំណត់ទីតាំង > ទិន្នន័យ.length - 4) {
            throw new IllegalArgumentException("ELF ចំនួនគត់ 범위를 벗어났습니다.");
        }
        return (ទិន្នន័យ[កំណត់ទីតាំង] & 0xff)
                | ((ទិន្នន័យ[កំណត់ទីតាំង + 1] & 0xff) << 8)
                | ((ទិន្នន័យ[កំណត់ទីតាំង + 2] & 0xff) << 16)
                | ((ទិន្នន័យ[កំណត់ទីតាំង + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ទិន្នន័យ, int កំណត់ទីតាំង) {
        if (កំណត់ទីតាំង < 0 || កំណត់ទីតាំង > ទិន្នន័យ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ចំនួនគត់ 범위를 벗어났습니다.");
        }
        return (ទិន្នន័យ[កំណត់ទីតាំង] & 0xff) | ((ទិន្នន័យ[កំណត់ទីតាំង + 1] & 0xff) << 8);
    }
}
