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

## Wurf3D

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
## On git now


function [ dat1,dat2 ] = Wurf3D(vars)
## Variablen und Konstanten bestimmten
    %vars(1),vars(2),vars(3),vars(4),vars(5),vars(6),vars(7),vars(8),vars(9),vars(10),vars(11),vars(12),vars(13).
    %rhop   ,dp     ,V      ,elev   ,azim   ,steps  ,durat  ,windx  ,windy  ,windz   ,rhog    ,eta     ,grav
	rhop=2900;																%Dichte des Partikels in kg/qm
    rhop=vars(1);
	rhog=1.205;																%Dichte des Fluides in kg/qm
	rhog=vars(11);
	steps=1000;																%Auflösung der Teilschritte
    steps=vars(6);
	dp=2E-04;																%Partikeldurchmesser in m
    dp=vars(2);
	dp=dp.*1E-6;
    dprint=dp.*1E06;														%Umrechnung von dp in Mikrometer
	eta=1.81E-05; 															%Dyn. Viskosität des Fluides
	eta=vars(12);
	grav=9.81;																%Gravitation Erde
	grav=vars(13);
	nsc=1;																	%NullStellenCounter - Hilfvariable
	V=3;																	%Abschussgeschwindigkeit
    V=vars(3);
	anglealpha=35;                                                          %Elevation         
    anglealpha=vars(4);
    anglebeta=35;                                                           %Azimuth
    anglebeta=vars(5);
	windx=(0);																%Windgeschwindigkeit gegen Bewegungsrichtung X-Achse
    windx=vars(8);
	windy=(0);																%Windgeschwindigkeit gegen Bewegungsrichtung Y-Achse
    windy=vars(9);
    windz=(0);
    windz=vars(10);
	alpha=anglealpha.*(pi()./180);											%Umrechnung Winkel in Bogenmaß
    beta=anglebeta.*(pi()./180);                                            %Umrechnung in Bogenmaß
	Vx=V.*cos(alpha).*cos(beta);											%Berechnung X-Anteil der Abschussgeschwindigkeit
	Vy=V.*cos(alpha).*sin(beta);											%Berechnung Y-Anteil der Abschussgeschwindigkeit
    Vz=V.*sin(alpha);
	x_0=0;																	%Bereits zurückgelegter Anfangsweg X-Achse
	y_0=0;																	%Bereits zurückgelegter Anfangsweg Y-Achse
    z_0=0;
	Vx																		%Ausgabe Vx (Kontrolle)
	Vy																		%Ausgabe Vy (Kontrolle)
    Vz
	V_0=[Vx,Vy,Vz,x_0,y_0,z_0];												%Anfangsvektors für gekoppelte DGL

## Rechnungen	


## Relaxationszeit abschätzen und Variablen anpassen
    trelax=rhop.*dp.^2./18./eta;
    if (vars(7) == 0)
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
        duration = vars(7);
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
    [ngt,r]=ode45(@Vts3D,[tspan],V_0,odeopt,rhop,rhog,grav,eta,dp,windx,windy,windz);		%Lösen der Gekoppelten DGL
    %    Vx   ;Vy   ;Vz   ;X    ;Y    ;Z
    printf("Gekoppelte DGL fertig \n");
    ngxs=r(:,1);
    ngys=r(:,3);
    ngzs=r(:,2);
    ngxp=r(:,4);
    ngyp=r(:,5);
    ngzp=r(:,6);
    [nusvt,nusvi]=ode45(@Vtsv,[0,duration],[1E-08,0],odeopt2,rhop,rhog,grav,eta,dp);
    nusv=nusvi(end,1);
    
    dat1=[ngt,ngxs,ngys,ngzs,ngxp,ngyp,ngzp];
    dat2=[duration,trelax,VTSN,VTSS,nusv];
    
   % h=figure();															%Ein neues Zeichenfenster wird geöffnet
   % plot3 (ngxp,ngyp,ngzp);
   % axis([0 20 0 20 0 20]);
endfunction

##
## Differentialgleichungen
##		
		## Vertikale Bewegung mit Gravitation, für positive Geschwindigkeiten
		## Ausgabe: Geschwindigkeit dy(1) und Weg dy(2)
		function 	dy= Vtsv(x,y,rhop,rhog,grav,eta,dp)								%Bew.gl. für positive Geschwindigkeiten, löst Geschwindigkeit und Weg auf
			k=(pi()./8).*rhog.*dp.^2;											%Konstanten berechnen
			c=rhog.*dp./eta;													%Konstanter Teil der Reynoldszahl berechnen
			m=pi()./6.*rhop.*dp.^3;												%Masse des Partikels berechnen
			dy(1) = -sign(y(1)).*((24./(c.*abs(y(1))))+(2.6.*(c.*abs(y(1))./5))./(1+(c.*abs(y(1))./5).^1.52)+(0.411.*(c.*abs(y(1))./263000).^-7.94)./(1+(c.*abs(y(1))./263000).^-8)+((c.*abs(y(1))).^0.8./461000)).*k.*abs(y(1)).^2./m - grav + (rhog./rhop.*grav);
			%dy(1)=-(24./(c.*y(1))).*(1+0.15.*(c.*y(1)).^0.687).*k.*y(1).^2 ./m - grav ; %alternative Formel nach Schiller und Naumann
			dy(2) = y(1);
			dy=[dy(1);dy(2)];
		endfunction
		
	## Gekoppelte DGLs
		
		## 
        function 	dy= Vts3D(x,y,rhop,rhog,grav,eta,dp,windx,windy,windz)
			k=(pi()./8).*rhog.*dp.^2;											%Konstanten berechnen
			c=rhog.*dp./eta;													%Konstanter Teil der Reynoldszahl berechnen
			m=pi()./6.*rhop.*dp.^3;												%Masse des Partikels berechnen
			## Morrison Variante
			dy(1) = -sign((y(1)+windx)).*((24./(c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2))))+(2.6.*((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./5))./(1+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./5).^1.52)+(0.411.*((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./263000).^-7.94)./(1+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./263000).^-8)+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2))).^0.8./461000)).*k.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)).*abs(y(1)+windx)./m;
			dy(2) = -sign((y(2)+windy)).*((24./(c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2))))+(2.6.*((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./5))./(1+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./5).^1.52)+(0.411.*((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./263000).^-7.94)./(1+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./263000).^-8)+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2))).^0.8./461000)).*k.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)).*abs(y(2)+windy)./m;
            dy(3) = -sign((y(3)+windz)).*((24./(c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2))))+(2.6.*((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./5))./(1+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./5).^1.52)+(0.411.*((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./263000).^-7.94)./(1+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)))./263000).^-8)+((c.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2))).^0.8./461000)).*k.*sqrt(((y(1)+windx).^2)+((y(2)+windy).^2)+((y(3)+windz).^2)).*abs(y(3)+windz)./m -grav + (rhog./rhop.*grav);
			dy(4) = y(1);
			dy(5) = y(2);
            dy(6) = y(3);
			dy= [dy(1);dy(2);dy(3);dy(4);dy(5);dy(6)];
            %    Vx   ;Vy   ;Vz   ;X    ;Y    ;Z
		endfunction	
		