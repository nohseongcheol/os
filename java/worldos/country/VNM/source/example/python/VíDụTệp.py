from tiếngViệt import ĐầuRa, ghiTệp, đọcTệp, mãHóaVănBản, giảiMãVănBản
DữLiệu = "PYTHON Tệp: Tiếng Việt 😀\n"
ghiTệp("python.txt", mãHóaVănBản(DữLiệu))
đọcGiáTrịVănBản = giảiMãVănBản(đọcTệp("python.txt"))
assert đọcGiáTrịVănBản == DữLiệu
ĐầuRa(đọcGiáTrịVănBản, phầnKết="")
