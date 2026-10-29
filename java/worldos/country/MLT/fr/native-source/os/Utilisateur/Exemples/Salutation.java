// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class Salutation {
    public static int lancer() {
        Utilisateur.écrire("Hello from a separate Java ELF!\n");
        Utilisateur.écrire(Utilisateur.permissionExécution() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int numéro = 0; numéro < Utilisateur.nombreÉlémentsArguments(); numéro++) {
            Utilisateur.écrire("arg: "); Utilisateur.écrire(Utilisateur.arguments(numéro)); Utilisateur.écrire("\n");
        }
        return Utilisateur.permissionExécution() == 3 ? 0 : 1;
    }
}
