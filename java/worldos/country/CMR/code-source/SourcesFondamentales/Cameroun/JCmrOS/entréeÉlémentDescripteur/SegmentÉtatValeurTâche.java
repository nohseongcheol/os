// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cameroun.JCmrOS.entréeÉlémentDescripteur;

/** Représentation gérée du TSS fournissant une pile privilégiée lors des changements de tâche x86. */
public final class SegmentÉtatValeurTâche {
    private int blocZéroPile;
    private int adresseZéroPile;
    private int positionTablePermissionEntréeSortie = 104;

    public void définirPilePrivilégié(int valeurFragment, int adresse) {
        blocZéroPile = valeurFragment;
        adresseZéroPile = adresse;
    }

    public int blocZéroPile() { return blocZéroPile; }
    public int adresseZéroPile() { return adresseZéroPile; }
    public int positionTablePermissionEntréeSortie() { return positionTablePermissionEntréeSortie; }
}

