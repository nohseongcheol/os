// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> tsenyo_lenaane = new ArrayList<String>(); tsenyo_lenaane.add("한글"); tsenyo_lenaane.add("😀"); tsenyo_lenaane.add("日本語");
        System.out.println(tsenyo_lenaane.get(1)); System.out.println(tsenyo_lenaane.set(1, "fetola_Boleng")); System.out.println(tsenyo_lenaane.remove(0));
        System.out.println(tsenyo_lenaane.size()); System.out.println(tsenyo_lenaane.get(0));
        Map<String, Integer> bukantswe = new HashMap<String, Integer>();
        bukantswe.put("하나", 1); bukantswe.put("둘", 2); System.out.println(bukantswe.put("하나", 3).intValue());
        System.out.println(bukantswe.get("하나").intValue()); System.out.println(bukantswe.containsKey("둘"));
        System.gc(); System.out.println(bukantswe.remove("둘").intValue()); System.out.println(bukantswe.size());
        tsenyo_lenaane.clear(); bukantswe.clear(); System.out.println(tsenyo_lenaane.isEmpty()); System.out.println(bukantswe.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
