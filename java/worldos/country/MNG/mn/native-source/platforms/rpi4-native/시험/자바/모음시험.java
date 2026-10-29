// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> оролт_Жагсаалт = new ArrayList<String>(); оролт_Жагсаалт.add("한글"); оролт_Жагсаалт.add("😀"); оролт_Жагсаалт.add("日本語");
        System.out.println(оролт_Жагсаалт.get(1)); System.out.println(оролт_Жагсаалт.set(1, "өөрчлөх_утга")); System.out.println(оролт_Жагсаалт.remove(0));
        System.out.println(оролт_Жагсаалт.size()); System.out.println(оролт_Жагсаалт.get(0));
        Map<String, Integer> Толь_бичиг = new HashMap<String, Integer>();
        Толь_бичиг.put("하나", 1); Толь_бичиг.put("둘", 2); System.out.println(Толь_бичиг.put("하나", 3).intValue());
        System.out.println(Толь_бичиг.get("하나").intValue()); System.out.println(Толь_бичиг.containsKey("둘"));
        System.gc(); System.out.println(Толь_бичиг.remove("둘").intValue()); System.out.println(Толь_бичиг.size());
        оролт_Жагсаалт.clear(); Толь_бичиг.clear(); System.out.println(оролт_Жагсаалт.isEmpty()); System.out.println(Толь_бичиг.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Бичвэр")));
        String keep = "남는 Бичвэр"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
