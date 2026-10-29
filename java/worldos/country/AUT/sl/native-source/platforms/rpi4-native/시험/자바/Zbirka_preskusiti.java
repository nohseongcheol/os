// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class Zbirka_preskusiti {
    public static void main(String[] a) {
        List<String> vnos_Seznam = new ArrayList<String>(); vnos_Seznam.add("한글"); vnos_Seznam.add("😀"); vnos_Seznam.add("日本語");
        System.out.println(vnos_Seznam.get(1)); System.out.println(vnos_Seznam.set(1, "spremeniti_VALUE")); System.out.println(vnos_Seznam.remove(0));
        System.out.println(vnos_Seznam.size()); System.out.println(vnos_Seznam.get(0));
        Map<String, Integer> slovar = new HashMap<String, Integer>();
        slovar.put("하나", 1); slovar.put("둘", 2); System.out.println(slovar.put("하나", 3).intValue());
        System.out.println(slovar.get("하나").intValue()); System.out.println(slovar.containsKey("둘"));
        System.gc(); System.out.println(slovar.remove("둘").intValue()); System.out.println(slovar.size());
        vnos_Seznam.clear(); slovar.clear(); System.out.println(vnos_Seznam.isEmpty()); System.out.println(slovar.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Besedilo")));
        String keep = "남는 Besedilo"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
