/* -*- Mode:Prolog; coding:iso-8859-1; indent-tabs-mode:nil; prolog-indent-width:8; prolog-paren-indent:4; tab-width:8; -*- 
Logic Assignment

Author: Tony Lindgren
Student: Godwin Mba
*/



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Part 1: Usage of Knowledgbase
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

belongs_to(harry_potter, gryffindor).
belongs_to(hermione_granger, gryffindor).
belongs_to(cedric_diggory, hufflepuff).
belongs_to(draco_malfoy, slytherin).
wand(harry_potter, '11"_holly_phoenix').
wand(harry_potter, '11"_vine_dragon').
wand(harry_potter, '10"_blackthorn_unknown').
wand(harry_potter, '10"_hawthorn_unicorn').
wand(harry_potter, '15"_elder_thestral_hair').
wand(hermione_granger, '11"_vine_dragon_heartstring').
wand(hermione_granger, '13"_walnut_dragon_heartstring').
wand(cedric_diggory, '12"_ash_unicorn_hair').
wand(draco_malfoy, '10"_hawthorn_unicorn_hair').
wand(draco_malfoy, '15"_elder_thestral_hair').
patronus(harry_potter, stag).
patronus(hermione_granger, otter).
boggart(harry_potter,dementor).
boggart(hermione_granger,failure).
boggart(draco_malfoy,lord_voldemort).
loyalty(harry_potter, gryffindor).
loyalty(harry_potter, hermione_granger).
loyalty(hermione_granger, gryffindor).
loyalty(hermione_granger, harry_potter).
loyalty(cedric_diggory, hufflepuff).
loyalty(cedric_diggory, harry_potter).
influence(harry_potter, hermione_granger).
influence(hermione_granger, harry_potter).
influence(cedric_diggory, hermione_granger).
influence(cedric_diggory, harry_potter).
influence(draco_malfoy, hogwarts).
influence(hogwarts, gryffindor).
influence(hogwarts, slytherin).
influence(hogwarts, hufflepuff).
influence(hogwarts, harry_potter).
influence(hogwarts, hermione_granger).
influence(hogwarts, cedric_diggory).
influence(hogwarts, draco_malfoy).
trans_influence(X,Y):-
        influence(X,Z),
        influence(Z,Y),
        influence(X,Y).


% Does it exist a wand that has had two different owners?

exists(X,Y) :-
       setof(X, wand(X,Y), L).



%Who influences hermoine granger?
influences(X, Y) :-
        influence(X,Y).

% Find out if there exist some, who has influence over something, that it also belongs to.
influence_belong(X,Y):-
        influence(X,Y),
        belongs_to(X,Y).




%  Find out if there exist any entity that has (transitional) influence over themself
trans_influence_over_themself(X):-
        influence(X,Y),
        influence(Y,X),
        X =:= X.
% Does it exist anything that has (transitional) influence over anything else and the latter is
% not loyal to the former (and they cannot be the same object). 
trans_infl_and_not_loyal(X, Y):-
        trans_influence(X,Y),
        \+ loyalty(Y, X),
        X \== Y.

% Does it exist anything that has (transitional) influence over anything else and the latter is
%loyal to the former (and they cannot be the same object).
trans_infl_and_loyal(X, Y):-
        trans_influence(X,Y),
        loyalty(Y, X),
        X \== Y.





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Part 2: Define set and handle terms
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% to_set(+List, -Set) Transforms a list of atoms into a set




to_set([], []).

to_set([H|T], X):- member(H, T), !, to_set(T, X).

to_set([H|T], [H|X]):- to_set(T, X).



                                                             
%union(+L1, +L2, -S3) S3 is the union of L1 and L2
union([], U, U).                                      
union([H|T], SET2, RESULT) :-
   member(H,SET2), !, 
   union(T,SET2,RESULT).    
union([H|T], SET2, [H|RESULT]) :- 
   
   union(T,SET2,RESULT).


%intersection(+L1, +L2, -S3) S3 is the intersection of L1 and L2 
intersection([], _, []).

intersection([H1|T1], L2, [H1|Res]) :-
    member(H1, L2),
    intersection(T1, L2, Res).

intersection([_|T1], L2, Res) :-
    intersection(T1, L2, Res).



%diff(+L1, +L2, -S3) S3 is the difference of L1 - L2 
diff([],_,[]):- !.
diff([H|T],B,[H|T1]):-
    \+member(H,B), !,
    diff(T,B,T1).
diff([H|T],B,[H1|T1]):-
    member(H,B), !,
    diff(T,B,[H1|T1]).

test:-
    LA = [a,b,b,a],
    LB = [c,b,b,c,e,f],
    diff(LA,LB,LO1),    
    writeln(LO1).

%subset(+L1, +L2) True if L1 is a subset of L2 
sublist( [], _ ).
sublist( [X|XS], [X|XSS] ) :- sublist( XS, XSS ).
sublist( [X|XS], [_|XSS] ) :- sublist( [X|XS], XSS ).




% Define predicates to handle sets  
% p(s(X),a,Z,Z) = p(Y,X,r(Y),r(s(a))). 

% assuming a universe with function symbols g/2, p/2, q/2

% identical terms unify (delete rule)
unify(X, Y) :-
    X == Y,
    !.

% a variable unifies with anything (eliminate rule)
unify(X, Y) :-
    var(X),
    !,
    X = Y.

% an equation Term = Variable can be solved as Variable = Term (swap rule)
unify(X, Y) :-
    var(Y),
    !,
    unify(Y, X).

% given equal function symbols, unify the arguments (decompose rule)
unify(g(A, B), g(X, Y)) :-
    unify(A, X),
    unify(B, Y).
unify(p(A, B), p(X, Y)) :-
    unify(A, X),
    unify(B, Y).
unify(q(A, B), q(X, Y)) :-
    unify(A, X),
    unify(B, Y).

unify(T, R) :-
  T =.. [F,X,Y,Z],
  ( R =.. [F,X,X,Z] ; R =.. [F,X,Y,Z] ; R =.. [F,X,Y,Y] ).




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Part 3: Monkey and banana
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This predicate initialises the search for a solution to the problem. 
% The 1st argument of solve/4 is the initial state, 
% the 2nd the goal statepaint,
% the 3rd is a temporary list of actions creating the plan, initially empty 
% the 4th the plan that will be produced.

start(Plan):-   
    solve([on(monkey,floor),on(box,floor),at(monkey,a),at(box,b),
           at(bananas,c),at(stick,d),status(bananas,hanging)],
           [status(bananas,grabbed)], [], Plan).

% This predicate produces the plan. Once the Goal list is a subset 
% of the current State the plan is complete and it is written to 
% the screen using write_sol/1.
solve(State, Goal, Plan, Plan):-
        sublist(Goal, State).

solve(State, Goal, Sofar, Plan):-
        op(Op, Preconditions, Delete, Add),

        % TODO 1:
        % Check if an operator can be utilized or not
        % predicate_name(Preconditions, State)
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Define a predicate that becomes true if:  
        %       all members of Preconditions are part of current State (State) 
        % and return false otherwise
        sublist(Preconditions, State),
        
        
        % TODO 2:
        % Test to avoid using the operator multiple times 
        % (To avoid infinite loops, in more comlex problems this is often implemented via states)
        % predicate_name(Op, Sofar)
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Define a predicate that checks if Op has been done before
        % if so the predicate should fail otherwise be true 
        \+ sublist(Op, Sofar),
           
           
        % TODO 3: 
        % First half of applying an operator  
        % predicate_name(State, Delete, Remainder),
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Define a predicate that removes all members of the Delete list 
        % from the state and the results are returned in the Reminder 
        diff(State, Delete, Remainder),
        
        
        append(Add, Remainder, NewState),
        % Useful for debugging (de-comment to see output) 
        format('Operator:~w ~N', [Op]),    
        format('NewState:~w ~N', [NewState]),
        solve(NewState, Goal, [Op|Sofar], Plan).

solve(State, Goal, Plan, RPlan):-
        % TODO 4:
        % add a check if State is a subset of Goal here 
        sublist(Goal, State),
        reverse(Plan,RPlan).

% TODO 5: 
% reverse(Plan,RPlan) - define this predicate which returns a reversed list
reverse(Plan,RPlan):-
        reverse_helper(Plan,RPlan,[]).

reverse_helper([],Ys,Ys).
reverse_helper([X|Xs], Ys, Zs) :-
        reverse_helper(Xs, Ys, [X|Zs]).
        
% The operators take 4 arguments
% 1st arg = name
% 2nd arg = preconditions
% 3rd arg = delete list
% 4th arg = add list.

op(swing(stick),
    [on(monkey,box), at(monkey,X), at(box,X), holding(monkey,stick), at(bananas,X), status(bananas,hanging)],
    [status(B,hanging)],
    [status(B,grabbed)]).

op(grab(stick),
        [at(monkey,X), at(stick, X), on(monkey,floor)],
        [at(stick, X)],
        [holding(monkey,stick)]).

% TODO 6: 
% op(climbon(box) - define this operator
op(climbon(box),
   [on(box,floor), at(monkey,X), at(box,X), on(monkey,floor)],
   [on(monkey,floor)],
   [on(monkey,box)]).        



% TODO 7:
% op(push(box,X,Y) - define this operator
op(push(box,X,Y),
        [at(monkey,X), on(monkey,floor),at(box,X),on(box,floor)],
        [at(box,X),at(monkey,X)],
        [at(monkey,Y), at(box,Y)]):- 
        X \== Y.       


op(go(X,Y),
        [at(monkey,X), on(monkey,floor)],
        [at(monkey,X)],
        [at(monkey,Y)]):- 
        X \== Y.