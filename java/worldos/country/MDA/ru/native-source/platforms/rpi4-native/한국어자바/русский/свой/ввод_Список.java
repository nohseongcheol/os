// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;
import java.util.ArrayList;
/** ввод_Список(目錄): 순서가 있는 항목의 모음. 이 판은 строка_ЗНАЧЕН 목록을 제공한다. */
public final class ввод_Список {
    private final ArrayList<String> ввод_ЗНАЧЕН = new ArrayList<String>();
    public void 더하기(String ЗНАЧЕН) { ввод_ЗНАЧЕН.add(ЗНАЧЕН); }
    public String Чтение(int заказ_ЗНАЧЕН) { return ввод_ЗНАЧЕН.get(заказ_ЗНАЧЕН); }
    public String ЗАМЕНИТЬ_ЗНАЧЕН(int заказ_ЗНАЧЕН, String ЗНАЧЕН) { return ввод_ЗНАЧЕН.set(заказ_ЗНАЧЕН, ЗНАЧЕН); }
    public String удалить_ввод_c8dbc399(int заказ_ЗНАЧЕН) { return ввод_ЗНАЧЕН.remove(заказ_ЗНАЧЕН); }
    public int Размер() { return ввод_ЗНАЧЕН.size(); }
    public boolean ИТ_службы_пустой_ЗНАЧЕН() { return ввод_ЗНАЧЕН.isEmpty(); }
    public void очищать_Оглавление() { ввод_ЗНАЧЕН.clear(); }
}
