# Replit configuration for AtriuumCoverUploader
# This file enables Playwright and browser dependencies on Replit

{ pkgs }: {
  deps = [
    pkgs.nodejs-18_x
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.python3Packages.virtualenv
    
    # Browser dependencies for Playwright
    pkgs.chromium
    pkgs.chromedriver
    pkgs.firefox
    pkgs.geckodriver
    pkgs.webkitgtk
    
    # System dependencies
    pkgs.which
    pkgs.gnused
    pkgs.gnutar
    pkgs.gzip
    pkgs.xorg.libxshmfence
  ];

  env = {
    PYTHONPATH = "";
    PLAYWRIGHT_BROWSERS_PATH = "${pkgs.chromium}/bin/chromium:${pkgs.firefox}/bin/firefox:${pkgs.webkitgtk}/bin/webkit";
  };

  # Post-install script to set up Playwright browsers
  run = ''
    python -m pip install -r requirements.txt
    python -m playwright install --with-deps chromium
    echo "Replit environment configured for browser automation"
  '';
}