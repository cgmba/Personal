/* -*- Mode:Prolog; coding:iso-8859-1; indent-tabs-mode:nil; prolog-indent-width:8; prolog-paren-indent:4; tab-width:8; -*- 
Constraint store

Author: Tony Lindgren
Student: Mba Godwin
*/
:- use_module([library(clpfd)]).

zebra:-
        % Define variabels and their domain      
                House_colors = [Red, Green, White, Yellow, Blue],
		Nation =	[Norwegian,Dane,English,German,Swede], 
		Pet    = 	[Cats,Horse,Birds,Zebra,Dog],
		Smoke  =     	[Dunhill,Blend,Pallmall,Prince,BlueMaster],
		Drink  = 	[Tea,Coffee,Milk,Beer,Water],
		
		
        domain(House_colors, 1, 5),
		domain(Nation, 1,5),
		domain(Pet, 1,5),
		domain(Smoke, 1,5),
		domain(Drink, 1,5),
		
		
		
	
	
		%TODO - add more varaibels and their domains	
        % Define constraints and relations
        all_different(House_colors), 
		all_different(Nation),		
		all_different(Pet),
		all_different(Smoke),
		all_different(Drink),
		
                Red 		#= English, 
		Swede	  	#= Dog,
		Dane	  	#= Tea,
		Green         #= Coffee,    
		Green         #= White + 1,
		Pallmall      #= Birds,
		Yellow        #= Dunhill,
		Milk          #= 3,
		Norwegian     #= 1,
		(Blend        #= Cats   - 1 #\/ Blend #= Cats   + 1),
		(Dunhill      #= Horse - 1 #\/ Dunhill#= Horse + 1),
		BlueMaster    #= Beer,
		German        #= Prince,
		(Norwegian    #= Blue  - 1 #\/ Norwegian    #= Blue  + 1),
		(Water        #= Blend - 1 #\/ Water #= Blend  + 1),






		
		%TODO - add more constraints and relations	
        % append variables to one list
        append(House_colors, Nation, Temp1),
        append(Temp1, Pet, Temp2),
	append(Temp2, Smoke, Temp3),
		%TODO - append all variabels
        append(Temp3, Smoke, VariableList),
        % find solution
        labeling([], VariableList),                                           
        % connect answers with right objects
        sort([Red-red, Green-green, White-white, Yellow-yellow, Blue-blue], House_color_connection),
        sort([English-english, Swede-swede, Dane-dane, Norwegian-norwegian, German-german], Nation_connection),
	sort([Dog-dog,Birds-birds,Cats-cats,Horse-horse,Zebra-zebra], Pet_connection),
	sort([Pallmall-pallmall,Dunhill-dunhill,Blend-blend,BlueMaster-bluemaster,Prince-prince], Smoke_connection),
	sort([Tea-tea,Coffee-coffee,Milk-milk,Beer-beer, Water-water], Drink_connection),
		
		
		%TODO - add sorting of all variabels
        % print solution
        Format = '~w~15|~w~30|~w~45|~w~60|~w~n',
        format(Format, ['house 1', 'house 2', 'house 3', 'house 4', 'house 5']),
        format(Format, House_color_connection),
        format(Format, Pet_connection),
        format(Format, Smoke_connection),
        format(Format, Drink_connection),
		%TODO - print of all variabels
        format(Format, Nation_connection).                                                        

            
        