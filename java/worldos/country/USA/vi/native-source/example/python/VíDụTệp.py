from tiếngViệt import ĐầuRa, ghiTệp, đọcTệp, mãHóaVănBản, giảiMãVănBản
DữLiệu = "PYTHON Tệp: vi 😀\n"
ghiTệp("python.txt", mãHóaVănBản(DữLiệu))
đọcGiáTrịVănBản = giảiMãVănBản(đọcTệp("python.txt"))
assert đọcGiáTrịVănBản == DữLiệu
ĐầuRa(đọcGiáTrịVănBản, phầnKết="")
