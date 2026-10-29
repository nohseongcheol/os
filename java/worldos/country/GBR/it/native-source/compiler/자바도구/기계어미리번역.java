// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Java Corso_VALORE 파일에서 독립 ARM64 커널용 C 원문을 만든다. host JDK에서 실행한다. */
public final class 기계어미리번역 {
    static final class Traduzione_errore extends RuntimeException {
        Traduzione_errore(String 설명) { super(설명); }
    }
    static final class dati_Lettore {
        final byte[] dati;
        int posizione;
        dati_Lettore(byte[] input_dati) { dati = input_dati; }
        byte[] Lettura(int durata_VALORE) {
            if (durata_VALORE < 0 || durata_VALORE > dati.length - posizione) throw new Traduzione_errore("잘린 Corso_VALORE 또는 comando dati");
            byte[] risultato = Arrays.copyOfRange(dati, posizione, posizione + durata_VALORE); posizione += durata_VALORE; return risultato;
        }
        int 한바이트() { if (posizione >= dati.length) throw new Traduzione_errore("잘린 comando dati"); return dati[posizione++] & 255; }
        int 두바이트() { return (한바이트() << 8) | 한바이트(); }
        int 네바이트() { return (두바이트() << 16) | 두바이트(); }
        int 부호한바이트() { return (byte) 한바이트(); }
        int 부호두바이트() { return (short) 두바이트(); }
    }
    static final class membro_dati {
        final int accesso_voce;
        final String Nome, 서술;
        final Map<String, byte[]> valore_dell_attributo;
        membro_dati(int accesso_VALORE, String nome_VALORE, String descrittore_dati, Map<String, byte[]> attributo_dati) {
            accesso_voce = accesso_VALORE; Nome = nome_VALORE; 서술 = descrittore_dati; valore_dell_attributo = attributo_dati;
        }
    }
    static final class metodo_fonti implements Comparable<metodo_fonti> {
        final String proprietario_VALORE, Nome, 서술;
        metodo_fonti(String 소유값, String nome_VALORE, String descrittore_dati) { proprietario_VALORE = 소유값; Nome = nome_VALORE; 서술 = descrittore_dati; }
        String[] 부분들() { return new String[]{proprietario_VALORE, Nome, 서술}; }
        public int compareTo(metodo_fonti peer_VALORE) {
            int Confronto_VALORE = proprietario_VALORE.compareTo(peer_VALORE.proprietario_VALORE);
            if (Confronto_VALORE == 0) Confronto_VALORE = Nome.compareTo(peer_VALORE.Nome);
            return Confronto_VALORE == 0 ? 서술.compareTo(peer_VALORE.서술) : Confronto_VALORE;
        }
        public boolean equals(Object peer_VALORE) { return peer_VALORE instanceof metodo_fonti && compareTo((metodo_fonti) peer_VALORE) == 0; }
        public int hashCode() { return Objects.hash(proprietario_VALORE, Nome, 서술); }
    }
    static final class Corso_dati {
        final int[] costante_Kind;
        final Object[] costante_dati;
        final String Nome;
        final List<membro_dati> valore_del_campo, FUNZIONE_VALORE;
        Corso_dati(Path percorso) throws IOException {
            dati_Lettore Lettore_VALORE = new dati_Lettore(Files.readAllBytes(percorso));
            if (Lettore_VALORE.네바이트() != 0xcafebabe) throw new Traduzione_errore("Java Corso_VALORE 표식이 아님");
            Lettore_VALORE.Lettura(4);
            int articolo_CONTA_NUMERI = Lettore_VALORE.두바이트(); costante_Kind = new int[articolo_CONTA_NUMERI]; costante_dati = new Object[articolo_CONTA_NUMERI];
            for (int 순번 = 1; 순번 < articolo_CONTA_NUMERI; 순번++) {
                int Kind_VALORE = Lettore_VALORE.한바이트(); costante_Kind[순번] = Kind_VALORE;
                switch (Kind_VALORE) {
                    case 1:
                        int durata_VALORE = Lettore_VALORE.두바이트();
                        byte[] carattere_buffer = Lettore_VALORE.Lettura(durata_VALORE), 길이붙인자료 = new byte[durata_VALORE + 2];
                        길이붙인자료[0] = (byte)(durata_VALORE >> 8); 길이붙인자료[1] = (byte)durata_VALORE;
                        System.arraycopy(carattere_buffer, 0, 길이붙인자료, 2, durata_VALORE);
                        costante_dati[순번] = new DataInputStream(new ByteArrayInputStream(길이붙인자료)).readUTF(); break;
                    case 3: costante_dati[순번] = Lettore_VALORE.네바이트(); break;
                    case 4: Lettore_VALORE.Lettura(4); break;
                    case 5: case 6: Lettore_VALORE.Lettura(8); 순번++; break;
                    case 7: case 8: case 16: costante_dati[순번] = Lettore_VALORE.두바이트(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        costante_dati[순번] = new int[]{Lettore_VALORE.두바이트(), Lettore_VALORE.두바이트()}; break;
                    case 15: costante_dati[순번] = new int[]{Lettore_VALORE.한바이트(), Lettore_VALORE.두바이트()}; break;
                    default: throw new Traduzione_errore("지원하지 않는 costante_VALORE Kind_VALORE: " + Kind_VALORE);
                }
            }
            Lettore_VALORE.두바이트(); Nome = nome_della_classe(Lettore_VALORE.두바이트());
            if (!nome_della_classe(Lettore_VALORE.두바이트()).equals("java/lang/Object") || Lettore_VALORE.두바이트() != 0)
                throw new Traduzione_errore(Nome + ": 상속 및 인터페이스 미지원");
            valore_del_campo = 멤버읽기(Lettore_VALORE); FUNZIONE_VALORE = 멤버읽기(Lettore_VALORE); 속성읽기(Lettore_VALORE);
            if (Lettore_VALORE.posizione != Lettore_VALORE.dati.length) throw new Traduzione_errore("Corso_VALORE 뒤에 남은 dati");
        }
        String 문자(int INDICE) {
            if (INDICE < 1 || INDICE >= costante_Kind.length || costante_Kind[INDICE] != 1) throw new Traduzione_errore("문자 costante_VALORE INDICE errore");
            return (String) costante_dati[INDICE];
        }
        String nome_della_classe(int INDICE) {
            if (INDICE < 1 || INDICE >= costante_Kind.length || costante_Kind[INDICE] != 7) throw new Traduzione_errore("Corso_VALORE fonti errore");
            return 문자((Integer)costante_dati[INDICE]);
        }
        metodo_fonti fonti(int INDICE) {
            if (INDICE < 1 || INDICE >= costante_Kind.length || costante_Kind[INDICE] < 9 || costante_Kind[INDICE] > 11) throw new Traduzione_errore("멤버 fonti errore");
            int[] associare_VALORE = (int[])costante_dati[INDICE], nome_associare = (int[])costante_dati[associare_VALORE[1]];
            return new metodo_fonti(nome_della_classe(associare_VALORE[0]), 문자(nome_associare[0]), 문자(nome_associare[1]));
        }
        Map<String, byte[]> 속성읽기(dati_Lettore Lettore_VALORE) {
            Map<String, byte[]> risultato = new LinkedHashMap<>();
            int articolo_CONTA_NUMERI = Lettore_VALORE.두바이트();
            for (int 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) {
                String attributo_nome = 문자(Lettore_VALORE.두바이트()); byte[] VALORE = Lettore_VALORE.Lettura(Lettore_VALORE.네바이트());
                if (risultato.put(attributo_nome, VALORE) != null) throw new Traduzione_errore("겹친 valore_dell_attributo: " + attributo_nome);
            }
            return risultato;
        }
        List<membro_dati> 멤버읽기(dati_Lettore Lettore_VALORE) {
            List<membro_dati> risultato = new ArrayList<>(); int articolo_CONTA_NUMERI = Lettore_VALORE.두바이트();
            for (int 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) {
                int accesso_voce = Lettore_VALORE.두바이트(); String metodo_voce_nome = 문자(Lettore_VALORE.두바이트()), 서술 = 문자(Lettore_VALORE.두바이트());
                risultato.add(new membro_dati(accesso_voce, metodo_voce_nome, 서술, 속성읽기(Lettore_VALORE)));
            }
            return risultato;
        }
    }
    static final class metodo_descrittore {
        final List<String> argomenti = new ArrayList<>();
        final String Reso_KR;
        metodo_descrittore(String 서술) {
            if (!서술.startsWith("(")) throw new Traduzione_errore("FUNZIONE_VALORE 서술 errore: " + 서술);
            int 끝 = 서술.indexOf(')'); if (끝 < 0) throw new Traduzione_errore("FUNZIONE_VALORE 서술 errore: " + 서술);
            argomenti.addAll(형식읽기(서술.substring(1, 끝)));
            List<String> 반환들 = 형식읽기(서술.substring(끝 + 1));
            if (argomenti.contains("V") || 반환들.size() != 1) throw new Traduzione_errore("FUNZIONE_VALORE 서술 errore: " + 서술);
            Reso_KR = 반환들.get(0);
        }
    }
    static List<String> 형식읽기(String 서술) {
        List<String> risultato = new ArrayList<>();
        String[] 허용형식 = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int posizione = 0; posizione < 서술.length();) {
            String selezione_VALORE = null;
            for (String formato_VALORE : 허용형식) if (서술.startsWith(formato_VALORE, posizione)) { selezione_VALORE = formato_VALORE; break; }
            if (selezione_VALORE == null) throw new Traduzione_errore("지원하지 않는 tipo_di_dati: " + 서술);
            risultato.add(selezione_VALORE); posizione += selezione_VALORE.length();
        }
        return risultato;
    }
    static String simbolo(String Kind_VALORE, String... 부분들) {
        try {
            byte[] hash_File = MessageDigest.getInstance("SHA-256").digest(String.join("\0", 부분들).getBytes(StandardCharsets.UTF_8));
            StringBuilder testo = new StringBuilder("j_" + Kind_VALORE + "_");
            for (int 순번 = 0; 순번 < 12; 순번++) testo.append(String.format(Locale.ROOT, "%02x", hash_File[순번] & 255));
            return testo.toString();
        } catch (Exception errore) { throw new Traduzione_errore(errore.toString()); }
    }
    final Map<String, Corso_dati> 클래스들 = new TreeMap<>();
    final Map<metodo_fonti, membro_dati> 함수들 = new TreeMap<>(), 필드들 = new TreeMap<>();
    final Map<String, String> 문자열들 = new LinkedHashMap<>(), computer_Funzioni_c3a8e64a = new LinkedHashMap<>();
    final String esecuzione_target, computer_Corso;
    final int heap_Conteggio_parole;
    final Path risorsa_percorso;
    기계어미리번역(List<Path> percorso_elenco, String target, int 낱말수, Path risorsa_VALORE) throws IOException {
        if ((!target.equals("kernel") && !target.equals("user")) || 낱말수 < 1024 || 낱말수 > 1048576) throw new Traduzione_errore("Esegui_comando target 또는 Memoria_VALORE e_mail_area Dimensione errore");
        esecuzione_target = target; heap_Conteggio_parole = 낱말수; risorsa_percorso = risorsa_VALORE;
        // 이 이름도 국가별 fonte_albero generare 시 해당 언어로 옮긴다.
        computer_Corso = target.equals("kernel") ? "scheda" : "spazio_utente";
        for (String riga_di_ingresso : Files.readAllLines(risorsa_VALORE.resolve("computer_Funzioni.tsv"), StandardCharsets.UTF_8)) {
            String[] 부분들 = riga_di_ingresso.split("\t", -1);
            if (부분들.length != 4) throw new Traduzione_errore("computer FUNZIONE_VALORE dati errore");
            if (부분들[0].equals(target)) computer_Funzioni_c3a8e64a.put(부분들[1] + 부분들[2], 부분들[3]);
        }
        for (Path percorso : percorso_elenco) {
            Corso_dati dati = new Corso_dati(percorso);
            if (클래스들.put(dati.Nome, dati) != null) throw new Traduzione_errore("중복 Corso_VALORE: " + dati.Nome);
            for (membro_dati valore_del_campo : dati.valore_del_campo) {
                if ((valore_del_campo.accesso_voce & 8) == 0 || 형식읽기(valore_del_campo.서술).equals(Collections.singletonList("V"))) throw new Traduzione_errore("statico_VALORE 필드만 Supporto_VALORE");
                if (필드들.put(new metodo_fonti(dati.Nome, valore_del_campo.Nome, valore_del_campo.서술), valore_del_campo) != null) throw new Traduzione_errore("중복 valore_del_campo");
            }
            for (membro_dati FUNZIONE_VALORE : dati.FUNZIONE_VALORE) {
                if (FUNZIONE_VALORE.Nome.equals("<init>")) continue;
                if ((FUNZIONE_VALORE.accesso_voce & 8) == 0 || (FUNZIONE_VALORE.accesso_voce & (0x20 | 0x400)) != 0) throw new Traduzione_errore("statico_VALORE 비동기화 함수만 Supporto_VALORE");
                new metodo_descrittore(FUNZIONE_VALORE.서술);
                if (함수들.put(new metodo_fonti(dati.Nome, FUNZIONE_VALORE.Nome, FUNZIONE_VALORE.서술), FUNZIONE_VALORE) != null) throw new Traduzione_errore("중복 FUNZIONE_VALORE");
            }
        }
    }
    String stringa_simbolo(String testo) { return 문자열들.computeIfAbsent(testo, VALORE -> "j_text_" + 문자열들.size()); }
    String espressione_costante(Corso_dati dati, int INDICE) {
        if (INDICE < 1 || INDICE >= dati.costante_Kind.length) throw new Traduzione_errore("costante_VALORE INDICE ritagliare errore");
        if (dati.costante_Kind[INDICE] == 3) return "(word)(uint32_t)(" + dati.costante_dati[INDICE] + ")";
        if (dati.costante_Kind[INDICE] == 8) return "(word)" + stringa_simbolo(dati.문자((Integer)dati.costante_dati[INDICE]));
        throw new Traduzione_errore("정수와 stringa_VALORE 상수만 Supporto_VALORE");
    }
    String metodo_prototipo(metodo_fonti fonti) {
        List<String> 인수들 = new ArrayList<>(); int articolo_CONTA_NUMERI = new metodo_descrittore(fonti.서술).argomenti.size();
        for (int 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) 인수들.add("word a" + 순번);
        return "static word " + simbolo("method", fonti.부분들()) + "(" + (articolo_CONTA_NUMERI == 0 ? "void" : String.join(", ", 인수들)) + ")";
    }
    void assegno_locale(int INDICE, int variabile_locale_CONTA_NUMERI) { if (INDICE < 0 || INDICE >= variabile_locale_CONTA_NUMERI) throw new Traduzione_errore("locale_Scope variabile_VALORE INDICE ritagliare errore"); }
    void 분기넣기(List<String> uscitaTesto, Set<Integer> ramo_elenco, int posizione, int 이동량, String condizione) {
        int meta_VALORE = posizione + 이동량; ramo_elenco.add(meta_VALORE);
        uscitaTesto.add((condizione == null ? "" : "if (" + condizione + ") ") + "goto b" + meta_VALORE + ";");
    }
    String corpo_del_metodo(metodo_fonti FUNZIONE_VALORE, membro_dati dati) {
        byte[] corpo_dati = dati.valore_dell_attributo.get("Code"); if (corpo_dati == null) throw new Traduzione_errore("FUNZIONE_VALORE 몸체가 없음: " + FUNZIONE_VALORE.Nome);
        dati_Lettore Lettore_VALORE = new dati_Lettore(corpo_dati); int 쌓임깊이 = Lettore_VALORE.두바이트(), variabile_locale_CONTA_NUMERI = Lettore_VALORE.두바이트();
        dati_Lettore comando_dati = new dati_Lettore(Lettore_VALORE.Lettura(Lettore_VALORE.네바이트()));
        if (Lettore_VALORE.두바이트() != 0) throw new Traduzione_errore("try/catch/finally 미지원");
        metodo_descrittore formato_VALORE = new metodo_descrittore(FUNZIONE_VALORE.서술); if (variabile_locale_CONTA_NUMERI < formato_VALORE.argomenti.size()) throw new Traduzione_errore("매개변수보다 적은 locale_Scope variabile_VALORE");
        Corso_dati Corso_VALORE = 클래스들.get(FUNZIONE_VALORE.proprietario_VALORE);
        List<String> uscitaTesto = new ArrayList<>(); uscitaTesto.add(metodo_prototipo(FUNZIONE_VALORE) + " {");
        uscitaTesto.add("word s[" + Math.max(쌓임깊이, 1) + "], l[" + Math.max(variabile_locale_CONTA_NUMERI, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int 순번 = 0; 순번 < formato_VALORE.argomenti.size(); 순번++) uscitaTesto.add("l[" + 순번 + "] = a" + 순번 + ";");
        Set<Integer> 경계들 = new HashSet<>(), ramo_elenco = new HashSet<>();
        String[] 비교들 = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (comando_dati.posizione < comando_dati.dati.length) {
            int posizione = comando_dati.posizione, comando = comando_dati.한바이트(); 경계들.add(posizione); uscitaTesto.add("b" + posizione + ":;");
            if (comando == 0) continue;
            if (comando == 1) uscitaTesto.add("PUSH(0);");
            else if (comando >= 2 && comando <= 8) uscitaTesto.add("PUSH((uint32_t)(" + (comando - 3) + "));");
            else if (comando == 16 || comando == 17) uscitaTesto.add("PUSH((uint32_t)(" + (comando == 16 ? comando_dati.부호한바이트() : comando_dati.부호두바이트()) + "));");
            else if (comando == 18 || comando == 19) uscitaTesto.add("PUSH(" + espressione_costante(Corso_VALORE, comando == 18 ? comando_dati.한바이트() : comando_dati.두바이트()) + ");");
            else if (comando == 21 || comando == 25 || (comando >= 26 && comando <= 29) || (comando >= 42 && comando <= 45)) {
                int INDICE = comando == 21 || comando == 25 ? comando_dati.한바이트() : comando - (comando <= 29 ? 26 : 42);
                assegno_locale(INDICE, variabile_locale_CONTA_NUMERI); uscitaTesto.add("PUSH(l[" + INDICE + "]);");
            } else if (comando == 54 || comando == 58 || (comando >= 59 && comando <= 62) || (comando >= 75 && comando <= 78)) {
                int INDICE = comando == 54 || comando == 58 ? comando_dati.한바이트() : comando - (comando <= 62 ? 59 : 75);
                assegno_locale(INDICE, variabile_locale_CONTA_NUMERI); uscitaTesto.add("l[" + INDICE + "] = POP();");
            } else if (comando == 46) uscitaTesto.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (comando == 79) uscitaTesto.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (comando == 87 || comando == 88) uscitaTesto.add(comando == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (comando >= 89 && comando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; String[] ordine_elenco = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int 순번 = 0; 순번 < 개수들[comando - 89]; 순번++) uscitaTesto.add("abcd".charAt(순번) + " = POP();");
                for (char VALORE : ordine_elenco[comando - 89].toCharArray()) uscitaTesto.add("PUSH(" + VALORE + ");");
            } else if (comando == 96 || comando == 100 || comando == 104 || comando == 126 || comando == 128 || comando == 130) {
                String operazione_VALORE = comando == 96 ? "+" : comando == 100 ? "-" : comando == 104 ? "*" : comando == 126 ? "&" : comando == 128 ? "|" : "^";
                uscitaTesto.add("b = POP(); a = POP(); PUSH((uint32_t)a " + operazione_VALORE + " (uint32_t)b);");
            } else if (comando == 108 || comando == 112) uscitaTesto.add("b = POP(); a = POP(); PUSH(divide(a,b," + (comando == 112 ? 1 : 0) + "));");
            else if (comando == 116) uscitaTesto.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (comando == 120 || comando == 122 || comando == 124) {
                uscitaTesto.add("b = POP(); a = POP();"); uscitaTesto.add("PUSH(" + (comando == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (comando == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (comando == 132) {
                int INDICE = comando_dati.한바이트(), incremento_importo = comando_dati.부호한바이트(); assegno_locale(INDICE, variabile_locale_CONTA_NUMERI);
                uscitaTesto.add("l[" + INDICE + "] = (uint32_t)l[" + INDICE + "] + (uint32_t)(" + incremento_importo + ");");
            } else if (comando >= 145 && comando <= 147) uscitaTesto.add("a = POP(); PUSH((uint32_t)(" + (comando == 145 ? "int8_t" : comando == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (comando >= 153 && comando <= 158) {
                uscitaTesto.add("a = POP();"); 분기넣기(uscitaTesto, ramo_elenco, posizione, comando_dati.부호두바이트(), "(int32_t)a " + 비교들[comando - 153] + " 0");
            } else if (comando >= 159 && comando <= 166) {
                uscitaTesto.add("b = POP(); a = POP();"); 분기넣기(uscitaTesto, ramo_elenco, posizione, comando_dati.부호두바이트(), comando >= 165 ? "a " + 비교들[comando - 159] + " b" : "(int32_t)a " + 비교들[comando - 159] + " (int32_t)b");
            } else if (comando == 167 || comando == 200) 분기넣기(uscitaTesto, ramo_elenco, posizione, comando == 167 ? comando_dati.부호두바이트() : comando_dati.네바이트(), null);
            else if (comando == 170 || comando == 171) {
                while (comando_dati.posizione % 4 != 0) comando_dati.한바이트();
                int valore_predefinito = comando_dati.네바이트(); uscitaTesto.add("a = POP();");
                if (comando == 170) {
                    int 아래 = comando_dati.네바이트(), 위 = comando_dati.네바이트(); long articolo_CONTA_NUMERI = (long)위 - 아래 + 1;
                    if (articolo_CONTA_NUMERI < 1 || articolo_CONTA_NUMERI > (comando_dati.dati.length - comando_dati.posizione) / 4) throw new Traduzione_errore("switch ritagliare errore");
                    for (long VALORE = 아래; VALORE <= 위; VALORE++) 분기넣기(uscitaTesto, ramo_elenco, posizione, comando_dati.네바이트(), "(int32_t)a == (" + VALORE + ")");
                } else {
                    int articolo_CONTA_NUMERI = comando_dati.네바이트(), frontale_dati = 0;
                    if (articolo_CONTA_NUMERI < 0 || articolo_CONTA_NUMERI > (comando_dati.dati.length - comando_dati.posizione) / 8) throw new Traduzione_errore("switch Dimensione errore");
                    for (int 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) {
                        int VALORE = comando_dati.네바이트(); if (순번 > 0 && VALORE <= frontale_dati) throw new Traduzione_errore("switch ordine_VALORE errore"); frontale_dati = VALORE;
                        분기넣기(uscitaTesto, ramo_elenco, posizione, comando_dati.네바이트(), "(int32_t)a == (" + VALORE + ")");
                    }
                }
                분기넣기(uscitaTesto, ramo_elenco, posizione, valore_predefinito, null);
            } else if (comando == 172 || comando == 176 || comando == 177) uscitaTesto.add("return " + (comando == 177 ? "0" : "POP()") + ";");
            else if (comando == 178 || comando == 179) {
                metodo_fonti fonti = Corso_VALORE.fonti(comando_dati.두바이트()); if (!필드들.containsKey(fonti)) throw new Traduzione_errore("알 numero 없는 valore_del_campo");
                uscitaTesto.add(simbolo("init", fonti.proprietario_VALORE) + "();"); String valore_del_campo = simbolo("field", fonti.부분들());
                uscitaTesto.add(comando == 178 ? "PUSH(" + valore_del_campo + ");" : valore_del_campo + " = POP();");
            } else if (comando == 184) {
                metodo_fonti fonti = Corso_VALORE.fonti(comando_dati.두바이트()); if (!함수들.containsKey(fonti)) throw new Traduzione_errore("알 numero 없는 FUNZIONE_VALORE");
                metodo_descrittore 호출형식 = new metodo_descrittore(fonti.서술); int articolo_CONTA_NUMERI = 호출형식.argomenti.size();
                uscitaTesto.add(simbolo("init", fonti.proprietario_VALORE) + "();"); uscitaTesto.add("if(sp < " + articolo_CONTA_NUMERI + ") kernel_panic(\"call stack underflow\"); sp -= " + articolo_CONTA_NUMERI + ";");
                List<String> 호출인수 = new ArrayList<>(); for (int 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) 호출인수.add("s[sp + " + 순번 + "]");
                uscitaTesto.add("a = " + simbolo("method", fonti.부분들()) + "(" + String.join(",", 호출인수) + ");");
                if (!호출형식.Reso_KR.equals("V")) uscitaTesto.add("PUSH(a);");
            } else if (comando == 182) {
                metodo_fonti fonti = Corso_VALORE.fonti(comando_dati.두바이트());
                if (fonti.equals(new metodo_fonti("java/lang/String", "length", "()I"))) uscitaTesto.add("a = POP(); PUSH(length(a));");
                else if (fonti.equals(new metodo_fonti("java/lang/String", "charAt", "(I)C"))) uscitaTesto.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new Traduzione_errore("가상 FUNZIONE_VALORE 호출 미지원");
            } else if (comando == 188) {
                if (comando_dati.한바이트() != 10) throw new Traduzione_errore("new int[]만 Supporto_VALORE"); uscitaTesto.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (comando == 190) uscitaTesto.add("a = POP(); PUSH(length(a));");
            else if (comando == 196) {
                int estensione_VALORE = comando_dati.한바이트(), INDICE = comando_dati.두바이트(); assegno_locale(INDICE, variabile_locale_CONTA_NUMERI);
                if (estensione_VALORE == 21 || estensione_VALORE == 25) uscitaTesto.add("PUSH(l[" + INDICE + "]);");
                else if (estensione_VALORE == 54 || estensione_VALORE == 58) uscitaTesto.add("l[" + INDICE + "] = POP();");
                else if (estensione_VALORE == 132) uscitaTesto.add("l[" + INDICE + "] = (uint32_t)l[" + INDICE + "] + (uint32_t)(" + comando_dati.부호두바이트() + ");");
                else throw new Traduzione_errore("미지원 wide comando");
            } else if (comando == 198 || comando == 199) {
                uscitaTesto.add("a = POP();"); 분기넣기(uscitaTesto, ramo_elenco, posizione, comando_dati.부호두바이트(), "a " + (comando == 198 ? "==" : "!=") + " 0");
            } else throw new Traduzione_errore(FUNZIONE_VALORE.proprietario_VALORE + "." + FUNZIONE_VALORE.Nome + ", byte_VALORE " + posizione + ": 미지원 comando " + comando);
        }
        if (!경계들.containsAll(ramo_elenco)) throw new Traduzione_errore("comando 경계가 아닌 곳으로 ramo");
        uscitaTesto.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", uscitaTesto);
    }
    String esportare_metodo(String link_simbolo, String target, boolean 진입점여부) {
        int funzione_INDICE = target.lastIndexOf('.'); if (funzione_INDICE < 0 || !link_simbolo.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Traduzione_errore("내보내기 Assegna_VALORE errore");
        String proprietario_VALORE = target.substring(0, funzione_INDICE).replace('.', '/'), Nome = target.substring(funzione_INDICE + 1); metodo_fonti selezione_VALORE = null;
        for (metodo_fonti fonti : 함수들.keySet()) if (fonti.proprietario_VALORE.equals(proprietario_VALORE) && fonti.Nome.equals(Nome)) {
            if (selezione_VALORE != null) throw new Traduzione_errore("겹친 내보내기 target"); selezione_VALORE = fonti;
        }
        if (selezione_VALORE == null || (함수들.get(selezione_VALORE).accesso_voce & 0x100) != 0) throw new Traduzione_errore("내보낼 함수가 없음 또는 native FUNZIONE_VALORE");
        metodo_descrittore formato_VALORE = new metodo_descrittore(selezione_VALORE.서술);
        if ((진입점여부 && !formato_VALORE.argomenti.isEmpty()) || !Arrays.asList("V", "I").contains(formato_VALORE.Reso_KR)) throw new Traduzione_errore("punto_di_ingresso_VALORE 또는 C limite_VALORE formato_VALORE errore");
        List<String> 인수들 = new ArrayList<>(), 호출인수 = new ArrayList<>();
        for (int 순번 = 0; 순번 < formato_VALORE.argomenti.size(); 순번++) {
            if (!formato_VALORE.argomenti.get(순번).equals("I")) throw new Traduzione_errore("C 경계는 int 인수만 Supporto_VALORE");
            인수들.add("int32_t a" + 순번); 호출인수.add("(uint32_t)a" + 순번);
        }
        return (formato_VALORE.Reso_KR.equals("V") ? "void " : "int32_t ") + link_simbolo + "(" + (인수들.isEmpty() ? "void" : String.join(",", 인수들)) + ") { " + simbolo("init", selezione_VALORE.proprietario_VALORE) + "(); " + (formato_VALORE.Reso_KR.equals("V") ? "" : "return (int32_t)") + simbolo("method", selezione_VALORE.부분들()) + "(" + String.join(",", 호출인수) + "); }";
    }
    String generare(String punto_di_ingresso, List<String> 내보내기목록, boolean 범용표기) throws IOException {
        List<String> 선언들 = new ArrayList<>(), 몸체들 = new ArrayList<>(), 필드선언들 = new ArrayList<>();
        for (Map.Entry<metodo_fonti, membro_dati> voce_VALORE : 함수들.entrySet()) {
            metodo_fonti fonti = voce_VALORE.getKey(); membro_dati dati = voce_VALORE.getValue(); 선언들.add(metodo_prototipo(fonti) + ";");
            if ((dati.accesso_voce & 0x100) != 0) {
                String Connetti = computer_Funzioni_c3a8e64a.get(fonti.Nome + fonti.서술);
                if (!fonti.proprietario_VALORE.equals(computer_Corso) || Connetti == null) throw new Traduzione_errore("허용되지 않은 native FUNZIONE_VALORE: " + fonti.Nome);
                int articolo_CONTA_NUMERI = new metodo_descrittore(fonti.서술).argomenti.size(); List<String> 인수들 = new ArrayList<>();
                for (int 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) 인수들.add("a" + 순번);
                선언들.add("extern word " + Connetti + "(" + (articolo_CONTA_NUMERI == 0 ? "void" : String.join(",", Collections.nCopies(articolo_CONTA_NUMERI, "word"))) + ");");
                몸체들.add(metodo_prototipo(fonti) + " { return " + Connetti + "(" + String.join(",", 인수들) + "); }");
            } else 몸체들.add(corpo_del_metodo(fonti, dati));
        }
        for (Map.Entry<metodo_fonti, membro_dati> voce_VALORE : 필드들.entrySet()) {
            metodo_fonti fonti = voce_VALORE.getKey(); byte[] costante_VALORE = voce_VALORE.getValue().valore_dell_attributo.get("ConstantValue");
            String VALORE = costante_VALORE == null ? "0" : espressione_costante(클래스들.get(fonti.proprietario_VALORE), new dati_Lettore(costante_VALORE).두바이트());
            필드선언들.add("static word " + simbolo("field", fonti.부분들()) + " = " + VALORE + ";");
        }
        for (String Nome : 클래스들.keySet()) {
            String inizializza = simbolo("init", Nome), Stato_VALORE = simbolo("state", Nome);
            선언들.add("static void " + inizializza + "(void);"); 필드선언들.add("static unsigned " + Stato_VALORE + ";");
            metodo_fonti fonti = new metodo_fonti(Nome, "<clinit>", "()V");
            몸체들.add("static void " + inizializza + "(void) { if(" + Stato_VALORE + ") return; " + Stato_VALORE + " = 1; " + (함수들.containsKey(fonti) ? simbolo("method", fonti.부분들()) + "(); " : "") + Stato_VALORE + " = 2; }");
        }
        몸체들.add(esportare_metodo("java_entry", punto_di_ingresso, true)); Set<String> 공개이름 = new HashSet<>();
        for (String Assegna_VALORE : 내보내기목록) {
            int funzione_INDICE = Assegna_VALORE.indexOf('='); if (funzione_INDICE < 1) throw new Traduzione_errore("내보내기 Assegna_VALORE errore");
            String Nome = Assegna_VALORE.substring(0, funzione_INDICE); 공개이름.add(Nome); 몸체들.add(esportare_metodo(Nome, Assegna_VALORE.substring(funzione_INDICE + 1), false));
        }
        List<String> 문자열선언들 = new ArrayList<>();
        for (Map.Entry<String, String> voce_VALORE : 문자열들.entrySet()) {
            String testo = voce_VALORE.getKey(); StringBuilder array_VALORE = new StringBuilder("static const word " + voce_VALORE.getValue() + "[] = {" + testo.length());
            for (int 순번 = 0; 순번 < testo.length(); 순번++) array_VALORE.append(", ").append((int)testo.charAt(순번));
            문자열선언들.add(array_VALORE.append("};").toString());
        }
        String Supporto_VALORE = Files.readString(risorsa_percorso.resolve("CLR_Supporto.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(heap_Conteggio_parole));
        return 기계원문한국어화(Supporto_VALORE + String.join("\n", 문자열선언들) + "\n" + String.join("\n", 선언들) + "\n" + String.join("\n", 필드선언들) + "\n" + String.join("\n", 몸체들) + "\n", 공개이름, 범용표기);
    }
    String 기계원문한국어화(String codiceSorgente, Set<String> 공개이름, boolean 범용표기) throws IOException {
        Map<String, String> nome_tabella = new HashMap<>();
        for (String riga_di_ingresso : Files.readAllLines(risorsa_percorso.resolve("생성이름.tsv"), StandardCharsets.UTF_8)) {
            String[] associare_VALORE = riga_di_ingresso.split("\t"); nome_tabella.put(associare_VALORE[0], associare_VALORE[1]);
        }
        Pattern blocco_espressione = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher 찾개 = blocco_espressione.matcher(codiceSorgente); StringBuffer risultato = new StringBuffer();
        while (찾개.find()) {
            String Nome = 찾개.group(), 새이름 = Nome;
            if (!Nome.startsWith("//") && !Nome.startsWith("/*") && !Nome.startsWith("\"") && !Nome.startsWith("'") && !공개이름.contains(Nome)) {
                새이름 = nome_tabella.getOrDefault(Nome, Nome);
                if (Nome.matches("a[0-9]+")) 새이름 = "argomenti" + Nome.substring(1);
                if (Nome.matches("b[0-9]+")) 새이름 = "ramo" + Nome.substring(1);
                if (범용표기) {
                    StringBuilder notazione_VALORE = new StringBuilder();
                    for (char carattere_VALORE : 새이름.toCharArray()) notazione_VALORE.append(carattere_VALORE < 128 ? Character.toString(carattere_VALORE) : String.format(Locale.ROOT, "\\u%04x", (int)carattere_VALORE));
                    새이름 = notazione_VALORE.toString();
                }
            }
            찾개.appendReplacement(risultato, Matcher.quoteReplacement(새이름));
        }
        찾개.appendTail(risultato); return risultato.toString();
    }
    String X_86_corpo_del_metodo(metodo_fonti FUNZIONE_VALORE, membro_dati dati, Map<String,String> computer_tabella, String target) {
        String marcatore_VALORE = simbolo("method", FUNZIONE_VALORE.부분들());
        List<String> riga_di_ingresso = new ArrayList<>();
        if ((dati.accesso_voce & 0x100) != 0) {
            String Connetti = computer_tabella.get(FUNZIONE_VALORE.Nome + FUNZIONE_VALORE.서술);
            if (!FUNZIONE_VALORE.proprietario_VALORE.equals(target.equals("kernel") ? "cellulare_VALORE" : "spazio_utente") || Connetti == null) throw new Traduzione_errore("허용되지 않은 native FUNZIONE_VALORE");
            return ".text\n" + marcatore_VALORE + ":\njmp " + Connetti;
        }
        byte[] corpo_del_testo = dati.valore_dell_attributo.get("Code"); if (corpo_del_testo == null) throw new Traduzione_errore("FUNZIONE_VALORE 몸체가 없음");
        dati_Lettore Lettore_VALORE = new dati_Lettore(corpo_del_testo); Lettore_VALORE.두바이트(); int locale_CONTA_NUMERI = Lettore_VALORE.두바이트();
        dati_Lettore comando_dati = new dati_Lettore(Lettore_VALORE.Lettura(Lettore_VALORE.네바이트()));
        if (Lettore_VALORE.두바이트() != 0) throw new Traduzione_errore("try/catch/finally 미지원");
        metodo_descrittore formato_VALORE = new metodo_descrittore(FUNZIONE_VALORE.서술); if (locale_CONTA_NUMERI < formato_VALORE.argomenti.size()) throw new Traduzione_errore("매개변수보다 적은 locale_Scope variabile_VALORE");
        Collections.addAll(riga_di_ingresso,".text",".globl " + marcatore_VALORE,".type " + marcatore_VALORE + ", @function",marcatore_VALORE + ":","pushl %ebp","movl %esp, %ebp","subl $" + locale_CONTA_NUMERI * 4 + ", %esp");
        for (int 순번 = 0; 순번 < formato_VALORE.argomenti.size(); 순번++) Collections.addAll(riga_di_ingresso,"movl " + (8 + 4 * (formato_VALORE.argomenti.size() - 순번 - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (순번 + 1)) + "(%ebp)");
        Corso_dati Corso_VALORE = 클래스들.get(FUNZIONE_VALORE.proprietario_VALORE); Set<Integer> 경계들 = new HashSet<>(), ramo_elenco = new HashSet<>();
        String[] 비교들 = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (comando_dati.posizione < comando_dati.dati.length) {
            int posizione = comando_dati.posizione, comando = comando_dati.한바이트(); String funzione_INDICE = marcatore_VALORE + "_b" + posizione;
            riga_di_ingresso.add(funzione_INDICE + ":"); 경계들.add(posizione);
            if (comando == 0) riga_di_ingresso.add("nop");
            else if (comando == 1) riga_di_ingresso.add("pushl $0");
            else if (comando >= 2 && comando <= 8) riga_di_ingresso.add("pushl $" + (comando - 3));
            else if (comando == 16 || comando == 17) riga_di_ingresso.add("pushl $" + (comando == 16 ? comando_dati.부호한바이트() : comando_dati.부호두바이트()));
            else if (comando == 18 || comando == 19) {
                int INDICE = comando == 18 ? comando_dati.한바이트() : comando_dati.두바이트();
                riga_di_ingresso.add("pushl $" + X_86_costante(Corso_VALORE,INDICE));
            } else if (comando == 21 || comando == 25 || (comando >= 26 && comando <= 29) || (comando >= 42 && comando <= 45) || comando == 54 || comando == 58 || (comando >= 59 && comando <= 62) || (comando >= 75 && comando <= 78)) {
                boolean 읽음 = comando < 54; int INDICE = comando == 21 || comando == 25 || comando == 54 || comando == 58 ? comando_dati.한바이트() : comando - (comando <= 29 ? 26 : comando <= 45 ? 42 : comando <= 62 ? 59 : 75);
                assegno_locale(INDICE,locale_CONTA_NUMERI); riga_di_ingresso.add((읽음 ? "pushl " : "popl ") + "-" + (4 * (INDICE + 1)) + "(%ebp)");
            } else if (comando == 46) Collections.addAll(riga_di_ingresso,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (comando == 79) Collections.addAll(riga_di_ingresso,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (comando == 87 || comando == 88) riga_di_ingresso.add("addl $" + (comando == 87 ? 4 : 8) + ", %esp");
            else if (comando >= 89 && comando <= 95) {
                int[] 개수들 = {1,2,3,2,3,4,2}; int[][] ordine_elenco = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] 저장기들 = {"%eax","%ecx","%edx","%ebx"};
                for (int 순번 = 0; 순번 < 개수들[comando - 89]; 순번++) riga_di_ingresso.add("popl " + 저장기들[순번]);
                for (int 순번 : ordine_elenco[comando - 89]) riga_di_ingresso.add("pushl " + 저장기들[순번]);
            } else if (comando == 96 || comando == 100 || comando == 104 || comando == 126 || comando == 128 || comando == 130) {
                String operazione_VALORE = comando == 96 ? "addl" : comando == 100 ? "subl" : comando == 104 ? "imull" : comando == 126 ? "andl" : comando == 128 ? "orl" : "xorl";
                Collections.addAll(riga_di_ingresso,"popl %ecx","popl %eax",operazione_VALORE + " %ecx, %eax","pushl %eax");
            } else if (comando == 108 || comando == 112) Collections.addAll(riga_di_ingresso,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + funzione_INDICE + "_divide","cmpl $0x80000000, %eax","jne " + funzione_INDICE + "_divide","xorl %edx, %edx","jmp " + funzione_INDICE + "_done",funzione_INDICE + "_divide:","cltd","idivl %ecx",funzione_INDICE + "_done:","pushl " + (comando == 108 ? "%eax" : "%edx"));
            else if (comando == 116) riga_di_ingresso.add("negl (%esp)");
            else if (comando == 120 || comando == 122 || comando == 124) Collections.addAll(riga_di_ingresso,"popl %ecx","popl %eax",(comando == 120 ? "sall" : comando == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (comando == 132) {
                int INDICE = comando_dati.한바이트(), incremento_VALORE = comando_dati.부호한바이트(); assegno_locale(INDICE,locale_CONTA_NUMERI); riga_di_ingresso.add("addl $" + incremento_VALORE + ", -" + (4 * (INDICE + 1)) + "(%ebp)");
            } else if (comando >= 145 && comando <= 147) Collections.addAll(riga_di_ingresso,"popl %eax",comando == 145 ? "movsbl %al, %eax" : comando == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (comando >= 153 && comando <= 166) {
                if (comando <= 158) Collections.addAll(riga_di_ingresso,"popl %eax","testl %eax, %eax");
                else Collections.addAll(riga_di_ingresso,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int meta_VALORE = posizione + comando_dati.부호두바이트(); ramo_elenco.add(meta_VALORE); riga_di_ingresso.add(비교들[comando - (comando <= 158 ? 153 : 159)] + " " + marcatore_VALORE + "_b" + meta_VALORE);
            } else if (comando == 167 || comando == 200) {
                int meta_VALORE = posizione + (comando == 167 ? comando_dati.부호두바이트() : comando_dati.네바이트()); ramo_elenco.add(meta_VALORE); riga_di_ingresso.add("jmp " + marcatore_VALORE + "_b" + meta_VALORE);
            } else if (comando == 170 || comando == 171) {
                while (comando_dati.posizione % 4 != 0) comando_dati.한바이트();
                int valore_predefinito = posizione + comando_dati.네바이트(); ramo_elenco.add(valore_predefinito); riga_di_ingresso.add("popl %eax");
                int articolo_CONTA_NUMERI, 아래 = 0;
                if (comando == 170) { 아래 = comando_dati.네바이트(); int 위 = comando_dati.네바이트(); long durata_VALORE = (long)위 - 아래 + 1; if (durata_VALORE < 1 || durata_VALORE > (comando_dati.dati.length - comando_dati.posizione) / 4) throw new Traduzione_errore("switch ritagliare errore"); articolo_CONTA_NUMERI = (int)durata_VALORE; }
                else { articolo_CONTA_NUMERI = comando_dati.네바이트(); if (articolo_CONTA_NUMERI < 0 || articolo_CONTA_NUMERI > (comando_dati.dati.length - comando_dati.posizione) / 8) throw new Traduzione_errore("switch Dimensione errore"); }
                for (int 순번 = 0; 순번 < articolo_CONTA_NUMERI; 순번++) {
                    int VALORE = comando == 170 ? 아래 + 순번 : comando_dati.네바이트(), meta_VALORE = posizione + comando_dati.네바이트(); ramo_elenco.add(meta_VALORE);
                    Collections.addAll(riga_di_ingresso,"cmpl $" + VALORE + ", %eax","je " + marcatore_VALORE + "_b" + meta_VALORE);
                }
                riga_di_ingresso.add("jmp " + marcatore_VALORE + "_b" + valore_predefinito);
            } else if (comando == 172 || comando == 176 || comando == 177) {
                if (comando != 177) riga_di_ingresso.add("popl %eax"); Collections.addAll(riga_di_ingresso,"leave","ret");
            } else if (comando == 178 || comando == 179) {
                metodo_fonti fonti = Corso_VALORE.fonti(comando_dati.두바이트()); if (!필드들.containsKey(fonti)) throw new Traduzione_errore("알 numero 없는 valore_del_campo");
                Collections.addAll(riga_di_ingresso,"call " + simbolo("init",fonti.proprietario_VALORE),(comando == 178 ? "pushl " : "popl ") + simbolo("field",fonti.부분들()));
            } else if (comando == 184) {
                metodo_fonti fonti = Corso_VALORE.fonti(comando_dati.두바이트()); if (!함수들.containsKey(fonti)) throw new Traduzione_errore("알 numero 없는 FUNZIONE_VALORE");
                metodo_descrittore 호출형식 = new metodo_descrittore(fonti.서술); Collections.addAll(riga_di_ingresso,"call " + simbolo("init",fonti.proprietario_VALORE),"call " + simbolo("method",fonti.부분들()));
                if (!호출형식.argomenti.isEmpty()) riga_di_ingresso.add("addl $" + 호출형식.argomenti.size() * 4 + ", %esp");
                if (!호출형식.Reso_KR.equals("V")) riga_di_ingresso.add("pushl %eax");
            } else if (comando == 182) {
                metodo_fonti fonti = Corso_VALORE.fonti(comando_dati.두바이트());
                if (fonti.equals(new metodo_fonti("java/lang/String","length","()I"))) Collections.addAll(riga_di_ingresso,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (fonti.equals(new metodo_fonti("java/lang/String","charAt","(I)C"))) Collections.addAll(riga_di_ingresso,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new Traduzione_errore("가상 FUNZIONE_VALORE 호출 미지원");
            } else if (comando == 188) {
                if (comando_dati.한바이트() != 10) throw new Traduzione_errore("new int[]만 Supporto_VALORE"); Collections.addAll(riga_di_ingresso,"popl %eax","call rt_new_array","pushl %eax");
            } else if (comando == 190) Collections.addAll(riga_di_ingresso,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (comando == 196) {
                int estensione_VALORE = comando_dati.한바이트(), INDICE = comando_dati.두바이트(); assegno_locale(INDICE,locale_CONTA_NUMERI);
                if (estensione_VALORE == 21 || estensione_VALORE == 25 || estensione_VALORE == 54 || estensione_VALORE == 58) riga_di_ingresso.add((estensione_VALORE <= 25 ? "pushl " : "popl ") + "-" + 4 * (INDICE + 1) + "(%ebp)");
                else if (estensione_VALORE == 132) riga_di_ingresso.add("addl $" + comando_dati.부호두바이트() + ", -" + 4 * (INDICE + 1) + "(%ebp)");
                else throw new Traduzione_errore("wide comando 미지원");
            } else if (comando == 198 || comando == 199) {
                int meta_VALORE = posizione + comando_dati.부호두바이트(); ramo_elenco.add(meta_VALORE); Collections.addAll(riga_di_ingresso,"popl %eax","testl %eax, %eax",(comando == 198 ? "je " : "jne ") + marcatore_VALORE + "_b" + meta_VALORE);
            } else throw new Traduzione_errore("미지원 comando: " + comando);
        }
        if (!경계들.containsAll(ramo_elenco)) throw new Traduzione_errore("comando 경계가 아닌 곳으로 ramo");
        riga_di_ingresso.add(".size " + marcatore_VALORE + ", .-" + marcatore_VALORE); return String.join("\n",riga_di_ingresso);
    }
    String X_86_costante(Corso_dati dati, int INDICE) {
        if (dati.costante_Kind[INDICE] == 3) return dati.costante_dati[INDICE].toString();
        if (dati.costante_Kind[INDICE] == 8) return stringa_simbolo(dati.문자((Integer)dati.costante_dati[INDICE]));
        throw new Traduzione_errore("정수와 stringa_VALORE 상수만 Supporto_VALORE");
    }
    String X_86_assembly(String punto_di_ingresso, List<String> 내보냄, String target) throws IOException {
        Map<String,String> computer_tabella = new HashMap<>();
        for (String riga_di_ingresso : Files.readAllLines(risorsa_percorso.resolve("_86_computer_Funzioni.tsv"))) { String[] associare_VALORE = riga_di_ingresso.split("\t"); if (associare_VALORE[0].equals(target)) computer_tabella.put(associare_VALORE[1] + associare_VALORE[2],associare_VALORE[3]); }
        int funzione_INDICE = punto_di_ingresso.lastIndexOf('.'); if (funzione_INDICE < 0) throw new Traduzione_errore("punto_di_ingresso Assegna_VALORE errore");
        String proprietario_VALORE = punto_di_ingresso.substring(0,funzione_INDICE).replace('.','/'), metodo_voce_nome = punto_di_ingresso.substring(funzione_INDICE + 1); metodo_fonti punto_di_ingresso_VALORE = null;
        for (String 서술 : Arrays.asList("()I","()V")) { metodo_fonti fonti = new metodo_fonti(proprietario_VALORE,metodo_voce_nome,서술); if (함수들.containsKey(fonti)) { if (punto_di_ingresso_VALORE != null) throw new Traduzione_errore("겹친 punto_di_ingresso"); punto_di_ingresso_VALORE = fonti; } }
        if (punto_di_ingresso_VALORE == null || (함수들.get(punto_di_ingresso_VALORE).accesso_voce & 0x100) != 0) throw new Traduzione_errore("punto_di_ingresso_VALORE FUNZIONE_VALORE formato_VALORE errore");
        List<String> riga_di_ingresso = new ArrayList<>(); riga_di_ingresso.add(".code32");
        for (Corso_dati dati : 클래스들.values()) {
            String Stato_VALORE = simbolo("state",dati.Nome), inizializza = simbolo("init",dati.Nome);
            Collections.addAll(riga_di_ingresso,".bss",".balign 4",Stato_VALORE + ": .long 0",".text",inizializza + ":","cmpl $0, " + Stato_VALORE,"jne " + inizializza + "_done","movl $1, " + Stato_VALORE);
            metodo_fonti inizializzatore_fonti = new metodo_fonti(dati.Nome,"<clinit>","()V"); if (함수들.containsKey(inizializzatore_fonti)) riga_di_ingresso.add("call " + simbolo("method",inizializzatore_fonti.부분들()));
            Collections.addAll(riga_di_ingresso,"movl $2, " + Stato_VALORE,inizializza + "_done:","ret");
            for (membro_dati valore_del_campo : dati.valore_del_campo) {
                byte[] costante_VALORE = valore_del_campo.valore_dell_attributo.get("ConstantValue"); String VALORE = costante_VALORE == null ? "0" : X_86_costante(dati,new dati_Lettore(costante_VALORE).두바이트());
                Collections.addAll(riga_di_ingresso,".data",".balign 4",simbolo("field",dati.Nome,valore_del_campo.Nome,valore_del_campo.서술) + ": .long " + VALORE);
            }
            for (membro_dati FUNZIONE_VALORE : dati.FUNZIONE_VALORE) if (!FUNZIONE_VALORE.Nome.equals("<init>")) riga_di_ingresso.add(X_86_corpo_del_metodo(new metodo_fonti(dati.Nome,FUNZIONE_VALORE.Nome,FUNZIONE_VALORE.서술),FUNZIONE_VALORE,computer_tabella,target));
        }
        Collections.addAll(riga_di_ingresso,".text",".globl java_entry","java_entry:","call " + simbolo("init",punto_di_ingresso_VALORE.proprietario_VALORE),"call " + simbolo("method",punto_di_ingresso_VALORE.부분들()));
        if (punto_di_ingresso_VALORE.서술.equals("()V")) riga_di_ingresso.add("xorl %eax, %eax"); riga_di_ingresso.add("ret");
        for (String Assegna_VALORE : 내보냄) {
            int delimitatore_VALORE = Assegna_VALORE.indexOf('='); if (delimitatore_VALORE < 1) throw new Traduzione_errore("내보내기 Assegna_VALORE errore");
            String esterno_VALORE = Assegna_VALORE.substring(0,delimitatore_VALORE), FUNZIONE_VALORE = Assegna_VALORE.substring(delimitatore_VALORE + 1); int Divisione_KR = FUNZIONE_VALORE.lastIndexOf('.');
            if (Divisione_KR < 0 || !esterno_VALORE.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new Traduzione_errore("내보내기 simbolo errore");
            String Corso_VALORE = FUNZIONE_VALORE.substring(0,Divisione_KR).replace('.','/'), Nome = FUNZIONE_VALORE.substring(Divisione_KR + 1); metodo_fonti selezione_VALORE = null;
            for (metodo_fonti fonti : 함수들.keySet()) if (fonti.proprietario_VALORE.equals(Corso_VALORE) && fonti.Nome.equals(Nome)) { if (selezione_VALORE != null) throw new Traduzione_errore("겹친 내보내기 target"); selezione_VALORE = fonti; }
            if (selezione_VALORE == null) throw new Traduzione_errore("내보낼 함수가 없음");
            Collections.addAll(riga_di_ingresso,".text",".globl " + esterno_VALORE,esterno_VALORE + ":","call " + simbolo("init",selezione_VALORE.proprietario_VALORE),"jmp " + simbolo("method",selezione_VALORE.부분들()));
        }
        riga_di_ingresso.add(".section .rodata");
        for (Map.Entry<String,String> voce_VALORE : 문자열들.entrySet()) {
            Collections.addAll(riga_di_ingresso,".balign 4",voce_VALORE.getValue() + ":",".long " + voce_VALORE.getKey().length());
            List<String> 단위들 = new ArrayList<>(); for (char unità_VALORE : voce_VALORE.getKey().toCharArray()) 단위들.add(Integer.toString(unità_VALORE)); if (!단위들.isEmpty()) riga_di_ingresso.add(".long " + String.join(",",단위들));
        }
        riga_di_ingresso.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",riga_di_ingresso) + "\n";
    }
    static void Esegui_strumento(List<String> comando) throws Exception {
        if (new ProcessBuilder(comando).inheritIO().start().waitFor() != 0) throw new Traduzione_errore("compilare_fonte errore: " + comando.get(0));
    }
    static String dati_stringa(String testo) { return "\"" + testo.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void X_86_Traduzione(List<Path> input_elenco, String target, String punto_di_ingresso, List<String> 내보냄, Path uscitaTesto, Path risorsa_VALORE) throws Exception {
        Path 임시 = Files.createTempDirectory("jkoros-java-x86-"), Corso_percorso = 임시.resolve("classes"); Files.createDirectory(Corso_percorso);
        try {
            List<String> 자바명령 = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",Corso_percorso.toString(),"-sourcepath",Corso_percorso.toString(),"-d",Corso_percorso.toString()));
            List<Path> 바이트코드 = new ArrayList<>(); int fonte_CONTA_NUMERI = 0;
            for (Path input_VALORE : input_elenco) {
                if (uscitaTesto.toAbsolutePath().normalize().equals(input_VALORE.toAbsolutePath().normalize())) throw new Traduzione_errore("uscitaTesto 파일과 입력이 같음");
                if (input_VALORE.toString().endsWith(".java")) { 자바명령.add(input_VALORE.toString()); fonte_CONTA_NUMERI++; }
                else if (input_VALORE.toString().endsWith(".class")) 바이트코드.add(input_VALORE);
                else throw new Traduzione_errore(".java 또는 .class만 Supporto_VALORE");
            }
            if (fonte_CONTA_NUMERI > 0) Esegui_strumento(자바명령);
            try (java.util.stream.Stream<Path> percorso_elenco = Files.walk(Corso_percorso)) { percorso_elenco.filter(percorso -> percorso.toString().endsWith(".class")).sorted().forEach(바이트코드::add); }
            기계어미리번역 CONVERTI_VALORE = new 기계어미리번역(바이트코드,target.equals("user") ? "user" : "kernel",262144,risorsa_VALORE);
            String assemblare_VALORE = CONVERTI_VALORE.X_86_assembly(punto_di_ingresso,내보냄,target); Files.writeString(임시.resolve("program.s"),assemblare_VALORE,StandardCharsets.UTF_8);
            Path strumento_funzione = risorsa_VALORE.getParent();
            Esegui_strumento(Arrays.asList("as","--32","-o",임시.resolve("program.o").toString(),임시.resolve("program.s").toString()));
            Esegui_strumento(Arrays.asList("as","--32","-o",임시.resolve("runtime.o").toString(),strumento_funzione.resolve("CLR_Supporto.s").toString()));
            List<String> Connetti = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (target.equals("kernel")) Connetti.add("-r");
            else {
                Esegui_strumento(Arrays.asList("as","--32","-o",임시.resolve("start.o").toString(),strumento_funzione.resolve(target.equals("user") ? "START_USER_app.s" : "리눅스시작.s").toString()));
                Collections.addAll(Connetti,"-e","_start",임시.resolve("start.o").toString());
                if (target.equals("user")) Collections.addAll(Connetti,"-T",strumento_funzione.resolve("USER_link_Layout.ld").toString());
            }
            Collections.addAll(Connetti,"-o",임시.resolve("result").toString(),임시.resolve("program.o").toString(),임시.resolve("runtime.o").toString()); Esegui_strumento(Connetti);
            uscitaTesto = uscitaTesto.toAbsolutePath(); Files.createDirectories(uscitaTesto.getParent()); Path pubblicare_VALORE = Files.createTempFile(uscitaTesto.getParent(),".elf-",".tmp");
            try { Files.copy(임시.resolve("result"),pubblicare_VALORE,StandardCopyOption.REPLACE_EXISTING); Files.move(pubblicare_VALORE,uscitaTesto,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(pubblicare_VALORE); }
            Files.setPosixFilePermissions(uscitaTesto,java.nio.file.attribute.PosixFilePermissions.fromString(target.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(uscitaTesto + ".s"),assemblare_VALORE,StandardCharsets.UTF_8);
            List<String> simbolo_dati = new ArrayList<>(), dati_di_origine = new ArrayList<>();
            for (metodo_fonti fonti : CONVERTI_VALORE.함수들.keySet()) simbolo_dati.add(dati_stringa(simbolo("method",fonti.부분들())) + ":" + dati_stringa(fonti.proprietario_VALORE + "." + fonti.Nome + fonti.서술));
            for (Path input_VALORE : input_elenco) {
                byte[] hash_File = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(input_VALORE)); StringBuilder testo = new StringBuilder(); for (byte VALORE : hash_File) testo.append(String.format(Locale.ROOT,"%02x",VALORE & 255));
                dati_di_origine.add(dati_stringa(input_VALORE.toAbsolutePath().toString()) + ":" + dati_stringa(testo.toString()));
            }
            Files.writeString(Paths.get(uscitaTesto + ".json"),"{\"target\":" + dati_stringa(target) + ",\"entry\":" + dati_stringa(punto_di_ingresso) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",simbolo_dati) + "},\"sources\":{" + String.join(",",dati_di_origine) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> percorso_elenco = Files.walk(임시)) { for (Path percorso : (Iterable<Path>)percorso_elenco.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(percorso); }
        }
    }
    public static void main(String[] argomenti) {
        try {
            String punto_di_ingresso = null, target = "kernel", X_86_target = null; Path output_percorso = null; int 낱말수 = 262144; boolean 범용표기 = false;
            List<String> 내보냄 = new ArrayList<>(); List<Path> percorso_elenco = new ArrayList<>();
            for (int 순번 = 0; 순번 < argomenti.length; 순번++) {
                String VALORE = argomenti[순번];
                switch (VALORE) {
                    case "--target": X_86_target = argomenti[++순번]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry Corso_VALORE.FUNZIONE_VALORE -o uscitaTesto [--target linux|kernel|user] [--profile kernel|user] [--export simbolo=Corso_VALORE.FUNZIONE_VALORE] 클래스파일 또는 Java원문"); return;
                    case "--entry": punto_di_ingresso = argomenti[++순번]; break;
                    case "--profile": target = argomenti[++순번]; break;
                    case "--heap-words": 낱말수 = Integer.parseInt(argomenti[++순번]); break;
                    case "--export": 내보냄.add(argomenti[++순번]); break;
                    case "-o": output_percorso = Paths.get(argomenti[++순번]); break;
                    case "--ucn": 범용표기 = true; break;
                    default: if (VALORE.startsWith("-")) throw new Traduzione_errore("알 numero 없는 옵션: " + VALORE); percorso_elenco.add(Paths.get(VALORE));
                }
            }
            if (punto_di_ingresso == null || output_percorso == null || percorso_elenco.isEmpty()) throw new Traduzione_errore("--entry, -o, Corso_VALORE 파일이 필요합니다");
            Path risorsa_VALORE = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (X_86_target != null) {
                if (!Arrays.asList("linux","kernel","user").contains(X_86_target)) throw new Traduzione_errore("알 numero 없는 Esegui_comando target");
                X_86_Traduzione(percorso_elenco,X_86_target,punto_di_ingresso,내보냄,output_percorso,risorsa_VALORE); return;
            }
            String codiceSorgente = new 기계어미리번역(percorso_elenco, target, 낱말수, risorsa_VALORE).generare(punto_di_ingresso, 내보냄, 범용표기);
            output_percorso = output_percorso.toAbsolutePath(); Files.createDirectories(output_percorso.getParent());
            Path 임시 = Files.createTempFile(output_percorso.getParent(), ".aot-", ".tmp");
            try { Files.writeString(임시, codiceSorgente, StandardCharsets.UTF_8); Files.move(임시, output_percorso, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(임시); }
        } catch (Exception errore) { System.err.println("compilare_fonte errore: " + errore.getMessage()); System.exit(1); }
    }
}
