git checkout --orphan temp_branch
git add -A
git commit -m "Projet Cryptris : Réécriture complète en Python (ESIEA)"
git branch -D main
git branch -m main
git push -f origin main
