import os
import sys
import time
import random
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style, Back

# Fix for Windows console encoding issues
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

init(autoreset=True)

# Beautiful ASCII Logo
logo = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
{Fore.CYAN}║{Fore.RED}__________             __  .__                                {Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}\\____    /____   _____/  |_|__|______  ____   ____            {Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}  /     // __ \\ /    \\   __\\  \\_  __ \\/  _ \\ / ___\\           {Fore.CYAN}║
{Fore.CYAN}║{Fore.RED} /     /\\  ___/|   |  \\  | |  ||  | \\(  <_> ) /_/  >          {Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}/_______ \\___  >___|  /__| |__||__|   \\____/\\___  /           {Fore.CYAN}║
{Fore.CYAN}║{Fore.RED}        \\/   \\/     \\/                     /_____/            {Fore.CYAN}║
{Fore.CYAN}║{Fore.YELLOW}                  HypeSquad Badge Changer                     {Fore.CYAN}║
{Fore.CYAN}║{Fore.MAGENTA}                     discord.gg/zentirog                      {Fore.CYAN}║
{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# Badge mapping
BADGES = {
    '1': {'id': '1', 'name': 'Bravery', 'emoji': '🦁', 'color': Fore.RED},
    '2': {'id': '2', 'name': 'Brilliance', 'emoji': '💡', 'color': Fore.GREEN},
    '3': {'id': '3', 'name': 'Balance', 'emoji': '⚖️', 'color': Fore.BLUE},
    '4': {'id': None, 'name': 'Leave HypeSquad', 'emoji': '🚪', 'color': Fore.YELLOW}
}

class RateLimiter:
    def __init__(self):
        self.lock = threading.Lock()
        self.rate_limited_tokens = {}
    
    def is_rate_limited(self, token):
        with self.lock:
            if token in self.rate_limited_tokens:
                wait_until = self.rate_limited_tokens[token]
                if time.time() < wait_until:
                    return wait_until - time.time()
                else:
                    del self.rate_limited_tokens[token]
            return False
    
    def set_rate_limit(self, token, retry_after):
        with self.lock:
            self.rate_limited_tokens[token] = time.time() + retry_after

rate_limiter = RateLimiter()

def load_tokens():
    """Load tokens from tokens.txt file"""
    if not os.path.exists("tokens.txt"):
        print(f"{Fore.RED}[!] tokens.txt file not found!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Creating tokens.txt... Please add your tokens{Style.RESET_ALL}")
        with open("tokens.txt", "w", encoding='utf-8') as f:
            f.write("# Add your tokens here (one per line)\n")
            f.write("your_token_here\n")
        return []
    
    with open("tokens.txt", "r", encoding='utf-8') as f:
        tokens = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not tokens:
        print(f"{Fore.RED}[!] No tokens found in tokens.txt!{Style.RESET_ALL}")
        return []
    
    return tokens

def get_headers(token):
    """Get headers for a token"""
    return {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9127 Chrome/127.0.6533.99 Electron/32.0.1 Safari/537.36',
        'X-Debug-Options': 'bugReporterEnabled',
        'X-Discord-Locale': 'en-US',
        'X-Discord-Timezone': 'America/New_York',
    }

def change_hypesquad(token, house_id, badge_name, badge_color):
    """Change HypeSquad badge for a single token - no session overhead"""
    
    # Check if token is rate limited
    wait_time = rate_limiter.is_rate_limited(token)
    if wait_time:
        token_display = f"...{token[-10:]}" if len(token) > 10 else token[:10]
        print(f"{Fore.YELLOW}[⏳] {token_display} | Rate limited, waiting {wait_time:.1f}s{Style.RESET_ALL}")
        time.sleep(wait_time)
    
    try:
        headers = get_headers(token)
        
        if house_id:  # Join a house
            url = "https://discord.com/api/v9/hypesquad/online"
            payload = {'house_id': house_id}
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 204:
                return True, f"{badge_color}{badge_name}{Style.RESET_ALL}"
            elif response.status_code == 429:  # Rate limit
                retry_data = response.json()
                retry_after = retry_data.get('retry_after', 5)
                rate_limiter.set_rate_limit(token, retry_after)
                return False, f"Rate limited ({retry_after}s)"
            else:
                return False, f"HTTP {response.status_code}"
        
        else:  # Leave HypeSquad
            url = "https://discord.com/api/v9/hypesquad/online"
            response = requests.delete(url, headers=headers, timeout=15)
            
            if response.status_code == 204:
                return True, f"{Fore.YELLOW}Left HypeSquad{Style.RESET_ALL}"
            elif response.status_code == 429:
                retry_data = response.json()
                retry_after = retry_data.get('retry_after', 5)
                rate_limiter.set_rate_limit(token, retry_after)
                return False, f"Rate limited ({retry_after}s)"
            else:
                return False, f"HTTP {response.status_code}"
                
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, f"Error: {str(e)[:30]}"

def process_tokens(tokens, random_mode=False, specific_house=None, specific_name=None, specific_color=None):
    """Process all tokens with threading"""
    
    successful = 0
    failed = 0
    rate_limited = 0
    
    # Determine number of workers (optimized)
    max_workers = min(len(tokens), 30)  # 30 threads max for optimal performance
    
    print(f"\n{Fore.CYAN}[*] Starting with {max_workers} threads...{Style.RESET_ALL}")
    if random_mode:
        print(f"{Fore.YELLOW}[*] Mode: Random - Each token gets random badge{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}[*] Mode: Specific - {specific_color}{specific_name}{Style.RESET_ALL}\n")
    
    # Progress tracking
    completed = 0
    lock = threading.Lock()
    
    def process_single_token(token):
        nonlocal successful, failed, rate_limited, completed
        
        if random_mode:
            # Pick random badge for each token (excluding leave option)
            random_choice = random.choice(['1', '2', '3'])
            random_badge = BADGES[random_choice]
            success, message = change_hypesquad(token, random_badge['id'], random_badge['name'], random_badge['color'])
            badge_display = f"{random_badge['emoji']} {message}"
        else:
            success, message = change_hypesquad(token, specific_house, specific_name, specific_color)
            badge_display = f"{BADGES[str(specific_house)]['emoji'] if specific_house else '🚪'} {message}"
        
        token_display = f"...{token[-12:]}" if len(token) > 12 else token
        
        with lock:
            completed += 1
            if success:
                successful += 1
                print(f"{Fore.GREEN}[{completed:2d}/{len(tokens)}] ✓ {token_display} | {badge_display}{Style.RESET_ALL}")
            else:
                if "Rate limited" in message:
                    rate_limited += 1
                    failed += 1
                    print(f"{Fore.YELLOW}[{completed:2d}/{len(tokens)}] ⏰ {token_display} | {message}{Style.RESET_ALL}")
                else:
                    failed += 1
                    print(f"{Fore.RED}[{completed:2d}/{len(tokens)}] ✗ {token_display} | {message}{Style.RESET_ALL}")
        
        return success
    
    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_single_token, token): token for token in tokens}
        
        for future in as_completed(futures):
            try:
                future.result(timeout=30)
            except Exception as e:
                token = futures[future]
                token_display = f"...{token[-12:]}"
                with lock:
                    completed += 1
                    failed += 1
                    print(f"{Fore.RED}[{completed:2d}/{len(tokens)}] ✗ {token_display} | Exception: {str(e)[:30]}{Style.RESET_ALL}")
    
    return successful, failed, rate_limited

def main():
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print logo
    print(logo)
    
    # Load tokens
    print(f"{Fore.CYAN}[*] Loading tokens...{Style.RESET_ALL}")
    tokens = load_tokens()
    if not tokens:
        input(f"\n{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}[✓] Loaded {len(tokens)} tokens{Style.RESET_ALL}")
    
    # Ask for mode
    print(f"\n{Fore.CYAN}╔════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Fore.WHITE}         SELECT BADGE MODE              {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}1.{Style.RESET_ALL} Specific Badge (Same for all tokens)")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Random Badge (Random for each token)")
    
    mode_choice = input(f"\n{Fore.GREEN}[?] Choose mode (1-2): {Style.RESET_ALL}").strip()
    
    random_mode = False
    specific_house = None
    specific_name = None
    specific_color = None
    
    if mode_choice == '2':
        random_mode = True
        print(f"\n{Fore.GREEN}[✓] Random mode enabled! Each token will get a random HypeSquad badge{Style.RESET_ALL}")
    elif mode_choice == '1':
        # Show badge options
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Fore.WHITE}         SELECT HYPESQUAD BADGE         {Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚════════════════════════════════════════╝{Style.RESET_ALL}")
        
        for key, badge in BADGES.items():
            print(f"\n{Fore.YELLOW}{key}.{Style.RESET_ALL} {badge['emoji']} {badge['color']}{badge['name']}{Style.RESET_ALL}")
        
        badge_choice = input(f"\n{Fore.GREEN}[?] Choose badge (1-4): {Style.RESET_ALL}").strip()
        
        if badge_choice not in BADGES:
            print(f"{Fore.RED}[!] Invalid choice!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")
            return
        
        specific_house = BADGES[badge_choice]['id']
        specific_name = BADGES[badge_choice]['name']
        specific_color = BADGES[badge_choice]['color']
    else:
        print(f"{Fore.RED}[!] Invalid choice!{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")
        return
    
    # Confirmation
    print(f"\n{Fore.RED}{Back.YELLOW}[!] WARNING: This will change HypeSquad badges for {len(tokens)} tokens{Style.RESET_ALL}")
    if not random_mode:
        print(f"{Fore.YELLOW}[!] Badge: {specific_color}{specific_name}{Style.RESET_ALL}")
    
    confirm = input(f"\n{Fore.RED}[?] Type 'yes' to confirm: {Style.RESET_ALL}").strip().lower()
    
    if confirm != 'yes':
        print(f"{Fore.RED}[!] Cancelled.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")
        return
    
    # Start processing
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    start_time = time.time()
    successful, failed, rate_limited = process_tokens(tokens, random_mode, specific_house, specific_name, specific_color)
    elapsed_time = time.time() - start_time
    
    # Print summary
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╔════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Fore.WHITE}              RESULTS SUMMARY            {Fore.CYAN}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}✅ Successful: {successful}{Style.RESET_ALL}")
    print(f"{Fore.RED}❌ Failed: {failed}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⏰ Rate Limited: {rate_limited}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 Total Tokens: {len(tokens)}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}⚡ Speed: {len(tokens)/elapsed_time:.2f} tokens/second{Style.RESET_ALL}")
    print(f"{Fore.CYAN}⏱️  Time Elapsed: {elapsed_time:.2f} seconds{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    input(f"\n{Fore.GREEN}Press Enter to exit...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Interrupted by user{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Fatal Error: {e}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")
