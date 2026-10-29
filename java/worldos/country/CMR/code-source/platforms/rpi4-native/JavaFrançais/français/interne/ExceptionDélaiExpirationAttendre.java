// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionDélaiExpirationAttendre : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionDélaiExpirationAttendre extends ExceptionSortieEntrée {
    public ExceptionDélaiExpirationAttendre() { super(); }
    public ExceptionDélaiExpirationAttendre(String description) { super(description); }
    public String description() { return getMessage(); }
}
