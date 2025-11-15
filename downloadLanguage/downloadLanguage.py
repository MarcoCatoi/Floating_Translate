# en → pt e pt → en com Argos Translate
import argostranslate.package
import argostranslate.translate

# códigos ISO 639-1
pairs = [("en", "pt"), ("pt", "en")]

# Atualiza e lê o índice oficial (GitHub argospm-index)
argostranslate.package.update_package_index()  # lê index.json do repositório oficial [web:6]
available_packages = argostranslate.package.get_available_packages()  # retorna lista de pacotes [web:1]

# Instala os dois pares
for from_code, to_code in pairs:
    pkg = next(x for x in available_packages if x.from_code == from_code and x.to_code == to_code)  # filtra pelo par [web:1]
    download_path = pkg.download()  # baixa o .argosmodel para o disco [web:1]
    argostranslate.package.install_from_path(download_path)  # instala a partir do caminho baixado [web:1]

# Teste rápido de tradução
installed_languages = argostranslate.translate.get_installed_languages()  # lista idiomas instalados [web:1]
en = next(l for l in installed_languages if l.code == "en")  # seleciona inglês instalado [web:1]
pt = next(l for l in installed_languages if l.code == "pt")  # seleciona português instalado [web:1]

en2pt = en.get_translation(pt)  # obtém objeto de tradução en→pt [web:1]
pt2en = pt.get_translation(en)  # obtém objeto de tradução pt→en [web:1]

print(en2pt.translate("Hello world!"))     # Ex.: "Olá mundo!" [web:1]
print(pt2en.translate("Bom dia, pessoal")) # Ex.: inglês equivalente [web:1]
