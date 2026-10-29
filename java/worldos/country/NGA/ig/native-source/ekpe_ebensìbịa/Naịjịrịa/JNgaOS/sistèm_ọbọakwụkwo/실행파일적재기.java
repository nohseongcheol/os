// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian mee_nnyemiwu 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class nkebì_valuu {
        private final int 종류;
        private final int ọkọlọtọ_valuu;
        private final int àdreèsì;
        private final int 파일위치;
        private final int Ụhara;

        nkebì_valuu(int 종류, int ọkọlọtọ_valuu, int àdreèsì, int 파일위치, int Ụhara) {
            this.종류 = 종류;
            this.ọkọlọtọ_valuu = ọkọlọtọ_valuu;
            this.àdreèsì = àdreèsì;
            this.파일위치 = 파일위치;
            this.Ụhara = Ụhara;
        }

        public int 종류() {
            return 종류;
        }

        public int ọkọlọtọ_valuu() {
            return ọkọlọtọ_valuu;
        }

        public int àdreèsì() {
            return àdreèsì;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Ụhara() {
            return Ụhara;
        }
    }

    public static final class foto {
        private final int Mbido_àdreèsì;
        private final List<nkebì_valuu> 구역들;

        foto(int Mbido_àdreèsì, List<nkebì_valuu> 구역들) {
            this.Mbido_àdreèsì = Mbido_àdreèsì;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Mbido_àdreèsì() {
            return Mbido_àdreèsì;
        }

        public List<nkebì_valuu> 구역들() {
            return 구역들;
        }
    }

    public foto 검사(byte[] datà) {
        if (datà == null || datà.length < 52
                || datà[0] != 0x7f || datà[1] != 'E' || datà[2] != 'L' || datà[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (datà[4] != 1 || datà[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Mbido_àdreèsì = kerìsịa_ọnụọgụ_nzùrùòkè(datà, 24);
        int 구역표위치 = kerìsịa_ọnụọgụ_nzùrùòkè(datà, 32);
        int nkebì_ndebà_ụha = 짧은정수읽기(datà, 46);
        int 구역수 = 짧은정수읽기(datà, 48);
        if (nkebì_ndebà_ụha < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) nkebì_ndebà_ụha * 구역수 > datà.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<nkebì_valuu> 구역들 = new ArrayList<nkebì_valuu>();
        for (int indèks = 0; indèks < 구역수; indèks++) {
            int 위치 = 구역표위치 + indèks * nkebì_ndebà_ụha;
            int 종류 = kerìsịa_ọnụọgụ_nzùrùòkè(datà, 위치 + 4);
            int ọkọlọtọ_valuu = kerìsịa_ọnụọgụ_nzùrùòkè(datà, 위치 + 8);
            int àdreèsì = kerìsịa_ọnụọgụ_nzùrùòkè(datà, 위치 + 12);
            int 파일위치 = kerìsịa_ọnụọgụ_nzùrùòkè(datà, 위치 + 16);
            int Ụhara = kerìsịa_ọnụọgụ_nzùrùòkè(datà, 위치 + 20);
            if (Ụhara < 0 || (종류 != 8 && ((long) 파일위치 + Ụhara > datà.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF nkebì_valuu datà 범위가 올바르지 않습니다.");
            }
            구역들.add(new nkebì_valuu(종류, ọkọlọtọ_valuu, àdreèsì, 파일위치, Ụhara));
        }
        return new foto(Mbido_àdreèsì, 구역들);
    }

    private int kerìsịa_ọnụọgụ_nzùrùòkè(byte[] datà, int 위치) {
        if (위치 < 0 || 위치 > datà.length - 4) {
            throw new IllegalArgumentException("ELF ọnụọgụ_nzùrùòkè 범위를 벗어났습니다.");
        }
        return (datà[위치] & 0xff)
                | ((datà[위치 + 1] & 0xff) << 8)
                | ((datà[위치 + 2] & 0xff) << 16)
                | ((datà[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] datà, int 위치) {
        if (위치 < 0 || 위치 > datà.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ọnụọgụ_nzùrùòkè 범위를 벗어났습니다.");
        }
        return (datà[위치] & 0xff) | ((datà[위치 + 1] & 0xff) << 8);
    }
}
