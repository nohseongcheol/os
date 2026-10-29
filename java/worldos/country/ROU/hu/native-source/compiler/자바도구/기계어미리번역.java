// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java tanóra_ÉRTÉK 파일에서 독립 ARM64 커널용 C 원문을 만든다. gazda JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Fordítás_hiba extends RuntimeException {
        Fordítás_hiba(String 설명) { super(설명); }
    }
    static final class adat_Olvasó {
        final byte[] adat;
        int Pozíció;
        adat_Olvasó(byte[] bevitel_adat) { adat = bevitel_adat; }
        byte[] Olvasás(int hossz_ÉRTÉK) {
            if (hossz_ÉRTÉK < 0 || hossz_ÉRTÉK > adat.length - Pozíció) throw new Fordítás_hiba("잘린 tanóra_ÉRTÉK 또는 Parancs adat");
            byte[] KR = Arrays.copyOfRange(adat, Pozíció, Pozíció + hossz_ÉRTÉK); Pozíció += hossz_ÉRTÉK; return KR;
        }
        int 한바이트() { if (Pozíció >= adat.length) throw new Fordítás_hiba("잘린 Parancs adat"); return adat[Pozíció++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class tag_adat {
        final int hozzáfér_bejegyzés;
        final String Név, 서술;
        final Map<String, byte[]> attribútum_ÉRTÉK;
        tag_adat(int hozzáfér_ÉRTÉK, String név_ÉRTÉK, String 서술값, Map<String, byte[]> attribútum_adat) {
            hozzáfér_bejegyzés = hozzáfér_ÉRTÉK; Név = név_ÉRTÉK; 서술 = 서술값; attribútum_ÉRTÉK = attribútum_adat;
        }
    }
    static final class metódus_hivatkozik implements Comparable<metódus_hivatkozik> {
        final String tulajdonos_ÉRTÉK, Név, 서술;
        metódus_hivatkozik(String 소유값, String név_ÉRTÉK, String 서술값) { tulajdonos_ÉRTÉK = 소유값; Név = név_ÉRTÉK; 서술 = 서술값; }
        String[] 부분들() { return new String[]{tulajdonos_ÉRTÉK, Név, 서술}; }
        public int compareTo(metódus_hivatkozik társ_ÉRTÉK) {
            int Összehasonlítás_ÉRTÉK = tulajdonos_ÉRTÉK.compareTo(társ_ÉRTÉK.tulajdonos_ÉRTÉK);
            if (Összehasonlítás_ÉRTÉK == 0) Összehasonlítás_ÉRTÉK = Név.compareTo(társ_ÉRTÉK.Név);
            return Összehasonlítás_ÉRTÉK == 0 ? 서술.compareTo(társ_ÉRTÉK.서술) : Összehasonlítás_ÉRTÉK;
        }
        public boolean equals(Object társ_ÉRTÉK) { return társ_ÉRTÉK instanceof metódus_hivatkozik && compareTo((metódus_hivatkozik) társ_ÉRTÉK) == 0; }
        public int hashCode() { return Objects.hash(tulajdonos_ÉRTÉK, Név, 서술); }
    }
    static final class tanóra_adat {
        final int[] állandó_Altípus;
        final Object[] állandó_adat;
        final String Név;
        final List<tag_adat> mezőérték, FÜGGVÉNY_ÉRTÉK;
        tanóra_adat(Path ÚTVONAL) throws IOException {
            adat_Olvasó Olvasó_ÉRTÉK = new adat_Olvasó(Files.readAllBytes(ÚTVONAL));
            if (Olvasó_ÉRTÉK.네바이트() != 0xcafebabe) throw new Fordítás_hiba("Java tanóra_ÉRTÉK 표식이 아님");
            Olvasó_ÉRTÉK.Olvasás(4);
            int cikk_DARAB = Olvasó_ÉRTÉK.두바이트(); állandó_Altípus = new int[cikk_DARAB]; állandó_adat = new Object[cikk_DARAB];
            for (int 순번 = 1; 순번 < cikk_DARAB; 순번++) {
                int Altípus_ÉRTÉK = Olvasó_ÉRTÉK.한바이트(); állandó_Altípus[순번] = Altípus_ÉRTÉK;
                switch (Altípus_ÉRTÉK) {
                    case 1:
                        int hossz_ÉRTÉK = Olvasó_ÉRTÉK.두바이트();
                        byte[] karakter_puffer = Olvasó_ÉRTÉK.Olvasás(hossz_ÉRTÉK), 길이붙인자료 = new byte[hossz_ÉRTÉK + 2];
                        길이붙인자료[0] = (byte)(hossz_ÉRTÉK >> 8); 길이붙인자료[1] = (byte)hossz_ÉRTÉK;
                        System.arraycopy(karakter_puffer, 0, 길이붙인자료, 2, hossz_ÉRTÉK);
                        állandó_adat[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: állandó_adat[순번] = Olvasó_ÉRTÉK.네바이트(); break;
                    case 4: Olvasó_ÉRTÉK.Olvasás(4); break;
                    case 5: case 6: Olvasó_ÉRTÉK.Olvasás(8); 순번++; break;
                    case 7: case 8: case 16: állandó_adat[순번] = Olvasó_ÉRTÉK.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        állandó_adat[순번] = new int[]{Olvasó_ÉRTÉK.두바이트(), Olvasó_ÉRTÉK.두바이트()}; break;
                    case 15: állandó_adat[순번] = new int[]{Olvasó_ÉRTÉK.한바이트(), Olvasó_ÉRTÉK.두바이트()}; break;
                    default: throw new Fordítás_hiba("지원하지 않는 állandó_ÉRTÉK Altípus_ÉRTÉK: " + Altípus_ÉRTÉK);
                }
            }
            Olvasó_ÉRTÉK.두바이트(); Név = osztálynév(Olvasó_ÉRTÉK.두바이트());
            if (!osztálynév(Olvasó_ÉRTÉK.두바이트()).equals("java/lang/Object") || Olvasó_ÉRTÉK.두바이트() != 0)
                throw new Fordítás_hiba(Név + ": 상속 및 인터페이스 미지원");
            mezőérték = 멤버읽기(Olvasó_ÉRTÉK); FÜGGVÉNY_ÉRTÉK = 멤버읽기(Olvasó_ÉRTÉK); 속성읽기(Olvasó_ÉRTÉK);
            if (Olvasó_ÉRTÉK.Pozíció != Olvasó_ÉRTÉK.adat.length) throw new Fordítás_hiba("tanóra_ÉRTÉK 뒤에 남은 adat");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= állandó_Altípus.length || állandó_Altípus[INDEX] != 1) throw new Fordítás_hiba("문자 állandó_ÉRTÉK INDEX HIBA");
            return (String) állandó_adat[INDEX];
        }
        String osztálynév(int INDEX) {
            if (INDEX < 1 || INDEX >= állandó_Altípus.length || állandó_Altípus[INDEX] != 7) throw new Fordítás_hiba("tanóra_ÉRTÉK hivatkozik HIBA");
            return 문자((Integer)állandó_adat[INDEX]);
        }
        metódus_hivatkozik hivatkozik(int INDEX) {
            if (INDEX < 1 || INDEX >= állandó_Altípus.length || állandó_Altípus[INDEX] < 9 || állandó_Altípus[INDEX] > 11) throw new Fordítás_hiba("멤버 hivatkozik HIBA");
            int[] párosít_ÉRTÉK = (int[])állandó_adat[INDEX], név_párosít = (int[])állandó_adat[párosít_ÉRTÉK[1]];
            return new metódus_hivatkozik(osztálynév(párosít_ÉRTÉK[0]), 문자(név_párosít[0]), 문자(név_párosít[1]));
        }
        Map<String, byte[]> 속성읽기(adat_Olvasó Olvasó_ÉRTÉK) {
            Map<String, byte[]> KR = new LinkedHashMap<>();
            int cikk_DARAB = Olvasó_ÉRTÉK.두바이트();
            for (int 순번 = 0; 순번 < cikk_DARAB; 순번++) {
                String attribútum_név = 문자(Olvasó_ÉRTÉK.두바이트()); byte[] ÉRTÉK = Olvasó_ÉRTÉK.Olvasás(Olvasó_ÉRTÉK.네바이트());
                if (KR.put(attribútum_név, ÉRTÉK) != null) throw new Fordítás_hiba("겹친 attribútum_ÉRTÉK: " + attribútum_név);
            }
            return KR;
        }
        List<tag_adat> 멤버읽기(adat_Olvasó Olvasó_ÉRTÉK) {
            List<tag_adat> KR = new ArrayList<>(); int cikk_DARAB = Olvasó_ÉRTÉK.두바이트();
            for (int 순번 = 0; 순번 < cikk_DARAB; 순번++) {
                int hozzáfér_bejegyzés = Olvasó_ÉRTÉK.두바이트(); String metódus_bejegyzés_név = 문자(Olvasó_ÉRTÉK.두바이트()), 서술 = 문자(Olvasó_ÉRTÉK.두바이트());
                KR.add(new tag_adat(hozzáfér_bejegyzés, metódus_bejegyzés_név, 서술, 속성읽기(Olvasó_ÉRTÉK)));
            }
            return KR;
        }
    }
    static final class 함수형식 {
        final List<String> Argumentumok = new ArrayList<>();
        final String visszaküld_KR;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Fordítás_hiba("FÜGGVÉNY_ÉRTÉK 서술 HIBA: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Fordítás_hiba("FÜGGVÉNY_ÉRTÉK 서술 HIBA: " + 서술);
            Argumentumok.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Argumentumok.contains("V") || 반환들.size() != 1) throw new Fordítás_hiba("FÜGGVÉNY_ÉRTÉK 서술 HIBA: " + 서술);
            visszaküld_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> KR = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Pozíció = 0; Pozíció < 서술.length();) {
            String kijelölés_ÉRTÉK = null;
            for (String formáz_ÉRTÉK : 허용형식) if (서술.startsWith(formáz_ÉRTÉK, Pozíció)) { kijelölés_ÉRTÉK = formáz_ÉRTÉK; break; }
            if (kijelölés_ÉRTÉK == null) throw new Fordítás_hiba("지원하지 않는 adattípus: " + 서술);
            KR.add(kijelölés_ÉRTÉK); Pozíció += kijelölés_ÉRTÉK.length();
        }
        return KR;
    }
    static String szimbólum(String Altípus_ÉRTÉK, String... 부분들) {
        try {
            byte[] kivonat_Fájl = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Szöveg = new StringBuilder("j_" + Altípus_ÉRTÉK + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Szöveg.append(String.format(Locale.ROOT, "%02x", kivonat_Fájl[순번] & 255));
            return Szöveg.toString();
        } catch (Exception HIBA) { throw new Fordítás_hiba(HIBA.toString()); }
    }
    final Map<String, tanóra_adat> 클래스들 = new TreeMap<>();
    final Map<metódus_hivatkozik, tag_adat> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), gép_Functions_c3a8e64a = new LinkedHashMap<>();
    final String végrehajtás_cél, gép_tanóra;
    final int halommemória_szó_DARAB;
    final Path erőforrás_útvonal;
    기계어미리번역(List<Path> útvonal_Lista, String cél, int 낱말수, Path erőforrás_ÉRTÉK) throws IOException {
        if ((!cél.equals("kernel") && !cél.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Fordítás_hiba("végrehajt_parancs cél 또는 Memória_ÉRTÉK CÍM_régió Méret HIBA");
        végrehajtás_cél = cél; halommemória_szó_DARAB = 낱말수; erőforrás_útvonal = erőforrás_ÉRTÉK;
        // 이 이름도 국가별 forrás_fa generálás 시 해당 언어로 옮긴다.
        gép_tanóra = cél.equals("kernel") ? "fal" : "felhasználó";
        for (String Vonal : Files.readAllLines(erőforrás_ÉRTÉK.resolve("gép_Functions.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Vonal.split("\t", -1);
            if (부분들.length != 4) throw new Fordítás_hiba("gép FÜGGVÉNY_ÉRTÉK adat HIBA");
            if (부분들[0].equals(cél)) gép_Functions_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path ÚTVONAL : útvonal_Lista) {
            tanóra_adat adat = new tanóra_adat(ÚTVONAL);
            if (클래스들.put(adat.Név, adat) != null) throw new Fordítás_hiba("중복 tanóra_ÉRTÉK: " + adat.Név);
            for (tag_adat mezőérték : adat.mezőérték) {
                if ((mezőérték.hozzáfér_bejegyzés & 8) == 0 || 형식읽기(mezőérték.서술).equals(Collections.singletonList("V"))) throw new Fordítás_hiba("statikus_ÉRTÉK 필드만 támogat_ÉRTÉK");
                if (필드들.put(new metódus_hivatkozik(adat.Név, mezőérték.Név, mezőérték.서술), mezőérték) != null) throw new Fordítás_hiba("중복 mezőérték");
            }
            for (tag_adat FÜGGVÉNY_ÉRTÉK : adat.FÜGGVÉNY_ÉRTÉK) {
                if (FÜGGVÉNY_ÉRTÉK.Név.equals("<init>")) continue;
                if ((FÜGGVÉNY_ÉRTÉK.hozzáfér_bejegyzés & 8) == 0 || (FÜGGVÉNY_ÉRTÉK.hozzáfér_bejegyzés & (0x20 | 0x400)) != 0) throw new Fordítás_hiba("statikus_ÉRTÉK 비동기화 함수만 támogat_ÉRTÉK");
                new 함수형식(FÜGGVÉNY_ÉRTÉK.서술);
                if (함수들.put(new metódus_hivatkozik(adat.Név, FÜGGVÉNY_ÉRTÉK.Név, FÜGGVÉNY_ÉRTÉK.서술), FÜGGVÉNY_ÉRTÉK) != null) throw new Fordítás_hiba("중복 FÜGGVÉNY_ÉRTÉK");
            }
        }
    }
    String sztring_szimbólum(String Szöveg) { return 문자열들.computeIfAbsent(Szöveg, ÉRTÉK -> "j_text_" + 문자열들.size()); }
    String állandó_kifejezés(tanóra_adat adat, int INDEX) {
        if (INDEX < 1 || INDEX >= adat.állandó_Altípus.length) throw new Fordítás_hiba("állandó_ÉRTÉK INDEX klip HIBA");
        if (adat.állandó_Altípus[INDEX] == 3) return "(word)(uint32_t)(" + adat.állandó_adat[INDEX] + ")";
        if (adat.állandó_Altípus[INDEX] == 8) return "(word)" + sztring_szimbólum(adat.문자((Integer)adat.állandó_adat[INDEX]));
        throw new Fordítás_hiba("정수와 sztring_ÉRTÉK 상수만 támogat_ÉRTÉK");
    }
    String 함수원형(metódus_hivatkozik hivatkozik) {
        List<String> 인수들 = new ArrayList<>(); int cikk_DARAB = new 함수형식(hivatkozik.서술).Argumentumok.size();
        for (int 순번 = 0; 순번 < cikk_DARAB; 순번++) 인수들.add("word a" + 순번);
        return "static word " + szimbólum("method", hivatkozik.부분들()) + "(" + (cikk_DARAB == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void csekk_helyi(int INDEX, int helyi_változó_DARAB) { if (INDEX < 0 || INDEX >= helyi_változó_DARAB) throw new Fordítás_hiba("helyi_hatókör változó_ÉRTÉK INDEX klip HIBA"); }
    void 분기넣기(List<String> Kimenet, Set<Integer> ág_Lista, int Pozíció, int 이동량, String állapot) {
        int cél_ÉRTÉK = Pozíció + 이동량; ág_Lista.add(cél_ÉRTÉK);
        Kimenet.add((állapot == null ? "" : "if (" + állapot + ") ") + "goto b" + cél_ÉRTÉK + ";");
    }
    String metódus_törzs(metódus_hivatkozik FÜGGVÉNY_ÉRTÉK, tag_adat adat) {
        byte[] törzs_adat = adat.attribútum_ÉRTÉK.get("Code"); if (törzs_adat == null) throw new Fordítás_hiba("FÜGGVÉNY_ÉRTÉK 몸체가 없음: " + FÜGGVÉNY_ÉRTÉK.Név);
        adat_Olvasó Olvasó_ÉRTÉK = new adat_Olvasó(törzs_adat); int 쌓임깊이 = Olvasó_ÉRTÉK.두바이트(), helyi_változó_DARAB = Olvasó_ÉRTÉK.두바이트();
        adat_Olvasó parancs_adat = new adat_Olvasó(Olvasó_ÉRTÉK.Olvasás(Olvasó_ÉRTÉK.네바이트()));
        if (Olvasó_ÉRTÉK.두바이트() != 0) throw new Fordítás_hiba("try/catch/finally 미지원");
        함수형식 formáz_ÉRTÉK = new 함수형식(FÜGGVÉNY_ÉRTÉK.서술); if (helyi_változó_DARAB < formáz_ÉRTÉK.Argumentumok.size()) throw new Fordítás_hiba("매개변수보다 적은 helyi_hatókör változó_ÉRTÉK");
        tanóra_adat tanóra_ÉRTÉK = 클래스들.get(FÜGGVÉNY_ÉRTÉK.tulajdonos_ÉRTÉK);
        List<String> Kimenet = new ArrayList<>(); Kimenet.add(함수원형(FÜGGVÉNY_ÉRTÉK) + " {");
        Kimenet.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(helyi_változó_DARAB, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formáz_ÉRTÉK.Argumentumok.size(); 순번++) Kimenet.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), ág_Lista = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (parancs_adat.Pozíció < parancs_adat.adat.length) {
            int Pozíció = parancs_adat.Pozíció, Parancs = parancs_adat.한바이트(); 경계들.add(Pozíció); Kimenet.add("b" + Pozíció + ":;");
            if (Parancs == 0) continue;
            if (Parancs == 1) Kimenet.add("PUSH(0);");
            else if (Parancs >= 2 && Parancs <= 8) Kimenet.add("PUSH((uint32_t)(" + (Parancs - 3) + "));");
            else if (Parancs == 16 || Parancs == 17) Kimenet.add("PUSH((uint32_t)(" + (Parancs == 16 ? parancs_adat.부호한바이트() : parancs_adat.부호두바이트()) + "));");
            else if (Parancs == 18 || Parancs == 19) Kimenet.add("PUSH(" + állandó_kifejezés(tanóra_ÉRTÉK, Parancs == 18 ? parancs_adat.한바이트() : parancs_adat.두바이트()) + ");");
            else if (Parancs == 21 || Parancs == 25 || (Parancs >= 26 && Parancs <= 29) || (Parancs >= 42 && Parancs <= 45)) {
                int INDEX = Parancs == 21 || Parancs == 25 ? parancs_adat.한바이트() : Parancs - (Parancs <= 29 ? 26 : 42);
                csekk_helyi(INDEX, helyi_változó_DARAB); Kimenet.add("PUSH(l[" + INDEX + "]);");
            } else if (Parancs == 54 || Parancs == 58 || (Parancs >= 59 && Parancs <= 62) || (Parancs >= 75 && Parancs <= 78)) {
                int INDEX = Parancs == 54 || Parancs == 58 ? parancs_adat.한바이트() : Parancs - (Parancs <= 62 ? 59 : 75);
                csekk_helyi(INDEX, helyi_változó_DARAB); Kimenet.add("l[" + INDEX + "] = POP();");
            } else if (Parancs == 46) Kimenet.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Parancs == 79) Kimenet.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Parancs == 87 || Parancs == 88) Kimenet.add(Parancs == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Parancs >= 89 && Parancs <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] rendel_Lista = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Parancs - 89]; 순번++) Kimenet.add("abcd".charAt(순번) + " = POP();");
                for (char ÉRTÉK : rendel_Lista[Parancs - 89].toCharArray()) Kimenet.add("PUSH(" + ÉRTÉK + ");");
            } else if (Parancs == 96 || Parancs == 100 || Parancs == 104 || Parancs == 126 || Parancs == 128 || Parancs == 130) {
                String műtét_ÉRTÉK = Parancs == 96 ? "+" : Parancs == 100 ? "-" : Parancs == 104 ? "*" : Parancs == 126 ? "&" : Parancs == 128 ? "|" : "^";
                Kimenet.add("b = POP(); a = POP(); PUSH((uint32_t)a " + műtét_ÉRTÉK + " (uint32_t)b);");
            } else if (Parancs == 108 || Parancs == 112) Kimenet.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Parancs == 112 ? 1 : 0) + "));");
            else if (Parancs == 116) Kimenet.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Parancs == 120 || Parancs == 122 || Parancs == 124) {
                Kimenet.add("b = POP(); a = POP();"); Kimenet.add("PUSH(" + (Parancs == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Parancs == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Parancs == 132) {
                int INDEX = parancs_adat.한바이트(), növekmény_összeg = parancs_adat.부호한바이트(); csekk_helyi(INDEX, helyi_változó_DARAB);
                Kimenet.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + növekmény_összeg + ");");
            } else if (Parancs >= 145 && Parancs <= 147) Kimenet.add("a = POP(); PUSH((uint32_t)(" + (Parancs == 145 ? "int8_t" : Parancs == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Parancs >= 153 && Parancs <= 158) {
                Kimenet.add("a = POP();"); 분기넣기(Kimenet, ág_Lista, Pozíció, parancs_adat.부호두바이트(), "(int32_t)a " + 비교들[Parancs - 153] + " 0");
            } else if (Parancs >= 159 && Parancs <= 166) {
                Kimenet.add("b = POP(); a = POP();"); 분기넣기(Kimenet, ág_Lista, Pozíció, parancs_adat.부호두바이트(), Parancs >= 165 ? "a " + 비교들[Parancs - 159] + " b" : "(int32_t)a " + 비교들[Parancs - 159] + " (int32_t)b");
            } else if (Parancs == 167 || Parancs == 200) 분기넣기(Kimenet, ág_Lista, Pozíció, Parancs == 167 ? parancs_adat.부호두바이트() : parancs_adat.네바이트(), null);
            else if (Parancs == 170 || Parancs == 171) {
                while (parancs_adat.Pozíció % 4 != 0) parancs_adat.한바이트();
                int alapértelmezett_érték = parancs_adat.네바이트(); Kimenet.add("a = POP();");
                if (Parancs == 170) {
                    int 아래 = parancs_adat.네바이트(), 위 = parancs_adat.네바이트(); long cikk_DARAB = (long)위 - 아래 + 1;
                    if (cikk_DARAB < 1 || cikk_DARAB > (parancs_adat.adat.length - parancs_adat.Pozíció) / 4) throw new Fordítás_hiba("switch klip HIBA");
                    for (long ÉRTÉK = 아래; ÉRTÉK <= 위; ÉRTÉK++) 분기넣기(Kimenet, ág_Lista, Pozíció, parancs_adat.네바이트(), "(int32_t)a == (" + ÉRTÉK + ")");
                } else {
                    int cikk_DARAB = parancs_adat.네바이트(), elülső_kamera_adat = 0;
                    if (cikk_DARAB < 0 || cikk_DARAB > (parancs_adat.adat.length - parancs_adat.Pozíció) / 8) throw new Fordítás_hiba("switch Méret HIBA");
                    for (int 순번 = 0; 순번 < cikk_DARAB; 순번++) {
                        int ÉRTÉK = parancs_adat.네바이트(); if (순번 > 0 && ÉRTÉK <= elülső_kamera_adat) throw new Fordítás_hiba("switch rendel_ÉRTÉK HIBA"); elülső_kamera_adat = ÉRTÉK;
                        분기넣기(Kimenet, ág_Lista, Pozíció, parancs_adat.네바이트(), "(int32_t)a == (" + ÉRTÉK + ")");
                    }
                }
                분기넣기(Kimenet, ág_Lista, Pozíció, alapértelmezett_érték, null);
            } else if (Parancs == 172 || Parancs == 176 || Parancs == 177) Kimenet.add("return " + (Parancs == 177 ? "0" : "POP()") + ";");
            else if (Parancs == 178 || Parancs == 179) {
                metódus_hivatkozik hivatkozik = tanóra_ÉRTÉK.hivatkozik(parancs_adat.두바이트()); if (!필드들.containsKey(hivatkozik)) throw new Fordítás_hiba("알 szám 없는 mezőérték");
                Kimenet.add(szimbólum("init", hivatkozik.tulajdonos_ÉRTÉK) + "();"); String mezőérték = szimbólum("field", hivatkozik.부분들());
                Kimenet.add(Parancs == 178 ? "PUSH(" + mezőérték + ");" : mezőérték + " = POP();");
            } else if (Parancs == 184) {
                metódus_hivatkozik hivatkozik = tanóra_ÉRTÉK.hivatkozik(parancs_adat.두바이트()); if (!함수들.containsKey(hivatkozik)) throw new Fordítás_hiba("알 szám 없는 FÜGGVÉNY_ÉRTÉK");
                함수형식 호출형식 = new 함수형식(hivatkozik.서술); int cikk_DARAB = 호출형식.Argumentumok.size();
                Kimenet.add(szimbólum("init", hivatkozik.tulajdonos_ÉRTÉK) + "();"); Kimenet.add("if(sp < " + cikk_DARAB + ") kernel_panic(\"call stack underflow\"); sp -= " + cikk_DARAB + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < cikk_DARAB; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Kimenet.add("a = " + szimbólum("method", hivatkozik.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.visszaküld_KR.equals("V")) Kimenet.add("PUSH(a);");
            } else if (Parancs == 182) {
                metódus_hivatkozik hivatkozik = tanóra_ÉRTÉK.hivatkozik(parancs_adat.두바이트());
                if (hivatkozik.equals(new metódus_hivatkozik("java/lang/String", "length", "()I"))) Kimenet.add("a = POP(); PUSH(length(a));");
                else if (hivatkozik.equals(new metódus_hivatkozik("java/lang/String", "charAt", "(I)C"))) Kimenet.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Fordítás_hiba("가상 FÜGGVÉNY_ÉRTÉK 호출 미지원");
            } else if (Parancs == 188) {
                if (parancs_adat.한바이트() != 10) throw new Fordítás_hiba("new int[]만 támogat_ÉRTÉK"); Kimenet.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Parancs == 190) Kimenet.add("a = POP(); PUSH(length(a));");
            else if (Parancs == 196) {
                int bővítmény_ÉRTÉK = parancs_adat.한바이트(), INDEX = parancs_adat.두바이트(); csekk_helyi(INDEX, helyi_változó_DARAB);
                if (bővítmény_ÉRTÉK == 21 || bővítmény_ÉRTÉK == 25) Kimenet.add("PUSH(l[" + INDEX + "]);");
                else if (bővítmény_ÉRTÉK == 54 || bővítmény_ÉRTÉK == 58) Kimenet.add("l[" + INDEX + "] = POP();");
                else if (bővítmény_ÉRTÉK == 132) Kimenet.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + parancs_adat.부호두바이트() + ");");
                else throw new Fordítás_hiba("미지원 wide Parancs");
            } else if (Parancs == 198 || Parancs == 199) {
                Kimenet.add("a = POP();"); 분기넣기(Kimenet, ág_Lista, Pozíció, parancs_adat.부호두바이트(), "a " + (Parancs == 198 ? "==" : "!=") + " 0");
            } else throw new Fordítás_hiba(FÜGGVÉNY_ÉRTÉK.tulajdonos_ÉRTÉK + "." + FÜGGVÉNY_ÉRTÉK.Név + ", bájt_ÉRTÉK " + Pozíció + ": 미지원 Parancs " + Parancs);
        }
        if (!경계들.containsAll(ág_Lista)) throw new Fordítás_hiba("Parancs 경계가 아닌 곳으로 ág");
        Kimenet.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Kimenet);
    }
    String exportál_metódus(String csatol_szimbólum, String cél, boolean 진입점여부) {
        int helyzetindex = cél.lastIndexOf('.'); if (helyzetindex < 0 || !csatol_szimbólum.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Fordítás_hiba("내보내기 átruház_ÉRTÉK HIBA");
        String tulajdonos_ÉRTÉK = cél.substring(0, helyzetindex).replace('.', '/'), Név = cél.substring(helyzetindex + 1); metódus_hivatkozik kijelölés_ÉRTÉK = null;
        for (metódus_hivatkozik hivatkozik : 함수들.keySet()) if (hivatkozik.tulajdonos_ÉRTÉK.equals(tulajdonos_ÉRTÉK) && hivatkozik.Név.equals(Név)) {
            if (kijelölés_ÉRTÉK != null) throw new Fordítás_hiba("겹친 내보내기 cél"); kijelölés_ÉRTÉK = hivatkozik;
        }
        if (kijelölés_ÉRTÉK == null || (함수들.get(kijelölés_ÉRTÉK).hozzáfér_bejegyzés & 0x100) != 0) throw new Fordítás_hiba("내보낼 함수가 없음 또는 native FÜGGVÉNY_ÉRTÉK");
        함수형식 formáz_ÉRTÉK = new 함수형식(kijelölés_ÉRTÉK.서술);
        if ((진입점여부 && !formáz_ÉRTÉK.Argumentumok.isEmpty()) || !Arrays.asList("V", "I").contains(formáz_ÉRTÉK.visszaküld_KR)) throw new Fordítás_hiba("belépési_pont_ÉRTÉK 또는 C határ_ÉRTÉK formáz_ÉRTÉK HIBA");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formáz_ÉRTÉK.Argumentumok.size(); 순번++) {
            if (!formáz_ÉRTÉK.Argumentumok.get(순번).equals("I")) throw new Fordítás_hiba("C 경계는 int 인수만 támogat_ÉRTÉK");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formáz_ÉRTÉK.visszaküld_KR.equals("V") ? "void " : "int32_t ") + csatol_szimbólum + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + szimbólum("init", kijelölés_ÉRTÉK.tulajdonos_ÉRTÉK) + "(); " + (formáz_ÉRTÉK.visszaküld_KR.equals("V") ? "" : "return (int32_t)") + szimbólum("method", kijelölés_ÉRTÉK.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generálás(String belépési_pont, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metódus_hivatkozik, tag_adat> bejegyzés_ÉRTÉK : 함수들.entrySet()) {
            metódus_hivatkozik hivatkozik = bejegyzés_ÉRTÉK.getKey(); tag_adat adat = bejegyzés_ÉRTÉK.getValue(); 선언들.add(함수원형(hivatkozik) + ";");
            if ((adat.hozzáfér_bejegyzés & 0x100) != 0) {
                String Kapcsolódás = gép_Functions_c3a8e64a.get(hivatkozik.Név + hivatkozik.서술);
                if (!hivatkozik.tulajdonos_ÉRTÉK.equals(gép_tanóra) || Kapcsolódás == null) throw new Fordítás_hiba("허용되지 않은 native FÜGGVÉNY_ÉRTÉK: " + hivatkozik.Név);
                int cikk_DARAB = new 함수형식(hivatkozik.서술).Argumentumok.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < cikk_DARAB; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Kapcsolódás + "(" + (cikk_DARAB == 0 ? "void" : String.join(",", Collections.nCopies(cikk_DARAB, "word"))) + ");");
                몸체들.add(함수원형(hivatkozik) + " { return " + Kapcsolódás + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metódus_törzs(hivatkozik, adat));
        }
        for (Map.Entry<metódus_hivatkozik, tag_adat> bejegyzés_ÉRTÉK : 필드들.entrySet()) {
            metódus_hivatkozik hivatkozik = bejegyzés_ÉRTÉK.getKey(); byte[] állandó_ÉRTÉK = bejegyzés_ÉRTÉK.getValue().attribútum_ÉRTÉK.get("ConstantValue");
            String ÉRTÉK = állandó_ÉRTÉK == null ? "0" : állandó_kifejezés(클래스들.get(hivatkozik.tulajdonos_ÉRTÉK), new adat_Olvasó(állandó_ÉRTÉK).두바이트());
            필드선언들.add("static word " + szimbólum("field", hivatkozik.부분들()) + " = " + ÉRTÉK + ";");
        }
        for (String Név : 클래스들.keySet()) {
            String inicializál = szimbólum("init", Név), Állapot_ÉRTÉK = szimbólum("state", Név);
            선언들.add("static void " + inicializál + "(void);"); 필드선언들.add("static unsigned " + Állapot_ÉRTÉK + ";");
            metódus_hivatkozik hivatkozik = new metódus_hivatkozik(Név, "<clinit>", "()V");
            몸체들.add("static void " + inicializál + "(void) { if(" + Állapot_ÉRTÉK + ") return; " + Állapot_ÉRTÉK + " = 1; " + (함수들.containsKey(hivatkozik) ? szimbólum("method", hivatkozik.부분들()) + "(); " : "") + Állapot_ÉRTÉK + " = 2; }");
        }
        몸체들.add(exportál_metódus("java_entry", belépési_pont, true)); Set<String> 공개이름 = new HashSet<>();
        for (String átruház_ÉRTÉK : 내보내기목록) {
            int helyzetindex = átruház_ÉRTÉK.indexOf('='); if (helyzetindex < 1) throw new Fordítás_hiba("내보내기 átruház_ÉRTÉK HIBA");
            String Név = átruház_ÉRTÉK.substring(0, helyzetindex); 공개이름.add(Név); 몸체들.add(exportál_metódus(Név, átruház_ÉRTÉK.substring(helyzetindex + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> bejegyzés_ÉRTÉK : 문자열들.entrySet()) {
            String Szöveg = bejegyzés_ÉRTÉK.getKey(); StringBuilder TÖMB_ÉRTÉK = new StringBuilder("static const word " + bejegyzés_ÉRTÉK.getValue() + "[] = {" + Szöveg.length());
            for (int 순번 = 0; 순번 < Szöveg.length(); 순번++) TÖMB_ÉRTÉK.append(", ").append((int)Szöveg.charAt(순번));
            문자열선언들.add(TÖMB_ÉRTÉK.append("};").toString());
        }
        String támogat_ÉRTÉK = Files.readString(erőforrás_útvonal.resolve("CLR_támogat.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(halommemória_szó_DARAB));
        return 기계원문한국어화(támogat_ÉRTÉK + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String FORRÁS, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> név_tábla = new HashMap<>();
        for (String Vonal : Files.readAllLines(erőforrás_útvonal.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] párosít_ÉRTÉK = Vonal.split("\t"); név_tábla.put(párosít_ÉRTÉK[0], párosít_ÉRTÉK[1]);
        }
        Pattern adatrészlet_kifejezés = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = adatrészlet_kifejezés.matcher(FORRÁS); StringBuffer KR = new StringBuffer();
        while (찾개.find()) {
            String Név = 찾개.group(), 새이름 = Név;
            if (!Név.startsWith("//") && !Név.startsWith("/*") && !Név.startsWith("\"") && !Név.startsWith("'") && !공개이름.contains(Név)) {
                새이름 = név_tábla.getOrDefault(Név, Név);
                if (Név.matches("a[0-9]+")) 새이름 = "Argumentumok" + Név.substring(1);
                if (Név.matches("b[0-9]+")) 새이름 = "ág" + Név.substring(1);
                if (범용표기) {
                    StringBuilder jelölés_ÉRTÉK = new StringBuilder();
                    for (char karakter_ÉRTÉK : 새이름.toCharArray()) jelölés_ÉRTÉK.append(karakter_ÉRTÉK < 128 ? Character.toString(karakter_ÉRTÉK) : String.format(Locale.ROOT, "\\u%04x", (int)karakter_ÉRTÉK));
                    새이름 = jelölés_ÉRTÉK.toString();
                }
            }
            찾개.appendReplacement(KR, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(KR); return KR.toString();
    }
    String X_86_metódus_törzs(metódus_hivatkozik FÜGGVÉNY_ÉRTÉK, tag_adat adat, Map<String,String> gép_tábla, String cél) {
        String jelölő_ÉRTÉK = szimbólum("method", FÜGGVÉNY_ÉRTÉK.부분들());
        List<String> Vonal = new ArrayList<>();
        if ((adat.hozzáfér_bejegyzés & 0x100) != 0) {
            String Kapcsolódás = gép_tábla.get(FÜGGVÉNY_ÉRTÉK.Név + FÜGGVÉNY_ÉRTÉK.서술);
            if (!FÜGGVÉNY_ÉRTÉK.tulajdonos_ÉRTÉK.equals(cél.equals("kernel") ? "mobil_ÉRTÉK" : "felhasználó") || Kapcsolódás == null) throw new Fordítás_hiba("허용되지 않은 native FÜGGVÉNY_ÉRTÉK");
            return ".text\n" + jelölő_ÉRTÉK + ":\njmp " + Kapcsolódás;
        }
        byte[] törzsszöveg = adat.attribútum_ÉRTÉK.get("Code"); if (törzsszöveg == null) throw new Fordítás_hiba("FÜGGVÉNY_ÉRTÉK 몸체가 없음");
        adat_Olvasó Olvasó_ÉRTÉK = new adat_Olvasó(törzsszöveg); Olvasó_ÉRTÉK.두바이트(); int helyi_DARAB = Olvasó_ÉRTÉK.두바이트();
        adat_Olvasó parancs_adat = new adat_Olvasó(Olvasó_ÉRTÉK.Olvasás(Olvasó_ÉRTÉK.네바이트()));
        if (Olvasó_ÉRTÉK.두바이트() != 0) throw new Fordítás_hiba("try/catch/finally 미지원");
        함수형식 formáz_ÉRTÉK = new 함수형식(FÜGGVÉNY_ÉRTÉK.서술); if (helyi_DARAB < formáz_ÉRTÉK.Argumentumok.size()) throw new Fordítás_hiba("매개변수보다 적은 helyi_hatókör változó_ÉRTÉK");
        Collections.addAll(Vonal,".text",".globl " + jelölő_ÉRTÉK,".type " + jelölő_ÉRTÉK + ", @function",jelölő_ÉRTÉK + ":","pushl %ebp","movl %esp, %ebp","subl $" + helyi_DARAB * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formáz_ÉRTÉK.Argumentumok.size(); 순번++) Collections.addAll(Vonal,"movl " + (8 + 4 * (formáz_ÉRTÉK.Argumentumok.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        tanóra_adat tanóra_ÉRTÉK = 클래스들.get(FÜGGVÉNY_ÉRTÉK.tulajdonos_ÉRTÉK); Set<Integer> 경계들 = new HashSet<>(), ág_Lista = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (parancs_adat.Pozíció < parancs_adat.adat.length) {
            int Pozíció = parancs_adat.Pozíció, Parancs = parancs_adat.한바이트(); String helyzetindex = jelölő_ÉRTÉK + "_b" + Pozíció;
            Vonal.add(helyzetindex + ":"); 경계들.add(Pozíció);
            if (Parancs == 0) Vonal.add("nop");
            else if (Parancs == 1) Vonal.add("pushl $0");
            else if (Parancs >= 2 && Parancs <= 8) Vonal.add("pushl $" + (Parancs - 3));
            else if (Parancs == 16 || Parancs == 17) Vonal.add("pushl $" + (Parancs == 16 ? parancs_adat.부호한바이트() : parancs_adat.부호두바이트()));
            else if (Parancs == 18 || Parancs == 19) {
                int INDEX = Parancs == 18 ? parancs_adat.한바이트() : parancs_adat.두바이트();
                Vonal.add("pushl $" + X_86_állandó(tanóra_ÉRTÉK,INDEX));
            } else if (Parancs == 21 || Parancs == 25 || (Parancs >= 26 && Parancs <= 29) || (Parancs >= 42 && Parancs <= 45) || Parancs == 54 || Parancs == 58 || (Parancs >= 59 && Parancs <= 62) || (Parancs >= 75 && Parancs <= 78)) {
                boolean 읽음 = Parancs < 54; int INDEX = Parancs == 21 || Parancs == 25 || Parancs == 54 || Parancs == 58 ? parancs_adat.한바이트() : Parancs - (Parancs <= 29 ? 26 : Parancs <= 45 ? 42 : Parancs <= 62 ? 59 : 75);
                csekk_helyi(INDEX,helyi_DARAB); Vonal.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Parancs == 46) Collections.addAll(Vonal,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Parancs == 79) Collections.addAll(Vonal,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Parancs == 87 || Parancs == 88) Vonal.add("addl $" + (Parancs == 87 ? 4 : 8) + ", %esp");
            else if (Parancs >= 89 && Parancs <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] rendel_Lista = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Parancs - 89]; 순번++) Vonal.add("popl " + 저장기들[순번]);
                for (int 순번 : rendel_Lista[Parancs - 89]) Vonal.add("pushl " + 저장기들[순번]);
            } else if (Parancs == 96 || Parancs == 100 || Parancs == 104 || Parancs == 126 || Parancs == 128 || Parancs == 130) {
                String műtét_ÉRTÉK = Parancs == 96 ? "addl" : Parancs == 100 ? "subl" : Parancs == 104 ? "imull" : Parancs == 126 ? "andl" : Parancs == 128 ? "orl" : "xorl";
                Collections.addAll(Vonal,"popl %ecx","popl %eax",műtét_ÉRTÉK + " %ecx, %eax","pushl %eax");
            } else if (Parancs == 108 || Parancs == 112) Collections.addAll(Vonal,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + helyzetindex + "_divide","cmpl $0x80000000, %eax","jne " + helyzetindex + "_divide","xorl %edx, %edx","jmp " + helyzetindex + "_done",helyzetindex + "_divide:","cltd","idivl %ecx",helyzetindex + "_done:","pushl " + (Parancs == 108 ? "%eax" : "%edx"));
            else if (Parancs == 116) Vonal.add("negl (%esp)");
            else if (Parancs == 120 || Parancs == 122 || Parancs == 124) Collections.addAll(Vonal,"popl %ecx","popl %eax",(Parancs == 120 ? "sall" : Parancs == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Parancs == 132) {
                int INDEX = parancs_adat.한바이트(), növekmény_ÉRTÉK = parancs_adat.부호한바이트(); csekk_helyi(INDEX,helyi_DARAB); Vonal.add("addl $" + növekmény_ÉRTÉK + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Parancs >= 145 && Parancs <= 147) Collections.addAll(Vonal,"popl %eax",Parancs == 145 ? "movsbl %al, %eax" : Parancs == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Parancs >= 153 && Parancs <= 166) {
                if (Parancs <= 158) Collections.addAll(Vonal,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Vonal,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int cél_ÉRTÉK = Pozíció + parancs_adat.부호두바이트(); ág_Lista.add(cél_ÉRTÉK); Vonal.add(비교들[Parancs - (Parancs <= 158 ? 153 : 159)] + " " + jelölő_ÉRTÉK + "_b" + cél_ÉRTÉK);
            } else if (Parancs == 167 || Parancs == 200) {
                int cél_ÉRTÉK = Pozíció + (Parancs == 167 ? parancs_adat.부호두바이트() : parancs_adat.네바이트()); ág_Lista.add(cél_ÉRTÉK); Vonal.add("jmp " + jelölő_ÉRTÉK + "_b" + cél_ÉRTÉK);
            } else if (Parancs == 170 || Parancs == 171) {
                while (parancs_adat.Pozíció % 4 != 0) parancs_adat.한바이트();
                int alapértelmezett_érték = Pozíció + parancs_adat.네바이트(); ág_Lista.add(alapértelmezett_érték); Vonal.add("popl %eax");
                int cikk_DARAB, 아래 = 0;
                if (Parancs == 170) { 아래 = parancs_adat.네바이트(); int 위 = parancs_adat.네바이트(); long hossz_ÉRTÉK = (long)위 - 아래 + 1; if (hossz_ÉRTÉK < 1 || hossz_ÉRTÉK > (parancs_adat.adat.length - parancs_adat.Pozíció) / 4) throw new Fordítás_hiba("switch klip HIBA"); cikk_DARAB = (int)hossz_ÉRTÉK; }
                else { cikk_DARAB = parancs_adat.네바이트(); if (cikk_DARAB < 0 || cikk_DARAB > (parancs_adat.adat.length - parancs_adat.Pozíció) / 8) throw new Fordítás_hiba("switch Méret HIBA"); }
                for (int 순번 = 0; 순번 < cikk_DARAB; 순번++) {
                    int ÉRTÉK = Parancs == 170 ? 아래 + 순번 : parancs_adat.네바이트(), cél_ÉRTÉK = Pozíció + parancs_adat.네바이트(); ág_Lista.add(cél_ÉRTÉK);
                    Collections.addAll(Vonal,"cmpl $" + ÉRTÉK + ", %eax","je " + jelölő_ÉRTÉK + "_b" + cél_ÉRTÉK);
                }
                Vonal.add("jmp " + jelölő_ÉRTÉK + "_b" + alapértelmezett_érték);
            } else if (Parancs == 172 || Parancs == 176 || Parancs == 177) {
                if (Parancs != 177) Vonal.add("popl %eax"); Collections.addAll(Vonal,"leave","ret");
            } else if (Parancs == 178 || Parancs == 179) {
                metódus_hivatkozik hivatkozik = tanóra_ÉRTÉK.hivatkozik(parancs_adat.두바이트()); if (!필드들.containsKey(hivatkozik)) throw new Fordítás_hiba("알 szám 없는 mezőérték");
                Collections.addAll(Vonal,"call " + szimbólum("init",hivatkozik.tulajdonos_ÉRTÉK),(Parancs == 178 ? "pushl " : "popl ") + szimbólum("field",hivatkozik.부분들()));
            } else if (Parancs == 184) {
                metódus_hivatkozik hivatkozik = tanóra_ÉRTÉK.hivatkozik(parancs_adat.두바이트()); if (!함수들.containsKey(hivatkozik)) throw new Fordítás_hiba("알 szám 없는 FÜGGVÉNY_ÉRTÉK");
                함수형식 호출형식 = new 함수형식(hivatkozik.서술); Collections.addAll(Vonal,"call " + szimbólum("init",hivatkozik.tulajdonos_ÉRTÉK),"call " + szimbólum("method",hivatkozik.부분들()));
                if (!호출형식.Argumentumok.isEmpty()) Vonal.add("addl $" + 호출형식.Argumentumok.size() * 4 + ", %esp");
                if (!호출형식.visszaküld_KR.equals("V")) Vonal.add("pushl %eax");
            } else if (Parancs == 182) {
                metódus_hivatkozik hivatkozik = tanóra_ÉRTÉK.hivatkozik(parancs_adat.두바이트());
                if (hivatkozik.equals(new metódus_hivatkozik("java/lang/String","length","()I"))) Collections.addAll(Vonal,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (hivatkozik.equals(new metódus_hivatkozik("java/lang/String","charAt","(I)C"))) Collections.addAll(Vonal,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Fordítás_hiba("가상 FÜGGVÉNY_ÉRTÉK 호출 미지원");
            } else if (Parancs == 188) {
                if (parancs_adat.한바이트() != 10) throw new Fordítás_hiba("new int[]만 támogat_ÉRTÉK"); Collections.addAll(Vonal,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Parancs == 190) Collections.addAll(Vonal,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Parancs == 196) {
                int bővítmény_ÉRTÉK = parancs_adat.한바이트(), INDEX = parancs_adat.두바이트(); csekk_helyi(INDEX,helyi_DARAB);
                if (bővítmény_ÉRTÉK == 21 || bővítmény_ÉRTÉK == 25 || bővítmény_ÉRTÉK == 54 || bővítmény_ÉRTÉK == 58) Vonal.add((bővítmény_ÉRTÉK <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (bővítmény_ÉRTÉK == 132) Vonal.add("addl $" + parancs_adat.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Fordítás_hiba("wide Parancs 미지원");
            } else if (Parancs == 198 || Parancs == 199) {
                int cél_ÉRTÉK = Pozíció + parancs_adat.부호두바이트(); ág_Lista.add(cél_ÉRTÉK); Collections.addAll(Vonal,"popl %eax","testl %eax, %eax",(Parancs == 198 ? "je " : "jne ") + jelölő_ÉRTÉK + "_b" + cél_ÉRTÉK);
            } else throw new Fordítás_hiba("미지원 Parancs: " + Parancs);
        }
        if (!경계들.containsAll(ág_Lista)) throw new Fordítás_hiba("Parancs 경계가 아닌 곳으로 ág");
        Vonal.add(".size " + jelölő_ÉRTÉK + ", .-" + jelölő_ÉRTÉK); return String.join("\n",Vonal);
    }
    String X_86_állandó(tanóra_adat adat, int INDEX) {
        if (adat.állandó_Altípus[INDEX] == 3) return adat.állandó_adat[INDEX].toString();
        if (adat.állandó_Altípus[INDEX] == 8) return sztring_szimbólum(adat.문자((Integer)adat.állandó_adat[INDEX]));
        throw new Fordítás_hiba("정수와 sztring_ÉRTÉK 상수만 támogat_ÉRTÉK");
    }
    String X_86_szerelvény(String belépési_pont, List<String> 내보냄, String cél) throws IOException {
        Map<String,String> gép_tábla = new HashMap<>();
        for (String Vonal : Files.readAllLines(erőforrás_útvonal.resolve("_86_gép_Functions.tsv"))) { String[] párosít_ÉRTÉK = Vonal.split("\t"); if (párosít_ÉRTÉK[0].equals(cél)) gép_tábla.put(párosít_ÉRTÉK[1] + párosít_ÉRTÉK[2],párosít_ÉRTÉK[3]); }
        int helyzetindex = belépési_pont.lastIndexOf('.'); if (helyzetindex < 0) throw new Fordítás_hiba("belépési_pont átruház_ÉRTÉK HIBA");
        String tulajdonos_ÉRTÉK = belépési_pont.substring(0,helyzetindex).replace('.','/'), metódus_bejegyzés_név = belépési_pont.substring(helyzetindex + 1); metódus_hivatkozik belépési_pont_ÉRTÉK = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metódus_hivatkozik hivatkozik = new metódus_hivatkozik(tulajdonos_ÉRTÉK,metódus_bejegyzés_név,서술); if (함수들.containsKey(hivatkozik)) { if (belépési_pont_ÉRTÉK != null) throw new Fordítás_hiba("겹친 belépési_pont"); belépési_pont_ÉRTÉK = hivatkozik; } }
        if (belépési_pont_ÉRTÉK == null || (함수들.get(belépési_pont_ÉRTÉK).hozzáfér_bejegyzés & 0x100) != 0) throw new Fordítás_hiba("belépési_pont_ÉRTÉK FÜGGVÉNY_ÉRTÉK formáz_ÉRTÉK HIBA");
        List<String> Vonal = new ArrayList<>(); Vonal.add(".code32");
        for (tanóra_adat adat : 클래스들.values()) {
            String Állapot_ÉRTÉK = szimbólum("state",adat.Név), inicializál = szimbólum("init",adat.Név);
            Collections.addAll(Vonal,".bss",".balign 4",Állapot_ÉRTÉK + ": .long 0",".text",inicializál + ":","cmpl $0, " + Állapot_ÉRTÉK,"jne " + inicializál + "_done","movl $1, " + Állapot_ÉRTÉK);
            metódus_hivatkozik 초기화참조 = new metódus_hivatkozik(adat.Név,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Vonal.add("call " + szimbólum("method",초기화참조.부분들()));
            Collections.addAll(Vonal,"movl $2, " + Állapot_ÉRTÉK,inicializál + "_done:","ret");
            for (tag_adat mezőérték : adat.mezőérték) {
                byte[] állandó_ÉRTÉK = mezőérték.attribútum_ÉRTÉK.get("ConstantValue"); String ÉRTÉK = állandó_ÉRTÉK == null ? "0" : X_86_állandó(adat,new adat_Olvasó(állandó_ÉRTÉK).두바이트());
                Collections.addAll(Vonal,".data",".balign 4",szimbólum("field",adat.Név,mezőérték.Név,mezőérték.서술) + ": .long " + ÉRTÉK);
            }
            for (tag_adat FÜGGVÉNY_ÉRTÉK : adat.FÜGGVÉNY_ÉRTÉK) if (!FÜGGVÉNY_ÉRTÉK.Név.equals("<init>")) Vonal.add(X_86_metódus_törzs(new metódus_hivatkozik(adat.Név,FÜGGVÉNY_ÉRTÉK.Név,FÜGGVÉNY_ÉRTÉK.서술),FÜGGVÉNY_ÉRTÉK,gép_tábla,cél));
        }
        Collections.addAll(Vonal,".text",".globl java_entry","java_entry:","call " + szimbólum("init",belépési_pont_ÉRTÉK.tulajdonos_ÉRTÉK),"call " + szimbólum("method",belépési_pont_ÉRTÉK.부분들()));
        if (belépési_pont_ÉRTÉK.서술.equals("()V")) Vonal.add("xorl %eax, %eax"); Vonal.add("ret");
        for (String átruház_ÉRTÉK : 내보냄) {
            int elválasztó_karakter_ÉRTÉK = átruház_ÉRTÉK.indexOf('='); if (elválasztó_karakter_ÉRTÉK < 1) throw new Fordítás_hiba("내보내기 átruház_ÉRTÉK HIBA");
            String külső_ÉRTÉK = átruház_ÉRTÉK.substring(0,elválasztó_karakter_ÉRTÉK), FÜGGVÉNY_ÉRTÉK = átruház_ÉRTÉK.substring(elválasztó_karakter_ÉRTÉK + 1); int osztás_KR = FÜGGVÉNY_ÉRTÉK.lastIndexOf('.');
            if (osztás_KR < 0 || !külső_ÉRTÉK.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Fordítás_hiba("내보내기 szimbólum HIBA");
            String tanóra_ÉRTÉK = FÜGGVÉNY_ÉRTÉK.substring(0,osztás_KR).replace('.','/'), Név = FÜGGVÉNY_ÉRTÉK.substring(osztás_KR + 1); metódus_hivatkozik kijelölés_ÉRTÉK = null;
            for (metódus_hivatkozik hivatkozik : 함수들.keySet()) if (hivatkozik.tulajdonos_ÉRTÉK.equals(tanóra_ÉRTÉK) && hivatkozik.Név.equals(Név)) { if (kijelölés_ÉRTÉK != null) throw new Fordítás_hiba("겹친 내보내기 cél"); kijelölés_ÉRTÉK = hivatkozik; }
            if (kijelölés_ÉRTÉK == null) throw new Fordítás_hiba("내보낼 함수가 없음");
            Collections.addAll(Vonal,".text",".globl " + külső_ÉRTÉK,külső_ÉRTÉK + ":","call " + szimbólum("init",kijelölés_ÉRTÉK.tulajdonos_ÉRTÉK),"jmp " + szimbólum("method",kijelölés_ÉRTÉK.부분들()));
        }
        Vonal.add(".section .rodata");
        for (Map.Entry<String,String> bejegyzés_ÉRTÉK : 문자열들.entrySet()) {
            Collections.addAll(Vonal,".balign 4",bejegyzés_ÉRTÉK.getValue() + ":",".long " + bejegyzés_ÉRTÉK.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char lecke_ÉRTÉK : bejegyzés_ÉRTÉK.getKey().toCharArray()) 단위들.add(Integer.toString(lecke_ÉRTÉK)); if (!단위들.isEmpty()) Vonal.add(".long " + String.join(",",단위들));
        }
        Vonal.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Vonal) + "\n";
    }
    static void végrehajt_eszköz(List<String> Parancs) throws Exception {
        if (new ProcessBuilder(Parancs).inheritIO().start().waitFor() != 0) throw new Fordítás_hiba("épít_forrás HIBA: " + Parancs.get(0));
    }
    static String adat_sztring(String Szöveg) { return "\"" + Szöveg.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Fordítás(List<Path> bevitel_Lista, String cél, String belépési_pont, List<String> 내보냄, Path Kimenet, Path erőforrás_ÉRTÉK) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), tanóra_útvonal = 임시.resolve("classes"); Files.createDirectory(tanóra_útvonal);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",tanóra_útvonal.toString(),"-sourcepath",tanóra_útvonal.toString(),"-d",tanóra_útvonal.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int forrás_DARAB = 0;
            for (Path bevitel_ÉRTÉK : bevitel_Lista) {
                if (Kimenet.toAbsolutePath().normalize().equals(bevitel_ÉRTÉK.toAbsolutePath().normalize())) throw new Fordítás_hiba("Kimenet 파일과 입력이 같음");
                if (bevitel_ÉRTÉK.toString().endsWith(".java")) { 자바명령.add(bevitel_ÉRTÉK.toString()); forrás_DARAB++; }
                else if (bevitel_ÉRTÉK.toString().endsWith(".class")) 바이트코드.add(bevitel_ÉRTÉK);
                else throw new Fordítás_hiba(".java 또는 .class만 támogat_ÉRTÉK");
            }
            if (forrás_DARAB > 0) végrehajt_eszköz(자바명령);
            try (java.util.stream.Stream<Path> útvonal_Lista = Files.walk(tanóra_útvonal)) { útvonal_Lista.filter(ÚTVONAL -> ÚTVONAL.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 konvertál_ÉRTÉK = new 기계어미리번역(바이트코드,cél.equals("user") ? "user" : "kernel",262144,erőforrás_ÉRTÉK);
            String fordít_ÉRTÉK = konvertál_ÉRTÉK.X_86_szerelvény(belépési_pont,내보냄,cél); Files.writeString(임시.resolve("program.s"),fordít_ÉRTÉK,StandardCharsets.UTF_8);
            Path eszköz_pozíció = erőforrás_ÉRTÉK.getParent();
            végrehajt_eszköz(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            végrehajt_eszköz(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),eszköz_pozíció.resolve("CLR_támogat.s").toString()));
            List<String> Kapcsolódás = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (cél.equals("kernel")) Kapcsolódás.add("-r");
            else {
                végrehajt_eszköz(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),eszköz_pozíció.resolve(cél.equals("user") ? "START_felhasználó_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(Kapcsolódás,"-e","_start",임시.resolve("start.o").toString());
                if (cél.equals("user")) Collections.addAll(Kapcsolódás,"-T",eszköz_pozíció.resolve("felhasználó_csatol_Navigáció.ld").toString());
            }
            Collections.addAll(Kapcsolódás,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); végrehajt_eszköz(Kapcsolódás);
            Kimenet = Kimenet.toAbsolutePath(); Files.createDirectories(Kimenet.getParent()); Path közzétesz_ÉRTÉK = Files.createTempFile(Kimenet.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),közzétesz_ÉRTÉK,StandardCopyOption.REPLACE_EXISTING); Files.move(közzétesz_ÉRTÉK,Kimenet,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(közzétesz_ÉRTÉK); }
            Files.setPosixFilePermissions(Kimenet,java.nio.file.attribute.PosixFilePermissions.fromString(cél.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Kimenet + ".s"),fordít_ÉRTÉK,StandardCharsets.UTF_8);
            List<String> szimbólum_adat = new ArrayList<>(), forrás_adat = new ArrayList<>();
            for (metódus_hivatkozik hivatkozik : konvertál_ÉRTÉK.함수들.keySet()) szimbólum_adat.add(adat_sztring(szimbólum("method",hivatkozik.부분들())) + ":" + adat_sztring(hivatkozik.tulajdonos_ÉRTÉK + "." + hivatkozik.Név + hivatkozik.서술));
            for (Path bevitel_ÉRTÉK : bevitel_Lista) {
                byte[] kivonat_Fájl = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(bevitel_ÉRTÉK)); StringBuilder Szöveg = new StringBuilder(); for (byte ÉRTÉK : kivonat_Fájl) Szöveg.append(String.format(Locale.ROOT,"%02x",ÉRTÉK & 255));
                forrás_adat.add(adat_sztring(bevitel_ÉRTÉK.toAbsolutePath().toString()) + ":" + adat_sztring(Szöveg.toString()));
            }
            Files.writeString(Paths.get(Kimenet + ".json"),"{\"target\":" + adat_sztring(cél) + ",\"entry\":" + adat_sztring(belépési_pont) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",szimbólum_adat) + "},\"sources\":{" + String.join(",",forrás_adat) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> útvonal_Lista = Files.walk(임시)) { for (Path ÚTVONAL : (Iterable<Path>)útvonal_Lista.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(ÚTVONAL); }
        }
    }
    public static void main(String[] Argumentumok) {
        try {
            String belépési_pont = null, cél = "kernel", X_86_cél = null; Path kimenet_útvonal = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> útvonal_Lista = new ArrayList<>();
            for (int 순번 = 0; 순번 < Argumentumok.length; 순번++) {
                String ÉRTÉK = Argumentumok[순번];
                switch (ÉRTÉK) {
                    case "--target": X_86_cél = Argumentumok[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry tanóra_ÉRTÉK.FÜGGVÉNY_ÉRTÉK -o Kimenet [--target linux|kernel|user] [--profile kernel|user] [--export szimbólum=tanóra_ÉRTÉK.FÜGGVÉNY_ÉRTÉK] 클래스파일 또는 Java원문"); return;
                    case "--entry": belépési_pont = Argumentumok[++순번]; break;
                    case "--profile": cél = Argumentumok[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Argumentumok[++순번]); break;
                    case "--export": 내보냄.add(Argumentumok[++순번]); break;
                    case "-o": kimenet_útvonal = Paths.get(Argumentumok[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (ÉRTÉK.startsWith("-")) throw new Fordítás_hiba("알 szám 없는 옵션: " + ÉRTÉK); útvonal_Lista.add(Paths.get(ÉRTÉK));
                }
            }
            if (belépési_pont == null || kimenet_útvonal == null || útvonal_Lista.isEmpty()) throw new Fordítás_hiba("--entry, -o, tanóra_ÉRTÉK 파일이 필요합니다");
            Path erőforrás_ÉRTÉK = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_cél != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_cél)) throw new Fordítás_hiba("알 szám 없는 végrehajt_parancs cél");
                X_86_Fordítás(útvonal_Lista,X_86_cél,belépési_pont,내보냄,kimenet_útvonal,erőforrás_ÉRTÉK); return;
            }
            String FORRÁS = new 기계어미리번역(útvonal_Lista, cél, 낱말수, erőforrás_ÉRTÉK).generálás(belépési_pont, 내보냄, 범용표기);
            kimenet_útvonal = kimenet_útvonal.toAbsolutePath(); Files.createDirectories(kimenet_útvonal.getParent());
            Path 임시 = Files.createTempFile(kimenet_útvonal.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, FORRÁS, StandardCharsets.UTF_8); Files.move(임시, kimenet_útvonal, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception HIBA) { System.err.println("épít_forrás HIBA: " + HIBA.getMessage()); System.exit(1); }
    }
}
