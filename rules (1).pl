:- use_module(library(clpfd)).

% Kardelen Erdal 2018400024
location(1, 1, 1).
direction(1, east).
bump(-11).
wumpusSmell(-11).
wumpusSight(-11).

location(Time,X,Y) :-
  PreviousTime is Time - 1,
    (((action(PreviousTime,hit);action(PreviousTime,clockWise);action(PreviousTime,counterClockWise)), location(PreviousTime,X,Y));
    ((action(PreviousTime,forward)), bump(Time), !, location(PreviousTime,X,Y));
    ((action(PreviousTime,forward)), direction(PreviousTime,south), not(bump(Time)), 
    	location(PreviousTime,XNorth,Y), !, (X #= XNorth + 1), (Y #= Y));
    ((action(PreviousTime,forward)), direction(PreviousTime,north), not(bump(Time)), 
    	location(PreviousTime,XSouth,Y), !, (X #= XSouth - 1), (Y #= Y));
    ((action(PreviousTime,forward)), direction(PreviousTime,east), not(bump(Time)), 
    	location(PreviousTime,X,YWest), !, (X #= X), (Y #= YWest + 1));
    ((action(PreviousTime,forward)), direction(PreviousTime,west), not(bump(Time)), 
    	location(PreviousTime,X,YEast), !, (X #= X), (Y #= YEast - 1))), !.
 
direction(Time,north) :-
  PreviousTime is Time - 1,
        (((action(PreviousTime,hit);action(PreviousTime,forward)),direction(PreviousTime,north));
                (action(PreviousTime,clockWise),direction(PreviousTime,west));
                (action(PreviousTime,counterClockWise),direction(PreviousTime,east))).

direction(Time,east) :-
  PreviousTime is Time - 1,
        (((action(PreviousTime,hit);action(PreviousTime,forward)), direction(PreviousTime,east));
                (action(PreviousTime,clockWise),direction(PreviousTime,north));
                (action(PreviousTime,counterClockWise),direction(PreviousTime,south))).

direction(Time,south) :-
  PreviousTime is Time - 1,
        (((action(PreviousTime,hit);action(PreviousTime,forward)), direction(PreviousTime,south));
                (action(PreviousTime,clockWise),direction(PreviousTime,east));
                (action(PreviousTime,counterClockWise),direction(PreviousTime,west))).

direction(Time,west) :-
  PreviousTime is Time - 1,
        (((action(PreviousTime,hit);action(PreviousTime,forward)), direction(PreviousTime,west));
                (action(PreviousTime,clockWise),direction(PreviousTime,south));
                (action(PreviousTime,counterClockWise),direction(PreviousTime,north))).

is_empty(List):- not(member(_,List)). 

isWall(X,Y) :-
  bump(Time),
  PreviousTime is Time - 1,
  (((action(PreviousTime,hit);action(PreviousTime,forward)),
    ((direction(PreviousTime,south), location(PreviousTime,XNorth,Y), (X #= XNorth + 1), (Y #= Y));
    (direction(PreviousTime,east),location(PreviousTime,X,YWest), (X #= X), (Y #= YWest + 1));
    (direction(PreviousTime,north),location(PreviousTime,XSouth,Y), (X #= XSouth - 1), (Y #= Y));
    (direction(PreviousTime,west),location(PreviousTime,X,YEast), (X #= X), (Y #= YEast - 1))))).

wallInFront(Time) :- location(Time, X, Y), !,(XM is X-1), (XP is X+1), (YM is Y-1), (YP is Y+1), 
	((direction(Time,north),isWall(XM, Y));
	(direction(Time,south),isWall(XP, Y));
	(direction(Time,west),isWall(X, YM));
	(direction(Time,east),isWall(X, YP))).

isWinner(Time) :- 
	location(Time, X, Y), !, (XM is X-1), (XP is X+1), (YM is Y-1), (YP is Y+1), 
	action(Time, hit), wumpusSmell(Time),
	
	((direction(Time,north), (YM < 1; smellableButNotSmelled(Time,X,YM); visibleButNotSeen(Time,X,YM)), 
						     (smellableButNotSmelled(Time,XP,Y); visibleButNotSeen(Time,XP,Y)), 
						     (smellableButNotSmelled(Time,X,YP); visibleButNotSeen(Time,X,YP)),
						     (XM > 0, not(visibleButNotSeen(Time,XM,Y))));
	
	(direction(Time,south),  (YM < 1; smellableButNotSmelled(Time,X,YM); visibleButNotSeen(Time,X,YM)), 
						     (XM < 1; smellableButNotSmelled(Time,XM,Y); visibleButNotSeen(Time,XM,Y)), 
						     (smellableButNotSmelled(Time,X,YP); visibleButNotSeen(Time,X,YP)),
						     (not(visibleButNotSeen(Time,XP,Y))));
	
	(direction(Time,west),   (smellableButNotSmelled(Time,X,YP); visibleButNotSeen(Time,X,YP)), 
						     (smellableButNotSmelled(Time,XP,Y); visibleButNotSeen(Time,XP,Y)), 
						     (XM < 1; smellableButNotSmelled(Time,XM,Y); visibleButNotSeen(Time,XM,Y)),
						     (YM > 0, not(visibleButNotSeen(Time,X,YM))));
	
	(direction(Time,east),   (YM < 1; smellableButNotSmelled(Time,X,YM); visibleButNotSeen(Time,X,YM)), 
						     (smellableButNotSmelled(Time,XP,Y); visibleButNotSeen(Time,XP,Y)), 
						     (XM < 1; smellableButNotSmelled(Time,XM,Y); visibleButNotSeen(Time,XM,Y)),
						     (not(visibleButNotSeen(Time,X,YP))))).

smellableButNotSmelled(Time, X, Y) :- findTime(Times), 
findall(T, (member(T,Times), T=<Time, location(T,Row,Column), canBeSmelledFrom(Row,Column,X,Y), not(wumpusSmell(T))), Smellable),
not(is_empty(Smellable)).

visibleButNotSeen(Time,WumpusX,WumpusY) :- findTime(Times), 
findall(T, (member(T,Times), T=<Time, location(T,X,Y), direction(T,Dir), canBeSeenFrom(X,Y,WumpusX,WumpusY,Dir), (wumpusSight(T))), Visible),
(is_empty(Visible)).

canBeSmelledFrom(X,Y,WumpusX,WumpusY) :- (X=WumpusX, Y#=WumpusY+1);(X=WumpusX, Y#=WumpusY-1);
										 (X#=WumpusX+1, Y=WumpusY);(X#=WumpusX-1, Y=WumpusY).

canBeSeenFrom(X,Y,WumpusX,WumpusY,Dir) :- 	
	(((Dir = east), X=WumpusX, WumpusY < Y + 5, WumpusY > Y);
	 ((Dir = west), X=WumpusX, WumpusY < Y, WumpusY > Y - 5);
	 ((Dir = north), Y=WumpusY, WumpusX < X, WumpusX > X - 5);
	 ((Dir = south), Y=WumpusY, WumpusX < X + 5, WumpusX > X)).	

findTime(ActionTimes):- findall(T, action(T,_), ActionTimes).
