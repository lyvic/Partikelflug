## Copyright (C) 2013 Max
## 
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with Octave; see the file COPYING.  If not, see
## <http://www.gnu.org/licenses/>.

## Wurfrev2

## Author: Max <Max@MAX-LAPTOP-T60>
## Created: 2013-04-05
## Geschrieben für Octave 3.6.1_gcc4.6.2 mit mindestens ode-Packages und Gnuplot

## Das Programm errechnet Geschwindigkeits-Zeit und Weg-Zeit Entwicklungen einer abgeschossenen perfekten Kugel mit Luftreibung
## nach Stokes, Newton, numerisch und numerisch gekoppelt. Die Variablen können beliebig angepasst werden.
## Die Betrachtungsdauer wird für kleine Partikel über die Relaxationszeit abgeschätz. Bei großen Partikeln
## oder für Betrachtungsdauer über den Umkehrzeitpunkt nach Newton angepasst. 
## Eine Überlagerung mit einer Luftströmung ist bisher nur für die Gekoppelte Variante nach Morrison integriert.
## Beim Speichern als pdf kommt es zu Fehlern. Hier liegen Fehler bei Octave vor.
## Die Ergebnisse werden bisher als richtig angenommen. Oft sind unerwartete Werte das Resultat von Ungenauigkeiten oder der Effekt der
## getrennten Betrachtung einer gekoppelten Differentialgleichung.


function [ dat1,dat2 ] = Wurfp3(vars)
## %Variablen und Konstanten bestimmten
    printf("Ok, you gave me: %f , %f , %f\n%f, %f , %f, %f and %f\n",vars(1),vars(2),vars(3),vars(4),vars(5),vars(6),vars(7),vars(8));
	rhop=2900;																%Dichte des Partikels in kg/qm
    rhop=vars(1);
	%rhog=1.205;																%Dichte des Fluides in kg/qm
    rhog=1000;
	steps=1000;																%Auflösung der Teilschritte
    steps=vars(5);
	dp=2E-04;																%Partikeldurchmesser in m
    dp=vars(2);
	dp=dp.*1E-6;
    dprint=dp.*1E06;														%Umrechnung von dp in Mikrometer
	eta=1.81E-05; 															%Dyn. Viskosität Luft 20°C
	eta=1.0E-03;															%Dyn. Viskosität Wasser 20°C
	grav=9.81;																%Graviation Erde
    grav=1.622;																%Graviation Mond
	nsc=1;																	%NullStellenCounter - Hilfvariable
	V=3;																	%Abschussgeschwindigkeit
    V=vars(3);
	angle=35;
    angle=vars(4);
	windx=(0);																%Windgeschwindigkeit gegen Bewegungsrichtung X-Achse
	windx=vars(7);
	windy=(0);																%Windgeschwindigkeit gegen Bewegungsrichtung Y-Achse
	windy=vars(8);
	alpha=angle.*(pi()./180);												%Umrechnung Winkel in Bogenmaß
	Vx=V.*cos(alpha);														%Berechnung X-Anteil der Abschussgeschwindigkeit
	Vy=V.*sin(alpha);														%Berechnung Y-Anteil der Abschussgeschwindigkeit
	x_0=0;																	%Bereits zurückgelegter Anfangsweg X-Achse
	y_0=0;																	%Bereits zurückgelegter Anfangsweg Y-Achse
	Vx																		%Ausgabe Vx (Kontrolle)
	Vy																		%Ausgabe Vy (Kontrolle)
	V_0=[Vx,Vy,x_0,y_0];													%Anfangsvektors für gekoppelte DGL
	Vh=[Vx,x_0];															%Anfangsvektor für ungekoppelte DGL horizontal
	Vv=[Vy,y_0];															%Anfangsvektor für ungekoppelte DGL vertikal

## Rechnungen	


## Relaxationszeit abschätzen und Variablen anpassen
    trelax=rhop.*dp.^2./18./eta;
    if (vars(6) == 0)
        duration=15.*trelax;
        recduration=20.*trelax;
        if(duration>60)
            if(Vy>0)
                VTSN= sqrt(4.*rhop.*dp.*grav./3./0.44./rhog);							%VTS nach Newton
                tu= atan(Vy./VTSN).*VTSN./grav;										%Umkehrpunkt berechnen
                duration=tu.*10;
            else
                duration=60;
                duration=60;
                endif
        endif
    else
        duration = vars(6);
        endif
	duration
	stepset=duration./(steps-1);
	x=linspace(0,duration,steps)';
	tspan=linspace(0,duration,steps);
	VTSS=-rhop.*dp.^2.*grav./18./eta;
    VTSN=-sqrt(4.*rhop.*dp.*grav./3./0.44./rhog);
    
## Gekoppelte Bewegungsgleichung lösen	
    odeopt=odeset('MaxStep',10,'InitialStep',1E-06);						    %Konfiguration des ode45-Solvers
    odeopt2=odeset('MaxStep',10,'InitialStep',1E-06,'RelTol',1E-06,'AbsTol',1E-06);
    [ngt,r]=ode45(@Vts,[tspan],V_0,odeopt,rhop,rhog,grav,eta,dp,windx,windy);		%Lösen der Gekoppelten DGL
    printf("Gekoppelte DGL fertig \n");
    nghs=r(:,1);
    nghp=r(:,3);
    ngvs=r(:,2);
    ngvp=r(:,4);
    [nusvt,nusvi]=ode45(@Vtsv,[0,duration],[1E-08,0],odeopt2,rhop,rhog,grav,eta,dp);
    nusv=nusvi(end,1);
    [nuvt,nuvi]=ode45(@Vtsv,[tspan],Vv,odeopt,rhop,rhog,grav,eta,dp);			%Der ganze Verlauf kann mit Vtsneg gerechnet werden, da V_0 negativ ist.
    nuvs=nuvi(:,1);
    nuvp=nuvi(:,2);
    printf("Vertikal ungekoppelt fertig \n");
    [nuht,nuhi]=ode45(@Vtsh,[tspan],Vh,odeopt,rhop,rhog,eta,dp);				%Lösen der horizontalen DGL
    nuhs=nuhi(:,1);
    nuhp=nuhi(:,2);
    printf("Horizontal ungekoppelt fertig \n");
    %Berechnung der klassischen Ergebnisse
    svs=stokesvs(rhop,grav,eta,dp,Vy,x);										%Stokes Speed Vertikal berechnen
    nwvs=[];
	for i = (0:stepset:duration)										%Newton braucht eine for Schleife, da Berechnungen sonst zu Matrixmultiplikationen führen
		nwvs(end+1,1)=newtonvs(rhop,rhog,grav,eta,dp,Vy,i);							%Weg-Y-Werte nach Newton errechnen
	endfor
    svp=stokesvp(rhop,grav,eta,dp,Vy,x);
    nwvp=[];
    for i = (0:stepset:duration)
        nwvp(end+1,1)=newtonvp(rhop,rhog,grav,eta,dp,Vy,i);
    endfor
    shs=stokeshs(rhop,eta,dp,Vx,x);
    nwhs=[];
    for i = (0:stepset:duration)
        nwhs(end+1,1)=newtonhs(rhop,rhog,eta,dp,Vx,i);
    endfor
    shp=stokeshp(rhop,eta,dp,Vx,x);
    nwhp=[];
    for i =(0:stepset:duration)
        nwhp(end+1,1)=newtonhp(rhop,rhog,eta,dp,Vx,i);
    endfor
    size(nwvp)
    size(ngt)
    size(x)
    
    dat1=[x,nghs,nghp,ngvs,ngvp,nuhs,nuhp,nuvs,nuvp,shs,shp,svs,svp,nwhs,nwhp,nwvs,nwvp];
    dat2=[duration,trelax,VTSN,VTSS,nusv];
endfunction


##
##Hoizontale Funktionen
##
	# Stokes Wegfunktion horizontal
	function st = stokeshp (rhop,eta,dp,V_0,x)							
		m=pi()./6.*rhop.*dp.^3;											
		beta=3.*eta.*pi().*dp./m;
		st = (V_0./beta) - (1./beta.*e.^-(beta.*x).*V_0);				
	endfunction
	
	#Stokes Geschwindigkeitsfunktion horizontal
	function st = stokeshs (rhop,eta,dp,V_0,x)							
		beta=18.*eta./rhop./dp.^2;										
		m=pi()./6.*rhop.*dp.^3;
		st = V_0.*e.^(-3.*eta.*pi().*dp./m.*x);					
	endfunction
	
	#Newton Wegfunktion horizontal
	function nw = newtonhp (rhop,rhog,eta,dp,V_0,x)						
		k=4.*rhop.*dp./3./0.44./rhog;								
		nw =k.*log(((1./k).*V_0.*x)+1);
	endfunction
	
	#Newton Geschwindigkeitsfunktion horizontal
	function nws = newtonhs (rhop,rhog,eta,dp,V_0,x)						
		nws =V_0.*(1./((3.*0.44.*rhog.*V_0./4./dp./rhop.*x) +1));
	endfunction
	
##
##Vertikale Funktionen
##
	
	#Stokes Wegfunktion
	function st = stokesvp (rhop,grav,eta,dp,V_0,x)								
		beta=18.*eta./rhop./dp.^2;											
		VTS=rhop.*dp.^2.*grav./18./eta;										
		st = ((-V_0-VTS).*e.^(-beta.*x))./beta - VTS.*x - (-V_0-VTS)./beta;	
	endfunction
	
	#Stokes Geschwindigkeitsfunktion
	function st = stokesvs (rhop,grav,eta,dp,V_0,x)								
		beta=18.*eta./rhop./dp.^2;											
		VTS=rhop.*dp.^2.*grav./18./eta;										
		st = e.^(-beta.*x).*(V_0+VTS)-VTS;									
	endfunction
	
	#Newton Wegfunktion
	function nw=newtonvp (rhop,rhog,grav,eta,dp,V_0,x)
		VTS= sqrt(4.*rhop.*dp.*grav./3./0.44./rhog);							%VTS nach Newton
		tu= atan(V_0./VTS).*VTS./grav;										%Umkehrpunkt berechnen
		k=pi()./8.*0.44.*rhog.*dp.^2;										%Konstanten berechnen
		m=pi()./6.*rhop.*dp.^3;												%Masse berechnen
		p=2.*k./m.*(VTS);													%Konstante berechnen
		u1=(2./(-V_0./-VTS+1))-1;											%Integrationskonstante berechnen
			if (V_0>0)														%Für Positive Anfangsgeschwindigkeiten
				if (tu>=x)													%Umkehrpunkt mit Zeitpunkt überprüfen
					nw = VTS.^2./grav.*(log(cos(grav.*(tu-x)./VTS))-log(cos(grav.*tu./VTS)));
				endif
				if (x>tu)													%Umkehrzeitpunkt überschritten?
					x=x-tu;													%Umkehrzeitpunkt vom momentanen Zeitpunk abziehen
					nw0 = VTS.^2./grav.*(-log(cos(grav.*tu./VTS)));			%Bisher zurückgelegter Weg (Maximale Flughöhe), V_0 steckt in tu.
					nw = nw0-m./k.*log(cosh(sqrt(k.*grav./m).*x));			%Lösung erstellen
				endif
			endif
		if (0>=V_0)															%Für negative Anfangsgeschwindkeiten
			if (V_0>(-VTS))													%Mit VTS vergleichen, falls VTS noch nicht erreicht
				t=log((2./((V_0./-(sqrt(m.*grav./k))) +1)) -1)./(-2.*sqrt(k.*grav./m)); %Zeitpunkt errechnen, der V_0 entspricht
				nw0 = -m./k.*log(cosh(sqrt(k.*grav./m).*(t)));				%bisher zurückgelegter Weg
				nw = -m./k.*log(cosh(sqrt(k.*grav./m).*(t+x)))-nw0;			%Momentane Lösung erstellen
			else
				a=p.*x;														%Exponenten erstellen
				nw = -VTS.*x -m./k.*log(2.*u1+2.*e^-a) +m./k.*log(2.*u1+2);	%Lösung erstellen
			endif
		endif
	endfunction
	
	#Newton Geschwindigkeitsfunktion
	function nw = newtonvs(rhop,rhog,grav,eta,dp,V_0,x)								%Funktion für Lösungsvektor nach Newton
		VTS= sqrt(4.*rhop.*dp.*grav./3./0.44./rhog);							%VTS nach Newton
		tu= atan(V_0./VTS).*VTS./grav;										%Umkehrpunkt berechnen
		k=pi()./8.*0.44.*rhog.*dp.^2;										%Konstanten berechnen
		m=pi()./6.*rhop.*dp.^3;												%Masse berechnen
		p=2.*k./m.*(VTS);													%Konstante berechnen
		u1=(2./(V_0./VTS+1))-1;												%Integrationskonstante berechnen
		if (V_0>0)																%Für Positive Anfangsgeschwindigkeiten
			if (tu>=x)															%Umkehrpunkt mit Zeitpunkt überprüfen
				nw = VTS.*tan(-grav.*x./VTS + atan(V_0./VTS));					%Lösung erstellen
			endif
			if (x>tu)															%Umkehrzeitpunkt überschritten?
				x=x-tu;															%Umkehrzeitpunkt vom momentanen Zeitpunk abziehen
				nw = -sqrt(m.*grav./k).*tanh(sqrt(k.*grav./m).*x);				%Lösung erstellen
			endif
		endif
		if (0>=V_0)																%Für negative Anfangsgeschwindkeiten
			if (V_0>(-VTS))														%Mit VTS vergleichen,falls VTS noch nicht erreicht
				t=log((2./((V_0./-(sqrt(m.*grav./k))) +1)) -1)./(-2.*sqrt(k.*grav./m)); %Zeitpunkt errechnen, der der Anfangsgeschwindigkeit entspricht
				nw = -sqrt(m.*grav./k).*tanh(sqrt(k.*grav./m).*(t+x));			%Lösung erstellen
			else
				a=p.*x;															%Exponenten erstellen
				nw = -(VTS-((2.*VTS)./(u1.*(e.^a)+1)));							%Lösung erstellen
			endif
		endif
	endfunction
	
##
## Differentialgleichungen
##
	
	## Ungekoppelte DGLs
		
		## Horizontale Bewegung (ohne Gravitation), 
		## Ausgabe: Geschwindigkeit dy(1), Weg dy(2)
		
		function 	dy= Vtsh(x,y,rhop,rhog,eta,dp)						
				k=(pi()./8).*rhog.*dp.^2;										%Konstanten berechnen
				c=rhog.*dp./eta;												%Konstanter Teil der Reynoldszahl berechnen
				m=pi()./6.*rhop.*dp.^3;											%Masse des Partikels berechnen
				dy(1) = -((24./(c.*y(1)))+(2.6.*(c.*y(1)./5))./(1+(c.*y(1)./5).^1.52)+(0.411.*(c.*y(1)./263000).^-7.94)./(1+(c.*y(1)./263000).^-8)+((c.*y(1)).^0.8./461000)).*k.*y(1).^2./m;
				dy(2) = y(1);													%Geschwindigkeit nochmal integrieren ergibt den Weg
				dy=[dy(1);dy(2)];												%Lösungen in einer Matrix zurückgeben
		endfunction
		
		## Vertikale Bewegung mit Gravitation, für positive Geschwindigkeiten
		## Ausgabe: Geschwindigkeit dy(1) und Weg dy(2)
		function 	dy= Vtsv(x,y,rhop,rhog,grav,eta,dp)								%Bew.gl. für positive Geschwindigkeiten, löst Geschwindigkeit und Weg auf
			k=(pi()./8).*rhog.*dp.^2;											%Konstanten berechnen
			c=rhog.*dp./eta;													%Konstanter Teil der Reynoldszahl berechnen
			m=pi()./6.*rhop.*dp.^3;												%Masse des Partikels berechnen
			dy(1) = -sign(y(1)).*((24./(c.*abs(y(1))))+(2.6.*(c.*abs(y(1))./5))./(1+(c.*abs(y(1))./5).^1.52)+(0.411.*(c.*abs(y(1))./263000).^-7.94)./(1+(c.*abs(y(1))./263000).^-8)+((c.*abs(y(1))).^0.8./461000)).*k.*abs(y(1)).^2./m - grav;
			%dy(1)=-(24./(c.*y(1))).*(1+0.15.*(c.*y(1)).^0.687).*k.*y(1).^2 ./m - 9.81 ; %alternative Formel nach Schiller und Naumann
			dy(2) = y(1);
			dy=[dy(1);dy(2)];
		endfunction
		
	## Gekoppelte DGLs
		
		## 
		function 	dy= Vts(x,y,rhop,rhog,grav,eta,dp,windx,windy)
			k=(pi()./8).*rhog.*dp.^2;											%Konstanten berechnen
			c=rhog.*dp./eta;													%Konstanter Teil der Reynoldszahl berechnen
			m=pi()./6.*rhop.*dp.^3;												%Masse des Partikels berechnen
			m2=pi()./6.*rhog.*dp.^3;                                            %Anteil der Auftriebsmasse
			## Schiller und Naumann Variante (keine Signum Funktion integriert), bitte Anpassen vor Verwendung.
			%dy(1) = -((24./(c.*sqrt((y(1).^2)+(y(2).^2)))).*(1+0.15.*(c.*sqrt((y(1).^2)+(y(2).^2))).^0.687)).*k./m.*(sqrt((y(1).^2)+(y(2).^2)).*y(1));
			%dy(2) = -((24./(c.*sqrt((y(1).^2)+(y(2).^2)))).*(1+0.15.*(c.*sqrt((y(1).^2)+(y(2).^2))).^0.687)).*k./m.*(sqrt((y(1).^2)+(y(2).^2)).*y(2)) -grav +(rhog./rhop.*grav) ;		
			## Morrison Variante
			dy(1) = -sign((y(1)+windx)).*((24./(c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2))))+(2.6.*((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)))./5))./(1+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)))./5).^1.52)+(0.411.*((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)))./263000).^-7.94)./(1+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)))./263000).^-8)+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2))).^0.8./461000)).*k.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)).*abs(y(1)+windx)./m;
			dy(2) = -sign((y(2)+windy)).*((24./(c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2))))+(2.6.*((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)))./5))./(1+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)))./5).^1.52)+(0.411.*((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)))./263000).^-7.94)./(1+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)))./263000).^-8)+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2))).^0.8./461000)).*k.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)).*abs(y(2)+windy)./m -grav +(rhog./rhop.*grav);
			dy(3) = y(1);
			dy(4) = y(2);
			dy= [dy(1);dy(2);dy(3);dy(4)];
		endfunction		
		