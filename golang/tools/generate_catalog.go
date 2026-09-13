package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"sort"
)

const (
	languageDatabase = "/usr/share/iso-codes/json/iso_639-3.json"
	countryDatabase  = "/usr/share/iso-codes/json/iso_3166-1.json"
)

type language struct {
	Alpha2     string `json:"alpha_2"`
	Alpha3     string `json:"alpha_3"`
	Name       string `json:"name"`
	CommonName string `json:"common_name"`
	Scope      string `json:"scope"`
	Type       string `json:"type"`
}

type languageFile struct {
	Languages []language `json:"639-3"`
}

type country struct {
	Alpha2       string `json:"alpha_2"`
	Alpha3       string `json:"alpha_3"`
	Numeric      string `json:"numeric"`
	Name         string `json:"name"`
	OfficialName string `json:"official_name"`
	CommonName   string `json:"common_name"`
}

type countryFile struct {
	Countries []country `json:"3166-1"`
}

func readJSON(path string, target interface{}) {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		fmt.Fprintf(os.Stderr, "%s: iso-codes package is required: %v\n", path, err)
		os.Exit(1)
	}
	if err := json.Unmarshal(data, target); err != nil {
		panic(err)
	}
}

func write(path, contents string) {
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		panic(err)
	}
	if err := ioutil.WriteFile(path, []byte(contents), 0644); err != nil {
		panic(err)
	}
}

func main() {
	root, err := os.Getwd()
	if err != nil {
		panic(err)
	}
	if filepath.Base(root) == "tools" {
		root = filepath.Dir(root)
	}

	var languages languageFile
	var countries countryFile
	readJSON(languageDatabase, &languages)
	readJSON(countryDatabase, &countries)
	sort.Slice(languages.Languages, func(i, j int) bool { return languages.Languages[i].Alpha3 < languages.Languages[j].Alpha3 })
	sort.Slice(countries.Countries, func(i, j int) bool { return countries.Countries[i].Alpha3 < countries.Countries[j].Alpha3 })

	languageIndex, err := os.Create(filepath.Join(root, "언어-카탈로그.tsv"))
	if err != nil {
		panic(err)
	}
	lw := bufio.NewWriter(languageIndex)
	fmt.Fprintln(lw, "alpha3\talpha2\tname\tscope\ttype")
	for _, item := range languages.Languages {
		if len(item.Alpha3) != 3 {
			continue
		}
		dir := filepath.Join(root, "언어", item.Alpha3)
		name := item.Name
		if item.CommonName != "" {
			name = item.CommonName
		}
		conf := fmt.Sprintf("LANGUAGE_CODE=%s\nLANGUAGE_ALPHA2=%s\nLANGUAGE_NAME=%s\nLANGUAGE_SCOPE=%s\nLANGUAGE_TYPE=%s\nTEXT_DIRECTION=auto\nFONT=auto\nTRANSLATION_STATUS=fallback\n", item.Alpha3, item.Alpha2, name, item.Scope, item.Type)
		mk := fmt.Sprintf("LANGUAGE_CODE := %s\nLANGUAGE_SCOPE := %s\nLANGUAGE_TYPE := %s\ninclude ../../공통/언어판.mk\n", item.Alpha3, item.Scope, item.Type)
		write(filepath.Join(dir, "locale.conf"), conf)
		write(filepath.Join(dir, "Makefile"), mk)
		fmt.Fprintf(lw, "%s\t%s\t%s\t%s\t%s\n", item.Alpha3, item.Alpha2, name, item.Scope, item.Type)
	}
	lw.Flush()
	languageIndex.Close()

	countryIndex, err := os.Create(filepath.Join(root, "나라-카탈로그.tsv"))
	if err != nil {
		panic(err)
	}
	cw := bufio.NewWriter(countryIndex)
	fmt.Fprintln(cw, "alpha3\talpha2\tnumeric\tname\tofficial_name")
	for _, item := range countries.Countries {
		if len(item.Alpha3) != 3 {
			continue
		}
		dir := filepath.Join(root, "나라", item.Alpha3)
		name := item.Name
		if item.CommonName != "" {
			name = item.CommonName
		}
		conf := fmt.Sprintf("COUNTRY_ALPHA3=%s\nCOUNTRY_ALPHA2=%s\nCOUNTRY_NUMERIC=%s\nCOUNTRY_NAME=%s\nCOUNTRY_OFFICIAL_NAME=%s\nDEFAULT_LANGUAGE=und\n", item.Alpha3, item.Alpha2, item.Numeric, name, item.OfficialName)
		mk := fmt.Sprintf("COUNTRY_ALPHA3 := %s\nCOUNTRY_ALPHA2 := %s\n\n.PHONY: all kernel iso clean info source source-iso\n\nall: iso\ninfo:\n\t@sed -n '1,8p' country.conf\nkernel source:\n\t$(MAKE) -C 소스 kernel\niso source-iso:\n\t$(MAKE) -C 소스 iso\nclean:\n\t$(MAKE) -C 소스 clean\n", item.Alpha3, item.Alpha2)
		write(filepath.Join(dir, "country.conf"), conf)
		// Installed launchers own their parent Makefile, including local shell
		// and POSIX targets. Catalog regeneration must not erase these entries.
		if _, err := os.Lstat(filepath.Join(dir, "vbox-entry.json")); os.IsNotExist(err) {
			write(filepath.Join(dir, "Makefile"), mk)
		} else if err != nil {
			panic(err)
		}
		fmt.Fprintf(cw, "%s\t%s\t%s\t%s\t%s\n", item.Alpha3, item.Alpha2, item.Numeric, name, item.OfficialName)
	}
	cw.Flush()
	countryIndex.Close()

	fmt.Printf("generated %d ISO 639-3 language folders and %d ISO 3166-1 country folders\n", len(languages.Languages), len(countries.Countries))
}
