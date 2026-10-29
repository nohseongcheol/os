// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.sistema_de_ficheiros;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Lectura 계층과 같은 Lectura 전용 Ficheiro 저장소의 관리 모델이다. */
public final class sistema_de_ficheiros {
    static final class 열린파일 {
        final byte[] datos;
        int Posición;
        int Material_de_referencia_CONTAR = 1;

        열린파일(byte[] datos) {
            this.datos = datos;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Anexar_Ficheiro(String Nome, byte[] datos) {
        파일들.put(정규이름(Nome), Arrays.copyOf(datos, datos.length));
    }

    열린파일 Abrir(String Nome) {
        byte[] datos = 파일들.get(정규이름(Nome));
        if (datos == null) {
            return null;
        }
        return new 열린파일(datos);
    }

    public boolean 존재함(String Nome) {
        return 파일들.containsKey(정규이름(Nome));
    }

    public Ficheiro_información msinfo32_exe(String Nome) {
        byte[] datos = 파일들.get(정규이름(Nome));
        if (datos == null) {
            return null;
        }
        return new Ficheiro_información(datos.length, 0100444);
    }

    private String 정규이름(String Nome) {
        if (Nome == null) {
            throw new NullPointerException("Ficheiro 이름이 없습니다.");
        }
        String RESULTANTE = Nome.startsWith("/") ? Nome.substring(1) : Nome;
        return RESULTANTE.toUpperCase(Locale.ROOT);
    }
}
