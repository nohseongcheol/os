// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> киргизме_жазуу_Тизме = new ArrayList<String>(); киргизме_жазуу_Тизме.add("한글"); киргизме_жазуу_Тизме.add("😀"); киргизме_жазуу_Тизме.add("日本語");
        System.out.println(киргизме_жазуу_Тизме.get(1)); System.out.println(киргизме_жазуу_Тизме.set(1, "өзгөртүү_маани")); System.out.println(киргизме_жазуу_Тизме.remove(0));
        System.out.println(киргизме_жазуу_Тизме.size()); System.out.println(киргизме_жазуу_Тизме.get(0));
        Map<String, Integer> сөздүк = new HashMap<String, Integer>();
        сөздүк.put("하나", 1); сөздүк.put("둘", 2); System.out.println(сөздүк.put("하나", 3).intValue());
        System.out.println(сөздүк.get("하나").intValue()); System.out.println(сөздүк.containsKey("둘"));
        System.gc(); System.out.println(сөздүк.remove("둘").intValue()); System.out.println(сөздүк.size());
        киргизме_жазуу_Тизме.clear(); сөздүк.clear(); System.out.println(киргизме_жазуу_Тизме.isEmpty()); System.out.println(сөздүк.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Текст")));
        String keep = "남는 Текст"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
