// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class EntréeÉlémentOutil {
    public static int lancer() {
        return Utilisateur.numéroOutil() == 0 ? CompilateurJava.lancer() : MachineVirtuelleJava.lancer();
    }
}
