// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.córas_comhad;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Rith_ordú 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class rannán_VALUE {
        private final int 종류;
        private final int bratach_VALUE;
        private final int ADDRESS;
        private final int comhad_suíomh;
        private final int Méid;

        rannán_VALUE(int 종류, int bratach_VALUE, int ADDRESS, int comhad_suíomh, int Méid) {
            this.종류 = 종류;
            this.bratach_VALUE = bratach_VALUE;
            this.ADDRESS = ADDRESS;
            this.comhad_suíomh = comhad_suíomh;
            this.Méid = Méid;
        }

        public int 종류() {
            return 종류;
        }

        public int bratach_VALUE() {
            return bratach_VALUE;
        }

        public int ADDRESS() {
            return ADDRESS;
        }

        public int comhad_suíomh() {
            return comhad_suíomh;
        }

        public int Méid() {
            return Méid;
        }
    }

    public static final class IMAGE {
        private final int seoladh_tosaithe;
        private final List<rannán_VALUE> 구역들;

        IMAGE(int seoladh_tosaithe, List<rannán_VALUE> 구역들) {
            this.seoladh_tosaithe = seoladh_tosaithe;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int seoladh_tosaithe() {
            return seoladh_tosaithe;
        }

        public List<rannán_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] sonraí) {
        if (sonraí == null || sonraí.length < 52
                || sonraí[0] != 0x7f || sonraí[1] != 'E' || sonraí[2] != 'L' || sonraí[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (sonraí[4] != 1 || sonraí[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int seoladh_tosaithe = parsáil_slánuimhir(sonraí, 24);
        int rannán_tábla_suíomh = parsáil_slánuimhir(sonraí, 32);
        int rannán_iontráil_socraigh_méid = 짧은정수읽기(sonraí, 46);
        int rannán_COUNT = 짧은정수읽기(sonraí, 48);
        if (rannán_iontráil_socraigh_méid < 40 || rannán_tábla_suíomh < 0
                || (long) rannán_tábla_suíomh + (long) rannán_iontráil_socraigh_méid * rannán_COUNT > sonraí.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<rannán_VALUE> 구역들 = new ArrayList<rannán_VALUE>();
        for (int INDEX = 0; INDEX < rannán_COUNT; INDEX++) {
            int suíomh = rannán_tábla_suíomh + INDEX * rannán_iontráil_socraigh_méid;
            int 종류 = parsáil_slánuimhir(sonraí, suíomh + 4);
            int bratach_VALUE = parsáil_slánuimhir(sonraí, suíomh + 8);
            int ADDRESS = parsáil_slánuimhir(sonraí, suíomh + 12);
            int comhad_suíomh = parsáil_slánuimhir(sonraí, suíomh + 16);
            int Méid = parsáil_slánuimhir(sonraí, suíomh + 20);
            if (Méid < 0 || (종류 != 8 && ((long) comhad_suíomh + Méid > sonraí.length || comhad_suíomh < 0))) {
                throw new IllegalArgumentException("ELF rannán_VALUE sonraí 범위가 올바르지 않습니다.");
            }
            구역들.add(new rannán_VALUE(종류, bratach_VALUE, ADDRESS, comhad_suíomh, Méid));
        }
        return new IMAGE(seoladh_tosaithe, 구역들);
    }

    private int parsáil_slánuimhir(byte[] sonraí, int suíomh) {
        if (suíomh < 0 || suíomh > sonraí.length - 4) {
            throw new IllegalArgumentException("ELF slánuimhir 범위를 벗어났습니다.");
        }
        return (sonraí[suíomh] & 0xff)
                | ((sonraí[suíomh + 1] & 0xff) << 8)
                | ((sonraí[suíomh + 2] & 0xff) << 16)
                | ((sonraí[suíomh + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] sonraí, int suíomh) {
        if (suíomh < 0 || suíomh > sonraí.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 slánuimhir 범위를 벗어났습니다.");
        }
        return (sonraí[suíomh] & 0xff) | ((sonraí[suíomh + 1] & 0xff) << 8);
    }
}
