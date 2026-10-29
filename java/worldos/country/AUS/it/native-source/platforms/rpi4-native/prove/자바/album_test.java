// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class album_test {
    public static void main(String[] a) {
        List<String> voce_elenco = new ArrayList<String>(); voce_elenco.add("한글"); voce_elenco.add("😀"); voce_elenco.add("日本語");
        System.out.println(voce_elenco.get(1)); System.out.println(voce_elenco.set(1, "cambiare_VALORE")); System.out.println(voce_elenco.remove(0));
        System.out.println(voce_elenco.size()); System.out.println(voce_elenco.get(0));
        Map<String, Integer> dizionario = new HashMap<String, Integer>();
        dizionario.put("하나", 1); dizionario.put("둘", 2); System.out.println(dizionario.put("하나", 3).intValue());
        System.out.println(dizionario.get("하나").intValue()); System.out.println(dizionario.containsKey("둘"));
        System.gc(); System.out.println(dizionario.remove("둘").intValue()); System.out.println(dizionario.size());
        voce_elenco.clear(); dizionario.clear(); System.out.println(voce_elenco.isEmpty()); System.out.println(dizionario.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("testo")));
        String keep = "남는 testo"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
