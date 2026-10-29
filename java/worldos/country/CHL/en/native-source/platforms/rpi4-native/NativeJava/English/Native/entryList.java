// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
import java.util.ArrayList;
/** An ordered collection of items. This edition provides lists of strings. */
public final class entryList {
    private final ArrayList<String> entryValue = new ArrayList<String>();
    public void addValues(String value) { entryValue.add(value); }
    public String read(int orderValue) { return entryValue.get(orderValue); }
    public String replaceValue(int orderValue, String value) { return entryValue.set(orderValue, value); }
    public String eraseEntry(int orderValue) { return entryValue.remove(orderValue); }
    public int size() { return entryValue.size(); }
    public boolean isEmptyValue() { return entryValue.isEmpty(); }
    public void clearContents() { entryValue.clear(); }
}
