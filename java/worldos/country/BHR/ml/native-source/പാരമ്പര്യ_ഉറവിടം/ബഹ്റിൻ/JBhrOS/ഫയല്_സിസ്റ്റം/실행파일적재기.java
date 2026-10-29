// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ബഹ്റിൻ.JBhrOS.ഫയല്_സിസ്റ്റം;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian നടപ്പാക്കുക_കമാന്_ഡ് 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class വിഭാഗം_മൂല്യം {
        private final int 종류;
        private final int ഫ്ലാഗുചെയ്യുക_മൂല്യം;
        private final int ഇമെയിൽ;
        private final int ഫയല്_പദവി;
        private final int വലിപ്പം;

        വിഭാഗം_മൂല്യം(int 종류, int ഫ്ലാഗുചെയ്യുക_മൂല്യം, int ഇമെയിൽ, int ഫയല്_പദവി, int വലിപ്പം) {
            this.종류 = 종류;
            this.ഫ്ലാഗുചെയ്യുക_മൂല്യം = ഫ്ലാഗുചെയ്യുക_മൂല്യം;
            this.ഇമെയിൽ = ഇമെയിൽ;
            this.ഫയല്_പദവി = ഫയല്_പദവി;
            this.വലിപ്പം = വലിപ്പം;
        }

        public int 종류() {
            return 종류;
        }

        public int ഫ്ലാഗുചെയ്യുക_മൂല്യം() {
            return ഫ്ലാഗുചെയ്യുക_മൂല്യം;
        }

        public int ഇമെയിൽ() {
            return ഇമെയിൽ;
        }

        public int ഫയല്_പദവി() {
            return ഫയല്_പദവി;
        }

        public int വലിപ്പം() {
            return വലിപ്പം;
        }
    }

    public static final class ഇമേജ് {
        private final int ആരംഭം_ഇമെയിൽ;
        private final List<വിഭാഗം_മൂല്യം> 구역들;

        ഇമേജ്(int ആരംഭം_ഇമെയിൽ, List<വിഭാഗം_മൂല്യം> 구역들) {
            this.ആരംഭം_ഇമെയിൽ = ആരംഭം_ഇമെയിൽ;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ആരംഭം_ഇമെയിൽ() {
            return ആരംഭം_ഇമെയിൽ;
        }

        public List<വിഭാഗം_മൂല്യം> 구역들() {
            return 구역들;
        }
    }

    public ഇമേജ് 검사(byte[] ഡാറ്റാ) {
        if (ഡാറ്റാ == null || ഡാറ്റാ.length < 52
                || ഡാറ്റാ[0] != 0x7f || ഡാറ്റാ[1] != 'E' || ഡാറ്റാ[2] != 'L' || ഡാറ്റാ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ഡാറ്റാ[4] != 1 || ഡാറ്റാ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ആരംഭം_ഇമെയിൽ = പാര്_സ്_ചെയ്യുക_പൂര്_ണ്ണസംഖ്യ(ഡാറ്റാ, 24);
        int വിഭാഗം_పట్టిక_പദവി = പാര്_സ്_ചെയ്യുക_പൂര്_ണ്ണസംഖ്യ(ഡാറ്റാ, 32);
        int വിഭാഗം_എന്_ട്രി_വലുപ്പം_ക്രമീകരിക്കുക = 짧은정수읽기(ഡാറ്റാ, 46);
        int 구역수 = 짧은정수읽기(ഡാറ്റാ, 48);
        if (വിഭാഗം_എന്_ട്രി_വലുപ്പം_ക്രമീകരിക്കുക < 40 || വിഭാഗം_పట్టిక_പദവി < 0
                || (long) വിഭാഗം_పట్టిక_പദവി + (long) വിഭാഗം_എന്_ട്രി_വലുപ്പം_ക്രമീകരിക്കുക * 구역수 > ഡാറ്റാ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<വിഭാഗം_മൂല്യം> 구역들 = new ArrayList<വിഭാഗം_മൂല്യം>();
        for (int സൂചിക = 0; സൂചിക < 구역수; സൂചിക++) {
            int സ്ഥാനം = വിഭാഗം_పట్టిక_പദവി + സൂചിക * വിഭാഗം_എന്_ട്രി_വലുപ്പം_ക്രമീകരിക്കുക;
            int 종류 = പാര്_സ്_ചെയ്യുക_പൂര്_ണ്ണസംഖ്യ(ഡാറ്റാ, സ്ഥാനം + 4);
            int ഫ്ലാഗുചെയ്യുക_മൂല്യം = പാര്_സ്_ചെയ്യുക_പൂര്_ണ്ണസംഖ്യ(ഡാറ്റാ, സ്ഥാനം + 8);
            int ഇമെയിൽ = പാര്_സ്_ചെയ്യുക_പൂര്_ണ്ണസംഖ്യ(ഡാറ്റാ, സ്ഥാനം + 12);
            int ഫയല്_പദവി = പാര്_സ്_ചെയ്യുക_പൂര്_ണ്ണസംഖ്യ(ഡാറ്റാ, സ്ഥാനം + 16);
            int വലിപ്പം = പാര്_സ്_ചെയ്യുക_പൂര്_ണ്ണസംഖ്യ(ഡാറ്റാ, സ്ഥാനം + 20);
            if (വലിപ്പം < 0 || (종류 != 8 && ((long) ഫയല്_പദവി + വലിപ്പം > ഡാറ്റാ.length || ഫയല്_പദവി < 0))) {
                throw new IllegalArgumentException("ELF വിഭാഗം_മൂല്യം ഡാറ്റാ 범위가 올바르지 않습니다.");
            }
            구역들.add(new വിഭാഗം_മൂല്യം(종류, ഫ്ലാഗുചെയ്യുക_മൂല്യം, ഇമെയിൽ, ഫയല്_പദവി, വലിപ്പം));
        }
        return new ഇമേജ്(ആരംഭം_ഇമെയിൽ, 구역들);
    }

    private int പാര്_സ്_ചെയ്യുക_പൂര്_ണ്ണസംഖ്യ(byte[] ഡാറ്റാ, int സ്ഥാനം) {
        if (സ്ഥാനം < 0 || സ്ഥാനം > ഡാറ്റാ.length - 4) {
            throw new IllegalArgumentException("ELF പൂര്_ണ്ണസംഖ്യ 범위를 벗어났습니다.");
        }
        return (ഡാറ്റാ[സ്ഥാനം] & 0xff)
                | ((ഡാറ്റാ[സ്ഥാനം + 1] & 0xff) << 8)
                | ((ഡാറ്റാ[സ്ഥാനം + 2] & 0xff) << 16)
                | ((ഡാറ്റാ[സ്ഥാനം + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ഡാറ്റാ, int സ്ഥാനം) {
        if (സ്ഥാനം < 0 || സ്ഥാനം > ഡാറ്റാ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 പൂര്_ണ്ണസംഖ്യ 범위를 벗어났습니다.");
        }
        return (ഡാറ്റാ[സ്ഥാനം] & 0xff) | ((ഡാറ്റാ[സ്ഥാനം + 1] & 0xff) << 8);
    }
}
