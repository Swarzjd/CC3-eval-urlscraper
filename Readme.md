# Projet CC3
- Hadrien
- CHIPPARI

## Fonctionnement du programme
Le programme fait tout d'abord appel à la classe ```ScraperUrl``` afin de traiter le fichier ```rss_list.txt``` et récupérer toutes les urls.

Une fois toutes les urls récupérées, on fait appel à la méthode ```process_url()``` qui va appeler en asynchrone toutes les apis et parser le content xml récupéré.
La méthode va chercher l'encoder du xml pour le décrypter si la méthode n'y arrive pas, elle testera en latin1 puis en utf-8.  

Après cela, on ouvre un fichier en ```"w"``` nommé ```"resultats.txt"``` pour y écrire le résultat de la recherche par mots clés.
Pour cela, nous faisons appel à la classe ````Searcher```` qui contient la méthode ```search_in_article``` qui va rechercher dans le titre et le sommaire si un des trois key word est dans l'article. 
La méthode renvoi un tuple qui contient le résultat en fonction de la méilleur recherche, si les trois mots clés matchent, seulement deux ou les trois.

Une fois toutes les infos récupérées sous forme ````title : {article['title']}, link : {article['link']}, published : {article['published']}, keyword : {keywords_matched}```` on écrit ces résultats dans l'ordre de pertinence dans le fichier résultat. 
