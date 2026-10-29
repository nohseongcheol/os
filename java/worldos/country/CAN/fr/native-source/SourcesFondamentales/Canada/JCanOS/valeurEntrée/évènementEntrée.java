// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.valeurEntrée;

public final class évènementEntrée {
    public enum valeurGenre {
        basDirectionTouche,
        hautDirectionTouche,
        mouvementSouris,
        enfoncéBoutonSouris,
        libéréBoutonSouris
    }

    private final valeurGenre genreÉvènement;
    private final int valeurPremier;
    private final int valeurDeuxième;

    public évènementEntrée(valeurGenre genreÉvènement, int valeurPremier, int valeurDeuxième) {
        this.genreÉvènement = genreÉvènement;
        this.valeurPremier = valeurPremier;
        this.valeurDeuxième = valeurDeuxième;
    }

    public valeurGenre genreÉvènement() {
        return genreÉvènement;
    }

    public int valeurPremier() {
        return valeurPremier;
    }

    public int valeurDeuxième() {
        return valeurDeuxième;
    }
}

