import os
import re

files = [
    'spidi-costruzioni.html',
    'servizi.html',
    'residenziale.html',
    'commerciale.html',
    'gdo.html',
    'galleria.html',
    'chi-siamo.html',
    'contatti.html'
]

css_block = '''    /* Mobile Menu Overlay (Dissolvenza Incrociata) - Design Uniforme */
    .mobile-menu-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      height: 100dvh; /* Forza l'altezza dinamica dell'overlay */
      background-color: #0c121e; /* Sfondo scuro e profondo del menu */
      z-index: 9999; /* Z-index altissimo per sovrapporsi a tutto ed essere cliccabile */
      display: flex;
      flex-direction: column;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.35s cubic-bezier(0.25, 1, 0.5, 1);
      box-sizing: border-box;
    }

    .mobile-menu-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }

    .mobile-menu-nav {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center; /* Centrato verticalmente */
      gap: 32px;
    }

    .mobile-nav-link {
      color: #FFFFFF;
      text-decoration: none;
      font-family: 'Google Sans Flex', 'Inter', sans-serif;
      font-size: 28px; /* Testo menu mobile */
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      opacity: 0.8;
      transition: opacity 0.2s ease, transform 0.2s ease;
    }

    .mobile-nav-link:hover {
      opacity: 1;
      transform: scale(1.05);
    }

    /* Indicazione dello stato attivo (Home o altre sezioni) */
    .mobile-nav-link.active {
      font-weight: 700; /* Testo in grassetto */
      opacity: 1; /* Piena opacità */
      border-bottom: 2.2px solid #FFFFFF; /* Linea bianca sotto */
      padding-bottom: 4px; /* Distanza tra linea e testo */
    }'''

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # We want to replace everything starting from an optional comment before .mobile-menu-overlay
    # up to the end of the mobile menu overlay CSS block.
    
    # regex to find .mobile-menu-overlay block and all following related blocks
    # we know they end with .mobile-nav-link:hover or .mobile-nav-link.active
    
    pattern = re.compile(r'(?:/\*.*?\*/\s*)?\.mobile-menu-overlay\s*\{.*?(?:\.mobile-nav-link\.active\s*\{[^\}]+\}|\.mobile-nav-link:hover(?:,\s*\.mobile-nav-link\.active)?\s*\{[^\}]+\})', re.DOTALL)
    
    if pattern.search(content):
        content = pattern.sub(css_block, content, count=1)
    else:
        print(f"Pattern not found in {f}")

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
        
print('Done!')
