// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class inkaso_test {
    public static void main(String[] a) {
        List<String> položka_Seznam = new ArrayList<String>(); položka_Seznam.add("한글"); položka_Seznam.add("😀"); položka_Seznam.add("日本語");
        System.out.println(položka_Seznam.get(1)); System.out.println(položka_Seznam.set(1, "změnit_HODNOTA")); System.out.println(položka_Seznam.remove(0));
        System.out.println(položka_Seznam.size()); System.out.println(položka_Seznam.get(0));
        Map<String, Integer> slovník = new HashMap<String, Integer>();
        slovník.put("하나", 1); slovník.put("둘", 2); System.out.println(slovník.put("하나", 3).intValue());
        System.out.println(slovník.get("하나").intValue()); System.out.println(slovník.containsKey("둘"));
        System.gc(); System.out.println(slovník.remove("둘").intValue()); System.out.println(slovník.size());
        položka_Seznam.clear(); slovník.clear(); System.out.println(položka_Seznam.isEmpty()); System.out.println(slovník.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("text")));
        String keep = "남는 text"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
