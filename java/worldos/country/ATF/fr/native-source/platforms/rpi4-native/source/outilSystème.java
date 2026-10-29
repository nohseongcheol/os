// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Commandes de gestion IPv4, ICMP, tâches, mémoire et stockage en RAM lisant l’état réel du noyau. */
public final class outilSystème {
    static int valeurAdresse;
    static boolean texteÉgal(int numéro, String texteMot) { return InterpréteurCommandes.texteÉgal(numéro, texteMot); }
    static int nombreÉlémentsÉlémentListe() { return InterpréteurCommandes.nombreÉlémentsJeton; }
    static void valeurÉchec(String Guide) { InterpréteurCommandes.résultat=2; EntréeSortieTerminal.écrire(Guide); EntréeSortieTerminal.Caractères(10); }
    static void erreur(int valeur) { InterpréteurCommandes.erreur(valeur); }
    static void entréeÉlémentNuméro(String nom, int valeur) { EntréeSortieTerminal.écrire(nom); EntréeSortieTerminal.nombre(valeur); EntréeSortieTerminal.Caractères(10); }
    static int valeurChiffre(int numéro, int limiteCapacité) {
        if (numéro>=nombreÉlémentsÉlémentListe() || InterpréteurCommandes.longueur[numéro]==0) return -1;
        int valeur=0;
        for (int indiceOrdinal=0; indiceOrdinal<InterpréteurCommandes.longueur[numéro]; indiceOrdinal++) {
            int valeurCaractère=InterpréteurCommandes.valeurJeton[InterpréteurCommandes.pointInitial[numéro]+indiceOrdinal]-'0';
            if (valeurCaractère<0 || valeurCaractère>9 || valeur>(limiteCapacité-valeurCaractère)/10) return -1;
            valeur=valeur*10+valeurCaractère;
        }
        return valeur<=limiteCapacité?valeur:-1;
    }
    static boolean lireAdresse(int numéro) {
        if (numéro>=nombreÉlémentsÉlémentListe()) return false;
        int valeur=0, valeurFragmentBloc=0, nombreÉlémentsChiffre=0, nombreÉlémentsPoint=0;
        for (int indiceOrdinal=0; indiceOrdinal<InterpréteurCommandes.longueur[numéro]; indiceOrdinal++) {
            int valeurCaractère=InterpréteurCommandes.valeurJeton[InterpréteurCommandes.pointInitial[numéro]+indiceOrdinal];
            if (valeurCaractère=='.') { if (nombreÉlémentsChiffre==0 || ++nombreÉlémentsPoint>3) return false; valeur=(valeur<<8)|valeurFragmentBloc; valeurFragmentBloc=nombreÉlémentsChiffre=0; }
            else { if (valeurCaractère<'0' || valeurCaractère>'9' || ++nombreÉlémentsChiffre>3) return false; valeurFragmentBloc=valeurFragmentBloc*10+valeurCaractère-'0'; if(valeurFragmentBloc>255)return false; }
        }
        if (nombreÉlémentsPoint!=3 || nombreÉlémentsChiffre==0) return false;
        valeurAdresse=(valeur<<8)|valeurFragmentBloc; return true;
    }
    static void écrireAdresse(int valeur) {
        EntréeSortieTerminal.nombre((valeur>>>24)&255); EntréeSortieTerminal.Caractères('.'); EntréeSortieTerminal.nombre((valeur>>>16)&255); EntréeSortieTerminal.Caractères('.');
        EntréeSortieTerminal.nombre((valeur>>>8)&255); EntréeSortieTerminal.Caractères('.'); EntréeSortieTerminal.nombre(valeur&255);
    }
    static void afficherÉtatRéseau() {
        EntréeSortieTerminal.écrire(CarteMatérielle.étatRéseau(20,0)!=0?"en0: ":"sl0: "); EntréeSortieTerminal.écrire(CarteMatérielle.étatRéseau(3,0)!=0?"UP":"DOWN");
        EntréeSortieTerminal.écrire(CarteMatérielle.étatRéseau(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        EntréeSortieTerminal.écrire(CarteMatérielle.étatRéseau(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); écrireAdresse(CarteMatérielle.étatRéseau(0,0));
        EntréeSortieTerminal.écrire(" netmask "); écrireAdresse(CarteMatérielle.étatRéseau(1,0)); EntréeSortieTerminal.écrire(" gateway "); écrireAdresse(CarteMatérielle.étatRéseau(2,0)); EntréeSortieTerminal.Caractères(10);
        EntréeSortieTerminal.écrire("  RX packets "); EntréeSortieTerminal.nombre(CarteMatérielle.étatRéseau(4,0)); EntréeSortieTerminal.écrire(" bytes "); EntréeSortieTerminal.nombre(CarteMatérielle.étatRéseau(6,0));
        EntréeSortieTerminal.écrire(" TX packets "); EntréeSortieTerminal.nombre(CarteMatérielle.étatRéseau(5,0)); EntréeSortieTerminal.écrire(" bytes "); EntréeSortieTerminal.nombre(CarteMatérielle.étatRéseau(7,0)); EntréeSortieTerminal.Caractères(10);
        entréeÉlémentNuméro("  dropped ",CarteMatérielle.étatRéseau(8,0));
    }
    static void définirAdresse(int lancer) {
        if (nombreÉlémentsÉlémentListe()!=lancer+3 || !lireAdresse(lancer)) { valeurÉchec("사용법: ipconfig set adresse 주소가림 valeurPasserelle"); return; }
        int adresse=valeurAdresse;
        if(!lireAdresse(lancer+1)){valeurÉchec("Invalid IPv4 netmask");return;} int valeurMasque=valeurAdresse;
        if(!lireAdresse(lancer+2)){valeurÉchec("Invalid IPv4 gateway");return;}
        int résultat=CarteMatérielle.réglagesRéseau(0,adresse,valeurMasque,valeurAdresse);
        if(résultat<0) { erreur(résultat); if(résultat==-16)EntréeSortieTerminal.écrire("Close sockets and stop ftpd before changing address.\n"); }
        else { EntréeSortieTerminal.écrire("IPv4 configuration applied (until reboot)\n"); afficherÉtatRéseau(); }
    }
    static void commandeRéseau(boolean adresseIP) {
        if (nombreÉlémentsÉlémentListe()==1 || nombreÉlémentsÉlémentListe()==2 && (texteÉgal(1,"show") || texteÉgal(1,"addr") || texteÉgal(1,"address") || texteÉgal(1,"sl0") || texteÉgal(1,"en0")) || nombreÉlémentsÉlémentListe()==3 && (texteÉgal(1,"addr") || texteÉgal(1,"address")) && texteÉgal(2,"show")) { afficherÉtatRéseau();return; }
        if (adresseIP && texteÉgal(1,"route") && (nombreÉlémentsÉlémentListe()==2 || nombreÉlémentsÉlémentListe()==3&&texteÉgal(2,"show"))) { afficherChemin();return; }
        if (texteÉgal(1,"set")) { définirAdresse(2);return; }
        if (nombreÉlémentsÉlémentListe()==2 && (texteÉgal(1,"up") || texteÉgal(1,"down"))) { CarteMatérielle.réglagesRéseau(texteÉgal(1,"up")?1:2,0,0,0);afficherÉtatRéseau();return; }
        if (adresseIP && nombreÉlémentsÉlémentListe()==6 && texteÉgal(1,"link") && texteÉgal(2,"set") && texteÉgal(3,"dev") && (texteÉgal(4,"sl0")||texteÉgal(4,"en0")) && (texteÉgal(5,"up") || texteÉgal(5,"down"))) { CarteMatérielle.réglagesRéseau(texteÉgal(5,"up")?1:2,0,0,0);afficherÉtatRéseau();return; }
        valeurÉchec("사용법: ip [addr show|route show|set adresse 주소가림 valeurPasserelle|link set dev sl0 up|down]");
    }
    static void afficherChemin() {
        EntréeSortieTerminal.écrire("Destination Netmask Gateway Interface\n");
        écrireAdresse(CarteMatérielle.étatRéseau(0,0)&CarteMatérielle.étatRéseau(1,0));EntréeSortieTerminal.Caractères(' ');écrireAdresse(CarteMatérielle.étatRéseau(1,0));EntréeSortieTerminal.écrire(CarteMatérielle.étatRéseau(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (CarteMatérielle.étatRéseau(2,0)!=0) {EntréeSortieTerminal.écrire("0.0.0.0 0.0.0.0 ");écrireAdresse(CarteMatérielle.étatRéseau(2,0));EntréeSortieTerminal.écrire(CarteMatérielle.étatRéseau(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void afficherRéseau() {
        EntréeSortieTerminal.écrire("Proto Local Remote State Queued\n");
        for(int numéro=0;numéro<32;numéro++) {
            int catégorieType=CarteMatérielle.étatRéseau(10,numéro);if(catégorieType==0)continue;
            EntréeSortieTerminal.écrire(catégorieType==1?"TCP ":"UDP ");écrireAdresse(CarteMatérielle.étatRéseau(16,numéro));EntréeSortieTerminal.Caractères(':');EntréeSortieTerminal.nombre(CarteMatérielle.étatRéseau(11,numéro));EntréeSortieTerminal.Caractères(' ');
            écrireAdresse(CarteMatérielle.étatRéseau(12,numéro));EntréeSortieTerminal.Caractères(':');EntréeSortieTerminal.nombre(CarteMatérielle.étatRéseau(13,numéro));EntréeSortieTerminal.Caractères(' ');
            int valeurÉtatValeur=CarteMatérielle.étatRéseau(14,numéro);EntréeSortieTerminal.écrire(catégorieType==2?"DATAGRAM":valeurÉtatValeur==1?"LISTEN":valeurÉtatValeur==2?"ESTABLISHED":valeurÉtatValeur==3?"CLOSE_WAIT":valeurÉtatValeur==4?"ERROR":"UNCONNECTED");
            EntréeSortieTerminal.Caractères(' ');EntréeSortieTerminal.nombre(CarteMatérielle.étatRéseau(15,numéro));EntréeSortieTerminal.Caractères(10);
        }
        EntréeSortieTerminal.écrire("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean attendreÉtatValeur(int millisecondes) {
        int lancer=CarteMatérielle.millisecondes();
        while(CarteMatérielle.millisecondes()-lancer<millisecondes) {
            if(EntréeSortieInterpréteurCommandes.estInteractif()!=0){int valeurCaractère=CarteMatérielle.lireSériel();if(valeurCaractère==3 || valeurCaractère=='q' || valeurCaractère=='Q' || valeurCaractère==27 || valeurCaractère==-4096)return false;}
            CarteMatérielle.céderProcesseur();
        }
        return true;
    }
    static void testRéponseRetour() {
        int nombreÉlémentsRépétition=4, valeurLimite=1000, valeurCible=-1;
        for(int indicePosition=1;indicePosition<nombreÉlémentsÉlémentListe();indicePosition++) {
            if(texteÉgal(indicePosition,"-c")){nombreÉlémentsRépétition=valeurChiffre(++indicePosition,100);if(nombreÉlémentsRépétition<1){valeurÉchec("ping: -c 1..100");return;}}
            else if(texteÉgal(indicePosition,"-W")){valeurLimite=valeurChiffre(++indicePosition,10);if(valeurLimite<1){valeurÉchec("ping: -W 1..10 seconds");return;}valeurLimite*=1000;}
            else if(valeurCible<0)valeurCible=indicePosition;else{valeurÉchec("사용법: ping [-c nombreÉlémentsRépétition] [-W valeurSecondes] IPv4");return;}
        }
        if(valeurCible<0 || !lireAdresse(valeurCible)){valeurÉchec("ping: an IPv4 address is required (DNS is not configured)");return;}
        int adresse=valeurAdresse, nombreÉlémentsEnvoyé=0, nombreÉlémentsReçu=0, valeurAccumulé=0, limiteMinimal=100000, limiteMaximal=0;
        EntréeSortieTerminal.écrire("PING ");écrireAdresse(adresse);EntréeSortieTerminal.écrire(" 32 ICMP bytes\n");
        boolean traitementContinuer=true;
        for(int valeurOrdre=1;valeurOrdre<=nombreÉlémentsRépétition && traitementContinuer;valeurOrdre++) {
            int valeurTraité=CarteMatérielle.envoyerRéponseRetour(adresse,valeurOrdre);
            if(valeurTraité<0){erreur(valeurTraité);break;}nombreÉlémentsEnvoyé++;
            int lancer=CarteMatérielle.millisecondes();
            while(CarteMatérielle.lireRéponseRetour(0)==-11 && CarteMatérielle.millisecondes()-lancer<valeurLimite)if(!attendreÉtatValeur(1)){traitementContinuer=false;break;}
            if(!traitementContinuer)break;
            if(CarteMatérielle.lireRéponseRetour(0)==0){
                int valeurTemps=CarteMatérielle.lireRéponseRetour(1);nombreÉlémentsReçu++;valeurAccumulé+=valeurTemps;if(valeurTemps<limiteMinimal)limiteMinimal=valeurTemps;if(valeurTemps>limiteMaximal)limiteMaximal=valeurTemps;
                EntréeSortieTerminal.écrire("32 bytes from ");écrireAdresse(adresse);EntréeSortieTerminal.écrire(" seq=");EntréeSortieTerminal.nombre(valeurOrdre);EntréeSortieTerminal.écrire(" ttl=");EntréeSortieTerminal.nombre(CarteMatérielle.lireRéponseRetour(2));EntréeSortieTerminal.écrire(" time=");EntréeSortieTerminal.nombre(valeurTemps);EntréeSortieTerminal.écrire(" ms\n");
            }else{EntréeSortieTerminal.écrire("Request timeout seq=");EntréeSortieTerminal.nombre(valeurOrdre);EntréeSortieTerminal.Caractères(10);}
            if(valeurOrdre<nombreÉlémentsRépétition)traitementContinuer=attendreÉtatValeur(200);
        }
        EntréeSortieTerminal.nombre(nombreÉlémentsEnvoyé);EntréeSortieTerminal.écrire(" transmitted, ");EntréeSortieTerminal.nombre(nombreÉlémentsReçu);EntréeSortieTerminal.écrire(" received, ");EntréeSortieTerminal.nombre(nombreÉlémentsEnvoyé==0?100:(nombreÉlémentsEnvoyé-nombreÉlémentsReçu)*100/nombreÉlémentsEnvoyé);EntréeSortieTerminal.écrire("% packet loss\n");
        if(nombreÉlémentsReçu>0){EntréeSortieTerminal.écrire("rtt min/avg/max = ");EntréeSortieTerminal.nombre(limiteMinimal);EntréeSortieTerminal.Caractères('/');EntréeSortieTerminal.nombre(valeurAccumulé/nombreÉlémentsReçu);EntréeSortieTerminal.Caractères('/');EntréeSortieTerminal.nombre(limiteMaximal);EntréeSortieTerminal.écrire(" ms\n");}
        InterpréteurCommandes.résultat=traitementContinuer?(nombreÉlémentsReçu==0?1:0):130;
    }
    static void afficherActivité() { EntréeSortieTerminal.écrire("up ");EntréeSortieTerminal.nombre(CarteMatérielle.millisecondes()/1000);EntréeSortieTerminal.écrire(" seconds\n"); }
    static void afficherMémoire() {
        entréeÉlémentNuméro("ARM RAM KiB (firmware): ",CarteMatérielle.systèmeInterroger(0,0));
        entréeÉlémentNuméro("Kernel image+BSS+stack KiB: ",CarteMatérielle.systèmeInterroger(1,0));
        int capacitéTotal=CarteMatérielle.systèmeInterroger(2,0), capacitéUtilisé=CarteMatérielle.systèmeInterroger(3,0);
        EntréeSortieTerminal.écrire("AOT heap KiB total/used/free: ");EntréeSortieTerminal.nombre(capacitéTotal);EntréeSortieTerminal.Caractères('/');EntréeSortieTerminal.nombre(capacitéUtilisé);EntréeSortieTerminal.Caractères('/');EntréeSortieTerminal.nombre(capacitéTotal-capacitéUtilisé);EntréeSortieTerminal.Caractères(10);
        entréeÉlémentNuméro("Framebuffer KiB: ",CarteMatérielle.systèmeInterroger(4,0));
        entréeÉlémentNuméro("EL0 arena+session reserve KiB: ",CarteMatérielle.systèmeInterroger(5,0));
        int valeurAssocié=0;for(int numéro=0;numéro<4;numéro++)valeurAssocié+=CarteMatérielle.systèmeInterroger(22,numéro);
        entréeÉlémentNuméro("EL0 mapped KiB: ",valeurAssocié);
        EntréeSortieTerminal.écrire("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void afficherTâches() {
        EntréeSortieTerminal.écrire("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        EntréeSortieTerminal.écrire("1 - RUN - - ");EntréeSortieTerminal.nombre(CarteMatérielle.millisecondes());EntréeSortieTerminal.écrire(" kernel/shell\n");
        for(int numéro=1;numéro<3;numéro++)if(CarteMatérielle.étatValeurTâche(numéro)>0){EntréeSortieTerminal.nombre(numéro+1);EntréeSortieTerminal.écrire(" - READY 64 - - kernel-task\n");}
        for(int numéro=0;numéro<4;numéro++){
            int valeurÉtatValeur=CarteMatérielle.systèmeInterroger(20,numéro);if(valeurÉtatValeur==0)continue;
            EntréeSortieTerminal.nombre(CarteMatérielle.systèmeInterroger(21,numéro));EntréeSortieTerminal.Caractères(' ');EntréeSortieTerminal.nombre(numéro);EntréeSortieTerminal.écrire(valeurÉtatValeur==1?" RUN ":" SUSPENDED ");
            EntréeSortieTerminal.nombre(CarteMatérielle.systèmeInterroger(22,numéro));EntréeSortieTerminal.Caractères(' ');EntréeSortieTerminal.nombre(CarteMatérielle.systèmeInterroger(24,numéro));EntréeSortieTerminal.Caractères(' ');EntréeSortieTerminal.nombre(CarteMatérielle.systèmeInterroger(23,numéro));EntréeSortieTerminal.Caractères(' ');
            for(int indicePosition=0;indicePosition<288;indicePosition++){int valeurOctet=CarteMatérielle.systèmeInterroger(25,numéro+indicePosition*4);if(valeurOctet==0)break;CarteMatérielle.écrireSériel(valeurOctet);}EntréeSortieTerminal.Caractères(10);
        }
    }
    static void afficherStockage() {
        int nombreÉlémentsEmplacement=0, nombreÉlémentsDonnées=0;
        for(int numéro=0;numéro<FichiersMémoire.nombreÉlémentsFichier;numéro++)if(FichiersMémoire.longueurNom[numéro]>0 || FichiersMémoire.nombreÉlémentsRéférence[numéro]>0){nombreÉlémentsEmplacement++;nombreÉlémentsDonnées+=FichiersMémoire.longueur[numéro];}
        EntréeSortieTerminal.écrire("Filesystem Total Reserved Available Data Files Mount\nramfs ");EntréeSortieTerminal.nombre(FichiersMémoire.nombreÉlémentsFichier*16384);EntréeSortieTerminal.Caractères(' ');EntréeSortieTerminal.nombre(nombreÉlémentsEmplacement*16384);EntréeSortieTerminal.Caractères(' ');EntréeSortieTerminal.nombre((FichiersMémoire.nombreÉlémentsFichier-nombreÉlémentsEmplacement)*16384);EntréeSortieTerminal.Caractères(' ');EntréeSortieTerminal.nombre(nombreÉlémentsDonnées);EntréeSortieTerminal.Caractères(' ');EntréeSortieTerminal.nombre(nombreÉlémentsEmplacement);EntréeSortieTerminal.Caractères('/');EntréeSortieTerminal.nombre(FichiersMémoire.nombreÉlémentsFichier);EntréeSortieTerminal.écrire(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void afficherÉtat() {
        int nombreÉlémentsRépétition=EntréeSortieInterpréteurCommandes.estInteractif()!=0?0:1;
        if(nombreÉlémentsÉlémentListe()>1){if(nombreÉlémentsÉlémentListe()!=3 || !texteÉgal(1,"-n") || (nombreÉlémentsRépétition=valeurChiffre(2,1000))<1){valeurÉchec("사용법: top [-n 1..1000]; q/Ctrl+C로 programmeTerminerSession");return;}}
        for(int valeurSéquence=0;nombreÉlémentsRépétition==0 || valeurSéquence<nombreÉlémentsRépétition;valeurSéquence++){
            if(EntréeSortieInterpréteurCommandes.estInteractif()!=0 && nombreÉlémentsRépétition==0)EntréeSortieTerminal.écrire("\u001b[2J\u001b[H");
            afficherActivité();afficherMémoire();afficherTâches();
            if(nombreÉlémentsRépétition!=0 && valeurSéquence+1>=nombreÉlémentsRépétition)break;
            if(!attendreÉtatValeur(1000))break;
        }
    }
    static String motStandard(int numéro) {
        if(numéro==0)return "ipconfig";if(numéro==1)return "ip";if(numéro==2)return "ping";if(numéro==3)return "route";if(numéro==4)return "netstat";
        if(numéro==5)return "ps";if(numéro==6)return "top";if(numéro==7)return "free";if(numéro==8)return "df";if(numéro==9)return "uptime";if(numéro==10)return "poweroff";return "help";
    }
    static void afficherAide() {
        EntréeSortieTerminal.écrire("--- Network / system commands ---\n");
        for(int numéro=0;numéro<12;numéro++){EntréeSortieTerminal.écrire(motStandard(numéro));EntréeSortieTerminal.écrire(" / ");EntréeSortieTerminal.écrire(CommandesAdministration.texteMot(numéro));EntréeSortieTerminal.écrire(" : ");EntréeSortieTerminal.écrire(CommandesAdministration.description(numéro));EntréeSortieTerminal.Caractères(10);}
        EntréeSortieTerminal.écrire("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        EntréeSortieTerminal.écrire("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        EntréeSortieTerminal.écrire("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean exécuterCommande() {
        int commande=-1;
        for(int numéro=0;numéro<12;numéro++)if(texteÉgal(0,motStandard(numéro)) || texteÉgal(0,CommandesAdministration.texteMot(numéro)))commande=numéro;
        if(texteÉgal(0,"ifconfig"))commande=0;if(texteÉgal(0,"ss"))commande=4;
        if(commande<0)return false;
        if(commande==11){if(texteÉgal(1,"net") || texteÉgal(1,"system"))afficherAide();else if(texteÉgal(1,"ko") || texteÉgal(1,"input"))InterpréteurCommandes.aideHangul();else InterpréteurCommandes.afficherAide();return true;}
        if(commande==0 || commande==1)commandeRéseau(commande==1);
        else if(commande==2)testRéponseRetour();
        else if(commande==6)afficherÉtat();
        else if(nombreÉlémentsÉlémentListe()!=1){valeurÉchec("This command takes no arguments; help system");}
        else if(commande==3)afficherChemin();else if(commande==4)afficherRéseau();else if(commande==5)afficherTâches();else if(commande==7)afficherMémoire();else if(commande==8)afficherStockage();else if(commande==9)afficherActivité();
        else if(commande==10)CarteMatérielle.désactivéAlimentation();
        return true;
    }
}
