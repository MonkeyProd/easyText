find frontend \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i 's/localhost:8080/easy-text.ru\/api/g'
