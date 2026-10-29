// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java tauaha_uara 파일에서 독립 ARM64 커널용 C 원문을 만든다. taurima JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Whakawhiti_Reo_hapa extends RuntimeException {
        Whakawhiti_Reo_hapa(String 설명) { super(설명); }
    }
    static final class raraunga_Pūpānui {
        final byte[] raraunga;
        int tūranga;
        raraunga_Pūpānui(byte[] 입력자료) { raraunga = 입력자료; }
        byte[] Pānuitia(int roa_uara) {
            if (roa_uara < 0 || roa_uara > raraunga.length - tūranga) throw new Whakawhiti_Reo_hapa("잘린 tauaha_uara 또는 tono raraunga");
            byte[] mēhua = Arrays.copyOfRange(raraunga, tūranga, tūranga + roa_uara); tūranga += roa_uara; return mēhua;
        }
        int 한바이트() { if (tūranga >= raraunga.length) throw new Whakawhiti_Reo_hapa("잘린 tono raraunga"); return raraunga[tūranga++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class mema_raraunga {
        final int uru_tāurunga;
        final String Ingoa, 서술;
        final Map<String, byte[]> huanga_uara;
        mema_raraunga(int uru_uara, String ingoa_uara, String 서술값, Map<String, byte[]> huanga_raraunga) {
            uru_tāurunga = uru_uara; Ingoa = ingoa_uara; 서술 = 서술값; huanga_uara = huanga_raraunga;
        }
    }
    static final class aratuka_Pūranga_kōrero implements Comparable<aratuka_Pūranga_kōrero> {
        final String kaipupuri_uara, Ingoa, 서술;
        aratuka_Pūranga_kōrero(String 소유값, String ingoa_uara, String 서술값) { kaipupuri_uara = 소유값; Ingoa = ingoa_uara; 서술 = 서술값; }
        String[] 부분들() { return new String[]{kaipupuri_uara, Ingoa, 서술}; }
        public int compareTo(aratuka_Pūranga_kōrero hoa_uara) {
            int 비교값 = kaipupuri_uara.compareTo(hoa_uara.kaipupuri_uara);
            if (비교값 == 0) 비교값 = Ingoa.compareTo(hoa_uara.Ingoa);
            return 비교값 == 0 ? 서술.compareTo(hoa_uara.서술) : 비교값;
        }
        public boolean equals(Object hoa_uara) { return hoa_uara instanceof aratuka_Pūranga_kōrero && compareTo((aratuka_Pūranga_kōrero) hoa_uara) == 0; }
        public int hashCode() { return Objects.hash(kaipupuri_uara, Ingoa, 서술); }
    }
    static final class tauaha_raraunga {
        final int[] 상수종류;
        final Object[] taimau_raraunga;
        final String Ingoa;
        final List<mema_raraunga> āpure_uara, TAUMAHI_uara;
        tauaha_raraunga(Path ara) throws IOException {
            raraunga_Pūpānui Pūpānui_uara = new raraunga_Pūpānui(Files.readAllBytes(ara));
            if (Pūpānui_uara.네바이트() != 0xcafebabe) throw new Whakawhiti_Reo_hapa("Java tauaha_uara 표식이 아님");
            Pūpānui_uara.Pānuitia(4);
            int tuemi_COUNT = Pūpānui_uara.두바이트(); 상수종류 = new int[tuemi_COUNT]; taimau_raraunga = new Object[tuemi_COUNT];
            for (int 순번 = 1; 순번 < tuemi_COUNT; 순번++) {
                int 종류 = Pūpānui_uara.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int roa_uara = Pūpānui_uara.두바이트();
                        byte[] pūāhua_pūreirei = Pūpānui_uara.Pānuitia(roa_uara), 길이붙인자료 = new byte[roa_uara + 2];
                        길이붙인자료[0] = (byte)(roa_uara >> 8); 길이붙인자료[1] = (byte)roa_uara;
                        System.arraycopy(pūāhua_pūreirei, 0, 길이붙인자료, 2, roa_uara);
                        taimau_raraunga[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: taimau_raraunga[순번] = Pūpānui_uara.네바이트(); break;
                    case 4: Pūpānui_uara.Pānuitia(4); break;
                    case 5: case 6: Pūpānui_uara.Pānuitia(8); 순번++; break;
                    case 7: case 8: case 16: taimau_raraunga[순번] = Pūpānui_uara.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        taimau_raraunga[순번] = new int[]{Pūpānui_uara.두바이트(), Pūpānui_uara.두바이트()}; break;
                    case 15: taimau_raraunga[순번] = new int[]{Pūpānui_uara.한바이트(), Pūpānui_uara.두바이트()}; break;
                    default: throw new Whakawhiti_Reo_hapa("지원하지 않는 taimau_uara 종류: " + 종류);
                }
            }
            Pūpānui_uara.두바이트(); Ingoa = tauaha_ingoa(Pūpānui_uara.두바이트());
            if (!tauaha_ingoa(Pūpānui_uara.두바이트()).equals("java/lang/Object") || Pūpānui_uara.두바이트() != 0)
                throw new Whakawhiti_Reo_hapa(Ingoa + ": 상속 및 인터페이스 미지원");
            āpure_uara = 멤버읽기(Pūpānui_uara); TAUMAHI_uara = 멤버읽기(Pūpānui_uara); 속성읽기(Pūpānui_uara);
            if (Pūpānui_uara.tūranga != Pūpānui_uara.raraunga.length) throw new Whakawhiti_Reo_hapa("tauaha_uara 뒤에 남은 raraunga");
        }
        String 문자(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 1) throw new Whakawhiti_Reo_hapa("문자 taimau_uara INDEX Pōhēhē");
            return (String) taimau_raraunga[INDEX];
        }
        String tauaha_ingoa(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] != 7) throw new Whakawhiti_Reo_hapa("tauaha_uara Pūranga_kōrero Pōhēhē");
            return 문자((Integer)taimau_raraunga[INDEX]);
        }
        aratuka_Pūranga_kōrero Pūranga_kōrero(int INDEX) {
            if (INDEX < 1 || INDEX >= 상수종류.length || 상수종류[INDEX] < 9 || 상수종류[INDEX] > 11) throw new Whakawhiti_Reo_hapa("멤버 Pūranga_kōrero Pōhēhē");
            int[] takirua_uara = (int[])taimau_raraunga[INDEX], ingoa_takirua = (int[])taimau_raraunga[takirua_uara[1]];
            return new aratuka_Pūranga_kōrero(tauaha_ingoa(takirua_uara[0]), 문자(ingoa_takirua[0]), 문자(ingoa_takirua[1]));
        }
        Map<String, byte[]> 속성읽기(raraunga_Pūpānui Pūpānui_uara) {
            Map<String, byte[]> mēhua = new LinkedHashMap<>();
            int tuemi_COUNT = Pūpānui_uara.두바이트();
            for (int 순번 = 0; 순번 < tuemi_COUNT; 순번++) {
                String huanga_ingoa = 문자(Pūpānui_uara.두바이트()); byte[] uara = Pūpānui_uara.Pānuitia(Pūpānui_uara.네바이트());
                if (mēhua.put(huanga_ingoa, uara) != null) throw new Whakawhiti_Reo_hapa("겹친 huanga_uara: " + huanga_ingoa);
            }
            return mēhua;
        }
        List<mema_raraunga> 멤버읽기(raraunga_Pūpānui Pūpānui_uara) {
            List<mema_raraunga> mēhua = new ArrayList<>(); int tuemi_COUNT = Pūpānui_uara.두바이트();
            for (int 순번 = 0; 순번 < tuemi_COUNT; 순번++) {
                int uru_tāurunga = Pūpānui_uara.두바이트(); String aratuka_tāurunga_ingoa = 문자(Pūpānui_uara.두바이트()), 서술 = 문자(Pūpānui_uara.두바이트());
                mēhua.add(new mema_raraunga(uru_tāurunga, aratuka_tāurunga_ingoa, 서술, 속성읽기(Pūpānui_uara)));
            }
            return mēhua;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Whakawhiti_Reo_hapa("TAUMAHI_uara 서술 Pōhēhē: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Whakawhiti_Reo_hapa("TAUMAHI_uara 서술 Pōhēhē: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Whakawhiti_Reo_hapa("TAUMAHI_uara 서술 Pōhēhē: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> mēhua = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int tūranga = 0; tūranga < 서술.length();) {
            String tīpakonga_uara = null;
            for (String hōputu_uara : 허용형식) if (서술.startsWith(hōputu_uara, tūranga)) { tīpakonga_uara = hōputu_uara; break; }
            if (tīpakonga_uara == null) throw new Whakawhiti_Reo_hapa("지원하지 않는 momo_raraunga: " + 서술);
            mēhua.add(tīpakonga_uara); tūranga += tīpakonga_uara.length();
        }
        return mēhua;
    }
    static String tohu(String 종류, String... 부분들) {
        try {
            byte[] hash_kōnae = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Ngā_kupu = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Ngā_kupu.append(String.format(Locale.ROOT, "%02x", hash_kōnae[순번] & 255));
            return Ngā_kupu.toString();
        } catch (Exception Pōhēhē) { throw new Whakawhiti_Reo_hapa(Pōhēhē.toString()); }
    }
    final Map<String, tauaha_raraunga> 클래스들 = new TreeMap<>();
    final Map<aratuka_Pūranga_kōrero, mema_raraunga> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, mīhini_tauaha;
    final int 동적기억낱말수;
    final Path rauemi_ara;
    기계어미리번역(List<Path> ara_Rārangi, String ūnga, int 낱말수, Path rauemi_uara) throws IOException {
        if ((!ūnga.equals("kernel") && !ūnga.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Whakawhiti_Reo_hapa("kawe_tono ūnga 또는 Pūmahara_uara 공간 rahi Pōhēhē");
        실행대상 = ūnga; 동적기억낱말수 = 낱말수; rauemi_ara = rauemi_uara;
        // 이 이름도 국가별 pūtake_rākau waihanga 시 해당 언어로 옮긴다.
        mīhini_tauaha = ūnga.equals("kernel") ? "papa" : "kaiwhakamahi";
        for (String hononga : Files.readAllLines(rauemi_uara.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = hononga.split("\t", -1);
            if (부분들.length != 4) throw new Whakawhiti_Reo_hapa("mīhini TAUMAHI_uara raraunga Pōhēhē");
            if (부분들[0].equals(ūnga)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path ara : ara_Rārangi) {
            tauaha_raraunga raraunga = new tauaha_raraunga(ara);
            if (클래스들.put(raraunga.Ingoa, raraunga) != null) throw new Whakawhiti_Reo_hapa("중복 tauaha_uara: " + raraunga.Ingoa);
            for (mema_raraunga āpure_uara : raraunga.āpure_uara) {
                if ((āpure_uara.uru_tāurunga & 8) == 0 || 형식읽기(āpure_uara.서술).equals(Collections.singletonList("V"))) throw new Whakawhiti_Reo_hapa("pateko_uara 필드만 Tautoko_uara");
                if (필드들.put(new aratuka_Pūranga_kōrero(raraunga.Ingoa, āpure_uara.Ingoa, āpure_uara.서술), āpure_uara) != null) throw new Whakawhiti_Reo_hapa("중복 āpure_uara");
            }
            for (mema_raraunga TAUMAHI_uara : raraunga.TAUMAHI_uara) {
                if (TAUMAHI_uara.Ingoa.equals("<init>")) continue;
                if ((TAUMAHI_uara.uru_tāurunga & 8) == 0 || (TAUMAHI_uara.uru_tāurunga & (0x20 | 0x400)) != 0) throw new Whakawhiti_Reo_hapa("pateko_uara 비동기화 함수만 Tautoko_uara");
                new 함수형식(TAUMAHI_uara.서술);
                if (함수들.put(new aratuka_Pūranga_kōrero(raraunga.Ingoa, TAUMAHI_uara.Ingoa, TAUMAHI_uara.서술), TAUMAHI_uara) != null) throw new Whakawhiti_Reo_hapa("중복 TAUMAHI_uara");
            }
        }
    }
    String aho_tohu(String Ngā_kupu) { return 문자열들.computeIfAbsent(Ngā_kupu, uara -> "j_text_" + 문자열들.size()); }
    String taimau_kīanga(tauaha_raraunga raraunga, int INDEX) {
        if (INDEX < 1 || INDEX >= raraunga.상수종류.length) throw new Whakawhiti_Reo_hapa("taimau_uara INDEX topenga Pōhēhē");
        if (raraunga.상수종류[INDEX] == 3) return "(word)(uint32_t)(" + raraunga.taimau_raraunga[INDEX] + ")";
        if (raraunga.상수종류[INDEX] == 8) return "(word)" + aho_tohu(raraunga.문자((Integer)raraunga.taimau_raraunga[INDEX]));
        throw new Whakawhiti_Reo_hapa("정수와 aho_uara 상수만 Tautoko_uara");
    }
    String 함수원형(aratuka_Pūranga_kōrero Pūranga_kōrero) {
        List<String> 인수들 = new ArrayList<>(); int tuemi_COUNT = new 함수형식(Pūranga_kōrero.서술).인수.size();
        for (int 순번 = 0; 순번 < tuemi_COUNT; 순번++) 인수들.add("word a" + 순번);
        return "static word " + tohu("method", Pūranga_kōrero.부분들()) + "(" + (tuemi_COUNT == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void taki_paetata(int INDEX, int 지역변수수) { if (INDEX < 0 || INDEX >= 지역변수수) throw new Whakawhiti_Reo_hapa("paetata_whānuitanga 변수 INDEX topenga Pōhēhē"); }
    void 분기넣기(List<String> 출력, Set<Integer> peka_Rārangi, int tūranga, int 이동량, String here) {
        int ūnga_uara = tūranga + 이동량; peka_Rārangi.add(ūnga_uara);
        출력.add((here == null ? "" : "if (" + here + ") ") + "goto b" + ūnga_uara + ";");
    }
    String 함수본문(aratuka_Pūranga_kōrero TAUMAHI_uara, mema_raraunga raraunga) {
        byte[] 본문자료 = raraunga.huanga_uara.get("Code"); if (본문자료 == null) throw new Whakawhiti_Reo_hapa("TAUMAHI_uara 몸체가 없음: " + TAUMAHI_uara.Ingoa);
        raraunga_Pūpānui Pūpānui_uara = new raraunga_Pūpānui(본문자료); int 쌓임깊이 = Pūpānui_uara.두바이트(), 지역변수수 = Pūpānui_uara.두바이트();
        raraunga_Pūpānui tono_raraunga = new raraunga_Pūpānui(Pūpānui_uara.Pānuitia(Pūpānui_uara.네바이트()));
        if (Pūpānui_uara.두바이트() != 0) throw new Whakawhiti_Reo_hapa("try/catch/finally 미지원");
        함수형식 hōputu_uara = new 함수형식(TAUMAHI_uara.서술); if (지역변수수 < hōputu_uara.인수.size()) throw new Whakawhiti_Reo_hapa("매개변수보다 적은 paetata_whānuitanga 변수");
        tauaha_raraunga tauaha_uara = 클래스들.get(TAUMAHI_uara.kaipupuri_uara);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(TAUMAHI_uara) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < hōputu_uara.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), peka_Rārangi = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (tono_raraunga.tūranga < tono_raraunga.raraunga.length) {
            int tūranga = tono_raraunga.tūranga, tono = tono_raraunga.한바이트(); 경계들.add(tūranga); 출력.add("b" + tūranga + ":;");
            if (tono == 0) continue;
            if (tono == 1) 출력.add("PUSH(0);");
            else if (tono >= 2 && tono <= 8) 출력.add("PUSH((uint32_t)(" + (tono - 3) + "));");
            else if (tono == 16 || tono == 17) 출력.add("PUSH((uint32_t)(" + (tono == 16 ? tono_raraunga.부호한바이트() : tono_raraunga.부호두바이트()) + "));");
            else if (tono == 18 || tono == 19) 출력.add("PUSH(" + taimau_kīanga(tauaha_uara, tono == 18 ? tono_raraunga.한바이트() : tono_raraunga.두바이트()) + ");");
            else if (tono == 21 || tono == 25 || (tono >= 26 && tono <= 29) || (tono >= 42 && tono <= 45)) {
                int INDEX = tono == 21 || tono == 25 ? tono_raraunga.한바이트() : tono - (tono <= 29 ? 26 : 42);
                taki_paetata(INDEX, 지역변수수); 출력.add("PUSH(l[" + INDEX + "]);");
            } else if (tono == 54 || tono == 58 || (tono >= 59 && tono <= 62) || (tono >= 75 && tono <= 78)) {
                int INDEX = tono == 54 || tono == 58 ? tono_raraunga.한바이트() : tono - (tono <= 62 ? 59 : 75);
                taki_paetata(INDEX, 지역변수수); 출력.add("l[" + INDEX + "] = POP();");
            } else if (tono == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (tono == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (tono == 87 || tono == 88) 출력.add(tono == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (tono >= 89 && tono <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] whakaraupapa_Rārangi = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[tono - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char uara : whakaraupapa_Rārangi[tono - 89].toCharArray()) 출력.add("PUSH(" + uara + ");");
            } else if (tono == 96 || tono == 100 || tono == 104 || tono == 126 || tono == 128 || tono == 130) {
                String mahi_uara = tono == 96 ? "+" : tono == 100 ? "-" : tono == 104 ? "*" : tono == 126 ? "&" : tono == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + mahi_uara + " (uint32_t)b);");
            } else if (tono == 108 || tono == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (tono == 112 ? 1 : 0) + "));");
            else if (tono == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (tono == 120 || tono == 122 || tono == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (tono == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (tono == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (tono == 132) {
                int INDEX = tono_raraunga.한바이트(), 증가량 = tono_raraunga.부호한바이트(); taki_paetata(INDEX, 지역변수수);
                출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + 증가량 + ");");
            } else if (tono >= 145 && tono <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (tono == 145 ? "int8_t" : tono == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (tono >= 153 && tono <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, peka_Rārangi, tūranga, tono_raraunga.부호두바이트(), "(int32_t)a " + 비교들[tono - 153] + " 0");
            } else if (tono >= 159 && tono <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, peka_Rārangi, tūranga, tono_raraunga.부호두바이트(), tono >= 165 ? "a " + 비교들[tono - 159] + " b" : "(int32_t)a " + 비교들[tono - 159] + " (int32_t)b");
            } else if (tono == 167 || tono == 200) 분기넣기(출력, peka_Rārangi, tūranga, tono == 167 ? tono_raraunga.부호두바이트() : tono_raraunga.네바이트(), null);
            else if (tono == 170 || tono == 171) {
                while (tono_raraunga.tūranga % 4 != 0) tono_raraunga.한바이트();
                int uara_taunoa = tono_raraunga.네바이트(); 출력.add("a = POP();");
                if (tono == 170) {
                    int 아래 = tono_raraunga.네바이트(), 위 = tono_raraunga.네바이트(); long tuemi_COUNT = (long)위 - 아래 + 1;
                    if (tuemi_COUNT < 1 || tuemi_COUNT > (tono_raraunga.raraunga.length - tono_raraunga.tūranga) / 4) throw new Whakawhiti_Reo_hapa("switch topenga Pōhēhē");
                    for (long uara = 아래; uara <= 위; uara++) 분기넣기(출력, peka_Rārangi, tūranga, tono_raraunga.네바이트(), "(int32_t)a == (" + uara + ")");
                } else {
                    int tuemi_COUNT = tono_raraunga.네바이트(), 앞값 = 0;
                    if (tuemi_COUNT < 0 || tuemi_COUNT > (tono_raraunga.raraunga.length - tono_raraunga.tūranga) / 8) throw new Whakawhiti_Reo_hapa("switch rahi Pōhēhē");
                    for (int 순번 = 0; 순번 < tuemi_COUNT; 순번++) {
                        int uara = tono_raraunga.네바이트(); if (순번 > 0 && uara <= 앞값) throw new Whakawhiti_Reo_hapa("switch whakaraupapa_uara Pōhēhē"); 앞값 = uara;
                        분기넣기(출력, peka_Rārangi, tūranga, tono_raraunga.네바이트(), "(int32_t)a == (" + uara + ")");
                    }
                }
                분기넣기(출력, peka_Rārangi, tūranga, uara_taunoa, null);
            } else if (tono == 172 || tono == 176 || tono == 177) 출력.add("return " + (tono == 177 ? "0" : "POP()") + ";");
            else if (tono == 178 || tono == 179) {
                aratuka_Pūranga_kōrero Pūranga_kōrero = tauaha_uara.Pūranga_kōrero(tono_raraunga.두바이트()); if (!필드들.containsKey(Pūranga_kōrero)) throw new Whakawhiti_Reo_hapa("알 수 없는 āpure_uara");
                출력.add(tohu("init", Pūranga_kōrero.kaipupuri_uara) + "();"); String āpure_uara = tohu("field", Pūranga_kōrero.부분들());
                출력.add(tono == 178 ? "PUSH(" + āpure_uara + ");" : āpure_uara + " = POP();");
            } else if (tono == 184) {
                aratuka_Pūranga_kōrero Pūranga_kōrero = tauaha_uara.Pūranga_kōrero(tono_raraunga.두바이트()); if (!함수들.containsKey(Pūranga_kōrero)) throw new Whakawhiti_Reo_hapa("알 수 없는 TAUMAHI_uara");
                함수형식 호출형식 = new 함수형식(Pūranga_kōrero.서술); int tuemi_COUNT = 호출형식.인수.size();
                출력.add(tohu("init", Pūranga_kōrero.kaipupuri_uara) + "();"); 출력.add("if(sp < " + tuemi_COUNT + ") kernel_panic(\"call stack underflow\"); sp -= " + tuemi_COUNT + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < tuemi_COUNT; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + tohu("method", Pūranga_kōrero.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (tono == 182) {
                aratuka_Pūranga_kōrero Pūranga_kōrero = tauaha_uara.Pūranga_kōrero(tono_raraunga.두바이트());
                if (Pūranga_kōrero.equals(new aratuka_Pūranga_kōrero("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Pūranga_kōrero.equals(new aratuka_Pūranga_kōrero("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Whakawhiti_Reo_hapa("가상 TAUMAHI_uara 호출 미지원");
            } else if (tono == 188) {
                if (tono_raraunga.한바이트() != 10) throw new Whakawhiti_Reo_hapa("new int[]만 Tautoko_uara"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (tono == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (tono == 196) {
                int toronga_uara = tono_raraunga.한바이트(), INDEX = tono_raraunga.두바이트(); taki_paetata(INDEX, 지역변수수);
                if (toronga_uara == 21 || toronga_uara == 25) 출력.add("PUSH(l[" + INDEX + "]);");
                else if (toronga_uara == 54 || toronga_uara == 58) 출력.add("l[" + INDEX + "] = POP();");
                else if (toronga_uara == 132) 출력.add("l[" + INDEX + "] = (uint32_t)l[" + INDEX + "] + (uint32_t)(" + tono_raraunga.부호두바이트() + ");");
                else throw new Whakawhiti_Reo_hapa("미지원 wide tono");
            } else if (tono == 198 || tono == 199) {
                출력.add("a = POP();"); 분기넣기(출력, peka_Rārangi, tūranga, tono_raraunga.부호두바이트(), "a " + (tono == 198 ? "==" : "!=") + " 0");
            } else throw new Whakawhiti_Reo_hapa(TAUMAHI_uara.kaipupuri_uara + "." + TAUMAHI_uara.Ingoa + ", paita_uara " + tūranga + ": 미지원 tono " + tono);
        }
        if (!경계들.containsAll(peka_Rārangi)) throw new Whakawhiti_Reo_hapa("tono 경계가 아닌 곳으로 peka");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String kaweake_aratuka(String Hono_tohu, String ūnga, boolean 진입점여부) {
        int tūranga_INDEX = ūnga.lastIndexOf('.'); if (tūranga_INDEX < 0 || !Hono_tohu.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Whakawhiti_Reo_hapa("내보내기 tautapa_uara Pōhēhē");
        String kaipupuri_uara = ūnga.substring(0, tūranga_INDEX).replace('.', '/'), Ingoa = ūnga.substring(tūranga_INDEX + 1); aratuka_Pūranga_kōrero tīpakonga_uara = null;
        for (aratuka_Pūranga_kōrero Pūranga_kōrero : 함수들.keySet()) if (Pūranga_kōrero.kaipupuri_uara.equals(kaipupuri_uara) && Pūranga_kōrero.Ingoa.equals(Ingoa)) {
            if (tīpakonga_uara != null) throw new Whakawhiti_Reo_hapa("겹친 내보내기 ūnga"); tīpakonga_uara = Pūranga_kōrero;
        }
        if (tīpakonga_uara == null || (함수들.get(tīpakonga_uara).uru_tāurunga & 0x100) != 0) throw new Whakawhiti_Reo_hapa("내보낼 함수가 없음 또는 native TAUMAHI_uara");
        함수형식 hōputu_uara = new 함수형식(tīpakonga_uara.서술);
        if ((진입점여부 && !hōputu_uara.인수.isEmpty()) || !Arrays.asList("V", "I").contains(hōputu_uara.반환)) throw new Whakawhiti_Reo_hapa("tāurunga_ira_uara 또는 C 경계 hōputu_uara Pōhēhē");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < hōputu_uara.인수.size(); 순번++) {
            if (!hōputu_uara.인수.get(순번).equals("I")) throw new Whakawhiti_Reo_hapa("C 경계는 int 인수만 Tautoko_uara");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (hōputu_uara.반환.equals("V") ? "void " : "int32_t ") + Hono_tohu + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + tohu("init", tīpakonga_uara.kaipupuri_uara) + "(); " + (hōputu_uara.반환.equals("V") ? "" : "return (int32_t)") + tohu("method", tīpakonga_uara.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String waihanga(String tāurunga_ira, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<aratuka_Pūranga_kōrero, mema_raraunga> tāurunga_uara : 함수들.entrySet()) {
            aratuka_Pūranga_kōrero Pūranga_kōrero = tāurunga_uara.getKey(); mema_raraunga raraunga = tāurunga_uara.getValue(); 선언들.add(함수원형(Pūranga_kōrero) + ";");
            if ((raraunga.uru_tāurunga & 0x100) != 0) {
                String TŪHONO = 기계함수들.get(Pūranga_kōrero.Ingoa + Pūranga_kōrero.서술);
                if (!Pūranga_kōrero.kaipupuri_uara.equals(mīhini_tauaha) || TŪHONO == null) throw new Whakawhiti_Reo_hapa("허용되지 않은 native TAUMAHI_uara: " + Pūranga_kōrero.Ingoa);
                int tuemi_COUNT = new 함수형식(Pūranga_kōrero.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < tuemi_COUNT; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + TŪHONO + "(" + (tuemi_COUNT == 0 ? "void" : String.join(",", Collections.nCopies(tuemi_COUNT, "word"))) + ");");
                몸체들.add(함수원형(Pūranga_kōrero) + " { return " + TŪHONO + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Pūranga_kōrero, raraunga));
        }
        for (Map.Entry<aratuka_Pūranga_kōrero, mema_raraunga> tāurunga_uara : 필드들.entrySet()) {
            aratuka_Pūranga_kōrero Pūranga_kōrero = tāurunga_uara.getKey(); byte[] taimau_uara = tāurunga_uara.getValue().huanga_uara.get("ConstantValue");
            String uara = taimau_uara == null ? "0" : taimau_kīanga(클래스들.get(Pūranga_kōrero.kaipupuri_uara), new raraunga_Pūpānui(taimau_uara).두바이트());
            필드선언들.add("static word " + tohu("field", Pūranga_kōrero.부분들()) + " = " + uara + ";");
        }
        for (String Ingoa : 클래스들.keySet()) {
            String arawhiti = tohu("init", Ingoa), tūnga_uara = tohu("state", Ingoa);
            선언들.add("static void " + arawhiti + "(void);"); 필드선언들.add("static unsigned " + tūnga_uara + ";");
            aratuka_Pūranga_kōrero Pūranga_kōrero = new aratuka_Pūranga_kōrero(Ingoa, "<clinit>", "()V");
            몸체들.add("static void " + arawhiti + "(void) { if(" + tūnga_uara + ") return; " + tūnga_uara + " = 1; " + (함수들.containsKey(Pūranga_kōrero) ? tohu("method", Pūranga_kōrero.부분들()) + "(); " : "") + tūnga_uara + " = 2; }");
        }
        몸체들.add(kaweake_aratuka("java_entry", tāurunga_ira, true)); Set<String> 공개이름 = new HashSet<>();
        for (String tautapa_uara : 내보내기목록) {
            int tūranga_INDEX = tautapa_uara.indexOf('='); if (tūranga_INDEX < 1) throw new Whakawhiti_Reo_hapa("내보내기 tautapa_uara Pōhēhē");
            String Ingoa = tautapa_uara.substring(0, tūranga_INDEX); 공개이름.add(Ingoa); 몸체들.add(kaweake_aratuka(Ingoa, tautapa_uara.substring(tūranga_INDEX + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> tāurunga_uara : 문자열들.entrySet()) {
            String Ngā_kupu = tāurunga_uara.getKey(); StringBuilder HUĀNGA_uara = new StringBuilder("static const word " + tāurunga_uara.getValue() + "[] = {" + Ngā_kupu.length());
            for (int 순번 = 0; 순번 < Ngā_kupu.length(); 순번++) HUĀNGA_uara.append(", ").append((int)Ngā_kupu.charAt(순번));
            문자열선언들.add(HUĀNGA_uara.append("};").toString());
        }
        String Tautoko_uara = Files.readString(rauemi_ara.resolve("wāhaere_reo_noa_Tautoko.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(Tautoko_uara + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String pūtake, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> ingoa_ripanga = new HashMap<>();
        for (String hononga : Files.readAllLines(rauemi_ara.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] takirua_uara = hononga.split("\t"); ingoa_ripanga.put(takirua_uara[0], takirua_uara[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(pūtake); StringBuffer mēhua = new StringBuffer();
        while (찾개.find()) {
            String Ingoa = 찾개.group(), 새이름 = Ingoa;
            if (!Ingoa.startsWith("//") && !Ingoa.startsWith("/*") && !Ingoa.startsWith("\"") && !Ingoa.startsWith("'") && !공개이름.contains(Ingoa)) {
                새이름 = ingoa_ripanga.getOrDefault(Ingoa, Ingoa);
                if (Ingoa.matches("a[0-9]+")) 새이름 = "인수" + Ingoa.substring(1);
                if (Ingoa.matches("b[0-9]+")) 새이름 = "peka" + Ingoa.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char pūāhua_uara : 새이름.toCharArray()) 표기.append(pūāhua_uara < 128 ? Character.toString(pūāhua_uara) : String.format(Locale.ROOT, "\\u%04x", (int)pūāhua_uara));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(mēhua, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(mēhua); return mēhua.toString();
    }
    String 엑스함수본문(aratuka_Pūranga_kōrero TAUMAHI_uara, mema_raraunga raraunga, Map<String,String> mīhini_ripanga, String ūnga) {
        String 표식 = tohu("method", TAUMAHI_uara.부분들());
        List<String> hononga = new ArrayList<>();
        if ((raraunga.uru_tāurunga & 0x100) != 0) {
            String TŪHONO = mīhini_ripanga.get(TAUMAHI_uara.Ingoa + TAUMAHI_uara.서술);
            if (!TAUMAHI_uara.kaipupuri_uara.equals(ūnga.equals("kernel") ? "pūkoro_uara" : "kaiwhakamahi") || TŪHONO == null) throw new Whakawhiti_Reo_hapa("허용되지 않은 native TAUMAHI_uara");
            return ".text\n" + 표식 + ":\njmp " + TŪHONO;
        }
        byte[] kuputuhi_tinana = raraunga.huanga_uara.get("Code"); if (kuputuhi_tinana == null) throw new Whakawhiti_Reo_hapa("TAUMAHI_uara 몸체가 없음");
        raraunga_Pūpānui Pūpānui_uara = new raraunga_Pūpānui(kuputuhi_tinana); Pūpānui_uara.두바이트(); int paetata_COUNT = Pūpānui_uara.두바이트();
        raraunga_Pūpānui tono_raraunga = new raraunga_Pūpānui(Pūpānui_uara.Pānuitia(Pūpānui_uara.네바이트()));
        if (Pūpānui_uara.두바이트() != 0) throw new Whakawhiti_Reo_hapa("try/catch/finally 미지원");
        함수형식 hōputu_uara = new 함수형식(TAUMAHI_uara.서술); if (paetata_COUNT < hōputu_uara.인수.size()) throw new Whakawhiti_Reo_hapa("매개변수보다 적은 paetata_whānuitanga 변수");
        Collections.addAll(hononga,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + paetata_COUNT * 4 + ", %esp");
        for (int 순번 = 0; 순번 < hōputu_uara.인수.size(); 순번++) Collections.addAll(hononga,"movl " + (8 + 4 * (hōputu_uara.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        tauaha_raraunga tauaha_uara = 클래스들.get(TAUMAHI_uara.kaipupuri_uara); Set<Integer> 경계들 = new HashSet<>(), peka_Rārangi = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (tono_raraunga.tūranga < tono_raraunga.raraunga.length) {
            int tūranga = tono_raraunga.tūranga, tono = tono_raraunga.한바이트(); String tūranga_INDEX = 표식 + "_b" + tūranga;
            hononga.add(tūranga_INDEX + ":"); 경계들.add(tūranga);
            if (tono == 0) hononga.add("nop");
            else if (tono == 1) hononga.add("pushl $0");
            else if (tono >= 2 && tono <= 8) hononga.add("pushl $" + (tono - 3));
            else if (tono == 16 || tono == 17) hononga.add("pushl $" + (tono == 16 ? tono_raraunga.부호한바이트() : tono_raraunga.부호두바이트()));
            else if (tono == 18 || tono == 19) {
                int INDEX = tono == 18 ? tono_raraunga.한바이트() : tono_raraunga.두바이트();
                hononga.add("pushl $" + 엑스상수(tauaha_uara,INDEX));
            } else if (tono == 21 || tono == 25 || (tono >= 26 && tono <= 29) || (tono >= 42 && tono <= 45) || tono == 54 || tono == 58 || (tono >= 59 && tono <= 62) || (tono >= 75 && tono <= 78)) {
                boolean 읽음 = tono < 54; int INDEX = tono == 21 || tono == 25 || tono == 54 || tono == 58 ? tono_raraunga.한바이트() : tono - (tono <= 29 ? 26 : tono <= 45 ? 42 : tono <= 62 ? 59 : 75);
                taki_paetata(INDEX,paetata_COUNT); hononga.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (tono == 46) Collections.addAll(hononga,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (tono == 79) Collections.addAll(hononga,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (tono == 87 || tono == 88) hononga.add("addl $" + (tono == 87 ? 4 : 8) + ", %esp");
            else if (tono >= 89 && tono <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] whakaraupapa_Rārangi = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[tono - 89]; 순번++) hononga.add("popl " + 저장기들[순번]);
                for (int 순번 : whakaraupapa_Rārangi[tono - 89]) hononga.add("pushl " + 저장기들[순번]);
            } else if (tono == 96 || tono == 100 || tono == 104 || tono == 126 || tono == 128 || tono == 130) {
                String mahi_uara = tono == 96 ? "addl" : tono == 100 ? "subl" : tono == 104 ? "imull" : tono == 126 ? "andl" : tono == 128 ? "orl" : "xorl";
                Collections.addAll(hononga,"popl %ecx","popl %eax",mahi_uara + " %ecx, %eax","pushl %eax");
            } else if (tono == 108 || tono == 112) Collections.addAll(hononga,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + tūranga_INDEX + "_divide","cmpl $0x80000000, %eax","jne " + tūranga_INDEX + "_divide","xorl %edx, %edx","jmp " + tūranga_INDEX + "_done",tūranga_INDEX + "_divide:","cltd","idivl %ecx",tūranga_INDEX + "_done:","pushl " + (tono == 108 ? "%eax" : "%edx"));
            else if (tono == 116) hononga.add("negl (%esp)");
            else if (tono == 120 || tono == 122 || tono == 124) Collections.addAll(hononga,"popl %ecx","popl %eax",(tono == 120 ? "sall" : tono == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (tono == 132) {
                int INDEX = tono_raraunga.한바이트(), 증가 = tono_raraunga.부호한바이트(); taki_paetata(INDEX,paetata_COUNT); hononga.add("addl $" + 증가 + ", -" + (4 * (INDEX + 1)) + "(%ebp)");
            } else if (tono >= 145 && tono <= 147) Collections.addAll(hononga,"popl %eax",tono == 145 ? "movsbl %al, %eax" : tono == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (tono >= 153 && tono <= 166) {
                if (tono <= 158) Collections.addAll(hononga,"popl %eax","testl %eax, %eax");
                else Collections.addAll(hononga,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int ūnga_uara = tūranga + tono_raraunga.부호두바이트(); peka_Rārangi.add(ūnga_uara); hononga.add(비교들[tono - (tono <= 158 ? 153 : 159)] + " " + 표식 + "_b" + ūnga_uara);
            } else if (tono == 167 || tono == 200) {
                int ūnga_uara = tūranga + (tono == 167 ? tono_raraunga.부호두바이트() : tono_raraunga.네바이트()); peka_Rārangi.add(ūnga_uara); hononga.add("jmp " + 표식 + "_b" + ūnga_uara);
            } else if (tono == 170 || tono == 171) {
                while (tono_raraunga.tūranga % 4 != 0) tono_raraunga.한바이트();
                int uara_taunoa = tūranga + tono_raraunga.네바이트(); peka_Rārangi.add(uara_taunoa); hononga.add("popl %eax");
                int tuemi_COUNT, 아래 = 0;
                if (tono == 170) { 아래 = tono_raraunga.네바이트(); int 위 = tono_raraunga.네바이트(); long roa_uara = (long)위 - 아래 + 1; if (roa_uara < 1 || roa_uara > (tono_raraunga.raraunga.length - tono_raraunga.tūranga) / 4) throw new Whakawhiti_Reo_hapa("switch topenga Pōhēhē"); tuemi_COUNT = (int)roa_uara; }
                else { tuemi_COUNT = tono_raraunga.네바이트(); if (tuemi_COUNT < 0 || tuemi_COUNT > (tono_raraunga.raraunga.length - tono_raraunga.tūranga) / 8) throw new Whakawhiti_Reo_hapa("switch rahi Pōhēhē"); }
                for (int 순번 = 0; 순번 < tuemi_COUNT; 순번++) {
                    int uara = tono == 170 ? 아래 + 순번 : tono_raraunga.네바이트(), ūnga_uara = tūranga + tono_raraunga.네바이트(); peka_Rārangi.add(ūnga_uara);
                    Collections.addAll(hononga,"cmpl $" + uara + ", %eax","je " + 표식 + "_b" + ūnga_uara);
                }
                hononga.add("jmp " + 표식 + "_b" + uara_taunoa);
            } else if (tono == 172 || tono == 176 || tono == 177) {
                if (tono != 177) hononga.add("popl %eax"); Collections.addAll(hononga,"leave","ret");
            } else if (tono == 178 || tono == 179) {
                aratuka_Pūranga_kōrero Pūranga_kōrero = tauaha_uara.Pūranga_kōrero(tono_raraunga.두바이트()); if (!필드들.containsKey(Pūranga_kōrero)) throw new Whakawhiti_Reo_hapa("알 수 없는 āpure_uara");
                Collections.addAll(hononga,"call " + tohu("init",Pūranga_kōrero.kaipupuri_uara),(tono == 178 ? "pushl " : "popl ") + tohu("field",Pūranga_kōrero.부분들()));
            } else if (tono == 184) {
                aratuka_Pūranga_kōrero Pūranga_kōrero = tauaha_uara.Pūranga_kōrero(tono_raraunga.두바이트()); if (!함수들.containsKey(Pūranga_kōrero)) throw new Whakawhiti_Reo_hapa("알 수 없는 TAUMAHI_uara");
                함수형식 호출형식 = new 함수형식(Pūranga_kōrero.서술); Collections.addAll(hononga,"call " + tohu("init",Pūranga_kōrero.kaipupuri_uara),"call " + tohu("method",Pūranga_kōrero.부분들()));
                if (!호출형식.인수.isEmpty()) hononga.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) hononga.add("pushl %eax");
            } else if (tono == 182) {
                aratuka_Pūranga_kōrero Pūranga_kōrero = tauaha_uara.Pūranga_kōrero(tono_raraunga.두바이트());
                if (Pūranga_kōrero.equals(new aratuka_Pūranga_kōrero("java/lang/String","length","()I"))) Collections.addAll(hononga,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Pūranga_kōrero.equals(new aratuka_Pūranga_kōrero("java/lang/String","charAt","(I)C"))) Collections.addAll(hononga,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Whakawhiti_Reo_hapa("가상 TAUMAHI_uara 호출 미지원");
            } else if (tono == 188) {
                if (tono_raraunga.한바이트() != 10) throw new Whakawhiti_Reo_hapa("new int[]만 Tautoko_uara"); Collections.addAll(hononga,"popl %eax","call rt_new_array","pushl %eax");
            } else if (tono == 190) Collections.addAll(hononga,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (tono == 196) {
                int toronga_uara = tono_raraunga.한바이트(), INDEX = tono_raraunga.두바이트(); taki_paetata(INDEX,paetata_COUNT);
                if (toronga_uara == 21 || toronga_uara == 25 || toronga_uara == 54 || toronga_uara == 58) hononga.add((toronga_uara <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDEX + 1) + "(%ebp)");
                else if (toronga_uara == 132) hononga.add("addl $" + tono_raraunga.부호두바이트() + ", -" + 4 * (INDEX + 1) + "(%ebp)");
                else throw new Whakawhiti_Reo_hapa("wide tono 미지원");
            } else if (tono == 198 || tono == 199) {
                int ūnga_uara = tūranga + tono_raraunga.부호두바이트(); peka_Rārangi.add(ūnga_uara); Collections.addAll(hononga,"popl %eax","testl %eax, %eax",(tono == 198 ? "je " : "jne ") + 표식 + "_b" + ūnga_uara);
            } else throw new Whakawhiti_Reo_hapa("미지원 tono: " + tono);
        }
        if (!경계들.containsAll(peka_Rārangi)) throw new Whakawhiti_Reo_hapa("tono 경계가 아닌 곳으로 peka");
        hononga.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",hononga);
    }
    String 엑스상수(tauaha_raraunga raraunga, int INDEX) {
        if (raraunga.상수종류[INDEX] == 3) return raraunga.taimau_raraunga[INDEX].toString();
        if (raraunga.상수종류[INDEX] == 8) return aho_tohu(raraunga.문자((Integer)raraunga.taimau_raraunga[INDEX]));
        throw new Whakawhiti_Reo_hapa("정수와 aho_uara 상수만 Tautoko_uara");
    }
    String 엑스조립본(String tāurunga_ira, List<String> 내보냄, String ūnga) throws IOException {
        Map<String,String> mīhini_ripanga = new HashMap<>();
        for (String hononga : Files.readAllLines(rauemi_ara.resolve("엑스기계함수.tsv"))) { String[] takirua_uara = hononga.split("\t"); if (takirua_uara[0].equals(ūnga)) mīhini_ripanga.put(takirua_uara[1] + takirua_uara[2],takirua_uara[3]); }
        int tūranga_INDEX = tāurunga_ira.lastIndexOf('.'); if (tūranga_INDEX < 0) throw new Whakawhiti_Reo_hapa("tāurunga_ira tautapa_uara Pōhēhē");
        String kaipupuri_uara = tāurunga_ira.substring(0,tūranga_INDEX).replace('.','/'), aratuka_tāurunga_ingoa = tāurunga_ira.substring(tūranga_INDEX + 1); aratuka_Pūranga_kōrero tāurunga_ira_uara = null;
        for (String 서술 : Arrays.asList("()I","()V")) { aratuka_Pūranga_kōrero Pūranga_kōrero = new aratuka_Pūranga_kōrero(kaipupuri_uara,aratuka_tāurunga_ingoa,서술); if (함수들.containsKey(Pūranga_kōrero)) { if (tāurunga_ira_uara != null) throw new Whakawhiti_Reo_hapa("겹친 tāurunga_ira"); tāurunga_ira_uara = Pūranga_kōrero; } }
        if (tāurunga_ira_uara == null || (함수들.get(tāurunga_ira_uara).uru_tāurunga & 0x100) != 0) throw new Whakawhiti_Reo_hapa("tāurunga_ira_uara TAUMAHI_uara hōputu_uara Pōhēhē");
        List<String> hononga = new ArrayList<>(); hononga.add(".code32");
        for (tauaha_raraunga raraunga : 클래스들.values()) {
            String tūnga_uara = tohu("state",raraunga.Ingoa), arawhiti = tohu("init",raraunga.Ingoa);
            Collections.addAll(hononga,".bss",".balign 4",tūnga_uara + ": .long 0",".text",arawhiti + ":","cmpl $0, " + tūnga_uara,"jne " + arawhiti + "_done","movl $1, " + tūnga_uara);
            aratuka_Pūranga_kōrero 초기화참조 = new aratuka_Pūranga_kōrero(raraunga.Ingoa,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) hononga.add("call " + tohu("method",초기화참조.부분들()));
            Collections.addAll(hononga,"movl $2, " + tūnga_uara,arawhiti + "_done:","ret");
            for (mema_raraunga āpure_uara : raraunga.āpure_uara) {
                byte[] taimau_uara = āpure_uara.huanga_uara.get("ConstantValue"); String uara = taimau_uara == null ? "0" : 엑스상수(raraunga,new raraunga_Pūpānui(taimau_uara).두바이트());
                Collections.addAll(hononga,".data",".balign 4",tohu("field",raraunga.Ingoa,āpure_uara.Ingoa,āpure_uara.서술) + ": .long " + uara);
            }
            for (mema_raraunga TAUMAHI_uara : raraunga.TAUMAHI_uara) if (!TAUMAHI_uara.Ingoa.equals("<init>")) hononga.add(엑스함수본문(new aratuka_Pūranga_kōrero(raraunga.Ingoa,TAUMAHI_uara.Ingoa,TAUMAHI_uara.서술),TAUMAHI_uara,mīhini_ripanga,ūnga));
        }
        Collections.addAll(hononga,".text",".globl java_entry","java_entry:","call " + tohu("init",tāurunga_ira_uara.kaipupuri_uara),"call " + tohu("method",tāurunga_ira_uara.부분들()));
        if (tāurunga_ira_uara.서술.equals("()V")) hononga.add("xorl %eax, %eax"); hononga.add("ret");
        for (String tautapa_uara : 내보냄) {
            int pūwehe_uara = tautapa_uara.indexOf('='); if (pūwehe_uara < 1) throw new Whakawhiti_Reo_hapa("내보내기 tautapa_uara Pōhēhē");
            String 외부 = tautapa_uara.substring(0,pūwehe_uara), TAUMAHI_uara = tautapa_uara.substring(pūwehe_uara + 1); int whakawehenga_mēhua = TAUMAHI_uara.lastIndexOf('.');
            if (whakawehenga_mēhua < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Whakawhiti_Reo_hapa("내보내기 tohu Pōhēhē");
            String tauaha_uara = TAUMAHI_uara.substring(0,whakawehenga_mēhua).replace('.','/'), Ingoa = TAUMAHI_uara.substring(whakawehenga_mēhua + 1); aratuka_Pūranga_kōrero tīpakonga_uara = null;
            for (aratuka_Pūranga_kōrero Pūranga_kōrero : 함수들.keySet()) if (Pūranga_kōrero.kaipupuri_uara.equals(tauaha_uara) && Pūranga_kōrero.Ingoa.equals(Ingoa)) { if (tīpakonga_uara != null) throw new Whakawhiti_Reo_hapa("겹친 내보내기 ūnga"); tīpakonga_uara = Pūranga_kōrero; }
            if (tīpakonga_uara == null) throw new Whakawhiti_Reo_hapa("내보낼 함수가 없음");
            Collections.addAll(hononga,".text",".globl " + 외부,외부 + ":","call " + tohu("init",tīpakonga_uara.kaipupuri_uara),"jmp " + tohu("method",tīpakonga_uara.부분들()));
        }
        hononga.add(".section .rodata");
        for (Map.Entry<String,String> tāurunga_uara : 문자열들.entrySet()) {
            Collections.addAll(hononga,".balign 4",tāurunga_uara.getValue() + ":",".long " + tāurunga_uara.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char ngā_wae_uara : tāurunga_uara.getKey().toCharArray()) 단위들.add(Integer.toString(ngā_wae_uara)); if (!단위들.isEmpty()) hononga.add(".long " + String.join(",",단위들));
        }
        hononga.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",hononga) + "\n";
    }
    static void kawe_utauta(List<String> tono) throws Exception {
        if (new ProcessBuilder(tono).inheritIO().start().waitFor() != 0) throw new Whakawhiti_Reo_hapa("hanga_pūtake Pōhēhē: " + tono.get(0));
    }
    static String raraunga_aho(String Ngā_kupu) { return "\"" + Ngā_kupu.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String ūnga, String tāurunga_ira, List<String> 내보냄, Path 출력, Path rauemi_uara) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), tauaha_ara = 임시.resolve("classes"); Files.createDirectory(tauaha_ara);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",tauaha_ara.toString(),"-sourcepath",tauaha_ara.toString(),"-d",tauaha_ara.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int pūtake_COUNT = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Whakawhiti_Reo_hapa("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); pūtake_COUNT++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Whakawhiti_Reo_hapa(".java 또는 .class만 Tautoko_uara");
            }
            if (pūtake_COUNT > 0) kawe_utauta(자바명령);
            try (java.util.stream.Stream<Path> ara_Rārangi = Files.walk(tauaha_ara)) { ara_Rārangi.filter(ara -> ara.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERT_uara = new 기계어미리번역(바이트코드,ūnga.equals("user") ? "user" : "kernel",262144,rauemi_uara);
            String 조립 = CONVERT_uara.엑스조립본(tāurunga_ira,내보냄,ūnga); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path utauta_tūranga = rauemi_uara.getParent();
            kawe_utauta(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            kawe_utauta(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),utauta_tūranga.resolve("wāhaere_reo_noa_Tautoko.s").toString()));
            List<String> TŪHONO = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (ūnga.equals("kernel")) TŪHONO.add("-r");
            else {
                kawe_utauta(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),utauta_tūranga.resolve(ūnga.equals("user") ? "Start_kaiwhakamahi_kaupapa.s" : "리눅스시작.s").toString()));
                Collections.addAll(TŪHONO,"-e","_start",임시.resolve("start.o").toString());
                if (ūnga.equals("user")) Collections.addAll(TŪHONO,"-T",utauta_tūranga.resolve("kaiwhakamahi_Hono_Tahora.ld").toString());
            }
            Collections.addAll(TŪHONO,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); kawe_utauta(TŪHONO);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path whakaputa_uara = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),whakaputa_uara,StandardCopyOption.REPLACE_EXISTING); Files.move(whakaputa_uara,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(whakaputa_uara); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(ūnga.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> tohu_raraunga = new ArrayList<>(), raraunga_pūtake = new ArrayList<>();
            for (aratuka_Pūranga_kōrero Pūranga_kōrero : CONVERT_uara.함수들.keySet()) tohu_raraunga.add(raraunga_aho(tohu("method",Pūranga_kōrero.부분들())) + ":" + raraunga_aho(Pūranga_kōrero.kaipupuri_uara + "." + Pūranga_kōrero.Ingoa + Pūranga_kōrero.서술));
            for (Path 입력 : 입력들) {
                byte[] hash_kōnae = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Ngā_kupu = new StringBuilder(); for (byte uara : hash_kōnae) Ngā_kupu.append(String.format(Locale.ROOT,"%02x",uara & 255));
                raraunga_pūtake.add(raraunga_aho(입력.toAbsolutePath().toString()) + ":" + raraunga_aho(Ngā_kupu.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + raraunga_aho(ūnga) + ",\"entry\":" + raraunga_aho(tāurunga_ira) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",tohu_raraunga) + "},\"sources\":{" + String.join(",",raraunga_pūtake) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> ara_Rārangi = Files.walk(임시)) { for (Path ara : (Iterable<Path>)ara_Rārangi.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(ara); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String tāurunga_ira = null, ūnga = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> ara_Rārangi = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String uara = 인수[순번];
                switch (uara) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry tauaha_uara.TAUMAHI_uara -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export tohu=tauaha_uara.TAUMAHI_uara] 클래스파일 또는 Java원문"); return;
                    case "--entry": tāurunga_ira = 인수[++순번]; break;
                    case "--profile": ūnga = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (uara.startsWith("-")) throw new Whakawhiti_Reo_hapa("알 수 없는 옵션: " + uara); ara_Rārangi.add(Paths.get(uara));
                }
            }
            if (tāurunga_ira == null || 출력경로 == null || ara_Rārangi.isEmpty()) throw new Whakawhiti_Reo_hapa("--entry, -o, tauaha_uara 파일이 필요합니다");
            Path rauemi_uara = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Whakawhiti_Reo_hapa("알 수 없는 kawe_tono ūnga");
                엑스번역(ara_Rārangi,엑스대상,tāurunga_ira,내보냄,출력경로,rauemi_uara); return;
            }
            String pūtake = new 기계어미리번역(ara_Rārangi, ūnga, 낱말수, rauemi_uara).waihanga(tāurunga_ira, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, pūtake, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Pōhēhē) { System.err.println("hanga_pūtake Pōhēhē: " + Pōhēhē.getMessage()); System.exit(1); }
    }
}
