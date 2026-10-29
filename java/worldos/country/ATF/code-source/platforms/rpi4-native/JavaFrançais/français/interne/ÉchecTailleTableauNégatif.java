// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ÉchecTailleTableauNégatif : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ÉchecTailleTableauNégatif extends java.lang.NegativeArraySizeException {
    public ÉchecTailleTableauNégatif() { super(); }
    public ÉchecTailleTableauNégatif(String description) { super(description); }
    public String description() { return getMessage(); }
}
