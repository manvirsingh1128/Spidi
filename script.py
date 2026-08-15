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
    
    # We want to replace everything from /* Mobile Menu Overlay... up to the end of the mobile menu overlay CSS block.
    # We will search for a regex pattern that matches the old block.
    pattern = re.compile(r'\s*/\*\s*Mobile Menu Overlay.*?\.mobile-nav-link\.active\s*\{[^}]+\}', re.DOTALL)
    
    # Fallback pattern if the active class wasn't explicitly defined at the end like that:
    pattern2 = re.compile(r'\s*/\*\s*Mobile Menu Overlay.*?\.mobile-nav-link:hover(?:,\s*\.mobile-nav-link\.active)?\s*\{[^}]+\}', re.DOTALL)
    
    # Try pattern 2 for the current spidi-costruzioni.html style
    content = pattern.sub('\n' + css_block, content)
    content = pattern2.sub('\n' + css_block, content)

    # Let's fix the HTML structure for the mobile menu nav links
    # The list should be:
    # Home, Servizi, Galleria, Contatti, Chi siamo
    
    # First extract the mobile-menu-nav block
    nav_pattern = re.compile(r'(<nav class="mobile-menu-nav">)(.*?)(</nav>)', re.DOTALL)
    
    match = nav_pattern.search(content)
    if match:
        nav_start = match.group(1)
        nav_content = match.group(2)
        nav_end = match.group(3)
        
        # We need to construct the new nav content
        # We can extract the links to know the exact href and text
        links = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', nav_content, re.IGNORECASE)
        
        # Determine the current page to set the active class
        # f is the current filename
        
        new_nav_content = "\n"
        
        # Expected ordered URLs
        expected_links = [
            ('spidi-costruzioni.html', 'Home'),
            ('servizi.html', 'Servizi'),
            ('galleria.html', 'Galleria'),
            ('contatti.html', 'Contatti'),
            ('chi-siamo.html', 'Chi siamo')
        ]
        
        for url, text in expected_links:
            active_class = " active" if url == f else ""
            new_nav_content += f'      <a href="{url}" class="mobile-nav-link{active_class}">{text}</a>\n'
            
        content = content[:match.start()] + nav_start + new_nav_content + "    " + nav_end + content[match.end():]
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
        
print('Done!')
