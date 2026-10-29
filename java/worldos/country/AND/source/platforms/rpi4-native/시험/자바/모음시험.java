// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> introducció_Llista = new ArrayList<String>(); introducció_Llista.add("한글"); introducció_Llista.add("😀"); introducció_Llista.add("日本語");
        System.out.println(introducció_Llista.get(1)); System.out.println(introducció_Llista.set(1, "canviar_VALOR")); System.out.println(introducció_Llista.remove(0));
        System.out.println(introducció_Llista.size()); System.out.println(introducció_Llista.get(0));
        Map<String, Integer> diccionari = new HashMap<String, Integer>();
        diccionari.put("하나", 1); diccionari.put("둘", 2); System.out.println(diccionari.put("하나", 3).intValue());
        System.out.println(diccionari.get("하나").intValue()); System.out.println(diccionari.containsKey("둘"));
        System.gc(); System.out.println(diccionari.remove("둘").intValue()); System.out.println(diccionari.size());
        introducció_Llista.clear(); diccionari.clear(); System.out.println(introducció_Llista.isEmpty()); System.out.println(diccionari.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
