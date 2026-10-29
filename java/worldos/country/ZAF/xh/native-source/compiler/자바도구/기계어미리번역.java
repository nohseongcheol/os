// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java iklasi_ixabiso 파일에서 독립 ARM64 커널용 C 원문을 만든다. umsingathi JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Uguqulelo_magama_impazamo extends RuntimeException {
        Uguqulelo_magama_impazamo(String 설명) { super(설명); }
    }
    static final class iingcombolo_Umfundi {
        final byte[] iingcombolo;
        int 위치;
        iingcombolo_Umfundi(byte[] 입력자료) { iingcombolo = 입력자료; }
        byte[] Funda(int ubude_ixabiso) {
            if (ubude_ixabiso < 0 || ubude_ixabiso > iingcombolo.length - 위치) throw new Uguqulelo_magama_impazamo("잘린 iklasi_ixabiso 또는 Umyalelo iingcombolo");
            byte[] 결과 = Arrays.copyOfRange(iingcombolo, 위치, 위치 + ubude_ixabiso); 위치 += ubude_ixabiso; return 결과;
        }
        int 한바이트() { if (위치 >= iingcombolo.length) throw new Uguqulelo_magama_impazamo("잘린 Umyalelo iingcombolo"); return iingcombolo[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class ilungu_iingcombolo {
        final int fikelela_ufako_nkcukacha;
        final String Igama, 서술;
        final Map<String, byte[]> uphawu_ixabiso;
        ilungu_iingcombolo(int fikelela_ixabiso, String igama_ixabiso, String 서술값, Map<String, byte[]> uphawu_iingcombolo) {
            fikelela_ufako_nkcukacha = fikelela_ixabiso; Igama = igama_ixabiso; 서술 = 서술값; uphawu_ixabiso = uphawu_iingcombolo;
        }
    }
    static final class imethodi_Isalathiso implements Comparable<imethodi_Isalathiso> {
        final String umnini_ixabiso, Igama, 서술;
        imethodi_Isalathiso(String 소유값, String igama_ixabiso, String 서술값) { umnini_ixabiso = 소유값; Igama = igama_ixabiso; 서술 = 서술값; }
        String[] 부분들() { return new String[]{umnini_ixabiso, Igama, 서술}; }
        public int compareTo(imethodi_Isalathiso untanga_ixabiso) {
            int 비교값 = umnini_ixabiso.compareTo(untanga_ixabiso.umnini_ixabiso);
            if (비교값 == 0) 비교값 = Igama.compareTo(untanga_ixabiso.Igama);
            return 비교값 == 0 ? 서술.compareTo(untanga_ixabiso.서술) : 비교값;
        }
        public boolean equals(Object untanga_ixabiso) { return untanga_ixabiso instanceof imethodi_Isalathiso && compareTo((imethodi_Isalathiso) untanga_ixabiso) == 0; }
        public int hashCode() { return Objects.hash(umnini_ixabiso, Igama, 서술); }
    }
    static final class iklasi_iingcombolo {
        final int[] 상수종류;
        final Object[] engajikiyo_iingcombolo;
        final String Igama;
        final List<ilungu_iingcombolo> ifildi_ixabiso, INKQUBO_ixabiso;
        iklasi_iingcombolo(Path INDLELA) throws IOException {
            iingcombolo_Umfundi Umfundi_ixabiso = new iingcombolo_Umfundi(Files.readAllBytes(INDLELA));
            if (Umfundi_ixabiso.네바이트() != 0xcafebabe) throw new Uguqulelo_magama_impazamo("Java iklasi_ixabiso 표식이 아님");
            Umfundi_ixabiso.Funda(4);
            int 개수 = Umfundi_ixabiso.두바이트(); 상수종류 = new int[개수]; engajikiyo_iingcombolo = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = Umfundi_ixabiso.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int ubude_ixabiso = Umfundi_ixabiso.두바이트();
                        byte[] ikharakhtha_isigcini_lwazi_sethutyana = Umfundi_ixabiso.Funda(ubude_ixabiso), 길이붙인자료 = new byte[ubude_ixabiso + 2];
                        길이붙인자료[0] = (byte)(ubude_ixabiso >> 8); 길이붙인자료[1] = (byte)ubude_ixabiso;
                        System.arraycopy(ikharakhtha_isigcini_lwazi_sethutyana, 0, 길이붙인자료, 2, ubude_ixabiso);
                        engajikiyo_iingcombolo[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: engajikiyo_iingcombolo[순번] = Umfundi_ixabiso.네바이트(); break;
                    case 4: Umfundi_ixabiso.Funda(4); break;
                    case 5: case 6: Umfundi_ixabiso.Funda(8); 순번++; break;
                    case 7: case 8: case 16: engajikiyo_iingcombolo[순번] = Umfundi_ixabiso.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        engajikiyo_iingcombolo[순번] = new int[]{Umfundi_ixabiso.두바이트(), Umfundi_ixabiso.두바이트()}; break;
                    case 15: engajikiyo_iingcombolo[순번] = new int[]{Umfundi_ixabiso.한바이트(), Umfundi_ixabiso.두바이트()}; break;
                    default: throw new Uguqulelo_magama_impazamo("지원하지 않는 engajikiyo_ixabiso 종류: " + 종류);
                }
            }
            Umfundi_ixabiso.두바이트(); Igama = iklasi_igama(Umfundi_ixabiso.두바이트());
            if (!iklasi_igama(Umfundi_ixabiso.두바이트()).equals("java/lang/Object") || Umfundi_ixabiso.두바이트() != 0)
                throw new Uguqulelo_magama_impazamo(Igama + ": 상속 및 인터페이스 미지원");
            ifildi_ixabiso = 멤버읽기(Umfundi_ixabiso); INKQUBO_ixabiso = 멤버읽기(Umfundi_ixabiso); 속성읽기(Umfundi_ixabiso);
            if (Umfundi_ixabiso.위치 != Umfundi_ixabiso.iingcombolo.length) throw new Uguqulelo_magama_impazamo("iklasi_ixabiso 뒤에 남은 iingcombolo");
        }
        String 문자(int indeksa) {
            if (indeksa < 1 || indeksa >= 상수종류.length || 상수종류[indeksa] != 1) throw new Uguqulelo_magama_impazamo("문자 engajikiyo_ixabiso indeksa Impazamo");
            return (String) engajikiyo_iingcombolo[indeksa];
        }
        String iklasi_igama(int indeksa) {
            if (indeksa < 1 || indeksa >= 상수종류.length || 상수종류[indeksa] != 7) throw new Uguqulelo_magama_impazamo("iklasi_ixabiso Isalathiso Impazamo");
            return 문자((Integer)engajikiyo_iingcombolo[indeksa]);
        }
        imethodi_Isalathiso Isalathiso(int indeksa) {
            if (indeksa < 1 || indeksa >= 상수종류.length || 상수종류[indeksa] < 9 || 상수종류[indeksa] > 11) throw new Uguqulelo_magama_impazamo("멤버 Isalathiso Impazamo");
            int[] beka_ngazibini_ixabiso = (int[])engajikiyo_iingcombolo[indeksa], igama_beka_ngazibini = (int[])engajikiyo_iingcombolo[beka_ngazibini_ixabiso[1]];
            return new imethodi_Isalathiso(iklasi_igama(beka_ngazibini_ixabiso[0]), 문자(igama_beka_ngazibini[0]), 문자(igama_beka_ngazibini[1]));
        }
        Map<String, byte[]> 속성읽기(iingcombolo_Umfundi Umfundi_ixabiso) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = Umfundi_ixabiso.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String uphawu_igama = 문자(Umfundi_ixabiso.두바이트()); byte[] ixabiso = Umfundi_ixabiso.Funda(Umfundi_ixabiso.네바이트());
                if (결과.put(uphawu_igama, ixabiso) != null) throw new Uguqulelo_magama_impazamo("겹친 uphawu_ixabiso: " + uphawu_igama);
            }
            return 결과;
        }
        List<ilungu_iingcombolo> 멤버읽기(iingcombolo_Umfundi Umfundi_ixabiso) {
            List<ilungu_iingcombolo> 결과 = new ArrayList<>(); int 개수 = Umfundi_ixabiso.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int fikelela_ufako_nkcukacha = Umfundi_ixabiso.두바이트(); String imethodi_ufako_nkcukacha_igama = 문자(Umfundi_ixabiso.두바이트()), 서술 = 문자(Umfundi_ixabiso.두바이트());
                결과.add(new ilungu_iingcombolo(fikelela_ufako_nkcukacha, imethodi_ufako_nkcukacha_igama, 서술, 속성읽기(Umfundi_ixabiso)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Uguqulelo_magama_impazamo("INKQUBO_ixabiso 서술 Impazamo: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Uguqulelo_magama_impazamo("INKQUBO_ixabiso 서술 Impazamo: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Uguqulelo_magama_impazamo("INKQUBO_ixabiso 서술 Impazamo: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String ukukhetha_ixabiso = null;
            for (String fomatha_ixabiso : 허용형식) if (서술.startsWith(fomatha_ixabiso, 위치)) { ukukhetha_ixabiso = fomatha_ixabiso; break; }
            if (ukukhetha_ixabiso == null) throw new Uguqulelo_magama_impazamo("지원하지 않는 ugcino_lweengcombolo: " + 서술);
            결과.add(ukukhetha_ixabiso); 위치 += ukukhetha_ixabiso.length();
        }
        return 결과;
    }
    static String isimboli(String 종류, String... 부분들) {
        try {
            byte[] i_hash_ifayile = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder Umbhalo = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) Umbhalo.append(String.format(Locale.ROOT, "%02x", i_hash_ifayile[순번] & 255));
            return Umbhalo.toString();
        } catch (Exception Impazamo) { throw new Uguqulelo_magama_impazamo(Impazamo.toString()); }
    }
    final Map<String, iklasi_iingcombolo> 클래스들 = new TreeMap<>();
    final Map<imethodi_Isalathiso, ilungu_iingcombolo> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, umatshini_iklasi;
    final int 동적기억낱말수;
    final Path isixhobo_sekhompyutha_indlela;
    기계어미리번역(List<Path> indlela_uludwe, String ithagethi, int 낱말수, Path isixhobo_sekhompyutha_ixabiso) throws IOException {
        if ((!ithagethi.equals("kernel") && !ithagethi.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Uguqulelo_magama_impazamo("ukwenza_umyalelo ithagethi 또는 imemori_ixabiso 공간 Ubukhulu Impazamo");
        실행대상 = ithagethi; 동적기억낱말수 = 낱말수; isixhobo_sekhompyutha_indlela = isixhobo_sekhompyutha_ixabiso;
        // 이 이름도 국가별 umthombo_umthi 생성 시 해당 언어로 옮긴다.
        umatshini_iklasi = ithagethi.equals("kernel") ? "보드" : "umsebenzisi";
        for (String umgca : Files.readAllLines(isixhobo_sekhompyutha_ixabiso.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = umgca.split("\t", -1);
            if (부분들.length != 4) throw new Uguqulelo_magama_impazamo("umatshini INKQUBO_ixabiso iingcombolo Impazamo");
            if (부분들[0].equals(ithagethi)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path INDLELA : indlela_uludwe) {
            iklasi_iingcombolo iingcombolo = new iklasi_iingcombolo(INDLELA);
            if (클래스들.put(iingcombolo.Igama, iingcombolo) != null) throw new Uguqulelo_magama_impazamo("중복 iklasi_ixabiso: " + iingcombolo.Igama);
            for (ilungu_iingcombolo ifildi_ixabiso : iingcombolo.ifildi_ixabiso) {
                if ((ifildi_ixabiso.fikelela_ufako_nkcukacha & 8) == 0 || 형식읽기(ifildi_ixabiso.서술).equals(Collections.singletonList("V"))) throw new Uguqulelo_magama_impazamo("imi_ndawonye_ixabiso 필드만 inkxaso_ixabiso");
                if (필드들.put(new imethodi_Isalathiso(iingcombolo.Igama, ifildi_ixabiso.Igama, ifildi_ixabiso.서술), ifildi_ixabiso) != null) throw new Uguqulelo_magama_impazamo("중복 ifildi_ixabiso");
            }
            for (ilungu_iingcombolo INKQUBO_ixabiso : iingcombolo.INKQUBO_ixabiso) {
                if (INKQUBO_ixabiso.Igama.equals("<init>")) continue;
                if ((INKQUBO_ixabiso.fikelela_ufako_nkcukacha & 8) == 0 || (INKQUBO_ixabiso.fikelela_ufako_nkcukacha & (0x20 | 0x400)) != 0) throw new Uguqulelo_magama_impazamo("imi_ndawonye_ixabiso 비동기화 함수만 inkxaso_ixabiso");
                new 함수형식(INKQUBO_ixabiso.서술);
                if (함수들.put(new imethodi_Isalathiso(iingcombolo.Igama, INKQUBO_ixabiso.Igama, INKQUBO_ixabiso.서술), INKQUBO_ixabiso) != null) throw new Uguqulelo_magama_impazamo("중복 INKQUBO_ixabiso");
            }
        }
    }
    String uluhlu_lweekharektha_isimboli(String Umbhalo) { return 문자열들.computeIfAbsent(Umbhalo, ixabiso -> "j_text_" + 문자열들.size()); }
    String engajikiyo_usetyenziso_oluxubileyo(iklasi_iingcombolo iingcombolo, int indeksa) {
        if (indeksa < 1 || indeksa >= iingcombolo.상수종류.length) throw new Uguqulelo_magama_impazamo("engajikiyo_ixabiso indeksa ikliphu Impazamo");
        if (iingcombolo.상수종류[indeksa] == 3) return "(word)(uint32_t)(" + iingcombolo.engajikiyo_iingcombolo[indeksa] + ")";
        if (iingcombolo.상수종류[indeksa] == 8) return "(word)" + uluhlu_lweekharektha_isimboli(iingcombolo.문자((Integer)iingcombolo.engajikiyo_iingcombolo[indeksa]));
        throw new Uguqulelo_magama_impazamo("정수와 uluhlu_lweekharektha_ixabiso 상수만 inkxaso_ixabiso");
    }
    String 함수원형(imethodi_Isalathiso Isalathiso) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Isalathiso.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + isimboli("method", Isalathiso.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void jonga_eyale_ndawo(int indeksa, int 지역변수수) { if (indeksa < 0 || indeksa >= 지역변수수) throw new Uguqulelo_magama_impazamo("eyale_ndawo_umda 변수 indeksa ikliphu Impazamo"); }
    void 분기넣기(List<String> 출력, Set<Integer> isebe_uludwe, int 위치, int 이동량, String imo) {
        int indawo_ekuyiwa_kuyo_ixabiso = 위치 + 이동량; isebe_uludwe.add(indawo_ekuyiwa_kuyo_ixabiso);
        출력.add((imo == null ? "" : "if (" + imo + ") ") + "goto b" + indawo_ekuyiwa_kuyo_ixabiso + ";");
    }
    String 함수본문(imethodi_Isalathiso INKQUBO_ixabiso, ilungu_iingcombolo iingcombolo) {
        byte[] 본문자료 = iingcombolo.uphawu_ixabiso.get("Code"); if (본문자료 == null) throw new Uguqulelo_magama_impazamo("INKQUBO_ixabiso 몸체가 없음: " + INKQUBO_ixabiso.Igama);
        iingcombolo_Umfundi Umfundi_ixabiso = new iingcombolo_Umfundi(본문자료); int 쌓임깊이 = Umfundi_ixabiso.두바이트(), 지역변수수 = Umfundi_ixabiso.두바이트();
        iingcombolo_Umfundi umyalelo_iingcombolo = new iingcombolo_Umfundi(Umfundi_ixabiso.Funda(Umfundi_ixabiso.네바이트()));
        if (Umfundi_ixabiso.두바이트() != 0) throw new Uguqulelo_magama_impazamo("try/catch/finally 미지원");
        함수형식 fomatha_ixabiso = new 함수형식(INKQUBO_ixabiso.서술); if (지역변수수 < fomatha_ixabiso.인수.size()) throw new Uguqulelo_magama_impazamo("매개변수보다 적은 eyale_ndawo_umda 변수");
        iklasi_iingcombolo iklasi_ixabiso = 클래스들.get(INKQUBO_ixabiso.umnini_ixabiso);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(INKQUBO_ixabiso) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < fomatha_ixabiso.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), isebe_uludwe = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (umyalelo_iingcombolo.위치 < umyalelo_iingcombolo.iingcombolo.length) {
            int 위치 = umyalelo_iingcombolo.위치, Umyalelo = umyalelo_iingcombolo.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (Umyalelo == 0) continue;
            if (Umyalelo == 1) 출력.add("PUSH(0);");
            else if (Umyalelo >= 2 && Umyalelo <= 8) 출력.add("PUSH((uint32_t)(" + (Umyalelo - 3) + "));");
            else if (Umyalelo == 16 || Umyalelo == 17) 출력.add("PUSH((uint32_t)(" + (Umyalelo == 16 ? umyalelo_iingcombolo.부호한바이트() : umyalelo_iingcombolo.부호두바이트()) + "));");
            else if (Umyalelo == 18 || Umyalelo == 19) 출력.add("PUSH(" + engajikiyo_usetyenziso_oluxubileyo(iklasi_ixabiso, Umyalelo == 18 ? umyalelo_iingcombolo.한바이트() : umyalelo_iingcombolo.두바이트()) + ");");
            else if (Umyalelo == 21 || Umyalelo == 25 || (Umyalelo >= 26 && Umyalelo <= 29) || (Umyalelo >= 42 && Umyalelo <= 45)) {
                int indeksa = Umyalelo == 21 || Umyalelo == 25 ? umyalelo_iingcombolo.한바이트() : Umyalelo - (Umyalelo <= 29 ? 26 : 42);
                jonga_eyale_ndawo(indeksa, 지역변수수); 출력.add("PUSH(l[" + indeksa + "]);");
            } else if (Umyalelo == 54 || Umyalelo == 58 || (Umyalelo >= 59 && Umyalelo <= 62) || (Umyalelo >= 75 && Umyalelo <= 78)) {
                int indeksa = Umyalelo == 54 || Umyalelo == 58 ? umyalelo_iingcombolo.한바이트() : Umyalelo - (Umyalelo <= 62 ? 59 : 75);
                jonga_eyale_ndawo(indeksa, 지역변수수); 출력.add("l[" + indeksa + "] = POP();");
            } else if (Umyalelo == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Umyalelo == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Umyalelo == 87 || Umyalelo == 88) 출력.add(Umyalelo == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Umyalelo >= 89 && Umyalelo <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ulandelelwano_uludwe = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Umyalelo - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char ixabiso : ulandelelwano_uludwe[Umyalelo - 89].toCharArray()) 출력.add("PUSH(" + ixabiso + ");");
            } else if (Umyalelo == 96 || Umyalelo == 100 || Umyalelo == 104 || Umyalelo == 126 || Umyalelo == 128 || Umyalelo == 130) {
                String isibalo_ixabiso = Umyalelo == 96 ? "+" : Umyalelo == 100 ? "-" : Umyalelo == 104 ? "*" : Umyalelo == 126 ? "&" : Umyalelo == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + isibalo_ixabiso + " (uint32_t)b);");
            } else if (Umyalelo == 108 || Umyalelo == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Umyalelo == 112 ? 1 : 0) + "));");
            else if (Umyalelo == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Umyalelo == 120 || Umyalelo == 122 || Umyalelo == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Umyalelo == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Umyalelo == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Umyalelo == 132) {
                int indeksa = umyalelo_iingcombolo.한바이트(), 증가량 = umyalelo_iingcombolo.부호한바이트(); jonga_eyale_ndawo(indeksa, 지역변수수);
                출력.add("l[" + indeksa + "] = (uint32_t)l[" + indeksa + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Umyalelo >= 145 && Umyalelo <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Umyalelo == 145 ? "int8_t" : Umyalelo == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Umyalelo >= 153 && Umyalelo <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, isebe_uludwe, 위치, umyalelo_iingcombolo.부호두바이트(), "(int32_t)a " + 비교들[Umyalelo - 153] + " 0");
            } else if (Umyalelo >= 159 && Umyalelo <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, isebe_uludwe, 위치, umyalelo_iingcombolo.부호두바이트(), Umyalelo >= 165 ? "a " + 비교들[Umyalelo - 159] + " b" : "(int32_t)a " + 비교들[Umyalelo - 159] + " (int32_t)b");
            } else if (Umyalelo == 167 || Umyalelo == 200) 분기넣기(출력, isebe_uludwe, 위치, Umyalelo == 167 ? umyalelo_iingcombolo.부호두바이트() : umyalelo_iingcombolo.네바이트(), null);
            else if (Umyalelo == 170 || Umyalelo == 171) {
                while (umyalelo_iingcombolo.위치 % 4 != 0) umyalelo_iingcombolo.한바이트();
                int ixabiso_elisisiseko = umyalelo_iingcombolo.네바이트(); 출력.add("a = POP();");
                if (Umyalelo == 170) {
                    int 아래 = umyalelo_iingcombolo.네바이트(), 위 = umyalelo_iingcombolo.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (umyalelo_iingcombolo.iingcombolo.length - umyalelo_iingcombolo.위치) / 4) throw new Uguqulelo_magama_impazamo("switch ikliphu Impazamo");
                    for (long ixabiso = 아래; ixabiso <= 위; ixabiso++) 분기넣기(출력, isebe_uludwe, 위치, umyalelo_iingcombolo.네바이트(), "(int32_t)a == (" + ixabiso + ")");
                } else {
                    int 개수 = umyalelo_iingcombolo.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (umyalelo_iingcombolo.iingcombolo.length - umyalelo_iingcombolo.위치) / 8) throw new Uguqulelo_magama_impazamo("switch Ubukhulu Impazamo");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int ixabiso = umyalelo_iingcombolo.네바이트(); if (순번 > 0 && ixabiso <= 앞값) throw new Uguqulelo_magama_impazamo("switch ulandelelwano_ixabiso Impazamo"); 앞값 = ixabiso;
                        분기넣기(출력, isebe_uludwe, 위치, umyalelo_iingcombolo.네바이트(), "(int32_t)a == (" + ixabiso + ")");
                    }
                }
                분기넣기(출력, isebe_uludwe, 위치, ixabiso_elisisiseko, null);
            } else if (Umyalelo == 172 || Umyalelo == 176 || Umyalelo == 177) 출력.add("return " + (Umyalelo == 177 ? "0" : "POP()") + ";");
            else if (Umyalelo == 178 || Umyalelo == 179) {
                imethodi_Isalathiso Isalathiso = iklasi_ixabiso.Isalathiso(umyalelo_iingcombolo.두바이트()); if (!필드들.containsKey(Isalathiso)) throw new Uguqulelo_magama_impazamo("알 수 없는 ifildi_ixabiso");
                출력.add(isimboli("init", Isalathiso.umnini_ixabiso) + "();"); String ifildi_ixabiso = isimboli("field", Isalathiso.부분들());
                출력.add(Umyalelo == 178 ? "PUSH(" + ifildi_ixabiso + ");" : ifildi_ixabiso + " = POP();");
            } else if (Umyalelo == 184) {
                imethodi_Isalathiso Isalathiso = iklasi_ixabiso.Isalathiso(umyalelo_iingcombolo.두바이트()); if (!함수들.containsKey(Isalathiso)) throw new Uguqulelo_magama_impazamo("알 수 없는 INKQUBO_ixabiso");
                함수형식 호출형식 = new 함수형식(Isalathiso.서술); int 개수 = 호출형식.인수.size();
                출력.add(isimboli("init", Isalathiso.umnini_ixabiso) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + isimboli("method", Isalathiso.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Umyalelo == 182) {
                imethodi_Isalathiso Isalathiso = iklasi_ixabiso.Isalathiso(umyalelo_iingcombolo.두바이트());
                if (Isalathiso.equals(new imethodi_Isalathiso("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Isalathiso.equals(new imethodi_Isalathiso("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Uguqulelo_magama_impazamo("가상 INKQUBO_ixabiso 호출 미지원");
            } else if (Umyalelo == 188) {
                if (umyalelo_iingcombolo.한바이트() != 10) throw new Uguqulelo_magama_impazamo("new int[]만 inkxaso_ixabiso"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Umyalelo == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Umyalelo == 196) {
                int isongezelelo_ixabiso = umyalelo_iingcombolo.한바이트(), indeksa = umyalelo_iingcombolo.두바이트(); jonga_eyale_ndawo(indeksa, 지역변수수);
                if (isongezelelo_ixabiso == 21 || isongezelelo_ixabiso == 25) 출력.add("PUSH(l[" + indeksa + "]);");
                else if (isongezelelo_ixabiso == 54 || isongezelelo_ixabiso == 58) 출력.add("l[" + indeksa + "] = POP();");
                else if (isongezelelo_ixabiso == 132) 출력.add("l[" + indeksa + "] = (uint32_t)l[" + indeksa + "] + (uint32_t)(" + umyalelo_iingcombolo.부호두바이트() + ");");
                else throw new Uguqulelo_magama_impazamo("미지원 wide Umyalelo");
            } else if (Umyalelo == 198 || Umyalelo == 199) {
                출력.add("a = POP();"); 분기넣기(출력, isebe_uludwe, 위치, umyalelo_iingcombolo.부호두바이트(), "a " + (Umyalelo == 198 ? "==" : "!=") + " 0");
            } else throw new Uguqulelo_magama_impazamo(INKQUBO_ixabiso.umnini_ixabiso + "." + INKQUBO_ixabiso.Igama + ", ibhayithi_ixabiso " + 위치 + ": 미지원 Umyalelo " + Umyalelo);
        }
        if (!경계들.containsAll(isebe_uludwe)) throw new Uguqulelo_magama_impazamo("Umyalelo 경계가 아닌 곳으로 isebe");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String thumela_ngaphandle_imethodi(String Ilinki_isimboli, String ithagethi, boolean 진입점여부) {
        int 자리 = ithagethi.lastIndexOf('.'); if (자리 < 0 || !Ilinki_isimboli.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Uguqulelo_magama_impazamo("내보내기 yabela_ixabiso Impazamo");
        String umnini_ixabiso = ithagethi.substring(0, 자리).replace('.', '/'), Igama = ithagethi.substring(자리 + 1); imethodi_Isalathiso ukukhetha_ixabiso = null;
        for (imethodi_Isalathiso Isalathiso : 함수들.keySet()) if (Isalathiso.umnini_ixabiso.equals(umnini_ixabiso) && Isalathiso.Igama.equals(Igama)) {
            if (ukukhetha_ixabiso != null) throw new Uguqulelo_magama_impazamo("겹친 내보내기 ithagethi"); ukukhetha_ixabiso = Isalathiso;
        }
        if (ukukhetha_ixabiso == null || (함수들.get(ukukhetha_ixabiso).fikelela_ufako_nkcukacha & 0x100) != 0) throw new Uguqulelo_magama_impazamo("내보낼 함수가 없음 또는 native INKQUBO_ixabiso");
        함수형식 fomatha_ixabiso = new 함수형식(ukukhetha_ixabiso.서술);
        if ((진입점여부 && !fomatha_ixabiso.인수.isEmpty()) || !Arrays.asList("V", "I").contains(fomatha_ixabiso.반환)) throw new Uguqulelo_magama_impazamo("ufako_nkcukacha_inqaku_ixabiso 또는 C 경계 fomatha_ixabiso Impazamo");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < fomatha_ixabiso.인수.size(); 순번++) {
            if (!fomatha_ixabiso.인수.get(순번).equals("I")) throw new Uguqulelo_magama_impazamo("C 경계는 int 인수만 inkxaso_ixabiso");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (fomatha_ixabiso.반환.equals("V") ? "void " : "int32_t ") + Ilinki_isimboli + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + isimboli("init", ukukhetha_ixabiso.umnini_ixabiso) + "(); " + (fomatha_ixabiso.반환.equals("V") ? "" : "return (int32_t)") + isimboli("method", ukukhetha_ixabiso.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String ufako_nkcukacha_inqaku, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<imethodi_Isalathiso, ilungu_iingcombolo> ufako_nkcukacha_ixabiso : 함수들.entrySet()) {
            imethodi_Isalathiso Isalathiso = ufako_nkcukacha_ixabiso.getKey(); ilungu_iingcombolo iingcombolo = ufako_nkcukacha_ixabiso.getValue(); 선언들.add(함수원형(Isalathiso) + ";");
            if ((iingcombolo.fikelela_ufako_nkcukacha & 0x100) != 0) {
                String Nxulumanisa = 기계함수들.get(Isalathiso.Igama + Isalathiso.서술);
                if (!Isalathiso.umnini_ixabiso.equals(umatshini_iklasi) || Nxulumanisa == null) throw new Uguqulelo_magama_impazamo("허용되지 않은 native INKQUBO_ixabiso: " + Isalathiso.Igama);
                int 개수 = new 함수형식(Isalathiso.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Nxulumanisa + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Isalathiso) + " { return " + Nxulumanisa + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Isalathiso, iingcombolo));
        }
        for (Map.Entry<imethodi_Isalathiso, ilungu_iingcombolo> ufako_nkcukacha_ixabiso : 필드들.entrySet()) {
            imethodi_Isalathiso Isalathiso = ufako_nkcukacha_ixabiso.getKey(); byte[] engajikiyo_ixabiso = ufako_nkcukacha_ixabiso.getValue().uphawu_ixabiso.get("ConstantValue");
            String ixabiso = engajikiyo_ixabiso == null ? "0" : engajikiyo_usetyenziso_oluxubileyo(클래스들.get(Isalathiso.umnini_ixabiso), new iingcombolo_Umfundi(engajikiyo_ixabiso).두바이트());
            필드선언들.add("static word " + isimboli("field", Isalathiso.부분들()) + " = " + ixabiso + ";");
        }
        for (String Igama : 클래스들.keySet()) {
            String qalisa_umsebenzi = isimboli("init", Igama), imo_ixabiso = isimboli("state", Igama);
            선언들.add("static void " + qalisa_umsebenzi + "(void);"); 필드선언들.add("static unsigned " + imo_ixabiso + ";");
            imethodi_Isalathiso Isalathiso = new imethodi_Isalathiso(Igama, "<clinit>", "()V");
            몸체들.add("static void " + qalisa_umsebenzi + "(void) { if(" + imo_ixabiso + ") return; " + imo_ixabiso + " = 1; " + (함수들.containsKey(Isalathiso) ? isimboli("method", Isalathiso.부분들()) + "(); " : "") + imo_ixabiso + " = 2; }");
        }
        몸체들.add(thumela_ngaphandle_imethodi("java_entry", ufako_nkcukacha_inqaku, true)); Set<String> 공개이름 = new HashSet<>();
        for (String yabela_ixabiso : 내보내기목록) {
            int 자리 = yabela_ixabiso.indexOf('='); if (자리 < 1) throw new Uguqulelo_magama_impazamo("내보내기 yabela_ixabiso Impazamo");
            String Igama = yabela_ixabiso.substring(0, 자리); 공개이름.add(Igama); 몸체들.add(thumela_ngaphandle_imethodi(Igama, yabela_ixabiso.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> ufako_nkcukacha_ixabiso : 문자열들.entrySet()) {
            String Umbhalo = ufako_nkcukacha_ixabiso.getKey(); StringBuilder ULUHLU_ixabiso = new StringBuilder("static const word " + ufako_nkcukacha_ixabiso.getValue() + "[] = {" + Umbhalo.length());
            for (int 순번 = 0; 순번 < Umbhalo.length(); 순번++) ULUHLU_ixabiso.append(", ").append((int)Umbhalo.charAt(순번));
            문자열선언들.add(ULUHLU_ixabiso.append("};").toString());
        }
        String inkxaso_ixabiso = Files.readString(isixhobo_sekhompyutha_indlela.resolve("ixesha_lokusebenza_kolwimi_oluqhelekileyo_inkxaso.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(inkxaso_ixabiso + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String UMTHOMBO, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> igama_itheyibhile = new HashMap<>();
        for (String umgca : Files.readAllLines(isixhobo_sekhompyutha_indlela.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] beka_ngazibini_ixabiso = umgca.split("\t"); igama_itheyibhile.put(beka_ngazibini_ixabiso[0], beka_ngazibini_ixabiso[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(UMTHOMBO); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String Igama = 찾개.group(), 새이름 = Igama;
            if (!Igama.startsWith("//") && !Igama.startsWith("/*") && !Igama.startsWith("\"") && !Igama.startsWith("'") && !공개이름.contains(Igama)) {
                새이름 = igama_itheyibhile.getOrDefault(Igama, Igama);
                if (Igama.matches("a[0-9]+")) 새이름 = "인수" + Igama.substring(1);
                if (Igama.matches("b[0-9]+")) 새이름 = "isebe" + Igama.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char ikharakhtha_ixabiso : 새이름.toCharArray()) 표기.append(ikharakhtha_ixabiso < 128 ? Character.toString(ikharakhtha_ixabiso) : String.format(Locale.ROOT, "\\u%04x", (int)ikharakhtha_ixabiso));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(imethodi_Isalathiso INKQUBO_ixabiso, ilungu_iingcombolo iingcombolo, Map<String,String> umatshini_itheyibhile, String ithagethi) {
        String 표식 = isimboli("method", INKQUBO_ixabiso.부분들());
        List<String> umgca = new ArrayList<>();
        if ((iingcombolo.fikelela_ufako_nkcukacha & 0x100) != 0) {
            String Nxulumanisa = umatshini_itheyibhile.get(INKQUBO_ixabiso.Igama + INKQUBO_ixabiso.서술);
            if (!INKQUBO_ixabiso.umnini_ixabiso.equals(ithagethi.equals("kernel") ? "isixhobo_ixabiso" : "umsebenzisi") || Nxulumanisa == null) throw new Uguqulelo_magama_impazamo("허용되지 않은 native INKQUBO_ixabiso");
            return ".text\n" + 표식 + ":\njmp " + Nxulumanisa;
        }
        byte[] isiqu_sombhalo = iingcombolo.uphawu_ixabiso.get("Code"); if (isiqu_sombhalo == null) throw new Uguqulelo_magama_impazamo("INKQUBO_ixabiso 몸체가 없음");
        iingcombolo_Umfundi Umfundi_ixabiso = new iingcombolo_Umfundi(isiqu_sombhalo); Umfundi_ixabiso.두바이트(); int 지역수 = Umfundi_ixabiso.두바이트();
        iingcombolo_Umfundi umyalelo_iingcombolo = new iingcombolo_Umfundi(Umfundi_ixabiso.Funda(Umfundi_ixabiso.네바이트()));
        if (Umfundi_ixabiso.두바이트() != 0) throw new Uguqulelo_magama_impazamo("try/catch/finally 미지원");
        함수형식 fomatha_ixabiso = new 함수형식(INKQUBO_ixabiso.서술); if (지역수 < fomatha_ixabiso.인수.size()) throw new Uguqulelo_magama_impazamo("매개변수보다 적은 eyale_ndawo_umda 변수");
        Collections.addAll(umgca,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < fomatha_ixabiso.인수.size(); 순번++) Collections.addAll(umgca,"movl " + (8 + 4 * (fomatha_ixabiso.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        iklasi_iingcombolo iklasi_ixabiso = 클래스들.get(INKQUBO_ixabiso.umnini_ixabiso); Set<Integer> 경계들 = new HashSet<>(), isebe_uludwe = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (umyalelo_iingcombolo.위치 < umyalelo_iingcombolo.iingcombolo.length) {
            int 위치 = umyalelo_iingcombolo.위치, Umyalelo = umyalelo_iingcombolo.한바이트(); String 자리 = 표식 + "_b" + 위치;
            umgca.add(자리 + ":"); 경계들.add(위치);
            if (Umyalelo == 0) umgca.add("nop");
            else if (Umyalelo == 1) umgca.add("pushl $0");
            else if (Umyalelo >= 2 && Umyalelo <= 8) umgca.add("pushl $" + (Umyalelo - 3));
            else if (Umyalelo == 16 || Umyalelo == 17) umgca.add("pushl $" + (Umyalelo == 16 ? umyalelo_iingcombolo.부호한바이트() : umyalelo_iingcombolo.부호두바이트()));
            else if (Umyalelo == 18 || Umyalelo == 19) {
                int indeksa = Umyalelo == 18 ? umyalelo_iingcombolo.한바이트() : umyalelo_iingcombolo.두바이트();
                umgca.add("pushl $" + 엑스상수(iklasi_ixabiso,indeksa));
            } else if (Umyalelo == 21 || Umyalelo == 25 || (Umyalelo >= 26 && Umyalelo <= 29) || (Umyalelo >= 42 && Umyalelo <= 45) || Umyalelo == 54 || Umyalelo == 58 || (Umyalelo >= 59 && Umyalelo <= 62) || (Umyalelo >= 75 && Umyalelo <= 78)) {
                boolean 읽음 = Umyalelo < 54; int indeksa = Umyalelo == 21 || Umyalelo == 25 || Umyalelo == 54 || Umyalelo == 58 ? umyalelo_iingcombolo.한바이트() : Umyalelo - (Umyalelo <= 29 ? 26 : Umyalelo <= 45 ? 42 : Umyalelo <= 62 ? 59 : 75);
                jonga_eyale_ndawo(indeksa,지역수); umgca.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (indeksa + 1)) + "(%ebp)");
            } else if (Umyalelo == 46) Collections.addAll(umgca,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Umyalelo == 79) Collections.addAll(umgca,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Umyalelo == 87 || Umyalelo == 88) umgca.add("addl $" + (Umyalelo == 87 ? 4 : 8) + ", %esp");
            else if (Umyalelo >= 89 && Umyalelo <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ulandelelwano_uludwe = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Umyalelo - 89]; 순번++) umgca.add("popl " + 저장기들[순번]);
                for (int 순번 : ulandelelwano_uludwe[Umyalelo - 89]) umgca.add("pushl " + 저장기들[순번]);
            } else if (Umyalelo == 96 || Umyalelo == 100 || Umyalelo == 104 || Umyalelo == 126 || Umyalelo == 128 || Umyalelo == 130) {
                String isibalo_ixabiso = Umyalelo == 96 ? "addl" : Umyalelo == 100 ? "subl" : Umyalelo == 104 ? "imull" : Umyalelo == 126 ? "andl" : Umyalelo == 128 ? "orl" : "xorl";
                Collections.addAll(umgca,"popl %ecx","popl %eax",isibalo_ixabiso + " %ecx, %eax","pushl %eax");
            } else if (Umyalelo == 108 || Umyalelo == 112) Collections.addAll(umgca,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (Umyalelo == 108 ? "%eax" : "%edx"));
            else if (Umyalelo == 116) umgca.add("negl (%esp)");
            else if (Umyalelo == 120 || Umyalelo == 122 || Umyalelo == 124) Collections.addAll(umgca,"popl %ecx","popl %eax",(Umyalelo == 120 ? "sall" : Umyalelo == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Umyalelo == 132) {
                int indeksa = umyalelo_iingcombolo.한바이트(), 증가 = umyalelo_iingcombolo.부호한바이트(); jonga_eyale_ndawo(indeksa,지역수); umgca.add("addl $" + 증가 + ", -" + (4 * (indeksa + 1)) + "(%ebp)");
            } else if (Umyalelo >= 145 && Umyalelo <= 147) Collections.addAll(umgca,"popl %eax",Umyalelo == 145 ? "movsbl %al, %eax" : Umyalelo == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Umyalelo >= 153 && Umyalelo <= 166) {
                if (Umyalelo <= 158) Collections.addAll(umgca,"popl %eax","testl %eax, %eax");
                else Collections.addAll(umgca,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int indawo_ekuyiwa_kuyo_ixabiso = 위치 + umyalelo_iingcombolo.부호두바이트(); isebe_uludwe.add(indawo_ekuyiwa_kuyo_ixabiso); umgca.add(비교들[Umyalelo - (Umyalelo <= 158 ? 153 : 159)] + " " + 표식 + "_b" + indawo_ekuyiwa_kuyo_ixabiso);
            } else if (Umyalelo == 167 || Umyalelo == 200) {
                int indawo_ekuyiwa_kuyo_ixabiso = 위치 + (Umyalelo == 167 ? umyalelo_iingcombolo.부호두바이트() : umyalelo_iingcombolo.네바이트()); isebe_uludwe.add(indawo_ekuyiwa_kuyo_ixabiso); umgca.add("jmp " + 표식 + "_b" + indawo_ekuyiwa_kuyo_ixabiso);
            } else if (Umyalelo == 170 || Umyalelo == 171) {
                while (umyalelo_iingcombolo.위치 % 4 != 0) umyalelo_iingcombolo.한바이트();
                int ixabiso_elisisiseko = 위치 + umyalelo_iingcombolo.네바이트(); isebe_uludwe.add(ixabiso_elisisiseko); umgca.add("popl %eax");
                int 개수, 아래 = 0;
                if (Umyalelo == 170) { 아래 = umyalelo_iingcombolo.네바이트(); int 위 = umyalelo_iingcombolo.네바이트(); long ubude_ixabiso = (long)위 - 아래 + 1; if (ubude_ixabiso < 1 || ubude_ixabiso > (umyalelo_iingcombolo.iingcombolo.length - umyalelo_iingcombolo.위치) / 4) throw new Uguqulelo_magama_impazamo("switch ikliphu Impazamo"); 개수 = (int)ubude_ixabiso; }
                else { 개수 = umyalelo_iingcombolo.네바이트(); if (개수 < 0 || 개수 > (umyalelo_iingcombolo.iingcombolo.length - umyalelo_iingcombolo.위치) / 8) throw new Uguqulelo_magama_impazamo("switch Ubukhulu Impazamo"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int ixabiso = Umyalelo == 170 ? 아래 + 순번 : umyalelo_iingcombolo.네바이트(), indawo_ekuyiwa_kuyo_ixabiso = 위치 + umyalelo_iingcombolo.네바이트(); isebe_uludwe.add(indawo_ekuyiwa_kuyo_ixabiso);
                    Collections.addAll(umgca,"cmpl $" + ixabiso + ", %eax","je " + 표식 + "_b" + indawo_ekuyiwa_kuyo_ixabiso);
                }
                umgca.add("jmp " + 표식 + "_b" + ixabiso_elisisiseko);
            } else if (Umyalelo == 172 || Umyalelo == 176 || Umyalelo == 177) {
                if (Umyalelo != 177) umgca.add("popl %eax"); Collections.addAll(umgca,"leave","ret");
            } else if (Umyalelo == 178 || Umyalelo == 179) {
                imethodi_Isalathiso Isalathiso = iklasi_ixabiso.Isalathiso(umyalelo_iingcombolo.두바이트()); if (!필드들.containsKey(Isalathiso)) throw new Uguqulelo_magama_impazamo("알 수 없는 ifildi_ixabiso");
                Collections.addAll(umgca,"call " + isimboli("init",Isalathiso.umnini_ixabiso),(Umyalelo == 178 ? "pushl " : "popl ") + isimboli("field",Isalathiso.부분들()));
            } else if (Umyalelo == 184) {
                imethodi_Isalathiso Isalathiso = iklasi_ixabiso.Isalathiso(umyalelo_iingcombolo.두바이트()); if (!함수들.containsKey(Isalathiso)) throw new Uguqulelo_magama_impazamo("알 수 없는 INKQUBO_ixabiso");
                함수형식 호출형식 = new 함수형식(Isalathiso.서술); Collections.addAll(umgca,"call " + isimboli("init",Isalathiso.umnini_ixabiso),"call " + isimboli("method",Isalathiso.부분들()));
                if (!호출형식.인수.isEmpty()) umgca.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) umgca.add("pushl %eax");
            } else if (Umyalelo == 182) {
                imethodi_Isalathiso Isalathiso = iklasi_ixabiso.Isalathiso(umyalelo_iingcombolo.두바이트());
                if (Isalathiso.equals(new imethodi_Isalathiso("java/lang/String","length","()I"))) Collections.addAll(umgca,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Isalathiso.equals(new imethodi_Isalathiso("java/lang/String","charAt","(I)C"))) Collections.addAll(umgca,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Uguqulelo_magama_impazamo("가상 INKQUBO_ixabiso 호출 미지원");
            } else if (Umyalelo == 188) {
                if (umyalelo_iingcombolo.한바이트() != 10) throw new Uguqulelo_magama_impazamo("new int[]만 inkxaso_ixabiso"); Collections.addAll(umgca,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Umyalelo == 190) Collections.addAll(umgca,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Umyalelo == 196) {
                int isongezelelo_ixabiso = umyalelo_iingcombolo.한바이트(), indeksa = umyalelo_iingcombolo.두바이트(); jonga_eyale_ndawo(indeksa,지역수);
                if (isongezelelo_ixabiso == 21 || isongezelelo_ixabiso == 25 || isongezelelo_ixabiso == 54 || isongezelelo_ixabiso == 58) umgca.add((isongezelelo_ixabiso <= 25 ? "pushl " : "popl ") + "-" + 4 * (indeksa + 1) + "(%ebp)");
                else if (isongezelelo_ixabiso == 132) umgca.add("addl $" + umyalelo_iingcombolo.부호두바이트() + ", -" + 4 * (indeksa + 1) + "(%ebp)");
                else throw new Uguqulelo_magama_impazamo("wide Umyalelo 미지원");
            } else if (Umyalelo == 198 || Umyalelo == 199) {
                int indawo_ekuyiwa_kuyo_ixabiso = 위치 + umyalelo_iingcombolo.부호두바이트(); isebe_uludwe.add(indawo_ekuyiwa_kuyo_ixabiso); Collections.addAll(umgca,"popl %eax","testl %eax, %eax",(Umyalelo == 198 ? "je " : "jne ") + 표식 + "_b" + indawo_ekuyiwa_kuyo_ixabiso);
            } else throw new Uguqulelo_magama_impazamo("미지원 Umyalelo: " + Umyalelo);
        }
        if (!경계들.containsAll(isebe_uludwe)) throw new Uguqulelo_magama_impazamo("Umyalelo 경계가 아닌 곳으로 isebe");
        umgca.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",umgca);
    }
    String 엑스상수(iklasi_iingcombolo iingcombolo, int indeksa) {
        if (iingcombolo.상수종류[indeksa] == 3) return iingcombolo.engajikiyo_iingcombolo[indeksa].toString();
        if (iingcombolo.상수종류[indeksa] == 8) return uluhlu_lweekharektha_isimboli(iingcombolo.문자((Integer)iingcombolo.engajikiyo_iingcombolo[indeksa]));
        throw new Uguqulelo_magama_impazamo("정수와 uluhlu_lweekharektha_ixabiso 상수만 inkxaso_ixabiso");
    }
    String 엑스조립본(String ufako_nkcukacha_inqaku, List<String> 내보냄, String ithagethi) throws IOException {
        Map<String,String> umatshini_itheyibhile = new HashMap<>();
        for (String umgca : Files.readAllLines(isixhobo_sekhompyutha_indlela.resolve("엑스기계함수.tsv"))) { String[] beka_ngazibini_ixabiso = umgca.split("\t"); if (beka_ngazibini_ixabiso[0].equals(ithagethi)) umatshini_itheyibhile.put(beka_ngazibini_ixabiso[1] + beka_ngazibini_ixabiso[2],beka_ngazibini_ixabiso[3]); }
        int 자리 = ufako_nkcukacha_inqaku.lastIndexOf('.'); if (자리 < 0) throw new Uguqulelo_magama_impazamo("ufako_nkcukacha_inqaku yabela_ixabiso Impazamo");
        String umnini_ixabiso = ufako_nkcukacha_inqaku.substring(0,자리).replace('.','/'), imethodi_ufako_nkcukacha_igama = ufako_nkcukacha_inqaku.substring(자리 + 1); imethodi_Isalathiso ufako_nkcukacha_inqaku_ixabiso = null;
        for (String 서술 : Arrays.asList("()I","()V")) { imethodi_Isalathiso Isalathiso = new imethodi_Isalathiso(umnini_ixabiso,imethodi_ufako_nkcukacha_igama,서술); if (함수들.containsKey(Isalathiso)) { if (ufako_nkcukacha_inqaku_ixabiso != null) throw new Uguqulelo_magama_impazamo("겹친 ufako_nkcukacha_inqaku"); ufako_nkcukacha_inqaku_ixabiso = Isalathiso; } }
        if (ufako_nkcukacha_inqaku_ixabiso == null || (함수들.get(ufako_nkcukacha_inqaku_ixabiso).fikelela_ufako_nkcukacha & 0x100) != 0) throw new Uguqulelo_magama_impazamo("ufako_nkcukacha_inqaku_ixabiso INKQUBO_ixabiso fomatha_ixabiso Impazamo");
        List<String> umgca = new ArrayList<>(); umgca.add(".code32");
        for (iklasi_iingcombolo iingcombolo : 클래스들.values()) {
            String imo_ixabiso = isimboli("state",iingcombolo.Igama), qalisa_umsebenzi = isimboli("init",iingcombolo.Igama);
            Collections.addAll(umgca,".bss",".balign 4",imo_ixabiso + ": .long 0",".text",qalisa_umsebenzi + ":","cmpl $0, " + imo_ixabiso,"jne " + qalisa_umsebenzi + "_done","movl $1, " + imo_ixabiso);
            imethodi_Isalathiso 초기화참조 = new imethodi_Isalathiso(iingcombolo.Igama,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) umgca.add("call " + isimboli("method",초기화참조.부분들()));
            Collections.addAll(umgca,"movl $2, " + imo_ixabiso,qalisa_umsebenzi + "_done:","ret");
            for (ilungu_iingcombolo ifildi_ixabiso : iingcombolo.ifildi_ixabiso) {
                byte[] engajikiyo_ixabiso = ifildi_ixabiso.uphawu_ixabiso.get("ConstantValue"); String ixabiso = engajikiyo_ixabiso == null ? "0" : 엑스상수(iingcombolo,new iingcombolo_Umfundi(engajikiyo_ixabiso).두바이트());
                Collections.addAll(umgca,".data",".balign 4",isimboli("field",iingcombolo.Igama,ifildi_ixabiso.Igama,ifildi_ixabiso.서술) + ": .long " + ixabiso);
            }
            for (ilungu_iingcombolo INKQUBO_ixabiso : iingcombolo.INKQUBO_ixabiso) if (!INKQUBO_ixabiso.Igama.equals("<init>")) umgca.add(엑스함수본문(new imethodi_Isalathiso(iingcombolo.Igama,INKQUBO_ixabiso.Igama,INKQUBO_ixabiso.서술),INKQUBO_ixabiso,umatshini_itheyibhile,ithagethi));
        }
        Collections.addAll(umgca,".text",".globl java_entry","java_entry:","call " + isimboli("init",ufako_nkcukacha_inqaku_ixabiso.umnini_ixabiso),"call " + isimboli("method",ufako_nkcukacha_inqaku_ixabiso.부분들()));
        if (ufako_nkcukacha_inqaku_ixabiso.서술.equals("()V")) umgca.add("xorl %eax, %eax"); umgca.add("ret");
        for (String yabela_ixabiso : 내보냄) {
            int isinqandi_esimiselweyo_ixabiso = yabela_ixabiso.indexOf('='); if (isinqandi_esimiselweyo_ixabiso < 1) throw new Uguqulelo_magama_impazamo("내보내기 yabela_ixabiso Impazamo");
            String 외부 = yabela_ixabiso.substring(0,isinqandi_esimiselweyo_ixabiso), INKQUBO_ixabiso = yabela_ixabiso.substring(isinqandi_esimiselweyo_ixabiso + 1); int 나눔 = INKQUBO_ixabiso.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Uguqulelo_magama_impazamo("내보내기 isimboli Impazamo");
            String iklasi_ixabiso = INKQUBO_ixabiso.substring(0,나눔).replace('.','/'), Igama = INKQUBO_ixabiso.substring(나눔 + 1); imethodi_Isalathiso ukukhetha_ixabiso = null;
            for (imethodi_Isalathiso Isalathiso : 함수들.keySet()) if (Isalathiso.umnini_ixabiso.equals(iklasi_ixabiso) && Isalathiso.Igama.equals(Igama)) { if (ukukhetha_ixabiso != null) throw new Uguqulelo_magama_impazamo("겹친 내보내기 ithagethi"); ukukhetha_ixabiso = Isalathiso; }
            if (ukukhetha_ixabiso == null) throw new Uguqulelo_magama_impazamo("내보낼 함수가 없음");
            Collections.addAll(umgca,".text",".globl " + 외부,외부 + ":","call " + isimboli("init",ukukhetha_ixabiso.umnini_ixabiso),"jmp " + isimboli("method",ukukhetha_ixabiso.부분들()));
        }
        umgca.add(".section .rodata");
        for (Map.Entry<String,String> ufako_nkcukacha_ixabiso : 문자열들.entrySet()) {
            Collections.addAll(umgca,".balign 4",ufako_nkcukacha_ixabiso.getValue() + ":",".long " + ufako_nkcukacha_ixabiso.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char isifundo_ixabiso : ufako_nkcukacha_ixabiso.getKey().toCharArray()) 단위들.add(Integer.toString(isifundo_ixabiso)); if (!단위들.isEmpty()) umgca.add(".long " + String.join(",",단위들));
        }
        umgca.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",umgca) + "\n";
    }
    static void ukwenza_isixhobo_sokutayipha(List<String> Umyalelo) throws Exception {
        if (new ProcessBuilder(Umyalelo).inheritIO().start().waitFor() != 0) throw new Uguqulelo_magama_impazamo("yakha_umthombo Impazamo: " + Umyalelo.get(0));
    }
    static String iingcombolo_uluhlu_lweekharektha(String Umbhalo) { return "\"" + Umbhalo.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String ithagethi, String ufako_nkcukacha_inqaku, List<String> 내보냄, Path 출력, Path isixhobo_sekhompyutha_ixabiso) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), iklasi_indlela = 임시.resolve("classes"); Files.createDirectory(iklasi_indlela);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",iklasi_indlela.toString(),"-sourcepath",iklasi_indlela.toString(),"-d",iklasi_indlela.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Uguqulelo_magama_impazamo("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Uguqulelo_magama_impazamo(".java 또는 .class만 inkxaso_ixabiso");
            }
            if (원문수 > 0) ukwenza_isixhobo_sokutayipha(자바명령);
            try (java.util.stream.Stream<Path> indlela_uludwe = Files.walk(iklasi_indlela)) { indlela_uludwe.filter(INDLELA -> INDLELA.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,ithagethi.equals("user") ? "user" : "kernel",262144,isixhobo_sekhompyutha_ixabiso);
            String 조립 = 변환.엑스조립본(ufako_nkcukacha_inqaku,내보냄,ithagethi); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = isixhobo_sekhompyutha_ixabiso.getParent();
            ukwenza_isixhobo_sokutayipha(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            ukwenza_isixhobo_sokutayipha(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("ixesha_lokusebenza_kolwimi_oluqhelekileyo_inkxaso.s").toString()));
            List<String> Nxulumanisa = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (ithagethi.equals("kernel")) Nxulumanisa.add("-r");
            else {
                ukwenza_isixhobo_sokutayipha(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(ithagethi.equals("user") ? "qala_umsebenzisi_inkqubo.s" : "리눅스시작.s").toString()));
                Collections.addAll(Nxulumanisa,"-e","_start",임시.resolve("start.o").toString());
                if (ithagethi.equals("user")) Collections.addAll(Nxulumanisa,"-T",도구위치.resolve("umsebenzisi_Ilinki_ubume.ld").toString());
            }
            Collections.addAll(Nxulumanisa,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); ukwenza_isixhobo_sokutayipha(Nxulumanisa);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path papasha_ixabiso = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),papasha_ixabiso,StandardCopyOption.REPLACE_EXISTING); Files.move(papasha_ixabiso,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(papasha_ixabiso); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(ithagethi.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> isimboli_iingcombolo = new ArrayList<>(), umthombo_weengcombolo = new ArrayList<>();
            for (imethodi_Isalathiso Isalathiso : 변환.함수들.keySet()) isimboli_iingcombolo.add(iingcombolo_uluhlu_lweekharektha(isimboli("method",Isalathiso.부분들())) + ":" + iingcombolo_uluhlu_lweekharektha(Isalathiso.umnini_ixabiso + "." + Isalathiso.Igama + Isalathiso.서술));
            for (Path 입력 : 입력들) {
                byte[] i_hash_ifayile = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder Umbhalo = new StringBuilder(); for (byte ixabiso : i_hash_ifayile) Umbhalo.append(String.format(Locale.ROOT,"%02x",ixabiso & 255));
                umthombo_weengcombolo.add(iingcombolo_uluhlu_lweekharektha(입력.toAbsolutePath().toString()) + ":" + iingcombolo_uluhlu_lweekharektha(Umbhalo.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + iingcombolo_uluhlu_lweekharektha(ithagethi) + ",\"entry\":" + iingcombolo_uluhlu_lweekharektha(ufako_nkcukacha_inqaku) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",isimboli_iingcombolo) + "},\"sources\":{" + String.join(",",umthombo_weengcombolo) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> indlela_uludwe = Files.walk(임시)) { for (Path INDLELA : (Iterable<Path>)indlela_uludwe.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(INDLELA); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String ufako_nkcukacha_inqaku = null, ithagethi = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> indlela_uludwe = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String ixabiso = 인수[순번];
                switch (ixabiso) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry iklasi_ixabiso.INKQUBO_ixabiso -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export isimboli=iklasi_ixabiso.INKQUBO_ixabiso] 클래스파일 또는 Java원문"); return;
                    case "--entry": ufako_nkcukacha_inqaku = 인수[++순번]; break;
                    case "--profile": ithagethi = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (ixabiso.startsWith("-")) throw new Uguqulelo_magama_impazamo("알 수 없는 옵션: " + ixabiso); indlela_uludwe.add(Paths.get(ixabiso));
                }
            }
            if (ufako_nkcukacha_inqaku == null || 출력경로 == null || indlela_uludwe.isEmpty()) throw new Uguqulelo_magama_impazamo("--entry, -o, iklasi_ixabiso 파일이 필요합니다");
            Path isixhobo_sekhompyutha_ixabiso = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Uguqulelo_magama_impazamo("알 수 없는 ukwenza_umyalelo ithagethi");
                엑스번역(indlela_uludwe,엑스대상,ufako_nkcukacha_inqaku,내보냄,출력경로,isixhobo_sekhompyutha_ixabiso); return;
            }
            String UMTHOMBO = new 기계어미리번역(indlela_uludwe, ithagethi, 낱말수, isixhobo_sekhompyutha_ixabiso).생성(ufako_nkcukacha_inqaku, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, UMTHOMBO, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception Impazamo) { System.err.println("yakha_umthombo Impazamo: " + Impazamo.getMessage()); System.exit(1); }
    }
}
