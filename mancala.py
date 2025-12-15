import copy
import math
import time
from typing import List, Tuple, Optional





#TODO: class MancalaBoard

class MancalaBoard:
    def __init__(self, seeds_per_pit: int = 4):
        pits = list("ABCDEF") + list("GHIJKL")
        self.board = {}
        for p in pits:
            self.board[p] = seeds_per_pit
        self.board['S1'] = 0
        self.board['S2'] = 0

        self.player1_pits = tuple("ABCDEF")
        self.player2_pits = tuple("GHIJKL")

        self.opposite = {
            'A':'L','B':'K','C':'J','D':'I','E':'H','F':'G',
            'G':'F','H':'E','I':'D','J':'C','K':'B','L':'A'
        }

        self.next_pit = {
            'A':'B','B':'C','C':'D','D':'E','E':'F','F':'S1',
            'S1':'G',
            'G':'H','H':'I','I':'J','J':'K','K':'L','L':'S2',
            'S2':'A'
        }

    def copy(self):
        new = MancalaBoard(0)
        new.board = self.board.copy()
        new.player1_pits = self.player1_pits
        new.player2_pits = self.player2_pits
        new.opposite = self.opposite.copy()
        new.next_pit = self.next_pit.copy()
        return new

    def possibleMoves(self, player_side: int) -> List[str]:
        if player_side == 1:
            pits = self.player1_pits
        else:
            pits = self.player2_pits
        return [p for p in pits if self.board[p] > 0]

    def is_player_pit(self, player_side: int, pit: str) -> bool:
        if player_side == 1:
            return pit in self.player1_pits
        else:
            return pit in self.player2_pits

    def doMove(self, player_side: int, pit: str):
        seeds = self.board[pit]
        if seeds == 0:
            raise ValueError(f"Cannot play empty pit {pit}.")
        self.board[pit] = 0
        current = pit

        while seeds > 0:
            current = self.next_pit[current]
            # skip opponent's store
            if player_side == 1 and current == 'S2':
                continue
            if player_side == 2 and current == 'S1':
                continue
            self.board[current] += 1
            seeds -= 1

        # Capture rule: if last seed landed in an empty pit on player's side
        if current in self.opposite:
            if self.board[current] == 1 and self.is_player_pit(player_side, current):
                opposite_pit = self.opposite[current]
                captured = self.board[opposite_pit] + self.board[current]
                self.board[opposite_pit] = 0
                self.board[current] = 0
                if player_side == 1:
                    self.board['S1'] += captured
                else:
                    self.board['S2'] += captured

    def side_pits_empty(self, player_side: int) -> bool:
        if player_side == 1:
            return all(self.board[p] == 0 for p in self.player1_pits)
        else:
            return all(self.board[p] == 0 for p in self.player2_pits)

    def collect_remaining_to_store(self):
        if self.side_pits_empty(1):
            total = 0
            for p in self.player2_pits:
                total += self.board[p]
                self.board[p] = 0
            self.board['S2'] += total
        elif self.side_pits_empty(2):
            total = 0
            for p in self.player1_pits:
                total += self.board[p]
                self.board[p] = 0
            self.board['S1'] += total

    def get_score(self, player_side: int) -> int:
        return self.board['S1'] if player_side == 1 else self.board['S2']

    def __str__(self):
        top = "  " + " ".join(self.player2_pits[::-1])
        top_vals = "  " + " ".join(str(self.board[p]).rjust(2) for p in self.player2_pits[::-1])
        bottom = "  " + " ".join(self.player1_pits)
        bottom_vals = "  " + " ".join(str(self.board[p]).rjust(2) for p in self.player1_pits)
        s = []
        s.append("      Player 2 side")
        s.append("Store S2: {}".format(str(self.board['S2'])))
        s.append(top)
        s.append(top_vals)
        s.append("")
        s.append(bottom)
        s.append(bottom_vals)
        s.append("Store S1: {}".format(str(self.board['S1'])))
        s.append("      Player 1 side")
        return "\n".join(s)










#FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:
#FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:
#FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:







#TODO: class Game

class Game:
    def __init__(self, board: Optional[MancalaBoard] = None, human_side: int = 1, heuristic: str = "H1"):
        self.state = board if board is not None else MancalaBoard()
        computer_side = 2 if human_side == 1 else 1
        # mapping: 1 -> COMPUTER (MAX), -1 -> HUMAN (MIN)
        self.playerSide = {
            1: computer_side,
            -1: human_side
        }
        # Heuristic type: "H1" (simple) or "H2" (advanced)
        self.heuristic = heuristic

    def gameOver(self) -> bool:
        if self.state.side_pits_empty(1) or self.state.side_pits_empty(2):
            self.state.collect_remaining_to_store()
            return True
        return False

    def findWinner(self, is_cvc_mode: bool = False) -> Tuple[Optional[str], int]:
        s1 = self.state.board['S1']
        s2 = self.state.board['S2']
        if s1 > s2:
            if is_cvc_mode:
                winner = "COMPUTER 1 (P1)"
            else:
                winner = "HUMAN" if self.playerSide[-1] == 1 else "COMPUTER"
            return winner, abs(s1 - s2)
        elif s2 > s1:
            if is_cvc_mode:
                winner = "COMPUTER 2 (P2)"
            else:
                winner = "HUMAN" if self.playerSide[-1] == 2 else "COMPUTER"
            return winner, abs(s2 - s1)
        else:
            return None, 0

    def evaluate_H1(self) -> float:
        """
        H1 - Heuristique simple: différence de graines dans les stores
        """
        comp_side = self.playerSide[1]
        human_side = self.playerSide[-1]
        comp_store = self.state.board['S1'] if comp_side == 1 else self.state.board['S2']
        human_store = self.state.board['S1'] if human_side == 1 else self.state.board['S2']
        return comp_store - human_store

    def evaluate_H2(self) -> float:
        """
        H2 - Heuristique avancée multi-critères:
        1. Score_Store: différence de graines dans les stores (poids: 1.0)
        2. Captures_Potentielles: opportunités de capture (poids: 0.5)
        3. Contrôle_Tempo: coups qui permettent de rejouer (poids: 0.3)
        4. Distribution: qualité de la distribution des graines (poids: 0.2)
        5. Mobilité: nombre de coups possibles (poids: 0.1)
        """
        comp_side = self.playerSide[1]
        human_side = self.playerSide[-1]
        
        # 1. Score de base (stores)
        comp_store = self.state.board['S1'] if comp_side == 1 else self.state.board['S2']
        human_store = self.state.board['S1'] if human_side == 1 else self.state.board['S2']
        score_diff = comp_store - human_store
        
        # 2. Captures potentielles
        comp_captures = self._count_potential_captures(comp_side)
        human_captures = self._count_potential_captures(human_side)
        capture_advantage = comp_captures - human_captures
        
        # 3. Contrôle du tempo (possibilité de rejouer)
        comp_tempo = self._count_tempo_moves(comp_side)
        human_tempo = self._count_tempo_moves(human_side)
        tempo_advantage = comp_tempo - human_tempo
        
        # 4. Distribution des graines
        comp_distribution = self._evaluate_distribution(comp_side)
        human_distribution = self._evaluate_distribution(human_side)
        distribution_advantage = comp_distribution - human_distribution
        
        # 5. Mobilité (nombre de coups possibles)
        comp_mobility = len(self.state.possibleMoves(comp_side))
        human_mobility = len(self.state.possibleMoves(human_side))
        mobility_advantage = comp_mobility - human_mobility
        
        # Combinaison pondérée
        total = (1.0 * score_diff + 
                 0.5 * capture_advantage + 
                 0.3 * tempo_advantage + 
                 0.2 * distribution_advantage + 
                 0.1 * mobility_advantage)
        
        return total

    def _count_potential_captures(self, player_side: int) -> int:
        """Compte les captures potentielles au prochain coup"""
        captures = 0
        pits = self.state.player1_pits if player_side == 1 else self.state.player2_pits
        
        for pit in pits:
            seeds = self.state.board[pit]
            if seeds == 0:
                continue
            
            # Simuler où la dernière graine va tomber
            current = pit
            temp_seeds = seeds
            while temp_seeds > 0:
                current = self.state.next_pit[current]
                if player_side == 1 and current == 'S2':
                    continue
                if player_side == 2 and current == 'S1':
                    continue
                temp_seeds -= 1
            
            # Vérifier si c'est une capture
            if current in self.state.opposite:
                if self.state.board[current] == 0 and self.state.is_player_pit(player_side, current):
                    opposite_pit = self.state.opposite[current]
                    if self.state.board[opposite_pit] > 0:
                        captures += self.state.board[opposite_pit] + 1
        
        return captures

    def _count_tempo_moves(self, player_side: int) -> int:
        """Compte les coups qui permettent de rejouer (finir dans son store)"""
        tempo_moves = 0
        pits = self.state.player1_pits if player_side == 1 else self.state.player2_pits
        my_store = 'S1' if player_side == 1 else 'S2'
        
        for pit in pits:
            seeds = self.state.board[pit]
            if seeds == 0:
                continue
            
            # Simuler où la dernière graine va tomber
            current = pit
            temp_seeds = seeds
            while temp_seeds > 0:
                current = self.state.next_pit[current]
                if player_side == 1 and current == 'S2':
                    continue
                if player_side == 2 and current == 'S1':
                    continue
                temp_seeds -= 1
            
            if current == my_store:
                tempo_moves += 1
        
        return tempo_moves

    def _evaluate_distribution(self, player_side: int) -> float:
        """Évalue la qualité de la distribution des graines"""
        pits = self.state.player1_pits if player_side == 1 else self.state.player2_pits
        seeds_list = [self.state.board[p] for p in pits]
        
        if sum(seeds_list) == 0:
            return 0
        
        # Pénaliser les distributions déséquilibrées
        # Une bonne distribution = graines réparties uniformément
        avg = sum(seeds_list) / len(seeds_list)
        variance = sum((s - avg) ** 2 for s in seeds_list) / len(seeds_list)
        
        # Plus la variance est faible, meilleure est la distribution
        return -variance * 0.1

    def evaluate(self) -> float:
        """
        Évalue la position selon l'heuristique choisie
        """
        if self.heuristic == "H1":
            return self.evaluate_H1()
        elif self.heuristic == "H2":
            return self.evaluate_H2()
        else:
            return self.evaluate_H1()  # fallback










#FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:
#FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:
#FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:




















#TODO: class Play




class Play:
    def __init__(self, human_side: int = 1, heuristic: str = "H1"):
        self.game = Game(MancalaBoard(), human_side=human_side, heuristic=heuristic)

    def humanTurn(self):
        gs = self.game.state
        human_side = self.game.playerSide[-1]
        moves = gs.possibleMoves(human_side)
        if not moves:
            print("You have no moves.")
            return
        print("Your possible moves:", " ".join(moves))
        while True:
            choice = input("Choose a pit to play (e.g. A): ").strip().upper()
            if choice in moves:
                try:
                    gs.doMove(human_side, choice)
                except Exception as e:
                    print("Invalid move:", e)
                break
            else:
                print("Invalid choice, try again.")

    def computerTurn(self, depth: int = 6) -> Optional[str]:
        val, pit = self.MinimaxAlphaBetaPruning(self.game, 1, depth, -math.inf, math.inf)
        comp_side = self.game.playerSide[1]
        if pit is None:
            moves = self.game.state.possibleMoves(comp_side)
            if not moves:
                return None
            pit = moves[0]
        print(f"Computer (side {comp_side}) chooses pit {pit} (value={val:.2f}, heuristic={self.game.heuristic})")
        self.game.state.doMove(comp_side, pit)
        return pit

    def MinimaxAlphaBetaPruning(self, game: Game, player: int, depth: int, alpha: float, beta: float) -> Tuple[float, Optional[str]]:
        if game.gameOver():
            bestValue = game.evaluate()
            return bestValue, None

        if depth == 1:
            bestValue = game.evaluate()
            return bestValue, None

        if player == 1:  # MAX (computer)
            bestValue = -math.inf
            bestPit = None
            comp_side = game.playerSide[1]
            moves = game.state.possibleMoves(comp_side)
            if not moves:
                return game.evaluate(), None
            for pit in moves:
                child_game = copy.deepcopy(game)
                child_game.state.doMove(comp_side, pit)
                value, _ = self.MinimaxAlphaBetaPruning(child_game, -player, depth - 1, alpha, beta)
                if value > bestValue:
                    bestValue = value
                    bestPit = pit
                if bestValue >= beta:
                    break
                if bestValue > alpha:
                    alpha = bestValue
            return bestValue, bestPit
        else:  # MIN (human)
            bestValue = math.inf
            bestPit = None
            human_side = game.playerSide[-1]
            moves = game.state.possibleMoves(human_side)
            if not moves:
                return game.evaluate(), None
            for pit in moves:
                child_game = copy.deepcopy(game)
                child_game.state.doMove(human_side, pit)
                value, _ = self.MinimaxAlphaBetaPruning(child_game, -player, depth - 1, alpha, beta)
                if value < bestValue:
                    bestValue = value
                    bestPit = pit
                if bestValue <= alpha:
                    break
                if bestValue < beta:
                    beta = bestValue
            return bestValue, bestPit

    def computerVsComputer(self, depth1: int = 6, depth2: int = 6, heuristic1: str = "H1", heuristic2: str = "H2", delay: float = 0.5):
        """
        Run AI vs AI match. 
        - Computer1 (side 1) uses heuristic1
        - Computer2 (side 2) uses heuristic2
        """
        board = self.game.state
        print(f"\nStarting Computer vs Computer match.")
        print(f"Computer 1 (side 1, A-F): depth={depth1}, heuristic={heuristic1}")
        print(f"Computer 2 (side 2, G-L): depth={depth2}, heuristic={heuristic2}")
        print("Initial board:")
        print(board)
        turn_side = 1
        
        while True:
            if self.game.gameOver():
                print("\nGame over!")
                print(board)
                winner, diff = self.game.findWinner()
                if winner is None:
                    print("It's a tie!")
                else:
                    print(f"Winner: {winner} by {diff} seeds.")
                break

            if turn_side == 1:
                depth = depth1
                side = 1
                heuristic = heuristic1
            else:
                depth = depth2
                side = 2
                heuristic = heuristic2

            other_side = 1 if side == 2 else 2
            temp_board = copy.deepcopy(board)
            temp_game = Game(temp_board, human_side=other_side, heuristic=heuristic)
            val, pit = self.MinimaxAlphaBetaPruning(temp_game, 1, depth, -math.inf, math.inf)

            moves = board.possibleMoves(side)
            if not moves:
                print(f"Side {side} has no legal moves.")
                turn_side = 1 if turn_side == 2 else 2
                continue

            if pit is None:
                pit = moves[0]

            print(f"\nComputer (side {side}) chooses pit {pit} (value={val:.2f}, depth={depth}, heuristic={heuristic})")
            board.doMove(side, pit)
            print(board)
            time.sleep(delay)

            turn_side = 1 if turn_side == 2 else 2








#FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:
#FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:
#FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:





















#ici  main 


#TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:
#TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:MAIN PartieTODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:
#TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:
#TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:










def main():
    print("Mancala (Awalé) - Menu")
    print("Rules: Capture implemented. Option 1 rules: NO extra turn when landing in store.")
    print("Menu:")
    print("1. Human vs Computer (Computer uses H1)")
    print("2. Computer vs Computer (Computer1=H1, Computer2=H2)")
    print("3. Exit")
    while True:
        choice = input("Choose mode (1/2/3): ").strip()
        if choice not in ('1','2','3'):
            print("Invalid choice.")
            continue
        if choice == '3':
            print("Goodbye.")
            return

        if choice == '1':
            hs = input("Play as Player 1 (A-F) or Player 2 (G-L)? Enter 1 or 2 [default 1]: ").strip()
            human_side = 1
            if hs == '2':
                human_side = 2
            
            # Computer uses H1 in Human vs Computer mode
            play = Play(human_side=human_side, heuristic="H1")

            while True:
                try:
                    d = input("Enter search depth for computer (3-10 recommended) [default 6]: ").strip()
                    if d == "":
                        depth = 6
                    else:
                        depth = int(d)
                        if depth < 1:
                            depth = 6
                    break
                except:
                    print("Invalid input.")
                    continue

            turn_side = 1
            print("\nInitial board:")
            print(play.game.state)
            while True:
                if play.game.gameOver():
                    print("\nGame over!")
                    print(play.game.state)
                    winner, diff = play.game.findWinner()
                    if winner is None:
                        print("It's a tie!")
                    else:
                        print(f"Winner: {winner} by {diff} seeds.")
                    break

                if turn_side == play.game.playerSide[-1]:
                    print("\nYour turn (Human). Current board:")
                    print(play.game.state)
                    play.humanTurn()
                else:
                    print("\nComputer's turn. Current board:")
                    print(play.game.state)
                    play.computerTurn(depth=depth)

                turn_side = 1 if turn_side == 2 else 2

        else:
            def read_depth(prompt, default):
                while True:
                    try:
                        d = input(prompt).strip()
                        if d == "":
                            return default
                        v = int(d)
                        if v < 1:
                            print("Enter >=1.")
                            continue
                        return v
                    except:
                        print("Invalid number.")
            
            depth1 = read_depth("Enter search depth for Computer 1 (Player 1 / A-F) [default 6]: ", 6)
            depth2 = read_depth("Enter search depth for Computer 2 (Player 2 / G-L) [default 6]: ", 6)
            
            while True:
                dt = input("Enter delay between moves in seconds (0 for no delay) [default 0.5]: ").strip()
                if dt == "":
                    delay = 0.5
                    break
                try:
                    delay = float(dt)
                    if delay < 0:
                        print("Enter non-negative.")
                        continue
                    break
                except:
                    print("Invalid number.")
            
            # Computer1 uses H1, Computer2 uses H2
            play = Play(human_side=1, heuristic="H1")
            play.computerVsComputer(depth1=depth1, depth2=depth2, heuristic1="H1", heuristic2="H2", delay=delay)


if __name__ == "__main__":
    main()