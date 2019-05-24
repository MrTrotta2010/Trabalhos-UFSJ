entradas=("compilador.log" "matriz.log" "compressor.log" "simulador.log")
algoritmos=("lru" "nru" "segunda_chance")
pagina=(2 4 8 16 32 64)
memoria=(4 8 16 32 64 128 256 512)

for e in "${entradas[@]}"
do
	for a in "${algoritmos[@]}"
	do
		for p in "${pagina[@]}"
		do
			./tp2virtual $a Entradas/$e $p 512 > Testes/"pg"$p"_"$a"_"$e
			echo "pg"$p"_"$a"_"$e
		done

		for m in "${memoria[@]}"
		do
			./tp2virtual $a Entradas/$e 4 $m > Testes/"mem"$m"_"$a"_"$e
			echo "mem"$m"_"$a"_"$e
		done
	done 
done