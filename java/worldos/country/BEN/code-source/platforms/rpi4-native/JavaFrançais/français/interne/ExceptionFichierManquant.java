// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionFichierManquant : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionFichierManquant extends ExceptionSortieEntrée {
    public ExceptionFichierManquant() { super(); }
    public ExceptionFichierManquant(String description) { super(description); }
    public String description() { return getMessage(); }
}
