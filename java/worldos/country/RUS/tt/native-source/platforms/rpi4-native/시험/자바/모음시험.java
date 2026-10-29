// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> кертү_Исемлек = new ArrayList<String>(); кертү_Исемлек.add("한글"); кертү_Исемлек.add("😀"); кертү_Исемлек.add("日本語");
        System.out.println(кертү_Исемлек.get(1)); System.out.println(кертү_Исемлек.set(1, "үзгәртү_VALUE")); System.out.println(кертү_Исемлек.remove(0));
        System.out.println(кертү_Исемлек.size()); System.out.println(кертү_Исемлек.get(0));
        Map<String, Integer> сүзлек = new HashMap<String, Integer>();
        сүзлек.put("하나", 1); сүзлек.put("둘", 2); System.out.println(сүзлек.put("하나", 3).intValue());
        System.out.println(сүзлек.get("하나").intValue()); System.out.println(сүзлек.containsKey("둘"));
        System.gc(); System.out.println(сүзлек.remove("둘").intValue()); System.out.println(сүзлек.size());
        кертү_Исемлек.clear(); сүзлек.clear(); System.out.println(кертү_Исемлек.isEmpty()); System.out.println(сүзлек.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Mäten")));
        String keep = "남는 Mäten"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
