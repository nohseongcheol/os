// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.sistema_de_ficheiros;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Ficheiro 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final sistema_de_ficheiros.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(sistema_de_ficheiros.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sistema_de_ficheiros sistema_de_ficheiros;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(sistema_de_ficheiros sistema_de_ficheiros) {
        this.sistema_de_ficheiros = sistema_de_ficheiros;
    }

    public int Abrir(String Nome) {
        sistema_de_ficheiros.열린파일 열린파일 = sistema_de_ficheiros.Abrir(Nome);
        if (열린파일 == null) {
            return -2;
        }
        int ÍNDICE = baleiro_ÍNDICE(3);
        if (ÍNDICE < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ÍNDICE), new 서술자(열린파일));
        return ÍNDICE;
    }

    public int Lectura(int ÍNDICE, byte[] 받을곳, int Tamaño) {
        서술자 introdución_VALOR = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (introdución_VALOR == null) {
            return -9;
        }
        if (Tamaño < 0 || Tamaño > 받을곳.length) {
            return -22;
        }
        int 남음 = introdución_VALOR.열린파일.datos.length - introdución_VALOR.열린파일.Posición;
        int 읽을크기 = Math.min(Tamaño, Math.max(남음, 0));
        System.arraycopy(introdución_VALOR.열린파일.datos, introdución_VALOR.열린파일.Posición, 받을곳, 0, 읽을크기);
        introdución_VALOR.열린파일.Posición += 읽을크기;
        return 읽을크기;
    }

    public int mover_cargo(int ÍNDICE, int 거리, int Project_raíz) {
        서술자 introdución_VALOR = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (introdución_VALOR == null) {
            return -9;
        }
        int Fondo_VALOR;
        if (Project_raíz == 0) {
            Fondo_VALOR = 0;
        } else if (Project_raíz == 1) {
            Fondo_VALOR = introdución_VALOR.열린파일.Posición;
        } else if (Project_raíz == 2) {
            Fondo_VALOR = introdución_VALOR.열린파일.datos.length;
        } else {
            return -22;
        }
        int 새위치 = Fondo_VALOR + 거리;
        if (새위치 < 0) {
            return -22;
        }
        introdución_VALOR.열린파일.Posición = 새위치;
        return 새위치;
    }

    public int Pechar(int ÍNDICE) {
        서술자 introdución_VALOR = 서술자들.remove(Integer.valueOf(ÍNDICE));
        if (introdución_VALOR == null) {
            return -9;
        }
        introdución_VALOR.열린파일.Material_de_referencia_CONTAR--;
        return 0;
    }

    public int 복제서술자(int ÍNDICE, int 최소번호) {
        서술자 introdución_VALOR = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (introdución_VALOR == null) {
            return -9;
        }
        int 새번호 = baleiro_ÍNDICE(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        introdución_VALOR.열린파일.Material_de_referencia_CONTAR++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(introdución_VALOR.열린파일));
        return 새번호;
    }

    public int 지정복제(int ÍNDICE, int 새번호) {
        if (ÍNDICE == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ÍNDICE)) ? ÍNDICE : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Pechar(새번호);
        }
        원본.열린파일.Material_de_referencia_CONTAR++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ÍNDICE, boolean VALOR) {
        서술자 introdución_VALOR = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (introdución_VALOR == null) {
            return -9;
        }
        introdución_VALOR.실행시닫기 = VALOR;
        return 0;
    }

    public int 실행시닫기값(int ÍNDICE) {
        서술자 introdución_VALOR = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (introdución_VALOR == null) {
            return -9;
        }
        return introdución_VALOR.실행시닫기 ? 1 : 0;
    }

    public Ficheiro_información msinfo32_exe(int ÍNDICE) {
        if (ÍNDICE >= 0 && ÍNDICE <= 2) {
            return new Ficheiro_información(0, 0020666);
        }
        서술자 introdución_VALOR = 서술자들.get(Integer.valueOf(ÍNDICE));
        if (introdución_VALOR == null) {
            return null;
        }
        return new Ficheiro_información(introdución_VALOR.열린파일.datos.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ÍNDICE : 번호들) {
            서술자 introdución_VALOR = 서술자들.get(ÍNDICE);
            if (introdución_VALOR != null && introdución_VALOR.실행시닫기) {
                Pechar(ÍNDICE.intValue());
            }
        }
    }

    public boolean Tecnoloxía_da_información_TI_abrir(int ÍNDICE) {
        return 서술자들.containsKey(Integer.valueOf(ÍNDICE));
    }

    public 파일서술자표 clon_VALOR() {
        파일서술자표 RESULTANTE = new 파일서술자표(sistema_de_ficheiros);
        for (Map.Entry<Integer, 서술자> introdución_VALOR : 서술자들.entrySet()) {
            introdución_VALOR.getValue().열린파일.Material_de_referencia_CONTAR++;
            서술자 새서술자 = new 서술자(introdución_VALOR.getValue().열린파일);
            새서술자.실행시닫기 = introdución_VALOR.getValue().실행시닫기;
            RESULTANTE.서술자들.put(introdución_VALOR.getKey(), 새서술자);
        }
        return RESULTANTE;
    }

    private int baleiro_ÍNDICE(int 최소번호) {
        for (int ÍNDICE = Math.max(0, 최소번호); ÍNDICE < 최대서술자; ÍNDICE++) {
            if (!서술자들.containsKey(Integer.valueOf(ÍNDICE))) {
                return ÍNDICE;
            }
        }
        return -1;
    }
}
