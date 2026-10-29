// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> introdución_Lista = new ArrayList<String>(); introdución_Lista.add("한글"); introdución_Lista.add("😀"); introdución_Lista.add("日本語");
        System.out.println(introdución_Lista.get(1)); System.out.println(introdución_Lista.set(1, "modificar_VALOR")); System.out.println(introdución_Lista.remove(0));
        System.out.println(introdución_Lista.size()); System.out.println(introdución_Lista.get(0));
        Map<String, Integer> dicionario = new HashMap<String, Integer>();
        dicionario.put("하나", 1); dicionario.put("둘", 2); System.out.println(dicionario.put("하나", 3).intValue());
        System.out.println(dicionario.get("하나").intValue()); System.out.println(dicionario.containsKey("둘"));
        System.gc(); System.out.println(dicionario.remove("둘").intValue()); System.out.println(dicionario.size());
        introdución_Lista.clear(); dicionario.clear(); System.out.println(introdución_Lista.isEmpty()); System.out.println(dicionario.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Texto")));
        String keep = "남는 Texto"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
