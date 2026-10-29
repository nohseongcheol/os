// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;
import java.util.HashMap;
/** словник(辭典): 찾는 Ігри_в_слова_Текст(열쇠)에 값을 대응시킨다. */
public final class словник {
    private final HashMap<String, String> запис_значення_962f286b = new HashMap<String, String>();
    public String 넣기(String 열쇠, String значення) { return запис_значення_962f286b.put(열쇠, значення); }
    public String Знайти_запис(String 열쇠) { return запис_значення_962f286b.get(열쇠); }
    public boolean 있는가(String 열쇠) { return запис_значення_962f286b.containsKey(열쇠); }
    public String видаляти_запис(String 열쇠) { return запис_значення_962f286b.remove(열쇠); }
    public int Розмір() { return запис_значення_962f286b.size(); }
    public void очищати_Зміст() { запис_значення_962f286b.clear(); }
}
