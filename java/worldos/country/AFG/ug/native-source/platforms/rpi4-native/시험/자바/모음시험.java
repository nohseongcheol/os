// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> كىرگۈزۈش_تىزىم = new ArrayList<String>(); كىرگۈزۈش_تىزىم.add("한글"); كىرگۈزۈش_تىزىم.add("😀"); كىرگۈزۈش_تىزىم.add("日本語");
        System.out.println(كىرگۈزۈش_تىزىم.get(1)); System.out.println(كىرگۈزۈش_تىزىم.set(1, "ئۆزگەرتمەك_قىممىتى")); System.out.println(كىرگۈزۈش_تىزىم.remove(0));
        System.out.println(كىرگۈزۈش_تىزىم.size()); System.out.println(كىرگۈزۈش_تىزىم.get(0));
        Map<String, Integer> لۇغەت = new HashMap<String, Integer>();
        لۇغەت.put("하나", 1); لۇغەت.put("둘", 2); System.out.println(لۇغەت.put("하나", 3).intValue());
        System.out.println(لۇغەت.get("하나").intValue()); System.out.println(لۇغەت.containsKey("둘"));
        System.gc(); System.out.println(لۇغەت.remove("둘").intValue()); System.out.println(لۇغەت.size());
        كىرگۈزۈش_تىزىم.clear(); لۇغەت.clear(); System.out.println(كىرگۈزۈش_تىزىم.isEmpty()); System.out.println(لۇغەت.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("تېكىست")));
        String keep = "남는 تېكىست"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
