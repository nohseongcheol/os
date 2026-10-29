// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espanya.JEspOS.sistema_d_arxius;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fitxer 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final sistema_d_arxius.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(sistema_d_arxius.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sistema_d_arxius sistema_d_arxius;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(sistema_d_arxius sistema_d_arxius) {
        this.sistema_d_arxius = sistema_d_arxius;
    }

    public int Obre(String Nom) {
        sistema_d_arxius.열린파일 열린파일 = sistema_d_arxius.Obre(Nom);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = 빈번호(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Lectura(int INDEX, byte[] rebre_destinació, int Mida) {
        서술자 introducció_VALOR = 서술자들.get(Integer.valueOf(INDEX));
        if (introducció_VALOR == null) {
            return -9;
        }
        if (Mida < 0 || Mida > rebre_destinació.length) {
            return -22;
        }
        int 남음 = introducció_VALOR.열린파일.dades.length - introducció_VALOR.열린파일.Posició;
        int tancar_canviar_la_mida = Math.min(Mida, Math.max(남음, 0));
        System.arraycopy(introducció_VALOR.열린파일.dades, introducció_VALOR.열린파일.Posició, rebre_destinació, 0, tancar_canviar_la_mida);
        introducció_VALOR.열린파일.Posició += tancar_canviar_la_mida;
        return tancar_canviar_la_mida;
    }

    public int moure_càrrec(int INDEX, int 거리, int Project_rel) {
        서술자 introducció_VALOR = 서술자들.get(Integer.valueOf(INDEX));
        if (introducció_VALOR == null) {
            return -9;
        }
        int Fons_VALOR;
        if (Project_rel == 0) {
            Fons_VALOR = 0;
        } else if (Project_rel == 1) {
            Fons_VALOR = introducció_VALOR.열린파일.Posició;
        } else if (Project_rel == 2) {
            Fons_VALOR = introducció_VALOR.열린파일.dades.length;
        } else {
            return -22;
        }
        int 새위치 = Fons_VALOR + 거리;
        if (새위치 < 0) {
            return -22;
        }
        introducció_VALOR.열린파일.Posició = 새위치;
        return 새위치;
    }

    public int Tanca(int INDEX) {
        서술자 introducció_VALOR = 서술자들.remove(Integer.valueOf(INDEX));
        if (introducció_VALOR == null) {
            return -9;
        }
        introducció_VALOR.열린파일.Referència_COMPT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 introducció_VALOR = 서술자들.get(Integer.valueOf(INDEX));
        if (introducció_VALOR == null) {
            return -9;
        }
        int Número_nou = 빈번호(최소번호);
        if (Número_nou < 0) {
            return -24;
        }
        introducció_VALOR.열린파일.Referència_COMPT++;
        서술자들.put(Integer.valueOf(Número_nou), new 서술자(introducció_VALOR.열린파일));
        return Número_nou;
    }

    public int 지정복제(int INDEX, int Número_nou) {
        if (INDEX == Número_nou) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Número_nou < 0 || Número_nou >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Número_nou))) {
            Tanca(Número_nou);
        }
        원본.열린파일.Referència_COMPT++;
        서술자들.put(Integer.valueOf(Número_nou), new 서술자(원본.열린파일));
        return Número_nou;
    }

    public int 실행시닫기설정(int INDEX, boolean VALOR) {
        서술자 introducció_VALOR = 서술자들.get(Integer.valueOf(INDEX));
        if (introducció_VALOR == null) {
            return -9;
        }
        introducció_VALOR.실행시닫기 = VALOR;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 introducció_VALOR = 서술자들.get(Integer.valueOf(INDEX));
        if (introducció_VALOR == null) {
            return -9;
        }
        return introducció_VALOR.실행시닫기 ? 1 : 0;
    }

    public arxiu_informació msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new arxiu_informació(0, 0020666);
        }
        서술자 introducció_VALOR = 서술자들.get(Integer.valueOf(INDEX));
        if (introducció_VALOR == null) {
            return null;
        }
        return new arxiu_informació(introducció_VALOR.열린파일.dades.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 introducció_VALOR = 서술자들.get(INDEX);
            if (introducció_VALOR != null && introducció_VALOR.실행시닫기) {
                Tanca(INDEX.intValue());
            }
        }
    }

    public boolean tecnologies_de_la_informació_crear(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 clon_VALOR() {
        파일서술자표 RESULTAT = new 파일서술자표(sistema_d_arxius);
        for (Map.Entry<Integer, 서술자> introducció_VALOR : 서술자들.entrySet()) {
            introducció_VALOR.getValue().열린파일.Referència_COMPT++;
            서술자 새서술자 = new 서술자(introducció_VALOR.getValue().열린파일);
            새서술자.실행시닫기 = introducció_VALOR.getValue().실행시닫기;
            RESULTAT.서술자들.put(introducció_VALOR.getKey(), 새서술자);
        }
        return RESULTAT;
    }

    private int 빈번호(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
