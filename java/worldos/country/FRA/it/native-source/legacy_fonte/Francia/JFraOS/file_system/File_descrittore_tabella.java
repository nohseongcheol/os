// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Francia.JFraOS.file_system;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 file 설명을 유지한다. */
public final class File_descrittore_tabella {
    private static final int 최대서술자 = 32;

    private static final class descrittore_voce {
        private final file_system.열린파일 열린파일;
        private boolean 실행시닫기;

        descrittore_voce(file_system.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final file_system file_system;
    private final Map<Integer, descrittore_voce> 서술자들 = new HashMap<Integer, descrittore_voce>();

    public File_descrittore_tabella(file_system file_system) {
        this.file_system = file_system;
    }

    public int Apri(String Nome) {
        file_system.열린파일 열린파일 = file_system.Apri(Nome);
        if (열린파일 == null) {
            return -2;
        }
        int INDICE = vuota_INDICE(3);
        if (INDICE < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDICE), new descrittore_voce(열린파일));
        return INDICE;
    }

    public int Lettura(int INDICE, byte[] ricevere_meta, int Dimensione) {
        descrittore_voce voce_VALORE = 서술자들.get(Integer.valueOf(INDICE));
        if (voce_VALORE == null) {
            return -9;
        }
        if (Dimensione < 0 || Dimensione > ricevere_meta.length) {
            return -22;
        }
        int 남음 = voce_VALORE.열린파일.dati.length - voce_VALORE.열린파일.posizione;
        int 읽을크기 = Math.min(Dimensione, Math.max(남음, 0));
        System.arraycopy(voce_VALORE.열린파일.dati, voce_VALORE.열린파일.posizione, ricevere_meta, 0, 읽을크기);
        voce_VALORE.열린파일.posizione += 읽을크기;
        return 읽을크기;
    }

    public int spostare_funzione(int INDICE, int 거리, int azione_radice) {
        descrittore_voce voce_VALORE = 서술자들.get(Integer.valueOf(INDICE));
        if (voce_VALORE == null) {
            return -9;
        }
        int sfondo_VALORE;
        if (azione_radice == 0) {
            sfondo_VALORE = 0;
        } else if (azione_radice == 1) {
            sfondo_VALORE = voce_VALORE.열린파일.posizione;
        } else if (azione_radice == 2) {
            sfondo_VALORE = voce_VALORE.열린파일.dati.length;
        } else {
            return -22;
        }
        int 새위치 = sfondo_VALORE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        voce_VALORE.열린파일.posizione = 새위치;
        return 새위치;
    }

    public int Chiudi(int INDICE) {
        descrittore_voce voce_VALORE = 서술자들.remove(Integer.valueOf(INDICE));
        if (voce_VALORE == null) {
            return -9;
        }
        voce_VALORE.열린파일.fonti_CONTA_NUMERI--;
        return 0;
    }

    public int 복제서술자(int INDICE, int 최소번호) {
        descrittore_voce voce_VALORE = 서술자들.get(Integer.valueOf(INDICE));
        if (voce_VALORE == null) {
            return -9;
        }
        int Nuovo_numero = vuota_INDICE(최소번호);
        if (Nuovo_numero < 0) {
            return -24;
        }
        voce_VALORE.열린파일.fonti_CONTA_NUMERI++;
        서술자들.put(Integer.valueOf(Nuovo_numero), new descrittore_voce(voce_VALORE.열린파일));
        return Nuovo_numero;
    }

    public int 지정복제(int INDICE, int Nuovo_numero) {
        if (INDICE == Nuovo_numero) {
            return 서술자들.containsKey(Integer.valueOf(INDICE)) ? INDICE : -9;
        }
        if (Nuovo_numero < 0 || Nuovo_numero >= 최대서술자) {
            return -9;
        }
        descrittore_voce 원본 = 서술자들.get(Integer.valueOf(INDICE));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Nuovo_numero))) {
            Chiudi(Nuovo_numero);
        }
        원본.열린파일.fonti_CONTA_NUMERI++;
        서술자들.put(Integer.valueOf(Nuovo_numero), new descrittore_voce(원본.열린파일));
        return Nuovo_numero;
    }

    public int 실행시닫기설정(int INDICE, boolean VALORE) {
        descrittore_voce voce_VALORE = 서술자들.get(Integer.valueOf(INDICE));
        if (voce_VALORE == null) {
            return -9;
        }
        voce_VALORE.실행시닫기 = VALORE;
        return 0;
    }

    public int 실행시닫기값(int INDICE) {
        descrittore_voce voce_VALORE = 서술자들.get(Integer.valueOf(INDICE));
        if (voce_VALORE == null) {
            return -9;
        }
        return voce_VALORE.실행시닫기 ? 1 : 0;
    }

    public File_info msinfo32_exe(int INDICE) {
        if (INDICE >= 0 && INDICE <= 2) {
            return new File_info(0, 0020666);
        }
        descrittore_voce voce_VALORE = 서술자들.get(Integer.valueOf(INDICE));
        if (voce_VALORE == null) {
            return null;
        }
        return new File_info(voce_VALORE.열린파일.dati.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] numero_elenco = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDICE : numero_elenco) {
            descrittore_voce voce_VALORE = 서술자들.get(INDICE);
            if (voce_VALORE != null && voce_VALORE.실행시닫기) {
                Chiudi(INDICE.intValue());
            }
        }
    }

    public boolean reparto_IT_aperto(int INDICE) {
        return 서술자들.containsKey(Integer.valueOf(INDICE));
    }

    public File_descrittore_tabella clone_VALORE() {
        File_descrittore_tabella risultato = new File_descrittore_tabella(file_system);
        for (Map.Entry<Integer, descrittore_voce> voce_VALORE : 서술자들.entrySet()) {
            voce_VALORE.getValue().열린파일.fonti_CONTA_NUMERI++;
            descrittore_voce 새서술자 = new descrittore_voce(voce_VALORE.getValue().열린파일);
            새서술자.실행시닫기 = voce_VALORE.getValue().실행시닫기;
            risultato.서술자들.put(voce_VALORE.getKey(), 새서술자);
        }
        return risultato;
    }

    private int vuota_INDICE(int 최소번호) {
        for (int INDICE = Math.max(0, 최소번호); INDICE < 최대서술자; INDICE++) {
            if (!서술자들.containsKey(Integer.valueOf(INDICE))) {
                return INDICE;
            }
        }
        return -1;
    }
}
