// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class sokaság_teszt {
    public static void main(String[] a) {
        List<String> bejegyzés_Lista = new ArrayList<String>(); bejegyzés_Lista.add("한글"); bejegyzés_Lista.add("😀"); bejegyzés_Lista.add("日本語");
        System.out.println(bejegyzés_Lista.get(1)); System.out.println(bejegyzés_Lista.set(1, "módosítás_ÉRTÉK")); System.out.println(bejegyzés_Lista.remove(0));
        System.out.println(bejegyzés_Lista.size()); System.out.println(bejegyzés_Lista.get(0));
        Map<String, Integer> szótár = new HashMap<String, Integer>();
        szótár.put("하나", 1); szótár.put("둘", 2); System.out.println(szótár.put("하나", 3).intValue());
        System.out.println(szótár.get("하나").intValue()); System.out.println(szótár.containsKey("둘"));
        System.gc(); System.out.println(szótár.remove("둘").intValue()); System.out.println(szótár.size());
        bejegyzés_Lista.clear(); szótár.clear(); System.out.println(bejegyzés_Lista.isEmpty()); System.out.println(szótár.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Szöveg")));
        String keep = "남는 Szöveg"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
