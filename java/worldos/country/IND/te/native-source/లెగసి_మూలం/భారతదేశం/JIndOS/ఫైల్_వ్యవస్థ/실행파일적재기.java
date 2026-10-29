// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.ఫైల్_వ్యవస్థ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian అమలు_చేయి_ఆదేశం 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class విభాగం_మూల్యం {
        private final int 종류;
        private final int పతాకం_మూల్యం;
        private final int ఇమెయిల్;
        private final int ఫైలు_స్థాయి;
        private final int పరిమాణం;

        విభాగం_మూల్యం(int 종류, int పతాకం_మూల్యం, int ఇమెయిల్, int ఫైలు_స్థాయి, int పరిమాణం) {
            this.종류 = 종류;
            this.పతాకం_మూల్యం = పతాకం_మూల్యం;
            this.ఇమెయిల్ = ఇమెయిల్;
            this.ఫైలు_స్థాయి = ఫైలు_స్థాయి;
            this.పరిమాణం = పరిమాణం;
        }

        public int 종류() {
            return 종류;
        }

        public int పతాకం_మూల్యం() {
            return పతాకం_మూల్యం;
        }

        public int ఇమెయిల్() {
            return ఇమెయిల్;
        }

        public int ఫైలు_స్థాయి() {
            return ఫైలు_స్థాయి;
        }

        public int పరిమాణం() {
            return పరిమాణం;
        }
    }

    public static final class చిత్రం {
        private final int ప్రారంభం_ఇమెయిల్;
        private final List<విభాగం_మూల్యం> 구역들;

        చిత్రం(int ప్రారంభం_ఇమెయిల్, List<విభాగం_మూల్యం> 구역들) {
            this.ప్రారంభం_ఇమెయిల్ = ప్రారంభం_ఇమెయిల్;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ప్రారంభం_ఇమెయిల్() {
            return ప్రారంభం_ఇమెయిల్;
        }

        public List<విభాగం_మూల్యం> 구역들() {
            return 구역들;
        }
    }

    public చిత్రం 검사(byte[] డేటా) {
        if (డేటా == null || డేటా.length < 52
                || డేటా[0] != 0x7f || డేటా[1] != 'E' || డేటా[2] != 'L' || డేటా[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (డేటా[4] != 1 || డేటా[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ప్రారంభం_ఇమెయిల్ = పార్స్_పూర్ణాంకం(డేటా, 24);
        int విభాగం_పట్టిక_స్థాయి = పార్స్_పూర్ణాంకం(డేటా, 32);
        int విభాగం_ప్రవేశం_పరిమాణం_మార్చు = 짧은정수읽기(డేటా, 46);
        int 구역수 = 짧은정수읽기(డేటా, 48);
        if (విభాగం_ప్రవేశం_పరిమాణం_మార్చు < 40 || విభాగం_పట్టిక_స్థాయి < 0
                || (long) విభాగం_పట్టిక_స్థాయి + (long) విభాగం_ప్రవేశం_పరిమాణం_మార్చు * 구역수 > డేటా.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<విభాగం_మూల్యం> 구역들 = new ArrayList<విభాగం_మూల్యం>();
        for (int సూచీ = 0; సూచీ < 구역수; సూచీ++) {
            int స్థానము = విభాగం_పట్టిక_స్థాయి + సూచీ * విభాగం_ప్రవేశం_పరిమాణం_మార్చు;
            int 종류 = పార్స్_పూర్ణాంకం(డేటా, స్థానము + 4);
            int పతాకం_మూల్యం = పార్స్_పూర్ణాంకం(డేటా, స్థానము + 8);
            int ఇమెయిల్ = పార్స్_పూర్ణాంకం(డేటా, స్థానము + 12);
            int ఫైలు_స్థాయి = పార్స్_పూర్ణాంకం(డేటా, స్థానము + 16);
            int పరిమాణం = పార్స్_పూర్ణాంకం(డేటా, స్థానము + 20);
            if (పరిమాణం < 0 || (종류 != 8 && ((long) ఫైలు_స్థాయి + పరిమాణం > డేటా.length || ఫైలు_స్థాయి < 0))) {
                throw new IllegalArgumentException("ELF విభాగం_మూల్యం డేటా 범위가 올바르지 않습니다.");
            }
            구역들.add(new విభాగం_మూల్యం(종류, పతాకం_మూల్యం, ఇమెయిల్, ఫైలు_స్థాయి, పరిమాణం));
        }
        return new చిత్రం(ప్రారంభం_ఇమెయిల్, 구역들);
    }

    private int పార్స్_పూర్ణాంకం(byte[] డేటా, int స్థానము) {
        if (స్థానము < 0 || స్థానము > డేటా.length - 4) {
            throw new IllegalArgumentException("ELF పూర్ణాంకం 범위를 벗어났습니다.");
        }
        return (డేటా[స్థానము] & 0xff)
                | ((డేటా[స్థానము + 1] & 0xff) << 8)
                | ((డేటా[స్థానము + 2] & 0xff) << 16)
                | ((డేటా[స్థానము + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] డేటా, int స్థానము) {
        if (స్థానము < 0 || స్థానము > డేటా.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 పూర్ణాంకం 범위를 벗어났습니다.");
        }
        return (డేటా[స్థానము] & 0xff) | ((డేటా[స్థానము + 1] & 0xff) << 8);
    }
}
