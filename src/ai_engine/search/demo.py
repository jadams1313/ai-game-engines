"""
Animated River Crossing - Polished Edition

Beautiful terminal animation with colors and emojis (falls back to ASCII).
"""

import sys
import time

from ai_engine.search.algorithms import uniformed_search
from ai_engine.search.problems import MissionariesCannibalsProblem


# ANSI color codes
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def colored(text, color):
    """Add color to text."""
    return f"{color}{text}{Colors.END}"


def draw_river_scene(state, step_num, total_steps, action="", use_emoji=True):
    """
    Draw an ASCII art river crossing scene.
    
    Args:
        state: Current MissionariesCannibalsState
        step_num: Current step number (0-indexed)
        total_steps: Total number of steps
        action: Description of current action
        use_emoji: Whether to use emoji characters
    """
    # Character choices
    if use_emoji:
        M = "👤"  # Missionary
        C = "👹"  # Cannibal
        BOAT = "🚣"
        WAVE = "〰️"
    else:
        M = colored("M", Colors.GREEN)
        C = colored("C", Colors.RED)
        BOAT = colored("[=]", Colors.CYAN)
        WAVE = colored("~", Colors.BLUE)
    
    width = 80
    
    lines = []
    
    # Header
    lines.append(colored("=" * width, Colors.CYAN))
    title = "MISSIONARIES & CANNIBALS RIVER CROSSING"
    lines.append(colored(title.center(width), Colors.BOLD))
    lines.append(colored("=" * width, Colors.CYAN))
    lines.append("")
    
    # Step information
    if action:
        step_text = f"Step {step_num}/{total_steps}: {action}"
    else:
        step_text = f"Step {step_num}/{total_steps}"
    lines.append(colored(step_text.center(width), Colors.YELLOW))
    lines.append("")
    
    # Progress bar
    progress = int((step_num / max(total_steps, 1)) * 40)
    progress_bar = f"[{'█' * progress}{'░' * (40 - progress)}] {step_num}/{total_steps}"
    lines.append(progress_bar.center(width))
    lines.append("")
    
    # Scene layout
    bank_width = 20
    river_width = 40
    
    lines.append(colored(f"{'LEFT BANK':<{bank_width}}{'RIVER':^{river_width}}{'RIGHT BANK':>{bank_width}}", 
                        Colors.BOLD))
    lines.append("─" * width)
    
    # Build people representations
    left_people = []
    for _ in range(state.missionaries_left):
        left_people.append(M)
    for _ in range(state.cannibals_left):
        left_people.append(C)
    
    right_people = []
    for _ in range(state.missionaries_right):
        right_people.append(M)
    for _ in range(state.cannibals_right):
        right_people.append(C)
    
    # Draw the river banks
    for row in range(7):
        if row == 0 or row == 6:
            # Top and bottom borders
            left_part = "┌" + "─" * (bank_width - 2) + "┐" if row == 0 else "└" + "─" * (bank_width - 2) + "┘"
            river_part = " " * river_width
            right_part = "┌" + "─" * (bank_width - 2) + "┐" if row == 0 else "└" + "─" * (bank_width - 2) + "┘"
        elif row == 3:
            # Middle row - boat and main people display
            left_content = " ".join(left_people[:5]) if left_people else ""
            right_content = " ".join(right_people[:5]) if right_people else ""
            
            if state.boat_location == 'L':
                left_part = "│ " + f"{left_content} {BOAT}".ljust(bank_width - 4) + " │"
            else:
                left_part = "│ " + left_content.ljust(bank_width - 4) + " │"
            
            # River with waves
            river_part = (WAVE + " ") * (river_width // 4)
            river_part = river_part[:river_width]
            
            if state.boat_location == 'R':
                right_part = "│ " + f"{BOAT} {right_content}".ljust(bank_width - 4) + " │"
            else:
                right_part = "│ " + right_content.ljust(bank_width - 4) + " │"
        else:
            # Other rows
            left_content = ""
            right_content = ""
            
            if row == 2 and len(left_people) > 5:
                left_content = " ".join(left_people[5:])
            if row == 2 and len(right_people) > 5:
                right_content = " ".join(right_people[5:])
            
            left_part = "│ " + left_content.ljust(bank_width - 4) + " │"
            river_part = " " * river_width
            right_part = "│ " + right_content.ljust(bank_width - 4) + " │"
        
        lines.append(left_part + river_part + right_part)
    
    lines.append("─" * width)
    lines.append("")
    
    # Status information
    status = f"Left: {state.missionaries_left}M {state.cannibals_left}C │ "
    status += f"Boat: {colored('←', Colors.GREEN) if state.boat_location == 'L' else colored('→', Colors.GREEN)} │ "
    status += f"Right: {state.missionaries_right}M {state.cannibals_right}C │ "
    status += f"Cost: {state.cost}"
    lines.append(status.center(width + 20))  # +20 for color codes
    
    return "\n".join(lines)


def animate_solution(result, delay=1.8, use_emoji=True):
    """
    Animate the complete solution.
    
    Args:
        result: SearchResult from solving the problem
        delay: Seconds between frames
        use_emoji: Use emoji characters
    """
    if not result.success:
        print(colored("❌ No solution found!", Colors.RED))
        return
    
    total_steps = len(result.path) - 1
    
    # Action descriptions
    action_names = {
        'MM': 'Move 2 Missionaries →',
        'MC': 'Move 1 Missionary + 1 Cannibal →',
        'CC': 'Move 2 Cannibals →',
        'M': 'Move 1 Missionary →',
        'C': 'Move 1 Cannibal →'
    }
    
    for i, state in enumerate(result.path):
        # Clear screen
        print("\033[2J\033[H", end="")
        
        # Determine action description
        if i == 0:
            action = colored("INITIAL STATE - Everyone on left bank", Colors.CYAN)
        elif i == len(result.path) - 1:
            action = colored("🎉 GOAL REACHED - Everyone safely across! 🎉", Colors.GREEN)
        else:
            action_code = result.actions[i-1] if i-1 < len(result.actions) else ""
            direction = "←" if state.boat_location == 'L' else "→"
            action_text = action_names.get(action_code, action_code)
            if state.boat_location == 'L':
                # Just moved to right, so boat is coming back left
                action_text = action_text.replace("→", "←")
            action = colored(action_text, Colors.YELLOW)
        
        # Draw scene
        scene = draw_river_scene(state, i, total_steps, action, use_emoji)
        print(scene)
        
        # Add footer message
        if i == len(result.path) - 1:
            print("\n" + colored("=" * 80, Colors.GREEN))
            print(colored("✓ SUCCESS! All missionaries and cannibals crossed safely!", Colors.GREEN).center(90))
            print(colored("=" * 80, Colors.GREEN))
        
        time.sleep(delay)


def main():
    """Main function to run the animation."""
    # Title screen
    print("\n" + colored("█" * 80, Colors.CYAN))
    print(colored("█" + " " * 78 + "█", Colors.CYAN))
    print(colored("█" + "      MISSIONARIES & CANNIBALS - ANIMATED RIVER CROSSING      ".center(78) + "█", Colors.CYAN + Colors.BOLD))
    print(colored("█" + " " * 78 + "█", Colors.CYAN))
    print(colored("█" * 80, Colors.CYAN))
    print()
    
    print(colored("The Classic River Crossing Puzzle", Colors.BOLD).center(90))
    print()
    print("Problem: Transport 3 missionaries and 3 cannibals across a river.")
    print("Constraint: Missionaries must NEVER be outnumbered on either bank.")
    print("Boat capacity: Maximum 2 people per trip.")
    print()
    print(colored("=" * 80, Colors.CYAN))
    
    time.sleep(3)
    
    print(colored("\n🔍 Solving with Breadth-First Search...", Colors.YELLOW))
    problem = MissionariesCannibalsProblem(missionaries=3, cannibals=3)
    result = uniformed_search.breadth_first_search(problem)
    
    if result.success:
        print(colored(f"✓ Solution found!", Colors.GREEN))
        print(f"  • Steps: {result.solution_depth}")
        print(f"  • Cost: {result.cost}")
        print(f"  • Nodes explored: {result.nodes_expanded}")
        print(f"  • Time: {result.time_elapsed:.4f}s")
        
        print(colored("\n🎬 Starting animation in 3 seconds...", Colors.YELLOW))
        time.sleep(3)
        
        # Check if emoji support (try to detect terminal capability)
        use_emoji = True  # Default to emoji
        
        animate_solution(result, delay=1.8, use_emoji=use_emoji)
        
        # Final statistics
        print("\n" + colored("=" * 80, Colors.CYAN))
        print(colored("SOLUTION STATISTICS", Colors.BOLD).center(90))
        print(colored("=" * 80, Colors.CYAN))
        print(f"Algorithm:      {result.algorithm}")
        print(f"Solution steps: {result.solution_depth}")
        print(f"Total cost:     {result.cost}")
        print(f"Nodes expanded: {result.nodes_expanded}")
        print(f"Runtime:        {result.time_elapsed:.4f} seconds")
        print(colored("=" * 80, Colors.CYAN))
        
    else:
        print(colored("❌ No solution found!", Colors.RED))
    
    print("\n" + colored("=" * 80, Colors.CYAN))
    print(colored("🎉 Animation complete! Thanks for watching!", Colors.GREEN + Colors.BOLD).center(90))
    print(colored("=" * 80, Colors.CYAN))
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n\n⏸️  Animation stopped by user.", Colors.YELLOW))
    except Exception as e:
        print(colored(f"\n❌ Error: {e}", Colors.RED))
        import traceback
        traceback.print_exc()