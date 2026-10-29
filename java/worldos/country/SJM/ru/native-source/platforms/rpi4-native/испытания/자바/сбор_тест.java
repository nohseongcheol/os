// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class сбор_тест {
    public static void main(String[] a) {
        List<String> ввод_Список = new ArrayList<String>(); ввод_Список.add("한글"); ввод_Список.add("😀"); ввод_Список.add("日本語");
        System.out.println(ввод_Список.get(1)); System.out.println(ввод_Список.set(1, "изменить_ЗНАЧЕН")); System.out.println(ввод_Список.remove(0));
        System.out.println(ввод_Список.size()); System.out.println(ввод_Список.get(0));
        Map<String, Integer> словарь = new HashMap<String, Integer>();
        словарь.put("하나", 1); словарь.put("둘", 2); System.out.println(словарь.put("하나", 3).intValue());
        System.out.println(словарь.get("하나").intValue()); System.out.println(словарь.containsKey("둘"));
        System.gc(); System.out.println(словарь.remove("둘").intValue()); System.out.println(словарь.size());
        ввод_Список.clear(); словарь.clear(); System.out.println(ввод_Список.isEmpty()); System.out.println(словарь.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("текст")));
        String keep = "남는 текст"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
