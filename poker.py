import math

# Adding players to the table
def get_players():
    players = []
    while True:
        try:
            player_name = input("Enter player name (or 'S' to finish): ")
            if player_name.lower() == 's':
                break
            if player_name.strip():
                players.append(player_name)
        except Exception:
            print("\nAn error occurred. Please try again.")
    return players

# Starting chip limit
def get_chips():
    while True:
        try:
            n = int(input("Start chips per player: "))
            blind = int(input("Initial blind amount: "))
            if n <= 0 or blind <= 0:
                print("Please enter a positive integer.")
                continue
            return n, blind
        except ValueError:
            print("Please enter a valid integer.")

def blind_increase(blind):
    return blind + math.ceil(blind / 2)


def run_betting_phase(phase_name, active_players, player_chips, start_idx, min_bet):
    print("\n--- {} Phase ---".format(phase_name))
    phase_pot = 0
    highest_bet = min_bet
    current_bets = {p: 0 for p in active_players} 
    folded = []
    
    action_index = start_idx
    players_acted = 0
    
    while True:
        current_active = [p for p in active_players if p not in folded]
        active_count = len(current_active)
        
        # Stop if everyone else folded
        if active_count <= 1:
            break 
            
        # Check if everyone has acted AND matched the highest bet
        all_matched = True
        for p in current_active:
            if current_bets[p] < highest_bet:
                all_matched = False
                break
                
        if all_matched and players_acted >= active_count:
            break
            
        player = active_players[action_index % len(active_players)]
        
        if player not in folded:
            print("\nPot: {} | Bet to match: {}".format(phase_pot, highest_bet))
            print("{}'s turn (Wallet: {} chips)".format(player, player_chips[player]))
            to_call = highest_bet - current_bets[player]
            
            # Allow "Check" if there is no current bet to match
            if to_call == 0:
                action = input("(F)old, (C)heck, or (R)aise? ").lower()
            else:
                action = input("(F)old, (C)all {}, or (R)aise? ".format(to_call)).lower()
            
            if action == 'f':
                folded.append(player)
            elif action == 'c':
                call_amount = min(to_call, player_chips[player]) 
                current_bets[player] += call_amount
                player_chips[player] -= call_amount
                phase_pot += call_amount
            elif action == 'r':
                try:
                    raise_amt = int(input("Raise BY how much extra? "))
                    total_put_in = min(to_call + raise_amt, player_chips[player])
                    current_bets[player] += total_put_in
                    player_chips[player] -= total_put_in
                    highest_bet += raise_amt
                    phase_pot += total_put_in
                except ValueError:
                    print("Invalid amount. Treated as a fold.")
                    folded.append(player)
            else:
                print("Invalid input. Treated as a fold.")
                folded.append(player)
            
            players_acted += 1
            
        action_index += 1
        
    remaining_players = [p for p in active_players if p not in folded]
    return phase_pot, remaining_players

def main():
    print("Welcome to the Poker Helper!")
    players_list = get_players()
    if not players_list:
        print("No players entered. Exiting.")
        return
    
    chip_count, blind = get_chips()
    player_chips = {player: chip_count for player in players_list}
    
    round_counter = 0
    dealer_idx = 0
    
    while len(players_list) > 1:
        round_counter += 1
        print("\n" + "="*20)
        print("HAND {}".format(round_counter))
        print("Blind is: {}".format(blind))
        print("="*20)
        
        hand_pot = 0
        active_in_hand = list(players_list)
        
        # The 4 betting phases of standard community poker
        # Pre-flop requires matching the blind. The rest start at a 0 bet.
        phases = [("Pre-flop", blind), ("Flop", 0), ("Turn", 0), ("River", 0)]
        
        for phase_name, starting_bet in phases:
            if len(active_in_hand) > 1:
                phase_pot, active_in_hand = run_betting_phase(
                    phase_name, active_in_hand, player_chips, dealer_idx, starting_bet
                )
                hand_pot += phase_pot
            else:
                # Everyone else folded, skip remaining phases
                break 
        
        # Determine winners
        print("\nHand over! Total Pot size: {}".format(hand_pot))
        if len(active_in_hand) == 1:
            winner = active_in_hand[0]
            print("{} wins {} chips by default!".format(winner, hand_pot))
            player_chips[winner] += hand_pot
        else:
            print("Active players at showdown: {}".format(", ".join(active_in_hand)))
            winner_input = input("Who won? (For ties, separate names with commas): ")
            
            winners = [w.strip() for w in winner_input.split(',')]
            valid_winners = [w for w in winners if w in player_chips]
            
            if not valid_winners:
                print("No valid names entered. Pot is lost.")
            else:
                split_amount = hand_pot // len(valid_winners)
                remainder = hand_pot % len(valid_winners)
                
                for index, w in enumerate(valid_winners):
                    payout = split_amount
                    if index == 0: 
                        payout += remainder
                    player_chips[w] += payout
                    print("{} wins {} chips!".format(w, payout))
                
        # Status update & elimination
        print("\n--- Current Chip Counts ---")
        for p in list(players_list):
            print("{}: {} chips".format(p, player_chips[p]))
            if player_chips[p] <= 0:
                print(">> {} has been eliminated!".format(p))
                players_list.remove(p)
                
        dealer_idx = (dealer_idx + 1) % len(players_list)
        
        if round_counter % len(players_list) == 0:
            blind = blind_increase(blind)
            print("\n*** Blind increased to: {} ***".format(blind))
            
        cont = input("\nPlay next hand? (Y/N): ").lower()
        if cont == 'n':
            break

    print("\nGame Over! Final Standings:")
    for p, c in player_chips.items():
        if c > 0:
            print("{}: {} chips".format(p, c))



if __name__ == "__main__":
    main()
