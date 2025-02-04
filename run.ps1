# Install dependencies
pip install -r requirements.txt | Out-Null

# Check argument and execute the appropriate script
if ($args[0] -eq "-b") {
    python exec-bot.py
} else {
    python exec.py
}
