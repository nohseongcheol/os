// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
import java.util.HashMap;
/** dicionário(辭典): 찾는 Word_SMS(Chave_material)에 값을 대응시킨다. */
public final class dicionário {
    private final HashMap<String, String> entrada_VALOR_962f286b = new HashMap<String, String>();
    public String 넣기(String Chave_material, String VALOR) { return entrada_VALOR_962f286b.put(Chave_material, VALOR); }
    public String PROCURAR_entrada(String Chave_material) { return entrada_VALOR_962f286b.get(Chave_material); }
    public boolean 있는가(String Chave_material) { return entrada_VALOR_962f286b.containsKey(Chave_material); }
    public String apagar_entrada(String Chave_material) { return entrada_VALOR_962f286b.remove(Chave_material); }
    public int Tamanho() { return entrada_VALOR_962f286b.size(); }
    public void limpar_Sumário() { entrada_VALOR_962f286b.clear(); }
}
