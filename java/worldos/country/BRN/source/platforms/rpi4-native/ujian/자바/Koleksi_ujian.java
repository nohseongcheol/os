// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class Koleksi_ujian {
    public static void main(String[] a) {
        List<String> pemasukan_Senarai = new ArrayList<String>(); pemasukan_Senarai.add("한글"); pemasukan_Senarai.add("😀"); pemasukan_Senarai.add("日本語");
        System.out.println(pemasukan_Senarai.get(1)); System.out.println(pemasukan_Senarai.set(1, "ubah_VALUE")); System.out.println(pemasukan_Senarai.remove(0));
        System.out.println(pemasukan_Senarai.size()); System.out.println(pemasukan_Senarai.get(0));
        Map<String, Integer> kamus = new HashMap<String, Integer>();
        kamus.put("하나", 1); kamus.put("둘", 2); System.out.println(kamus.put("하나", 3).intValue());
        System.out.println(kamus.get("하나").intValue()); System.out.println(kamus.containsKey("둘"));
        System.gc(); System.out.println(kamus.remove("둘").intValue()); System.out.println(kamus.size());
        pemasukan_Senarai.clear(); kamus.clear(); System.out.println(pemasukan_Senarai.isEmpty()); System.out.println(kamus.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Teks")));
        String keep = "남는 Teks"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
