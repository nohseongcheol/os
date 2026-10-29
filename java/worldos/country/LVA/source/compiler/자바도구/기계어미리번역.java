// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java klase_VALUE 파일에서 독립 ARM64 커널용 C 원문을 만든다. viesot JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Tulkošana_kļūda extends RuntimeException {
        Tulkošana_kļūda(String 설명) { super(설명); }
    }
    static final class dati_Lasītājs {
        final byte[] dati;
        int Novietojums;
        dati_Lasītājs(byte[] 입력자료) { dati = 입력자료; }
        byte[] Lasīt(int 길이) {
            if (길이 < 0 || 길이 > dati.length - Novietojums) throw new Tulkošana_kļūda("잘린 klase_VALUE 또는 Komanda dati");
            byte[] mērs = Arrays.copyOfRange(dati, Novietojums, Novietojums + 길이); Novietojums += 길이; return mērs;
        }
        int 한바이트() { if (Novietojums >= dati.length) throw new Tulkošana_kļūda("잘린 Komanda dati"); return dati[Novietojums++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class elements_dati {
        final int piekļūt_ievade;
        final String Nosaukums, 서술;
        final Map<String, byte[]> atribūts_VALUE;
        elements_dati(int piekļūt_VALUE, String nosaukums_VALUE, String 서술값, Map<String, byte[]> atribūts_dati) {
            piekļūt_ievade = piekļūt_VALUE; Nosaukums = nosaukums_VALUE; 서술 = 서술값; atribūts_VALUE = atribūts_dati;
        }
    }
    static final class metode_Uzziņas implements Comparable<metode_Uzziņas> {
        final String īpašnieks_VALUE, Nosaukums, 서술;
        metode_Uzziņas(String 소유값, String nosaukums_VALUE, String 서술값) { īpašnieks_VALUE = 소유값; Nosaukums = nosaukums_VALUE; 서술 = 서술값; }
        String[] 부분들() { return new String[]{īpašnieks_VALUE, Nosaukums, 서술}; }
        public int compareTo(metode_Uzziņas vienranga_VALUE) {
            int Salīdzinājums_VALUE = īpašnieks_VALUE.compareTo(vienranga_VALUE.īpašnieks_VALUE);
            if (Salīdzinājums_VALUE == 0) Salīdzinājums_VALUE = Nosaukums.compareTo(vienranga_VALUE.Nosaukums);
            return Salīdzinājums_VALUE == 0 ? 서술.compareTo(vienranga_VALUE.서술) : Salīdzinājums_VALUE;
        }
        public boolean equals(Object vienranga_VALUE) { return vienranga_VALUE instanceof metode_Uzziņas && compareTo((metode_Uzziņas) vienranga_VALUE) == 0; }
        public int hashCode() { return Objects.hash(īpašnieks_VALUE, Nosaukums, 서술); }
    }
    static final class klase_dati {
        final int[] 상수종류;
        final Object[] konstante_dati;
        final String Nosaukums;
        final List<elements_dati> lauka_vērtība, FUNCTION_VALUE;
        klase_dati(Path CEĻŠ) throws IOException {
            dati_Lasītājs Lasītājs_VALUE = new dati_Lasītājs(Files.readAllBytes(CEĻŠ));
            if (Lasītājs_VALUE.네바이트() != 0xcafebabe) throw new Tulkošana_kļūda("Java klase_VALUE 표식이 아님");
            Lasītājs_VALUE.Lasīt(4);
            int krājums_COUNT = Lasītājs_VALUE.두바이트(); 상수종류 = new int[krājums_COUNT]; konstante_dati = new Object[krājums_COUNT];
            for (int 순번 = 1; 순번 < krājums_COUNT; 순번++) {
                int 종류 = Lasītājs_VALUE.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int 길이 = Lasītājs_VALUE.두바이트();
                        byte[] rakstzīme_buferis = Lasītājs_VALUE.Lasīt(길이), 길이붙인자료 = new byte[길이 + 2];
                        길이붙인자료[0] = (byte)(길이 >> 8); 길이붙인자료[1] = (byte)길이;
                        System.arraycopy(rakstzīme_buferis, 0, 길이붙인자료, 2, 길이);
                        konstante_dati[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: konstante_dati[순번] = Lasītājs_VALUE.네바이트(); break;
                    case 4: Lasītājs_VALUE.Lasīt(4); break;
                    case 5: case 6: Lasītājs_VALUE.Lasīt(8); 순번++; break;
                    case 7: case 8: case 16: konstante_dati[순번] = Lasītājs_VALUE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        konstante_dati[순번] = new int[]{Lasītājs_VALUE.두바이트(), Lasītājs_VALUE.두바이트()}; break;
                    case 15: konstante_dati[순번] = new int[]{Lasītājs_VALUE.한바이트(), Lasītājs_VALUE.두바이트()}; break;
                    default: throw new Tulkošana_kļūda("지원하지 않는 konstante_VALUE 종류: " + 종류);
                }
            }
            Lasītājs_VALUE.두바이트(); Nosaukums = klases_nosaukums(Lasītājs_VALUE.두바이트());
            if (!klases_nosaukums(Lasītājs_VALUE.두바이트()).equals("java/lang/Object") || Lasītājs_VALUE.두바이트() != 0)
                throw new Tulkošana_kļūda(Nosaukums + ": 상속 및 인터페이스 미지원");
            lauka_vērtība = 멤버읽기(Lasītājs_VALUE); FUNCTION_VALUE = 멤버읽기(Lasītājs_VALUE); 속성읽기(Lasītājs_VALUE);
            if (Lasītājs_VALUE.Novietojums != Lasītājs_VALUE.dati.length) throw new Tulkošana_kļūda("klase_VALUE 뒤에 남은 dati");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Tulkošana_kļūda("문자 konstante_VALUE INDEX Kļūda");
            return (String) konstante_dati[INDEX];
        }
        String klases_nosaukums(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Tulkošana_kļūda("klase_VALUE Uzziņas Kļūda");
            return 문자((Integer)konstante_dati[INDEX]);
        }
        metode_Uzziņas Uzziņas(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Tulkošana_kļūda("멤버 Uzziņas Kļūda");
            int[] savienot_pārī_VALUE = (int[])konstante_dati[INDEX], nosaukums_savienot_pārī = (int[])konstante_dati[savienot_pārī_VALUE[1]];
            return new metode_Uzziņas(klases_nosaukums(savienot_pārī_VALUE[0]), 문자(nosaukums_savienot_pārī[0]), 문자(nosaukums_savienot_pārī[1]));
        }
        Map<String, byte[]> 속성읽기(dati_Lasītājs Lasītājs_VALUE) {
            Map<String, byte[]> mērs = new LinkedHashMap<>();
            int krājums_COUNT = Lasītājs_VALUE.두바이트();
            for (int 순번 = 0; 순번 < krājums_COUNT; 순번++) {
                String atribūts_nosaukums = 문자(Lasītājs_VALUE.두바이트()); byte[] VALUE = Lasītājs_VALUE.Lasīt(Lasītājs_VALUE.네바이트());
                if (mērs.put(atribūts_nosaukums, VALUE) != null) throw new Tulkošana_kļūda("겹친 atribūts_VALUE: " + atribūts_nosaukums);
            }
            return mērs;
        }
        List<elements_dati> 멤버읽기(dati_Lasītājs Lasītājs_VALUE) {
            List<elements_dati> mērs = new ArrayList<>(); int krājums_COUNT = Lasītājs_VALUE.두바이트();
            for (int 순번 = 0; 순번 < krājums_COUNT; 순번++) {
                int piekļūt_ievade = Lasītājs_VALUE.두바이트(); String metode_ievade_nosaukums = 문자(Lasītājs_VALUE.두바이트()), 서술 = 문자(Lasītājs_VALUE.두바이트());
                mērs.add(new elements_dati(piekļūt_ievade, metode_ievade_nosaukums, 서술, 속성읽기(Lasītājs_VALUE)));
            }
            return mērs;
        }
    }
    static final class 함수형식 {
        final List<String> Parametri = new ArrayList<>();
        final String atdot_mērs;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Tulkošana_kļūda("FUNCTION_VALUE 서술 Kļūda: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Tulkošana_kļūda("FUNCTION_VALUE 서술 Kļūda: " + 서술);
            Parametri.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (Parametri.contains("V") || 반환들.size() != 1) throw new Tulkošana_kļūda("FUNCTION_VALUE 서술 Kļūda: " + 서술);
            atdot_mērs = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> mērs = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int Novietojums = 0; Novietojums < 서술.length();) {
            String atlase_VALUE = null;
            for (String formāts_VALUE : 허용형식) if (서술.startsWith(formāts_VALUE, Novietojums)) { atlase_VALUE = formāts_VALUE; break; }
            if (atlase_VALUE == null) throw new Tulkošana_kļūda("지원하지 않는 datu_tips: " + 서술);
            mērs.add(atlase_VALUE); Novietojums += atlase_VALUE.length();
        }
        return mērs;
    }
    static String simbols(String 종류, String... 부분들) {
        try {
            byte[] jaukšana_Fails = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Teksts = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Teksts.append(String.format(Locale.ROOT, "%02x", jaukšana_Fails[순번] & 255));
            return Teksts.toString();
        } catch (Exception Kļūda) { throw new Tulkošana_kļūda(Kļūda.toString()); }
    }
    final Map<String, klase_dati> 클래스들 = new TreeMap<>();
    final Map<metode_Uzziņas, elements_dati> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), mašīna_Azure_funkcijas_c3a8e64a = new LinkedHashMap<>();
    final String 실행대상, mašīna_klase;
    final int kaudze_Word_COUNT;
    final Path resurss_ceļš;
    기계어미리번역(List<Path> ceļš_Saraksts, String mērķis, int 낱말수, Path resurss_VALUE) throws IOException {
        if ((!mērķis.equals("kernel") && !mērķis.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Tulkošana_kļūda("Izpildīt_komanda mērķis 또는 atmiņa_VALUE adrese_reģions Izmērs Kļūda");
        실행대상 = mērķis; kaudze_Word_COUNT = 낱말수; resurss_ceļš = resurss_VALUE;
        // 이 이름도 국가별 avots_koks ģenerēt 시 해당 언어로 옮긴다.
        mašīna_klase = mērķis.equals("kernel") ? "Panelis" : "lietotājs";
        for (String Līniju : Files.readAllLines(resurss_VALUE.resolve("mašīna_Azure_funkcijas.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = Līniju.split("\t", -1);
            if (부분들.length != 4) throw new Tulkošana_kļūda("mašīna FUNCTION_VALUE dati Kļūda");
            if (부분들[0].equals(mērķis)) mašīna_Azure_funkcijas_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path CEĻŠ : ceļš_Saraksts) {
            klase_dati dati = new klase_dati(CEĻŠ);
            if (클래스들.put(dati.Nosaukums, dati) != null) throw new Tulkošana_kļūda("중복 klase_VALUE: " + dati.Nosaukums);
            for (elements_dati lauka_vērtība : dati.lauka_vērtība) {
                if ((lauka_vērtība.piekļūt_ievade & 8) == 0 || 형식읽기(lauka_vērtība.서술).equals(Collections.singletonList("V"))) throw new Tulkošana_kļūda("정적 필드만 Atbalsts_VALUE");
                if (필드들.put(new metode_Uzziņas(dati.Nosaukums, lauka_vērtība.Nosaukums, lauka_vērtība.서술), lauka_vērtība) != null) throw new Tulkošana_kļūda("중복 lauka_vērtība");
            }
            for (elements_dati FUNCTION_VALUE : dati.FUNCTION_VALUE) {
                if (FUNCTION_VALUE.Nosaukums.equals("<init>")) continue;
                if ((FUNCTION_VALUE.piekļūt_ievade & 8) == 0 || (FUNCTION_VALUE.piekļūt_ievade & (0x20 | 0x400)) != 0) throw new Tulkošana_kļūda("정적 비동기화 함수만 Atbalsts_VALUE");
                new 함수형식(FUNCTION_VALUE.서술);
                if (함수들.put(new metode_Uzziņas(dati.Nosaukums, FUNCTION_VALUE.Nosaukums, FUNCTION_VALUE.서술), FUNCTION_VALUE) != null) throw new Tulkošana_kļūda("중복 FUNCTION_VALUE");
            }
        }
    }
    String virkne_simbols(String Teksts) { return 문자열들.computeIfAbsent(Teksts, VALUE -> "j_text_" + 문자열들.size()); }
    String konstante_izteiksme(klase_dati dati, int INDEX) {
        if (INDEX < 1 || INDEX >= dati.상수종류.length) throw new Tulkošana_kļūda("konstante_VALUE INDEX klips Kļūda");
        if (dati.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + dati.konstante_dati[INDEX] + ")";
        if (dati.상수종류[INDEX] == 8) return "(word)" + virkne_simbols(dati.문자((Integer)dati.konstante_dati[INDEX]));
        throw new Tulkošana_kļūda("정수와 virkne_VALUE 상수만 Atbalsts_VALUE");
    }
    String 함수원형(metode_Uzziņas Uzziņas) {
        List<String> 인수들 = new ArrayList<>(); int krājums_COUNT = new 함수형식(Uzziņas.서술).Parametri.size();
        for (int 순번 = 0; 순번 < krājums_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbols("method", Uzziņas.부분들()) + "(" + (krājums_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void čeks_vietējs(int INDEX, int vietējs_mainīgais_COUNT) { if (INDEX < 0 || INDEX >= vietējs_mainīgais_COUNT) throw new Tulkošana_kļūda("vietējs_Tvērums mainīgais_VALUE INDEX klips Kļūda"); }
    void 분기넣기(List<String> Izvade, Set<Integer> zars_Saraksts, int Novietojums, int 이동량, String nosacījums) {
        int mērķis_VALUE = Novietojums + 이동량; zars_Saraksts.add(mērķis_VALUE);
        Izvade.add((nosacījums == null ? "" : "if (" + nosacījums + ") ") + "goto b" + mērķis_VALUE + ";");
    }
    String metode_pamatteksts(metode_Uzziņas FUNCTION_VALUE, elements_dati dati) {
        byte[] pamatteksts_dati = dati.atribūts_VALUE.get("Code"); if (pamatteksts_dati == null) throw new Tulkošana_kļūda("FUNCTION_VALUE 몸체가 없음: " + FUNCTION_VALUE.Nosaukums);
        dati_Lasītājs Lasītājs_VALUE = new dati_Lasītājs(pamatteksts_dati); int 쌓임깊이 = Lasītājs_VALUE.두바이트(), vietējs_mainīgais_COUNT = Lasītājs_VALUE.두바이트();
        dati_Lasītājs komanda_dati = new dati_Lasītājs(Lasītājs_VALUE.Lasīt(Lasītājs_VALUE.네바이트()));
        if (Lasītājs_VALUE.두바이트() != 0) throw new Tulkošana_kļūda("try/catch/finally 미지원");
        함수형식 formāts_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (vietējs_mainīgais_COUNT < formāts_VALUE.Parametri.size()) throw new Tulkošana_kļūda("매개변수보다 적은 vietējs_Tvērums mainīgais_VALUE");
        klase_dati klase_VALUE = 클래스들.get(FUNCTION_VALUE.īpašnieks_VALUE);
        List<String> Izvade = new ArrayList<>(); Izvade.add(함수원형(FUNCTION_VALUE) + " {");
        Izvade.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(vietējs_mainīgais_COUNT, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formāts_VALUE.Parametri.size(); 순번++) Izvade.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), zars_Saraksts = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (komanda_dati.Novietojums < komanda_dati.dati.length) {
            int Novietojums = komanda_dati.Novietojums, Komanda = komanda_dati.한바이트(); 경계들.add(Novietojums); Izvade.add("b" + Novietojums + ":;");
            if (Komanda == 0) continue;
            if (Komanda == 1) Izvade.add("PUSH(0);");
            else if (Komanda >= 2 && Komanda <= 8) Izvade.add("PUSH((uint32_t)(" + (Komanda - 3) + "));");
            else if (Komanda == 16 || Komanda == 17) Izvade.add("PUSH((uint32_t)(" + (Komanda == 16 ? komanda_dati.부호한바이트() : komanda_dati.부호두바이트()) + "));");
            else if (Komanda == 18 || Komanda == 19) Izvade.add("PUSH(" + konstante_izteiksme(klase_VALUE, Komanda == 18 ? komanda_dati.한바이트() : komanda_dati.두바이트()) + ");");
            else if (Komanda == 21 || Komanda == 25 || (Komanda >= 26 && Komanda <= 29) || (Komanda >= 42 && Komanda <= 45)) {
                int INDEX = Komanda == 21 || Komanda == 25 ? komanda_dati.한바이트() : Komanda - (Komanda <= 29 ? 26 : 42);
                čeks_vietējs(INDEX, vietējs_mainīgais_COUNT); Izvade.add("PUSH(l[" + INDEX + "]);");
            } else if (Komanda == 54 || Komanda == 58 || (Komanda >= 59 && Komanda <= 62) || (Komanda >= 75 && Komanda <= 78)) {
                int INDEX = Komanda == 54 || Komanda == 58 ? komanda_dati.한바이트() : Komanda - (Komanda <= 62 ? 59 : 75);
                čeks_vietējs(INDEX, vietējs_mainīgais_COUNT); Izvade.add("l[" + INDEX + "] = POP();");
            } else if (Komanda == 46) Izvade.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Komanda == 79) Izvade.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Komanda == 87 || Komanda == 88) Izvade.add(Komanda == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Komanda >= 89 && Komanda <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] secība_Saraksts = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Komanda - 89]; 순번++) Izvade.add("abcd".charAt(순번) + " = POP();");
                for (char VALUE : secība_Saraksts[Komanda - 89].toCharArray()) Izvade.add("PUSH(" + VALUE + ");");
            } else if (Komanda == 96 || Komanda == 100 || Komanda == 104 || Komanda == 126 || Komanda == 128 || Komanda == 130) {
                String operācija_VALUE = Komanda == 96 ? "+" : Komanda == 100 ? "-" : Komanda == 104 ? "*" : Komanda == 126 ? "&" : Komanda == 128 ? "|" : "^";
                Izvade.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operācija_VALUE + " (uint32_t)b);");
            } else if (Komanda == 108 || Komanda == 112) Izvade.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Komanda == 112 ? 1 : 0) + "));");
            else if (Komanda == 116) Izvade.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Komanda == 120 || Komanda == 122 || Komanda == 124) {
                Izvade.add("b = POP(); a = POP();"); Izvade.add("PUSH(" + (Komanda == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Komanda == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Komanda == 132) {
                int INDEX = komanda_dati.한바이트(), palielinājums_summa = komanda_dati.부호한바이트(); čeks_vietējs(INDEX, vietējs_mainīgais_COUNT);
                Izvade.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + palielinājums_summa + ");");
            } else if (Komanda >= 145 && Komanda <= 147) Izvade.add("a = POP(); PUSH((uint32_t)(" + (Komanda == 145 ? "int8_t" : Komanda == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Komanda >= 153 && Komanda <= 158) {
                Izvade.add("a = POP();"); 분기넣기(Izvade, zars_Saraksts, Novietojums, komanda_dati.부호두바이트(), "(int32_t)a " + 비교들[Komanda - 153] + " 0");
            } else if (Komanda >= 159 && Komanda <= 166) {
                Izvade.add("b = POP(); a = POP();"); 분기넣기(Izvade, zars_Saraksts, Novietojums, komanda_dati.부호두바이트(), Komanda >= 165 ? "a " + 비교들[Komanda - 159] + " b" : "(int32_t)a " + 비교들[Komanda - 159] + " (int32_t)b");
            } else if (Komanda == 167 || Komanda == 200) 분기넣기(Izvade, zars_Saraksts, Novietojums, Komanda == 167 ? komanda_dati.부호두바이트() : komanda_dati.네바이트(), null);
            else if (Komanda == 170 || Komanda == 171) {
                while (komanda_dati.Novietojums % 4 != 0) komanda_dati.한바이트();
                int noklusējuma_vērtība = komanda_dati.네바이트(); Izvade.add("a = POP();");
                if (Komanda == 170) {
                    int 아래 = komanda_dati.네바이트(), 위 = komanda_dati.네바이트(); long krājums_COUNT = (long)위 - 아래 + 1;
                    if (krājums_COUNT < 1 || krājums_COUNT > (komanda_dati.dati.length - komanda_dati.Novietojums) / 4) throw new Tulkošana_kļūda("switch klips Kļūda");
                    for (long VALUE = 아래; VALUE <= 위; VALUE++) 분기넣기(Izvade, zars_Saraksts, Novietojums, komanda_dati.네바이트(), "(int32_t)a == (" + VALUE + ")");
                } else {
                    int krājums_COUNT = komanda_dati.네바이트(), priekšējā_dati = 0;
                    if (krājums_COUNT < 0 || krājums_COUNT > (komanda_dati.dati.length - komanda_dati.Novietojums) / 8) throw new Tulkošana_kļūda("switch Izmērs Kļūda");
                    for (int 순번 = 0; 순번 < krājums_COUNT; 순번++) {
                        int VALUE = komanda_dati.네바이트(); if (순번 > 0 && VALUE <= priekšējā_dati) throw new Tulkošana_kļūda("switch secība_VALUE Kļūda"); priekšējā_dati = VALUE;
                        분기넣기(Izvade, zars_Saraksts, Novietojums, komanda_dati.네바이트(), "(int32_t)a == (" + VALUE + ")");
                    }
                }
                분기넣기(Izvade, zars_Saraksts, Novietojums, noklusējuma_vērtība, null);
            } else if (Komanda == 172 || Komanda == 176 || Komanda == 177) Izvade.add("return " + (Komanda == 177 ? "0" : "POP()") + ";");
            else if (Komanda == 178 || Komanda == 179) {
                metode_Uzziņas Uzziņas = klase_VALUE.Uzziņas(komanda_dati.두바이트()); if (!필드들.containsKey(Uzziņas)) throw new Tulkošana_kļūda("알 numurs 없는 lauka_vērtība");
                Izvade.add(simbols("init", Uzziņas.īpašnieks_VALUE) + "();"); String lauka_vērtība = simbols("field", Uzziņas.부분들());
                Izvade.add(Komanda == 178 ? "PUSH(" + lauka_vērtība + ");" : lauka_vērtība + " = POP();");
            } else if (Komanda == 184) {
                metode_Uzziņas Uzziņas = klase_VALUE.Uzziņas(komanda_dati.두바이트()); if (!함수들.containsKey(Uzziņas)) throw new Tulkošana_kļūda("알 numurs 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Uzziņas.서술); int krājums_COUNT = 호출형식.Parametri.size();
                Izvade.add(simbols("init", Uzziņas.īpašnieks_VALUE) + "();"); Izvade.add("if(sp < " + krājums_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + krājums_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < krājums_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                Izvade.add("a = " + simbols("method", Uzziņas.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.atdot_mērs.equals("V")) Izvade.add("PUSH(a);");
            } else if (Komanda == 182) {
                metode_Uzziņas Uzziņas = klase_VALUE.Uzziņas(komanda_dati.두바이트());
                if (Uzziņas.equals(new metode_Uzziņas("java/lang/String", "length", "()I"))) Izvade.add("a = POP(); PUSH(length(a));");
                else if (Uzziņas.equals(new metode_Uzziņas("java/lang/String", "charAt", "(I)C"))) Izvade.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Tulkošana_kļūda("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Komanda == 188) {
                if (komanda_dati.한바이트() != 10) throw new Tulkošana_kļūda("new int[]만 Atbalsts_VALUE"); Izvade.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Komanda == 190) Izvade.add("a = POP(); PUSH(length(a));");
            else if (Komanda == 196) {
                int paplašinājums_VALUE = komanda_dati.한바이트(), INDEX = komanda_dati.두바이트(); čeks_vietējs(INDEX, vietējs_mainīgais_COUNT);
                if (paplašinājums_VALUE == 21 || paplašinājums_VALUE == 25) Izvade.add("PUSH(l[" + INDEX + "]);");
                else if (paplašinājums_VALUE == 54 || paplašinājums_VALUE == 58) Izvade.add("l[" + INDEX + "] = POP();");
                else if (paplašinājums_VALUE == 132) Izvade.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + komanda_dati.부호두바이트() + ");");
                else throw new Tulkošana_kļūda("미지원 wide Komanda");
            } else if (Komanda == 198 || Komanda == 199) {
                Izvade.add("a = POP();"); 분기넣기(Izvade, zars_Saraksts, Novietojums, komanda_dati.부호두바이트(), "a " + (Komanda == 198 ? "==" : "!=") + " 0");
            } else throw new Tulkošana_kļūda(FUNCTION_VALUE.īpašnieks_VALUE + "." + FUNCTION_VALUE.Nosaukums + ", byte_VALUE " + Novietojums + ": 미지원 Komanda " + Komanda);
        }
        if (!경계들.containsAll(zars_Saraksts)) throw new Tulkošana_kļūda("Komanda 경계가 아닌 곳으로 zars");
        Izvade.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Izvade);
    }
    String eksportēt_metode(String Saite_simbols, String mērķis, boolean 진입점여부) {
        int pozīcijas_indekss = mērķis.lastIndexOf('.'); if (pozīcijas_indekss < 0 || !Saite_simbols.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tulkošana_kļūda("내보내기 nodot_VALUE Kļūda");
        String īpašnieks_VALUE = mērķis.substring(0, pozīcijas_indekss).replace('.', '/'), Nosaukums = mērķis.substring(pozīcijas_indekss + 1); metode_Uzziņas atlase_VALUE = null;
        for (metode_Uzziņas Uzziņas : 함수들.keySet()) if (Uzziņas.īpašnieks_VALUE.equals(īpašnieks_VALUE) && Uzziņas.Nosaukums.equals(Nosaukums)) {
            if (atlase_VALUE != null) throw new Tulkošana_kļūda("겹친 내보내기 mērķis"); atlase_VALUE = Uzziņas;
        }
        if (atlase_VALUE == null || (함수들.get(atlase_VALUE).piekļūt_ievade & 0x100) != 0) throw new Tulkošana_kļūda("내보낼 함수가 없음 또는 native FUNCTION_VALUE");
        함수형식 formāts_VALUE = new 함수형식(atlase_VALUE.서술);
        if ((진입점여부 && !formāts_VALUE.Parametri.isEmpty()) || !Arrays.asList("V", "I").contains(formāts_VALUE.atdot_mērs)) throw new Tulkošana_kļūda("ieejas_punkts_VALUE 또는 C 경계 formāts_VALUE Kļūda");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formāts_VALUE.Parametri.size(); 순번++) {
            if (!formāts_VALUE.Parametri.get(순번).equals("I")) throw new Tulkošana_kļūda("C 경계는 int 인수만 Atbalsts_VALUE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formāts_VALUE.atdot_mērs.equals("V") ? "void " : "int32_t ") + Saite_simbols + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbols("init", atlase_VALUE.īpašnieks_VALUE) + "(); " + (formāts_VALUE.atdot_mērs.equals("V") ? "" : "return (int32_t)") + simbols("method", atlase_VALUE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String ģenerēt(String ieejas_punkts, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metode_Uzziņas, elements_dati> ievade_VALUE : 함수들.entrySet()) {
            metode_Uzziņas Uzziņas = ievade_VALUE.getKey(); elements_dati dati = ievade_VALUE.getValue(); 선언들.add(함수원형(Uzziņas) + ";");
            if ((dati.piekļūt_ievade & 0x100) != 0) {
                String Savienoties = mašīna_Azure_funkcijas_c3a8e64a.get(Uzziņas.Nosaukums + Uzziņas.서술);
                if (!Uzziņas.īpašnieks_VALUE.equals(mašīna_klase) || Savienoties == null) throw new Tulkošana_kļūda("허용되지 않은 native FUNCTION_VALUE: " + Uzziņas.Nosaukums);
                int krājums_COUNT = new 함수형식(Uzziņas.서술).Parametri.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < krājums_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Savienoties + "(" + (krājums_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(krājums_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Uzziņas) + " { return " + Savienoties + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(metode_pamatteksts(Uzziņas, dati));
        }
        for (Map.Entry<metode_Uzziņas, elements_dati> ievade_VALUE : 필드들.entrySet()) {
            metode_Uzziņas Uzziņas = ievade_VALUE.getKey(); byte[] konstante_VALUE = ievade_VALUE.getValue().atribūts_VALUE.get("ConstantValue");
            String VALUE = konstante_VALUE == null ? "0" : konstante_izteiksme(클래스들.get(Uzziņas.īpašnieks_VALUE), new dati_Lasītājs(konstante_VALUE).두바이트());
            필드선언들.add("static word " + simbols("field", Uzziņas.부분들()) + " = " + VALUE + ";");
        }
        for (String Nosaukums : 클래스들.keySet()) {
            String 초기화 = simbols("init", Nosaukums), Statuss_VALUE = simbols("state", Nosaukums);
            선언들.add("static void " + 초기화 + "(void);"); 필드선언들.add("static unsigned " + Statuss_VALUE + ";");
            metode_Uzziņas Uzziņas = new metode_Uzziņas(Nosaukums, "<clinit>", "()V");
            몸체들.add("static void " + 초기화 + "(void) { if(" + Statuss_VALUE + ") return; " + Statuss_VALUE + " = 1; " + (함수들.containsKey(Uzziņas) ? simbols("method", Uzziņas.부분들()) + "(); " : "") + Statuss_VALUE + " = 2; }");
        }
        몸체들.add(eksportēt_metode("java_entry", ieejas_punkts, true)); Set<String> 공개이름 = new HashSet<>();
        for (String nodot_VALUE : 내보내기목록) {
            int pozīcijas_indekss = nodot_VALUE.indexOf('='); if (pozīcijas_indekss < 1) throw new Tulkošana_kļūda("내보내기 nodot_VALUE Kļūda");
            String Nosaukums = nodot_VALUE.substring(0, pozīcijas_indekss); 공개이름.add(Nosaukums); 몸체들.add(eksportēt_metode(Nosaukums, nodot_VALUE.substring(pozīcijas_indekss + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> ievade_VALUE : 문자열들.entrySet()) {
            String Teksts = ievade_VALUE.getKey(); StringBuilder ARRAY_VALUE = new StringBuilder("static const word " + ievade_VALUE.getValue() + "[] = {" + Teksts.length());
            for (int 순번 = 0; 순번 < Teksts.length(); 순번++) ARRAY_VALUE.append(", ").append((int)Teksts.charAt(순번));
            문자열선언들.add(ARRAY_VALUE.append("};").toString());
        }
        String Atbalsts_VALUE = Files.readString(resurss_ceļš.resolve("CLR_Atbalsts.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(kaudze_Word_COUNT));
        return 기계원문한국어화(Atbalsts_VALUE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String AVOTS, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nosaukums_tabula = new HashMap<>();
        for (String Līniju : Files.readAllLines(resurss_ceļš.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] savienot_pārī_VALUE = Līniju.split("\t"); nosaukums_tabula.put(savienot_pārī_VALUE[0], savienot_pārī_VALUE[1]);
        }
        Pattern porcija_izteiksme = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = porcija_izteiksme.matcher(AVOTS); StringBuffer mērs = new StringBuffer();
        while (찾개.find()) {
            String Nosaukums = 찾개.group(), 새이름 = Nosaukums;
            if (!Nosaukums.startsWith("//") && !Nosaukums.startsWith("/*") && !Nosaukums.startsWith("\"") && !Nosaukums.startsWith("'") && !공개이름.contains(Nosaukums)) {
                새이름 = nosaukums_tabula.getOrDefault(Nosaukums, Nosaukums);
                if (Nosaukums.matches("a[0-9]+")) 새이름 = "Parametri" + Nosaukums.substring(1);
                if (Nosaukums.matches("b[0-9]+")) 새이름 = "zars" + Nosaukums.substring(1);
                if (범용표기) {
                    StringBuilder notācija_VALUE = new StringBuilder();
                    for (char rakstzīme_VALUE : 새이름.toCharArray()) notācija_VALUE.append(rakstzīme_VALUE < 128 ? Character.toString(rakstzīme_VALUE) : String.format(Locale.ROOT, "\\u%04x", (int)rakstzīme_VALUE));
                    새이름 = notācija_VALUE.toString();
                }
            }
            찾개.appendReplacement(mērs, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(mērs); return mērs.toString();
    }
    String X_86_metode_pamatteksts(metode_Uzziņas FUNCTION_VALUE, elements_dati dati, Map<String,String> mašīna_tabula, String mērķis) {
        String marķieris_VALUE = simbols("method", FUNCTION_VALUE.부분들());
        List<String> Līniju = new ArrayList<>();
        if ((dati.piekļūt_ievade & 0x100) != 0) {
            String Savienoties = mašīna_tabula.get(FUNCTION_VALUE.Nosaukums + FUNCTION_VALUE.서술);
            if (!FUNCTION_VALUE.īpašnieks_VALUE.equals(mērķis.equals("kernel") ? "ierīce_VALUE" : "lietotājs") || Savienoties == null) throw new Tulkošana_kļūda("허용되지 않은 native FUNCTION_VALUE");
            return ".text\n" + marķieris_VALUE + ":\njmp " + Savienoties;
        }
        byte[] pamatteksts = dati.atribūts_VALUE.get("Code"); if (pamatteksts == null) throw new Tulkošana_kļūda("FUNCTION_VALUE 몸체가 없음");
        dati_Lasītājs Lasītājs_VALUE = new dati_Lasītājs(pamatteksts); Lasītājs_VALUE.두바이트(); int vietējs_COUNT = Lasītājs_VALUE.두바이트();
        dati_Lasītājs komanda_dati = new dati_Lasītājs(Lasītājs_VALUE.Lasīt(Lasītājs_VALUE.네바이트()));
        if (Lasītājs_VALUE.두바이트() != 0) throw new Tulkošana_kļūda("try/catch/finally 미지원");
        함수형식 formāts_VALUE = new 함수형식(FUNCTION_VALUE.서술); if (vietējs_COUNT < formāts_VALUE.Parametri.size()) throw new Tulkošana_kļūda("매개변수보다 적은 vietējs_Tvērums mainīgais_VALUE");
        Collections.addAll(Līniju,".text",".globl " + marķieris_VALUE,".type " + marķieris_VALUE + ", @function",marķieris_VALUE + ":","pushl %ebp","movl %esp, %ebp","subl $" + vietējs_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formāts_VALUE.Parametri.size(); 순번++) Collections.addAll(Līniju,"movl " + (8 + 4 * (formāts_VALUE.Parametri.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        klase_dati klase_VALUE = 클래스들.get(FUNCTION_VALUE.īpašnieks_VALUE); Set<Integer> 경계들 = new HashSet<>(), zars_Saraksts = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (komanda_dati.Novietojums < komanda_dati.dati.length) {
            int Novietojums = komanda_dati.Novietojums, Komanda = komanda_dati.한바이트(); String pozīcijas_indekss = marķieris_VALUE + "_b" + Novietojums;
            Līniju.add(pozīcijas_indekss + ":"); 경계들.add(Novietojums);
            if (Komanda == 0) Līniju.add("nop");
            else if (Komanda == 1) Līniju.add("pushl $0");
            else if (Komanda >= 2 && Komanda <= 8) Līniju.add("pushl $" + (Komanda - 3));
            else if (Komanda == 16 || Komanda == 17) Līniju.add("pushl $" + (Komanda == 16 ? komanda_dati.부호한바이트() : komanda_dati.부호두바이트()));
            else if (Komanda == 18 || Komanda == 19) {
                int INDEX = Komanda == 18 ? komanda_dati.한바이트() : komanda_dati.두바이트();
                Līniju.add("pushl $" + X_86_konstante(klase_VALUE,INDEX));
            } else if (Komanda == 21 || Komanda == 25 || (Komanda >= 26 && Komanda <= 29) || (Komanda >= 42 && Komanda <= 45) || Komanda == 54 || Komanda == 58 || (Komanda >= 59 && Komanda <= 62) || (Komanda >= 75 && Komanda <= 78)) {
                boolean 읽음 = Komanda < 54; int INDEX = Komanda == 21 || Komanda == 25 || Komanda == 54 || Komanda == 58 ? komanda_dati.한바이트() : Komanda - (Komanda <= 29 ? 26 : Komanda <= 45 ? 42 : Komanda <= 62 ? 59 : 75);
                čeks_vietējs(INDEX,vietējs_COUNT); Līniju.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Komanda == 46) Collections.addAll(Līniju,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Komanda == 79) Collections.addAll(Līniju,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Komanda == 87 || Komanda == 88) Līniju.add("addl $" + (Komanda == 87 ? 4 : 8) + ", %esp");
            else if (Komanda >= 89 && Komanda <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] secība_Saraksts = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Komanda - 89]; 순번++) Līniju.add("popl " + 저장기들[순번]);
                for (int 순번 : secība_Saraksts[Komanda - 89]) Līniju.add("pushl " + 저장기들[순번]);
            } else if (Komanda == 96 || Komanda == 100 || Komanda == 104 || Komanda == 126 || Komanda == 128 || Komanda == 130) {
                String operācija_VALUE = Komanda == 96 ? "addl" : Komanda == 100 ? "subl" : Komanda == 104 ? "imull" : Komanda == 126 ? "andl" : Komanda == 128 ? "orl" : "xorl";
                Collections.addAll(Līniju,"popl %ecx","popl %eax",operācija_VALUE + " %ecx, %eax","pushl %eax");
            } else if (Komanda == 108 || Komanda == 112) Collections.addAll(Līniju,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + pozīcijas_indekss + "_divide","cmpl $0x80000000, %eax","jne " + pozīcijas_indekss + "_divide","xorl %edx, %edx","jmp " + pozīcijas_indekss + "_done",pozīcijas_indekss + "_divide:","cltd","idivl %ecx",pozīcijas_indekss + "_done:","pushl " + (Komanda == 108 ? "%eax" : "%edx"));
            else if (Komanda == 116) Līniju.add("negl (%esp)");
            else if (Komanda == 120 || Komanda == 122 || Komanda == 124) Collections.addAll(Līniju,"popl %ecx","popl %eax",(Komanda == 120 ? "sall" : Komanda == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Komanda == 132) {
                int INDEX = komanda_dati.한바이트(), palielinājums_VALUE = komanda_dati.부호한바이트(); čeks_vietējs(INDEX,vietējs_COUNT); Līniju.add("addl $" + palielinājums_VALUE + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (Komanda >= 145 && Komanda <= 147) Collections.addAll(Līniju,"popl %eax",Komanda == 145 ? "movsbl %al, %eax" : Komanda == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Komanda >= 153 && Komanda <= 166) {
                if (Komanda <= 158) Collections.addAll(Līniju,"popl %eax","testl %eax, %eax");
                else Collections.addAll(Līniju,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int mērķis_VALUE = Novietojums + komanda_dati.부호두바이트(); zars_Saraksts.add(mērķis_VALUE); Līniju.add(비교들[Komanda - (Komanda <= 158 ? 153 : 159)] + " " + marķieris_VALUE + "_b" + mērķis_VALUE);
            } else if (Komanda == 167 || Komanda == 200) {
                int mērķis_VALUE = Novietojums + (Komanda == 167 ? komanda_dati.부호두바이트() : komanda_dati.네바이트()); zars_Saraksts.add(mērķis_VALUE); Līniju.add("jmp " + marķieris_VALUE + "_b" + mērķis_VALUE);
            } else if (Komanda == 170 || Komanda == 171) {
                while (komanda_dati.Novietojums % 4 != 0) komanda_dati.한바이트();
                int noklusējuma_vērtība = Novietojums + komanda_dati.네바이트(); zars_Saraksts.add(noklusējuma_vērtība); Līniju.add("popl %eax");
                int krājums_COUNT, 아래 = 0;
                if (Komanda == 170) { 아래 = komanda_dati.네바이트(); int 위 = komanda_dati.네바이트(); long 길이 = (long)위 - 아래 + 1; if (길이 < 1 || 길이 > (komanda_dati.dati.length - komanda_dati.Novietojums) / 4) throw new Tulkošana_kļūda("switch klips Kļūda"); krājums_COUNT = (int)길이; }
                else { krājums_COUNT = komanda_dati.네바이트(); if (krājums_COUNT < 0 || krājums_COUNT > (komanda_dati.dati.length - komanda_dati.Novietojums) / 8) throw new Tulkošana_kļūda("switch Izmērs Kļūda"); }
                for (int 순번 = 0; 순번 < krājums_COUNT; 순번++) {
                    int VALUE = Komanda == 170 ? 아래 + 순번 : komanda_dati.네바이트(), mērķis_VALUE = Novietojums + komanda_dati.네바이트(); zars_Saraksts.add(mērķis_VALUE);
                    Collections.addAll(Līniju,"cmpl $" + VALUE + ", %eax","je " + marķieris_VALUE + "_b" + mērķis_VALUE);
                }
                Līniju.add("jmp " + marķieris_VALUE + "_b" + noklusējuma_vērtība);
            } else if (Komanda == 172 || Komanda == 176 || Komanda == 177) {
                if (Komanda != 177) Līniju.add("popl %eax"); Collections.addAll(Līniju,"leave","ret");
            } else if (Komanda == 178 || Komanda == 179) {
                metode_Uzziņas Uzziņas = klase_VALUE.Uzziņas(komanda_dati.두바이트()); if (!필드들.containsKey(Uzziņas)) throw new Tulkošana_kļūda("알 numurs 없는 lauka_vērtība");
                Collections.addAll(Līniju,"call " + simbols("init",Uzziņas.īpašnieks_VALUE),(Komanda == 178 ? "pushl " : "popl ") + simbols("field",Uzziņas.부분들()));
            } else if (Komanda == 184) {
                metode_Uzziņas Uzziņas = klase_VALUE.Uzziņas(komanda_dati.두바이트()); if (!함수들.containsKey(Uzziņas)) throw new Tulkošana_kļūda("알 numurs 없는 FUNCTION_VALUE");
                함수형식 호출형식 = new 함수형식(Uzziņas.서술); Collections.addAll(Līniju,"call " + simbols("init",Uzziņas.īpašnieks_VALUE),"call " + simbols("method",Uzziņas.부분들()));
                if (!호출형식.Parametri.isEmpty()) Līniju.add("addl $" + 호출형식.Parametri.size() * 4 + ", %esp");
                if (!호출형식.atdot_mērs.equals("V")) Līniju.add("pushl %eax");
            } else if (Komanda == 182) {
                metode_Uzziņas Uzziņas = klase_VALUE.Uzziņas(komanda_dati.두바이트());
                if (Uzziņas.equals(new metode_Uzziņas("java/lang/String","length","()I"))) Collections.addAll(Līniju,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Uzziņas.equals(new metode_Uzziņas("java/lang/String","charAt","(I)C"))) Collections.addAll(Līniju,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Tulkošana_kļūda("가상 FUNCTION_VALUE 호출 미지원");
            } else if (Komanda == 188) {
                if (komanda_dati.한바이트() != 10) throw new Tulkošana_kļūda("new int[]만 Atbalsts_VALUE"); Collections.addAll(Līniju,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Komanda == 190) Collections.addAll(Līniju,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Komanda == 196) {
                int paplašinājums_VALUE = komanda_dati.한바이트(), INDEX = komanda_dati.두바이트(); čeks_vietējs(INDEX,vietējs_COUNT);
                if (paplašinājums_VALUE == 21 || paplašinājums_VALUE == 25 || paplašinājums_VALUE == 54 || paplašinājums_VALUE == 58) Līniju.add((paplašinājums_VALUE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (paplašinājums_VALUE == 132) Līniju.add("addl $" + komanda_dati.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Tulkošana_kļūda("wide Komanda 미지원");
            } else if (Komanda == 198 || Komanda == 199) {
                int mērķis_VALUE = Novietojums + komanda_dati.부호두바이트(); zars_Saraksts.add(mērķis_VALUE); Collections.addAll(Līniju,"popl %eax","testl %eax, %eax",(Komanda == 198 ? "je " : "jne ") + marķieris_VALUE + "_b" + mērķis_VALUE);
            } else throw new Tulkošana_kļūda("미지원 Komanda: " + Komanda);
        }
        if (!경계들.containsAll(zars_Saraksts)) throw new Tulkošana_kļūda("Komanda 경계가 아닌 곳으로 zars");
        Līniju.add(".size " + marķieris_VALUE + ", .-" + marķieris_VALUE); return String.join("\n",Līniju);
    }
    String X_86_konstante(klase_dati dati, int INDEX) {
        if (dati.상수종류[INDEX] == 3) return dati.konstante_dati[INDEX].toString();
        if (dati.상수종류[INDEX] == 8) return virkne_simbols(dati.문자((Integer)dati.konstante_dati[INDEX]));
        throw new Tulkošana_kļūda("정수와 virkne_VALUE 상수만 Atbalsts_VALUE");
    }
    String X_86_montāža(String ieejas_punkts, List<String> 내보냄, String mērķis) throws IOException {
        Map<String,String> mašīna_tabula = new HashMap<>();
        for (String Līniju : Files.readAllLines(resurss_ceļš.resolve("_86_mašīna_Azure_funkcijas.tsv"))) { String[] savienot_pārī_VALUE = Līniju.split("\t"); if (savienot_pārī_VALUE[0].equals(mērķis)) mašīna_tabula.put(savienot_pārī_VALUE[1] + savienot_pārī_VALUE[2],savienot_pārī_VALUE[3]); }
        int pozīcijas_indekss = ieejas_punkts.lastIndexOf('.'); if (pozīcijas_indekss < 0) throw new Tulkošana_kļūda("ieejas_punkts nodot_VALUE Kļūda");
        String īpašnieks_VALUE = ieejas_punkts.substring(0,pozīcijas_indekss).replace('.','/'), metode_ievade_nosaukums = ieejas_punkts.substring(pozīcijas_indekss + 1); metode_Uzziņas ieejas_punkts_VALUE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metode_Uzziņas Uzziņas = new metode_Uzziņas(īpašnieks_VALUE,metode_ievade_nosaukums,서술); if (함수들.containsKey(Uzziņas)) { if (ieejas_punkts_VALUE != null) throw new Tulkošana_kļūda("겹친 ieejas_punkts"); ieejas_punkts_VALUE = Uzziņas; } }
        if (ieejas_punkts_VALUE == null || (함수들.get(ieejas_punkts_VALUE).piekļūt_ievade & 0x100) != 0) throw new Tulkošana_kļūda("ieejas_punkts_VALUE FUNCTION_VALUE formāts_VALUE Kļūda");
        List<String> Līniju = new ArrayList<>(); Līniju.add(".code32");
        for (klase_dati dati : 클래스들.values()) {
            String Statuss_VALUE = simbols("state",dati.Nosaukums), 초기화 = simbols("init",dati.Nosaukums);
            Collections.addAll(Līniju,".bss",".balign 4",Statuss_VALUE + ": .long 0",".text",초기화 + ":","cmpl $0, " + Statuss_VALUE,"jne " + 초기화 + "_done","movl $1, " + Statuss_VALUE);
            metode_Uzziņas 초기화참조 = new metode_Uzziņas(dati.Nosaukums,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) Līniju.add("call " + simbols("method",초기화참조.부분들()));
            Collections.addAll(Līniju,"movl $2, " + Statuss_VALUE,초기화 + "_done:","ret");
            for (elements_dati lauka_vērtība : dati.lauka_vērtība) {
                byte[] konstante_VALUE = lauka_vērtība.atribūts_VALUE.get("ConstantValue"); String VALUE = konstante_VALUE == null ? "0" : X_86_konstante(dati,new dati_Lasītājs(konstante_VALUE).두바이트());
                Collections.addAll(Līniju,".data",".balign 4",simbols("field",dati.Nosaukums,lauka_vērtība.Nosaukums,lauka_vērtība.서술) + ": .long " + VALUE);
            }
            for (elements_dati FUNCTION_VALUE : dati.FUNCTION_VALUE) if (!FUNCTION_VALUE.Nosaukums.equals("<init>")) Līniju.add(X_86_metode_pamatteksts(new metode_Uzziņas(dati.Nosaukums,FUNCTION_VALUE.Nosaukums,FUNCTION_VALUE.서술),FUNCTION_VALUE,mašīna_tabula,mērķis));
        }
        Collections.addAll(Līniju,".text",".globl java_entry","java_entry:","call " + simbols("init",ieejas_punkts_VALUE.īpašnieks_VALUE),"call " + simbols("method",ieejas_punkts_VALUE.부분들()));
        if (ieejas_punkts_VALUE.서술.equals("()V")) Līniju.add("xorl %eax, %eax"); Līniju.add("ret");
        for (String nodot_VALUE : 내보냄) {
            int norobežotājs_VALUE = nodot_VALUE.indexOf('='); if (norobežotājs_VALUE < 1) throw new Tulkošana_kļūda("내보내기 nodot_VALUE Kļūda");
            String ārējs_VALUE = nodot_VALUE.substring(0,norobežotājs_VALUE), FUNCTION_VALUE = nodot_VALUE.substring(norobežotājs_VALUE + 1); int nodaļa_mērs = FUNCTION_VALUE.lastIndexOf('.');
            if (nodaļa_mērs < 0 || !ārējs_VALUE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Tulkošana_kļūda("내보내기 simbols Kļūda");
            String klase_VALUE = FUNCTION_VALUE.substring(0,nodaļa_mērs).replace('.','/'), Nosaukums = FUNCTION_VALUE.substring(nodaļa_mērs + 1); metode_Uzziņas atlase_VALUE = null;
            for (metode_Uzziņas Uzziņas : 함수들.keySet()) if (Uzziņas.īpašnieks_VALUE.equals(klase_VALUE) && Uzziņas.Nosaukums.equals(Nosaukums)) { if (atlase_VALUE != null) throw new Tulkošana_kļūda("겹친 내보내기 mērķis"); atlase_VALUE = Uzziņas; }
            if (atlase_VALUE == null) throw new Tulkošana_kļūda("내보낼 함수가 없음");
            Collections.addAll(Līniju,".text",".globl " + ārējs_VALUE,ārējs_VALUE + ":","call " + simbols("init",atlase_VALUE.īpašnieks_VALUE),"jmp " + simbols("method",atlase_VALUE.부분들()));
        }
        Līniju.add(".section .rodata");
        for (Map.Entry<String,String> ievade_VALUE : 문자열들.entrySet()) {
            Collections.addAll(Līniju,".balign 4",ievade_VALUE.getValue() + ":",".long " + ievade_VALUE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char vienība_VALUE : ievade_VALUE.getKey().toCharArray()) 단위들.add(Integer.toString(vienība_VALUE)); if (!단위들.isEmpty()) Līniju.add(".long " + String.join(",",단위들));
        }
        Līniju.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",Līniju) + "\n";
    }
    static void Izpildīt_rīks(List<String> Komanda) throws Exception {
        if (new ProcessBuilder(Komanda).inheritIO().start().waitFor() != 0) throw new Tulkošana_kļūda("kompilēt_avots Kļūda: " + Komanda.get(0));
    }
    static String dati_virkne(String Teksts) { return "\"" + Teksts.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Tulkošana(List<Path> 입력들, String mērķis, String ieejas_punkts, List<String> 내보냄, Path Izvade, Path resurss_VALUE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), klase_ceļš = 임시.resolve("classes"); Files.createDirectory(klase_ceļš);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",klase_ceļš.toString(),"-sourcepath",klase_ceļš.toString(),"-d",klase_ceļš.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int avots_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (Izvade.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Tulkošana_kļūda("Izvade 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); avots_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Tulkošana_kļūda(".java 또는 .class만 Atbalsts_VALUE");
            }
            if (avots_COUNT > 0) Izpildīt_rīks(자바명령);
            try (java.util.stream.Stream<Path> ceļš_Saraksts = Files.walk(klase_ceļš)) { ceļš_Saraksts.filter(CEĻŠ -> CEĻŠ.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_VALUE = new 기계어미리번역(바이트코드,mērķis.equals("user") ? "user" : "kernel",262144,resurss_VALUE);
            String 조립 = CONVERT_VALUE.X_86_montāža(ieejas_punkts,내보냄,mērķis); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path rīks_amats = resurss_VALUE.getParent();
            Izpildīt_rīks(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Izpildīt_rīks(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),rīks_amats.resolve("CLR_Atbalsts.s").toString()));
            List<String> Savienoties = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (mērķis.equals("kernel")) Savienoties.add("-r");
            else {
                Izpildīt_rīks(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),rīks_amats.resolve(mērķis.equals("user") ? "Sākt_lietotājs_programma.s" : "리눅스시작.s").toString()));
                Collections.addAll(Savienoties,"-e","_start",임시.resolve("start.o").toString());
                if (mērķis.equals("user")) Collections.addAll(Savienoties,"-T",rīks_amats.resolve("lietotājs_Saite_shēma.ld").toString());
            }
            Collections.addAll(Savienoties,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Izpildīt_rīks(Savienoties);
            Izvade = Izvade.toAbsolutePath(); Files.createDirectories(Izvade.getParent()); Path publicēt_VALUE = Files.createTempFile(Izvade.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),publicēt_VALUE,StandardCopyOption.REPLACE_EXISTING); Files.move(publicēt_VALUE,Izvade,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(publicēt_VALUE); }
            Files.setPosixFilePermissions(Izvade,java.nio.file.attribute.PosixFilePermissions.fromString(mērķis.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Izvade + ".s"),조립,StandardCharsets.UTF_8);
            List<String> simbols_dati = new ArrayList<>(), avots_dati = new ArrayList<>();
            for (metode_Uzziņas Uzziņas : CONVERT_VALUE.함수들.keySet()) simbols_dati.add(dati_virkne(simbols("method",Uzziņas.부분들())) + ":" + dati_virkne(Uzziņas.īpašnieks_VALUE + "." + Uzziņas.Nosaukums + Uzziņas.서술));
            for (Path 입력 : 입력들) {
                byte[] jaukšana_Fails = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Teksts = new StringBuilder(); for (byte VALUE : jaukšana_Fails) Teksts.append(String.format(Locale.ROOT,"%02x",VALUE & 255));
                avots_dati.add(dati_virkne(입력.toAbsolutePath().toString()) + ":" + dati_virkne(Teksts.toString()));
            }
            Files.writeString(Paths.get(Izvade + ".json"),"{\"target\":" + dati_virkne(mērķis) + ",\"entry\":" + dati_virkne(ieejas_punkts) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbols_dati) + "},\"sources\":{" + String.join(",",avots_dati) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> ceļš_Saraksts = Files.walk(임시)) { for (Path CEĻŠ : (Iterable<Path>)ceļš_Saraksts.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(CEĻŠ); }
        }
    }
    public static void main(String[] Parametri) {
        try {
            String ieejas_punkts = null, mērķis = "kernel", X_86_mērķis = null; Path ražojums_ceļš = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> ceļš_Saraksts = new ArrayList<>();
            for (int 순번 = 0; 순번 < Parametri.length; 순번++) {
                String VALUE = Parametri[순번];
                switch (VALUE) {
                    case "--target": X_86_mērķis = Parametri[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry klase_VALUE.FUNCTION_VALUE -o Izvade [--target linux|kernel|user] [--profile kernel|user] [--export simbols=klase_VALUE.FUNCTION_VALUE] 클래스파일 또는 Java원문"); return;
                    case "--entry": ieejas_punkts = Parametri[++순번]; break;
                    case "--profile": mērķis = Parametri[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(Parametri[++순번]); break;
                    case "--export": 내보냄.add(Parametri[++순번]); break;
                    case "-o": ražojums_ceļš = Paths.get(Parametri[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALUE.startsWith("-")) throw new Tulkošana_kļūda("알 numurs 없는 옵션: " + VALUE); ceļš_Saraksts.add(Paths.get(VALUE));
                }
            }
            if (ieejas_punkts == null || ražojums_ceļš == null || ceļš_Saraksts.isEmpty()) throw new Tulkošana_kļūda("--entry, -o, klase_VALUE 파일이 필요합니다");
            Path resurss_VALUE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_mērķis != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_mērķis)) throw new Tulkošana_kļūda("알 numurs 없는 Izpildīt_komanda mērķis");
                X_86_Tulkošana(ceļš_Saraksts,X_86_mērķis,ieejas_punkts,내보냄,ražojums_ceļš,resurss_VALUE); return;
            }
            String AVOTS = new 기계어미리번역(ceļš_Saraksts, mērķis, 낱말수, resurss_VALUE).ģenerēt(ieejas_punkts, 내보냄, 범용표기);
            ražojums_ceļš = ražojums_ceļš.toAbsolutePath(); Files.createDirectories(ražojums_ceļš.getParent());
            Path 임시 = Files.createTempFile(ražojums_ceļš.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, AVOTS, StandardCharsets.UTF_8); Files.move(임시, ražojums_ceļš, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Kļūda) { System.err.println("kompilēt_avots Kļūda: " + Kļūda.getMessage()); System.exit(1); }
    }
}
