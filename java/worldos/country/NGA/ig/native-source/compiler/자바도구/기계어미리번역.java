// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java klaàsị_valuu 파일에서 독립 ARM64 커널용 C 원문을 만든다. usu JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Ntụgharị_mmejọ extends RuntimeException {
        Ntụgharị_mmejọ(String 설명) { super(설명); }
    }
    static final class datà_Ọgụụ {
        final byte[] datà;
        int 위치;
        datà_Ọgụụ(byte[] 입력자료) { datà = 입력자료; }
        byte[] Wepụta_ọzi(int ogologo_valuu) {
            if (ogologo_valuu < 0 || ogologo_valuu > datà.length - 위치) throw new Ntụgharị_mmejọ("잘린 klaàsị_valuu 또는 Ntiiwu datà");
            byte[] 결과 = Arrays.copyOfRange(datà, 위치, 위치 + ogologo_valuu); 위치 += ogologo_valuu; return 결과;
        }
        int 한바이트() { if (위치 >= datà.length) throw new Ntụgharị_mmejọ("잘린 Ntiiwu datà"); return datà[위치++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class onyeòtù_datà {
        final int òhèrè_ndebà;
        final String Aha, 서술;
        final Map<String, byte[]> njìama_valuu;
        onyeòtù_datà(int òhèrè_valuu, String akara_ahà_valuu, String 서술값, Map<String, byte[]> njìama_datà) {
            òhèrè_ndebà = òhèrè_valuu; Aha = akara_ahà_valuu; 서술 = 서술값; njìama_valuu = njìama_datà;
        }
    }
    static final class usoro_Nrụtụ_aka implements Comparable<usoro_Nrụtụ_aka> {
        final String nwe_valuu, Aha, 서술;
        usoro_Nrụtụ_aka(String 소유값, String akara_ahà_valuu, String 서술값) { nwe_valuu = 소유값; Aha = akara_ahà_valuu; 서술 = 서술값; }
        String[] 부분들() { return new String[]{nwe_valuu, Aha, 서술}; }
        public int compareTo(usoro_Nrụtụ_aka ibè_valuu) {
            int 비교값 = nwe_valuu.compareTo(ibè_valuu.nwe_valuu);
            if (비교값 == 0) 비교값 = Aha.compareTo(ibè_valuu.Aha);
            return 비교값 == 0 ? 서술.compareTo(ibè_valuu.서술) : 비교값;
        }
        public boolean equals(Object ibè_valuu) { return ibè_valuu instanceof usoro_Nrụtụ_aka && compareTo((usoro_Nrụtụ_aka) ibè_valuu) == 0; }
        public int hashCode() { return Objects.hash(nwe_valuu, Aha, 서술); }
    }
    static final class klaàsị_datà {
        final int[] 상수종류;
        final Object[] ihendịgide_datà;
        final String Aha;
        final List<onyeòtù_datà> fild_valuu, ọrụ_valuu;
        klaàsị_datà(Path ụzọ_ozi) throws IOException {
            datà_Ọgụụ Ọgụụ_valuu = new datà_Ọgụụ(Files.readAllBytes(ụzọ_ozi));
            if (Ọgụụ_valuu.네바이트() != 0xcafebabe) throw new Ntụgharị_mmejọ("Java klaàsị_valuu 표식이 아님");
            Ọgụụ_valuu.Wepụta_ọzi(4);
            int 개수 = Ọgụụ_valuu.두바이트(); 상수종류 = new int[개수]; ihendịgide_datà = new Object[개수];
            for (int 순번 = 1; 순번 < 개수; 순번++) {
                int 종류 = Ọgụụ_valuu.한바이트(); 상수종류[순번] = 종류;
                switch (종류) {
                    case 1:
                        int ogologo_valuu = Ọgụụ_valuu.두바이트();
                        byte[] mkpụrụedemede_ebenchekwatụ = Ọgụụ_valuu.Wepụta_ọzi(ogologo_valuu), 길이붙인자료 = new byte[ogologo_valuu + 2];
                        길이붙인자료[0] = (byte)(ogologo_valuu >> 8); 길이붙인자료[1] = (byte)ogologo_valuu;
                        System.arraycopy(mkpụrụedemede_ebenchekwatụ, 0, 길이붙인자료, 2, ogologo_valuu);
                        ihendịgide_datà[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: ihendịgide_datà[순번] = Ọgụụ_valuu.네바이트(); break;
                    case 4: Ọgụụ_valuu.Wepụta_ọzi(4); break;
                    case 5: case 6: Ọgụụ_valuu.Wepụta_ọzi(8); 순번++; break;
                    case 7: case 8: case 16: ihendịgide_datà[순번] = Ọgụụ_valuu.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        ihendịgide_datà[순번] = new int[]{Ọgụụ_valuu.두바이트(), Ọgụụ_valuu.두바이트()}; break;
                    case 15: ihendịgide_datà[순번] = new int[]{Ọgụụ_valuu.한바이트(), Ọgụụ_valuu.두바이트()}; break;
                    default: throw new Ntụgharị_mmejọ("지원하지 않는 ihendịgide_valuu 종류: " + 종류);
                }
            }
            Ọgụụ_valuu.두바이트(); Aha = klaàsị_akara_ahà(Ọgụụ_valuu.두바이트());
            if (!klaàsị_akara_ahà(Ọgụụ_valuu.두바이트()).equals("java/lang/Object") || Ọgụụ_valuu.두바이트() != 0)
                throw new Ntụgharị_mmejọ(Aha + ": 상속 및 인터페이스 미지원");
            fild_valuu = 멤버읽기(Ọgụụ_valuu); ọrụ_valuu = 멤버읽기(Ọgụụ_valuu); 속성읽기(Ọgụụ_valuu);
            if (Ọgụụ_valuu.위치 != Ọgụụ_valuu.datà.length) throw new Ntụgharị_mmejọ("klaàsị_valuu 뒤에 남은 datà");
        }
        String 문자(int indèks) {
            if (indèks < 1 || indèks >= 상수종류.length || 상수종류[indèks] != 1) throw new Ntụgharị_mmejọ("문자 ihendịgide_valuu indèks mmejọ");
            return (String) ihendịgide_datà[indèks];
        }
        String klaàsị_akara_ahà(int indèks) {
            if (indèks < 1 || indèks >= 상수종류.length || 상수종류[indèks] != 7) throw new Ntụgharị_mmejọ("klaàsị_valuu Nrụtụ_aka mmejọ");
            return 문자((Integer)ihendịgide_datà[indèks]);
        }
        usoro_Nrụtụ_aka Nrụtụ_aka(int indèks) {
            if (indèks < 1 || indèks >= 상수종류.length || 상수종류[indèks] < 9 || 상수종류[indèks] > 11) throw new Ntụgharị_mmejọ("멤버 Nrụtụ_aka mmejọ");
            int[] àbụọ_àbụọ_valuu = (int[])ihendịgide_datà[indèks], akara_ahà_àbụọ_àbụọ = (int[])ihendịgide_datà[àbụọ_àbụọ_valuu[1]];
            return new usoro_Nrụtụ_aka(klaàsị_akara_ahà(àbụọ_àbụọ_valuu[0]), 문자(akara_ahà_àbụọ_àbụọ[0]), 문자(akara_ahà_àbụọ_àbụọ[1]));
        }
        Map<String, byte[]> 속성읽기(datà_Ọgụụ Ọgụụ_valuu) {
            Map<String, byte[]> 결과 = new LinkedHashMap<>();
            int 개수 = Ọgụụ_valuu.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                String njìama_akara_ahà = 문자(Ọgụụ_valuu.두바이트()); byte[] valuu = Ọgụụ_valuu.Wepụta_ọzi(Ọgụụ_valuu.네바이트());
                if (결과.put(njìama_akara_ahà, valuu) != null) throw new Ntụgharị_mmejọ("겹친 njìama_valuu: " + njìama_akara_ahà);
            }
            return 결과;
        }
        List<onyeòtù_datà> 멤버읽기(datà_Ọgụụ Ọgụụ_valuu) {
            List<onyeòtù_datà> 결과 = new ArrayList<>(); int 개수 = Ọgụụ_valuu.두바이트();
            for (int 순번 = 0; 순번 < 개수; 순번++) {
                int òhèrè_ndebà = Ọgụụ_valuu.두바이트(); String usoro_ndebà_akara_ahà = 문자(Ọgụụ_valuu.두바이트()), 서술 = 문자(Ọgụụ_valuu.두바이트());
                결과.add(new onyeòtù_datà(òhèrè_ndebà, usoro_ndebà_akara_ahà, 서술, 속성읽기(Ọgụụ_valuu)));
            }
            return 결과;
        }
    }
    static final class 함수형식 {
        final List<String> 인수 = new ArrayList<>();
        final String 반환;
        함수형식(String 서술) {
            if (!서술.startsWith("(")) throw new Ntụgharị_mmejọ("ọrụ_valuu 서술 mmejọ: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Ntụgharị_mmejọ("ọrụ_valuu 서술 mmejọ: " + 서술);
            인수.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (인수.contains("V") || 반환들.size() != 1) throw new Ntụgharị_mmejọ("ọrụ_valuu 서술 mmejọ: " + 서술);
            반환 = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> 결과 = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int 위치 = 0; 위치 < 서술.length();) {
            String ebenhọrọ_valuu = null;
            for (String hàzie_valuu : 허용형식) if (서술.startsWith(hàzie_valuu, 위치)) { ebenhọrọ_valuu = hàzie_valuu; break; }
            if (ebenhọrọ_valuu == null) throw new Ntụgharị_mmejọ("지원하지 않는 ụdịrị_datà: " + 서술);
            결과.add(ebenhọrọ_valuu); 위치 += ebenhọrọ_valuu.length();
        }
        return 결과;
    }
    static String adimara(String 종류, String... 부분들) {
        try {
            byte[] di_ike_ọbọakwụkwọ = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder SMS = new StringBuilder("j_" + 종류 + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) SMS.append(String.format(Locale.ROOT, "%02x", di_ike_ọbọakwụkwọ[순번] & 255));
            return SMS.toString();
        } catch (Exception mmejọ) { throw new Ntụgharị_mmejọ(mmejọ.toString()); }
    }
    final Map<String, klaàsị_datà> 클래스들 = new TreeMap<>();
    final Map<usoro_Nrụtụ_aka, onyeòtù_datà> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), 기계함수들 = new LinkedHashMap<>();
    final String 실행대상, ngwa_komputa_klaàsị;
    final int 동적기억낱말수;
    final Path njìàrụọrụ_ụzọ_ozi;
    기계어미리번역(List<Path> ụzọ_ozi_ndepụta, String ebenlereanya, int 낱말수, Path njìàrụọrụ_valuu) throws IOException {
        if ((!ebenlereanya.equals("kernel") && !ebenlereanya.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Ntụgharị_mmejọ("mee_nnyemiwu ebenlereanya 또는 memọrị_valuu 공간 Ụhara mmejọ");
        실행대상 = ebenlereanya; 동적기억낱말수 = 낱말수; njìàrụọrụ_ụzọ_ozi = njìàrụọrụ_valuu;
        // 이 이름도 국가별 ebensìbịa_èsèrèsè_osisi 생성 시 해당 언어로 옮긴다.
        ngwa_komputa_klaàsị = ebenlereanya.equals("kernel") ? "보드" : "òjìàrụ";
        for (String ahịrī : Files.readAllLines(njìàrụọrụ_valuu.resolve("기계함수.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = ahịrī.split("\t", -1);
            if (부분들.length != 4) throw new Ntụgharị_mmejọ("ngwa_komputa ọrụ_valuu datà mmejọ");
            if (부분들[0].equals(ebenlereanya)) 기계함수들.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path ụzọ_ozi : ụzọ_ozi_ndepụta) {
            klaàsị_datà datà = new klaàsị_datà(ụzọ_ozi);
            if (클래스들.put(datà.Aha, datà) != null) throw new Ntụgharị_mmejọ("중복 klaàsị_valuu: " + datà.Aha);
            for (onyeòtù_datà fild_valuu : datà.fild_valuu) {
                if ((fild_valuu.òhèrè_ndebà & 8) == 0 || 형식읽기(fild_valuu.서술).equals(Collections.singletonList("V"))) throw new Ntụgharị_mmejọ("adịmgbanwò_valuu 필드만 nkwado_valuu");
                if (필드들.put(new usoro_Nrụtụ_aka(datà.Aha, fild_valuu.Aha, fild_valuu.서술), fild_valuu) != null) throw new Ntụgharị_mmejọ("중복 fild_valuu");
            }
            for (onyeòtù_datà ọrụ_valuu : datà.ọrụ_valuu) {
                if (ọrụ_valuu.Aha.equals("<init>")) continue;
                if ((ọrụ_valuu.òhèrè_ndebà & 8) == 0 || (ọrụ_valuu.òhèrè_ndebà & (0x20 | 0x400)) != 0) throw new Ntụgharị_mmejọ("adịmgbanwò_valuu 비동기화 함수만 nkwado_valuu");
                new 함수형식(ọrụ_valuu.서술);
                if (함수들.put(new usoro_Nrụtụ_aka(datà.Aha, ọrụ_valuu.Aha, ọrụ_valuu.서술), ọrụ_valuu) != null) throw new Ntụgharị_mmejọ("중복 ọrụ_valuu");
            }
        }
    }
    String ùsòròokwū_adimara(String SMS) { return 문자열들.computeIfAbsent(SMS, valuu -> "j_text_" + 문자열들.size()); }
    String ihendịgide_njìekwu(klaàsị_datà datà, int indèks) {
        if (indèks < 1 || indèks >= datà.상수종류.length) throw new Ntụgharị_mmejọ("ihendịgide_valuu indèks ntipanye mmejọ");
        if (datà.상수종류[indèks] == 3) return "(word)(uint32_t)(" + datà.ihendịgide_datà[indèks] + ")";
        if (datà.상수종류[indèks] == 8) return "(word)" + ùsòròokwū_adimara(datà.문자((Integer)datà.ihendịgide_datà[indèks]));
        throw new Ntụgharị_mmejọ("정수와 ùsòròokwū_valuu 상수만 nkwado_valuu");
    }
    String 함수원형(usoro_Nrụtụ_aka Nrụtụ_aka) {
        List<String> 인수들 = new ArrayList<>(); int 개수 = new 함수형식(Nrụtụ_aka.서술).인수.size();
        for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("word a" + 순번);
        return "static word " + adimara("method", Nrụtụ_aka.부분들()) + "(" + (개수 == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void cheèk_otù_ebe(int indèks, int 지역변수수) { if (indèks < 0 || indèks >= 지역변수수) throw new Ntụgharị_mmejọ("otù_ebe_ọgba 변수 indèks ntipanye mmejọ"); }
    void 분기넣기(List<String> 출력, Set<Integer> ogbè_ndepụta, int 위치, int 이동량, String ọnọdụ) {
        int ebemwèga_valuu = 위치 + 이동량; ogbè_ndepụta.add(ebemwèga_valuu);
        출력.add((ọnọdụ == null ? "" : "if (" + ọnọdụ + ") ") + "goto b" + ebemwèga_valuu + ";");
    }
    String 함수본문(usoro_Nrụtụ_aka ọrụ_valuu, onyeòtù_datà datà) {
        byte[] 본문자료 = datà.njìama_valuu.get("Code"); if (본문자료 == null) throw new Ntụgharị_mmejọ("ọrụ_valuu 몸체가 없음: " + ọrụ_valuu.Aha);
        datà_Ọgụụ Ọgụụ_valuu = new datà_Ọgụụ(본문자료); int 쌓임깊이 = Ọgụụ_valuu.두바이트(), 지역변수수 = Ọgụụ_valuu.두바이트();
        datà_Ọgụụ nnyemiwu_datà = new datà_Ọgụụ(Ọgụụ_valuu.Wepụta_ọzi(Ọgụụ_valuu.네바이트()));
        if (Ọgụụ_valuu.두바이트() != 0) throw new Ntụgharị_mmejọ("try/catch/finally 미지원");
        함수형식 hàzie_valuu = new 함수형식(ọrụ_valuu.서술); if (지역변수수 < hàzie_valuu.인수.size()) throw new Ntụgharị_mmejọ("매개변수보다 적은 otù_ebe_ọgba 변수");
        klaàsị_datà klaàsị_valuu = 클래스들.get(ọrụ_valuu.nwe_valuu);
        List<String> 출력 = new ArrayList<>(); 출력.add(함수원형(ọrụ_valuu) + " {");
        출력.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(지역변수수, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < hàzie_valuu.인수.size(); 순번++) 출력.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), ogbè_ndepụta = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (nnyemiwu_datà.위치 < nnyemiwu_datà.datà.length) {
            int 위치 = nnyemiwu_datà.위치, Ntiiwu = nnyemiwu_datà.한바이트(); 경계들.add(위치); 출력.add("b" + 위치 + ":;");
            if (Ntiiwu == 0) continue;
            if (Ntiiwu == 1) 출력.add("PUSH(0);");
            else if (Ntiiwu >= 2 && Ntiiwu <= 8) 출력.add("PUSH((uint32_t)(" + (Ntiiwu - 3) + "));");
            else if (Ntiiwu == 16 || Ntiiwu == 17) 출력.add("PUSH((uint32_t)(" + (Ntiiwu == 16 ? nnyemiwu_datà.부호한바이트() : nnyemiwu_datà.부호두바이트()) + "));");
            else if (Ntiiwu == 18 || Ntiiwu == 19) 출력.add("PUSH(" + ihendịgide_njìekwu(klaàsị_valuu, Ntiiwu == 18 ? nnyemiwu_datà.한바이트() : nnyemiwu_datà.두바이트()) + ");");
            else if (Ntiiwu == 21 || Ntiiwu == 25 || (Ntiiwu >= 26 && Ntiiwu <= 29) || (Ntiiwu >= 42 && Ntiiwu <= 45)) {
                int indèks = Ntiiwu == 21 || Ntiiwu == 25 ? nnyemiwu_datà.한바이트() : Ntiiwu - (Ntiiwu <= 29 ? 26 : 42);
                cheèk_otù_ebe(indèks, 지역변수수); 출력.add("PUSH(l[" + indèks + "]);");
            } else if (Ntiiwu == 54 || Ntiiwu == 58 || (Ntiiwu >= 59 && Ntiiwu <= 62) || (Ntiiwu >= 75 && Ntiiwu <= 78)) {
                int indèks = Ntiiwu == 54 || Ntiiwu == 58 ? nnyemiwu_datà.한바이트() : Ntiiwu - (Ntiiwu <= 62 ? 59 : 75);
                cheèk_otù_ebe(indèks, 지역변수수); 출력.add("l[" + indèks + "] = POP();");
            } else if (Ntiiwu == 46) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (Ntiiwu == 79) 출력.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (Ntiiwu == 87 || Ntiiwu == 88) 출력.add(Ntiiwu == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (Ntiiwu >= 89 && Ntiiwu <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ùsòrò_ndepụta = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[Ntiiwu - 89]; 순번++) 출력.add("abcd".charAt(순번) + " = POP();");
                for (char valuu : ùsòrò_ndepụta[Ntiiwu - 89].toCharArray()) 출력.add("PUSH(" + valuu + ");");
            } else if (Ntiiwu == 96 || Ntiiwu == 100 || Ntiiwu == 104 || Ntiiwu == 126 || Ntiiwu == 128 || Ntiiwu == 130) {
                String àrụmọrụ_valuu = Ntiiwu == 96 ? "+" : Ntiiwu == 100 ? "-" : Ntiiwu == 104 ? "*" : Ntiiwu == 126 ? "&" : Ntiiwu == 128 ? "|" : "^";
                출력.add("b = POP(); a = POP(); PUSH((uint32_t)a " + àrụmọrụ_valuu + " (uint32_t)b);");
            } else if (Ntiiwu == 108 || Ntiiwu == 112) 출력.add("b = POP(); a = POP(); PUSH(divide(a,b," + (Ntiiwu == 112 ? 1 : 0) + "));");
            else if (Ntiiwu == 116) 출력.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (Ntiiwu == 120 || Ntiiwu == 122 || Ntiiwu == 124) {
                출력.add("b = POP(); a = POP();"); 출력.add("PUSH(" + (Ntiiwu == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (Ntiiwu == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (Ntiiwu == 132) {
                int indèks = nnyemiwu_datà.한바이트(), 증가량 = nnyemiwu_datà.부호한바이트(); cheèk_otù_ebe(indèks, 지역변수수);
                출력.add("l[" + indèks + "] = (uint32_t)l[" + indèks + "] + (uint32_t)(" + 증가량 + ");");
            } else if (Ntiiwu >= 145 && Ntiiwu <= 147) 출력.add("a = POP(); PUSH((uint32_t)(" + (Ntiiwu == 145 ? "int8_t" : Ntiiwu == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (Ntiiwu >= 153 && Ntiiwu <= 158) {
                출력.add("a = POP();"); 분기넣기(출력, ogbè_ndepụta, 위치, nnyemiwu_datà.부호두바이트(), "(int32_t)a " + 비교들[Ntiiwu - 153] + " 0");
            } else if (Ntiiwu >= 159 && Ntiiwu <= 166) {
                출력.add("b = POP(); a = POP();"); 분기넣기(출력, ogbè_ndepụta, 위치, nnyemiwu_datà.부호두바이트(), Ntiiwu >= 165 ? "a " + 비교들[Ntiiwu - 159] + " b" : "(int32_t)a " + 비교들[Ntiiwu - 159] + " (int32_t)b");
            } else if (Ntiiwu == 167 || Ntiiwu == 200) 분기넣기(출력, ogbè_ndepụta, 위치, Ntiiwu == 167 ? nnyemiwu_datà.부호두바이트() : nnyemiwu_datà.네바이트(), null);
            else if (Ntiiwu == 170 || Ntiiwu == 171) {
                while (nnyemiwu_datà.위치 % 4 != 0) nnyemiwu_datà.한바이트();
                int Ngwa_ihe_dịadị = nnyemiwu_datà.네바이트(); 출력.add("a = POP();");
                if (Ntiiwu == 170) {
                    int 아래 = nnyemiwu_datà.네바이트(), 위 = nnyemiwu_datà.네바이트(); long 개수 = (long)위 - 아래 + 1;
                    if (개수 < 1 || 개수 > (nnyemiwu_datà.datà.length - nnyemiwu_datà.위치) / 4) throw new Ntụgharị_mmejọ("switch ntipanye mmejọ");
                    for (long valuu = 아래; valuu <= 위; valuu++) 분기넣기(출력, ogbè_ndepụta, 위치, nnyemiwu_datà.네바이트(), "(int32_t)a == (" + valuu + ")");
                } else {
                    int 개수 = nnyemiwu_datà.네바이트(), 앞값 = 0;
                    if (개수 < 0 || 개수 > (nnyemiwu_datà.datà.length - nnyemiwu_datà.위치) / 8) throw new Ntụgharị_mmejọ("switch Ụhara mmejọ");
                    for (int 순번 = 0; 순번 < 개수; 순번++) {
                        int valuu = nnyemiwu_datà.네바이트(); if (순번 > 0 && valuu <= 앞값) throw new Ntụgharị_mmejọ("switch ùsòrò_valuu mmejọ"); 앞값 = valuu;
                        분기넣기(출력, ogbè_ndepụta, 위치, nnyemiwu_datà.네바이트(), "(int32_t)a == (" + valuu + ")");
                    }
                }
                분기넣기(출력, ogbè_ndepụta, 위치, Ngwa_ihe_dịadị, null);
            } else if (Ntiiwu == 172 || Ntiiwu == 176 || Ntiiwu == 177) 출력.add("return " + (Ntiiwu == 177 ? "0" : "POP()") + ";");
            else if (Ntiiwu == 178 || Ntiiwu == 179) {
                usoro_Nrụtụ_aka Nrụtụ_aka = klaàsị_valuu.Nrụtụ_aka(nnyemiwu_datà.두바이트()); if (!필드들.containsKey(Nrụtụ_aka)) throw new Ntụgharị_mmejọ("알 수 없는 fild_valuu");
                출력.add(adimara("init", Nrụtụ_aka.nwe_valuu) + "();"); String fild_valuu = adimara("field", Nrụtụ_aka.부분들());
                출력.add(Ntiiwu == 178 ? "PUSH(" + fild_valuu + ");" : fild_valuu + " = POP();");
            } else if (Ntiiwu == 184) {
                usoro_Nrụtụ_aka Nrụtụ_aka = klaàsị_valuu.Nrụtụ_aka(nnyemiwu_datà.두바이트()); if (!함수들.containsKey(Nrụtụ_aka)) throw new Ntụgharị_mmejọ("알 수 없는 ọrụ_valuu");
                함수형식 호출형식 = new 함수형식(Nrụtụ_aka.서술); int 개수 = 호출형식.인수.size();
                출력.add(adimara("init", Nrụtụ_aka.nwe_valuu) + "();"); 출력.add("if(sp < " + 개수 + ") kernel_panic(\"call stack underflow\"); sp -= " + 개수 + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < 개수; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                출력.add("a = " + adimara("method", Nrụtụ_aka.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.반환.equals("V")) 출력.add("PUSH(a);");
            } else if (Ntiiwu == 182) {
                usoro_Nrụtụ_aka Nrụtụ_aka = klaàsị_valuu.Nrụtụ_aka(nnyemiwu_datà.두바이트());
                if (Nrụtụ_aka.equals(new usoro_Nrụtụ_aka("java/lang/String", "length", "()I"))) 출력.add("a = POP(); PUSH(length(a));");
                else if (Nrụtụ_aka.equals(new usoro_Nrụtụ_aka("java/lang/String", "charAt", "(I)C"))) 출력.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Ntụgharị_mmejọ("가상 ọrụ_valuu 호출 미지원");
            } else if (Ntiiwu == 188) {
                if (nnyemiwu_datà.한바이트() != 10) throw new Ntụgharị_mmejọ("new int[]만 nkwado_valuu"); 출력.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (Ntiiwu == 190) 출력.add("a = POP(); PUSH(length(a));");
            else if (Ntiiwu == 196) {
                int mgbatị_valuu = nnyemiwu_datà.한바이트(), indèks = nnyemiwu_datà.두바이트(); cheèk_otù_ebe(indèks, 지역변수수);
                if (mgbatị_valuu == 21 || mgbatị_valuu == 25) 출력.add("PUSH(l[" + indèks + "]);");
                else if (mgbatị_valuu == 54 || mgbatị_valuu == 58) 출력.add("l[" + indèks + "] = POP();");
                else if (mgbatị_valuu == 132) 출력.add("l[" + indèks + "] = (uint32_t)l[" + indèks + "] + (uint32_t)(" + nnyemiwu_datà.부호두바이트() + ");");
                else throw new Ntụgharị_mmejọ("미지원 wide Ntiiwu");
            } else if (Ntiiwu == 198 || Ntiiwu == 199) {
                출력.add("a = POP();"); 분기넣기(출력, ogbè_ndepụta, 위치, nnyemiwu_datà.부호두바이트(), "a " + (Ntiiwu == 198 ? "==" : "!=") + " 0");
            } else throw new Ntụgharị_mmejọ(ọrụ_valuu.nwe_valuu + "." + ọrụ_valuu.Aha + ", baịtị_valuu " + 위치 + ": 미지원 Ntiiwu " + Ntiiwu);
        }
        if (!경계들.containsAll(ogbè_ndepụta)) throw new Ntụgharị_mmejọ("Ntiiwu 경계가 아닌 곳으로 ogbè");
        출력.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", 출력);
    }
    String zifè_usoro(String Njikọ_adimara, String ebenlereanya, boolean 진입점여부) {
        int 자리 = ebenlereanya.lastIndexOf('.'); if (자리 < 0 || !Njikọ_adimara.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Ntụgharị_mmejọ("내보내기 지정 mmejọ");
        String nwe_valuu = ebenlereanya.substring(0, 자리).replace('.', '/'), Aha = ebenlereanya.substring(자리 + 1); usoro_Nrụtụ_aka ebenhọrọ_valuu = null;
        for (usoro_Nrụtụ_aka Nrụtụ_aka : 함수들.keySet()) if (Nrụtụ_aka.nwe_valuu.equals(nwe_valuu) && Nrụtụ_aka.Aha.equals(Aha)) {
            if (ebenhọrọ_valuu != null) throw new Ntụgharị_mmejọ("겹친 내보내기 ebenlereanya"); ebenhọrọ_valuu = Nrụtụ_aka;
        }
        if (ebenhọrọ_valuu == null || (함수들.get(ebenhọrọ_valuu).òhèrè_ndebà & 0x100) != 0) throw new Ntụgharị_mmejọ("내보낼 함수가 없음 또는 native ọrụ_valuu");
        함수형식 hàzie_valuu = new 함수형식(ebenhọrọ_valuu.서술);
        if ((진입점여부 && !hàzie_valuu.인수.isEmpty()) || !Arrays.asList("V", "I").contains(hàzie_valuu.반환)) throw new Ntụgharị_mmejọ("ndebà_akara_valuu 또는 C 경계 hàzie_valuu mmejọ");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < hàzie_valuu.인수.size(); 순번++) {
            if (!hàzie_valuu.인수.get(순번).equals("I")) throw new Ntụgharị_mmejọ("C 경계는 int 인수만 nkwado_valuu");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (hàzie_valuu.반환.equals("V") ? "void " : "int32_t ") + Njikọ_adimara + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + adimara("init", ebenhọrọ_valuu.nwe_valuu) + "(); " + (hàzie_valuu.반환.equals("V") ? "" : "return (int32_t)") + adimara("method", ebenhọrọ_valuu.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String 생성(String ndebà_akara, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<usoro_Nrụtụ_aka, onyeòtù_datà> ndebà_valuu : 함수들.entrySet()) {
            usoro_Nrụtụ_aka Nrụtụ_aka = ndebà_valuu.getKey(); onyeòtù_datà datà = ndebà_valuu.getValue(); 선언들.add(함수원형(Nrụtụ_aka) + ";");
            if ((datà.òhèrè_ndebà & 0x100) != 0) {
                String Banye = 기계함수들.get(Nrụtụ_aka.Aha + Nrụtụ_aka.서술);
                if (!Nrụtụ_aka.nwe_valuu.equals(ngwa_komputa_klaàsị) || Banye == null) throw new Ntụgharị_mmejọ("허용되지 않은 native ọrụ_valuu: " + Nrụtụ_aka.Aha);
                int 개수 = new 함수형식(Nrụtụ_aka.서술).인수.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < 개수; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Banye + "(" + (개수 == 0 ? "void" : String.join(",", Collections.nCopies(개수, "word"))) + ");");
                몸체들.add(함수원형(Nrụtụ_aka) + " { return " + Banye + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(함수본문(Nrụtụ_aka, datà));
        }
        for (Map.Entry<usoro_Nrụtụ_aka, onyeòtù_datà> ndebà_valuu : 필드들.entrySet()) {
            usoro_Nrụtụ_aka Nrụtụ_aka = ndebà_valuu.getKey(); byte[] ihendịgide_valuu = ndebà_valuu.getValue().njìama_valuu.get("ConstantValue");
            String valuu = ihendịgide_valuu == null ? "0" : ihendịgide_njìekwu(클래스들.get(Nrụtụ_aka.nwe_valuu), new datà_Ọgụụ(ihendịgide_valuu).두바이트());
            필드선언들.add("static word " + adimara("field", Nrụtụ_aka.부분들()) + " = " + valuu + ";");
        }
        for (String Aha : 클래스들.keySet()) {
            String kwàdo_mmàlite = adimara("init", Aha), ọnọdụ_valuu = adimara("state", Aha);
            선언들.add("static void " + kwàdo_mmàlite + "(void);"); 필드선언들.add("static unsigned " + ọnọdụ_valuu + ";");
            usoro_Nrụtụ_aka Nrụtụ_aka = new usoro_Nrụtụ_aka(Aha, "<clinit>", "()V");
            몸체들.add("static void " + kwàdo_mmàlite + "(void) { if(" + ọnọdụ_valuu + ") return; " + ọnọdụ_valuu + " = 1; " + (함수들.containsKey(Nrụtụ_aka) ? adimara("method", Nrụtụ_aka.부분들()) + "(); " : "") + ọnọdụ_valuu + " = 2; }");
        }
        몸체들.add(zifè_usoro("java_entry", ndebà_akara, true)); Set<String> 공개이름 = new HashSet<>();
        for (String 지정 : 내보내기목록) {
            int 자리 = 지정.indexOf('='); if (자리 < 1) throw new Ntụgharị_mmejọ("내보내기 지정 mmejọ");
            String Aha = 지정.substring(0, 자리); 공개이름.add(Aha); 몸체들.add(zifè_usoro(Aha, 지정.substring(자리 + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> ndebà_valuu : 문자열들.entrySet()) {
            String SMS = ndebà_valuu.getKey(); StringBuilder MKPOKỌTA_valuu = new StringBuilder("static const word " + ndebà_valuu.getValue() + "[] = {" + SMS.length());
            for (int 순번 = 0; 순번 < SMS.length(); 순번++) MKPOKỌTA_valuu.append(", ").append((int)SMS.charAt(순번));
            문자열선언들.add(MKPOKỌTA_valuu.append("};").toString());
        }
        String nkwado_valuu = Files.readString(njìàrụọrụ_ụzọ_ozi.resolve("ọgịga_oge_otu_asụsụ_nkwado.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(동적기억낱말수));
        return 기계원문한국어화(nkwado_valuu + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String ebensìbịa, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> akara_ahà_tebùl = new HashMap<>();
        for (String ahịrī : Files.readAllLines(njìàrụọrụ_ụzọ_ozi.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] àbụọ_àbụọ_valuu = ahịrī.split("\t"); akara_ahà_tebùl.put(àbụọ_àbụọ_valuu[0], àbụọ_àbụọ_valuu[1]);
        }
        Pattern 토막식 = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = 토막식.matcher(ebensìbịa); StringBuffer 결과 = new StringBuffer();
        while (찾개.find()) {
            String Aha = 찾개.group(), 새이름 = Aha;
            if (!Aha.startsWith("//") && !Aha.startsWith("/*") && !Aha.startsWith("\"") && !Aha.startsWith("'") && !공개이름.contains(Aha)) {
                새이름 = akara_ahà_tebùl.getOrDefault(Aha, Aha);
                if (Aha.matches("a[0-9]+")) 새이름 = "인수" + Aha.substring(1);
                if (Aha.matches("b[0-9]+")) 새이름 = "ogbè" + Aha.substring(1);
                if (범용표기) {
                    StringBuilder 표기 = new StringBuilder();
                    for (char mkpụrụedemede_valuu : 새이름.toCharArray()) 표기.append(mkpụrụedemede_valuu < 128 ? Character.toString(mkpụrụedemede_valuu) : String.format(Locale.ROOT, "\\u%04x", (int)mkpụrụedemede_valuu));
                    새이름 = 표기.toString();
                }
            }
            찾개.appendReplacement(결과, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(결과); return 결과.toString();
    }
    String 엑스함수본문(usoro_Nrụtụ_aka ọrụ_valuu, onyeòtù_datà datà, Map<String,String> ngwa_komputa_tebùl, String ebenlereanya) {
        String 표식 = adimara("method", ọrụ_valuu.부분들());
        List<String> ahịrī = new ArrayList<>();
        if ((datà.òhèrè_ndebà & 0x100) != 0) {
            String Banye = ngwa_komputa_tebùl.get(ọrụ_valuu.Aha + ọrụ_valuu.서술);
            if (!ọrụ_valuu.nwe_valuu.equals(ebenlereanya.equals("kernel") ? "njìarụ_valuu" : "òjìàrụ") || Banye == null) throw new Ntụgharị_mmejọ("허용되지 않은 native ọrụ_valuu");
            return ".text\n" + 표식 + ":\njmp " + Banye;
        }
        byte[] àhụngwè = datà.njìama_valuu.get("Code"); if (àhụngwè == null) throw new Ntụgharị_mmejọ("ọrụ_valuu 몸체가 없음");
        datà_Ọgụụ Ọgụụ_valuu = new datà_Ọgụụ(àhụngwè); Ọgụụ_valuu.두바이트(); int 지역수 = Ọgụụ_valuu.두바이트();
        datà_Ọgụụ nnyemiwu_datà = new datà_Ọgụụ(Ọgụụ_valuu.Wepụta_ọzi(Ọgụụ_valuu.네바이트()));
        if (Ọgụụ_valuu.두바이트() != 0) throw new Ntụgharị_mmejọ("try/catch/finally 미지원");
        함수형식 hàzie_valuu = new 함수형식(ọrụ_valuu.서술); if (지역수 < hàzie_valuu.인수.size()) throw new Ntụgharị_mmejọ("매개변수보다 적은 otù_ebe_ọgba 변수");
        Collections.addAll(ahịrī,".text",".globl " + 표식,".type " + 표식 + ", @function",표식 + ":","pushl %ebp","movl %esp, %ebp","subl $" + 지역수 * 4 + ", %esp");
        for (int 순번 = 0; 순번 < hàzie_valuu.인수.size(); 순번++) Collections.addAll(ahịrī,"movl " + (8 + 4 * (hàzie_valuu.인수.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        klaàsị_datà klaàsị_valuu = 클래스들.get(ọrụ_valuu.nwe_valuu); Set<Integer> 경계들 = new HashSet<>(), ogbè_ndepụta = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (nnyemiwu_datà.위치 < nnyemiwu_datà.datà.length) {
            int 위치 = nnyemiwu_datà.위치, Ntiiwu = nnyemiwu_datà.한바이트(); String 자리 = 표식 + "_b" + 위치;
            ahịrī.add(자리 + ":"); 경계들.add(위치);
            if (Ntiiwu == 0) ahịrī.add("nop");
            else if (Ntiiwu == 1) ahịrī.add("pushl $0");
            else if (Ntiiwu >= 2 && Ntiiwu <= 8) ahịrī.add("pushl $" + (Ntiiwu - 3));
            else if (Ntiiwu == 16 || Ntiiwu == 17) ahịrī.add("pushl $" + (Ntiiwu == 16 ? nnyemiwu_datà.부호한바이트() : nnyemiwu_datà.부호두바이트()));
            else if (Ntiiwu == 18 || Ntiiwu == 19) {
                int indèks = Ntiiwu == 18 ? nnyemiwu_datà.한바이트() : nnyemiwu_datà.두바이트();
                ahịrī.add("pushl $" + 엑스상수(klaàsị_valuu,indèks));
            } else if (Ntiiwu == 21 || Ntiiwu == 25 || (Ntiiwu >= 26 && Ntiiwu <= 29) || (Ntiiwu >= 42 && Ntiiwu <= 45) || Ntiiwu == 54 || Ntiiwu == 58 || (Ntiiwu >= 59 && Ntiiwu <= 62) || (Ntiiwu >= 75 && Ntiiwu <= 78)) {
                boolean 읽음 = Ntiiwu < 54; int indèks = Ntiiwu == 21 || Ntiiwu == 25 || Ntiiwu == 54 || Ntiiwu == 58 ? nnyemiwu_datà.한바이트() : Ntiiwu - (Ntiiwu <= 29 ? 26 : Ntiiwu <= 45 ? 42 : Ntiiwu <= 62 ? 59 : 75);
                cheèk_otù_ebe(indèks,지역수); ahịrī.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (indèks + 1)) + "(%ebp)");
            } else if (Ntiiwu == 46) Collections.addAll(ahịrī,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (Ntiiwu == 79) Collections.addAll(ahịrī,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (Ntiiwu == 87 || Ntiiwu == 88) ahịrī.add("addl $" + (Ntiiwu == 87 ? 4 : 8) + ", %esp");
            else if (Ntiiwu >= 89 && Ntiiwu <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ùsòrò_ndepụta = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[Ntiiwu - 89]; 순번++) ahịrī.add("popl " + 저장기들[순번]);
                for (int 순번 : ùsòrò_ndepụta[Ntiiwu - 89]) ahịrī.add("pushl " + 저장기들[순번]);
            } else if (Ntiiwu == 96 || Ntiiwu == 100 || Ntiiwu == 104 || Ntiiwu == 126 || Ntiiwu == 128 || Ntiiwu == 130) {
                String àrụmọrụ_valuu = Ntiiwu == 96 ? "addl" : Ntiiwu == 100 ? "subl" : Ntiiwu == 104 ? "imull" : Ntiiwu == 126 ? "andl" : Ntiiwu == 128 ? "orl" : "xorl";
                Collections.addAll(ahịrī,"popl %ecx","popl %eax",àrụmọrụ_valuu + " %ecx, %eax","pushl %eax");
            } else if (Ntiiwu == 108 || Ntiiwu == 112) Collections.addAll(ahịrī,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + 자리 + "_divide","cmpl $0x80000000, %eax","jne " + 자리 + "_divide","xorl %edx, %edx","jmp " + 자리 + "_done",자리 + "_divide:","cltd","idivl %ecx",자리 + "_done:","pushl " + (Ntiiwu == 108 ? "%eax" : "%edx"));
            else if (Ntiiwu == 116) ahịrī.add("negl (%esp)");
            else if (Ntiiwu == 120 || Ntiiwu == 122 || Ntiiwu == 124) Collections.addAll(ahịrī,"popl %ecx","popl %eax",(Ntiiwu == 120 ? "sall" : Ntiiwu == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (Ntiiwu == 132) {
                int indèks = nnyemiwu_datà.한바이트(), 증가 = nnyemiwu_datà.부호한바이트(); cheèk_otù_ebe(indèks,지역수); ahịrī.add("addl $" + 증가 + ", -" + (4 * (indèks + 1)) + "(%ebp)");
            } else if (Ntiiwu >= 145 && Ntiiwu <= 147) Collections.addAll(ahịrī,"popl %eax",Ntiiwu == 145 ? "movsbl %al, %eax" : Ntiiwu == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (Ntiiwu >= 153 && Ntiiwu <= 166) {
                if (Ntiiwu <= 158) Collections.addAll(ahịrī,"popl %eax","testl %eax, %eax");
                else Collections.addAll(ahịrī,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int ebemwèga_valuu = 위치 + nnyemiwu_datà.부호두바이트(); ogbè_ndepụta.add(ebemwèga_valuu); ahịrī.add(비교들[Ntiiwu - (Ntiiwu <= 158 ? 153 : 159)] + " " + 표식 + "_b" + ebemwèga_valuu);
            } else if (Ntiiwu == 167 || Ntiiwu == 200) {
                int ebemwèga_valuu = 위치 + (Ntiiwu == 167 ? nnyemiwu_datà.부호두바이트() : nnyemiwu_datà.네바이트()); ogbè_ndepụta.add(ebemwèga_valuu); ahịrī.add("jmp " + 표식 + "_b" + ebemwèga_valuu);
            } else if (Ntiiwu == 170 || Ntiiwu == 171) {
                while (nnyemiwu_datà.위치 % 4 != 0) nnyemiwu_datà.한바이트();
                int Ngwa_ihe_dịadị = 위치 + nnyemiwu_datà.네바이트(); ogbè_ndepụta.add(Ngwa_ihe_dịadị); ahịrī.add("popl %eax");
                int 개수, 아래 = 0;
                if (Ntiiwu == 170) { 아래 = nnyemiwu_datà.네바이트(); int 위 = nnyemiwu_datà.네바이트(); long ogologo_valuu = (long)위 - 아래 + 1; if (ogologo_valuu < 1 || ogologo_valuu > (nnyemiwu_datà.datà.length - nnyemiwu_datà.위치) / 4) throw new Ntụgharị_mmejọ("switch ntipanye mmejọ"); 개수 = (int)ogologo_valuu; }
                else { 개수 = nnyemiwu_datà.네바이트(); if (개수 < 0 || 개수 > (nnyemiwu_datà.datà.length - nnyemiwu_datà.위치) / 8) throw new Ntụgharị_mmejọ("switch Ụhara mmejọ"); }
                for (int 순번 = 0; 순번 < 개수; 순번++) {
                    int valuu = Ntiiwu == 170 ? 아래 + 순번 : nnyemiwu_datà.네바이트(), ebemwèga_valuu = 위치 + nnyemiwu_datà.네바이트(); ogbè_ndepụta.add(ebemwèga_valuu);
                    Collections.addAll(ahịrī,"cmpl $" + valuu + ", %eax","je " + 표식 + "_b" + ebemwèga_valuu);
                }
                ahịrī.add("jmp " + 표식 + "_b" + Ngwa_ihe_dịadị);
            } else if (Ntiiwu == 172 || Ntiiwu == 176 || Ntiiwu == 177) {
                if (Ntiiwu != 177) ahịrī.add("popl %eax"); Collections.addAll(ahịrī,"leave","ret");
            } else if (Ntiiwu == 178 || Ntiiwu == 179) {
                usoro_Nrụtụ_aka Nrụtụ_aka = klaàsị_valuu.Nrụtụ_aka(nnyemiwu_datà.두바이트()); if (!필드들.containsKey(Nrụtụ_aka)) throw new Ntụgharị_mmejọ("알 수 없는 fild_valuu");
                Collections.addAll(ahịrī,"call " + adimara("init",Nrụtụ_aka.nwe_valuu),(Ntiiwu == 178 ? "pushl " : "popl ") + adimara("field",Nrụtụ_aka.부분들()));
            } else if (Ntiiwu == 184) {
                usoro_Nrụtụ_aka Nrụtụ_aka = klaàsị_valuu.Nrụtụ_aka(nnyemiwu_datà.두바이트()); if (!함수들.containsKey(Nrụtụ_aka)) throw new Ntụgharị_mmejọ("알 수 없는 ọrụ_valuu");
                함수형식 호출형식 = new 함수형식(Nrụtụ_aka.서술); Collections.addAll(ahịrī,"call " + adimara("init",Nrụtụ_aka.nwe_valuu),"call " + adimara("method",Nrụtụ_aka.부분들()));
                if (!호출형식.인수.isEmpty()) ahịrī.add("addl $" + 호출형식.인수.size() * 4 + ", %esp");
                if (!호출형식.반환.equals("V")) ahịrī.add("pushl %eax");
            } else if (Ntiiwu == 182) {
                usoro_Nrụtụ_aka Nrụtụ_aka = klaàsị_valuu.Nrụtụ_aka(nnyemiwu_datà.두바이트());
                if (Nrụtụ_aka.equals(new usoro_Nrụtụ_aka("java/lang/String","length","()I"))) Collections.addAll(ahịrī,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (Nrụtụ_aka.equals(new usoro_Nrụtụ_aka("java/lang/String","charAt","(I)C"))) Collections.addAll(ahịrī,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Ntụgharị_mmejọ("가상 ọrụ_valuu 호출 미지원");
            } else if (Ntiiwu == 188) {
                if (nnyemiwu_datà.한바이트() != 10) throw new Ntụgharị_mmejọ("new int[]만 nkwado_valuu"); Collections.addAll(ahịrī,"popl %eax","call rt_new_array","pushl %eax");
            } else if (Ntiiwu == 190) Collections.addAll(ahịrī,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (Ntiiwu == 196) {
                int mgbatị_valuu = nnyemiwu_datà.한바이트(), indèks = nnyemiwu_datà.두바이트(); cheèk_otù_ebe(indèks,지역수);
                if (mgbatị_valuu == 21 || mgbatị_valuu == 25 || mgbatị_valuu == 54 || mgbatị_valuu == 58) ahịrī.add((mgbatị_valuu <= 25 ? "pushl " : "popl ") + "-" + 4 * (indèks + 1) + "(%ebp)");
                else if (mgbatị_valuu == 132) ahịrī.add("addl $" + nnyemiwu_datà.부호두바이트() + ", -" + 4 * (indèks + 1) + "(%ebp)");
                else throw new Ntụgharị_mmejọ("wide Ntiiwu 미지원");
            } else if (Ntiiwu == 198 || Ntiiwu == 199) {
                int ebemwèga_valuu = 위치 + nnyemiwu_datà.부호두바이트(); ogbè_ndepụta.add(ebemwèga_valuu); Collections.addAll(ahịrī,"popl %eax","testl %eax, %eax",(Ntiiwu == 198 ? "je " : "jne ") + 표식 + "_b" + ebemwèga_valuu);
            } else throw new Ntụgharị_mmejọ("미지원 Ntiiwu: " + Ntiiwu);
        }
        if (!경계들.containsAll(ogbè_ndepụta)) throw new Ntụgharị_mmejọ("Ntiiwu 경계가 아닌 곳으로 ogbè");
        ahịrī.add(".size " + 표식 + ", .-" + 표식); return String.join("\n",ahịrī);
    }
    String 엑스상수(klaàsị_datà datà, int indèks) {
        if (datà.상수종류[indèks] == 3) return datà.ihendịgide_datà[indèks].toString();
        if (datà.상수종류[indèks] == 8) return ùsòròokwū_adimara(datà.문자((Integer)datà.ihendịgide_datà[indèks]));
        throw new Ntụgharị_mmejọ("정수와 ùsòròokwū_valuu 상수만 nkwado_valuu");
    }
    String 엑스조립본(String ndebà_akara, List<String> 내보냄, String ebenlereanya) throws IOException {
        Map<String,String> ngwa_komputa_tebùl = new HashMap<>();
        for (String ahịrī : Files.readAllLines(njìàrụọrụ_ụzọ_ozi.resolve("엑스기계함수.tsv"))) { String[] àbụọ_àbụọ_valuu = ahịrī.split("\t"); if (àbụọ_àbụọ_valuu[0].equals(ebenlereanya)) ngwa_komputa_tebùl.put(àbụọ_àbụọ_valuu[1] + àbụọ_àbụọ_valuu[2],àbụọ_àbụọ_valuu[3]); }
        int 자리 = ndebà_akara.lastIndexOf('.'); if (자리 < 0) throw new Ntụgharị_mmejọ("ndebà_akara 지정 mmejọ");
        String nwe_valuu = ndebà_akara.substring(0,자리).replace('.','/'), usoro_ndebà_akara_ahà = ndebà_akara.substring(자리 + 1); usoro_Nrụtụ_aka ndebà_akara_valuu = null;
        for (String 서술 : Arrays.asList("()I","()V")) { usoro_Nrụtụ_aka Nrụtụ_aka = new usoro_Nrụtụ_aka(nwe_valuu,usoro_ndebà_akara_ahà,서술); if (함수들.containsKey(Nrụtụ_aka)) { if (ndebà_akara_valuu != null) throw new Ntụgharị_mmejọ("겹친 ndebà_akara"); ndebà_akara_valuu = Nrụtụ_aka; } }
        if (ndebà_akara_valuu == null || (함수들.get(ndebà_akara_valuu).òhèrè_ndebà & 0x100) != 0) throw new Ntụgharị_mmejọ("ndebà_akara_valuu ọrụ_valuu hàzie_valuu mmejọ");
        List<String> ahịrī = new ArrayList<>(); ahịrī.add(".code32");
        for (klaàsị_datà datà : 클래스들.values()) {
            String ọnọdụ_valuu = adimara("state",datà.Aha), kwàdo_mmàlite = adimara("init",datà.Aha);
            Collections.addAll(ahịrī,".bss",".balign 4",ọnọdụ_valuu + ": .long 0",".text",kwàdo_mmàlite + ":","cmpl $0, " + ọnọdụ_valuu,"jne " + kwàdo_mmàlite + "_done","movl $1, " + ọnọdụ_valuu);
            usoro_Nrụtụ_aka 초기화참조 = new usoro_Nrụtụ_aka(datà.Aha,"<clinit>","()V"); if (함수들.containsKey(초기화참조)) ahịrī.add("call " + adimara("method",초기화참조.부분들()));
            Collections.addAll(ahịrī,"movl $2, " + ọnọdụ_valuu,kwàdo_mmàlite + "_done:","ret");
            for (onyeòtù_datà fild_valuu : datà.fild_valuu) {
                byte[] ihendịgide_valuu = fild_valuu.njìama_valuu.get("ConstantValue"); String valuu = ihendịgide_valuu == null ? "0" : 엑스상수(datà,new datà_Ọgụụ(ihendịgide_valuu).두바이트());
                Collections.addAll(ahịrī,".data",".balign 4",adimara("field",datà.Aha,fild_valuu.Aha,fild_valuu.서술) + ": .long " + valuu);
            }
            for (onyeòtù_datà ọrụ_valuu : datà.ọrụ_valuu) if (!ọrụ_valuu.Aha.equals("<init>")) ahịrī.add(엑스함수본문(new usoro_Nrụtụ_aka(datà.Aha,ọrụ_valuu.Aha,ọrụ_valuu.서술),ọrụ_valuu,ngwa_komputa_tebùl,ebenlereanya));
        }
        Collections.addAll(ahịrī,".text",".globl java_entry","java_entry:","call " + adimara("init",ndebà_akara_valuu.nwe_valuu),"call " + adimara("method",ndebà_akara_valuu.부분들()));
        if (ndebà_akara_valuu.서술.equals("()V")) ahịrī.add("xorl %eax, %eax"); ahịrī.add("ret");
        for (String 지정 : 내보냄) {
            int nzinjedebe_valuu = 지정.indexOf('='); if (nzinjedebe_valuu < 1) throw new Ntụgharị_mmejọ("내보내기 지정 mmejọ");
            String 외부 = 지정.substring(0,nzinjedebe_valuu), ọrụ_valuu = 지정.substring(nzinjedebe_valuu + 1); int 나눔 = ọrụ_valuu.lastIndexOf('.');
            if (나눔 < 0 || !외부.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Ntụgharị_mmejọ("내보내기 adimara mmejọ");
            String klaàsị_valuu = ọrụ_valuu.substring(0,나눔).replace('.','/'), Aha = ọrụ_valuu.substring(나눔 + 1); usoro_Nrụtụ_aka ebenhọrọ_valuu = null;
            for (usoro_Nrụtụ_aka Nrụtụ_aka : 함수들.keySet()) if (Nrụtụ_aka.nwe_valuu.equals(klaàsị_valuu) && Nrụtụ_aka.Aha.equals(Aha)) { if (ebenhọrọ_valuu != null) throw new Ntụgharị_mmejọ("겹친 내보내기 ebenlereanya"); ebenhọrọ_valuu = Nrụtụ_aka; }
            if (ebenhọrọ_valuu == null) throw new Ntụgharị_mmejọ("내보낼 함수가 없음");
            Collections.addAll(ahịrī,".text",".globl " + 외부,외부 + ":","call " + adimara("init",ebenhọrọ_valuu.nwe_valuu),"jmp " + adimara("method",ebenhọrọ_valuu.부분들()));
        }
        ahịrī.add(".section .rodata");
        for (Map.Entry<String,String> ndebà_valuu : 문자열들.entrySet()) {
            Collections.addAll(ahịrī,".balign 4",ndebà_valuu.getValue() + ":",".long " + ndebà_valuu.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char ihe_ọmụmụ_valuu : ndebà_valuu.getKey().toCharArray()) 단위들.add(Integer.toString(ihe_ọmụmụ_valuu)); if (!단위들.isEmpty()) ahịrī.add(".long " + String.join(",",단위들));
        }
        ahịrī.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",ahịrī) + "\n";
    }
    static void mee_ngwaọrụ(List<String> Ntiiwu) throws Exception {
        if (new ProcessBuilder(Ntiiwu).inheritIO().start().waitFor() != 0) throw new Ntụgharị_mmejọ("wue_ebensìbịa mmejọ: " + Ntiiwu.get(0));
    }
    static String datà_ùsòròokwū(String SMS) { return "\"" + SMS.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void 엑스번역(List<Path> 입력들, String ebenlereanya, String ndebà_akara, List<String> 내보냄, Path 출력, Path njìàrụọrụ_valuu) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), klaàsị_ụzọ_ozi = 임시.resolve("classes"); Files.createDirectory(klaàsị_ụzọ_ozi);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",klaàsị_ụzọ_ozi.toString(),"-sourcepath",klaàsị_ụzọ_ozi.toString(),"-d",klaàsị_ụzọ_ozi.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int 원문수 = 0;
            for (Path 입력 : 입력들) {
                if (출력.toAbsolutePath().normalize().equals(입력.toAbsolutePath().normalize())) throw new Ntụgharị_mmejọ("출력 파일과 입력이 같음");
                if (입력.toString().endsWith(".java")) { 자바명령.add(입력.toString()); 원문수++; }
                else if (입력.toString().endsWith(".class")) 바이트코드.add(입력);
                else throw new Ntụgharị_mmejọ(".java 또는 .class만 nkwado_valuu");
            }
            if (원문수 > 0) mee_ngwaọrụ(자바명령);
            try (java.util.stream.Stream<Path> ụzọ_ozi_ndepụta = Files.walk(klaàsị_ụzọ_ozi)) { ụzọ_ozi_ndepụta.filter(ụzọ_ozi -> ụzọ_ozi.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 변환 = new 기계어미리번역(바이트코드,ebenlereanya.equals("user") ? "user" : "kernel",262144,njìàrụọrụ_valuu);
            String 조립 = 변환.엑스조립본(ndebà_akara,내보냄,ebenlereanya); Files.writeString(임시.resolve("program.s"),조립,StandardCharsets.UTF_8);
            Path 도구위치 = njìàrụọrụ_valuu.getParent();
            mee_ngwaọrụ(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            mee_ngwaọrụ(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),도구위치.resolve("ọgịga_oge_otu_asụsụ_nkwado.s").toString()));
            List<String> Banye = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (ebenlereanya.equals("kernel")) Banye.add("-r");
            else {
                mee_ngwaọrụ(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),도구위치.resolve(ebenlereanya.equals("user") ? "Mbido_òjìàrụ_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(Banye,"-e","_start",임시.resolve("start.o").toString());
                if (ebenlereanya.equals("user")) Collections.addAll(Banye,"-T",도구위치.resolve("òjìàrụ_Njikọ_Nhàzi.ld").toString());
            }
            Collections.addAll(Banye,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); mee_ngwaọrụ(Banye);
            출력 = 출력.toAbsolutePath(); Files.createDirectories(출력.getParent()); Path detuo_valuu = Files.createTempFile(출력.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),detuo_valuu,StandardCopyOption.REPLACE_EXISTING); Files.move(detuo_valuu,출력,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(detuo_valuu); }
            Files.setPosixFilePermissions(출력,java.nio.file.attribute.PosixFilePermissions.fromString(ebenlereanya.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(출력 + ".s"),조립,StandardCharsets.UTF_8);
            List<String> adimara_datà = new ArrayList<>(), data_ǹsìrìwèta = new ArrayList<>();
            for (usoro_Nrụtụ_aka Nrụtụ_aka : 변환.함수들.keySet()) adimara_datà.add(datà_ùsòròokwū(adimara("method",Nrụtụ_aka.부분들())) + ":" + datà_ùsòròokwū(Nrụtụ_aka.nwe_valuu + "." + Nrụtụ_aka.Aha + Nrụtụ_aka.서술));
            for (Path 입력 : 입력들) {
                byte[] di_ike_ọbọakwụkwọ = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(입력)); StringBuilder SMS = new StringBuilder(); for (byte valuu : di_ike_ọbọakwụkwọ) SMS.append(String.format(Locale.ROOT,"%02x",valuu & 255));
                data_ǹsìrìwèta.add(datà_ùsòròokwū(입력.toAbsolutePath().toString()) + ":" + datà_ùsòròokwū(SMS.toString()));
            }
            Files.writeString(Paths.get(출력 + ".json"),"{\"target\":" + datà_ùsòròokwū(ebenlereanya) + ",\"entry\":" + datà_ùsòròokwū(ndebà_akara) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",adimara_datà) + "},\"sources\":{" + String.join(",",data_ǹsìrìwèta) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> ụzọ_ozi_ndepụta = Files.walk(임시)) { for (Path ụzọ_ozi : (Iterable<Path>)ụzọ_ozi_ndepụta.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(ụzọ_ozi); }
        }
    }
    public static void main(String[] 인수) {
        try {
            String ndebà_akara = null, ebenlereanya = "kernel", 엑스대상 = null; Path 출력경로 = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> ụzọ_ozi_ndepụta = new ArrayList<>();
            for (int 순번 = 0; 순번 < 인수.length; 순번++) {
                String valuu = 인수[순번];
                switch (valuu) {
                    case "--target": 엑스대상 = 인수[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry klaàsị_valuu.ọrụ_valuu -o 출력 [--target linux|kernel|user] [--profile kernel|user] [--export adimara=klaàsị_valuu.ọrụ_valuu] 클래스파일 또는 Java원문"); return;
                    case "--entry": ndebà_akara = 인수[++순번]; break;
                    case "--profile": ebenlereanya = 인수[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(인수[++순번]); break;
                    case "--export": 내보냄.add(인수[++순번]); break;
                    case "-o": 출력경로 = Paths.get(인수[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (valuu.startsWith("-")) throw new Ntụgharị_mmejọ("알 수 없는 옵션: " + valuu); ụzọ_ozi_ndepụta.add(Paths.get(valuu));
                }
            }
            if (ndebà_akara == null || 출력경로 == null || ụzọ_ozi_ndepụta.isEmpty()) throw new Ntụgharị_mmejọ("--entry, -o, klaàsị_valuu 파일이 필요합니다");
            Path njìàrụọrụ_valuu = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (엑스대상 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(엑스대상)) throw new Ntụgharị_mmejọ("알 수 없는 mee_nnyemiwu ebenlereanya");
                엑스번역(ụzọ_ozi_ndepụta,엑스대상,ndebà_akara,내보냄,출력경로,njìàrụọrụ_valuu); return;
            }
            String ebensìbịa = new 기계어미리번역(ụzọ_ozi_ndepụta, ebenlereanya, 낱말수, njìàrụọrụ_valuu).생성(ndebà_akara, 내보냄, 범용표기);
            출력경로 = 출력경로.toAbsolutePath(); Files.createDirectories(출력경로.getParent());
            Path 임시 = Files.createTempFile(출력경로.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, ebensìbịa, StandardCharsets.UTF_8); Files.move(임시, 출력경로, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception mmejọ) { System.err.println("wue_ebensìbịa mmejọ: " + mmejọ.getMessage()); System.exit(1); }
    }
}
