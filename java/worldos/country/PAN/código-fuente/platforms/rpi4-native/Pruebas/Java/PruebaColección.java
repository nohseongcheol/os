// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class PruebaColección {
    public static void main(String[] a) {
        List<String> listaEntradaElemento = new ArrayList<String>(); listaEntradaElemento.add("한글"); listaEntradaElemento.add("😀"); listaEntradaElemento.add("日本語");
        System.out.println(listaEntradaElemento.get(1)); System.out.println(listaEntradaElemento.set(1, "cambiarValor")); System.out.println(listaEntradaElemento.remove(0));
        System.out.println(listaEntradaElemento.size()); System.out.println(listaEntradaElemento.get(0));
        Map<String, Integer> Diccionario = new HashMap<String, Integer>();
        Diccionario.put("valorUno", 1); Diccionario.put("둘", 2); System.out.println(Diccionario.put("valorUno", 3).intValue());
        System.out.println(Diccionario.get("valorUno").intValue()); System.out.println(Diccionario.containsKey("둘"));
        System.gc(); System.out.println(Diccionario.remove("둘").intValue()); System.out.println(Diccionario.size());
        listaEntradaElemento.clear(); Diccionario.clear(); System.out.println(listaEntradaElemento.isEmpty()); System.out.println(Diccionario.isEmpty());
        System.out.println("한글😀Caracteres".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("texto")));
        String keep = "남는 texto"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
