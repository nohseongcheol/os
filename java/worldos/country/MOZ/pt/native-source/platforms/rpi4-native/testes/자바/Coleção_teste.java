// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class Coleção_teste {
    public static void main(String[] a) {
        List<String> entrada_Lista_f07b3200 = new ArrayList<String>(); entrada_Lista_f07b3200.add("한글"); entrada_Lista_f07b3200.add("😀"); entrada_Lista_f07b3200.add("日本語");
        System.out.println(entrada_Lista_f07b3200.get(1)); System.out.println(entrada_Lista_f07b3200.set(1, "alterar_VALOR")); System.out.println(entrada_Lista_f07b3200.remove(0));
        System.out.println(entrada_Lista_f07b3200.size()); System.out.println(entrada_Lista_f07b3200.get(0));
        Map<String, Integer> dicionário = new HashMap<String, Integer>();
        dicionário.put("하나", 1); dicionário.put("둘", 2); System.out.println(dicionário.put("하나", 3).intValue());
        System.out.println(dicionário.get("하나").intValue()); System.out.println(dicionário.containsKey("둘"));
        System.gc(); System.out.println(dicionário.remove("둘").intValue()); System.out.println(dicionário.size());
        entrada_Lista_f07b3200.clear(); dicionário.clear(); System.out.println(entrada_Lista_f07b3200.isEmpty()); System.out.println(dicionário.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("texto")));
        String keep = "남는 texto"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
