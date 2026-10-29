// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.regex.*;

/** Produit du code source C pour un noyau ARM64 autonome à partir de fichiers de classes Java. S’exécute sur le JDK hôte. */
public final class CompilationAnticipée {
    static final class ErreurTraduction extends RuntimeException {
        ErreurTraduction(String description) { super(description); }
    }
    static final class LecteurDonnées {
        final byte[] Données;
        int position;
        LecteurDonnées(byte[] donnéesEntrée) { Données = donnéesEntrée; }
        byte[] lire(int longueur) {
            if (longueur < 0 || longueur > Données.length - position) throw new ErreurTraduction("valeurRogné valeurClasse 또는 commande Données");
            byte[] résultat = Arrays.copyOfRange(Données, position, position + longueur); position += longueur; return résultat;
        }
        int lireOctet() { if (position >= Données.length) throw new ErreurTraduction("valeurRogné commande Données"); return Données[position++] & 255; }
        int lireCourt() { return (lireOctet() << 8) | lireOctet(); }
        int lireTypeEntier() { return (lireCourt() << 16) | lireCourt(); }
        int lireOctetSigné() { return (byte) lireOctet(); }
        int lireCourtSigné() { return (short) lireCourt(); }
    }
    static final class DonnéesMembre {
        final int entréeÉlémentAccès;
        final String nom, valeurDescription;
        final Map<String, byte[]> valeurAttribut;
        DonnéesMembre(int valeurAccès, String valeurNom, String donnéesDescripteur, Map<String, byte[]> donnéesAttribut) {
            entréeÉlémentAccès = valeurAccès; nom = valeurNom; valeurDescription = donnéesDescripteur; valeurAttribut = donnéesAttribut;
        }
    }
    static final class RéférenceMéthode implements Comparable<RéférenceMéthode> {
        final String valeurPropriétaire, nom, valeurDescription;
        RéférenceMéthode(String valeurPossédé, String valeurNom, String donnéesDescripteur) { valeurPropriétaire = valeurPossédé; nom = valeurNom; valeurDescription = donnéesDescripteur; }
        String[] parties() { return new String[]{valeurPropriétaire, nom, valeurDescription}; }
        public int compareTo(RéférenceMéthode valeurPairRéseau) {
            int valeurComparaison = valeurPropriétaire.compareTo(valeurPairRéseau.valeurPropriétaire);
            if (valeurComparaison == 0) valeurComparaison = nom.compareTo(valeurPairRéseau.nom);
            return valeurComparaison == 0 ? valeurDescription.compareTo(valeurPairRéseau.valeurDescription) : valeurComparaison;
        }
        public boolean equals(Object valeurPairRéseau) { return valeurPairRéseau instanceof RéférenceMéthode && compareTo((RéférenceMéthode) valeurPairRéseau) == 0; }
        public int hashCode() { return Objects.hash(valeurPropriétaire, nom, valeurDescription); }
    }
    static final class DonnéesClasse {
        final int[] genreConstante;
        final Object[] donnéesConstante;
        final String nom;
        final List<DonnéesMembre> valeurChamp, Fonction;
        DonnéesClasse(Path chemin) throws IOException {
            LecteurDonnées valeurLecteur = new LecteurDonnées(Files.readAllBytes(chemin));
            if (valeurLecteur.lireTypeEntier() != 0xcafebabe) throw new ErreurTraduction("Java valeurClasse 표식이 아님");
            valeurLecteur.lire(4);
            int nombreÉlémentsÉlémentListe = valeurLecteur.lireCourt(); genreConstante = new int[nombreÉlémentsÉlémentListe]; donnéesConstante = new Object[nombreÉlémentsÉlémentListe];
            for (int indiceOrdinal = 1; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) {
                int valeurGenre = valeurLecteur.lireOctet(); genreConstante[indiceOrdinal] = valeurGenre;
                switch (valeurGenre) {
                    case 1:
                        int longueur = valeurLecteur.lireCourt();
                        byte[] tamponCaractère = valeurLecteur.lire(longueur), donnéesPréfixéLongueur = new byte[longueur + 2];
                        donnéesPréfixéLongueur[0] = (byte)(longueur >> 8); donnéesPréfixéLongueur[1] = (byte)longueur;
                        System.arraycopy(tamponCaractère, 0, donnéesPréfixéLongueur, 2, longueur);
                        donnéesConstante[indiceOrdinal] = new DataInputStream(new ByteArrayInputStream(donnéesPréfixéLongueur)).readUTF(); break;
                    case 3: donnéesConstante[indiceOrdinal] = valeurLecteur.lireTypeEntier(); break;
                    case 4: valeurLecteur.lire(4); break;
                    case 5: case 6: valeurLecteur.lire(8); indiceOrdinal++; break;
                    case 7: case 8: case 16: donnéesConstante[indiceOrdinal] = valeurLecteur.lireCourt(); break;
                    case 9: case 10: case 11: case 12: case 18:
                        donnéesConstante[indiceOrdinal] = new int[]{valeurLecteur.lireCourt(), valeurLecteur.lireCourt()}; break;
                    case 15: donnéesConstante[indiceOrdinal] = new int[]{valeurLecteur.lireOctet(), valeurLecteur.lireCourt()}; break;
                    default: throw new ErreurTraduction("지원하지 않는 valeurConstante valeurGenre: " + valeurGenre);
                }
            }
            valeurLecteur.lireCourt(); nom = nomClasse(valeurLecteur.lireCourt());
            if (!nomClasse(valeurLecteur.lireCourt()).equals("java/lang/Object") || valeurLecteur.lireCourt() != 0)
                throw new ErreurTraduction(nom + ": 상속 및 인터페이스 estNonPrisEnCharge");
            valeurChamp = lireMembres(valeurLecteur); Fonction = lireMembres(valeurLecteur); lireAttributs(valeurLecteur);
            if (valeurLecteur.position != valeurLecteur.Données.length) throw new ErreurTraduction("valeurClasse 뒤에 남은 Données");
        }
        String Caractères(int numéro) {
            if (numéro < 1 || numéro >= genreConstante.length || genreConstante[numéro] != 1) throw new ErreurTraduction("Caractères valeurConstante numéro erreur");
            return (String) donnéesConstante[numéro];
        }
        String nomClasse(int numéro) {
            if (numéro < 1 || numéro >= genreConstante.length || genreConstante[numéro] != 7) throw new ErreurTraduction("valeurClasse référence erreur");
            return Caractères((Integer)donnéesConstante[numéro]);
        }
        RéférenceMéthode référence(int numéro) {
            if (numéro < 1 || numéro >= genreConstante.length || genreConstante[numéro] < 9 || genreConstante[numéro] > 11) throw new ErreurTraduction("멤버 référence erreur");
            int[] valeurPaire = (int[])donnéesConstante[numéro], paireNom = (int[])donnéesConstante[valeurPaire[1]];
            return new RéférenceMéthode(nomClasse(valeurPaire[0]), Caractères(paireNom[0]), Caractères(paireNom[1]));
        }
        Map<String, byte[]> lireAttributs(LecteurDonnées valeurLecteur) {
            Map<String, byte[]> résultat = new LinkedHashMap<>();
            int nombreÉlémentsÉlémentListe = valeurLecteur.lireCourt();
            for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) {
                String nomAttribut = Caractères(valeurLecteur.lireCourt()); byte[] valeur = valeurLecteur.lire(valeurLecteur.lireTypeEntier());
                if (résultat.put(nomAttribut, valeur) != null) throw new ErreurTraduction("겹친 valeurAttribut: " + nomAttribut);
            }
            return résultat;
        }
        List<DonnéesMembre> lireMembres(LecteurDonnées valeurLecteur) {
            List<DonnéesMembre> résultat = new ArrayList<>(); int nombreÉlémentsÉlémentListe = valeurLecteur.lireCourt();
            for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) {
                int entréeÉlémentAccès = valeurLecteur.lireCourt(); String nomEntréeÉlémentMéthode = Caractères(valeurLecteur.lireCourt()), valeurDescription = Caractères(valeurLecteur.lireCourt());
                résultat.add(new DonnéesMembre(entréeÉlémentAccès, nomEntréeÉlémentMéthode, valeurDescription, lireAttributs(valeurLecteur)));
            }
            return résultat;
        }
    }
    static final class DescripteurMéthode {
        final List<String> arguments = new ArrayList<>();
        final String résultatRetourner;
        DescripteurMéthode(String valeurDescription) {
            if (!valeurDescription.startsWith("(")) throw new ErreurTraduction("Fonction valeurDescription erreur: " + valeurDescription);
            int terminaison = valeurDescription.indexOf(')'); if (terminaison < 0) throw new ErreurTraduction("Fonction valeurDescription erreur: " + valeurDescription);
            arguments.addAll(analyserTypes(valeurDescription.substring(1, terminaison)));
            List<String> valeursRetourné = analyserTypes(valeurDescription.substring(terminaison + 1));
            if (arguments.contains("V") || valeursRetourné.size() != 1) throw new ErreurTraduction("Fonction valeurDescription erreur: " + valeurDescription);
            résultatRetourner = valeursRetourné.get(0);
        }
    }
    static List<String> analyserTypes(String valeurDescription) {
        List<String> résultat = new ArrayList<>();
        String[] formatAutorisé = {"Ljava/lang/String;", "[I", "I", "Z", "B", "C", "S", "V"};
        for (int position = 0; position < valeurDescription.length();) {
            String valeurSélection = null;
            for (String valeurFormat : formatAutorisé) if (valeurDescription.startsWith(valeurFormat, position)) { valeurSélection = valeurFormat; break; }
            if (valeurSélection == null) throw new ErreurTraduction("지원하지 않는 typeDonnées: " + valeurDescription);
            résultat.add(valeurSélection); position += valeurSélection.length();
        }
        return résultat;
    }
    static String symbole(String valeurGenre, String... parties) {
        try {
            byte[] fichierHachage = MessageDigest.getInstance("SHA-256").digest(String.join("\0", parties).getBytes(StandardCharsets.UTF_8));
            StringBuilder texte = new StringBuilder("j_" + valeurGenre + "_");
            for (int indiceOrdinal = 0; indiceOrdinal < 12; indiceOrdinal++) texte.append(String.format(Locale.ROOT, "%02x", fichierHachage[indiceOrdinal] & 255));
            return texte.toString();
        } catch (Exception erreur) { throw new ErreurTraduction(erreur.toString()); }
    }
    final Map<String, DonnéesClasse> listeClasses = new TreeMap<>();
    final Map<RéférenceMéthode, DonnéesMembre> listeMéthodes = new TreeMap<>(), listeChamps = new TreeMap<>();
    final Map<String, String> valeursChaîne = new LinkedHashMap<>(), fonctionsMachine = new LinkedHashMap<>();
    final String cibleExécution, classeMachine;
    final int nombreÉlémentsMotTas;
    final Path cheminRessource;
    CompilationAnticipée(List<Path> listeChemin, String valeurCible, int nombreÉlémentsMotLexical, Path valeurRessource) throws IOException {
        if ((!valeurCible.equals("kernel") && !valeurCible.equals("user")) || nombreÉlémentsMotLexical < 1024 || nombreÉlémentsMotLexical > 1048576) throw new ErreurTraduction("exécuterCommande valeurCible 또는 Mémoire régionAdresse taille erreur");
        cibleExécution = valeurCible; nombreÉlémentsMotTas = nombreÉlémentsMotLexical; cheminRessource = valeurRessource;
        // Ce nom est lui aussi traduit lors de la génération des sources par pays.
        classeMachine = valeurCible.equals("kernel") ? "CarteMatérielle" : "Utilisateur";
        for (String ligne : Files.readAllLines(valeurRessource.resolve("FonctionsMachine.tsv"), StandardCharsets.UTF_8)) {
            String[] parties = ligne.split("\t", -1);
            if (parties.length != 4) throw new ErreurTraduction("machine Fonction Données erreur");
            if (parties[0].equals(valeurCible)) fonctionsMachine.put(parties[1] + parties[2], parties[3]);
        }
        for (Path chemin : listeChemin) {
            DonnéesClasse Données = new DonnéesClasse(chemin);
            if (listeClasses.put(Données.nom, Données) != null) throw new ErreurTraduction("중복 valeurClasse: " + Données.nom);
            for (DonnéesMembre valeurChamp : Données.valeurChamp) {
                if ((valeurChamp.entréeÉlémentAccès & 8) == 0 || analyserTypes(valeurChamp.valeurDescription).equals(Collections.singletonList("V"))) throw new ErreurTraduction("valeurStatique 필드만 valeurPriseEnCharge");
                if (listeChamps.put(new RéférenceMéthode(Données.nom, valeurChamp.nom, valeurChamp.valeurDescription), valeurChamp) != null) throw new ErreurTraduction("중복 valeurChamp");
            }
            for (DonnéesMembre Fonction : Données.Fonction) {
                if (Fonction.nom.equals("<init>")) continue;
                if ((Fonction.entréeÉlémentAccès & 8) == 0 || (Fonction.entréeÉlémentAccès & (0x20 | 0x400)) != 0) throw new ErreurTraduction("valeurStatique 비동기화 함수만 valeurPriseEnCharge");
                new DescripteurMéthode(Fonction.valeurDescription);
                if (listeMéthodes.put(new RéférenceMéthode(Données.nom, Fonction.nom, Fonction.valeurDescription), Fonction) != null) throw new ErreurTraduction("중복 Fonction");
            }
        }
    }
    String symboleChaîne(String texte) { return valeursChaîne.computeIfAbsent(texte, valeur -> "j_text_" + valeursChaîne.size()); }
    String expressionConstante(DonnéesClasse Données, int numéro) {
        if (numéro < 1 || numéro >= Données.genreConstante.length) throw new ErreurTraduction("valeurConstante numéro rogner erreur");
        if (Données.genreConstante[numéro] == 3) return "(word)(uint32_t)(" + Données.donnéesConstante[numéro] + ")";
        if (Données.genreConstante[numéro] == 8) return "(word)" + symboleChaîne(Données.Caractères((Integer)Données.donnéesConstante[numéro]));
        throw new ErreurTraduction("정수와 Chaîne 상수만 valeurPriseEnCharge");
    }
    String prototypeMéthode(RéférenceMéthode référence) {
        List<String> listeArguments = new ArrayList<>(); int nombreÉlémentsÉlémentListe = new DescripteurMéthode(référence.valeurDescription).arguments.size();
        for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) listeArguments.add("word a" + indiceOrdinal);
        return "static word " + symbole("method", référence.parties()) + "(" + (nombreÉlémentsÉlémentListe == 0 ? "void" : String.join(", ", listeArguments)) + ")";
    }
    void contrôlerLocal(int numéro, int nombreÉlémentsVariableLocal) { if (numéro < 0 || numéro >= nombreÉlémentsVariableLocal) throw new ErreurTraduction("portéeLocal valeurVariable numéro rogner erreur"); }
    void émettreBranche(List<String> Sortie, Set<Integer> listeBranche, int position, int montantMouvement, String condition) {
        int valeurDestination = position + montantMouvement; listeBranche.add(valeurDestination);
        Sortie.add((condition == null ? "" : "if (" + condition + ") ") + "goto b" + valeurDestination + ";");
    }
    String corpsMéthode(RéférenceMéthode Fonction, DonnéesMembre Données) {
        byte[] donnéesCorps = Données.valeurAttribut.get("Code"); if (donnéesCorps == null) throw new ErreurTraduction("Fonction 몸체가 méthodeManquant: " + Fonction.nom);
        LecteurDonnées valeurLecteur = new LecteurDonnées(donnéesCorps); int profondeurPile = valeurLecteur.lireCourt(), nombreÉlémentsVariableLocal = valeurLecteur.lireCourt();
        LecteurDonnées donnéesCommande = new LecteurDonnées(valeurLecteur.lire(valeurLecteur.lireTypeEntier()));
        if (valeurLecteur.lireCourt() != 0) throw new ErreurTraduction("try/catch/finally estNonPrisEnCharge");
        DescripteurMéthode valeurFormat = new DescripteurMéthode(Fonction.valeurDescription); if (nombreÉlémentsVariableLocal < valeurFormat.arguments.size()) throw new ErreurTraduction("매개변수보다 적은 portéeLocal valeurVariable");
        DonnéesClasse valeurClasse = listeClasses.get(Fonction.valeurPropriétaire);
        List<String> Sortie = new ArrayList<>(); Sortie.add(prototypeMéthode(Fonction) + " {");
        Sortie.add("word s[" + Math.max(profondeurPile, 1) + "], l[" + Math.max(nombreÉlémentsVariableLocal, 1) + "] = {0}, a,b,c,d; size_t sp = 0;");
        for (int indiceOrdinal = 0; indiceOrdinal < valeurFormat.arguments.size(); indiceOrdinal++) Sortie.add("l[" + indiceOrdinal + "] = a" + indiceOrdinal + ";");
        Set<Integer> listeFrontières = new HashSet<>(), listeBranche = new HashSet<>();
        String[] listeComparaisons = {"==", "!=", "<", ">=", ">", "<=", "==", "!="};
        while (donnéesCommande.position < donnéesCommande.Données.length) {
            int position = donnéesCommande.position, commande = donnéesCommande.lireOctet(); listeFrontières.add(position); Sortie.add("b" + position + ":;");
            if (commande == 0) continue;
            if (commande == 1) Sortie.add("PUSH(0);");
            else if (commande >= 2 && commande <= 8) Sortie.add("PUSH((uint32_t)(" + (commande - 3) + "));");
            else if (commande == 16 || commande == 17) Sortie.add("PUSH((uint32_t)(" + (commande == 16 ? donnéesCommande.lireOctetSigné() : donnéesCommande.lireCourtSigné()) + "));");
            else if (commande == 18 || commande == 19) Sortie.add("PUSH(" + expressionConstante(valeurClasse, commande == 18 ? donnéesCommande.lireOctet() : donnéesCommande.lireCourt()) + ");");
            else if (commande == 21 || commande == 25 || (commande >= 26 && commande <= 29) || (commande >= 42 && commande <= 45)) {
                int numéro = commande == 21 || commande == 25 ? donnéesCommande.lireOctet() : commande - (commande <= 29 ? 26 : 42);
                contrôlerLocal(numéro, nombreÉlémentsVariableLocal); Sortie.add("PUSH(l[" + numéro + "]);");
            } else if (commande == 54 || commande == 58 || (commande >= 59 && commande <= 62) || (commande >= 75 && commande <= 78)) {
                int numéro = commande == 54 || commande == 58 ? donnéesCommande.lireOctet() : commande - (commande <= 62 ? 59 : 75);
                contrôlerLocal(numéro, nombreÉlémentsVariableLocal); Sortie.add("l[" + numéro + "] = POP();");
            } else if (commande == 46) Sortie.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
            else if (commande == 79) Sortie.add("c = POP(); b = POP(); a = POP(); *checked(a,(int32_t)b) = (uint32_t)c;");
            else if (commande == 87 || commande == 88) Sortie.add(commande == 87 ? "(void)POP();" : "(void)POP(); (void)POP();");
            else if (commande >= 89 && commande <= 95) {
                int[] comptagesÉlémentListe = {1,2,3,2,3,4,2}; String[] listeOrdre = {"aa","aba","acba","baba","bacba","badcba","ab"};
                for (int indiceOrdinal = 0; indiceOrdinal < comptagesÉlémentListe[commande - 89]; indiceOrdinal++) Sortie.add("abcd".charAt(indiceOrdinal) + " = POP();");
                for (char valeur : listeOrdre[commande - 89].toCharArray()) Sortie.add("PUSH(" + valeur + ");");
            } else if (commande == 96 || commande == 100 || commande == 104 || commande == 126 || commande == 128 || commande == 130) {
                String valeurOpération = commande == 96 ? "+" : commande == 100 ? "-" : commande == 104 ? "*" : commande == 126 ? "&" : commande == 128 ? "|" : "^";
                Sortie.add("b = POP(); a = POP(); PUSH((uint32_t)a " + valeurOpération + " (uint32_t)b);");
            } else if (commande == 108 || commande == 112) Sortie.add("b = POP(); a = POP(); PUSH(divide(a,b," + (commande == 112 ? 1 : 0) + "));");
            else if (commande == 116) Sortie.add("a = POP(); PUSH(0u-(uint32_t)a);");
            else if (commande == 120 || commande == 122 || commande == 124) {
                Sortie.add("b = POP(); a = POP();"); Sortie.add("PUSH(" + (commande == 122 ? "arithmetic_shift(a,b)" : "(uint32_t)a " + (commande == 120 ? "<<" : ">>") + " ((uint32_t)b & 31)") + ");");
            } else if (commande == 132) {
                int numéro = donnéesCommande.lireOctet(), montantIncrément = donnéesCommande.lireOctetSigné(); contrôlerLocal(numéro, nombreÉlémentsVariableLocal);
                Sortie.add("l[" + numéro + "] = (uint32_t)l[" + numéro + "] + (uint32_t)(" + montantIncrément + ");");
            } else if (commande >= 145 && commande <= 147) Sortie.add("a = POP(); PUSH((uint32_t)(" + (commande == 145 ? "int8_t" : commande == 146 ? "uint16_t" : "int16_t") + ")a);");
            else if (commande >= 153 && commande <= 158) {
                Sortie.add("a = POP();"); émettreBranche(Sortie, listeBranche, position, donnéesCommande.lireCourtSigné(), "(int32_t)a " + listeComparaisons[commande - 153] + " 0");
            } else if (commande >= 159 && commande <= 166) {
                Sortie.add("b = POP(); a = POP();"); émettreBranche(Sortie, listeBranche, position, donnéesCommande.lireCourtSigné(), commande >= 165 ? "a " + listeComparaisons[commande - 159] + " b" : "(int32_t)a " + listeComparaisons[commande - 159] + " (int32_t)b");
            } else if (commande == 167 || commande == 200) émettreBranche(Sortie, listeBranche, position, commande == 167 ? donnéesCommande.lireCourtSigné() : donnéesCommande.lireTypeEntier(), null);
            else if (commande == 170 || commande == 171) {
                while (donnéesCommande.position % 4 != 0) donnéesCommande.lireOctet();
                int valeurDéfaut = donnéesCommande.lireTypeEntier(); Sortie.add("a = POP();");
                if (commande == 170) {
                    int valeurBasExtrémité = donnéesCommande.lireTypeEntier(), valeurSommet = donnéesCommande.lireTypeEntier(); long nombreÉlémentsÉlémentListe = (long)valeurSommet - valeurBasExtrémité + 1;
                    if (nombreÉlémentsÉlémentListe < 1 || nombreÉlémentsÉlémentListe > (donnéesCommande.Données.length - donnéesCommande.position) / 4) throw new ErreurTraduction("switch rogner erreur");
                    for (long valeur = valeurBasExtrémité; valeur <= valeurSommet; valeur++) émettreBranche(Sortie, listeBranche, position, donnéesCommande.lireTypeEntier(), "(int32_t)a == (" + valeur + ")");
                } else {
                    int nombreÉlémentsÉlémentListe = donnéesCommande.lireTypeEntier(), donnéesAvantCôté = 0;
                    if (nombreÉlémentsÉlémentListe < 0 || nombreÉlémentsÉlémentListe > (donnéesCommande.Données.length - donnéesCommande.position) / 8) throw new ErreurTraduction("switch taille erreur");
                    for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) {
                        int valeur = donnéesCommande.lireTypeEntier(); if (indiceOrdinal > 0 && valeur <= donnéesAvantCôté) throw new ErreurTraduction("switch valeurOrdre erreur"); donnéesAvantCôté = valeur;
                        émettreBranche(Sortie, listeBranche, position, donnéesCommande.lireTypeEntier(), "(int32_t)a == (" + valeur + ")");
                    }
                }
                émettreBranche(Sortie, listeBranche, position, valeurDéfaut, null);
            } else if (commande == 172 || commande == 176 || commande == 177) Sortie.add("return " + (commande == 177 ? "0" : "POP()") + ";");
            else if (commande == 178 || commande == 179) {
                RéférenceMéthode référence = valeurClasse.référence(donnéesCommande.lireCourt()); if (!listeChamps.containsKey(référence)) throw new ErreurTraduction("알 nombre 없는 valeurChamp");
                Sortie.add(symbole("init", référence.valeurPropriétaire) + "();"); String valeurChamp = symbole("field", référence.parties());
                Sortie.add(commande == 178 ? "PUSH(" + valeurChamp + ");" : valeurChamp + " = POP();");
            } else if (commande == 184) {
                RéférenceMéthode référence = valeurClasse.référence(donnéesCommande.lireCourt()); if (!listeMéthodes.containsKey(référence)) throw new ErreurTraduction("알 nombre 없는 Fonction");
                DescripteurMéthode typeInvocation = new DescripteurMéthode(référence.valeurDescription); int nombreÉlémentsÉlémentListe = typeInvocation.arguments.size();
                Sortie.add(symbole("init", référence.valeurPropriétaire) + "();"); Sortie.add("if(sp < " + nombreÉlémentsÉlémentListe + ") kernel_panic(\"call stack underflow\"); sp -= " + nombreÉlémentsÉlémentListe + ";");
                List<String> argumentsInvocation = new ArrayList<>(); for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) argumentsInvocation.add("s[sp + " + indiceOrdinal + "]");
                Sortie.add("a = " + symbole("method", référence.parties()) + "(" + String.join(",", argumentsInvocation) + ");");
                if (!typeInvocation.résultatRetourner.equals("V")) Sortie.add("PUSH(a);");
            } else if (commande == 182) {
                RéférenceMéthode référence = valeurClasse.référence(donnéesCommande.lireCourt());
                if (référence.equals(new RéférenceMéthode("java/lang/String", "length", "()I"))) Sortie.add("a = POP(); PUSH(length(a));");
                else if (référence.equals(new RéférenceMéthode("java/lang/String", "charAt", "(I)C"))) Sortie.add("b = POP(); a = POP(); PUSH(*checked(a,(int32_t)b));");
                else throw new ErreurTraduction("가상 Fonction invoquer estNonPrisEnCharge");
            } else if (commande == 188) {
                if (donnéesCommande.lireOctet() != 10) throw new ErreurTraduction("new int[]만 valeurPriseEnCharge"); Sortie.add("a = POP(); PUSH(new_array((int32_t)a));");
            } else if (commande == 190) Sortie.add("a = POP(); PUSH(length(a));");
            else if (commande == 196) {
                int valeurExtension = donnéesCommande.lireOctet(), numéro = donnéesCommande.lireCourt(); contrôlerLocal(numéro, nombreÉlémentsVariableLocal);
                if (valeurExtension == 21 || valeurExtension == 25) Sortie.add("PUSH(l[" + numéro + "]);");
                else if (valeurExtension == 54 || valeurExtension == 58) Sortie.add("l[" + numéro + "] = POP();");
                else if (valeurExtension == 132) Sortie.add("l[" + numéro + "] = (uint32_t)l[" + numéro + "] + (uint32_t)(" + donnéesCommande.lireCourtSigné() + ");");
                else throw new ErreurTraduction("estNonPrisEnCharge wide commande");
            } else if (commande == 198 || commande == 199) {
                Sortie.add("a = POP();"); émettreBranche(Sortie, listeBranche, position, donnéesCommande.lireCourtSigné(), "a " + (commande == 198 ? "==" : "!=") + " 0");
            } else throw new ErreurTraduction(Fonction.valeurPropriétaire + "." + Fonction.nom + ", valeurOctet " + position + ": estNonPrisEnCharge commande " + commande);
        }
        if (!listeFrontières.containsAll(listeBranche)) throw new ErreurTraduction("commande 경계가 아닌 곳으로 branche");
        Sortie.add("kernel_panic(\"method fell through\"); }"); return String.join("\n", Sortie);
    }
    String méthodeExporter(String symboleLier, String valeurCible, boolean possèdePointEntréeÉlément) {
        int indicePosition = valeurCible.lastIndexOf('.'); if (indicePosition < 0 || !symboleLier.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ErreurTraduction("émettreValeur valeurAffecter erreur");
        String valeurPropriétaire = valeurCible.substring(0, indicePosition).replace('.', '/'), nom = valeurCible.substring(indicePosition + 1); RéférenceMéthode valeurSélection = null;
        for (RéférenceMéthode référence : listeMéthodes.keySet()) if (référence.valeurPropriétaire.equals(valeurPropriétaire) && référence.nom.equals(nom)) {
            if (valeurSélection != null) throw new ErreurTraduction("겹친 émettreValeur valeurCible"); valeurSélection = référence;
        }
        if (valeurSélection == null || (listeMéthodes.get(valeurSélection).entréeÉlémentAccès & 0x100) != 0) throw new ErreurTraduction("내보낼 함수가 méthodeManquant 또는 native Fonction");
        DescripteurMéthode valeurFormat = new DescripteurMéthode(valeurSélection.valeurDescription);
        if ((possèdePointEntréeÉlément && !valeurFormat.arguments.isEmpty()) || !Arrays.asList("V", "I").contains(valeurFormat.résultatRetourner)) throw new ErreurTraduction("valeurPointEntréeÉlément 또는 C valeurFrontière valeurFormat erreur");
        List<String> listeArguments = new ArrayList<>(), argumentsInvocation = new ArrayList<>();
        for (int indiceOrdinal = 0; indiceOrdinal < valeurFormat.arguments.size(); indiceOrdinal++) {
            if (!valeurFormat.arguments.get(indiceOrdinal).equals("I")) throw new ErreurTraduction("C 경계는 int 인수만 valeurPriseEnCharge");
            listeArguments.add("int32_t a" + indiceOrdinal); argumentsInvocation.add("(uint32_t)a" + indiceOrdinal);
        }
        return (valeurFormat.résultatRetourner.equals("V") ? "void " : "int32_t ") + symboleLier + "(" + (listeArguments.isEmpty() ? "void" : String.join(",", listeArguments)) + ") { " + symbole("init", valeurSélection.valeurPropriétaire) + "(); " + (valeurFormat.résultatRetourner.equals("V") ? "" : "return (int32_t)") + symbole("method", valeurSélection.parties()) + "(" + String.join(",", argumentsInvocation) + "); }";
    }
    String générer(String pointEntréeÉlément, List<String> entréesListeExporter, boolean notationUniversel) throws IOException {
        List<String> listeDéclarations = new ArrayList<>(), listeCorpsListe = new ArrayList<>(), déclarationsChamp = new ArrayList<>();
        for (Map.Entry<RéférenceMéthode, DonnéesMembre> valeurEntréeÉlément : listeMéthodes.entrySet()) {
            RéférenceMéthode référence = valeurEntréeÉlément.getKey(); DonnéesMembre Données = valeurEntréeÉlément.getValue(); listeDéclarations.add(prototypeMéthode(référence) + ";");
            if ((Données.entréeÉlémentAccès & 0x100) != 0) {
                String connecter = fonctionsMachine.get(référence.nom + référence.valeurDescription);
                if (!référence.valeurPropriétaire.equals(classeMachine) || connecter == null) throw new ErreurTraduction("허용되지 않은 native Fonction: " + référence.nom);
                int nombreÉlémentsÉlémentListe = new DescripteurMéthode(référence.valeurDescription).arguments.size(); List<String> listeArguments = new ArrayList<>();
                for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) listeArguments.add("a" + indiceOrdinal);
                listeDéclarations.add("extern word " + connecter + "(" + (nombreÉlémentsÉlémentListe == 0 ? "void" : String.join(",", Collections.nCopies(nombreÉlémentsÉlémentListe, "word"))) + ");");
                listeCorpsListe.add(prototypeMéthode(référence) + " { return " + connecter + "(" + String.join(",", listeArguments) + "); }");
            } else listeCorpsListe.add(corpsMéthode(référence, Données));
        }
        for (Map.Entry<RéférenceMéthode, DonnéesMembre> valeurEntréeÉlément : listeChamps.entrySet()) {
            RéférenceMéthode référence = valeurEntréeÉlément.getKey(); byte[] valeurConstante = valeurEntréeÉlément.getValue().valeurAttribut.get("ConstantValue");
            String valeur = valeurConstante == null ? "0" : expressionConstante(listeClasses.get(référence.valeurPropriétaire), new LecteurDonnées(valeurConstante).lireCourt());
            déclarationsChamp.add("static word " + symbole("field", référence.parties()) + " = " + valeur + ";");
        }
        for (String nom : listeClasses.keySet()) {
            String initialiser = symbole("init", nom), valeurÉtatValeur = symbole("state", nom);
            listeDéclarations.add("static void " + initialiser + "(void);"); déclarationsChamp.add("static unsigned " + valeurÉtatValeur + ";");
            RéférenceMéthode référence = new RéférenceMéthode(nom, "<clinit>", "()V");
            listeCorpsListe.add("static void " + initialiser + "(void) { if(" + valeurÉtatValeur + ") return; " + valeurÉtatValeur + " = 1; " + (listeMéthodes.containsKey(référence) ? symbole("method", référence.parties()) + "(); " : "") + valeurÉtatValeur + " = 2; }");
        }
        listeCorpsListe.add(méthodeExporter("java_entry", pointEntréeÉlément, true)); Set<String> nomExporté = new HashSet<>();
        for (String valeurAffecter : entréesListeExporter) {
            int indicePosition = valeurAffecter.indexOf('='); if (indicePosition < 1) throw new ErreurTraduction("émettreValeur valeurAffecter erreur");
            String nom = valeurAffecter.substring(0, indicePosition); nomExporté.add(nom); listeCorpsListe.add(méthodeExporter(nom, valeurAffecter.substring(indicePosition + 1), false));
        }
        List<String> déclarationsChaîne = new ArrayList<>();
        for (Map.Entry<String, String> valeurEntréeÉlément : valeursChaîne.entrySet()) {
            String texte = valeurEntréeÉlément.getKey(); StringBuilder valeurTableau = new StringBuilder("static const word " + valeurEntréeÉlément.getValue() + "[] = {" + texte.length());
            for (int indiceOrdinal = 0; indiceOrdinal < texte.length(); indiceOrdinal++) valeurTableau.append(", ").append((int)texte.charAt(indiceOrdinal));
            déclarationsChaîne.add(valeurTableau.append("};").toString());
        }
        String valeurPriseEnCharge = Files.readString(cheminRessource.resolve("PriseEnChargeEnvironnementExécution.c.txt"), StandardCharsets.UTF_8).replace("262144", Integer.toString(nombreÉlémentsMotTas));
        return localiserSourceGénéré(valeurPriseEnCharge + String.join("\n", déclarationsChaîne) + "\n" + String.join("\n", listeDéclarations) + "\n" + String.join("\n", déclarationsChamp) + "\n" + String.join("\n", listeCorpsListe) + "\n", nomExporté, notationUniversel);
    }
    String localiserSourceGénéré(String source, Set<String> nomExporté, boolean notationUniversel) throws IOException {
        Map<String, String> tableNom = new HashMap<>();
        for (String ligne : Files.readAllLines(cheminRessource.resolve("NomsGénéré.tsv"), StandardCharsets.UTF_8)) {
            String[] valeurPaire = ligne.split("\t"); tableNom.put(valeurPaire[0], valeurPaire[1]);
        }
        Pattern expressionFragmentBloc = Pattern.compile("//[^\\n]*|/\\*[\\s\\S]*?\\*/|\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'|\\b[A-Za-z_]\\w*\\b");
        Matcher valeurRechercheur = expressionFragmentBloc.matcher(source); StringBuffer résultat = new StringBuffer();
        while (valeurRechercheur.find()) {
            String nom = valeurRechercheur.group(), nomNouveau = nom;
            if (!nom.startsWith("//") && !nom.startsWith("/*") && !nom.startsWith("\"") && !nom.startsWith("'") && !nomExporté.contains(nom)) {
                nomNouveau = tableNom.getOrDefault(nom, nom);
                if (nom.matches("a[0-9]+")) nomNouveau = "arguments" + nom.substring(1);
                if (nom.matches("b[0-9]+")) nomNouveau = "branche" + nom.substring(1);
                if (notationUniversel) {
                    StringBuilder valeurNotation = new StringBuilder();
                    for (char valeurCaractère : nomNouveau.toCharArray()) valeurNotation.append(valeurCaractère < 128 ? Character.toString(valeurCaractère) : String.format(Locale.ROOT, "\\u%04x", (int)valeurCaractère));
                    nomNouveau = valeurNotation.toString();
                }
            }
            valeurRechercheur.appendReplacement(résultat, Matcher.quoteReplacement(nomNouveau));
        }
        valeurRechercheur.appendTail(résultat); return résultat.toString();
    }
    String corpsMéthodeX86(RéférenceMéthode Fonction, DonnéesMembre Données, Map<String,String> tableMachine, String valeurCible) {
        String valeurMarqueur = symbole("method", Fonction.parties());
        List<String> ligne = new ArrayList<>();
        if ((Données.entréeÉlémentAccès & 0x100) != 0) {
            String connecter = tableMachine.get(Fonction.nom + Fonction.valeurDescription);
            if (!Fonction.valeurPropriétaire.equals(valeurCible.equals("kernel") ? "Périphérique" : "Utilisateur") || connecter == null) throw new ErreurTraduction("허용되지 않은 native Fonction");
            return ".text\n" + valeurMarqueur + ":\njmp " + connecter;
        }
        byte[] texteCorps = Données.valeurAttribut.get("Code"); if (texteCorps == null) throw new ErreurTraduction("Fonction 몸체가 méthodeManquant");
        LecteurDonnées valeurLecteur = new LecteurDonnées(texteCorps); valeurLecteur.lireCourt(); int nombreÉlémentsLocal = valeurLecteur.lireCourt();
        LecteurDonnées donnéesCommande = new LecteurDonnées(valeurLecteur.lire(valeurLecteur.lireTypeEntier()));
        if (valeurLecteur.lireCourt() != 0) throw new ErreurTraduction("try/catch/finally estNonPrisEnCharge");
        DescripteurMéthode valeurFormat = new DescripteurMéthode(Fonction.valeurDescription); if (nombreÉlémentsLocal < valeurFormat.arguments.size()) throw new ErreurTraduction("매개변수보다 적은 portéeLocal valeurVariable");
        Collections.addAll(ligne,".text",".globl " + valeurMarqueur,".type " + valeurMarqueur + ", @function",valeurMarqueur + ":","pushl %ebp","movl %esp, %ebp","subl $" + nombreÉlémentsLocal * 4 + ", %esp");
        for (int indiceOrdinal = 0; indiceOrdinal < valeurFormat.arguments.size(); indiceOrdinal++) Collections.addAll(ligne,"movl " + (8 + 4 * (valeurFormat.arguments.size() - indiceOrdinal - 1)) + "(%ebp), %eax","movl %eax, -" + (4 * (indiceOrdinal + 1)) + "(%ebp)");
        DonnéesClasse valeurClasse = listeClasses.get(Fonction.valeurPropriétaire); Set<Integer> listeFrontières = new HashSet<>(), listeBranche = new HashSet<>();
        String[] listeComparaisons = {"je","jne","jl","jge","jg","jle","je","jne"};
        while (donnéesCommande.position < donnéesCommande.Données.length) {
            int position = donnéesCommande.position, commande = donnéesCommande.lireOctet(); String indicePosition = valeurMarqueur + "_b" + position;
            ligne.add(indicePosition + ":"); listeFrontières.add(position);
            if (commande == 0) ligne.add("nop");
            else if (commande == 1) ligne.add("pushl $0");
            else if (commande >= 2 && commande <= 8) ligne.add("pushl $" + (commande - 3));
            else if (commande == 16 || commande == 17) ligne.add("pushl $" + (commande == 16 ? donnéesCommande.lireOctetSigné() : donnéesCommande.lireCourtSigné()));
            else if (commande == 18 || commande == 19) {
                int numéro = commande == 18 ? donnéesCommande.lireOctet() : donnéesCommande.lireCourt();
                ligne.add("pushl $" + constanteX86(valeurClasse,numéro));
            } else if (commande == 21 || commande == 25 || (commande >= 26 && commande <= 29) || (commande >= 42 && commande <= 45) || commande == 54 || commande == 58 || (commande >= 59 && commande <= 62) || (commande >= 75 && commande <= 78)) {
                boolean lireRésultat = commande < 54; int numéro = commande == 21 || commande == 25 || commande == 54 || commande == 58 ? donnéesCommande.lireOctet() : commande - (commande <= 29 ? 26 : commande <= 45 ? 42 : commande <= 62 ? 59 : 75);
                contrôlerLocal(numéro,nombreÉlémentsLocal); ligne.add((lireRésultat ? "pushl " : "popl ") + "-" + (4 * (numéro + 1)) + "(%ebp)");
            } else if (commande == 46) Collections.addAll(ligne,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
            else if (commande == 79) Collections.addAll(ligne,"popl %edx","popl %ecx","popl %eax","call rt_array_check","movl %edx, 4(%eax,%ecx,4)");
            else if (commande == 87 || commande == 88) ligne.add("addl $" + (commande == 87 ? 4 : 8) + ", %esp");
            else if (commande >= 89 && commande <= 95) {
                int[] comptagesÉlémentListe = {1,2,3,2,3,4,2}; int[][] listeOrdre = {{0,0},{0,1,0},{0,2,1,0},{1,0,1,0},{1,0,2,1,0},{1,0,3,2,1,0},{0,1}}; String[] registreValeurs = {"%eax","%ecx","%edx","%ebx"};
                for (int indiceOrdinal = 0; indiceOrdinal < comptagesÉlémentListe[commande - 89]; indiceOrdinal++) ligne.add("popl " + registreValeurs[indiceOrdinal]);
                for (int indiceOrdinal : listeOrdre[commande - 89]) ligne.add("pushl " + registreValeurs[indiceOrdinal]);
            } else if (commande == 96 || commande == 100 || commande == 104 || commande == 126 || commande == 128 || commande == 130) {
                String valeurOpération = commande == 96 ? "addl" : commande == 100 ? "subl" : commande == 104 ? "imull" : commande == 126 ? "andl" : commande == 128 ? "orl" : "xorl";
                Collections.addAll(ligne,"popl %ecx","popl %eax",valeurOpération + " %ecx, %eax","pushl %eax");
            } else if (commande == 108 || commande == 112) Collections.addAll(ligne,"popl %ecx","popl %eax","testl %ecx, %ecx","jz rt_div_zero","cmpl $-1, %ecx","jne " + indicePosition + "_divide","cmpl $0x80000000, %eax","jne " + indicePosition + "_divide","xorl %edx, %edx","jmp " + indicePosition + "_done",indicePosition + "_divide:","cltd","idivl %ecx",indicePosition + "_done:","pushl " + (commande == 108 ? "%eax" : "%edx"));
            else if (commande == 116) ligne.add("negl (%esp)");
            else if (commande == 120 || commande == 122 || commande == 124) Collections.addAll(ligne,"popl %ecx","popl %eax",(commande == 120 ? "sall" : commande == 122 ? "sarl" : "shrl") + " %cl, %eax","pushl %eax");
            else if (commande == 132) {
                int numéro = donnéesCommande.lireOctet(), valeurIncrément = donnéesCommande.lireOctetSigné(); contrôlerLocal(numéro,nombreÉlémentsLocal); ligne.add("addl $" + valeurIncrément + ", -" + (4 * (numéro + 1)) + "(%ebp)");
            } else if (commande >= 145 && commande <= 147) Collections.addAll(ligne,"popl %eax",commande == 145 ? "movsbl %al, %eax" : commande == 146 ? "movzwl %ax, %eax" : "movswl %ax, %eax","pushl %eax");
            else if (commande >= 153 && commande <= 166) {
                if (commande <= 158) Collections.addAll(ligne,"popl %eax","testl %eax, %eax");
                else Collections.addAll(ligne,"popl %ecx","popl %eax","cmpl %ecx, %eax");
                int valeurDestination = position + donnéesCommande.lireCourtSigné(); listeBranche.add(valeurDestination); ligne.add(listeComparaisons[commande - (commande <= 158 ? 153 : 159)] + " " + valeurMarqueur + "_b" + valeurDestination);
            } else if (commande == 167 || commande == 200) {
                int valeurDestination = position + (commande == 167 ? donnéesCommande.lireCourtSigné() : donnéesCommande.lireTypeEntier()); listeBranche.add(valeurDestination); ligne.add("jmp " + valeurMarqueur + "_b" + valeurDestination);
            } else if (commande == 170 || commande == 171) {
                while (donnéesCommande.position % 4 != 0) donnéesCommande.lireOctet();
                int valeurDéfaut = position + donnéesCommande.lireTypeEntier(); listeBranche.add(valeurDéfaut); ligne.add("popl %eax");
                int nombreÉlémentsÉlémentListe, valeurBasExtrémité = 0;
                if (commande == 170) { valeurBasExtrémité = donnéesCommande.lireTypeEntier(); int valeurSommet = donnéesCommande.lireTypeEntier(); long longueur = (long)valeurSommet - valeurBasExtrémité + 1; if (longueur < 1 || longueur > (donnéesCommande.Données.length - donnéesCommande.position) / 4) throw new ErreurTraduction("switch rogner erreur"); nombreÉlémentsÉlémentListe = (int)longueur; }
                else { nombreÉlémentsÉlémentListe = donnéesCommande.lireTypeEntier(); if (nombreÉlémentsÉlémentListe < 0 || nombreÉlémentsÉlémentListe > (donnéesCommande.Données.length - donnéesCommande.position) / 8) throw new ErreurTraduction("switch taille erreur"); }
                for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) {
                    int valeur = commande == 170 ? valeurBasExtrémité + indiceOrdinal : donnéesCommande.lireTypeEntier(), valeurDestination = position + donnéesCommande.lireTypeEntier(); listeBranche.add(valeurDestination);
                    Collections.addAll(ligne,"cmpl $" + valeur + ", %eax","je " + valeurMarqueur + "_b" + valeurDestination);
                }
                ligne.add("jmp " + valeurMarqueur + "_b" + valeurDéfaut);
            } else if (commande == 172 || commande == 176 || commande == 177) {
                if (commande != 177) ligne.add("popl %eax"); Collections.addAll(ligne,"leave","ret");
            } else if (commande == 178 || commande == 179) {
                RéférenceMéthode référence = valeurClasse.référence(donnéesCommande.lireCourt()); if (!listeChamps.containsKey(référence)) throw new ErreurTraduction("알 nombre 없는 valeurChamp");
                Collections.addAll(ligne,"call " + symbole("init",référence.valeurPropriétaire),(commande == 178 ? "pushl " : "popl ") + symbole("field",référence.parties()));
            } else if (commande == 184) {
                RéférenceMéthode référence = valeurClasse.référence(donnéesCommande.lireCourt()); if (!listeMéthodes.containsKey(référence)) throw new ErreurTraduction("알 nombre 없는 Fonction");
                DescripteurMéthode typeInvocation = new DescripteurMéthode(référence.valeurDescription); Collections.addAll(ligne,"call " + symbole("init",référence.valeurPropriétaire),"call " + symbole("method",référence.parties()));
                if (!typeInvocation.arguments.isEmpty()) ligne.add("addl $" + typeInvocation.arguments.size() * 4 + ", %esp");
                if (!typeInvocation.résultatRetourner.equals("V")) ligne.add("pushl %eax");
            } else if (commande == 182) {
                RéférenceMéthode référence = valeurClasse.référence(donnéesCommande.lireCourt());
                if (référence.equals(new RéférenceMéthode("java/lang/String","length","()I"))) Collections.addAll(ligne,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
                else if (référence.equals(new RéférenceMéthode("java/lang/String","charAt","(I)C"))) Collections.addAll(ligne,"popl %ecx","popl %eax","call rt_array_check","pushl 4(%eax,%ecx,4)");
                else throw new ErreurTraduction("가상 Fonction invoquer estNonPrisEnCharge");
            } else if (commande == 188) {
                if (donnéesCommande.lireOctet() != 10) throw new ErreurTraduction("new int[]만 valeurPriseEnCharge"); Collections.addAll(ligne,"popl %eax","call rt_new_array","pushl %eax");
            } else if (commande == 190) Collections.addAll(ligne,"popl %eax","testl %eax, %eax","jz rt_null","pushl (%eax)");
            else if (commande == 196) {
                int valeurExtension = donnéesCommande.lireOctet(), numéro = donnéesCommande.lireCourt(); contrôlerLocal(numéro,nombreÉlémentsLocal);
                if (valeurExtension == 21 || valeurExtension == 25 || valeurExtension == 54 || valeurExtension == 58) ligne.add((valeurExtension <= 25 ? "pushl " : "popl ") + "-" + 4 * (numéro + 1) + "(%ebp)");
                else if (valeurExtension == 132) ligne.add("addl $" + donnéesCommande.lireCourtSigné() + ", -" + 4 * (numéro + 1) + "(%ebp)");
                else throw new ErreurTraduction("wide commande estNonPrisEnCharge");
            } else if (commande == 198 || commande == 199) {
                int valeurDestination = position + donnéesCommande.lireCourtSigné(); listeBranche.add(valeurDestination); Collections.addAll(ligne,"popl %eax","testl %eax, %eax",(commande == 198 ? "je " : "jne ") + valeurMarqueur + "_b" + valeurDestination);
            } else throw new ErreurTraduction("estNonPrisEnCharge commande: " + commande);
        }
        if (!listeFrontières.containsAll(listeBranche)) throw new ErreurTraduction("commande 경계가 아닌 곳으로 branche");
        ligne.add(".size " + valeurMarqueur + ", .-" + valeurMarqueur); return String.join("\n",ligne);
    }
    String constanteX86(DonnéesClasse Données, int numéro) {
        if (Données.genreConstante[numéro] == 3) return Données.donnéesConstante[numéro].toString();
        if (Données.genreConstante[numéro] == 8) return symboleChaîne(Données.Caractères((Integer)Données.donnéesConstante[numéro]));
        throw new ErreurTraduction("정수와 Chaîne 상수만 valeurPriseEnCharge");
    }
    String assembleurX86(String pointEntréeÉlément, List<String> valeurExporté, String valeurCible) throws IOException {
        Map<String,String> tableMachine = new HashMap<>();
        for (String ligne : Files.readAllLines(cheminRessource.resolve("FonctionsMachineX86.tsv"))) { String[] valeurPaire = ligne.split("\t"); if (valeurPaire[0].equals(valeurCible)) tableMachine.put(valeurPaire[1] + valeurPaire[2],valeurPaire[3]); }
        int indicePosition = pointEntréeÉlément.lastIndexOf('.'); if (indicePosition < 0) throw new ErreurTraduction("pointEntréeÉlément valeurAffecter erreur");
        String valeurPropriétaire = pointEntréeÉlément.substring(0,indicePosition).replace('.','/'), nomEntréeÉlémentMéthode = pointEntréeÉlément.substring(indicePosition + 1); RéférenceMéthode valeurPointEntréeÉlément = null;
        for (String valeurDescription : Arrays.asList("()I","()V")) { RéférenceMéthode référence = new RéférenceMéthode(valeurPropriétaire,nomEntréeÉlémentMéthode,valeurDescription); if (listeMéthodes.containsKey(référence)) { if (valeurPointEntréeÉlément != null) throw new ErreurTraduction("겹친 pointEntréeÉlément"); valeurPointEntréeÉlément = référence; } }
        if (valeurPointEntréeÉlément == null || (listeMéthodes.get(valeurPointEntréeÉlément).entréeÉlémentAccès & 0x100) != 0) throw new ErreurTraduction("valeurPointEntréeÉlément Fonction valeurFormat erreur");
        List<String> ligne = new ArrayList<>(); ligne.add(".code32");
        for (DonnéesClasse Données : listeClasses.values()) {
            String valeurÉtatValeur = symbole("state",Données.nom), initialiser = symbole("init",Données.nom);
            Collections.addAll(ligne,".bss",".balign 4",valeurÉtatValeur + ": .long 0",".text",initialiser + ":","cmpl $0, " + valeurÉtatValeur,"jne " + initialiser + "_done","movl $1, " + valeurÉtatValeur);
            RéférenceMéthode référenceInitialiseur = new RéférenceMéthode(Données.nom,"<clinit>","()V"); if (listeMéthodes.containsKey(référenceInitialiseur)) ligne.add("call " + symbole("method",référenceInitialiseur.parties()));
            Collections.addAll(ligne,"movl $2, " + valeurÉtatValeur,initialiser + "_done:","ret");
            for (DonnéesMembre valeurChamp : Données.valeurChamp) {
                byte[] valeurConstante = valeurChamp.valeurAttribut.get("ConstantValue"); String valeur = valeurConstante == null ? "0" : constanteX86(Données,new LecteurDonnées(valeurConstante).lireCourt());
                Collections.addAll(ligne,".data",".balign 4",symbole("field",Données.nom,valeurChamp.nom,valeurChamp.valeurDescription) + ": .long " + valeur);
            }
            for (DonnéesMembre Fonction : Données.Fonction) if (!Fonction.nom.equals("<init>")) ligne.add(corpsMéthodeX86(new RéférenceMéthode(Données.nom,Fonction.nom,Fonction.valeurDescription),Fonction,tableMachine,valeurCible));
        }
        Collections.addAll(ligne,".text",".globl java_entry","java_entry:","call " + symbole("init",valeurPointEntréeÉlément.valeurPropriétaire),"call " + symbole("method",valeurPointEntréeÉlément.parties()));
        if (valeurPointEntréeÉlément.valeurDescription.equals("()V")) ligne.add("xorl %eax, %eax"); ligne.add("ret");
        for (String valeurAffecter : valeurExporté) {
            int valeurDélimiteur = valeurAffecter.indexOf('='); if (valeurDélimiteur < 1) throw new ErreurTraduction("émettreValeur valeurAffecter erreur");
            String valeurExtérieur = valeurAffecter.substring(0,valeurDélimiteur), Fonction = valeurAffecter.substring(valeurDélimiteur + 1); int résultatDivision = Fonction.lastIndexOf('.');
            if (résultatDivision < 0 || !valeurExtérieur.matches("[A-Za-z_][A-Za-z0-9_]*")) throw new ErreurTraduction("émettreValeur symbole erreur");
            String valeurClasse = Fonction.substring(0,résultatDivision).replace('.','/'), nom = Fonction.substring(résultatDivision + 1); RéférenceMéthode valeurSélection = null;
            for (RéférenceMéthode référence : listeMéthodes.keySet()) if (référence.valeurPropriétaire.equals(valeurClasse) && référence.nom.equals(nom)) { if (valeurSélection != null) throw new ErreurTraduction("겹친 émettreValeur valeurCible"); valeurSélection = référence; }
            if (valeurSélection == null) throw new ErreurTraduction("내보낼 함수가 méthodeManquant");
            Collections.addAll(ligne,".text",".globl " + valeurExtérieur,valeurExtérieur + ":","call " + symbole("init",valeurSélection.valeurPropriétaire),"jmp " + symbole("method",valeurSélection.parties()));
        }
        ligne.add(".section .rodata");
        for (Map.Entry<String,String> valeurEntréeÉlément : valeursChaîne.entrySet()) {
            Collections.addAll(ligne,".balign 4",valeurEntréeÉlément.getValue() + ":",".long " + valeurEntréeÉlément.getKey().length());
            List<String> listeUnités = new ArrayList<>(); for (char valeurUnité : valeurEntréeÉlément.getKey().toCharArray()) listeUnités.add(Integer.toString(valeurUnité)); if (!listeUnités.isEmpty()) ligne.add(".long " + String.join(",",listeUnités));
        }
        ligne.add(".section .note.GNU-stack,\"\",@progbits"); return String.join("\n",ligne) + "\n";
    }
    static void exécuterOutil(List<String> commande) throws Exception {
        if (new ProcessBuilder(commande).inheritIO().start().waitFor() != 0) throw new ErreurTraduction("compilerSource erreur: " + commande.get(0));
    }
    static String chaîneDonnées(String texte) { return "\"" + texte.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r").replace("\t","\\t") + "\""; }
    static void traductionX86(List<Path> listeEntrée, String valeurCible, String pointEntréeÉlément, List<String> valeurExporté, Path Sortie, Path valeurRessource) throws Exception {
        Path valeurTemporaire = Files.createTempDirectory("jkoros-java-x86-"), cheminClasse = valeurTemporaire.resolve("classes"); Files.createDirectory(cheminClasse);
        try {
            List<String> commandeJava = new ArrayList<>(Arrays.asList("javac","-J-XX:-UsePerfData","--release","8","-encoding","UTF-8","-g:none","-proc:none","-implicit:none","-classpath",cheminClasse.toString(),"-sourcepath",cheminClasse.toString(),"-d",cheminClasse.toString()));
            List<Path> codeOctets = new ArrayList<>(); int nombreÉlémentsSource = 0;
            for (Path valeurEntrée : listeEntrée) {
                if (Sortie.toAbsolutePath().normalize().equals(valeurEntrée.toAbsolutePath().normalize())) throw new ErreurTraduction("Sortie 파일과 입력이 texteÉgal");
                if (valeurEntrée.toString().endsWith(".java")) { commandeJava.add(valeurEntrée.toString()); nombreÉlémentsSource++; }
                else if (valeurEntrée.toString().endsWith(".class")) codeOctets.add(valeurEntrée);
                else throw new ErreurTraduction(".java 또는 .class만 valeurPriseEnCharge");
            }
            if (nombreÉlémentsSource > 0) exécuterOutil(commandeJava);
            try (java.util.stream.Stream<Path> listeChemin = Files.walk(cheminClasse)) { listeChemin.filter(chemin -> chemin.toString().endsWith(".class")).sorted().forEach(codeOctets::add); }
            CompilationAnticipée convertirValeur = new CompilationAnticipée(codeOctets,valeurCible.equals("user") ? "user" : "kernel",262144,valeurRessource);
            String assemblerValeur = convertirValeur.assembleurX86(pointEntréeÉlément,valeurExporté,valeurCible); Files.writeString(valeurTemporaire.resolve("program.s"),assemblerValeur,StandardCharsets.UTF_8);
            Path positionOutil = valeurRessource.getParent();
            exécuterOutil(Arrays.asList("as","--32","-o",valeurTemporaire.resolve("program.o").toString(),valeurTemporaire.resolve("program.s").toString()));
            exécuterOutil(Arrays.asList("as","--32","-o",valeurTemporaire.resolve("runtime.o").toString(),positionOutil.resolve("PriseEnChargeEnvironnementExécution.s").toString()));
            List<String> connecter = new ArrayList<>(Arrays.asList("ld","-m","elf_i386"));
            if (valeurCible.equals("kernel")) connecter.add("-r");
            else {
                exécuterOutil(Arrays.asList("as","--32","-o",valeurTemporaire.resolve("start.o").toString(),positionOutil.resolve(valeurCible.equals("user") ? "démarrerProgrammeUtilisateur.s" : "démarrageLinux.s").toString()));
                Collections.addAll(connecter,"-e","_start",valeurTemporaire.resolve("start.o").toString());
                if (valeurCible.equals("user")) Collections.addAll(connecter,"-T",positionOutil.resolve("dispositionLierUtilisateur.ld").toString());
            }
            Collections.addAll(connecter,"-o",valeurTemporaire.resolve("result").toString(),valeurTemporaire.resolve("program.o").toString(),valeurTemporaire.resolve("runtime.o").toString()); exécuterOutil(connecter);
            Sortie = Sortie.toAbsolutePath(); Files.createDirectories(Sortie.getParent()); Path valeurPublier = Files.createTempFile(Sortie.getParent(),".elf-",".tmp");
            try { Files.copy(valeurTemporaire.resolve("result"),valeurPublier,StandardCopyOption.REPLACE_EXISTING); Files.move(valeurPublier,Sortie,StandardCopyOption.REPLACE_EXISTING); } finally { Files.deleteIfExists(valeurPublier); }
            Files.setPosixFilePermissions(Sortie,java.nio.file.attribute.PosixFilePermissions.fromString(valeurCible.equals("linux") ? "rwxr-xr-x" : "rw-r--r--"));
            Files.writeString(Paths.get(Sortie + ".s"),assemblerValeur,StandardCharsets.UTF_8);
            List<String> donnéesSymbole = new ArrayList<>(), donnéesSource = new ArrayList<>();
            for (RéférenceMéthode référence : convertirValeur.listeMéthodes.keySet()) donnéesSymbole.add(chaîneDonnées(symbole("method",référence.parties())) + ":" + chaîneDonnées(référence.valeurPropriétaire + "." + référence.nom + référence.valeurDescription));
            for (Path valeurEntrée : listeEntrée) {
                byte[] fichierHachage = MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(valeurEntrée)); StringBuilder texte = new StringBuilder(); for (byte valeur : fichierHachage) texte.append(String.format(Locale.ROOT,"%02x",valeur & 255));
                donnéesSource.add(chaîneDonnées(valeurEntrée.toAbsolutePath().toString()) + ":" + chaîneDonnées(texte.toString()));
            }
            Files.writeString(Paths.get(Sortie + ".json"),"{\"target\":" + chaîneDonnées(valeurCible) + ",\"entry\":" + chaîneDonnées(pointEntréeÉlément) + ",\"format\":\"ELF32 i386\",\"runtime_jvm\":false,\"symbols\":{" + String.join(",",donnéesSymbole) + "},\"sources\":{" + String.join(",",donnéesSource) + "}}\n",StandardCharsets.UTF_8);
        } finally {
            try (java.util.stream.Stream<Path> listeChemin = Files.walk(valeurTemporaire)) { for (Path chemin : (Iterable<Path>)listeChemin.sorted(Comparator.reverseOrder())::iterator) Files.deleteIfExists(chemin); }
        }
    }
    public static void main(String[] arguments) {
        try {
            String pointEntréeÉlément = null, valeurCible = "kernel", cibleX86 = null; Path cheminSortie = null; int nombreÉlémentsMotLexical = 262144; boolean notationUniversel = false;
            List<String> valeurExporté = new ArrayList<>(); List<Path> listeChemin = new ArrayList<>();
            for (int indiceOrdinal = 0; indiceOrdinal < arguments.length; indiceOrdinal++) {
                String valeur = arguments[indiceOrdinal];
                switch (valeur) {
                    case "--target": cibleX86 = arguments[++indiceOrdinal]; break;
                    case "--help": case "-h": System.out.println("사용법: --entry valeurClasse.Fonction -o Sortie [--target linux|kernel|user] [--profile kernel|user] [--export symbole=valeurClasse.Fonction] 클래스파일 또는 Java원문"); return;
                    case "--entry": pointEntréeÉlément = arguments[++indiceOrdinal]; break;
                    case "--profile": valeurCible = arguments[++indiceOrdinal]; break;
                    case "--heap-words": nombreÉlémentsMotLexical = Integer.parseInt(arguments[++indiceOrdinal]); break;
                    case "--export": valeurExporté.add(arguments[++indiceOrdinal]); break;
                    case "-o": cheminSortie = Paths.get(arguments[++indiceOrdinal]); break;
                    case "--ucn": notationUniversel = true; break;
                    default: if (valeur.startsWith("-")) throw new ErreurTraduction("알 nombre 없는 옵션: " + valeur); listeChemin.add(Paths.get(valeur));
                }
            }
            if (pointEntréeÉlément == null || cheminSortie == null || listeChemin.isEmpty()) throw new ErreurTraduction("--entry, -o, valeurClasse 파일이 필요합니다");
            Path valeurRessource = Paths.get(System.getProperty("jkoros.compiler.resources"));
            if (cibleX86 != null) {
                if (!Arrays.asList("linux","kernel","user").contains(cibleX86)) throw new ErreurTraduction("알 nombre 없는 exécuterCommande valeurCible");
                traductionX86(listeChemin,cibleX86,pointEntréeÉlément,valeurExporté,cheminSortie,valeurRessource); return;
            }
            String source = new CompilationAnticipée(listeChemin, valeurCible, nombreÉlémentsMotLexical, valeurRessource).générer(pointEntréeÉlément, valeurExporté, notationUniversel);
            cheminSortie = cheminSortie.toAbsolutePath(); Files.createDirectories(cheminSortie.getParent());
            Path valeurTemporaire = Files.createTempFile(cheminSortie.getParent(), ".aot-", ".tmp");
            try { Files.writeString(valeurTemporaire, source, StandardCharsets.UTF_8); Files.move(valeurTemporaire, cheminSortie, StandardCopyOption.REPLACE_EXISTING); }
            finally { Files.deleteIfExists(valeurTemporaire); }
        } catch (Exception erreur) { System.err.println("compilerSource erreur: " + erreur.getMessage()); System.exit(1); }
    }
}
