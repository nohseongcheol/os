// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;
import java.util.HashMap;
/** словарь(辭典): 찾는 Word_SMS(Ключ_материал)에 값을 대응시킨다. */
public final class словарь {
    private final HashMap<String, String> ввод_ЗНАЧЕН = new HashMap<String, String>();
    public String 넣기(String Ключ_материал, String ЗНАЧЕН) { return ввод_ЗНАЧЕН.put(Ключ_материал, ЗНАЧЕН); }
    public String НАЙТИ_ввод(String Ключ_материал) { return ввод_ЗНАЧЕН.get(Ключ_материал); }
    public boolean 있는가(String Ключ_материал) { return ввод_ЗНАЧЕН.containsKey(Ключ_материал); }
    public String удалить_ввод_c8dbc399(String Ключ_материал) { return ввод_ЗНАЧЕН.remove(Ключ_материал); }
    public int Размер() { return ввод_ЗНАЧЕН.size(); }
    public void очищать_Оглавление() { ввод_ЗНАЧЕН.clear(); }
}
