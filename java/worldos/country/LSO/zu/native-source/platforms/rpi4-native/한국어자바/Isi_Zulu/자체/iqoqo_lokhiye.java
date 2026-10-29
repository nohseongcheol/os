// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자체;
import java.util.HashMap;
/** iqoqo_lokhiye(辭典): 찾는 Amagama_I_SMS(열쇠)에 값을 대응시킨다. */
public final class iqoqo_lokhiye {
    private final HashMap<String, String> okufakwayo_inani = new HashMap<String, String>();
    public String 넣기(String 열쇠, String inani) { return okufakwayo_inani.put(열쇠, inani); }
    public String thola_okufakwayo(String 열쇠) { return okufakwayo_inani.get(열쇠); }
    public boolean 있는가(String 열쇠) { return okufakwayo_inani.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return okufakwayo_inani.remove(열쇠); }
    public int Ubungako() { return okufakwayo_inani.size(); }
    public void sula_i_TOC() { okufakwayo_inani.clear(); }
}
