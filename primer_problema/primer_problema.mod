
// Variables

dvar boolean Y[1..20][1..20];											// Y[i][j] = 1 cuando la prenda i se lava en el lavado j


dvar int+ YL[1..20];													// YL[i]   = Tiempo del lavado i


// Tiempos de lavado de cada prenda
int tiempos[1..20] = [8, 10, 9, 7, 3, 9, 10, 2, 9, 8, 6, 9, 5, 1, 5, 9, 10, 4, 4, 5];


dvar int TTL;															// Tiempo total de lavados


//dvar boolean L[1..20];												// L[i] = 1 si se usa el lavado i



// Funcional
minimize
  	TTL;
  


// Modelo
subject to {  
  
  // Incompatibilidades entre prendas
  	// Prenda 1
	forall(lavado in 1..20) {
	  forall (otraPrenda in {2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 19}) {
	    Y[1][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
  	
  	
  	// Prenda 2
	forall(lavado in 1..20) {
	  forall (otraPrenda in {3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 20}) {
	    Y[2][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 3
	forall(lavado in 1..20) {
	  forall (otraPrenda in {4, 5, 6, 7, 8, 10, 11, 12, 17, 19}) {
	    Y[3][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 4
	forall(lavado in 1..20) {
	  forall (otraPrenda in {5, 6, 7, 8, 11, 12, 13, 18, 20}) {
	    Y[4][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 5
	forall(lavado in 1..20) {
	  forall (otraPrenda in {6, 7, 8, 12, 13, 14, 19}) {
	    Y[5][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 6
	forall(lavado in 1..20) {
	  forall (otraPrenda in {7, 8, 13, 14, 15, 20}) {
	    Y[6][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 7
	forall(lavado in 1..20) {
	  forall (otraPrenda in {8, 14, 15, 16}) {
	    Y[7][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 8
	forall(lavado in 1..20) {
	  forall (otraPrenda in {15, 16}) {
	    Y[8][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 9
	forall(lavado in 1..20) {
	  forall (otraPrenda in {10, 11, 12, 13, 14, 15, 16, 17, 18}) {
	    Y[9][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 10
	forall(lavado in 1..20) {
	  forall (otraPrenda in {11, 12, 13, 14, 15, 16, 17, 18, 19}) {
	    Y[10][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 11
	forall(lavado in 1..20) {
	  forall (otraPrenda in {12, 13, 14, 15, 16, 18, 19, 20}) {
	    Y[11][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 12
	forall(lavado in 1..20) {
	  forall (otraPrenda in {13, 14, 15, 16, 19, 20}) {
	    Y[12][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 13
	forall(lavado in 1..20) {
	  forall (otraPrenda in {14, 15, 16, 20}) {
	    Y[13][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 14
	forall(lavado in 1..20) {
	  forall (otraPrenda in {15, 16}) {
	    Y[14][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 15
	forall(lavado in 1..20) {
	  forall (otraPrenda in {16}) {
	    Y[15][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 16 --> Restringida por los anteriores
	
	
	// Prenda 17
	forall(lavado in 1..20) {
	  forall (otraPrenda in {18, 19, 20}) {
	    Y[17][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 18
	forall(lavado in 1..20) {
	  forall (otraPrenda in {19, 20}) {
	    Y[18][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 19
	forall(lavado in 1..20) {
	  forall (otraPrenda in {20}) {
	    Y[19][lavado] + Y[otraPrenda][lavado] <= 1;						// Solo puede estar una de las dos prendas
	  }
	}
	
	
	// Prenda 20 --> Restringida por los anteriores

  
  
    // Restringir solo un lavado por prenda
	forall(prenda in 1..20) {
	    (sum(lavado in 1..20) Y[prenda][lavado]) == 1;					// Solo se puede lavar la prenda una vez
	}

	
	
    // Tiempo de cada lavado
	forall(lavado in 1..20) {
	  forall (prenda in 1..20) {										// Uso la indicadora Y_prenda_lavado que me dice si la prenda fue colocada en el lavado o no --> la multiplico por el tiempo que tarda la prenda.
	    YL[lavado] >= Y[prenda][lavado] * tiempos[prenda];				// El tiempo del lavado es el tiempo de la prenda que mas tarda --> tiempos[prenda] es una constante, no una variable --> no se rompe la linealidad. 
	  }																	// Lo hago asi para hacerlo todo en un ciclo y no tener que hacer hardcodeos.
	}
	
  
    TTL == (sum(lavado in 1..20) YL[lavado]);
	
}
