// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.sistema_de_ficheiros;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian executar_comando 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class sección_VALOR {
        private final int 종류;
        private final int marca_VALOR;
        private final int ENDEREZO;
        private final int Ficheiro_cargo;
        private final int Tamaño;

        sección_VALOR(int 종류, int marca_VALOR, int ENDEREZO, int Ficheiro_cargo, int Tamaño) {
            this.종류 = 종류;
            this.marca_VALOR = marca_VALOR;
            this.ENDEREZO = ENDEREZO;
            this.Ficheiro_cargo = Ficheiro_cargo;
            this.Tamaño = Tamaño;
        }

        public int 종류() {
            return 종류;
        }

        public int marca_VALOR() {
            return marca_VALOR;
        }

        public int ENDEREZO() {
            return ENDEREZO;
        }

        public int Ficheiro_cargo() {
            return Ficheiro_cargo;
        }

        public int Tamaño() {
            return Tamaño;
        }
    }

    public static final class IMAXE {
        private final int START_ENDEREZO;
        private final List<sección_VALOR> 구역들;

        IMAXE(int START_ENDEREZO, List<sección_VALOR> 구역들) {
            this.START_ENDEREZO = START_ENDEREZO;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_ENDEREZO() {
            return START_ENDEREZO;
        }

        public List<sección_VALOR> 구역들() {
            return 구역들;
        }
    }

    public IMAXE 검사(byte[] datos) {
        if (datos == null || datos.length < 52
                || datos[0] != 0x7f || datos[1] != 'E' || datos[2] != 'L' || datos[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (datos[4] != 1 || datos[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_ENDEREZO = analizar_número_enteiro(datos, 24);
        int sección_táboa_cargo = analizar_número_enteiro(datos, 32);
        int 구역항목크기 = 짧은정수읽기(datos, 46);
        int sección_CONTAR = 짧은정수읽기(datos, 48);
        if (구역항목크기 < 40 || sección_táboa_cargo < 0
                || (long) sección_táboa_cargo + (long) 구역항목크기 * sección_CONTAR > datos.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sección_VALOR> 구역들 = new ArrayList<sección_VALOR>();
        for (int ÍNDICE = 0; ÍNDICE < sección_CONTAR; ÍNDICE++) {
            int Posición = sección_táboa_cargo + ÍNDICE * 구역항목크기;
            int 종류 = analizar_número_enteiro(datos, Posición + 4);
            int marca_VALOR = analizar_número_enteiro(datos, Posición + 8);
            int ENDEREZO = analizar_número_enteiro(datos, Posición + 12);
            int Ficheiro_cargo = analizar_número_enteiro(datos, Posición + 16);
            int Tamaño = analizar_número_enteiro(datos, Posición + 20);
            if (Tamaño < 0 || (종류 != 8 && ((long) Ficheiro_cargo + Tamaño > datos.length || Ficheiro_cargo < 0))) {
                throw new IllegalArgumentException("ELF sección_VALOR datos 범위가 올바르지 않습니다.");
            }
            구역들.add(new sección_VALOR(종류, marca_VALOR, ENDEREZO, Ficheiro_cargo, Tamaño));
        }
        return new IMAXE(START_ENDEREZO, 구역들);
    }

    private int analizar_número_enteiro(byte[] datos, int Posición) {
        if (Posición < 0 || Posición > datos.length - 4) {
            throw new IllegalArgumentException("ELF número_enteiro 범위를 벗어났습니다.");
        }
        return (datos[Posición] & 0xff)
                | ((datos[Posición + 1] & 0xff) << 8)
                | ((datos[Posición + 2] & 0xff) << 16)
                | ((datos[Posición + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] datos, int Posición) {
        if (Posición < 0 || Posición > datos.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 número_enteiro 범위를 벗어났습니다.");
        }
        return (datos[Posición] & 0xff) | ((datos[Posición + 1] & 0xff) << 8);
    }
}
