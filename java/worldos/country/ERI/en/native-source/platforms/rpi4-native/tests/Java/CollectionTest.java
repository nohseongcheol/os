// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class CollectionTest {
    public static void main(String[] a) {
        List<String> entryList = new ArrayList<String>(); entryList.add("한글"); entryList.add("😀"); entryList.add("日本語");
        System.out.println(entryList.get(1)); System.out.println(entryList.set(1, "changeValue")); System.out.println(entryList.remove(0));
        System.out.println(entryList.size()); System.out.println(entryList.get(0));
        Map<String, Integer> Dictionary = new HashMap<String, Integer>();
        Dictionary.put("oneValue", 1); Dictionary.put("둘", 2); System.out.println(Dictionary.put("oneValue", 3).intValue());
        System.out.println(Dictionary.get("oneValue").intValue()); System.out.println(Dictionary.containsKey("둘"));
        System.gc(); System.out.println(Dictionary.remove("둘").intValue()); System.out.println(Dictionary.size());
        entryList.clear(); Dictionary.clear(); System.out.println(entryList.isEmpty()); System.out.println(Dictionary.isEmpty());
        System.out.println("한글😀Characters".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("text")));
        String keep = "남는 text"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
