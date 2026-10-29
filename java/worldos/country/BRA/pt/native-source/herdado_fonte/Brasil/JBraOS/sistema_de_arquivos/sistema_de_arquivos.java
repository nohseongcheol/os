// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Brasil.JBraOS.sistema_de_arquivos;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Leitura 계층과 같은 Leitura 전용 ficheiro 저장소의 관리 모델이다. */
public final class sistema_de_arquivos {
    static final class 열린파일 {
        final byte[] dados;
        int posição;
        int Referência_CONT_NÚM = 1;

        열린파일(byte[] dados) {
            this.dados = dados;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Acrescentar_Arquivo(String Nome, byte[] dados) {
        파일들.put(nome_canônico(Nome), Arrays.copyOf(dados, dados.length));
    }

    열린파일 Abrir(String Nome) {
        byte[] dados = 파일들.get(nome_canônico(Nome));
        if (dados == null) {
            return null;
        }
        return new 열린파일(dados);
    }

    public boolean 존재함(String Nome) {
        return 파일들.containsKey(nome_canônico(Nome));
    }

    public Arquivo_informações msinfo32_exe(String Nome) {
        byte[] dados = 파일들.get(nome_canônico(Nome));
        if (dados == null) {
            return null;
        }
        return new Arquivo_informações(dados.length, 0100444);
    }

    private String nome_canônico(String Nome) {
        if (Nome == null) {
            throw new NullPointerException("ficheiro 이름이 없습니다.");
        }
        String resultado = Nome.startsWith("/") ? Nome.substring(1) : Nome;
        return resultado.toUpperCase(Locale.ROOT);
    }
}
