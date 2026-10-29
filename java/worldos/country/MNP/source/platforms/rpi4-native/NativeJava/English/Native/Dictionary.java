// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
import java.util.HashMap;
/** Maps lookup keys to values. */
public final class Dictionary {
    private final HashMap<String, String> entryValue = new HashMap<String, String>();
    public String putValue(String keyMaterial, String value) { return entryValue.put(keyMaterial, value); }
    public String findEntry(String keyMaterial) { return entryValue.get(keyMaterial); }
    public boolean doesExist(String keyMaterial) { return entryValue.containsKey(keyMaterial); }
    public String eraseEntry(String keyMaterial) { return entryValue.remove(keyMaterial); }
    public int size() { return entryValue.size(); }
    public void clearContents() { entryValue.clear(); }
}
