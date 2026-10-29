// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
import java.util.ArrayList;
/** entrada_Lista_f07b3200(目錄): 순서가 있는 항목의 모음. 이 판은 cadeia_VALOR 목록을 제공한다. */
public final class entrada_Lista_f07b3200 {
    private final ArrayList<String> entrada_VALOR_962f286b = new ArrayList<String>();
    public void 더하기(String VALOR) { entrada_VALOR_962f286b.add(VALOR); }
    public String Leitura(int ordem_VALOR) { return entrada_VALOR_962f286b.get(ordem_VALOR); }
    public String MUDAR_VALOR(int ordem_VALOR, String VALOR) { return entrada_VALOR_962f286b.set(ordem_VALOR, VALOR); }
    public String apagar_entrada(int ordem_VALOR) { return entrada_VALOR_962f286b.remove(ordem_VALOR); }
    public int Tamanho() { return entrada_VALOR_962f286b.size(); }
    public boolean TI_vazio_VALOR() { return entrada_VALOR_962f286b.isEmpty(); }
    public void limpar_Sumário() { entrada_VALOR_962f286b.clear(); }
}
